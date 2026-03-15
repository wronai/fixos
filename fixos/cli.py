"""
fixos CLI – wielopoziomowe komendy
  fixos scan          – diagnostyka systemu
  fixos fix           – diagnoza + sesja naprawcza
  fixos token         – zarządzanie tokenem API
  fixos config        – konfiguracja i ustawienia
  fixos providers     – lista dostępnych providerów LLM
  fixos test-llm      – test połączenia z LLM
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional, List

import click

from .config import (
    FixOsConfig, get_providers_list, ENV_SEARCH_PATHS, PROVIDER_DEFAULTS,
    detect_provider_from_key, interactive_provider_setup,
)
from .diagnostics import get_full_diagnostics, DIAGNOSTIC_MODULES
from .utils.anonymizer import anonymize, display_anonymized_preview
from .agent.hitl import run_hitl_session
from .agent.autonomous import run_autonomous_session

BANNER = r"""
  ___  _       ___  ____
 / _(_)_  __  / _ \/ ___|
| |_| \ \/ / | | | \___ \
|  _| |>  <  | |_| |___) |
|_| |_/_/\_\  \___/|____/
  AI-powered OS Diagnostics  •  v2.0.0
"""

COMMON_OPTIONS = [
    click.option("--provider", "-p", default=None,
                 help="Provider LLM: gemini|openai|xai|openrouter|ollama"),
    click.option("--token", "-t", default=None, envvar="API_KEY",
                 help="Klucz API (override .env)"),
    click.option("--model", "-m", default=None,
                 help="Nazwa modelu LLM"),
    click.option("--no-banner", is_flag=True, default=False),
]


def add_common_options(fn):
    for opt in reversed(COMMON_OPTIONS):
        fn = opt(fn)
    return fn

def add_shared_options(func):
    """Shared options for both scan and fix commands"""
    func = click.option("--show-raw", "show_raw", is_flag=True, default=False,
                       help="Pokaż surowe dane diagnostyczne (JSON)")(func)
    func = click.option("--no-banner", "no_banner", is_flag=True, default=False,
                       help="Ukryj baner fixos")(func)
    func = click.option("--disc", is_flag=True, default=False,
                       help="Analiza zajętości dysku + grupowanie przyczyn")(func)
    func = click.option("--disk", "disc", is_flag=True, default=False,
                       help="Analiza zajętości dysku (alias do --disc)")(func)
    func = click.option("--dry-run", is_flag=True, default=False,
                       help="Symuluj wykonanie komend bez faktycznego uruchamiania")(func)
    func = click.option("--interactive/--no-interactive", default=True,
                       help="Tryb interaktywny (pytaj przed każdą akcją)")(func)
    func = click.option("--json", "json_output", is_flag=True, default=False,
                       help="Wyjście w formacie JSON")(func)
    func = click.option("--llm-fallback/--no-llm-fallback", default=True,
                       help="Użyj LLM gdy heurystyki nie wystarczą")(func)
    return func



# ══════════════════════════════════════════════════════════
#  GŁÓWNA GRUPA
# ══════════════════════════════════════════════════════════

class NaturalLanguageGroup(click.Group):
    def resolve_command(self, ctx, args):
        cmd_name = args[0] if args else None
        cmd = self.get_command(ctx, cmd_name) if cmd_name else None
        if cmd is None and args and not args[0].startswith("-"):
            return super().resolve_command(ctx, ["ask"] + args)
        return super().resolve_command(ctx, args)

@click.group(cls=NaturalLanguageGroup, invoke_without_command=True)
@click.pass_context
@click.option("--dry-run", is_flag=True, default=False, help="Symuluj bez wykonania (dla komend naturalnych)")
@click.option("--version", "-v", is_flag=True, default=False, help="Pokaż wersję fixos")
def cli(ctx, dry_run, version):
    """
    fixos – AI-powered diagnostyka i naprawa Linux, Windows, macOS.

    \b
    Szybki start:
      fixos token set AIzaSy...   # zapisz token Gemini
      fixos fix                   # diagnostyka + naprawa
      fixos scan --audio          # tylko skan audio

    \b
    Polecenia w jezyku naturalnym:
      fixos "wylacz wszystkie kontenery docker"
      fixos "zlap bledy w systemie"
      fixos "napraw audio"

    \b
    Więcej:
      fixos --help
      fixos fix --help
    """
    if version:
        click.echo("fixos v2.0.0")
        return
    
    if ctx.invoked_subcommand is None:
        _print_welcome()


# Osobna komenda dla poleceń naturalnych
@cli.command("ask")
@click.argument("prompt")
@click.option("--dry-run", is_flag=True, default=False, help="Symuluj bez wykonania")
def ask(prompt, dry_run):
    """Wykonaj polecenie w języku naturalnym."""
    _handle_natural_command(prompt, dry_run)


def _handle_natural_command(prompt: str, dry_run: bool = False):
    """Obsluga polecen w jezyku naturalnym z wyjściem YAML i walidacją LLM."""
    import subprocess
    import yaml
    
    prompt_lower = prompt.lower()
    
    # Wykryj akcję (pierwsze dopasowanie) - heurystyka
    # Uwaga: "wylacz" = usun (nie tylko stop) żeby wyłączyć WSZYSTKIE kontenery
    action_keywords = {
        # Docker actions - "wylacz wszystkie" = usun wszystkie kontenery (zatrzymane też)
        ("wylacz", "wyłącz"): "docker ps -aq | xargs -r docker rm -f",
        ("stop", "zatrzymaj"): "docker ps -aq | xargs -r docker stop",
        ("usun", "rm", "remove", "delete", "usuń"): "docker ps -aq | xargs -r docker rm -f",
        
        # System actions
        ("scan", "diagnostyka", "zlap", "bledy", "errors"): ("fixos", ["scan"]),
        ("fix", "napraw", "naprawa"): ("fixos", ["fix"]),
        
        # Other
        ("lista", "list", "ps", "pokaz", "pokaż"): None,  # handled below
    }
    
    matched_cmd = None
    used_llm = False
    llm_provider = None
    
    for keywords, cmd in action_keywords.items():
        if any(kw in prompt_lower for kw in keywords):
            if cmd is not None:
                matched_cmd = cmd
                break
            # dla "lista" - sprawdź czy to docker
            if "docker" in prompt_lower or "kontener" in prompt_lower:
                matched_cmd = ("docker", ["ps", "-a"])
                break
    else:
        # Jeśli nie znaleziono akcji, sprawdź obiekty
        if "docker" in prompt_lower or "kontener" in prompt_lower or "container" in prompt_lower:
            matched_cmd = ("docker", ["ps", "-aq"])
        elif "audio" in prompt_lower or "dzwięk" in prompt_lower or "sound" in prompt_lower:
            matched_cmd = ("fixos", ["fix", "--modules", "audio"])
        elif "siec" in prompt_lower or "network" in prompt_lower or "internet" in prompt_lower:
            matched_cmd = ("fixos", ["scan", "--modules", "system"])
        elif "bezpieczenstwo" in prompt_lower or "security" in prompt_lower:
            matched_cmd = ("fixos", ["scan", "--modules", "security"])

    if not matched_cmd:
        # Nie rozpoznano polecenia - użyj LLM do wygenerowania komendy
        try:
            cfg = FixOsConfig.load()
            if not cfg.api_key:
                output = {
                    "status": "error",
                    "reason": "no_api_key",
                    "message": "Brak klucza API. Użyj: fixos token set <KLUCZ>",
                    "hint": 'fixos ask "wylacz wszystkie kontenery docker"'
                }
                click.echo(yaml.dump(output, default_flow_style=False, allow_unicode=True))
                return
            
            from .providers.llm import LLMClient
            llm = LLMClient(cfg)
            used_llm = True
            llm_provider = f"{cfg.provider}/{cfg.model}"
            
            # Prompt do LLM
            llm_prompt = f"""Jesteś asystentem CLI. Użytkownik wpisał: '{prompt}'
Wybierz najlepszą komendę systemową Linux do wykonania.
Odpowiedz TYLKO komendą (bez żadnego dodatkowego tekstu).
Przykłady:
- "wyłącz docker" → docker ps -aq | xargs -r docker stop
- "pokaż procesy" → ps aux
- "sprawdź sieć" → ip addr
- "napraw dźwięk" → fixos fix --modules audio
- "diagnostyka" → fixos scan
"""
            resp = llm.chat([{"role": "user", "content": llm_prompt}], max_tokens=200)
            cmd_str = resp.strip().split('\n')[0].strip()
            
            # Usuń backticks jeśli są
            cmd_str = cmd_str.strip('`').strip()
            
            if not cmd_str or len(cmd_str) <= 2:
                output = {
                    "status": "error",
                    "reason": "llm_empty_response",
                    "message": "LLM nie zwrócił komendy"
                }
                click.echo(yaml.dump(output, default_flow_style=False, allow_unicode=True))
                return
            
            if dry_run:
                output = {
                    "status": "dry_run",
                    "prompt": prompt,
                    "source": "llm",
                    "llm": llm_provider,
                    "command": cmd_str
                }
                click.echo(yaml.dump(output, default_flow_style=False, allow_unicode=True))
                return
            
            # Wykonaj wygenerowaną komendę
            result = subprocess.run(cmd_str, capture_output=True, text=True, shell=True)
            output = {
                "status": "success" if result.returncode == 0 else "failed",
                "exit_code": result.returncode,
                "prompt": prompt,
                "source": "llm",
                "llm": llm_provider,
                "command": cmd_str,
                "stdout": result.stdout if result.stdout else "",
                "stderr": result.stderr if result.stderr else ""
            }
            click.echo(yaml.dump(output, default_flow_style=False, allow_unicode=True))
            
            # Walidacja LLM
            _validate_result_with_llm(prompt, cmd_str, result, cfg)
            return
        except Exception as e:
            output = {
                "status": "error",
                "reason": "llm_error",
                "message": str(e),
                "hint": 'fixos ask "wylacz wszystkie kontenery docker"'
            }
            click.echo(yaml.dump(output, default_flow_style=False, allow_unicode=True))
            return

    # Wykonaj polecenie - matched_cmd może być stringiem lub krotką
    if isinstance(matched_cmd, str):
        cmd_str = matched_cmd
    else:
        cmd_program = matched_cmd[0]
        cmd_args = matched_cmd[1] if len(matched_cmd) > 1 else []
        cmd_full = [cmd_program] + cmd_args
        cmd_str = " ".join(cmd_full)

    if dry_run:
        output = {
            "status": "dry_run",
            "prompt": prompt,
            "source": "heuristics",
            "llm": None,
            "command": cmd_str
        }
        click.echo(yaml.dump(output, default_flow_style=False, allow_unicode=True))
        return

    try:
        result = subprocess.run(cmd_str, capture_output=True, text=True, shell=True)
        
        # Buduj dict tylko z niepustymi polami
        output = {
            "status": "success" if result.returncode == 0 else "failed",
            "exit_code": result.returncode,
            "prompt": prompt,
            "source": "heuristics",
            "command": cmd_str,
        }
        if result.stdout:
            output["stdout"] = result.stdout
        if result.stderr:
            output["stderr"] = result.stderr
        
        click.echo(yaml.dump(output, default_flow_style=False, allow_unicode=True))
        
        # Walidacja LLM - sprawdź czy wynik odpowiada oczekiwaniom użytkownika
        try:
            cfg = FixOsConfig.load()
            if cfg.api_key:
                _validate_result_with_llm(prompt, cmd_str, result, cfg)
        except:
            pass  # Ignoruj błędy walidacji
    except Exception as e:
        output = {
            "status": "error",
            "reason": "execution_error",
            "prompt": prompt,
            "source": "heuristics",
            "llm": None,
            "command": cmd_str,
            "error": str(e)
        }
        click.echo(yaml.dump(output, default_flow_style=False, allow_unicode=True))


def _validate_result_with_llm(prompt: str, cmd_str: str, result, cfg):
    """Waliduje wynik polecenia przez LLM - generuje komende sprawdzającą stan."""
    import yaml
    import subprocess
    from .providers.llm import LLMClient
    
    try:
        llm = LLMClient(cfg)
        llm_provider = f"{cfg.provider}/{cfg.model}"
        
        # Pobierz stdout do walidacji (limit 2000 znaków)
        stdout_preview = result.stdout[:2000] if result.stdout else "(puste)"
        
        # LLM generuje komendę sprawdzającą stan systemu
        check_prompt = f"""Jesteś asystentem CLI. Użytkownik chciał: "{prompt}"
