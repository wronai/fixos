"""
Config management commands for fixOS CLI
"""
import click
from pathlib import Path


def _env_path() -> Path:
    """Return path to active .env file (cwd > home)."""
    for p in [Path.cwd() / ".env", Path.home() / ".fixos.env", Path.home() / ".fixos.conf"]:
        if p.exists():
            return p
    return Path.cwd() / ".env"


def _set_env_key(key: str, value: str) -> Path:
    """Update or insert KEY=VALUE in the active .env file."""
    path = _env_path()
    lines: list[str] = path.read_text(encoding="utf-8").splitlines() if path.exists() else []
    replaced = False
    for i, line in enumerate(lines):
        if line.startswith(f"{key}="):
            lines[i] = f"{key}={value}"
            replaced = True
            break
    if not replaced:
        lines.append(f"{key}={value}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    path.chmod(0o600)
    return path


@click.group("config")
def config() -> None:
    """Zarządzanie konfiguracją fixOS."""
    pass


@config.command("show")
def config_show() -> None:
    """Pokaż aktualną konfigurację."""
    from fixos.config import FixOsConfig

    cfg = FixOsConfig.load()
    click.echo(click.style("\nKonfiguracja fixOS:", fg="cyan", bold=True))
    click.echo(click.style("─" * 40, fg="cyan"))

    click.echo(f"  Provider: {cfg.provider}")
    click.echo(f"  Model: {cfg.model}")
    click.echo(f"  Timeout: {cfg.session_timeout}s")
    click.echo(f"  Agent mode: {cfg.agent_mode}")
    click.echo(f"  Web search: {'włączone' if cfg.enable_web_search else 'wyłączone'}")

    key_status = click.style("skonfigurowany", fg="green") if cfg.api_key else click.style("BRAK", fg="red")
    click.echo(f"  API Key: {key_status}")

    if cfg.env_file_loaded:
        click.echo(f"  Plik .env: {cfg.env_file_loaded}")
    else:
        click.echo("  Plik .env: nie znaleziono")
    click.echo()


@config.command("init")
@click.option("--force", is_flag=True, help="Nadpisz istniejący plik")
def config_init(force: bool) -> None:
    """Zainicjalizuj plik konfiguracyjny .env."""

    env_path = Path(".env")
    if env_path.exists() and not force:
        click.echo(click.style("Plik .env już istnieje. Użyj --force aby nadpisać.", fg="yellow"))
        return

    template = """# fixOS Configuration
# Provider: gemini|openai|xai|openrouter|ollama|custom
PROVIDER=gemini

# API Keys (wypełnij odpowiedni dla swojego providera)
GEMINI_API_KEY=
# OPENAI_API_KEY=
# XAI_API_KEY=
# OPENROUTER_API_KEY=

# Opcjonalne ustawienia
# MODEL=gemini-2.0-flash-exp
# SESSION_TIMEOUT=300
# AGENT_MODE=hitl
"""
    env_path.write_text(template)
    click.echo(click.style(f"Utworzono {env_path}", fg="green"))
    click.echo("Edytuj plik i dodaj swój klucz API.")


@config.command("set")
@click.argument("key")
@click.argument("value")
def config_set(key: str, value: str) -> None:
    """Ustaw wartość konfiguracyjną w .env."""
    from dotenv import set_key

    env_path = Path(".env")
    if not env_path.exists():
        click.echo(click.style("Plik .env nie istnieje. Uruchom: fixos config init", fg="yellow"))
        return

    set_key(str(env_path), key.upper(), value)
    click.echo(click.style(f"Ustawiono {key.upper()}={value}", fg="green"))


@config.command("model")
@click.option("--provider", "-p", default=None, help="Provider (domyślnie: aktualny z .env)")
def config_model(provider: str) -> None:
    """Interaktywnie wybierz model LLM z listy."""
    from fixos.config import FixOsConfig, PROVIDER_MODELS, PROVIDER_DEFAULTS

    cfg = FixOsConfig.load(provider=provider)
    current_provider = cfg.provider
    models = PROVIDER_MODELS.get(current_provider, [])

    click.echo(click.style(f"\n🤖 Wybór modelu dla providera: ", fg="cyan") +
               click.style(current_provider, fg="yellow", bold=True))
    click.echo(click.style(f"   Aktualny model: {cfg.model}", fg="white"))
    click.echo(click.style("─" * 50, fg="cyan"))

    if not models:
        click.echo(click.style(f"Brak znanych modeli dla '{current_provider}'.", fg="yellow"))
        custom = click.prompt("Podaj nazwę modelu ręcznie", default=cfg.model)
        chosen = custom
    else:
        click.echo()
        for i, m in enumerate(models, 1):
            marker = click.style("◀ aktualny", fg="green") if m == cfg.model else ""
            click.echo(f"  [{i:2d}] {m}  {marker}")
        click.echo(f"  [ 0] Wpisz własną nazwę modelu")
        click.echo()

        while True:
            raw = click.prompt(click.style("Wybierz numer lub 0", fg="cyan"), default="1")
            if raw == "0":
                chosen = click.prompt("Podaj nazwę modelu", default=cfg.model)
                break
            if raw.isdigit() and 1 <= int(raw) <= len(models):
                chosen = models[int(raw) - 1]
                break
            click.echo(click.style(f"  ❌ Wpisz numer 0–{len(models)}", fg="red"))

    provider_key = f"{current_provider.upper()}_MODEL"
    env_file = _set_env_key(provider_key, chosen)
    click.echo()
    click.echo(click.style(f"  ✅ Ustawiono {provider_key}={chosen}", fg="green"))
    click.echo(click.style(f"  💾 Zapisano → {env_file}", fg="cyan"))
    click.echo()


@config.command("provider")
def config_provider() -> None:
    """Interaktywnie wybierz providera LLM z listy."""
    from fixos.config import FixOsConfig, PROVIDER_DEFAULTS

    cfg = FixOsConfig.load()
    free = [(n, d) for n, d in PROVIDER_DEFAULTS.items() if d.get("free_tier")]
    paid = [(n, d) for n, d in PROVIDER_DEFAULTS.items() if not d.get("free_tier")]

    click.echo(click.style("\n⚙️  Wybór providera LLM", fg="cyan", bold=True))
    click.echo(click.style(f"   Aktualny: {cfg.provider} ({cfg.model})", fg="white"))
    click.echo(click.style("─" * 60, fg="cyan"))
    click.echo()
    click.echo(click.style("  🟢 DARMOWE:", fg="green"))

    num_map: dict[int, str] = {}
    idx = 1
    for name, d in free:
        marker = click.style(" ◀ aktualny", fg="green") if name == cfg.provider else ""
        click.echo(f"  [{idx:2d}] {click.style(name, fg='yellow'):<20} {d['model']:<38}{marker}")
        num_map[idx] = name
        idx += 1

    click.echo()
    click.echo(click.style("  💰 PŁATNE:", fg="yellow"))
    for name, d in paid:
        marker = click.style(" ◀ aktualny", fg="green") if name == cfg.provider else ""
        click.echo(f"  [{idx:2d}] {click.style(name, fg='yellow'):<20} {d['model']:<38}{marker}")
        num_map[idx] = name
        idx += 1

    click.echo()
    click.echo("  [ 0] Anuluj")
    click.echo()

    while True:
        raw = click.prompt(click.style("Wybierz numer providera", fg="cyan"), default="0")
        if raw == "0":
            click.echo(click.style("Anulowano.", fg="yellow"))
            return
        if raw.isdigit() and int(raw) in num_map:
            chosen = num_map[int(raw)]
            break
        click.echo(click.style(f"  ❌ Wpisz numer 0–{len(num_map)}", fg="red"))

    pdef = PROVIDER_DEFAULTS[chosen]
    key_env = pdef.get("key_env")

    env_file = _set_env_key("LLM_PROVIDER", chosen)
    click.echo()
    click.echo(click.style(f"  ✅ Ustawiono LLM_PROVIDER={chosen}", fg="green"))

    if chosen != "ollama" and key_env:
        import os
        existing_key = os.environ.get(key_env, "")
        if not existing_key:
            click.echo(click.style(f"  ℹ️  Pobierz klucz API: {pdef.get('key_url', '')}", fg="cyan"))
            if click.confirm(click.style(f"  Chcesz teraz wpisać klucz {key_env}?", fg="yellow"), default=False):
                key = click.prompt(f"  Wklej klucz {key_env}", hide_input=True)
                if key.strip():
                    _set_env_key(key_env, key.strip())
                    click.echo(click.style(f"  ✅ Zapisano {key_env}", fg="green"))

    click.echo(click.style(f"  💾 Zapisano → {env_file}", fg="cyan"))
    click.echo(click.style(f"\n  Następny krok – wybierz model: fixos config model", fg="white"))
    click.echo()
