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
@click.option("--full", "-f", "full_analysis", is_flag=True, default=False,
              help="Pełna analiza systemu (DNF, kernels, logs, Docker, cache)")
def cleanup_services(threshold, services, json_output, cleanup, dry_run, list_only, full_analysis):
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
      fixos cleanup --full              # pełna analiza systemu
    """
    # Full system analysis
    if full_analysis:
        _cleanup_full_system(json_output, dry_run)
        return
    
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
    Detailed interactive Flatpak cleanup with menu selection.
    
    Wyświetla menu z opcjami i pokazuje korzyści na bazie rzeczywistych danych.
    """
    from fixos.diagnostics.flatpak_analyzer import FlatpakAnalyzer
    
    analyzer = FlatpakAnalyzer()
    
    # Najpierw wykonaj pełną analizę
    click.echo(click.style("\n🔍 Analizuję Flatpak...", fg="cyan"))
    analysis = analyzer.analyze()
    
    # JSON output mode
    if json_output:
        import json
        click.echo(json.dumps(analysis, indent=2, default=str))
        return
    
    # Wyświetl podsumowanie stanu
    _display_flatpak_status(analysis)
    
    # Pobierz rekomendacje
    recommendations = analyzer.get_cleanup_recommendations()
    
    if not recommendations:
        click.echo(click.style("\n✅ Brak rekomendacji czyszczenia - Flatpak jest w dobrym stanie.", fg="green"))
        return
    
    # Wyświetl menu z opcjami
    click.echo("\n" + click.style("="*60, fg="cyan"))
    click.echo(click.style("📋 WYBIERZ OPCJE DO WYKONANIA", fg="cyan", bold=True))
    click.echo(click.style("="*60, fg="cyan"))
    
    if dry_run:
        click.echo(click.style("\n[TRYB DRY-RUN] - brak faktycznych zmian\n", fg="yellow"))
    
    # Wyświetl każdą opcję z korzyściami
    total_potential_savings = 0
    for i, rec in enumerate(recommendations, 1):
        priority_icon = {"critical": "💣", "high": "🔥", "medium": "⚠️", "low": "💡"}.get(rec['priority'], "•")
        risk_color = {"none": "green", "low": "green", "medium": "yellow", "high": "red"}.get(rec['risk'], "white")
        
        click.echo(f"\n{click.style(f'[{i}]', fg='cyan', bold=True)} {priority_icon} {click.style(rec['description'], fg='yellow', bold=True)}")
        click.echo(f"    Komenda: {click.style(rec['action'], fg='white', dim=True)}")
        
        # Korzyść na bazie rzeczywistych danych
        savings = rec.get('estimated_savings', '0 B')
        click.echo(f"    {click.style('Korzyść:', fg='green')} ~{savings}")
        total_potential_savings += _parse_size_to_bytes(savings)
        
        click.echo(f"    {click.style('Ryzyko:', fg='white')} {click.style(rec['risk'].upper(), fg=risk_color)}")
        
        # Dodatkowe info
        if rec.get('items'):
            click.echo(f"    {click.style(f'Elementów: {len(rec["items"])}', fg='white', dim=True)}")
    
    # Podsumowanie potencjalnych korzyści
    click.echo("\n" + click.style("-"*60, fg="cyan"))
    click.echo(f"💰 {click.style('ŁĄCZNA POTENCJALNA KORZYŚĆ:', fg='green', bold=True)} ~{_format_bytes(total_potential_savings)}")
    click.echo(click.style("-"*60, fg="cyan"))
    
    # Menu wyboru
    click.echo(f"\n{click.style('Dostępne opcje:', fg='white', bold=True)}")
    click.echo(f"  {click.style('1,2,3...', fg='cyan')} - wybierz konkretne opcje (np. '1,3')")
    click.echo(f"  {click.style('all', fg='green')}    - wykonaj wszystkie bezpieczne (ryzyko low/none)")
    click.echo(f"  {click.style('critical', fg='red')} - wykonaj tylko krytyczne")
    click.echo(f"  {click.style('none', fg='yellow')}   - pomiń wszystko")
    click.echo(f"  {click.style('?', fg='white')}      - pokaż szczegóły każdej opcji")
    
    # Pytaj o wybór
    click.echo()
    selection = click.prompt(
        click.style("Twój wybór", fg="cyan"),
        default="none",
        show_default=False
    )
    
    # Obsłuż '?'
    if selection.strip() == '?':
        _display_detailed_recommendations(recommendations)
        selection = click.prompt(
            click.style("\nTwój wybór", fg="cyan"),
            default="none",
            show_default=False
        )
    
    # Parsuj wybór
    selected_indices = _parse_selection(selection, len(recommendations))
    
    if not selected_indices:
        click.echo(click.style("\n⏭️ Nie wybrano żadnych akcji.", fg="yellow"))
        return
    
    # Wykonaj wybrane akcje
    results = {
        "executed": [],
        "skipped": [],
        "failed": [],
        "space_reclaimed": 0,
    }
    
    click.echo("\n" + click.style("="*60, fg="cyan"))
    click.echo(click.style("🚀 WYKONYWANIE WYBRANYCH AKCJI", fg="cyan", bold=True))
    click.echo(click.style("="*60, fg="cyan") + "\n")
    
    for idx in selected_indices:
        rec = recommendations[idx]
        click.echo(f"\n[{idx+1}/{len(recommendations)}] {rec['description']}")
        
        if dry_run:
            click.echo(click.style(f"   [DRY-RUN] Wykonano by: {rec['action']}", fg="cyan"))
            results['executed'].append({"action": rec['action'], "dry_run": True})
            savings_bytes = _parse_size_to_bytes(rec.get('estimated_savings', '0 B'))
            results['space_reclaimed'] += savings_bytes
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
    
    # Podsumowanie końcowe
    click.echo("\n" + click.style("="*60, fg="cyan"))
    click.echo(click.style("📊 PODSUMOWANIE", fg="cyan", bold=True))
    click.echo(click.style("="*60, fg="cyan"))
    click.echo(f"   ✅ Wykonano: {len(results['executed'])}")
    click.echo(f"   ⏭️ Pominięto: {len(results['skipped'])}")
    click.echo(f"   ❌ Błędy: {len(results['failed'])}")
    
    freed_gb = results['space_reclaimed'] / (1024**3)
    if dry_run:
        click.echo(click.style(f"\n   💰 [DRY-RUN] Zwolniono by: {freed_gb:.2f} GB", fg="cyan"))
    else:
        click.echo(click.style(f"\n   💰 Odzyskano: {freed_gb:.2f} GB", fg="green"))
    
    click.echo(click.style("="*60 + "\n", fg="cyan"))