Wykonana komenda: {cmd_str}
Wynik (stdout):
{stdout_preview}

Wynik (stderr): {result.stderr[:500] if result.stderr else '(brak)'}
Exit code: {result.returncode}

Wygeneruj komendę Linux która sprawdzi czy oczekiwany efekt został osiągnięty.
Odpowiedz TYLKO komendą (bez żadnego dodatkowego tekstu).
Przykłady:
- "wyłącz docker" → docker ps -a
- "zatrzymaj usługę" → systemctl status usługa
- "sprawdź sieć" → ip addr
- "napraw dźwięk" → pactl info
"""
        
        check_cmd_resp = llm.chat([{"role": "user", "content": check_prompt}], max_tokens=200)
        check_cmd = check_cmd_resp.strip().split('\n')[0].strip()
        check_cmd = check_cmd.strip('`').strip()
        
        if not check_cmd or len(check_cmd) <= 2:
            return
        
        # Wykonaj komendę sprawdzającą
        check_result = subprocess.run(check_cmd, capture_output=True, text=True, shell=True)
        
        # Teraz oceń wynik
        validation_prompt = f"""Jesteś walidatorem wyników poleceń systemowych.
Oczekiwany efekt: "{prompt}"
Komenda wykonana: {cmd_str}
Wynik wykonania (stdout): {stdout_preview}

Komenda sprawdzająca: {check_cmd}
Wynik sprawdzenia (stdout): {check_result.stdout[:2000] if check_result.stdout else '(puste)'}
Wynik sprawdzenia (stderr): {check_result.stderr[:500] if check_result.stderr else '(brak)'}

Odpowiedz w formacie YAML:
validation:
  success: true/false - czy komenda osiągnęła to co użytkownik chciał
  interpretation: "krótka interpretacja wyniku"
  user_intent_met: true/false - czy oczekiwania użytkownika zostały spełnione
  suggestion: "opcjonalna sugestia jeśli coś poszło nie tak"
