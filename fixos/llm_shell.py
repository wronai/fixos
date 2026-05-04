"""
Interaktywny shell LLM do diagnostyki i naprawy systemu system.
Sesja trwa maksymalnie 1 godzinę (3600 sekund).
Dane diagnostyczne są wysyłane jawnie do modelu.
"""

import signal
import subprocess
import sys
import time
from typing import Optional

try:
    import openai
except ImportError:
    print("[BŁĄD] Zainstaluj: pip install openai")
    sys.exit(1)

try:
    from prompt_toolkit import PromptSession
    from prompt_toolkit.styles import Style
    from prompt_toolkit.formatted_text import HTML
except ImportError:
    print("[BŁĄD] Zainstaluj: pip install prompt_toolkit")
    sys.exit(1)

from .anonymizer import anonymize

# ── Stałe ──────────────────────────────────────────────────────────────────
SESSION_TIMEOUT = 3600  # 1 godzina w sekundach
SYSTEM_PROMPT = """Jesteś ekspertem od diagnostyki i naprawy systemu Linux, Windows, macOS.
Otrzymujesz anonimizowane dane diagnostyczne z systemu użytkownika.

Twoje zadania:
1. Przeanalizuj dane i zidentyfikuj WSZYSTKIE problemy (błędy, ostrzeżenia, nieaktualne pakiety, failed usługi, przepełnione dyski, etc.)
2. Przedstaw problemy jako numerowaną listę, od najpoważniejszego
3. Dla każdego problemu zaproponuj KONKRETNĄ komendę naprawczą
4. ZAWSZE pytaj o potwierdzenie przed wykonaniem jakiejkolwiek komendy
5. Informuj o ryzyku każdej operacji

Format odpowiedzi:
🔍 DIAGNOZA: [krótkie podsumowanie]

Wykryte problemy:
1. [opis] → Komenda: `<komenda>`
2. ...

Co naprawiamy? (wpisz numer, 'all', 'skip' lub 'q' aby zakończyć)"""

# ── Timeout handler ─────────────────────────────────────────────────────────
from fixos.utils.timeout import SessionTimeout

def _timeout_handler(signum, frame):
    raise SessionTimeout()


# ── Formatowanie czasu ──────────────────────────────────────────────────────
def format_time(seconds: int) -> str:
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:02d}"


# ── Bezpieczne wykonanie komendy ────────────────────────────────────────────
def execute_command(cmd: str) -> tuple[bool, str]:
    """
    Wykonuje komendę systemową z potwierdzeniem użytkownika.
    Zwraca (sukces, output).
    """
    # Komendy wymagające sudo
    dangerous_prefixes = ['dnf', 'rpm', 'systemctl', 'firewall-cmd', 'setenforce',
                          'chmod', 'chown', 'rm ', 'mv ', 'dd ', 'mkfs']
    is_dangerous = any(cmd.strip().startswith(p) for p in dangerous_prefixes)

    if is_dangerous and not cmd.strip().startswith('sudo '):
        cmd = 'sudo ' + cmd.strip()

    print(f"\n  [exec] {cmd}")
    confirm = input("  Potwierdź wykonanie (Y/n): ").strip().lower()
    if confirm not in ('y', 'yes', ''):
        return False, "Anulowano przez użytkownika."

    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=120
        )
        output = result.stdout.strip() or result.stderr.strip() or "(brak outputu)"
        success = result.returncode == 0
        status = "✅ Sukces" if success else f"❌ Błąd (kod {result.returncode})"
        print(f"  {status}")
        return success, output
    except subprocess.TimeoutExpired:
        return False, "Komenda przekroczyła limit czasu (120s)."
    except Exception as e:
        return False, f"Wyjątek: {e}"


# ── Główna funkcja sesji LLM ────────────────────────────────────────────────
def _llm_call(client, model: str, messages: list) -> Optional[str]:
    """Call the LLM; return reply text, '' on rate-limit, None on fatal error."""
    try:
        response = client.chat.completions.create(
            model=model, messages=messages, max_tokens=2000, temperature=0.3,
        )
        return response.choices[0].message.content
    except openai.AuthenticationError:
        print("\n❌ Błąd autoryzacji – sprawdź token API.")
        return None
    except openai.RateLimitError:
        print("\n⚠️ Rate limit – poczekaj chwilę...")
        time.sleep(10)
        return ""
    except Exception as e:
        print(f"\n❌ Błąd API: {e}")
        return None


