"""
Config management commands for fixOS CLI
"""
import click


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
def config_init(force) -> None:
    """Zainicjalizuj plik konfiguracyjny .env."""
    from pathlib import Path

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
def config_set(key, value) -> None:
    """Ustaw wartość konfiguracyjną w .env."""
    from pathlib import Path
    from dotenv import set_key

    env_path = Path(".env")
    if not env_path.exists():
        click.echo(click.style("Plik .env nie istnieje. Uruchom: fixos config init", fg="yellow"))
        return

    set_key(str(env_path), key.upper(), value)
    click.echo(click.style(f"Ustawiono {key.upper()}={value}", fg="green"))
