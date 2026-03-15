"""
Tryb autonomiczny – agent sam diagnozuje i naprawia system.
Wymaga jawnego włączenia: --mode autonomous lub AGENT_MODE=autonomous
Posiada mechanizmy bezpieczeństwa i limity.
"""

from __future__ import annotations

import re
import signal
import subprocess
import time
from dataclasses import dataclass, field
from typing import Optional

from ..providers.llm import LLMClient, LLMError
from ..utils.anonymizer import anonymize, display_anonymized_preview
from ..utils.web_search import search_all, format_results_for_llm
from ..config import FixOsConfig


# Komendy NIGDY nie wykonywane automatycznie (bez względu na wszystko)
FORBIDDEN_COMMANDS = [
    r"rm\s+-rf\s+/",        # rm -rf /
    r"dd\s+if=",            # dd (nadpisanie dysku)
    r"mkfs\.",              # formatowanie partycji
    r":(){ :|:& };:",       # fork bomb
    r"chmod\s+-R\s+777",   # chmod 777 rekurencyjny
    r">\s+/dev/sd",        # nadpisanie urządzenia blokowego
    r"fdisk|parted|gdisk", # partycjonowanie
    r"systemctl\s+disable\s+--now\s+(network|sshd|firewalld)",
    r"iptables\s+-F",      # flush reguł zapory
    r"passwd\s+root",      # zmiana hasła roota
]

# Komendy wymagające sudo (dodawane automatycznie)
SUDO_PREFIXES = [
    "dnf", "rpm", "systemctl", "firewall-cmd", "setenforce",
    "modprobe", "rmmod", "alsactl", "grub2-", "update-grub",
]

SYSTEM_PROMPT_AUTONOMOUS = """Jesteś autonomicznym agentem diagnostyki Linux, Windows, macOS.

Działasz w pętli: OBSERVE → ANALYZE → ACT → VERIFY

Protokół odpowiedzi (WYMAGANY format JSON):
{
  "analysis": "krótka analiza sytuacji",
  "severity": "critical|high|medium|low",
  "action": "EXEC|SEARCH|SKIP|DONE",
  "command": "komenda do wykonania (gdy action=EXEC)",
  "search_query": "zapytanie (gdy action=SEARCH)",
  "reason": "uzasadnienie akcji",
  "next_step": "co sprawdzimy po tej akcji"
}

Zasady:
1. Zaczynaj od najbezpieczniejszych akcji (read-only: status, list, check)
2. Wykonuj jedną komendę naraz, weryfikuj wynik przed następną
3. Nigdy nie wykonuj destrukcyjnych operacji (rm -rf, mkfs, fdisk)
4. Gdy nie masz pewności → action=SEARCH lub action=SKIP
5. Po naprawieniu problemu zweryfikuj fix (uruchom komendę sprawdzającą)
6. Zakończ gdy action=DONE lub po MAX_FIXES naprawach
"""


@dataclass
class FixAction:
    command: str
    reason: str
    result: Optional[str] = None
    success: Optional[bool] = None
    timestamp: float = field(default_factory=time.time)


@dataclass
class AgentReport:
    fixes_applied: list[FixAction] = field(default_factory=list)
    searches_done: list[str] = field(default_factory=list)
    problems_found: list[str] = field(default_factory=list)
    start_time: float = field(default_factory=time.time)

    def summary(self) -> str:
        elapsed = int(time.time() - self.start_time)
        lines = [
            f"  ⏱️  Czas: {elapsed}s",
            f"  🔧 Naprawiono: {len(self.fixes_applied)} operacji",
            f"  🔎 Wyszukiwania: {len(self.searches_done)}",
            f"  🔴 Wykryte problemy: {len(self.problems_found)}",
        ]
        if self.fixes_applied:
            lines.append("\n  Wykonane akcje:")
            for i, a in enumerate(self.fixes_applied, 1):
                icon = "✅" if a.success else "❌"
                lines.append(f"    {i}. {icon} `{a.command}`")
                lines.append(f"       Powód: {a.reason}")
        return "\n".join(lines)


from fixos.utils.timeout import SessionTimeout


def _timeout_handler(signum, frame):
    raise SessionTimeout()


