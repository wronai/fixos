"""
FixOrchestrator – główna pętla egzekucji napraw.
Zarządza grafem problemów, re-diagnozą po każdym kroku i eskalacją.
"""

from __future__ import annotations

import asyncio
import json
import time
import uuid
from typing import Optional

from ..config import FixOsConfig
from ..providers.llm import LLMClient, LLMError
from ..utils.anonymizer import anonymize
from ..utils.terminal import (
    _C, console, print_problem_header, print_cmd_block,
    print_stdout_box, print_stderr_box, render_tree_colored,
)
from .executor import CommandExecutor, ExecutionResult, DangerousCommandError, CommandTimeoutError
from .graph import Problem, ProblemGraph, ProblemSeverity


class _SkipAll(Exception):
    """Rzucany gdy user wpisuje 's' – pomija wszystkie komendy bieżącego problemu."""


DIAGNOSE_PROMPT = """\
You are a Linux system repair assistant. Analyze the diagnostic data and identify problems.

System info: {os_info}
Known problems already in graph: {known_problems}
Diagnostic data (anonymized):
{diagnostic_data}

Return ONLY valid JSON (no markdown, no explanation outside JSON):
{{
  "new_problems": [
    {{
      "id": "p_<short_slug>",
      "description": "...",
      "severity": "critical|warning|info",
      "fix_commands": ["cmd1", "cmd2"],
      "related_to": []
    }}
  ],
  "explanation": "..."
}}
"""

EVALUATE_PROMPT = """\
You are a Linux system repair assistant. Evaluate the result of a fix attempt.

Problem that was fixed:
{problem}

Fix command executed: {command}
Return code: {returncode}
Stdout (anonymized): {stdout}
Stderr (anonymized): {stderr}

Based on the output, did the fix succeed? Are there any new problems discovered?

Return ONLY valid JSON:
{{
  "verdict": "resolved|failed|partial",
  "confidence": 0.0,
  "new_problems": [
    {{
      "id": "p_<short_slug>",
      "description": "...",
      "severity": "critical|warning|info",
      "fix_commands": ["cmd1"],
      "related_to": ["{problem_id}"]
    }}
  ],
  "explanation": "..."
}}
"""


