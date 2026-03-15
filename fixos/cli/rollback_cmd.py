"""
Rollback commands for fixOS CLI
"""
import click
from fixos.orchestrator.rollback import RollbackSession


@click.group("rollback")
def rollback():
    """Zarządzanie cofaniem operacji fixOS."""
    pass


@rollback.command("list")
@click.option("--limit", default=20, help="Ile sesji pokazać")
def rollback_list(limit):
    """Pokaż historię sesji naprawczych."""
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
