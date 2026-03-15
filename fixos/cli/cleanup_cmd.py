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
    click.echo()
    click.echo(click.style("Usługi wymagające przeglądu:", fg="yellow"))
    for svc in services:
        click.echo(f"  • {svc['name']}: {svc['cleanup_command']}")


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
    """
    from fixos.diagnostics.flatpak_analyzer import FlatpakAnalyzer
    
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