"""
        
        resp = llm.chat([{"role": "user", "content": validation_prompt}], max_tokens=500)
        
        # Spróbuj parsować YAML z odpowiedzi
        try:
            yaml_start = resp.find('---')
            if yaml_start >= 0:
                yaml_content = resp[yaml_start:]
            else:
                yaml_content = resp
            
            validation = yaml.safe_load(yaml_content)
            if validation:
                # Dodaj info o komendzie sprawdzającej
                validation['validation']['check_command'] = check_cmd
                validation['validation']['check_result'] = check_result.stdout[:500] if check_result.stdout else ""
                validation['validation']['llm_provider'] = llm_provider
                click.echo(yaml.dump({"validation": validation['validation']}, default_flow_style=False, allow_unicode=True))
                return
        except:
            pass
        
        # Fallback: pokaż info o komendzie sprawdzającej
        click.echo(yaml.dump({
            "validation": {
                "llm_provider": llm_provider,
                "check_command": check_cmd,
                "check_result": check_result.stdout[:500] if check_result.stdout else "",
                "raw_response": resp[:500]
            }
        }, default_flow_style=False, allow_unicode=True))
    except Exception as e:
        pass


def _print_welcome():
    """Ekran powitalny fixos przy braku podkomendy."""
    click.echo(click.style(BANNER, fg="cyan"))

    cfg = FixOsConfig.load()
    has_key = bool(cfg.api_key)
    key_status = click.style("skonfigurowany", fg="green") if has_key else click.style("BRAK", fg="red")
    provider_info = f"{cfg.provider} ({cfg.model})"

    click.echo(click.style("═" * 60, fg="cyan"))
    click.echo(click.style("  DOSTĘPNE KOMENDY", fg="cyan", bold=True))
    click.echo(click.style("═" * 60, fg="cyan"))
    click.echo()

    commands = [
        ("fixos fix",         "", "Diagnostyka + sesja naprawcza z AI (HITL)"),
        ("fixos scan",        "", "Diagnostyka systemu bez AI"),
        ("fixos quickfix",    "", "Naprawy offline bez API (baza znanych bugów)"),
        ("fixos cleanup",     "", "Skanuj i czyść dane usług (Docker, Ollama)"),
        ("fixos orchestrate", "", "Zaawansowana orkiestracja napraw (graf problemów)"),
        ("fixos watch",       "", "Monitoring w tle z powiadomieniami"),
        ("fixos report",      "", "Eksport diagnostyki do HTML/Markdown/JSON"),
        ("fixos history",     "", "Historia sesji naprawczych"),
        ("fixos rollback",    "", "Cofanie operacji (undo/list/show)"),
        ("fixos profile",     "", "Profile diagnostyczne (server/desktop/dev)"),
        ("fixos llm",         "", "Lista providerów LLM + linki do kluczy API"),
        ("fixos token set",   "", "Zapisz klucz API (auto-detekcja providera)"),
        ("fixos config show", "", "Pokaż konfigurację"),
        ("fixos test-llm",    "", "Test połączenia z LLM"),
    ]

    for cmd, icon, desc in commands:
        cmd_styled = click.style(f"{cmd:<26}", fg="yellow")
        click.echo(f"  {icon}  {cmd_styled} {desc}")

    click.echo()
    click.echo(click.style("─" * 60, fg="cyan"))
    click.echo(click.style("  🔬 MODUŁY DIAGNOSTYKI", fg="cyan"))
    click.echo(click.style("─" * 60, fg="cyan"))
    modules_info = [
        ("system",     " ", "CPU, RAM, dyski, usługi, aktualizacje"),
        ("audio",      "", "ALSA, PipeWire, SOF firmware, mikrofon"),
        ("thumbnails", " ", "Podglądy plików, cache, GStreamer"),
        ("hardware",   "", "DMI, GPU, touchpad, kamera, bateria"),
        ("security",   "", "Firewall, porty, SELinux, SSH, fail2ban"),
        ("resources",  "", "Dysk (co zajmuje), procesy, autostart"),
    ]
    for mod, icon, desc in modules_info:
        mod_styled = click.style(f"{mod:<12}", fg="white")
        click.echo(f"  {icon}  {mod_styled} {desc}")
    click.echo(click.style("  Użycie: fixos scan --modules security,resources", fg="cyan"))

    click.echo()
    click.echo(click.style("─" * 60, fg="cyan"))
    click.echo(click.style("  AKTUALNY STATUS", fg="cyan"))
    click.echo(click.style("─" * 60, fg="cyan"))
    click.echo(f"  Provider  : {provider_info}")
    click.echo(f"  API Key   : {key_status}")
    click.echo(f"  .env plik : {cfg.env_file_loaded or 'nie znaleziono'}")
    click.echo()

    if not has_key:
        click.echo(click.style("  Szybki start:", fg="yellow", bold=True))
        click.echo(click.style("     fixos llm", fg="yellow") + "                    # wybierz provider i pobierz klucz")
        click.echo(click.style("     fixos token set <KLUCZ>", fg="yellow") + "      # zapisz klucz (auto-detekcja providera)")
        click.echo(click.style("     fixos fix", fg="yellow") + "                    # uruchom diagnostykę + naprawę")
        click.echo()
        click.echo(click.style("  ⚡ Lub po prostu:", fg="yellow"))
        click.echo(click.style("     fixos fix", fg="yellow") + "  # zapyta o provider interaktywnie")
    else:
        click.echo(click.style("  Przykłady użycia:", fg="yellow", bold=True))
        click.echo(click.style("     fixos fix", fg="yellow") + "                           # pełna diagnostyka + naprawa")
        click.echo(click.style("     fixos fix --modules security,resources", fg="yellow") + " # bezpieczeństwo + zasoby")
        click.echo(click.style("     fixos scan --modules security", fg="yellow") + "        # tylko skan bezpieczeństwa")
        click.echo(click.style("     fixos orchestrate --dry-run", fg="yellow") + "          # podgląd napraw bez wykonania")
    click.echo()


# ══════════════════════════════════════════════════════════
#  fixos scan
# ══════════════════════════════════════════════════════════

@cli.command()
@click.option("--audio", "modules", flag_value="audio", help="Tylko diagnostyka dźwięku")
@click.option("--thumbnails", "modules", flag_value="thumbnails", help="Tylko podglądy plików")
@click.option("--hardware", "modules", flag_value="hardware", help="Tylko sprzęt")
@click.option("--system", "modules", flag_value="system", help="Tylko system")
@click.option("--all", "modules", flag_value="all", default=True, help="Wszystkie moduły (domyślnie)")
@add_shared_options
@click.option("--output", "-o", default=None, help="Zapisz wyniki do pliku")
@click.option("--profile", "-p", default=None, help="Profil diagnostyczny (server/desktop/developer/minimal)")
def scan(modules, output, show_raw, no_banner, disc, dry_run, interactive, json_output, llm_fallback, profile):
    """
    Przeprowadza diagnostykę systemu.

    \b
    Nowe opcje:
      --disc          – Analiza zajętości dysku
      --dry-run       – Symulacja (dla kompatybilności)
      --interactive   – Tryb interaktywny (dla kompatybilności)
      --json          – Wyjście w formacie JSON
      --llm-fallback  – Użyj LLM gdy heurystyki nie wystarczą
      --profile       – Profil diagnostyczny (nadpisuje --modules)

    \b
    Przykłady:
      fixos scan                    # pełna diagnostyka
      fixos scan --disc              # z analizą dysku
      fixos scan --disc --json      # analiza dysku w JSON
      fixos scan --audio             # tylko diagnostyka dźwięku
      fixos scan --profile server    # profil serwera
    """
    if not no_banner:
        click.echo(click.style(BANNER, fg="cyan"))

    selected_modules = [modules] if modules and modules != "all" else None

    # Profile overrides module selection
    if profile:
        from .profiles import Profile as DiagProfile
        try:
            prof = DiagProfile.load(profile)
            selected_modules = prof.modules
            click.echo(click.style(f"  Profil: {prof.name} — {prof.description}", fg="cyan"))
        except FileNotFoundError as e:
            click.echo(click.style(str(e), fg="red"))
            return
    
    if disc and modules == "all":
        # Skip heavy system diagnostics if only disk is requested implicitly
        data = {}
    else:
        click.echo(click.style("Zbieranie diagnostyki...", fg="yellow"))
        def progress(name, desc):
            click.echo(f"  → {desc}...")
        data = get_full_diagnostics(selected_modules, progress_callback=progress)
    
    if disc:
        _run_disk_analysis(data, json_output=json_output, is_fix_mode=False)

    if show_raw:
        import json
        click.echo(json.dumps(data, indent=2, default=str))
    else:
        # Display regular diagnostic summary
        click.echo(click.style("Diagnostyka zakończona.", fg="green"))
        
    if output:
        try:
            import json
            Path(output).write_text(
                json.dumps(data, ensure_ascii=False, indent=2, default=str),
                encoding="utf-8"
            )
            click.echo(click.style(f"Zapisano: {output}", fg="green"))
        except Exception as e:
            click.echo(f"Błąd zapisu: {e}")

def _run_disk_analysis(data: dict, json_output: bool, is_fix_mode: bool = False):
    """Helper for disk analysis logic to avoid duplication between scan and fix"""
    click.echo(click.style("Analizowanie zajętości dysku...", fg="blue"))
    try:
        from .diagnostics.disk_analyzer import DiskAnalyzer
        analyzer = DiskAnalyzer()
        disk_analysis = analyzer.analyze_disk_usage()
        
        if "error" not in disk_analysis:
            data["disk_analysis"] = disk_analysis
            
            if json_output and not is_fix_mode:
                import json
                click.echo(json.dumps(disk_analysis, indent=2, default=str))
                return
                
            if is_fix_mode:
                status_color = {
                    "critical": "red",
                    "warning": "yellow", 
                    "moderate": "blue",
                    "healthy": "green"
                }.get(disk_analysis.get("status", "unknown"), "gray")
                
                click.echo(click.style(
                    f"  Dysk: {disk_analysis['usage_percent']:.1f}% zajęty "
                    f"({disk_analysis['used_gb']:.1f}GB / {disk_analysis['total_gb']:.1f}GB)",
                    fg=status_color
                ))
                
                suggestions = disk_analysis.get("suggestions", [])
                if suggestions:
                    safe_suggestions = [s for s in suggestions if s.get("safe", False)]
                    total_safe_gb = sum(s.get("size_gb", 0) for s in safe_suggestions)
                    
                    if total_safe_gb > 0.1:
                        click.echo(click.style(
                            f"  Można bezpiecznie zwolnić: {total_safe_gb:.1f}GB w {len(safe_suggestions)} akcjach",
                            fg="green"
                        ))
            else:
                click.echo(click.style(f"\nAnaliza dysku:", fg="cyan"))
                click.echo(f"  📈 Użycie: {disk_analysis['usage_percent']:.1f}%")
                click.echo(f"  Zajęte: {disk_analysis['used_gb']:.1f} GB")
                click.echo(f"  🆓 Wolne: {disk_analysis['free_gb']:.1f} GB")
                click.echo(f"  📁 Status: {disk_analysis['status']}")
                
                suggestions = disk_analysis.get("suggestions", [])
                if suggestions:
                    click.echo(click.style(f"\nSugestie czyszczenia:", fg="yellow"))
                    for suggestion in suggestions[:5]:
                        safe_icon = "" if suggestion.get("safe") else ""
                        click.echo(f"  {safe_icon} {suggestion['description']} ({suggestion.get('size_gb', 0):.1f}GB)")
        else:
            click.echo(click.style(f"{'  ' if is_fix_mode else ''}Błąd analizy dysku: {disk_analysis['error']}", fg="red"))
            
    except ImportError:
        click.echo(click.style(f"{'  ' if is_fix_mode else ''}Moduł analizy dysku nie jest dostępny", fg="yellow"))
    except Exception as e:
        click.echo(click.style(f"{'  ' if is_fix_mode else ''}Błąd podczas analizy dysku: {str(e)}", fg="red"))

def _print_quick_issues(data: dict):
    """Wyświetla szybki przegląd problemów z zebranych danych."""
    click.echo(click.style("\nSzybki przegląd problemów:", fg="cyan"))
    issues = []

    # Sprawdź audio
    audio = data.get("audio", {})
    if "brak" in str(audio.get("alsa_cards", "")).lower() or not audio.get("alsa_cards","").strip() or audio.get("alsa_cards","") == "(brak outputu)":
        issues.append("Dźwięk: brak kart ALSA – prawdopodobnie brak sterownika SOF")
    if "failed" in str(audio.get("pipewire_status", "")).lower():
        issues.append("PipeWire: usługa failed")
    if "failed" in str(audio.get("wireplumber_status", "")).lower():
        issues.append("WirePlumber: usługa failed")

    # Sprawdź thumbnails
    thumb = data.get("thumbnails", {})
    thumb_count = str(thumb.get("thumbnail_cache_count", "0")).strip()
    if thumb_count == "0":
        issues.append("Thumbnails: pusty cache – brak podglądów")
    if "nie zainstalowany" in str(thumb.get("ffmpegthumbnailer", "")):
        issues.append("ffmpegthumbnailer: nie zainstalowany")
    if "nie znaleziony" in str(thumb.get("totem_thumb", "")):
        issues.append("totem-video-thumbnailer: nie znaleziony")

    # Sprawdź system
    sys_data = data.get("system", {})
    failed = str(sys_data.get("systemctl_failed", "")).strip()
    if failed and failed != "(brak outputu)" and "0 loaded" not in failed:
        issues.append(f"systemctl: usługi failed:\n    {failed[:200]}")

    if not issues:
        click.echo("  Brak oczywistych problemów w zebranych danych.")
    else:
        for issue in issues:
            click.echo(f"  {issue}")
        click.echo(f"\n  Uruchom 'fixos fix' aby naprawić z pomocą AI.")


# ══════════════════════════════════════════════════════════
#  fixos fix
# ══════════════════════════════════════════════════════════

@cli.command()
@add_common_options
@click.option("--mode", type=click.Choice(["hitl", "autonomous"]), default=None,
              help="Tryb: hitl (domyślny) lub autonomous")
@click.option("--timeout", default=300, show_default=True,
              help="Timeout sesji agenta (sekundy)")
@click.option("--modules", "-M", default=None,
              help="Moduły diagnostyki: audio,thumbnails,hardware,system")
@click.option("--no-show-data", is_flag=True, default=False,
              help="Nie pokazuj danych diagnostycznych (tylko podsumowanie)")
@click.option("--output", "-o", default=None, help="Zapisz log sesji do JSON")
@click.option("--max-fixes", default=10, show_default=True,
              help="Maksymalna liczba napraw w sesji")
@add_shared_options
def fix(provider, token, model, no_banner, mode, timeout, modules, no_show_data, output, max_fixes,
        disc, dry_run, interactive, json_output, llm_fallback):
    """
    Przeprowadza pełną diagnostykę i uruchamia sesję naprawczą z LLM.

    \b
    Tryby:
      hitl        – Human-in-the-Loop (pyta o każdą akcję) [domyślny]
      autonomous  – Agent sam wykonuje komendy (UWAGA: wymaga potwierdzenia)

    \b
    Opcje dyskowe:
      --disc      – Analiza zajętości dysku + grupowanie przyczyn
      --dry-run   – Symulacja bez wykonywania akcji
      --interactive – Tryb interaktywny (domyślnie włączony)
      --json      – Wyjście w formacie JSON
      --llm-fallback – Użyj LLM gdy heurystyki nie wystarczą

    \b
    Przykłady:
      fixos fix                              # domyślnie hitl + Gemini z .env
      fixos fix --disc                       # z analizą dysku
      fixos fix --disc --dry-run             # analiza dysku bez wykonywania
      fixos fix --mode autonomous            # tryb autonomiczny
      fixos fix --modules audio,thumbnails   # tylko audio i thumbnails
      fixos fix --provider openai --token sk-...
    """
    if not no_banner:
        click.echo(click.style(BANNER, fg="cyan"))

    # Load configuration
    cfg = FixOsConfig.load(
        provider=provider,
        api_key=token,
        model=model,
        agent_mode=mode,
        session_timeout=timeout,
        show_anonymized_data=not no_show_data,
    )

    # Override mode if provided
    if mode:
        cfg.agent_mode = mode

    errors = cfg.validate()
    if errors:
        # No API key - propose interactive provider selection
        click.echo(click.style("\nBrak konfiguracji LLM.", fg="yellow"))
        new_cfg = interactive_provider_setup()
        if new_cfg is None:
            click.echo(click.style("Anulowano. Użyj: fixos llm  aby zobaczyć dostępne providery.", fg="red"))
            sys.exit(1)
        cfg = new_cfg
        errors = cfg.validate()
        if errors:
            for err in errors:
                click.echo(click.style(f"{err}", fg="red"))
            sys.exit(1)

    click.echo(click.style("\nKonfiguracja:", fg="cyan"))
    click.echo(cfg.summary())
    
    if dry_run:
        click.echo(click.style("  Tryb: DRY-RUN (komendy nie będą wykonywane)", fg="yellow"))
    if disc:
        click.echo(click.style("  Analiza dysku: Włączona", fg="blue"))

    # Diagnostics
    selected_modules = modules.split(",") if modules else None
    
    if disc and not modules:
        # Skip heavy system diagnostics if only disk is requested implicitly
        data = {}
    else:
        click.echo(click.style("\nZbieranie diagnostyki...", fg="yellow"))
        def progress(name, desc):
            click.echo(f"  → {desc}...")
        data = get_full_diagnostics(selected_modules, progress_callback=progress)
    
    # Add disk analysis if --disc flag is used
    if disc:
        _run_disk_analysis(data, json_output=json_output, is_fix_mode=True)

    if output:
        anon_str, _ = anonymize(str(data))
        try:
            Path(output).write_text(
                json.dumps({"anonymized": anon_str, "raw": data}, ensure_ascii=False, indent=2, default=str),
                encoding="utf-8"
            )
            click.echo(click.style(f"Raport: {output}", fg="green"))
        except Exception as e:
            click.echo(f"Błąd zapisu: {e}")

    click.echo(click.style("Diagnostyka gotowa.\n", fg="green"))

    # Handle disk analysis mode
    if disc and "disk_analysis" in data:
        return handle_disk_cleanup_mode(data["disk_analysis"], cfg, dry_run, interactive, json_output, llm_fallback)

    # Run appropriate agent mode
    if cfg.agent_mode == "autonomous":
        run_autonomous_session(
            diagnostics=data,
            config=cfg,
            show_data=cfg.show_anonymized_data,
            max_fixes=max_fixes,
        )
    else:
        run_hitl_session(
            diagnostics=data,
            config=cfg,
            show_data=cfg.show_anonymized_data,
        )


def handle_disk_cleanup_mode(disk_analysis: Dict[str, Any], cfg, dry_run: bool, 
                           interactive: bool, json_output: bool, llm_fallback: bool):
    """Handle disk cleanup mode with interactive planning"""
    from .interactive.cleanup_planner import CleanupPlanner
    
    suggestions = disk_analysis.get("suggestions", [])
    if not suggestions:
        click.echo(click.style("Brak sugestii czyszczenia dysku.", fg="green"))
        return
    
    # Create cleanup plan
    planner = CleanupPlanner()
    plan = planner.create_cleanup_plan(suggestions)
    
    if json_output:
        import json
        click.echo(json.dumps(plan, indent=2, default=str))
        return
    
    # Display plan summary
    summary = plan["summary"]
    click.echo(click.style(f"\nPlan czyszczenia dysku:", fg="cyan"))
    click.echo(f"  🔢 Akcje: {summary['total_actions']}")
    click.echo(f"  Miejsce: {summary['total_size_gb']:.1f} GB")
    click.echo(f"  Bezpieczne: {summary['safe_size_gb']:.1f} GB")
    click.echo(f"  📂 Kategorie: {summary['categories_count']}")
    
    # Show categories
    for category_id, category_data in plan["categories"].items():
        info = category_data["info"]
        click.echo(f"\n{info['icon']} {info['name']}:")
        click.echo(f"  📁 Akcje: {category_data['actions_count']}")
        click.echo(f"  Miejsce: {category_data['total_size_gb']:.1f} GB")
        
        # Show top actions
        for action in category_data["actions"][:3]:
            safe_icon = "" if action["safe"] else ""
            priority_icon = {"critical": "", "high": "", "medium": "", "low": ""}.get(action["priority"], "")
            click.echo(f"    {safe_icon} {priority_icon} {action['description']} ({action['size_gb']:.1f}GB)")
    
    # Show recommendations
    recommendations = plan.get("recommendations", [])
    if recommendations:
        click.echo(click.style(f"\nRekomendacje:", fg="yellow"))
        for rec in recommendations:
            priority_color = {"high": "red", "medium": "yellow", "low": "blue"}.get(rec["priority"], "gray")
            click.echo(click.style(f"  🎯 {rec['title']}", fg=priority_color))
            click.echo(f"     {rec['description']}")
    
    if dry_run:
        click.echo(click.style("\nTryb DRY-RUN - żadne akcje nie zostaną wykonane", fg="yellow"))
        return
    
    if interactive:
        selection = planner.interactive_selection(plan)
        click.echo(click.style(f"\nWybrano {selection['total_selected']} akcji do wykonania", fg="green"))
        click.echo(click.style(f"Szacowane miejsce: {selection['estimated_space_gb']:.1f} GB", fg="green"))
        
        # Execute selected actions
        execute_cleanup_actions(selection["selected_actions"], cfg, llm_fallback)
    else:
        # Auto-execute safe actions
        safe_actions = [a for a in plan["prioritized_actions"] if a.get("safe", False)]
        if safe_actions:
            click.echo(click.style(f"\nAutomatyczne wykonanie {len(safe_actions)} bezpiecznych akcji", fg="blue"))
            execute_cleanup_actions(safe_actions, cfg, llm_fallback)
        else:
            click.echo(click.style("\nBrak bezpiecznych akcji do automatycznego wykonania", fg="yellow"))


def execute_cleanup_actions(actions: List[Dict], cfg, llm_fallback: bool):
    """Execute cleanup actions with safety checks"""
    from .orchestrator.executor import CommandExecutor
    
    executor = CommandExecutor(
        default_timeout=60,
        require_confirmation=False,  # Already confirmed
        dry_run=False
    )
    
    successful = []
    failed = []
    
    for i, action in enumerate(actions, 1):
        click.echo(f"\n[{i}/{len(actions)}] {action['description']}")
        
        # Pokaż podgląd plików do usunięcia przed prośbą o sudo
        if "preview_command" in action:
            click.echo(click.style("  Pliki do usunięcia:", fg="blue"))
            
            # Najpierw spróbuj bez sudo
            preview = executor.execute_sync(action["preview_command"], add_sudo=False)
            if preview.stdout and preview.stdout.strip():
                lines = preview.stdout.splitlines()
                for line in lines[:8]:
                    click.echo("   - " + line)
                if len(lines) > 8:
                    click.echo(click.style(f"   ...i {len(lines)-8} więcej.", fg="bright_black"))
            else:
                # Jeśli bez sudo nie działa, poinformuj użytkownika że potrzebne są uprawnienia
                click.echo(click.style("   (Wymaga uprawnień sudo do wyświetlenia listy plików)", fg="yellow"))
                
                # Pytaj o potwierdzenie przed użyciem sudo do podglądu
                if click.confirm(click.style("  Pokazać listę plików z użyciem sudo?", fg="yellow")):
                    preview_with_sudo = executor.execute_sync(action["preview_command"], add_sudo=True)
                    if preview_with_sudo.stdout and preview_with_sudo.stdout.strip():
                        lines = preview_with_sudo.stdout.splitlines()
                        for line in lines[:8]:
                            click.echo("   - " + line)
                        if len(lines) > 8:
                            click.echo(click.style(f"   ...i {len(lines)-8} więcej.", fg="bright_black"))
                    else:
                        click.echo(click.style("   (nie znaleziono plików)", fg="bright_black"))
                else:
                    click.echo("   (pominięto podgląd plików)")

        needs_sudo = action.get("command", "").startswith("sudo ") or " sudo " in action.get("command", "")
        if not action.get("safe", False) or needs_sudo:
            # Pytaj o potwierdzenie wykonania akcji
            prompt_msg = "Wykonać tę akcję?" if needs_sudo else "Ta akcja nie jest bezpieczna. Kontynuować?"
            if not click.confirm(click.style(f"  {prompt_msg}", fg="yellow")):
                click.echo("  ⏭️  Pominięto")
                continue
        
        try:
            result = executor.execute_sync(action["command"])
            if result.returncode == 0:
                click.echo(click.style(f"Sukces: {action['description']}", fg="green"))
                successful.append(action)
            else:
                click.echo(click.style(f"Błąd: {action['description']}", fg="red"))
                from rich.syntax import Syntax
                from .utils.terminal import console
                err_text = result.stderr or 'Unknown error'
                syntax = Syntax(err_text, "bash", theme="monokai", word_wrap=True)
                console.print(syntax)
                failed.append(action)
        except Exception as e:
            click.echo(click.style(f"Wyjątek: {str(e)}", fg="red"))
            failed.append(action)
    
    # Summary
    click.echo(click.style(f"\nPodsumowanie:", fg="cyan"))
    click.echo(f"Sukces: {len(successful)}")
    click.echo(f"Błędy: {len(failed)}")
    
    if successful:
        total_freed = sum(a.get("size_gb", 0) for a in successful)
        click.echo(click.style(f"Zwolniono miejsca: ~{total_freed:.1f} GB", fg="green"))
    
    if failed and llm_fallback:
        click.echo(click.style("\nPróba naprawy błędów za pomocą LLM...", fg="yellow"))
        # Implement LLM fallback for failed actions
        try_llm_fallback_for_failures(failed, cfg)


def try_llm_fallback_for_failures(failed_actions: List[Dict], cfg):
    """Use LLM to analyze and suggest fixes for failed cleanup actions"""
    try:
        from .providers.llm import LLMClient
        
        llm = LLMClient(cfg)
        
        for action in failed_actions[:3]:  # Limit to first 3 failures
            prompt = f"""