def _display_flatpak_status(analysis: dict) -> None:
    """Wyświetl status Flatpak z rzeczywistymi danymi"""
    click.echo("\n" + click.style("="*60, fg="cyan"))
    click.echo(click.style("📊 STATUS FLATPAK", fg="cyan", bold=True))
    click.echo(click.style("="*60, fg="cyan"))
    
    # Aplikacje
    apps_count = len(analysis.get('installed_apps', []))
    apps_size = sum(a.get('size_bytes', 0) for a in analysis.get('installed_apps', []))
    click.echo(f"\n📱 Aplikacje: {click.style(str(apps_count), fg='yellow')} ({_format_bytes(apps_size)})")
    
    # Runtimes
    runtimes_count = len(analysis.get('installed_runtimes', []))
    runtimes_size = sum(r.get('size_bytes', 0) for r in analysis.get('installed_runtimes', []))
    click.echo(f"🔧 Runtime'y: {click.style(str(runtimes_count), fg='yellow')} ({_format_bytes(runtimes_size)})")
    
    # Repo bloat
    repo_bloat = analysis.get('repo_bloat', {})
    if repo_bloat.get('bloat_detected'):
        click.echo(f"\n{click.style('⚠️  PROBLEM: Repo zajmuje za dużo miejsca!', fg='red', bold=True)}")
        click.echo(f"   Repo: {_format_bytes(repo_bloat.get('repo_total_size', 0))}")
        click.echo(f"   Aplikacje+Runtime'y: {_format_bytes(repo_bloat.get('installed_size', 0))}")
        click.echo(f"   Ratio: {repo_bloat.get('ratio', 0):.1f}x (powinno być ~1-1.5x)")
        click.echo(f"   {click.style('Marnotrawstwo:', fg='red')} {_format_bytes(repo_bloat.get('wasted_size', 0))}")
    
    # Duplikaty
    duplicates = analysis.get('duplicate_apps', [])
    if duplicates:
        dup_size = sum(d.get('total_size', 0) for d in duplicates)
        click.echo(f"\n🔄 Duplikaty aplikacji: {click.style(str(len(duplicates)), fg='yellow')} ({_format_bytes(dup_size)})")
        for dup in duplicates[:3]:
            click.echo(f"   • {dup.get('name', '?')} ({dup.get('count', 0)} wersje)")
    
    # Nieużywane runtime'y
    unused = analysis.get('unused_runtimes', [])
    if unused:
        unused_size = analysis.get('total_size_unused', 0)
        click.echo(f"\n🗑️ Nieużywane runtime'y: {click.style(str(len(unused)), fg='yellow')} ({_format_bytes(unused_size)})")
    
    # Leftover data
    leftover = analysis.get('leftover_data', [])
    if leftover:
        leftover_size = analysis.get('total_size_leftover', 0)
        click.echo(f"\n📁 Dane po odinstalowanych: {click.style(str(len(leftover)), fg='yellow')} ({_format_bytes(leftover_size)})")


