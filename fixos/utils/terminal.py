"""
Terminal rendering utilities – shared between hitl, orchestrator, cli.

Provides:
- console     : shared rich Console instance
- _C          : legacy ANSI stubs (no-op) kept for backward compat
- render_md() : print markdown-formatted LLM text via rich
- colorize()  : inline **bold** / `code` colorization (plain text passthrough)
- print_cmd_block()      : pretty command preview panel
- print_stdout_box()     : stdout in a rich Panel
- print_stderr_box()     : stderr in a rich Panel
- print_problem_header() : colored severity header for a problem
- render_tree_colored()  : colorized problem graph tree (rich Text)
"""

from __future__ import annotations

import re
from typing import Optional

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.rule import Rule
from rich.syntax import Syntax
from rich.text import Text
from rich.theme import Theme


# ── Shared console ─────────────────────────────────────────────────────────

_theme = Theme({
    "critical": "bold red",
    "warning":  "bold yellow",
    "info":     "bold green",
    "cmd":      "bold cyan",
    "dim":      "dim",
    "stdout":   "green",
    "stderr":   "red",
})

console = Console(theme=_theme, highlight=False)


# ── Legacy _C stub (backward compat – callers that still use _C.RED etc.) ──

class _C:
    """No-op stubs – kept so existing callers don't break at import time."""
    RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = ""
    BOLD = DIM = RESET = BG_DARK = ""


# ── Inline colorization (plain-text passthrough for rich) ──────────────────

def colorize(line: str) -> str:
    """Return line unchanged – rich handles markup in render_md()."""
    return line


# ── Markdown renderer ──────────────────────────────────────────────────────

def render_md(text: str) -> None:
    """
    Print LLM markdown reply to terminal via rich.

    Handles:
    - ``` code blocks ``` rendered as Syntax panels
    - # / ## headings via rich Markdown
    - ━━━ / === / --- section dividers → rich Rule
    - 🔴 🟡 🟢 severity lines with color
    - **bold**, `inline code` via rich Markdown
    - [N] / [A] / [S] / [Q] action items in yellow
    - - / * bullet lists via rich Markdown
    """
    in_code_block = False
    code_lang = ""
    code_lines: list[str] = []
    md_buffer: list[str] = []

    def _flush_md() -> None:
        if md_buffer:
            block = "\n".join(md_buffer)
            md_buffer.clear()
            if block.strip():
                console.print(Markdown(block))

    for raw_line in text.splitlines():
        line = raw_line

        # ── Code block fence ──────────────────────────────────────
        if line.strip().startswith("```"):
            if not in_code_block:
                _flush_md()
                in_code_block = True
                code_lang = line.strip()[3:].strip() or "text"
                code_lines = []
            else:
                in_code_block = False
                code_str = "\n".join(code_lines)
                syntax = Syntax(
                    code_str,
                    code_lang,
                    theme="monokai",
                    line_numbers=False,
                    word_wrap=True,
                )
                console.print(Panel(syntax, title=f"[dim]{code_lang}[/dim]", border_style="dim cyan"))
                code_lines = []
            continue

        if in_code_block:
            code_lines.append(line)
            continue

        stripped = line.strip()

        # ── Section dividers (━━━ TEXT ━━━ / === / ---) ────────────
        if re.match(r'^[━═─]{3,}', stripped):
            _flush_md()
            inner = re.sub(r'^[━═─\s]+|[━═─\s]+$', '', stripped)
            if inner:
                console.print(Rule(f"[bold cyan]{inner}[/bold cyan]", style="cyan"))
            else:
                console.print(Rule(style="dim cyan"))
            continue

        # ── Severity lines ─────────────────────────────────────────
        if stripped.startswith("🔴"):
            _flush_md()
            console.print(Text(line, style="bold red"))
            continue
        if stripped.startswith("🟡"):
            _flush_md()
            console.print(Text(line, style="bold yellow"))
            continue
        if stripped.startswith("🟢"):
            _flush_md()
            console.print(Text(line, style="bold green"))
            continue
        if stripped.startswith("✅"):
            _flush_md()
            console.print(Text(line, style="green"))
            continue
        if stripped.startswith("❌"):
            _flush_md()
            console.print(Text(line, style="red"))
            continue
        if stripped.startswith("⚠️") or stripped.startswith("⚠"):
            _flush_md()
            console.print(Text(line, style="yellow"))
            continue

        # ── Action items [N] / [A] / [S] / [Q] ────────────────────
        if re.match(r'^\s*\[([\dASDQ?!])\]', line):
            _flush_md()
            console.print(Text(line, style="bold yellow"))
            continue

        # ── Everything else → accumulate as Markdown ───────────────
        md_buffer.append(line)

    _flush_md()


# ── Command preview box ────────────────────────────────────────────────────