class FixOrchestrator:
    """
    Orkiestrator napraw systemowych.
    
    Tryby:
    - hitl: każda komenda wymaga potwierdzenia użytkownika
    - autonomous: automatyczne wykonanie gdy confidence > threshold
    """

    def __init__(
        self,
        config: FixOsConfig,
        executor: Optional[CommandExecutor] = None,
        auto_confirm_threshold: float = 0.90,
    ):
        self.config = config
        self.llm = LLMClient(config)
        self.executor = executor or CommandExecutor(
            default_timeout=120,
            require_confirmation=(config.agent_mode == "hitl"),
            dry_run=False,
        )
        self.graph = ProblemGraph()
        self.session_log: list[dict] = []
        self.auto_confirm_threshold = auto_confirm_threshold
        self._start_time = time.time()

    # ── Public API ─────────────────────────────────────────────────────────

    def load_from_diagnostics(self, diagnostics: dict) -> list[Problem]:
        """Parsuje dane diagnostyczne przez LLM i buduje graf problemów."""
        anon_str, _ = anonymize(str(diagnostics))
        os_info_raw = diagnostics.get("system", {}).get("os_release", "Linux")
        os_info, _ = anonymize(os_info_raw)

        known = [p.to_summary() for p in self.graph.nodes.values()]

        prompt = DIAGNOSE_PROMPT.format(
            os_info=os_info,
            known_problems=json.dumps(known, ensure_ascii=False),
            diagnostic_data=anon_str[:6000],
        )

        try:
            raw = self.llm.chat(
                [{"role": "user", "content": prompt}],
                max_tokens=2000,
                temperature=0.1,
            )
            data = self._parse_json(raw)
            problems = []
            for pd in data.get("new_problems", []):
                p = Problem(
                    id=pd.get("id") or f"p_{uuid.uuid4().hex[:6]}",
                    description=pd.get("description", "Nieznany problem"),
                    severity=pd.get("severity", "warning"),
                    fix_commands=pd.get("fix_commands", []),
                    caused_by=pd.get("related_to", []),
                )
                self.graph.add(p)
                problems.append(p)
            self._log("diagnose", {"found": len(problems), "explanation": data.get("explanation", "")})
            return problems
        except (LLMError, ValueError) as e:
            self._log("diagnose_error", {"error": str(e)})
            return []

    def load_from_dict(self, problems_data: list[dict]) -> list[Problem]:
        """Ładuje problemy bezpośrednio z listy dict (bez LLM)."""
        problems = []
        for pd in problems_data:
            p = Problem(
                id=pd.get("id") or f"p_{uuid.uuid4().hex[:6]}",
                description=pd["description"],
                severity=pd.get("severity", "warning"),
                fix_commands=pd.get("fix_commands", []),
                caused_by=pd.get("caused_by", []),
            )
            self.graph.add(p)
            problems.append(p)
        return problems

    def run_sync(
        self,
        confirm_fn=None,
        progress_fn=None,
    ) -> dict:
        """
        Synchroniczna pętla napraw (dla trybu HITL).
        
        Args:
            confirm_fn: callable(problem, command) -> bool – pytaj użytkownika
            progress_fn: callable(problem, result) – callback po każdym kroku
        """
        if confirm_fn is None:
            confirm_fn = self._default_confirm
        if progress_fn is None:
            progress_fn = self._default_progress

        max_iterations = 50
        iteration = 0

        while not self.graph.all_done() and iteration < max_iterations:
            iteration += 1
            problem = self.graph.next_actionable()
            if problem is None:
                break

            problem.status = "in_progress"
            problem.attempts += 1

            # Wykonaj każdą komendę fix
            last_result = None
            skip_all = False
            for cmd in problem.fix_commands:
                try:
                    if not confirm_fn(problem, cmd):
                        problem.status = "skipped"
                        self._log("skipped", {"problem_id": problem.id, "command": cmd})
                        break
                except _SkipAll:
                    skip_all = True
                    problem.status = "skipped"
                    self._log("skipped_all", {"problem_id": problem.id})
                    break

                if skip_all:
                    break

                try:
                    result = self.executor.execute_sync(cmd)
                    last_result = result
                    self._log("executed", result.to_context())
                    progress_fn(problem, result)

                    if not result.success and result.executed:
                        break
                except DangerousCommandError as e:
                    console.print(f"\n  [bold red]⛔ ZABLOKOWANO:[/bold red] {e}")
                    problem.status = "failed"
                    self._log("dangerous_blocked", {"command": cmd, "error": str(e)})
                    break
                except CommandTimeoutError as e:
                    console.print(f"\n  [bold yellow]⏰ TIMEOUT:[/bold yellow] {e}")
                    last_result = ExecutionResult(command=cmd, timed_out=True, executed=False)
                    break

            if skip_all:
                continue

            # Oceń wynik przez LLM i wykryj nowe problemy
            if last_result is not None:
                new_problems = self._evaluate_and_rediagnose(problem, last_result)
                for np in new_problems:
                    np.caused_by.append(problem.id)
                    problem.may_cause.append(np.id)
                    self.graph.add(np)
                    console.print(f"\n  [cyan]Odkryto nowy problem:[/cyan] [{np.id}] {np.description}")

        return self._session_summary()

    async def run_async(self, confirm_fn=None, progress_fn=None) -> dict:
        """Asynchroniczna wersja run_sync."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, lambda: self.run_sync(confirm_fn, progress_fn)
        )

    # ── Private helpers ────────────────────────────────────────────────────

    def _evaluate_and_rediagnose(
        self, problem: Problem, result: ExecutionResult
    ) -> list[Problem]:
        """Wysyła wynik do LLM, ocenia sukces i wykrywa nowe problemy."""
        anon_stdout, _ = anonymize(result.stdout)
        anon_stderr, _ = anonymize(result.stderr)

        prompt = EVALUATE_PROMPT.format(
            problem=json.dumps(problem.to_summary(), ensure_ascii=False),
            command=result.command,
            returncode=result.returncode,
            stdout=anon_stdout[:1500],
            stderr=anon_stderr[:500],
            problem_id=problem.id,
        )

        try:
            raw = self.llm.chat(
                [{"role": "user", "content": prompt}],
                max_tokens=1000,
                temperature=0.1,
            )
            data = self._parse_json(raw)
            verdict = data.get("verdict", "failed")
            confidence = float(data.get("confidence", 0.5))

            if verdict == "resolved" or (verdict == "partial" and confidence >= self.auto_confirm_threshold):
                problem.status = "resolved"
            elif problem.attempts >= problem.max_attempts:
                problem.status = "failed"
            else:
                problem.status = "pending"

            self._log("evaluate", {
                "problem_id": problem.id,
                "verdict": verdict,
                "confidence": confidence,
                "explanation": data.get("explanation", ""),
            })

            new_problems = []
            for pd in data.get("new_problems", []):
                p = Problem(
                    id=pd.get("id") or f"p_{uuid.uuid4().hex[:6]}",
                    description=pd.get("description", "Nieznany problem"),
                    severity=pd.get("severity", "warning"),
                    fix_commands=pd.get("fix_commands", []),
                    caused_by=pd.get("related_to", []),
                )
                new_problems.append(p)
            return new_problems

        except (LLMError, ValueError) as e:
            self._log("evaluate_error", {"error": str(e)})
            # Fallback: oceniaj po returncode
            if result.success:
                problem.status = "resolved"
            elif problem.attempts >= problem.max_attempts:
                problem.status = "failed"
            else:
                problem.status = "pending"
            return []

    def _parse_json(self, raw: str) -> dict:
        """Parsuje JSON z odpowiedzi LLM (usuwa markdown code fences)."""
        text = raw.strip()
        # Usuń ```json ... ``` jeśli obecne
        if text.startswith("```"):
            lines = text.splitlines()
            text = "\n".join(
                line for line in lines
                if not line.strip().startswith("```")
            )
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            # Spróbuj wyciągnąć JSON z tekstu
            import re
            m = re.search(r"\{.*\}", text, re.DOTALL)
            if m:
                return json.loads(m.group())
            raise ValueError(f"Nie można sparsować JSON z odpowiedzi LLM: {raw[:200]}")

    def _log(self, event: str, data: dict) -> None:
        self.session_log.append({
            "event": event,
            "timestamp": time.time() - self._start_time,
            **data,
        })

    def _session_summary(self) -> dict:
        summary = self.graph.summary()
        summary["elapsed_seconds"] = int(time.time() - self._start_time)
        summary["log_entries"] = len(self.session_log)
        return summary

    @staticmethod
    def _default_confirm(problem: Problem, command: str) -> bool:
        print_problem_header(
            problem.id, problem.description, problem.severity,
            status=problem.status, attempts=problem.attempts, max_attempts=problem.max_attempts,
        )
        print_cmd_block(command)
        try:
            ans = console.input(
                r"  [bold]Wykonać?[/bold] [green]\[Y][/green]es / "
                r"[red]\[n][/red]o / [yellow]\[s][/yellow]kip all: "
            ).strip().lower()
        except (EOFError, KeyboardInterrupt):
            return False
        if ans in ("s", "skip", "skip all"):
            raise _SkipAll()
        return ans in ("y", "yes", "")

    @staticmethod
    def _default_progress(problem: Problem, result: ExecutionResult) -> None:
        if not result.executed:
            console.print(f"\n  [dim yellow]⏭️  DRY-RUN:[/dim yellow] [cyan]`{result.command}`[/cyan]")
            if result.preview:
                console.print(f"  [dim]{result.preview}[/dim]")
            return
        console.print()
        if result.success:
            console.print(f"  [bold green]OK[/bold green]  [cyan]`{result.command}`[/cyan]")
        else:
            console.print(f"  [bold red]kod {result.returncode}[/bold red]  [cyan]`{result.command}`[/cyan]")
        if result.stdout and not result.stdout.startswith("(już wykonane"):
            print_stdout_box(result.stdout)
        if result.stderr and not result.success:
            print_stderr_box(result.stderr)
