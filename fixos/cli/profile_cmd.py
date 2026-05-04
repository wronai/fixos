"""
Profile commands for fixOS CLI
"""
import click


@click.group("profile")
def profile() -> None:
    """Zarządzanie profilami diagnostycznymi."""
    pass


@profile.command("list")
def profile_list() -> None:
    """Pokaż dostępne profile diagnostyczne."""
    from fixos.profiles import Profile

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
    from fixos.profiles import Profile
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