def _is_forbidden(cmd: str) -> Optional[str]:
    """Zwraca opis zagrożenia jeśli komenda jest zabroniona."""
    for pattern in FORBIDDEN_COMMANDS:
        if re.search(pattern, cmd, re.IGNORECASE):
            return f"Komenda pasuje do wzorca zabronionego: {pattern}"
    return None


def _add_sudo(cmd: str) -> str:
    """Dodaje sudo jeśli komenda tego wymaga."""
    if cmd.strip().startswith("sudo"):
        return cmd
    for prefix in SUDO_PREFIXES:
        if cmd.strip().startswith(prefix):
            return "sudo " + cmd.strip()
    return cmd


def _execute(cmd: str) -> tuple[bool, str]:
    """Wykonuje komendę i zwraca (sukces, output)."""
    try:
        proc = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=90
        )
        out = proc.stdout.strip() or proc.stderr.strip() or "(brak outputu)"
        return proc.returncode == 0, out[:1000]
    except subprocess.TimeoutExpired:
        return False, "[TIMEOUT 90s]"
    except Exception as e:
        return False, f"[WYJĄTEK: {e}]"


def run_autonomous_session(
    diagnostics: dict,
    config: FixOsConfig,
    show_data: bool = True,
    max_fixes: int = 10,
):
    """
    Uruchamia autonomiczny tryb agenta.
    """
    print("\n" + "═" * 65)
    print("  ⚠️  TRYB AUTONOMICZNY – agent sam wykonuje komendy!")
    print("  Naciśnij Ctrl+C w dowolnym momencie aby przerwać.")
    print("═" * 65)
    print(f"\n  Max napraw: {max_fixes}")
    print(f"  Timeout sesji: {config.session_timeout}s")
    print(f"  Model: {config.model}")

    confirm = input("\n  Czy na pewno chcesz uruchomić tryb autonomiczny? (yes/N): ").strip()
    if confirm.lower() not in ("yes", "tak"):
        print("  Anulowano. Użyj --mode hitl dla trybu z potwierdzeniem.")
        return

    llm = LLMClient(config)
    report = AgentReport()

    # Anonimizacja
    anon_str, anon_report = anonymize(str(diagnostics))
    if show_data:
        display_anonymized_preview(anon_str, anon_report)

    # Timeout
    signal.signal(signal.SIGALRM, _timeout_handler)
    signal.alarm(config.session_timeout)
    start_ts = time.time()

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT_AUTONOMOUS},
        {
            "role": "user",
            "content": (
                f"Dane diagnostyczne system:\n```\n{anon_str}\n```\n\n"
                f"Rozpocznij analizę i naprawę. Odpowiadaj TYLKO w formacie JSON."
            ),
        },
    ]

    fix_count = 0
    search_count = 0
    MAX_SEARCHES = 3

    print("\n\n  🤖 Agent uruchomiony...\n")

    try:
        while fix_count < max_fixes:
            rem = config.session_timeout - int(time.time() - start_ts)
            if rem <= 0:
                raise SessionTimeout()

            print(f"  ⟳ Tura {fix_count + 1}/{max_fixes} | ⏰ {rem}s pozostało")

            # Zapytaj LLM
            try:
                reply = llm.chat(messages, max_tokens=1000, temperature=0.1)
                messages.append({"role": "assistant", "content": reply})
            except LLMError as e:
                print(f"  ❌ LLM błąd: {e}")
                if config.enable_web_search and search_count < MAX_SEARCHES:
                    results = search_all("fedora repair diagnostics", config.serpapi_key)
                    if results:
                        messages.append({
                            "role": "user",
                            "content": format_results_for_llm(results)
                        })
                        search_count += 1
                        continue
                break

            # Parsuj JSON z odpowiedzi
            action_data = _parse_agent_json(reply)
            if not action_data:
                print(f"  ⚠️  Nieprawidłowy format JSON, kontynuuję...")
                messages.append({
                    "role": "user",
                    "content": "Odpowiedz TYLKO w formacie JSON jak w instrukcji."
                })
                continue

            action = action_data.get("action", "SKIP")
            analysis = action_data.get("analysis", "")
            reason = action_data.get("reason", "")

            print(f"\n  📋 Analiza: {analysis}")
            print(f"  🎯 Akcja: {action} – {reason}")

            # DONE
            if action == "DONE":
                print("\n  ✅ Agent zakończył – wszystkie problemy naprawione!")
                break

            # SKIP
            if action == "SKIP":
                print(f"  ⏭️  Pomijam: {reason}")
                messages.append({
                    "role": "user",
                    "content": f"Pominięto: {reason}. Co dalej?"
                })
                fix_count += 1
                continue

            # SEARCH
            if action == "SEARCH":
                query = action_data.get("search_query", "fedora fix")
                if search_count < MAX_SEARCHES:
                    results = search_all(query, config.serpapi_key)
                    search_count += 1
                    report.searches_done.append(query)
                    if results:
                        web_ctx = format_results_for_llm(results)
                        messages.append({
                            "role": "user",
                            "content": f"Wyniki dla '{query}':\n{web_ctx}\nKontynuuj naprawę."
                        })
                    else:
                        messages.append({
                            "role": "user",
                            "content": f"Brak wyników dla '{query}'. Co innego możemy zrobić?"
                        })
                else:
                    print("  ⚠️  Limit wyszukiwań osiągnięty.")
                    messages.append({"role": "user", "content": "Brak więcej wyszukiwań. Co możemy zrobić bez zewnętrznych źródeł?"})
                continue

            # EXEC
            if action == "EXEC":
                cmd_raw = action_data.get("command", "").strip()
                if not cmd_raw:
                    messages.append({"role": "user", "content": "Brak komendy. Podaj konkretną komendę."})
                    continue

                # Sprawdzenie bezpieczeństwa
                danger = _is_forbidden(cmd_raw)
                if danger:
                    print(f"  🚫 ZABLOKOWANO: {danger}")
                    messages.append({
                        "role": "user",
                        "content": f"Komenda `{cmd_raw}` jest zabroniona: {danger}. Zaproponuj bezpieczniejszą alternatywę."
                    })
                    continue

                cmd = _add_sudo(cmd_raw)
                print(f"  ▶️  Wykonuję: {cmd}")

                ok, out = _execute(cmd)
                fix = FixAction(command=cmd, reason=reason, result=out, success=ok)
                report.fixes_applied.append(fix)
                fix_count += 1

                icon = "✅" if ok else "❌"
                print(f"  {icon} Wynik: {out[:200]}")

                # Anonimizuj komendę i output przed wysłaniem do LLM
                anon_out, _ = anonymize(out)
                anon_cmd, _ = anonymize(cmd)

                messages.append({
                    "role": "user",
                    "content": (
                        f"Wykonano: `{anon_cmd}`\n"
                        f"Sukces: {ok}\n"
                        f"Output: {anon_out[:500]}\n"
                        f"Zweryfikuj wynik i zaproponuj następną akcję."
                    ),
                })

            time.sleep(1)  # Krótka pauza między akcjami

    except SessionTimeout:
        print(f"\n  ⏰ Timeout sesji.")
    except KeyboardInterrupt:
        print(f"\n\n  ⛔ Przerwano przez użytkownika (Ctrl+C).")
    finally:
        signal.alarm(0)

    print(f"\n{'═' * 65}")
    print("  📊 RAPORT SESJI AUTONOMICZNEJ")
    print("═" * 65)
    print(report.summary())
    print("═" * 65 + "\n")
    return report


def _parse_agent_json(text: str) -> Optional[dict]:
    """Wyciąga JSON z odpowiedzi LLM (nawet jeśli zawiera dodatkowy tekst)."""
    import json
    # Szukaj bloku ```json ... ``` lub bezpośrednio {...}
    patterns = [
        r"```(?:json)?\s*(\{.*?\})\s*```",
        r"(\{[^{}]*\"action\"[^{}]*\})",
    ]
    for pattern in patterns:
        m = re.search(pattern, text, re.DOTALL)
        if m:
            try:
                return json.loads(m.group(1))
            except json.JSONDecodeError:
                pass
    # Próba całego tekstu jako JSON
    try:
        return json.loads(text.strip())
    except json.JSONDecodeError:
        return None