def _handle_user_turn(session, messages: list, remaining: int, verbose: bool) -> str:
    """Read user input, update messages. Returns 'quit', 'break', 'continue', or 'ok'."""
    try:
        user_input = session.prompt(
            HTML(f"\n<prompt>fixos</prompt> <timer>[{format_time(remaining)}]</timer> ❯ ")
        ).strip()
    except (EOFError, KeyboardInterrupt):
        print("\n\nSesja przerwana przez użytkownika.")
        return "break"

    if not user_input:
        return "continue"
    if user_input.lower() in ('q', 'quit', 'exit', 'koniec'):
        print("\n✅ Sesja zakończona przez użytkownika.")
        return "quit"

    if user_input.startswith('!'):
        cmd = user_input[1:].strip()
        _, output = execute_command(cmd)
        feedback = f"Wynik komendy `{cmd}`:\n{output}"
        messages.append({"role": "user", "content": feedback})
        if verbose:
            print(f"\n[DEBUG] Dodano wynik do historii: {feedback[:100]}...")
        return "continue"

    messages.append({"role": "user", "content": user_input})
    if user_input.isdigit() or user_input.lower() == 'all':
        messages.append({
            "role": "user",
            "content": (
                f"Podaj TYLKO konkretną komendę shell do naprawy problemu {user_input}. "
                f"Format: `komenda`. Bez opisu."
            )
        })
    return "ok"


def run_llm_shell(
    diagnostics_data: dict,
    token: str,
    model: str = "gpt-4o-mini",
    timeout: int = SESSION_TIMEOUT,
    verbose: bool = False,
    base_url: Optional[str] = None,
):
    """
    Uruchamia interaktywny shell LLM z przekazanymi danymi diagnostycznymi.

    Args:
        diagnostics_data: Słownik z danymi diagnostycznymi (przed anonimizacją)
        token: Klucz API OpenAI lub kompatybilnego serwisu
        model: Nazwa modelu LLM
        timeout: Maksymalny czas sesji w sekundach
        verbose: Czy wyświetlać dodatkowe informacje debugowania
        base_url: Opcjonalny URL dla alternatywnych API (np. xAI, Ollama)
    """
    anon_data, _ = anonymize(str(diagnostics_data))

    client_kwargs: dict = {"api_key": token}
    if base_url:
        client_kwargs["base_url"] = base_url
    client = openai.OpenAI(**client_kwargs)

    signal.signal(signal.SIGALRM, _timeout_handler)
    signal.alarm(timeout)
    start_time = time.time()

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": (
            f"Oto anonimizowane dane diagnostyczne mojego systemu system:\n\n"
            f"```\n{anon_data}\n```\n\n"
            f"Przeanalizuj je i przedstaw wykryte problemy."
        )},
    ]

    style = Style.from_dict({'prompt': '#00aa00 bold', 'timer': '#888888'})
    session = PromptSession(style=style)

    print("\n" + "═" * 60)
    print(f"  🤖 fixos LLM Shell  |  Model: {model}")
    print(f"  ⏰ Sesja: max {format_time(timeout)}  |  Wpisz 'q' aby wyjść")
    print("═" * 60 + "\n")

    elapsed = 0
    try:
        while True:
            elapsed = int(time.time() - start_time)
            remaining = timeout - elapsed
            if remaining <= 0:
                raise SessionTimeout()

            print("🧠 LLM analizuje... ", end="", flush=True)
            reply = _llm_call(client, model, messages)
            if reply is None:
                break
            if reply == "":
                continue
            messages.append({"role": "assistant", "content": reply})

            print("\r" + " " * 25 + "\r", end="")  # wyczyść "analizuje..."
            print(f"\n{'─' * 60}")
            print(reply)
            print(f"{'─' * 60}")
            print(f"  ⏰ Pozostały czas: {format_time(remaining)}")

            action = _handle_user_turn(session, messages, remaining, verbose)
            if action in ("quit", "break"):
                break

    except SessionTimeout:
        print(f"\n\n⏰ Sesja wygasła po {format_time(timeout)}. Połączenie zakończone.")
    finally:
        signal.alarm(0)  # Wyłącz alarm

    print(f"\n{'═' * 60}")
    print(f"  📊 Podsumowanie sesji: {len(messages) - 2} interakcji w {format_time(elapsed)}")
    print(f"{'═' * 60}\n")