def _display_detailed_recommendations(recommendations: list) -> None:
    """Wyświetl szczegółowe informacje o każdej rekomendacji"""
    click.echo("\n" + click.style("="*60, fg="cyan"))
    click.echo(click.style("📖 SZCZEGÓŁY REKOMENDACJI", fg="cyan", bold=True))
    click.echo(click.style("="*60, fg="cyan"))
    
    for i, rec in enumerate(recommendations, 1):
        click.echo(f"\n{click.style(f'[{i}]', fg='cyan', bold=True)} {rec['description']}")
        click.echo(click.style("-"*50, fg="white", dim=True))
        click.echo(f"\n{rec['explanation']}")
        
        if rec.get('items'):
            click.echo(f"\nElementy do usunięcia ({len(rec['items'])}):")
            for item in rec['items'][:10]:
                name = item.get('name', '?')
                size = item.get('size_human', '?')
                click.echo(f"  • {name} ({size})")
            if len(rec['items']) > 10:
                click.echo(f"  ... i {len(rec['items']) - 10} więcej")


def _parse_selection(selection: str, max_count: int) -> list:
    """Parsuj wybór użytkownika na listę indeksów"""
    selection = selection.strip().lower()
    
    if selection in ['none', 'n', 'skip', 's', '']:
        return []
    
    if selection == 'all':
        # Wszystkie opcje z ryzykiem low lub none
        return list(range(max_count))
    
    if selection == 'critical':
        # Tylko krytyczne
        return [i for i in range(max_count)]  # TODO: filter by priority
    
    # Parsuj numery
    try:
        indices = []
        for part in selection.split(','):
            part = part.strip()
            if part.isdigit():
                idx = int(part) - 1
                if 0 <= idx < max_count:
                    indices.append(idx)
        return sorted(set(indices))
    except Exception:
        return []


def _parse_size_to_bytes(size_str: str) -> int:
    """Parse human-readable size to bytes"""
    size_str = size_str.strip().upper().replace(' ', '')
    multipliers = {
        'B': 1,
        'KB': 1024,
        'MB': 1024**2,
        'GB': 1024**3,
        'TB': 1024**4,
    }
    
    for suffix, mult in sorted(multipliers.items(), key=lambda x: -len(x[0])):
        if size_str.endswith(suffix):
            try:
                return int(float(size_str[:-len(suffix)].strip()) * mult)
            except ValueError:
                return 0
    
    try:
        return int(float(size_str))
    except ValueError:
        return 0


