"""
History command for fixOS CLI
"""
import click


@click.command("history")
@click.option("--limit", default=20, help="Ile sesji pokazać")
@click.option("--json", "json_output", is_flag=True, default=False, help="Wyjście JSON")
def history(limit, json_output) -> None:
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
    from fixos.orchestrator.rollback import RollbackSession

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