Cleanup action failed:
- Description: {action['description']}
- Command: {action['command']}
- Path: {action['path']}

Please suggest alternative approaches to clean this up safely.
Respond with JSON format: {{"alternative_commands": ["cmd1", "cmd2"], "explanation": "..."}}
"""
            
            response = llm.chat([{"role": "user", "content": prompt}], max_tokens=200)
            click.echo(click.style(f"Sugestia LLM dla {action['description']}:", fg="blue"))
            click.echo(f"   {response[:200]}...")
            
    except Exception as e:
        click.echo(click.style(f"LLM fallback nieudany: {str(e)}", fg="red"))

#  fixos token
# ══════════════════════════════════════════════════════════

@cli.group()
def token():
    """Zarządzanie tokenami API LLM."""
    pass


@token.command("set")
@click.argument("key")
@click.option("--provider", "-p", default=None, help="Provider (gemini/openai/xai/...)")
@click.option("--env-file", default=None, help="Ścieżka do pliku .env")
def token_set(key, provider, env_file):
    """
    Zapisuje token API do pliku .env.

    \b
    Przykłady:
      fixos token set AIzaSy...          # Gemini (domyślny)
      fixos token set sk-... --provider openai
      fixos token set xai-... --provider xai
    """
    target = Path(env_file) if env_file else Path.cwd() / ".env"

    # Wykryj provider po prefiksie klucza
    if not provider:
        if key.startswith("AIzaSy") or key.startswith("AI"):
            provider = "gemini"
        elif key.startswith("sk-or-"):
            provider = "openrouter"
        elif key.startswith("sk-ant-"):
            provider = "anthropic"
        elif key.startswith("sk-"):
            provider = "openai"
        elif key.startswith("xai-"):
            provider = "xai"
        elif key.startswith("gsk_"):
            provider = "groq"
        else:
            provider = "gemini"  # domyślny

    pdef = PROVIDER_DEFAULTS.get(provider, {})
    key_env = pdef.get("key_env", "API_KEY")

    # Wczytaj istniejący .env lub stwórz nowy
    lines = []
    if target.exists():
        lines = target.read_text(encoding="utf-8").splitlines()

    # Znajdź i zastąp lub dodaj
    key_line = f"{key_env}={key}"
    replaced = False
    for i, line in enumerate(lines):
        if line.startswith(f"{key_env}=") or line.startswith(f"# {key_env}="):
            lines[i] = key_line
            replaced = True
            break

    if not replaced:
        # Dodaj też LLM_PROVIDER jeśli nie ma
        if not any(l.startswith("LLM_PROVIDER=") for l in lines):
            lines.insert(0, f"LLM_PROVIDER={provider}")
        lines.append(key_line)

    target.write_text("\n".join(lines) + "\n", encoding="utf-8")
    target.chmod(0o600)

    masked = f"{key[:8]}...{key[-4:]}" if len(key) > 12 else "***"
    click.echo(click.style(f"Token zapisany: {key_env}={masked}", fg="green"))
    click.echo(f"   Provider: {provider}")
    click.echo(f"   Plik: {target}")


@token.command("show")
def token_show():
    """Pokazuje aktualnie skonfigurowany token (zamaskowany)."""
    cfg = FixOsConfig.load()
    if cfg.api_key:
        key = cfg.api_key
        masked = f"{key[:8]}...{key[-4:]}" if len(key) > 12 else "***"
        click.echo(f"  Provider : {cfg.provider}")
        click.echo(f"  Token    : {masked}")
        click.echo(f"  Env plik : {cfg.env_file_loaded or 'brak'}")
    else:
        click.echo(click.style("  Brak tokena. Użyj: fixos token set <KLUCZ>", fg="red"))


@token.command("clear")
@click.option("--env-file", default=None)
def token_clear(env_file):
    """Usuwa token z pliku .env."""
    target = Path(env_file) if env_file else Path.cwd() / ".env"
    if not target.exists():
        click.echo("  Brak pliku .env.")
        return

    lines = target.read_text(encoding="utf-8").splitlines()
    key_patterns = [f"{p.get('key_env','API_KEY')}=" for p in PROVIDER_DEFAULTS.values()]
    new_lines = [l for l in lines if not any(l.startswith(p) for p in key_patterns)]
    target.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    click.echo(click.style("Token usunięty.", fg="green"))


# ══════════════════════════════════════════════════════════
#  fixos config
# ══════════════════════════════════════════════════════════

@cli.group()
def config():
    """Zarządzanie konfiguracją fixos."""
    pass


@config.command("show")
def config_show():
    """Wyświetla aktualną konfigurację."""
    cfg = FixOsConfig.load()
    click.echo(click.style("\nAktualna konfiguracja:", fg="cyan"))
    click.echo(cfg.summary())
    errors = cfg.validate()
    if errors:
        click.echo(click.style("\nBłędy konfiguracji:", fg="red"))
        for e in errors:
            click.echo(f"  • {e}")


@config.command("init")
@click.option("--force", is_flag=True, default=False, help="Nadpisz istniejący .env")
def config_init(force):
    """Tworzy plik .env na podstawie szablonu .env.example."""
    target = Path.cwd() / ".env"
    example = Path(__file__).parent.parent / ".env.example"

    if target.exists() and not force:
        click.echo(f"  Plik {target} już istnieje. Użyj --force aby nadpisać.")
        return

    if example.exists():
        import shutil
        shutil.copy(example, target)
    else:
        # Minimalny template
        target.write_text(
            "LLM_PROVIDER=gemini\n"
            "GEMINI_API_KEY=\n"
            "AGENT_MODE=hitl\n"
            "SESSION_TIMEOUT=3600\n"
            "SHOW_ANONYMIZED_DATA=true\n"
            "ENABLE_WEB_SEARCH=true\n",
            encoding="utf-8"
        )
    target.chmod(0o600)
    click.echo(click.style(f"Utworzono {target}", fg="green"))
    click.echo(f"   Edytuj go: nano {target}")
    click.echo(f"   Następnie: fixos token set TWOJ_KLUCZ")


@config.command("set")
@click.argument("key")
@click.argument("value")
def config_set(key, value):
    """
    Ustawia wartość w pliku .env.

    \b
    Przykłady:
      fixos config set AGENT_MODE autonomous
      fixos config set SESSION_TIMEOUT 1800
      fixos config set LLM_PROVIDER openai
    """
    target = Path.cwd() / ".env"
    lines = target.read_text(encoding="utf-8").splitlines() if target.exists() else []

    replaced = False
    for i, line in enumerate(lines):
        if line.startswith(f"{key}="):
            lines[i] = f"{key}={value}"
            replaced = True
            break
    if not replaced:
        lines.append(f"{key}={value}")

    target.write_text("\n".join(lines) + "\n", encoding="utf-8")
    click.echo(click.style(f"{key}={value}", fg="green"))


# ══════════════════════════════════════════════════════════
#  fixos llm
# ══════════════════════════════════════════════════════════

@cli.command("llm")
@click.option("--free", is_flag=True, default=False, help="Pokaż tylko darmowe providery")
def llm_providers(free):
    """
    Lista providerów LLM z linkami do generowania kluczy API.

    \b
    Po wybraniu providera:
      1. Kliknij lub skopiuj URL z kolumny 'Klucz API'
      2. Zaloguj się i wygeneruj klucz
      3. Uruchom: fixos token set <TWÓJ_KLUCZ> --provider <PROVIDER>
    """
    providers_data = get_providers_list()
    if free:
        providers_data = [p for p in providers_data if p["free_tier"]]

    cfg = FixOsConfig.load()
    current = cfg.provider

    click.echo(click.style("\nDOSTĘPNI PROVIDERZY LLM", fg="cyan", bold=True))
    click.echo(click.style("═" * 72, fg="cyan"))

    for i, p in enumerate(providers_data, 1):
        is_current = p["name"] == current
        free_badge = click.style(" FREE", fg="green", bold=True) if p["free_tier"] else click.style(" PAID", fg="yellow")
        current_badge = click.style(" ◀ aktywny", fg="cyan", bold=True) if is_current else ""

        name_styled = click.style(f"{p['name']:<12}", fg="cyan" if is_current else "white", bold=is_current)
        click.echo(f"  {i:>2}. {name_styled}{free_badge}{current_badge}")
        click.echo(f"       {p['description']}")
        click.echo(f"       Model   : {p['model']}")
        click.echo(f"       Env var : {p['key_env']}")
        url_styled = click.style(p['key_url'], fg="blue", underline=True)
        click.echo(f"       Klucz   : {url_styled}")
        click.echo()

    click.echo(click.style("─" * 72, fg="cyan"))
    click.echo(click.style("  JAK USTAWIĆ KLUCZ API:", fg="yellow", bold=True))
    click.echo()
    click.echo("  1. Skopiuj URL z kolumny 'Klucz API' i otwórz w przeglądarce")
    click.echo("  2. Zaloguj się i wygeneruj nowy klucz API")
    click.echo("  3. Uruchom jedną z poniższych komend:")
    click.echo()
    for p in providers_data:
        if p["key_env"] == "(brak – lokalny)":
            continue
        example_key = _example_key(p["name"])
        cmd = click.style(f"  fixos token set {example_key} --provider {p['name']}", fg="yellow")
        click.echo(cmd)
    click.echo()
    click.echo(click.style("  Tip: ", fg="cyan") + "fixos llm --free   # pokaż tylko darmowe providery")
    click.echo()


def _example_key(provider: str) -> str:
    """Zwraca przykładowy format klucza dla danego providera."""
    examples = {
        "gemini":     "AIzaSy...",
        "openai":     "sk-...",
        "openrouter": "sk-or-v1-...",
        "xai":        "xai-...",
        "anthropic":  "sk-ant-...",
        "mistral":    "<KLUCZ_MISTRAL>",
        "groq":       "gsk_...",
        "together":   "<KLUCZ_TOGETHER>",
        "cohere":     "<KLUCZ_COHERE>",
        "deepseek":   "<KLUCZ_DEEPSEEK>",
        "cerebras":   "<KLUCZ_CEREBRAS>",
        "ollama":     "(brak – lokalny)",
    }
    return examples.get(provider, "<KLUCZ>")


# ══════════════════════════════════════════════════════════
#  fixos providers
# ══════════════════════════════════════════════════════════

@cli.command()
def providers():
    """Lista dostępnych providerów LLM (skrócona). Użyj 'fixos llm' po więcej."""
    providers_data = get_providers_list()
    click.echo(click.style("\nDostępni providerzy LLM:", fg="cyan"))
    for p in providers_data:
        free = click.style("FREE", fg="green") if p["free_tier"] else click.style("PAID", fg="yellow")
        click.echo(f"  {p['name']:<12} [{free}]  {p['model']:<45} {p['key_env']}")
    click.echo("\nSzczegóły + linki do kluczy API:")
    click.echo("  fixos llm")
    click.echo("\nAby ustawić provider:")
    click.echo("  fixos config set LLM_PROVIDER gemini")
    click.echo("  fixos token set AIzaSy... --provider gemini")


# ══════════════════════════════════════════════════════════
#  fixos test-llm
# ══════════════════════════════════════════════════════════

@cli.command("test-llm")
@add_common_options
def test_llm(provider, token, model, no_banner):
    """Testuje połączenie z wybranym providerem LLM."""
    if not no_banner:
        click.echo(click.style(BANNER, fg="cyan"))

    cfg = FixOsConfig.load(provider=provider, api_key=token, model=model)
    errors = cfg.validate()
    if errors:
        for err in errors:
            click.echo(click.style(f"{err}", fg="red"))
        sys.exit(1)

    click.echo(f"\n  Testuję: {cfg.provider} / {cfg.model}")
    click.echo(f"  URL: {cfg.base_url}")

    from .providers.llm import LLMClient, LLMError
    llm = LLMClient(cfg)
    try:
        resp = llm.chat(
            [{"role": "user", "content": "Odpowiedz jednym zdaniem po polsku: co to jest Linux, Windows, macOS?"}],
            max_tokens=100,
        )
        click.echo(click.style(f"\n  Połączenie działa!", fg="green"))
        click.echo(f"  Odpowiedź: {resp[:200]}")
    except Exception as e:
        click.echo(click.style(f"\n  Błąd: {e}", fg="red"))
        sys.exit(1)


# ══════════════════════════════════════════════════════════
#  fixos orchestrate
# ══════════════════════════════════════════════════════════

@cli.command()
@add_common_options
@click.option("--mode", type=click.Choice(["hitl", "autonomous"]), default=None,
              help="Tryb: hitl (domyślny) lub autonomous")
@click.option("--modules", "-M", default=None,
              help="Moduły diagnostyki: audio,thumbnails,hardware,system")
@click.option("--dry-run", is_flag=True, default=False,
              help="Symuluj wykonanie komend bez faktycznego uruchamiania")
@click.option("--max-iterations", default=50, show_default=True,
              help="Maksymalna liczba iteracji napraw")
@click.option("--output", "-o", default=None, help="Zapisz log sesji do JSON")
def orchestrate(provider, token, model, no_banner, mode, modules, dry_run, max_iterations, output):
    """
    Orkiestracja napraw z grafem kaskadowych problemów.

    \b
    Różnica od 'fix':
      - Buduje graf zależności między problemami (DAG)
      - Po każdej naprawie re-diagnozuje i wykrywa nowe problemy
      - LLM ocenia wynik każdej komendy (JSON structured output)
      - Transparentne drzewo problemów z linkowanymi przyczynami

    \b
    Przykłady:
      fixos orchestrate                    # pełna diagnostyka + naprawy
      fixos orchestrate --dry-run          # podgląd bez wykonywania
      fixos orchestrate --modules audio    # tylko problemy audio
      fixos orchestrate --mode autonomous  # bez pytania o każdą komendę
    """
    if not no_banner:
        click.echo(click.style(BANNER, fg="cyan"))

    cfg = FixOsConfig.load(
        provider=provider,
        api_key=token,
        model=model,
        agent_mode=mode,
    )
    if mode:
        cfg.agent_mode = mode

    errors = cfg.validate()
    if errors:
        click.echo(click.style("\nBrak konfiguracji LLM.", fg="yellow"))
        new_cfg = interactive_provider_setup()
        if new_cfg is None:
            click.echo(click.style("Anulowano. Użyj: fixos llm  aby zobaczyć dostępne providery.", fg="red"))
            sys.exit(1)
        cfg = new_cfg
        errors = cfg.validate()
        if errors:
            for err in errors:
                click.echo(click.style(f"{err}", fg="red"))
            sys.exit(1)

    click.echo(click.style("\nKonfiguracja:", fg="cyan"))
    click.echo(cfg.summary())
    if dry_run:
        click.echo(click.style("  Tryb: DRY-RUN (komendy nie będą wykonywane)", fg="yellow"))

    # Diagnostyka
    selected_modules = modules.split(",") if modules else None
    click.echo(click.style("\nZbieranie diagnostyki...", fg="yellow"))

    def progress(name, desc):
        click.echo(f"  → {desc}...")

    data = get_full_diagnostics(selected_modules, progress_callback=progress)
    click.echo(click.style("Diagnostyka gotowa.\n", fg="green"))

    # Inicjalizuj orkiestrator
    from .orchestrator import FixOrchestrator
    from .orchestrator.executor import CommandExecutor

    executor = CommandExecutor(
        default_timeout=120,
        require_confirmation=(cfg.agent_mode == "hitl"),
        dry_run=dry_run,
    )
    orch = FixOrchestrator(config=cfg, executor=executor)

    # Załaduj problemy przez LLM
    click.echo(click.style("🧠 LLM analizuje dane diagnostyczne...", fg="yellow"))
    problems = orch.load_from_diagnostics(data)

    if not problems:
        click.echo(click.style("  LLM nie wykrył problemów wymagających naprawy.", fg="green"))
        return

    from .utils.terminal import console, render_tree_colored
    from rich.rule import Rule
    from rich.panel import Panel
    from rich.text import Text

    console.print(Rule(f"[bold cyan]Graf problemów ({len(problems)} wykrytych)[/bold cyan]", style="cyan"))
    console.print(render_tree_colored(orch.graph.nodes, orch.graph.execution_order))
    console.print()

    # Główna pętla napraw
    summary = orch.run_sync()

    # Podsumowanie
    by_status = summary.get("by_status", {})
    resolved = len(by_status.get("resolved", []))
    failed   = len(by_status.get("failed", []))
    skipped  = len(by_status.get("skipped", []))
    pending  = len(by_status.get("pending", []))
    elapsed  = summary.get("elapsed_seconds", 0)
    summary_text = Text()
    summary_text.append(f"Naprawiono  : {resolved}\n", style="green")
    summary_text.append(f"Nieudane    : {failed}\n", style="red")
    summary_text.append(f"⏭️  Pominięte   : {skipped}\n", style="yellow")
    summary_text.append(f"⏳ Pozostałe   : {pending}\n", style="dim")
    summary_text.append(f"⏱️  Czas sesji  : {elapsed}s", style="dim")
    console.print(Panel(summary_text, title="[bold cyan]PODSUMOWANIE SESJI[/bold cyan]", border_style="cyan"))
    console.print()
    console.print("[cyan]  Aktualny stan grafu:[/cyan]")
    console.print(render_tree_colored(orch.graph.nodes, orch.graph.execution_order))

    if output:
        try:
            Path(output).write_text(
                json.dumps({
                    "summary": summary,
                    "log": orch.session_log,
                    "graph": {pid: p.to_summary() for pid, p in orch.graph.nodes.items()},
                }, ensure_ascii=False, indent=2, default=str),
                encoding="utf-8"
            )
            click.echo(click.style(f"\nLog sesji: {output}", fg="green"))
        except Exception as e:
            click.echo(f"Błąd zapisu: {e}")


def _cleanup_flatpak_detailed(scanner, json_output: bool, dry_run: bool):
    """
    Detailed interactive Flatpak cleanup showing unused runtimes, 
    leftover data, and orphaned apps for user selection.
    """
    from .diagnostics.flatpak_analyzer import FlatpakAnalyzer
    
    analyzer = FlatpakAnalyzer()
    analysis = analyzer.analyze()
    
    # JSON output mode
    if json_output:
        import json
        click.echo(json.dumps(analysis, indent=2, default=str))
        return
    
    # Interactive mode
    click.echo(click.style("\n=== Analiza Flatpak ===", fg="cyan", bold=True))
    click.echo(click.style("═" * 60, fg="cyan"))
    
    if dry_run:
        click.echo(click.style("[TRYB DRY-RUN] - brak faktycznych zmian\n", fg="yellow"))
    
    # Collect all removable items
    all_items = []
    
    # Unused runtimes
    if analysis.get("unused_runtimes"):
        click.echo(click.style("\nNieużywane runtimes:", fg="yellow", bold=True))
        for i, rt in enumerate(analysis["unused_runtimes"], 1):
            size = rt.get("size_human", "?")
            name = rt.get("name", "unknown")
            ref = rt.get("ref", "")
            click.echo(f"  [{i}] {click.style(name, fg='white')} - {size}")
            click.echo(f"      Ref: {ref}")
            all_items.append({
                "type": "runtime",
                "name": name,
                "ref": ref,
                "size_human": size,
                "cleanup_command": f"flatpak uninstall {ref} -y"
            })
    
    # Leftover data from uninstalled apps
    if analysis.get("leftover_data"):
        click.echo(click.style("\nPozostałości po odinstalowanych aplikacjach:", fg="yellow", bold=True))
        offset = len(all_items)
        for i, data in enumerate(analysis["leftover_data"], offset + 1):
            size = data.get("size_human", "?")
            name = data.get("name", "unknown")
            click.echo(f"  [{i}] {click.style(name, fg='white')} - {size}")
            click.echo(f"      Ścieżka: ~/.var/app/{name}")
            all_items.append({
                "type": "data",
                "name": name,
                "ref": data.get("ref", ""),
                "size_human": size,
                "cleanup_command": f"rm -rf ~/.var/app/{name}"
            })
    
    # Orphaned apps
    if analysis.get("orphaned_apps"):
        click.echo(click.style("\nOsierocone aplikacje (niedostępny remote):", fg="red", bold=True))
        offset = len(all_items)
        for i, app in enumerate(analysis["orphaned_apps"], offset + 1):
            size = app.get("size_human", "?")
            name = app.get("name", "unknown")
            origin = app.get("origin", "unknown")
            click.echo(f"  [{i}] {click.style(name, fg='white')} - {size}")
            click.echo(f"      Origin: {origin} (niedostępny)")
            all_items.append({
                "type": "orphan",
                "name": name,
                "ref": app.get("ref", ""),
                "size_human": size,
                "cleanup_command": f"flatpak uninstall {app.get('ref', '')} -y"
            })
    
    if not all_items:
        click.echo(click.style("\nBrak elementów do wyczyszczenia!", fg="green"))
        return
    
    # Show summary
    total_items = len(all_items)
    total_bytes = (
        analysis.get("total_unused_bytes", 0) + 
        analysis.get("total_leftover_bytes", 0) + 
        analysis.get("total_orphaned_bytes", 0)
    )
    total_gb = total_bytes / (1024**3)
    
    click.echo(click.style(f"\n═" * 60, fg="cyan"))
    click.echo(f"Znaleziono {total_items} elementów do usunięcia ({total_gb:.2f} GB)")
    click.echo()
    
    # Interactive selection
    click.echo("Wybierz elementy do usunięcia:")
    click.echo("  - Wpisz numery rozdzielone przecinkami (np. 1,3,5)")
    click.echo("  - Wpisz 'all' aby usunąć wszystko")
    click.echo("  - Wciśnij Enter aby pominąć")
    
    selection = click.prompt("Wybór", default="", show_default=False)
    
    if not selection:
        click.echo(click.style("Anulowano.", fg="yellow"))
        return
    
    # Parse selection
    selected_indices = []
    if selection.strip().lower() == "all":
        selected_indices = list(range(len(all_items)))
    else:
        try:
            selected_indices = [
                int(x.strip()) - 1 
                for x in selection.split(",") 
                if x.strip().isdigit()
            ]
            selected_indices = [i for i in selected_indices if 0 <= i < len(all_items)]
        except ValueError:
            click.echo(click.style("Nieprawidłowy wybór.", fg="red"))
            return
    
    if not selected_indices:
        click.echo(click.style("Nie wybrano żadnych elementów.", fg="yellow"))
        return
    
    # Execute cleanup
    click.echo()
    freed_total = 0
    
    for idx in selected_indices:
        item = all_items[idx]
        item_type = item["type"]
        name = item["name"]
        cmd = item["cleanup_command"]
        
        click.echo(f"Czyszczenie: {name} ({item_type})")
        
        if dry_run:
            click.echo(click.style(f"  [DRY-RUN] {cmd}", fg="cyan"))
            continue
        
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                click.echo(click.style("  OK", fg="green"))
                # Parse size
                size_str = item.get("size_human", "0")
                freed_total += _parse_size_to_gb(size_str)
            else:
                click.echo(click.style(f"  Błąd: {result.stderr[:100]}", fg="red"))
        except Exception as e:
            click.echo(click.style(f"  Błąd: {e}", fg="red"))
    
    click.echo()
    if dry_run:
        click.echo(click.style(f"[DRY-RUN] Zwolniono by: {freed_total:.2f} GB", fg="cyan"))
    else:
        click.echo(click.style(f"Zwolniono: {freed_total:.2f} GB", fg="green"))


def _parse_size_to_gb(size_str: str) -> float:
    """Parse human-readable size to GB"""
    size_str = size_str.strip().upper()
    multipliers = {
        'B': 1 / (1024**3),
        'KB': 1 / (1024**2),
        'MB': 1 / 1024,
        'GB': 1,
        'TB': 1024,
    }
    
    for suffix, mult in sorted(multipliers.items(), key=lambda x: -len(x[0])):
        if size_str.endswith(suffix):
            try:
                return float(size_str[:-len(suffix)].strip()) * mult
            except ValueError:
                return 0
    
    try:
        return float(size_str) / (1024**3)
    except ValueError:
        return 0


# ══════════════════════════════════════════════════════════
#  fixos cleanup-services
# ══════════════════════════════════════════════════════════

@cli.command("cleanup")
@click.option("--threshold", "-t", default=500, type=int,
              help="Próg wielkości w MB (domyślnie 500MB)")
@click.option("--services", "-s", default=None,
              help="Usługi do przeskanowania: docker,ollama,npm,pip,... (domyślnie wszystkie)")
@click.option("--json", "json_output", is_flag=True, default=False,
              help="Wyjście w formacie JSON")
@click.option("--cleanup", "-c", default=None,
              help="Wyczyść konkretną usługę (docker, ollama, npm, ...)")
@click.option("--dry-run", is_flag=True, default=False,
              help="Symuluj czyszczenie bez faktycznego usuwania")
@click.option("--list", "list_only", is_flag=True, default=False,
              help="Tylko wyświetl listę bez interakcji")
def cleanup_services(threshold, services, json_output, cleanup, dry_run, list_only):
    """
    Skanuje i czyści dane usług przekraczające próg.

    \b
    Wyszukuje dane usług (Docker, Ollama, npm, pip, yarn, pnpm, conda,
    gradle, cargo, go, flutter, android, chrome, vscode, huggingface,
    terraform, snap, flatpak, brew, nix, i wiele innych) które zajmują
    więcej miejsca niż podany próg (domyślnie 500MB) i pozwala je usunąć.

    \b
    Dostępne usługi:
      docker, ollama, podman          - kontenery
      npm, yarn, pnpm                 - pakiety JS/Node
      pip, conda, poetry              - pakiety Python
      gradle, maven, cargo, go        - pakiety Java/Rust/Go
      flutter, dart, android          - mobile development
      apt, dnf, pacman, snap, flatpak - pakiety systemowe
      chrome, firefox, edge           - przeglądarki
      vscode, cursor, jetbrains       - edytory/IDE
      huggingface                     - modele AI/ML
      terraform, pulumi               - infrastructure as code
      gcloud, aws, azure              - cloud CLI
      vagrant, vbox, vmware           - wirtualizacja
      nix, brew                       - menedżery pakietów
      unity, unreal                   - silniki gier
      thumbnails, trash, logs         - systemowe

    \b
    Przykłady:
      fixos cleanup                    # skanuj wszystkie usługi
      fixos cleanup -t 1000           # próg 1000MB (1GB)
      fixos cleanup -s docker,ollama  # tylko Docker i Ollama
      fixos cleanup -s npm,yarn,pnpm # wszystkie menedżery JS
      fixos cleanup --list              # tylko lista, bez czyszczenia
      fixos cleanup -c docker --dry-run  # symulacja czyszczenia Dockera
      fixos cleanup -c chrome         # wyczyść cache Chrome
    """
    from .diagnostics.service_scanner import ServiceDataScanner, ServiceType

    # Initialize scanner with threshold
    scanner = ServiceDataScanner(threshold_mb=threshold)

    # Handle specific cleanup
    if cleanup:
        # Special handling for flatpak - show detailed breakdown
        if cleanup == "flatpak":
            _cleanup_flatpak_detailed(scanner, json_output, dry_run)
            return
            
        if json_output:
            result = scanner.cleanup_service(cleanup, dry_run=dry_run)
            import json
            click.echo(json.dumps(result, indent=2, default=str))
        else:
            click.echo(click.style(f"Czyszczenie usługi: {cleanup}", fg="yellow"))
            if dry_run:
                click.echo(click.style("[TRYB DRY-RUN] - brak faktycznych zmian", fg="cyan"))

            result = scanner.cleanup_service(cleanup, dry_run=dry_run)

            if result["success"]:
                click.echo(click.style(f"Zakończono czyszczenie {cleanup}", fg="green"))
                if result["space_freed_gb"] > 0:
                    click.echo(f"  Zwolniono: {result['space_freed_gb']:.2f} GB")
            else:
                click.echo(click.style(f"Błąd: {result.get('error', 'Nieznany błąd')}", fg="red"))
                if result.get("output"):
                    click.echo(f"Output: {result['output']}")
        return

    # Parse services filter
    service_filter = None
    if services:
        service_filter = [s.strip() for s in services.split(",")]

    # Get cleanup plan
    plan = scanner.get_cleanup_plan(selected_services=service_filter)

    # JSON output
    if json_output:
        import json
        click.echo(json.dumps(plan, indent=2, default=str))
        return

    # Display results
    click.echo(click.style(f"\nSkanowanie usług (próg: {threshold} MB)...", fg="cyan"))
    click.echo(click.style("═" * 60, fg="cyan"))

    if plan["services_found"] == 0:
        click.echo(click.style("\nNie znaleziono usług powyżej progu.", fg="green"))
        return

    click.echo(f"Znaleziono {plan['services_found']} usług:")
    click.echo(f"  Całkowity rozmiar: {plan['total_size_gb']:.2f} GB")
    click.echo(f"  Bezpieczne do usunięcia: {plan['safe_cleanup_gb']:.2f} GB")
    click.echo(f"  Wymaga przeglądu: {plan['requires_review_gb']:.2f} GB")
    click.echo()

    # Display services
    for svc in plan["services"]:
        size_str = f"{svc['size_gb']:.2f} GB" if svc['size_gb'] >= 1 else f"{svc['size_mb']:.0f} MB"
        safe_icon = " " if svc['safe_to_cleanup'] else " "
        safe_text = "(bezpieczne)" if svc['safe_to_cleanup'] else "(wymaga przeglądu)"

        click.echo(f"{safe_icon} {click.style(svc['name'], fg='yellow', bold=True)} - {size_str}")
        click.echo(f"   {svc['description']}")
        click.echo(f"   Ścieżka: {svc['path']}")
        click.echo(f"   {safe_text}")

        # Show details for specific services
        if svc.get("details"):
            if svc["service_type"] == "docker" and svc["details"].get("components"):
                comps = svc["details"]["components"]
                click.echo(f"   Komponenty: {comps}")
            elif svc["service_type"] == "ollama" and svc["details"].get("models"):
                models = svc["details"]["models"]
                if models:
                    click.echo(f"   Modele: {', '.join(models[:3])}{'...' if len(models) > 3 else ''}")
        click.echo()

    # Interactive mode (unless --list)
    if not list_only and plan["safe_to_cleanup"]:
        safe_total = sum(s['size_gb'] for s in plan["safe_to_cleanup"])
        click.echo(click.style("Bezpieczne do wyczyszczenia:", fg="green"))
        for svc in plan["safe_to_cleanup"]:
            size_str = f"{svc['size_gb']:.2f} GB" if svc['size_gb'] >= 1 else f"{svc['size_mb']:.0f} MB"
            click.echo(f"  • {svc['name']}: {size_str}")

        click.echo()
        if click.confirm(f"Wyczyścić bezpieczne usługi? (zwolni {safe_total:.2f} GB)"):
            for svc in plan["safe_to_cleanup"]:
                svc_type = svc["service_type"]
                click.echo(f"Czyszczenie {svc_type}...")
                result = scanner.cleanup_service(svc_type, dry_run=False)
                if result["success"]:
                    freed = result.get("space_freed_gb", 0)
                    click.echo(click.style(f"  Zwolniono {freed:.2f} GB", fg="green"))
                else:
                    click.echo(click.style(f"  Błąd: {result.get('error', 'nieznany')}", fg="red"))

    # Show cleanup hints for unsafe services
    if plan["requires_review"] and not list_only:
        click.echo()
        click.echo(click.style("Usługi wymagające przeglądu:", fg="yellow"))
        for svc in plan["requires_review"]:
            click.echo(f"  • {svc['name']}: {svc['cleanup_command']}")



# ══════════════════════════════════════════════════════════
#  fixos rollback
# ══════════════════════════════════════════════════════════

@cli.group("rollback")
def rollback():
    """Zarządzanie cofaniem operacji fixOS."""
    pass


@rollback.command("list")
@click.option("--limit", default=20, help="Ile sesji pokazać")
def rollback_list(limit):
    """Pokaż historię sesji naprawczych."""
    from .orchestrator.rollback import RollbackSession

    sessions = RollbackSession.list_sessions(limit)
    if not sessions:
        click.echo("  Brak zapisanych sesji rollback.")
        return

    click.echo(click.style("\nHistoria sesji naprawczych:", fg="cyan"))
    click.echo(click.style("═" * 65, fg="cyan"))
    for s in sessions:
        click.echo(
            f"  {click.style(s['session_id'], fg='yellow')}  "
            f"{s['created_at'][:16]}  "
            f"{s['operations']} ops  "
            f"{s['rollbackable']} rollbackable"
        )
    click.echo()


@rollback.command("show")
@click.argument("session_id")
def rollback_show(session_id):
    """Pokaż szczegóły sesji rollback."""
    from .orchestrator.rollback import RollbackSession

    try:
        session = RollbackSession.load(session_id)
    except FileNotFoundError:
        click.echo(click.style(f"Sesja '{session_id}' nie znaleziona.", fg="red"))
        return

    click.echo(click.style(f"\nSesja: {session.session_id}", fg="cyan"))
    click.echo(f"  Utworzono: {session.created_at}")
    click.echo(f"  Operacji: {len(session.entries)}")
    click.echo()

    for i, entry in enumerate(session.entries, 1):
        status = click.style("OK", fg="green") if entry.success else click.style("FAIL", fg="red")
        click.echo(f"  {i}. [{status}] {entry.command}")
        if entry.rollback_command:
            click.echo(f"     Rollback: {entry.rollback_command}")
        click.echo(f"     Exit: {entry.exit_code}  |  {entry.timestamp[:19]}")
    click.echo()


@rollback.command("undo")
@click.argument("session_id")
@click.option("--last", default=1, help="Ile ostatnich operacji cofnąć")
@click.option("--dry-run", is_flag=True, default=False, help="Tylko pokaż co by się cofnęło")
def rollback_undo(session_id, last, dry_run):
    """Cofnij operacje z podanej sesji."""
    from .orchestrator.rollback import RollbackSession

    try:
        session = RollbackSession.load(session_id)
    except FileNotFoundError:
        click.echo(click.style(f"Sesja '{session_id}' nie znaleziona.", fg="red"))
        return

    commands = session.get_rollback_commands()[:last]
    if not commands:
        click.echo("  Brak operacji do cofnięcia w tej sesji.")
        return

    if dry_run:
        click.echo(click.style("[DRY-RUN] Operacje do cofnięcia:", fg="yellow"))
    else:
        click.echo(click.style("Cofanie operacji:", fg="cyan"))

    results = session.rollback_last(n=last, dry_run=dry_run)
    for r in results:
        click.echo(f"  Cofam: {r['command']}")
        click.echo(f"    → {r['rollback_command']}")
        if r['success'] is None:
            click.echo(click.style("    [DRY-RUN]", fg="yellow"))
        elif r['success']:
            click.echo(click.style("    OK", fg="green"))
        else:
            click.echo(click.style(f"    FAIL: {r['output']}", fg="red"))


# ══════════════════════════════════════════════════════════
#  fixos watch
# ══════════════════════════════════════════════════════════

@cli.command("watch")
@click.option("--interval", "-i", default=300, show_default=True,
              help="Interwał diagnostyki w sekundach")
@click.option("--modules", "-m", default=None,
              help="Moduły diagnostyki: system,security,disk,audio,...")
@click.option("--alert-on", type=click.Choice(["ok", "info", "warning", "critical"]),
              default="critical", show_default=True,
              help="Minimalny poziom alertów")
@click.option("--max-iterations", default=0, show_default=True,
              help="Maksymalna liczba iteracji (0 = bez limitu)")
def watch(interval, modules, alert_on, max_iterations):
    """
    Monitorowanie systemu w tle z powiadomieniami.

    \b
    Wykonuje cykliczną diagnostykę i wysyła powiadomienia
    desktop (notify-send na Linux) gdy pojawią się nowe
    problemy powyżej wybranego poziomu.

    \b
    Przykłady:
      fixos watch                              # co 5 min, alert na critical
      fixos watch -i 60 --alert-on warning     # co minutę, alert na warning
      fixos watch -m system,security -i 120    # system+security co 2 min
    """
    from .watch import WatchDaemon
    from .plugins.base import Severity

    severity_map = {
        "ok": Severity.OK,
        "info": Severity.INFO,
        "warning": Severity.WARNING,
        "critical": Severity.CRITICAL,
    }

    mods = modules.split(",") if modules else None
    daemon = WatchDaemon(
        interval=interval,
        modules=mods,
        alert_on=severity_map[alert_on],
        max_iterations=max_iterations,
    )
    daemon.run()


# ══════════════════════════════════════════════════════════
#  fixos profile
# ══════════════════════════════════════════════════════════

@cli.group("profile")
def profile():
    """Zarządzanie profilami diagnostycznymi."""
    pass


@profile.command("list")
def profile_list():
    """Pokaż dostępne profile diagnostyczne."""
    from .profiles import Profile

    available = Profile.list_available()
    if not available:
        click.echo("  Brak dostępnych profili.")
        return

    click.echo(click.style("\nDostępne profile diagnostyczne:", fg="cyan"))
    click.echo(click.style("═" * 55, fg="cyan"))
    for name in available:
        try:
            p = Profile.load(name)
            mods = ", ".join(p.modules)
            click.echo(f"  {click.style(name, fg='yellow', bold=True)}")
            click.echo(f"    {p.description}")
            click.echo(f"    Moduły: {mods}")
        except Exception:
            click.echo(f"  {click.style(name, fg='yellow')} (błąd ładowania)")
    click.echo()
    click.echo("  Użycie: fixos scan --profile <nazwa>")
    click.echo()


@profile.command("show")
@click.argument("name")
def profile_show(name):
    """Pokaż szczegóły profilu diagnostycznego."""
    from .profiles import Profile
    import yaml

    try:
        p = Profile.load(name)
    except FileNotFoundError as e:
        click.echo(click.style(str(e), fg="red"))
        return

    click.echo(click.style(f"\nProfil: {p.name}", fg="cyan"))
    click.echo(f"  Opis: {p.description}")
    click.echo(f"  Moduły: {', '.join(p.modules)}")
    if p.thresholds:
        click.echo("  Progi:")
        for k, v in p.thresholds.items():
            click.echo(f"    {k}: {v}")
    click.echo()


# ══════════════════════════════════════════════════════════
#  fixos quickfix (v2.3 — heuristic fixes without LLM)
# ══════════════════════════════════════════════════════════

@cli.command("quickfix")
@click.option("--dry-run", is_flag=True, default=False, help="Symuluj bez wykonania")
@click.option("--modules", "-m", default=None, help="Moduły: audio,disk,security,...")
def quickfix(dry_run, modules):
    """
    Natychmiastowe naprawy bez API — baza znanych bugów.

    \b
    Działa offline, zero tokenów. Używa wbudowanych heurystyk
    do naprawy typowych problemów.

    \b
    Przykłady:
      fixos quickfix                    # napraw wszystko co można
      fixos quickfix --dry-run          # podgląd bez wykonywania
      fixos quickfix -m audio,disk      # tylko audio i dysk
    """
    from .plugins.registry import PluginRegistry
    from .plugins.base import Severity

    registry = PluginRegistry()
    registry.discover()

    mods = modules.split(",") if modules else None
    click.echo(click.style("Szybka diagnostyka (bez LLM)...", fg="cyan"))

    results = registry.run(modules=mods)
    fixes_found = 0
    fixes_applied = 0

    for result in results:
        for finding in result.findings:
            if finding.command:
                fixes_found += 1
                click.echo(
                    f"\n  [{finding.severity.value.upper()}] "
                    f"{click.style(finding.title, fg='yellow')}"
                )
                click.echo(f"    {finding.description}")
                if finding.suggestion:
                    click.echo(f"    Sugestia: {finding.suggestion}")
                click.echo(f"    Komenda: {click.style(finding.command, fg='cyan')}")

                if dry_run:
                    click.echo(click.style("    [DRY-RUN] — pominięto", fg="yellow"))
                else:
                    if finding.severity in (Severity.CRITICAL, Severity.WARNING):
                        if click.confirm("    Wykonać?"):
                            import subprocess
                            try:
                                proc = subprocess.run(
                                    finding.command, shell=True,
                                    capture_output=True, text=True, timeout=60,
                                )
                                if proc.returncode == 0:
                                    click.echo(click.style("    OK", fg="green"))
                                    fixes_applied += 1
                                else:
                                    click.echo(click.style(
                                        f"    FAIL (exit {proc.returncode}): {proc.stderr[:200]}",
                                        fg="red",
                                    ))
                            except Exception as e:
                                click.echo(click.style(f"    Błąd: {e}", fg="red"))

    click.echo(click.style(f"\nPodsumowanie quickfix:", fg="cyan"))
    click.echo(f"  Znalezione naprawy: {fixes_found}")
    if not dry_run:
        click.echo(f"  Wykonane: {fixes_applied}")
    click.echo()


# ══════════════════════════════════════════════════════════
#  fixos report (v2.4 — export to HTML/Markdown)
# ══════════════════════════════════════════════════════════

@cli.command("report")
@click.option("--format", "output_format", type=click.Choice(["html", "markdown", "json"]),
              default="html", show_default=True, help="Format raportu")
@click.option("--output", "-o", default=None, help="Ścieżka pliku wyjściowego")
@click.option("--modules", "-m", default=None, help="Moduły diagnostyki")
@click.option("--profile", "-p", default=None, help="Profil diagnostyczny")
def report(output_format, output, modules, profile):
    """
    Eksport wyników diagnostyki do raportu HTML/Markdown/JSON.

    \b
    Przykłady:
      fixos report                           # HTML do stdout
      fixos report -o raport.html            # zapisz HTML
      fixos report --format markdown -o r.md # Markdown
      fixos report --format json -o r.json   # JSON
      fixos report -p server -o server.html  # profil serwera
    """
    from .plugins.registry import PluginRegistry
    import json as json_module
    from datetime import datetime

    registry = PluginRegistry()
    registry.discover()

    # Resolve modules from profile
    mods = None
    if profile:
        from .profiles import Profile
        try:
            prof = Profile.load(profile)
            mods = prof.modules
        except FileNotFoundError as e:
            click.echo(click.style(str(e), fg="red"))
            return
    if modules:
        mods = modules.split(",")

    click.echo(click.style("Generowanie raportu...", fg="yellow"), err=True)
    results = registry.run(modules=mods)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if output_format == "json":
        data = {
            "timestamp": timestamp,
            "results": [r.to_dict() for r in results],
        }
        content = json_module.dumps(data, indent=2, ensure_ascii=False)

    elif output_format == "markdown":
        lines = [
            f"# fixOS Diagnostic Report",
            f"",
            f"**Timestamp:** {timestamp}",
            f"",
        ]
        for r in results:
            status_icon = {"ok": "✅", "warning": "⚠️", "critical": "❌"}.get(r.status.value, "ℹ️")
            lines.append(f"## {status_icon} {r.plugin_name} ({r.status.value})")
            lines.append(f"*Duration: {r.duration_ms:.0f}ms*\n")
            if r.findings:
                for f in r.findings:
                    lines.append(f"- **[{f.severity.value.upper()}]** {f.title}")
                    lines.append(f"  {f.description}")
                    if f.command:
                        lines.append(f"  `{f.command}`")
                    lines.append("")
            else:
                lines.append("Brak problemów.\n")
        content = "\n".join(lines)

    else:  # html
        rows = []
        for r in results:
            for f in r.findings:
                color = {"critical": "#dc3545", "warning": "#ffc107", "ok": "#28a745"}.get(
                    f.severity.value, "#6c757d"
                )
                cmd_html = f"<code>{f.command}</code>" if f.command else ""
                rows.append(
                    f"<tr><td>{r.plugin_name}</td>"
                    f"<td style='color:{color};font-weight:bold'>{f.severity.value.upper()}</td>"
                    f"<td>{f.title}</td><td>{f.description}</td>"
                    f"<td>{cmd_html}</td></tr>"
                )
        table_rows = "\n".join(rows) if rows else "<tr><td colspan='5'>Brak problemów</td></tr>"
        content = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>fixOS Report</title>
<style>
body {{ font-family: -apple-system, sans-serif; max-width: 900px; margin: 2em auto; padding: 0 1em; }}
h1 {{ color: #0d6efd; }}
table {{ width: 100%; border-collapse: collapse; margin: 1em 0; }}
th, td {{ padding: 8px 12px; border: 1px solid #dee2e6; text-align: left; }}
th {{ background: #f8f9fa; }}
code {{ background: #e9ecef; padding: 2px 6px; border-radius: 3px; }}
</style></head><body>
<h1>fixOS Diagnostic Report</h1>
<p><strong>Timestamp:</strong> {timestamp}</p>
<table><thead><tr><th>Module</th><th>Severity</th><th>Issue</th><th>Description</th><th>Fix</th></tr></thead>
<tbody>{table_rows}</tbody></table>
</body></html>"""

    if output:
        Path(output).write_text(content, encoding="utf-8")
        click.echo(click.style(f"Raport zapisany: {output}", fg="green"), err=True)
    else:
        click.echo(content)