def _format_bytes(size_bytes: int) -> str:
    """Format bytes to human-readable string"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} PB"


def _cleanup_full_system(json_output: bool, dry_run: bool):
    """
    Full system storage analysis and cleanup.
    
    Analizuje cały system: DNF, kernels, logs, Docker, Podman, cache, etc.
    """
    from fixos.diagnostics.storage_analyzer import StorageAnalyzer
    
    analyzer = StorageAnalyzer()
    
    click.echo(click.style("\n🔍 Analizuję system...", fg="cyan"))
    analysis = analyzer.analyze_full()
    
    # JSON output
    if json_output:
        import json
        click.echo(json.dumps(analysis, indent=2, default=str))
        return
    
    # Display summary
    click.echo(analyzer.get_summary())
    
    if not analysis['items']:
        return
    
    # Show recommendations
    click.echo("\n" + click.style("="*60, fg="cyan"))
    click.echo(click.style("📋 REKOMENDACJE", fg="cyan", bold=True))
    click.echo(click.style("="*60, fg="cyan"))
    
    if dry_run:
        click.echo(click.style("\n[TRYB DRY-RUN] - brak faktycznych zmian\n", fg="yellow"))
    
    # Group items by risk
    safe_items = [item for item in analyzer.items if item.risk in ['none', 'low']]
    medium_items = [item for item in analyzer.items if item.risk == 'medium']
    
    # Safe items
    if safe_items:
        total_safe = sum(item.size_bytes for item in safe_items)
        click.echo(f"\n{click.style('✅ BEZPIECZNE (automatyczne):', fg='green', bold=True)}")
        for item in safe_items[:10]:
            click.echo(f"  • {item.name}: {_format_bytes(item.size_bytes)}")
            click.echo(f"    → {click.style(item.cleanup_command, fg='cyan', dim=True)}")
        click.echo(f"\n  💰 Łącznie: {click.style(_format_bytes(total_safe), fg='green')}")
    
    # Medium risk items
    if medium_items:
        total_medium = sum(item.size_bytes for item in medium_items)
        click.echo(f"\n{click.style('🟡 WYMAGA POTWIERDZENIA:', fg='yellow', bold=True)}")
        for item in medium_items[:5]:
            click.echo(f"  • {item.name}: {_format_bytes(item.size_bytes)}")
            click.echo(f"    → {click.style(item.cleanup_command, fg='cyan', dim=True)}")
        click.echo(f"\n  💰 Łącznie: {click.style(_format_bytes(total_medium), fg='yellow')}")
    
    # Menu
    click.echo("\n" + click.style("-"*60, fg="cyan"))
    click.echo(f"💰 {click.style('ŁĄCZNIE DO ODZYSKANIA:', fg='green', bold=True)} {analysis['total_reclaimable_human']}")
    click.echo(click.style("-"*60, fg="cyan"))
    
    # Show category breakdown for dev_projects
    dev_items = [item for item in analyzer.items if item.category == 'dev_projects']
    if dev_items:
        # Group by dependency type
        dep_types = {}
        for item in dev_items:
            # Extract dep_type from name (e.g., "node_modules (project)" -> "node_modules")
            dep_type = item.name.split(' (')[0] if ' (' in item.name else item.name
            if dep_type not in dep_types:
                dep_types[dep_type] = {"items": [], "total": 0}
            dep_types[dep_type]["items"].append(item)
            dep_types[dep_type]["total"] += item.size_bytes
        
        # Show available types
        click.echo(f"\n{click.style('📦 TYPY ZALEŻNOŚCI:', fg='magenta', bold=True)}")
        for dep_type, data in sorted(dep_types.items(), key=lambda x: -x[1]["total"]):
            count = len(data["items"])
            total = data["total"]
            click.echo(f"  {click.style(dep_type, fg='yellow')}: {count} folderów, {_format_bytes(total)}")
    
    click.echo(f"\n{click.style('Dostępne opcje:', fg='white', bold=True)}")
    click.echo(f"  {click.style('safe', fg='green')}           - wykonaj bezpieczne czyszczenie")
    click.echo(f"  {click.style('all', fg='yellow')}            - wykonaj wszystko (z potwierdzeniem)")
    click.echo(f"  {click.style('type:NAME', fg='magenta')}     - usuń tylko wybrany typ (np. type:node_modules)")
    click.echo(f"  {click.style('types', fg='cyan')}            - pokaż szczegóły typów")
    click.echo(f"  {click.style('none', fg='white')}            - pomiń")
    
    selection = click.prompt(
        click.style("\nTwój wybór", fg="cyan"),
        default="none",
        show_default=False
    )
    
    selection = selection.strip().lower()
    
    if selection in ['none', 'n', '']:
        click.echo(click.style("\n⏭️ Nie wybrano żadnych akcji.", fg="yellow"))
        return
    
    # Show types details
    if selection == 'types':
        click.echo(f"\n{click.style('📦 SZCZEGÓŁY TYPÓW:', fg='magenta', bold=True)}")
        for dep_type, data in sorted(dep_types.items(), key=lambda x: -x[1]["total"]):
            count = len(data["items"])
            total = data["total"]
            click.echo(f"\n{click.style(dep_type, fg='yellow', bold=True)}: {count} folderów, {_format_bytes(total)}")
            for item in data["items"][:5]:
                click.echo(f"  • {item.path}: {_format_bytes(item.size_bytes)}")
            if count > 5:
                click.echo(f"  ... i {count - 5} więcej")
        return
    
    # Execute cleanup
    items_to_clean = []
    
    if selection == 'safe':
        items_to_clean = safe_items
    elif selection == 'all':
        items_to_clean = analyzer.items
    elif selection.startswith('type:'):
        # Filter by type
        selected_type = selection[5:].strip()
        
        # Find matching items
        for item in analyzer.items:
            item_type = item.name.split(' (')[0] if ' (' in item.name else item.name
            if item_type == selected_type or selected_type in item_type:
                items_to_clean.append(item)
        
        if not items_to_clean:
            click.echo(click.style(f"\n❌ Nie znaleziono typu '{selected_type}'", fg="red"))
            return
        
        total_type = sum(item.size_bytes for item in items_to_clean)
        click.echo(click.style(f"\n📦 Wybrano typ '{selected_type}': {len(items_to_clean)} folderów, {_format_bytes(total_type)}", fg="magenta"))
    
    if not items_to_clean:
        return
    
    click.echo("\n" + click.style("="*60, fg="cyan"))
    click.echo(click.style("🚀 WYKONYWANIE CZYSZCZENIA", fg="cyan", bold=True))
    click.echo(click.style("="*60, fg="cyan") + "\n")
    
    results = {"success": 0, "failed": 0, "space_reclaimed": 0}
    
    for item in items_to_clean:
        click.echo(f"\n• {item.name} ({_format_bytes(item.size_bytes)})")
        
        if dry_run:
            click.echo(click.style(f"  [DRY-RUN] Wykonano by: {item.cleanup_command}", fg="cyan"))
            results['success'] += 1
            results['space_reclaimed'] += item.size_bytes
        else:
            # Ask for confirmation on medium risk
            if item.risk == 'medium':
                if not click.confirm(f"  Wykonać {item.cleanup_command}?", default=False):
                    click.echo("  ⏭️ Pominięto")
                    continue
            
            # Execute
            click.echo(f"  🚀 Wykonuję: {item.cleanup_command}")
            try:
                result = subprocess.run(
                    item.cleanup_command.split(),
                    capture_output=True,
                    text=True,
                    timeout=300,
                )
                if result.returncode == 0:
                    click.echo(click.style("  ✅ Sukces", fg="green"))
                    results['success'] += 1
                    results['space_reclaimed'] += item.size_bytes
                else:
                    click.echo(click.style(f"  ❌ Błąd: {result.stderr[:100]}", fg="red"))
                    results['failed'] += 1
            except Exception as e:
                click.echo(click.style(f"  ❌ Błąd: {e}", fg="red"))
                results['failed'] += 1
    
    # Summary
    click.echo("\n" + click.style("="*60, fg="cyan"))
    click.echo(click.style("📊 PODSUMOWANIE", fg="cyan", bold=True))
    click.echo(click.style("="*60, fg="cyan"))
    click.echo(f"   ✅ Sukces: {results['success']}")
    click.echo(f"   ❌ Błędy: {results['failed']}")
    
    if dry_run:
        click.echo(click.style(f"\n   💰 [DRY-RUN] Zwolniono by: {_format_bytes(results['space_reclaimed'])}", fg="cyan"))
    else:
        click.echo(click.style(f"\n   💰 Odzyskano: {_format_bytes(results['space_reclaimed'])}", fg="green"))
    
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
