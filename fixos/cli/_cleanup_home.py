"""Home directory analysis and cleanup CLI handlers."""

from __future__ import annotations

import click

from fixos.cli._cleanup_utils import _format_bytes, _parse_numeric_range_set
from fixos.constants import MAX_HOME_LARGE_FILES_DISPLAY, MAX_HOME_LARGE_DIRS_DISPLAY


def _display_home_items(large_files: list, large_dirs: list) -> None:
    """Print large files and directories found in home."""
    if large_files:
        click.echo(f"\n{click.style('📄 DUŻE PLIKI (>200MB):', fg='red', bold=True)}")
        for i, f in enumerate(large_files[:MAX_HOME_LARGE_FILES_DISPLAY], 1):
            click.echo(
                f"  [{i:3d}] 📄 {click.style(f['path'], fg='cyan')}: {f['size_human']}"
            )
        if len(large_files) > MAX_HOME_LARGE_FILES_DISPLAY:
            click.echo(
                f"  ... i {len(large_files) - MAX_HOME_LARGE_FILES_DISPLAY} więcej"
            )
    if large_dirs:
        click.echo(
            f"\n{click.style('📁 DUŻE FOLDERY (>500MB):', fg='magenta', bold=True)}"
        )
        offset = len(large_files)
        for i, d in enumerate(large_dirs[:MAX_HOME_LARGE_DIRS_DISPLAY], 1):
            click.echo(
                f"  [{offset + i:3d}] 📁 {click.style(d['path'], fg='yellow')}: {d['size_human']}"
            )
        if len(large_dirs) > MAX_HOME_LARGE_DIRS_DISPLAY:
            click.echo(
                f"  ... i {len(large_dirs) - MAX_HOME_LARGE_DIRS_DISPLAY} więcej"
            )


def _resolve_home_selection(nums: str, large_files: list, large_dirs: list) -> list:
    """Convert index string into the list of selected home items."""
    total_items = len(large_files) + len(large_dirs)
    selected_indices = _parse_numeric_range_set(nums)
    items = []
    for i in selected_indices:
        if 1 <= i <= len(large_files):
            items.append(large_files[i - 1])
        elif len(large_files) < i <= total_items:
            items.append(large_dirs[i - len(large_files) - 1])
    return items


def _remove_home_items(items_to_remove: list) -> None:
    """Delete files/directories and report result."""
    import os
    import shutil

    click.echo(f"\n{click.style('🚀 USUWANIE ELEMENTÓW:', fg='cyan', bold=True)}")
    for item in items_to_remove:
        click.echo(f"\n• {item['path']}")
        try:
            if item.get("type") == "file":
                os.remove(item["path"])
            else:
                shutil.rmtree(item["path"])
            click.echo(click.style("  ✅ Usunięto", fg="green"))
        except Exception as e:
            click.echo(click.style(f"  ❌ Błąd: {e}", fg="red"))


def _show_home_item_info(
    nums: str, large_files: list, large_dirs: list, total_items: int
) -> None:
    """Display info about a single home item by index."""
    import os
    import mimetypes

    try:
        idx = int(nums[5:])
        if 1 <= idx <= len(large_files):
            f = large_files[idx - 1]
            click.echo(
                f"\n{click.style('📦 SZCZEGÓŁY PLIKU:', fg='yellow', bold=True)}"
            )
            click.echo(f"  Ścieżka:   {f['path']}")
            click.echo(f"  Rozmiar:   {f['size_human']}")
            if os.path.exists(f["path"]):
                click.echo(click.style("  ✅ Istnieje", fg="green"))
                mime_type, _ = mimetypes.guess_type(f["path"])
                if mime_type:
                    click.echo(f"  Typ:       {mime_type}")
            else:
                click.echo(click.style("  ⚠️ Nie istnieje", fg="yellow"))
        elif len(large_files) < idx <= total_items:
            d = large_dirs[idx - len(large_files) - 1]
            click.echo(
                f"\n{click.style('📦 SZCZEGÓŁY FOLDERU:', fg='yellow', bold=True)}"
            )
            click.echo(f"  Ścieżka:   {d['path']}")
            click.echo(f"  Rozmiar:   {d['size_human']}")
        else:
            click.echo(click.style(f"❌ Nieprawidłowy numer: {idx}", fg="red"))
    except ValueError:
        click.echo(click.style("❌ Format: info:N (np. info:5)", fg="red"))


def _handle_home_analysis(analyzer, dry_run: bool) -> None:
    """Handle home directory large-file analysis and removal."""
    large_files = getattr(analyzer, "home_large_files", [])
    large_dirs = getattr(analyzer, "home_large_dirs", [])

    if not large_files and not large_dirs:
        click.echo(click.style("\n❌ Brak dużych plików w home do analizy.", fg="red"))
        return

    click.echo(f"\n{click.style('🏠 ANALIZA HOME DIRECTORY:', fg='yellow', bold=True)}")
    click.echo(
        click.style(
            f"Znaleziono {len(large_files)} dużych plików (>200MB) i {len(large_dirs)} folderów (>500MB)",
            fg="white",
        )
    )
    _display_home_items(large_files, large_dirs)

    total_items = len(large_files) + len(large_dirs)
    click.echo(
        f"\n{click.style('💡 Wybierz numery plików/folderów do usunięcia:', fg='cyan')}"
    )
    click.echo(
        click.style(
            "  • Pliki: 1-{}, Foldery: {}-{}".format(
                len(large_files), len(large_files) + 1, total_items
            ),
            fg="white",
        )
    )

    nums = click.prompt(
        click.style(
            "\nWybierz numery (np. 1,3,5-10) lub 'info:N' dla szczegółów", fg="cyan"
        ),
        default="",
    )
    if not nums.strip():
        click.echo(click.style("⏭️ Nie wybrano żadnych elementów.", fg="yellow"))
        return

    nums = nums.strip().lower()
    if nums.startswith("info:"):
        _show_home_item_info(nums, large_files, large_dirs, total_items)
        return

    items_to_remove = _resolve_home_selection(nums, large_files, large_dirs)
    if not items_to_remove:
        click.echo(click.style("❌ Nie wybrano żadnych elementów.", fg="red"))
        return

    click.echo(
        f"\n{click.style('📦 WYBRANE ELEMENTY DO USUNIĘCIA:', fg='red', bold=True)}"
    )
    for i, item in enumerate(items_to_remove, 1):
        icon = "📄" if item.get("type") == "file" else "📁"
        click.echo(
            f"  {i:3d}. {icon} {click.style(item['path'], fg='cyan')}: {item['size_human']}"
        )
    total_size = sum(item["size"] for item in items_to_remove)
    click.echo(
        f"\n{click.style('💰 Łącznie do usunięcia:', fg='red', bold=True)} {_format_bytes(total_size)}"
    )

    if dry_run:
        click.echo(
            click.style("\n[DRY-RUN] - symulacja, nic nie zostanie usunięte", fg="cyan")
        )
        return
    if not click.confirm(
        click.style("\n⚠️ Potwierdzasz usunięcie tych elementów?", fg="yellow"),
        default=False,
    ):
        click.echo(click.style("⏭️ Anulowano.", fg="yellow"))
        return

    _remove_home_items(items_to_remove)