# ══════════════════════════════════════════════════════════
#  fixos history (v2.4 — repair history)
# ══════════════════════════════════════════════════════════

@cli.command("history")
@click.option("--limit", default=20, help="Ile sesji pokazać")
@click.option("--json", "json_output", is_flag=True, default=False, help="Wyjście JSON")
def history(limit, json_output):
    """
    Historia napraw fixOS.

    \b
    Pokazuje ostatnie sesje naprawcze z wynikami.

    \b
    Przykłady:
      fixos history              # ostatnie 20 sesji
      fixos history --limit 5    # ostatnie 5 sesji
      fixos history --json       # JSON output
    """
    from .orchestrator.rollback import RollbackSession

    sessions = RollbackSession.list_sessions(limit)
    if json_output:
        import json as json_module
        click.echo(json_module.dumps(sessions, indent=2, ensure_ascii=False))
        return

    if not sessions:
        click.echo("  Brak historii napraw.")
        return

    click.echo(click.style("\nHistoria napraw fixOS:", fg="cyan"))
    click.echo(click.style("═" * 65, fg="cyan"))
    for s in sessions:
        rollback_info = (
            click.style(f" ({s['rollbackable']} cofnięć dostępnych)", fg="green")
            if s['rollbackable'] > 0 else ""
        )
        click.echo(
            f"  {click.style(s['session_id'], fg='yellow')}  "
            f"{s['created_at'][:16]}  "
            f"{s['operations']} operacji{rollback_info}"
        )
    click.echo(f"\n  Szczegóły: fixos rollback show <session_id>")
    click.echo(f"  Cofnięcie: fixos rollback undo <session_id>")
    click.echo()


# ══════════════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════════════

def main():
    cli()


if __name__ == "__main__":
    main()
