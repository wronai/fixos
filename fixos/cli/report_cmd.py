"""
Report command for fixOS CLI
"""
import click
from pathlib import Path


def _render_report_json(results: list, timestamp: str) -> str:
    """Render diagnostic results as a JSON string."""
    import json as json_module
    data = {"timestamp": timestamp, "results": [r.to_dict() for r in results]}
    return json_module.dumps(data, indent=2, ensure_ascii=False)


def _render_report_markdown(results: list, timestamp: str) -> str:
    """Render diagnostic results as a Markdown string."""
    lines = ["# fixOS Diagnostic Report", "", f"**Timestamp:** {timestamp}", ""]
    for r in results:
        status_icon = {"ok": "✅", "warning": "⚠️", "critical": "❌"}.get(r.status.value, "ℹ️")
        lines.append(f"## {status_icon} {r.plugin_name} ({r.status.value})")
        lines.append(f"*Duration: {r.duration_ms:.0f}ms*\n")
        if r.findings:
            for f in r.findings:
                lines.append(f"- **[{f.severity.value.upper()}]** {f.title}")
                lines.append(f"  {f.description}")
                if f.command:
                    lines.append(f"  `{f.command}`")
                lines.append("")
        else:
            lines.append("Brak problemów.\n")
    return "\n".join(lines)


def _render_report_html(results: list, timestamp: str) -> str:
    """Render diagnostic results as an HTML string."""
    rows = []
    for r in results:
        for f in r.findings:
            color = {"critical": "#dc3545", "warning": "#ffc107", "ok": "#28a745"}.get(
                f.severity.value, "#6c757d"
            )
            cmd_html = f"<code>{f.command}</code>" if f.command else ""
            rows.append(
                f"<tr><td>{r.plugin_name}</td>"
                f"<td style='color:{color};font-weight:bold'>{f.severity.value.upper()}</td>"
                f"<td>{f.title}</td><td>{f.description}</td>"
                f"<td>{cmd_html}</td></tr>"
            )
    table_rows = "\n".join(rows) if rows else "<tr><td colspan='5'>Brak problemów</td></tr>"
    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>fixOS Report</title>
<style>
body {{ font-family: -apple-system, sans-serif; max-width: 900px; margin: 2em auto; padding: 0 1em; }}
h1 {{ color: #0d6efd; }}
table {{ width: 100%; border-collapse: collapse; margin: 1em 0; }}
th, td {{ padding: 8px 12px; border: 1px solid #dee2e6; text-align: left; }}
th {{ background: #f8f9fa; }}
code {{ background: #e9ecef; padding: 2px 6px; border-radius: 3px; }}
</style></head><body>
<h1>fixOS Diagnostic Report</h1>
<p><strong>Timestamp:</strong> {timestamp}</p>
<table><thead><tr><th>Module</th><th>Severity</th><th>Issue</th><th>Description</th><th>Fix</th></tr></thead>
<tbody>{table_rows}</tbody></table>
</body></html>"""


@click.command("report")
@click.option("--format", "output_format", type=click.Choice(["html", "markdown", "json"]),
              default="html", show_default=True, help="Format raportu")
@click.option("--output", "-o", default=None, help="Ścieżka pliku wyjściowego")
@click.option("--modules", "-m", default=None, help="Moduły diagnostyki")
@click.option("--profile", "-p", default=None, help="Profil diagnostyczny")
def report(output_format, output, modules, profile):
    """
    Eksport wyników diagnostyki do raportu HTML/Markdown/JSON.

    \b
    Przykłady:
      fixos report                           # HTML do stdout
      fixos report -o raport.html            # zapisz HTML
      fixos report --format markdown -o r.md # Markdown
      fixos report --format json -o r.json   # JSON
      fixos report -p server -o server.html  # profil serwera
    """
    from fixos.plugins.registry import PluginRegistry
    from datetime import datetime

    registry = PluginRegistry()
    registry.discover()

    mods = None
    if profile:
        from fixos.profiles import Profile
        try:
            prof = Profile.load(profile)
            mods = prof.modules
        except FileNotFoundError as e:
            click.echo(click.style(str(e), fg="red"))
            return
    if modules:
        mods = modules.split(",")

    click.echo(click.style("Generowanie raportu...", fg="yellow"), err=True)
    results = registry.run(modules=mods)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    renderers = {
        "json": _render_report_json,
        "markdown": _render_report_markdown,
    }
    renderer = renderers.get(output_format, _render_report_html)
    content = renderer(results, timestamp)

    if output:
        Path(output).write_text(content, encoding="utf-8")
        click.echo(click.style(f"Raport zapisany: {output}", fg="green"), err=True)
    else:
        click.echo(content)
