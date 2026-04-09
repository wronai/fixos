"""
Interactive provider setup module.
Handles user prompts for LLM provider configuration.
"""

from pathlib import Path
from typing import Optional

from .config import FixOsConfig, PROVIDER_DEFAULTS


def _print_provider_menu() -> dict[int, str]:
    """Print provider selection menu and return number mapping."""
    free = [(n, d) for n, d in PROVIDER_DEFAULTS.items() if d.get("free_tier")]
    paid = [(n, d) for n, d in PROVIDER_DEFAULTS.items() if not d.get("free_tier")]
    ordered = free + paid

    print()
    print("  ┌─────────────────────────────────────────────────────────────┐")
    print("  │  ⚙️  Brak konfiguracji LLM – wybierz provider               │")
    print("  └─────────────────────────────────────────────────────────────┘")
    print()
    print("  🟢 DARMOWE:")
    idx = 1
    num_map: dict[int, str] = {}
    for name, d in free:
        key_env = d.get("key_env") or "(brak)"
        print(f"  [{idx:2d}] {name:<12} {d['model']:<35} {key_env}")
        num_map[idx] = name
        idx += 1
    print()
    print("  💰 PŁATNE:")
    for name, d in paid:
        key_env = d.get("key_env") or "(brak)"
        print(f"  [{idx:2d}] {name:<12} {d['model']:<35} {key_env}")
        num_map[idx] = name
        idx += 1
    print()
    print("  [0]  Anuluj")
    print()
    
    return num_map


def _get_user_choice(num_map: dict[int, str]) -> Optional[str]:
    """Get validated user choice for provider."""
    while True:
        try:
            raw = input("  Wybierz numer providera: ").strip()
        except (EOFError, KeyboardInterrupt):
            return None
        if raw == "0":
            return None
        if raw.isdigit() and int(raw) in num_map:
            return num_map[int(raw)]
        print(f"  ❌ Nieprawidłowy wybór. Wpisz numer 1–{len(num_map)} lub 0 aby anulować.")


def _get_api_key(provider: str) -> Optional[str]:
    """Prompt user for API key."""
    pdef = PROVIDER_DEFAULTS[provider]
    key_env = pdef.get("key_env")

    if provider == "ollama":
        print(f"\n  ✅ Wybrano: {provider} (lokalny, brak klucza API)")
        return ""

    print(f"\n  ✅ Wybrano: {provider}")
    print(f"  Pobierz klucz API: {pdef.get('key_url', '')}")
    print()
    try:
        key = input(f"  Wklej klucz API ({key_env}): ").strip()
    except (EOFError, KeyboardInterrupt):
        return None

    if not key:
        print("  ❌ Brak klucza – anulowano.")
        return None
    
    return key


def _save_to_env(provider: str, key: str, key_env: Optional[str]) -> Path:
    """Save provider config to .env file."""
    env_path = Path.cwd() / ".env"
    lines: list[str] = []
    if env_path.exists():
        lines = env_path.read_text(encoding="utf-8").splitlines()

    key_line = f"{key_env}={key}"
    provider_line = f"LLM_PROVIDER={provider}"

    # Update or add API key
    key_replaced = False
    for i, line in enumerate(lines):
        if line.startswith(f"{key_env}="):
            lines[i] = key_line
            key_replaced = True
            break
    if not key_replaced:
        lines.append(key_line)

    # Update or add LLM_PROVIDER
    provider_replaced = False
    for i, line in enumerate(lines):
        if line.startswith("LLM_PROVIDER="):
            lines[i] = provider_line
            provider_replaced = True
            break
    if not provider_replaced:
        lines.insert(0, provider_line)

    env_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    env_path.chmod(0o600)
    
    return env_path


def interactive_provider_setup() -> Optional[FixOsConfig]:
    """
    Interaktywny wybór providera gdy brak konfiguracji.
    Wyświetla numerowaną listę providerów i pyta użytkownika.
    Zwraca FixOsConfig lub None jeśli user zrezygnował.
    """
    num_map = _print_provider_menu()
    chosen = _get_user_choice(num_map)
    if chosen is None:
        return None

    pdef = PROVIDER_DEFAULTS[chosen]
    key_env = pdef.get("key_env")

    key = _get_api_key(chosen)
    if key is None:
        return None
    
    if key == "":  # ollama, no key needed
        return FixOsConfig.load(provider=chosen)

    env_path = _save_to_env(chosen, key, key_env)

    CONSTANT_4 = 4
    CONSTANT_8 = 8
    CONSTANT_12 = 12
    masked = f"{key[:CONSTANT_8]}...{key[-CONSTANT_4:]}" if len(key) > CONSTANT_12 else "***"
    print(f"  💾 Zapisano {key_env}={masked} → {env_path}")
    print()

    return FixOsConfig.load(provider=chosen, api_key=key)
