"""
Cleanup command for fixOS CLI - service data cleanup with detailed flatpak support
"""
import click
import subprocess
from fixos.cli.shared import BANNER
from fixos.diagnostics.service_scanner import ServiceDataScanner
from fixos.config import FixOsConfig


@click.command("cleanup")
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
    Przykłady:
      fixos cleanup                    # skanuj wszystkie usługi
      fixos cleanup -t 1000           # próg 1000MB (1GB)
      fixos cleanup -s docker,ollama  # tylko Docker i Ollama
      fixos cleanup --list              # tylko lista, bez czyszczenia
      fixos cleanup -c docker --dry-run  # symulacja czyszczenia Dockera
    """
    scanner = ServiceDataScanner(threshold_mb=threshold)

    # Handle single service cleanup
    if cleanup:
        if cleanup == "flatpak":
            _cleanup_flatpak_detailed(scanner, json_output, dry_run)
            return
        
        _cleanup_single_service(cleanup, scanner, json_output, dry_run)
        return

    # Parse services filter
    service_filter = services.split(",") if services else None
    plan = scanner.get_cleanup_plan(selected_services=service_filter)

    # JSON output mode
    if json_output:
        import json
        click.echo(json.dumps(plan, indent=2, default=str))
        return

    # Display results
    _display_cleanup_summary(plan, threshold)
    
    if plan["services_found"] == 0:
        return

    for svc in plan["services"]:
        _display_service_item(svc)

    # Interactive cleanup mode
    if not list_only and plan["safe_to_cleanup"]:
        safe_total = sum(s['size_gb'] for s in plan["safe_to_cleanup"])
        click.echo(click.style("Bezpieczne do wyczyszczenia:", fg="green"))
        for svc in plan["safe_to_cleanup"]:
            size_str = f"{svc['size_gb']:.2f} GB" if svc['size_gb'] >= 1 else f"{svc['size_mb']:.0f} MB"
            click.echo(f"  • {svc['name']}: {size_str}")

        click.echo()
        if click.confirm(f"Wyczyścić bezpieczne usługi? (zwolni {safe_total:.2f} GB)"):
            _execute_safe_cleanup(plan["safe_to_cleanup"], scanner)

    # Show unsafe services
    if plan["requires_review"] and not list_only:
        _display_unsafe_services(plan["requires_review"])


def _display_cleanup_summary(plan: dict, threshold: int) -> None:
    """Display cleanup plan summary header."""
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


def _display_service_item(svc: dict) -> None:
    """Display a single service item with details."""
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
            click.echo(f"   Komponenty: {svc['details']['components']}")
        elif svc["service_type"] == "ollama" and svc["details"].get("models"):
            models = svc["details"]["models"]
            if models:
                click.echo(f"   Modele: {', '.join(models[:3])}{'...' if len(models) > 3 else ''}")
    click.echo()


def _execute_safe_cleanup(services: list, scanner) -> float:
    """
    Execute cleanup for safe-to-remove services.
    Returns total space freed in GB.
    """
    total_freed = 0.0
    
    for svc in services:
        svc_type = svc["service_type"]
        click.echo(f"Czyszczenie {svc_type}...")
        result = scanner.cleanup_service(svc_type, dry_run=False)
        
        if result["success"]:
            freed = result.get("space_freed_gb", 0)
            total_freed += freed
            click.echo(click.style(f"  Zwolniono {freed:.2f} GB", fg="green"))
        else:
            click.echo(click.style(f"  Błąd: {result.get('error', 'nieznany')}", fg="red"))
    
    return total_freed


def _display_unsafe_services(services: list) -> None:
    """Display services that require manual review."""
    from fixos.diagnostics.service_cleanup import ServiceCleaner
    from fixos.diagnostics.service_scanner import ServiceType
    
    click.echo()
    click.echo(click.style("Usługi wymagające przeglądu:", fg="yellow"))
    
    # Group services by type for cleaner display
    service_groups = {}
    for svc in services:
        service_type = svc.get('service_type', 'unknown')
        if service_type not in service_groups:
            service_groups[service_type] = []
        service_groups[service_type].append(svc)
    
    # Map service type strings to enum
    type_map = {
        'flatpak': ServiceType.FLATPAK,
        'docker': ServiceType.DOCKER,
        'ollama': ServiceType.OLLAMA,
    }
    
    for service_type, svcs in service_groups.items():
        # Display basic info
        total_size = sum(s.get('size_gb', 0) for s in svcs)
        click.echo(f"\n  • {service_type.title()}: {total_size:.2f} GB")
        
        # Show cleanup commands
        unique_commands = list(set(s['cleanup_command'] for s in svcs))
        for cmd in unique_commands[:2]:  # Show max 2 unique commands
            click.echo(f"    {cmd}")
        if len(unique_commands) > 2:
            click.echo(f"    ... (+{len(unique_commands)-2} more commands)")
        
        # Display hints if available
        service_enum = type_map.get(service_type.lower())
        if service_enum:
            hints = ServiceCleaner.get_cleanup_hints(service_enum, total_size)
            if hints:
                click.echo()
                for hint in hints:
                    if hint.startswith("  "):
                        # Indented commands
                        click.echo(click.style(hint, fg="cyan"))
                    elif hint.startswith("🔥") or hint.startswith("🐳") or hint.startswith("🤖"):
                        # Service headers
                        click.echo(click.style(f"\n    {hint}", fg="yellow", bold=True))
                    elif hint.startswith("💡"):
                        # Tips
                        click.echo(click.style(f"    {hint}", fg="green"))
                    elif hint.startswith("⚠️"):
                        # Warnings
                        click.echo(click.style(f"    {hint}", fg="red"))
                    elif hint.startswith("📊"):
                        # Investigation commands
                        click.echo(click.style(f"    {hint}", fg="blue"))
                    else:
                        # Regular text
                        click.echo(click.style(f"    {hint}", fg="white"))
    
    click.echo()
    click.echo(click.style("💡 Wskazówki: Powyższe komendy są bezpieczne i często odzyskują dużo miejsca", fg="green"))


def _cleanup_single_service(service_name: str, scanner, json_output: bool, dry_run: bool) -> None:
    """Handle cleanup of a single specific service."""
    if json_output:
        result = scanner.cleanup_service(service_name, dry_run=dry_run)
        import json
        click.echo(json.dumps(result, indent=2, default=str))
        return
    
    click.echo(click.style(f"Czyszczenie usługi: {service_name}", fg="yellow"))
    if dry_run:
        click.echo(click.style("[TRYB DRY-RUN] - brak faktycznych zmian", fg="cyan"))

    result = scanner.cleanup_service(service_name, dry_run=dry_run)

    if result["success"]:
        click.echo(click.style(f"Zakończono czyszczenie {service_name}", fg="green"))
        if result["space_freed_gb"] > 0:
            click.echo(f"  Zwolniono: {result['space_freed_gb']:.2f} GB")
    else:
        click.echo(click.style(f"Błąd: {result.get('error', 'Nieznany błąd')}", fg="red"))
        if result.get("output"):
            click.echo(f"Output: {result['output']}")


def _cleanup_flatpak_detailed(scanner, json_output: bool, dry_run: bool):
    """
    Detailed interactive Flatpak cleanup showing unused runtimes, 
    leftover data, and orphaned apps for user selection.
    
    Wyświetla rekomendacje z wyjaśnieniami i pyta użytkownika o zgodę.
    """
    from fixos.diagnostics.flatpak_analyzer import FlatpakAnalyzer
    
    analyzer = FlatpakAnalyzer()
    
    # JSON output mode - tylko analiza
    if json_output:
        analysis = analyzer.analyze()
        import json
        click.echo(json.dumps(analysis, indent=2, default=str))
        return
    
    # Tryb interaktywny z rekomendacjami
    click.echo(click.style("\n" + "="*60, fg="cyan"))
    click.echo(click.style("🔧 FLATPAK CLEANUP RECOMMENDATIONS", fg="cyan", bold=True))
    click.echo(click.style("="*60 + "\n", fg="cyan"))
    
    if dry_run:
        click.echo(click.style("[TRYB DRY-RUN] - brak faktycznych zmian\n", fg="yellow"))
    
    # Pobierz rekomendacje
    recommendations = analyzer.get_cleanup_recommendations()
    
    if not recommendations:
        click.echo(click.style("✅ Brak rekomendacji czyszczenia - Flatpak jest w dobrym stanie.", fg="green"))
        return
    
    # Wyświetl każdą rekomendację
    for i, rec in enumerate(recommendations, 1):
        click.echo(f"\n[{i}/{len(recommendations)}] {click.style(rec['description'], fg='yellow', bold=True)}")
        click.echo(f"   Komenda: {click.style(rec['action'], fg='cyan')}")
        click.echo(f"   Szacowane odzyskanie: {click.style(rec['estimated_savings'], fg='green')}")
        
        # Kolor dla ryzyka
        risk_color = {"none": "green", "low": "green", "medium": "yellow", "high": "red"}.get(rec['risk'], "white")
        click.echo(f"   Ryzyko: {click.style(rec['risk'].upper(), fg=risk_color)}")
        
        # Wyjaśnienie
        click.echo(f"\n   {rec['explanation']}")
        
        # Elementy do usunięcia (jeśli są)
        if rec.get('items'):
            click.echo(f"\n   Elementy ({len(rec['items'])}):")
            for item in rec['items'][:5]:
                click.echo(f"     - {item.get('name', '?')} ({item.get('size_human', '?')})")
            if len(rec['items']) > 5:
                click.echo(f"     ... i {len(rec['items']) - 5} więcej")
    
    click.echo("\n" + click.style("="*60, fg="cyan"))
    
    # Pytaj użytkownika o każdą akcję
    results = {
        "executed": [],
        "skipped": [],
        "failed": [],
        "space_reclaimed": 0,
    }
    
    for i, rec in enumerate(recommendations, 1):
        click.echo(f"\n[{i}/{len(recommendations)}] {rec['description']}")
        
        should_execute = False
        
        # Automatyczne wykonanie dla braku ryzyka
        if rec['risk'] == 'none':
            should_execute = True
            click.echo(click.style("   ▶️ Wykonuję automatycznie (brak ryzyka)...", fg="green"))
        else:
            # Pytaj użytkownika
            risk_text = click.style(f"[RYZYKO: {rec['risk'].upper()}]", fg=risk_color)
            click.echo(f"   {risk_text} Czy wykonać? [y/N] ", nl=False)
            
            try:
                response = input().strip().lower()
                should_execute = response in ['y', 'yes', 't', 'tak']
            except (EOFError, KeyboardInterrupt):
                click.echo("\n   ⏭️ Pomijam...")
                should_execute = False
        
        if should_execute:
            if dry_run:
                click.echo(click.style(f"   [DRY-RUN] Wykonano by: {rec['action']}", fg="cyan"))
                results['executed'].append({"action": rec['action'], "dry_run": True})
            else:
                click.echo(f"   🚀 Wykonuję: {rec['action']}")
                result = analyzer._execute_cleanup_action(rec)
                
                if result['success']:
                    results['executed'].append({
                        "action": rec['action'],
                        "output": result.get('output', ''),
                    })
                    results['space_reclaimed'] += result.get('bytes_reclaimed', 0)
                    click.echo(click.style("   ✅ Sukces", fg="green"))
                else:
                    results['failed'].append({
                        "action": rec['action'],
                        "error": result.get('error', 'Unknown error'),
                    })
                    click.echo(click.style(f"   ❌ Błąd: {result.get('error', 'Unknown error')}", fg="red"))
        else:
            results['skipped'].append(rec['action'])
            click.echo("   ⏭️ Pominięto")
    
    # Podsumowanie
    click.echo("\n" + click.style("="*60, fg="cyan"))
    click.echo(click.style("📊 PODSUMOWANIE", fg="cyan", bold=True))
    click.echo(click.style("="*60, fg="cyan"))
    click.echo(f"   Wykonano: {len(results['executed'])}")
    click.echo(f"   Pominięto: {len(results['skipped'])}")
    click.echo(f"   Błędy: {len(results['failed'])}")
    
    if dry_run:
        click.echo(click.style(f"   [DRY-RUN] Zwolniono by: {results['space_reclaimed'] / (1024**3):.2f} GB", fg="cyan"))
    else:
        freed_gb = results['space_reclaimed'] / (1024**3)
        click.echo(click.style(f"   Odzyskano: {freed_gb:.2f} GB", fg="green"))
    
    click.echo(click.style("="*60 + "\n", fg="cyan"))


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
