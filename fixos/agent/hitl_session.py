"""
Human-in-the-Loop (HITL) Session for fixOS Agent
Interactive session where user approves each action.
"""

import re
import time
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Any

# Constants for UI formatting and timeouts
MAX_SUMMARY_LENGTH = 80
MAX_STDOUT_LINES = 40
DEFAULT_COMMAND_TIMEOUT = 120

from ..providers.llm import LLMClient, LLMError
from ..utils.anonymizer import anonymize, display_anonymized_preview
from ..utils.web_search import search_all, format_results_for_llm
from ..utils.terminal import (
    _C, render_md as _render_md, console,
    print_cmd_block as _print_cmd_block_rich,
    print_stdout_box, print_stderr_box,
)
from rich.text import Text
from ..config import FixOsConfig
from ..platform_utils import (
    is_dangerous, elevate_cmd, run_command,
    setup_signal_timeout, cancel_signal_timeout,
    get_os_info, get_package_manager,
)
from ..utils.timeout import SessionTimeout


SYSTEM_PROMPT = """You are an expert Linux/Windows/macOS system diagnostics assistant.

You receive anonymized diagnostic data OR a user-described problem. Your tasks:

1. DIAGNOSE – identify ALL problems (🔴 critical → 🟡 important → 🟢 minor)
2. SOLUTIONS – for each problem provide a CONCRETE command with a brief explanation
3. FORMAT – always use this exact format:

━━━ DIAGNOZA ━━━
🔴 Problem 1: [description]
   **Komenda:** `command to run`
   **Co robi:** one-sentence explanation

🟡 Problem 2: [description]
   **Komenda:** `command`
   **Co robi:** explanation

Always end with:
━━━ DOSTĘPNE AKCJE ━━━
[1] Fix problem 1 – `command`
[2] Fix problem 2 – `command`
[A] Fix all automatically
[S] Skip all
[D] Describe a new problem
[Q] End session

IMPORTANT: Adapt commands to the detected OS (Linux/Windows/macOS).
"""


@dataclass
class CmdResult:
    cmd: str
    comment: str
    ok: bool
    stdout: str
    stderr: str
    returncode: int
    skipped: bool = False
    timestamp: float = field(default_factory=time.time)


