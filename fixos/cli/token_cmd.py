"""
Token management commands for fixOS CLI
"""
import click
import os
from pathlib import Path


@click.group("token")
def token() -> None:
    """Zarządzanie tokenem API."""
    pass


@token.command("set")
@click.argument("key")
@click.option("--provider", "-p", default=None, help="Provider (auto-detect if not provided)")
@click.option("--env-file", "-e", default=".env", help="Plik .env do zapisu")
def token_set(key, provider, env_file) -> None:
    """
    Zapisz token API do pliku .env.

    \b
    Przykłady:
      fixos token set AIzaSy...                    # auto-detect provider
      fixos token set sk-... --provider openai   # wymuszony provider
      fixos token set $TOKEN --env-file ~/.env   # inny plik
    """
    from fixos.config import detect_provider_from_key, FixOsConfig, ENV_SEARCH_PATHS
    from dotenv import set_key

    # Auto-detect provider if not specified
    detected = detect_provider_from_key(key)
    if provider is None:
        provider = detected
        click.echo(click.style(f"Wykryto provider: {provider}", fg="cyan"))

    env_path = Path(env_file).expanduser().resolve()

    # Check if file exists, if not create it
    if not env_path.exists():
        if click.confirm(f"Plik {env_path} nie istnieje. Utworzyć?"):
            env_path.touch()
        else:
            click.echo(click.style("Anulowano.", fg="yellow"))
            return

    # Map provider to env var
    provider_env_vars = {
        "gemini": "GEMINI_API_KEY",
        "openai": "OPENAI_API_KEY",
        "xai": "XAI_API_KEY",
        "openrouter": "OPENROUTER_API_KEY",
        "ollama": "OLLAMA_HOST",
        "groq": "GROQ_API_KEY",
        "mistral": "MISTRAL_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
        "together": "TOGETHER_API_KEY",
        "cohere": "COHERE_API_KEY",
        "deepseek": "DEEPSEEK_API_KEY",
        "cerebras": "CEREBRAS_API_KEY",
        "custom": "LLM_API_KEY",
    }

    env_var = provider_env_vars.get(provider, "LLM_API_KEY")

    # Write to .env
    try:
        set_key(str(env_path), env_var, key)
        # Set file permissions to 600 (owner read/write only)
        os.chmod(env_path, 0o600)
        masked = f"{key[:8]}...{key[-4:]}" if len(key) > 12 else "***"
        click.echo(click.style(f"Zapisano {env_var}={masked} do {env_path}", fg="green"))

        # Also update current process
        os.environ[env_var] = key

        # Validate by loading config
        cfg = FixOsConfig.load()
        if cfg.api_key == key:
            click.echo(click.style("Token aktywny i działa!", fg="green"))
        else:
            click.echo(click.style("Token zapisany, ale wymagany restart shell.", fg="yellow"))

    except Exception as e:
        click.echo(click.style(f"Błąd zapisu: {e}", fg="red"))


@token.command("show")
def token_show() -> None:
    """Pokaż obecny token (masked)."""
    from fixos.config import FixOsConfig

    cfg = FixOsConfig.load()
    if cfg.api_key:
        masked = f"{cfg.api_key[:8]}...{cfg.api_key[-4:]}"
        click.echo(f"Provider: {cfg.provider}")
        click.echo(f"Model: {cfg.model}")
        click.echo(f"Token: {masked}")
    else:
        click.echo(click.style("Brak skonfigurowanego tokenu.", fg="yellow"))


@token.command("clear")
@click.option("--env-file", "-e", default=".env", help="Plik .env do edycji")
def token_clear(env_file) -> None:
    """Usuń token z pliku .env."""
    from dotenv import unset_key

    env_path = Path(env_file).expanduser().resolve()
    if not env_path.exists():
        click.echo(click.style(f"Plik {env_path} nie istnieje.", fg="yellow"))
        return

    # Unset all known API keys
    keys = ["GEMINI_API_KEY", "OPENAI_API_KEY", "XAI_API_KEY",
            "OPENROUTER_API_KEY", "GROQ_API_KEY", "MISTRAL_API_KEY",
            "ANTHROPIC_API_KEY", "TOGETHER_API_KEY", "COHERE_API_KEY",
            "DEEPSEEK_API_KEY", "CEREBRAS_API_KEY", "LLM_API_KEY"]

    for key in keys:
        unset_key(str(env_path), key)

    click.echo(click.style("Tokeny usunięte z pliku .env", fg="green"))
