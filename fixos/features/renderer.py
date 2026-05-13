"""
Feature renderer - displays audit results in terminal.
"""

from typing import List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from .catalog import PackageInfo
from .auditor import AuditResult


console = Console()


class FeatureRenderer:
    """Renders audit results for terminal display."""

    @staticmethod
    def render_audit(result: AuditResult) -> None:
        """Render complete audit results."""
        console.print()
        console.print(
            Panel(
                f"[bold cyan]📊 Audyt profilu: {result.profile_name}[/bold cyan]\n"
                f"System: {result.system.distro} | DE: {result.system.desktop_env} | GPU: {result.system.gpu_vendor}",
                border_style="cyan",
            )
        )

        # Summary stats
        total = result.total_packages
        installed = len(result.installed)
        missing = len(result.missing)
        skipped = len(result.skipped)

        console.print()
        console.print(
            f"  [green]✅ Zainstalowane:[/green] {installed}/{total} ({result.completion_pct:.1f}%)"
        )
        console.print(f"  [red]❌ Brakujące:[/red] {missing}")
        if skipped:
            console.print(f"  [yellow]⏭️ Pominięte (warunki):[/yellow] {skipped}")
        console.print()

        # Missing packages table
        if result.missing:
            table = Table(
                title="[bold red]📦 Brakujące pakiety[/bold red]", border_style="red"
            )
            table.add_column("Pakiet", style="cyan")
            table.add_column("Opis", style="white")
            table.add_column("Dostępny jako", style="green")

            for pkg in result.missing[:20]:  # Limit to 20
                source = FeatureRenderer._get_source_info(pkg, result.system.distro)
                table.add_row(pkg.id, pkg.description[:50], source)

            if len(result.missing) > 20:
                table.add_row("...", f"i {len(result.missing) - 20} więcej", "")

            console.print(table)
            console.print()

        # Installed packages (summary)
        if result.installed:
            installed_str = ", ".join([p.id for p in result.installed[:10]])
            if len(result.installed) > 10:
                installed_str += f" ... i {len(result.installed) - 10} więcej"
            console.print(f"[dim]Zainstalowane: {installed_str}[/dim]")
            console.print()

    @staticmethod
    def _get_source_info(pkg: PackageInfo, distro: str) -> str:
        """Get installation source info for package."""
        sources = []

        distro_name = pkg.get_distro_name(distro)
        if distro_name:
            sources.append(f"📦 {distro_name}")

        if pkg.flatpak:
            sources.append("📦 Flatpak")

        if pkg.pip:
            sources.append("🐍 pip")

        if pkg.cargo:
            sources.append("🦀 cargo")

        if pkg.install_script:
            sources.append("📜 script")

        return " | ".join(sources) if sources else "N/D"

    @staticmethod
    def render_package_list(
        packages: List[PackageInfo], title: str = "Pakiety"
    ) -> None:
        """Render a list of packages."""
        if not packages:
            console.print(f"[dim]{title}: brak[/dim]")
            return

        table = Table(title=f"[bold]{title}[/bold]")
        table.add_column("ID", style="cyan")
        table.add_column("Opis", style="white")
        table.add_column("Kategoria", style="yellow")

        for pkg in packages:
            table.add_row(pkg.id, pkg.description[:40], pkg.category)

        console.print(table)

    @staticmethod
    def render_system_info(system) -> None:
        """Render system information."""
        console.print()
        console.print(
            Panel(
                "[bold cyan]🖥️  Informacje o systemie[/bold cyan]", border_style="cyan"
            )
        )

        console.print(
            f"  [bold]OS:[/bold]       {system.distro} {system.distro_version}"
        )
        console.print(
            f"  [bold]Desktop:[/bold]  {system.desktop_env} ({system.display_server})"
        )
        console.print(
            f"  [bold]GPU:[/bold]      {system.gpu_vendor} {system.gpu_model}"
        )
        console.print(f"  [bold]PM:[/bold]       {system.pkg_manager}")
        console.print(
            f"  [bold]Flatpak:[/bold]  {'✅' if system.has_flatpak else '❌'}"
        )
        console.print(
            f"  [bold]Pakiety:[/bold]  {len(system.installed_packages)} zainstalowanych"
        )
        console.print()