class HITLSession:
    """Interactive Human-in-the-Loop diagnostic and repair session."""

    MAX_WEB_SEARCHES = 3

    def __init__(
        self,
        diagnostics: Dict[str, Any],
        config: FixOsConfig,
        show_data: bool = True,
    ):
        self.diagnostics = diagnostics
        self.config = config
        self.show_data = show_data
        self.llm = LLMClient(config)
        self.os_info = get_os_info()
        self.pkg_manager = get_package_manager() or "unknown"
        self.messages: List[Dict[str, str]] = []
        self.executed: List[CmdResult] = []
        self.web_search_count = 0
        self.last_fixes: List[Tuple[str, str]] = []
        self.start_ts = time.time()
        self._setup_timeout()

    def _setup_timeout(self):
        """Setup session timeout handler."""
        def _timeout(signum, frame):
            raise SessionTimeout()
        setup_signal_timeout(self.config.session_timeout, _timeout)

    def _clear_timeout(self):
        """Clear the timeout alarm."""
        cancel_signal_timeout()

    def remaining(self) -> int:
        """Get remaining session time in seconds."""
        from . import get_remaining_time
        return get_remaining_time(self)

    @staticmethod
    def fmt_time(s: int) -> str:
        """Format seconds as HH:MM:SS."""
        return f"{s//3600:02d}:{(s%3600)//60:02d}:{s%60:02d}"

    def _initialize_messages(self) -> bool:
        """Initialize LLM message history with system prompt and diagnostics.
        
        Returns False if user rejects sending data.
        """
        anon_str, report = anonymize(str(self.diagnostics))

        if self.show_data:
            display_anonymized_preview(anon_str, report)
            ans = console.input("\n  Czy wysłać te dane do LLM? \\[Y/n]: ").strip().lower()
            if ans in ("n", "no", "nie"):
                console.print("  Anulowano.")
                return False

        self.messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    f"OS: {self.os_info['system']} {self.os_info['release']} | "
                    f"Package manager: {self.pkg_manager}\n\n"
                    f"Anonymized diagnostic data:\n```\n{anon_str}\n```\n\n"
                    f"Perform full analysis and list all detected problems."
                ),
            },
        ]
        return True

    def _print_header(self):
        """Print session header with system info."""
        from rich.panel import Panel

        header = Text()
        header.append(f"👤 HUMAN-IN-THE-LOOP  |  Model: {self.config.model}\n", style="bold cyan")
        header.append(f"🖥️  OS: {self.os_info['system']} {self.os_info['release']}  |  PM: {self.pkg_manager}\n", style="cyan")
        header.append(f"⏰ Sesja: max {self.fmt_time(self.config.session_timeout)}", style="dim")
        console.print()
        console.print(Panel(header, border_style="cyan"))

    @staticmethod
    def _extract_fixes(reply: str) -> List[Tuple[str, str]]:
        """Extract (command, comment) pairs from LLM reply."""
        fixes: List[Tuple[str, str]] = []
        for m in re.finditer(
            r"\*\*Komenda:\*\*\s*`([^`]+)`(?:[^\n]*?\*\*Co robi:\*\*\s*(.+?))?(?=\n|$)",
            reply, re.IGNORECASE,
        ):
            cmd = m.group(1).strip()
            if cmd:
                fixes.append((cmd, (m.group(2) or "").strip()))
        if not fixes:
            for m in re.finditer(r"→\s*Fix:\s*`([^`]+)`", reply, re.IGNORECASE):
                fixes.append((m.group(1).strip(), ""))
        if not fixes:
            for m in re.finditer(r"\[(\d+)\][^`\n]+`([^`]+)`", reply):
                fixes.append((m.group(2).strip(), f"Fix #{m.group(1)}"))
        if not fixes:
            for m in re.finditer(r"EXEC:\s*`([^`]+)`", reply, re.IGNORECASE):
                fixes.append((m.group(1).strip(), ""))
        return fixes

    def _extract_search_topic(self, llm_reply: str) -> str:
        """Extract search keywords from LLM reply."""
        tech_terms = re.findall(
            r"\b(sof-firmware|pipewire|alsa|thumbnails?|nautilus|"
            r"dnf|apt|systemctl|journalctl|codec|driver|nvidia|amd|"
            r"snd_hda|intel_sst|avs|wireplumber|pulseaudio|bluetooth|wifi)\b",
            llm_reply, re.IGNORECASE
        )
        if tech_terms:
            return " ".join(dict.fromkeys(tech_terms[:4]))
        first_sentence = llm_reply.split(".")[0][:MAX_SUMMARY_LENGTH]
        return first_sentence or "linux system diagnostics"

    def _print_action_menu(self):
        """Print the interactive numbered action menu."""
        from rich.rule import Rule
        from rich.syntax import Syntax

        console.print()
        console.print(Rule(
            f"[bold cyan]📋 DOSTĘPNE AKCJE[/bold cyan]  [dim]⏰ {self.fmt_time(self.remaining())}  ~{self.llm.total_tokens} tokenów[/dim]",
            style="cyan",
        ))
        if self.last_fixes:
            for i, (cmd, comment) in enumerate(self.last_fixes, 1):
                label = comment if comment else (cmd[:55] + "..." if len(cmd) > 55 else cmd)
                console.print(f"  [bold yellow][{i}][/bold yellow] {label}")
                console.print(Panel(
                    Syntax(cmd, "bash", theme="monokai", word_wrap=True),
                    border_style="dim cyan",
                    padding=(0, 1),
                ))
            console.print()
            console.print(f"  [bold yellow][A][/bold yellow]  Wykonaj wszystkie ({len(self.last_fixes)} komend)")
            console.print(f"  [bold yellow][S][/bold yellow]  Pomiń wszystkie")
        else:
            console.print("  [dim](brak zaproponowanych komend)[/dim]")
        console.print()
        console.print(f"  [bold yellow][D][/bold yellow]           Opisz własny problem / co chcesz zmienić")
        console.print(f"  [bold yellow][!cmd][/bold yellow]        Wykonaj własną komendę")
        console.print(f"  [bold yellow][search <q>][/bold yellow]  Szukaj zewnętrznie")
        console.print(f"  [bold yellow][?][/bold yellow]           Zapytaj o więcej szczegółów")
        console.print(f"  [bold yellow][Q][/bold yellow]           Zakończ sesję")
        console.print(Rule(style="cyan"))

    def _ask_user_problem(self) -> str:
        """Interactively asks the user to describe their problem."""
        body = Text()
        body.append("Napisz co chcesz naprawić, zmienić lub co nie działa.\n", style="white")
        body.append("Możesz pisać po polsku lub angielsku.\n\n", style="dim")
        body.append("Przykłady:\n", style="bold cyan")
        body.append(
            "  - 'brak dźwięku po aktualizacji'\n"
            "  - 'chcę przyspieszyć uruchamianie systemu'\n"
            "  - 'wifi nie działa po uśpieniu'\n"
            "  - 'chcę zainstalować sterowniki NVIDIA'\n"
            "  - 'dysk jest prawie pełny, co usunąć'\n"
            "  - 'jak skonfigurować firewall'",
            style="dim",
        )
        console.print()
        console.print(Panel(body, title="[bold cyan]💬 OPISZ SWÓJ PROBLEM[/bold cyan]", border_style="cyan"))
        try:
            return console.input("  [bold cyan]Twój problem:[/bold cyan] ").strip()
        except (EOFError, KeyboardInterrupt):
            return ""

    def _print_cmd_preview(self, cmd: str, comment: str = ""):
        """Shows command in a clear block before execution."""
        _print_cmd_block_rich(cmd, comment=comment)

    def _print_cmd_result(self, result: CmdResult):
        """Shows command result with colorized markdown."""
        if result.skipped:
            console.print(Text(f"⏭️  Pominięto: `{result.cmd}`", style="dim"))
            return

        if result.ok:
            console.print(Text(f"✅  {result.cmd}", style="bold green"))
        else:
            console.print(Text(f"❌  (kod {result.returncode})  {result.cmd}", style="bold red"))

        if result.stdout.strip():
            print_stdout_box(result.stdout, max_lines=MAX_STDOUT_LINES)
        elif not result.ok and not result.stderr.strip():
            console.print("[dim](brak stdout)[/dim]")

        if result.stderr.strip() and not result.ok:
            print_stderr_box(result.stderr)
        console.print()

    def _run_cmd(self, cmd: str, comment: str = "") -> CmdResult:
        """Runs a command with full transparency and markdown output."""
        cmd = elevate_cmd(cmd)
        danger = is_dangerous(cmd)
        if danger:
            console.print(f"\n  [bold red]⛔ ZABLOKOWANO:[/bold red] {danger}")
            console.print(f"  Komenda: [cyan]`{cmd}`[/cyan]")
            return CmdResult(cmd=cmd, comment=comment, ok=False,
                             stdout="", stderr=f"Zablokowano: {danger}", returncode=-99)
        self._print_cmd_preview(cmd, comment)
        ans = console.input("  [bold]Wykonać?[/bold] \\[Y/n]: ").strip().lower()
        if ans in ("n", "no", "nie"):
            return CmdResult(cmd=cmd, comment=comment, ok=False,
                             stdout="", stderr="Pominięto.", returncode=-1, skipped=True)
        console.print("  [dim]⏳ Wykonuję...[/dim]", end="")
        ok, stdout, stderr, rc = run_command(cmd, timeout=DEFAULT_COMMAND_TIMEOUT)
        console.print("\r" + " " * 30 + "\r", end="")
        result = CmdResult(cmd=cmd, comment=comment, ok=ok,
                           stdout=stdout, stderr=stderr, returncode=rc)
        self._print_cmd_result(result)
        return result

    def _handle_llm_error(self) -> bool:
        """Handle LLM error - try web search if enabled."""
        if self.config.enable_web_search and self.web_search_count < self.MAX_WEB_SEARCHES:
            self.web_search_count += 1
            console.print("  [yellow]🔎 Szukam zewnętrznie...[/yellow]")
            results = search_all("linux system diagnostics repair", self.config.serpapi_key)
            if results:
                console.print(format_results_for_llm(results))
                return True
        return False

    def _check_low_confidence(self, reply: str) -> bool:
        """Check if LLM is uncertain and perform web search if enabled."""
        low_conf = any(p in reply.lower() for p in [
            "nie wiem", "nie jestem pewien", "i don't know",
            "not sure", "cannot determine",
        ])
        if low_conf and self.config.enable_web_search and self.web_search_count < self.MAX_WEB_SEARCHES:
            if console.input("\n  [dim]💡 LLM niepewny – szukać zewnętrznie? [y/N]:[/dim] ").strip().lower() in ("y", "yes", "tak"):
                self.web_search_count += 1
                topic = self._extract_search_topic(reply)
                results = search_all(topic, self.config.serpapi_key)
                if results:
                    web_ctx = format_results_for_llm(results)
                    console.print(web_ctx)
                    self.messages.append({"role": "user",
                                     "content": f"External sources:\n{web_ctx}\nUpdate analysis."})
                    return True
        return False

    def _process_turn(self) -> bool:
        """Process one turn of the HITL session.

        Returns False to exit loop, True to continue.
        """
        from rich.rule import Rule

        rem = self.remaining()
        if rem <= 0:
            raise SessionTimeout()

        console.print(f"\n  [dim]🧠 Analizuję...[/dim]", end="")
        try:
            reply = self.llm.chat(self.messages, max_tokens=2500, temperature=0.2)
            self.messages.append({"role": "assistant", "content": reply})
        except LLMError as e:
            console.print(f"\n  [bold red]❌ Błąd LLM:[/bold red] {e}")
            if not self._handle_llm_error():
                return False
            return True
        console.print("\r" + " " * 30 + "\r", end="")

        console.print(Rule(style="dim cyan"))
        _render_md(reply)
        console.print(Rule(style="dim cyan"))

        self.last_fixes = self._extract_fixes(reply)

        if self._check_low_confidence(reply):
            return True

        self._print_action_menu()

        try:
            user_in = console.input(f"\n  [bold cyan]fixos [{self.fmt_time(rem)}] ❯[/bold cyan] ").strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\n  Sesja przerwana.")
            return False

        if not user_in:
            return True

        lo = user_in.lower()

        # [Q] Quit
        if lo in ("q", "quit", "exit", "koniec"):
            console.print("\n  [bold green]✅ Sesja zakończona.[/bold green]")
            return False

        # [D] Describe own problem
        if lo == "d":
            problem = self._ask_user_problem()
            if problem:
                self.messages.append({
                    "role": "user",
                    "content": (
                        f"User describes a new problem:\n"
                        f"{problem}\n\n"
                        f"Analyze this problem and provide numbered list of commands to fix it."
                    ),
                })
            return True

        # [S] Skip all
        if lo in ("s", "skip", "pomiń", "pomin"):
            self.messages.append({"role": "user",
                              "content": "Skip these fixes. What else can we check?"})
            return True

        # [A] Execute all
        if lo in ("a", "all", "wszystkie"):
            if not self.last_fixes:
                console.print("  [dim]Brak komend do wykonania.[/dim]")
                return True
            console.print(f"\n  [bold cyan]▶️  Wykonuję wszystkie {len(self.last_fixes)} komend...[/bold cyan]\n")
            summary_lines = []
            for cmd, comment in self.last_fixes:
                result = self._run_cmd(cmd, comment)
                self.executed.append(result)
                anon_out, _ = anonymize(result.stdout + result.stderr)
                status = "✅ sukces" if result.ok else f"❌ błąd (kod {result.returncode})"
                summary_lines.append(f"- `{cmd}`: {status}")
            self.messages.append({
                "role": "user",
                "content": (
                    f"Executed all commands:\n"
                    f"{'\n'.join(summary_lines)}\n"
                    f"\nEvaluate results and suggest next steps."
                ),
            })
            return True

        # [N] Execute specific fix by number
        if user_in.isdigit():
            idx = int(user_in) - 1
            if 0 <= idx < len(self.last_fixes):
                cmd, comment = self.last_fixes[idx]
                result = self._run_cmd(cmd, comment)
                self.executed.append(result)
                anon_out, _ = anonymize(result.stdout)
                anon_err, _ = anonymize(result.stderr)
                self.messages.append({
                    "role": "user",
                    "content": (
                        f"Executed: `{cmd}`\n"
                        f"Success: {result.ok}\n"
                        f"Stdout:\n```\n{anon_out[:800]}\n```\n"
                        f"Stderr:\n```\n{anon_err[:300]}\n```\n"
                        f"What next?"
                    ),
                })
            else:
                console.print(f"  [yellow]Brak opcji [{user_in}]. Dostępne: 1–{len(self.last_fixes)}[/yellow]")
            return True

        # [!cmd] Direct command execution
        if user_in.startswith("!"):
            cmd = user_in[1:].strip()
            result = self._run_cmd(cmd, "Komenda użytkownika")
            self.executed.append(result)
            anon_out, _ = anonymize(result.stdout + "\n" + result.stderr)
            self.messages.append({
                "role": "user",
                "content": f"User ran: `{cmd}`\nResult: {anon_out[:600]}\nWhat next?"
            })
            return True

        # [search <q>] Web search
        if lo.startswith("search "):
            query = user_in[7:].strip()
            results = search_all(query, self.config.serpapi_key)
            if results:
                web_ctx = format_results_for_llm(results)
                console.print(web_ctx)
                self.messages.append({
                    "role": "user",
                    "content": f"Search results for '{query}':\n{web_ctx}\nWhat do you think?"
                })
            else:
                console.print("  [dim]Brak wyników.[/dim]")
            return True

        # Free text → send to LLM
        self.messages.append({"role": "user", "content": user_in})
        return True

    def run(self) -> None:
        """Run the HITL session."""
        if not self._initialize_messages():
            return
        self._print_header()

        try:
            while True:
                should_continue = self._process_turn()
                if not should_continue:
                    break
        except SessionTimeout:
            console.print(f"\n\n  [bold yellow]⏰ Sesja wygasła (limit: {self.fmt_time(self.config.session_timeout)}).[/bold yellow]")
        finally:
            self._clear_timeout()

        self._print_summary()

    def _print_summary(self):
        """Print session summary."""
        elapsed = int(time.time() - self.start_ts)
        ok_count = sum(1 for r in self.executed if r.ok)
        console.print(
            f"\n  [bold cyan]📊 Sesja:[/bold cyan] {len(self.messages)-2} tur | {self.fmt_time(elapsed)} | "
            f"~{self.llm.total_tokens} tokenów | [green]{ok_count}[/green]/[red]{len(self.executed)}[/red] komend OK"
        )


def run_hitl_session(
    diagnostics: Dict[str, Any],
    config: FixOsConfig,
    show_data: bool = True,
) -> None:
    """Run interactive HITL session (backward compatible wrapper)."""
    session = HITLSession(
        diagnostics=diagnostics,
        config=config,
        show_data=show_data,
    )
    session.run()
