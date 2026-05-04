"""
Orchestrate command for fixOS CLI - advanced repair with problem graph
"""
import click
import json
from pathlib import Path
from fixos.cli.shared import add_common_options, BANNER
from fixos.config import FixOsConfig


@click.command()
@add_common_options
@click.option("--mode", type=click.Choice(["hitl", "autonomous"]), default="hitl",
              help="Tryb wykonania (domyślnie: hitl)")
@click.option("--modules", "-m", default=None,
              help="Moduły diagnostyczne do uruchomienia")
@click.option("--dry-run", is_flag=True, default=False,
              help="Symulacja bez wykonywania komend")
@click.option("--max-iterations", default=10, show_default=True,
              help="Maksymalna liczba iteracji")
@click.option("--output", "-o", default=None,
              help="Zapisz log wykonania do pliku JSON")
def orchestrate(provider: str, token: str, model: str, no_banner: bool, mode: str, modules: str, dry_run: bool, max_iterations: int, output: str) -> None:
    """
    Zaawansowana orkiestracja napraw z grafem problemów.

    \b
    Różnica od 'fix':
      - Buduje graf kaskadowych zależności między problemami
      - Wykonuje naprawy w optymalnej kolejności (topological sort)
      - Śledzi stan wszystkich problemów
      - Obsługuje rollback per operacja

    \b
    Przykłady:
      fixos orchestrate --dry-run          # podgląd bez wykonania
      fixos orchestrate -m audio,disk      # tylko wybrane moduły
      fixos orchestrate --mode autonomous  # tryb autonomiczny
    """
    from fixos.orchestrator.orchestrator import FixOrchestrator
    from fixos.plugins.registry import PluginRegistry

    if not no_banner:
        click.echo(click.style(BANNER, fg="cyan"))

    # Load config
    cfg = FixOsConfig.load(
        provider=provider,
        api_key=token,
        model=model,
        agent_mode=mode,
    )

    if not cfg.api_key:
        click.echo(click.style("\nBrak klucza API. Użyj: fixos token set <KLUCZ>", fg="red"))
        return

    click.echo(click.style("\nOrkiestracja napraw...", fg="cyan", bold=True))
    click.echo(f"  Provider: {cfg.provider}")
    click.echo(f"  Model: {cfg.model}")
    click.echo(f"  Tryb: {mode}")
    if dry_run:
        click.echo(click.style("  [DRY-RUN]", fg="yellow"))
    click.echo()

    # Run diagnostics
    click.echo(click.style("Faza 1: Diagnostyka", fg="yellow"))
    registry = PluginRegistry()
    registry.discover()

    mods = modules.split(",") if modules else None
    results = registry.run(modules=mods)

    # Convert to legacy format for orchestrator
    diagnostics = {r.plugin_name: r.to_dict() for r in results}

    # Build and execute problem graph
    click.echo(click.style("\nFaza 2: Analiza zależności", fg="yellow"))
    
    orch = FixOrchestrator(
        config=cfg,
        dry_run=dry_run,
        max_iterations=max_iterations,
    )

    # Build graph from diagnostics
    orch.build_from_diagnostics(diagnostics)

    click.echo(f"  Wykryto {len(orch.graph.nodes)} problemów")
    click.echo(f"  Zależności: {len(orch.graph.edges)} relacji")

    # Show execution order
    execution_order = orch.get_execution_order()
    click.echo(click.style("\nKolejność wykonania:", fg="cyan"))
    for i, node_id in enumerate(execution_order[:5], 1):
        node = orch.graph.nodes[node_id]
        click.echo(f"  {i}. {node.name}")
    if len(execution_order) > 5:
        click.echo(f"  ... i {len(execution_order) - 5} więcej")

    # Execute
    click.echo(click.style(f"\nFaza 3: Wykonanie (tryb: {mode})", fg="yellow"))
    
    if mode == "hitl":
        result = orch.run_interactive()
    else:
        result = orch.run_autonomous()

    # Summary
    click.echo(click.style("\nPodsumowanie:", fg="cyan", bold=True))
    click.echo(f"  Wykonane operacje: {result['executed']}")
    click.echo(f"  Błędy: {result['failed']}")
    click.echo(f"  Pominięte: {result['skipped']}")
    
    if result['rollback_available']:
        click.echo(click.style(f"\nRollback dostępny: fixos rollback undo {result['session_id']}", fg="green"))

    # Save output
    if output:
        try:
            Path(output).write_text(
                json.dumps({
                    "session_id": result.get('session_id'),
                    "diagnostics": diagnostics,
                    "execution": result,
                    "graph": {pid: p.to_summary() for pid, p in orch.graph.nodes.items()},
                }, ensure_ascii=False, indent=2, default=str),
                encoding="utf-8"
            )
            click.echo(click.style(f"\nLog zapisany: {output}", fg="green"))
        except Exception as e:
            click.echo(f"Błąd zapisu: {e}")