def print_cmd_block(cmd: str, comment: str = "", dry_run: bool = False) -> None:
    """Print a framed command preview panel."""
    label = "DRY-RUN" if dry_run else "🔧 KOMENDA DO WYKONANIA"
    border = "dim" if dry_run else "cyan"
    syntax = Syntax(cmd, "bash", theme="monokai", word_wrap=True)
    content = syntax
    if comment:
        from rich.console import Group
        note = Text(f"📝 Co robi: {comment}", style="dim")
        content = Group(syntax, note)
    console.print()
    console.print(Panel(content, title=f"[bold {border}]{label}[/bold {border}]", border_style=border))


# ── Result boxes ───────────────────────────────────────────────────────────

def print_stdout_box(stdout: str, max_lines: int = 30) -> None:
    """Print stdout in a rich Panel."""
    lines = stdout.strip().splitlines()
    shown = lines[:max_lines]
    body = "\n".join(shown)
    if len(lines) > max_lines:
        body += f"\n[dim]... ({len(lines) - max_lines} więcej linii)[/dim]"
    console.print(Panel(Text(body, style="green"), title="[dim]stdout[/dim]", border_style="dim green"))


def print_stderr_box(stderr: str, max_lines: int = 15) -> None:
    """Print stderr in a rich Panel."""
    lines = stderr.strip().splitlines()
    shown = lines[:max_lines]
    body = "\n".join(shown)
    if len(lines) > max_lines:
        body += f"\n[dim]... ({len(lines) - max_lines} więcej linii)[/dim]"
    console.print(Panel(Text(body, style="red"), title="[dim]stderr[/dim]", border_style="dim red"))


# ── Problem header ─────────────────────────────────────────────────────────

SEVERITY_COLOR = {
    "critical": "red",
    "warning":  "yellow",
    "info":     "green",
}
SEVERITY_ICON = {
    "critical": "🔴",
    "warning":  "🟡",
    "info":     "🟢",
}
STATUS_ICON = {
    "pending":     "⏳",
    "in_progress": "🔄",
    "resolved":    "✅",
    "failed":      "❌",
    "blocked":     "🚫",
    "skipped":     "⏭️ ",
}


def print_problem_header(
    problem_id: str,
    description: str,
    severity: str,
    status: Optional[str] = None,
    attempts: int = 0,
    max_attempts: int = 3,
) -> None:
    """Print a colored problem header panel."""
    color = SEVERITY_COLOR.get(severity, "white")
    icon = SEVERITY_ICON.get(severity, "⚪")

    title_parts = [f"[bold {color}]{icon} [{problem_id}][/bold {color}]"]
    if status:
        s_icon = STATUS_ICON.get(status, "?")
        title_parts.append(f"[dim]{s_icon} {status}[/dim]")
    if attempts > 0:
        title_parts.append(f"[dim](próba {attempts}/{max_attempts})[/dim]")

    title = "  ".join(title_parts)
    body = Text(description, style=color)
    console.print()
    console.print(Panel(body, title=title, border_style=color))


# ── Graph tree renderer ────────────────────────────────────────────────────

def render_tree_colored(nodes: dict, execution_order: list[str]) -> str:
    """
    Render a ProblemGraph as a rich-markup string.
    nodes: dict[str, Problem]
    """
    lines: list[str] = []
    visited: set[str] = set()

    def _render(pid: str, indent: int = 0) -> None:
        if pid in visited or pid not in nodes:
            return
        visited.add(pid)
        p = nodes[pid]
        color = SEVERITY_COLOR.get(p.severity, "white")
        sev_icon = SEVERITY_ICON.get(p.severity, "⚪")
        stat_icon = STATUS_ICON.get(p.status, "?")
        prefix = "  " * indent + ("└─ " if indent > 0 else "  ")
        desc = p.description[:70] + ("…" if len(p.description) > 70 else "")
        lines.append(
            f"{prefix}[bold {color}]{sev_icon} [{p.id}][/bold {color}] "
            f"[{color}]{desc}[/{color}]  [dim]{stat_icon}[/dim]"
        )
        for child_id in p.may_cause:
            _render(child_id, indent + 1)

    roots = [p for p in nodes.values() if not p.caused_by]
    for root in roots:
        _render(root.id)

    for p in nodes.values():
        if p.id not in visited:
            color = SEVERITY_COLOR.get(p.severity, "white")
            sev_icon = SEVERITY_ICON.get(p.severity, "⚪")
            stat_icon = STATUS_ICON.get(p.status, "?")
            desc = p.description[:70] + ("…" if len(p.description) > 70 else "")
            lines.append(
                f"  [dim]◦[/dim] [bold {color}]{sev_icon} [{p.id}][/bold {color}] "
                f"[{color}]{desc}[/{color}]  [dim]{stat_icon}[/dim]"
            )

    return "\n".join(lines) if lines else "  [dim](brak problemów)[/dim]"


# ── Helpers ────────────────────────────────────────────────────────────────

def _wrap(text: str, width: int) -> list[str]:
    """Simple word-wrap."""
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        if current and len(current) + 1 + len(word) > width:
            lines.append(current)
            current = word
        else:
            current = (current + " " + word).lstrip()
    if current:
        lines.append(current)
    return lines or [""]
