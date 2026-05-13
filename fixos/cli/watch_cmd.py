"""
Watch daemon command for fixOS CLI
"""

import click
from fixos.plugins.base import Severity


@click.command("watch")
@click.option(
    "--interval",
    "-i",
    default=300,
    show_default=True,
    help="Interwał diagnostyki w sekundach",
)
@click.option(
    "--modules",
    "-m",
    default=None,
    help="Moduły diagnostyki: system,security,disk,audio,...",
)
@click.option(
    "--alert-on",
    type=click.Choice(["ok", "info", "warning", "critical"]),
    default="critical",
    show_default=True,
    help="Minimalny poziom alertów",
)
@click.option(
    "--max-iterations",
    default=0,
    show_default=True,
    help="Maksymalna liczba iteracji (0 = bez limitu)",
)
def watch(interval, modules, alert_on, max_iterations) -> None:
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
    from fixos.watch import WatchDaemon

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
