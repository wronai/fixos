"""
Anonimizacja wrażliwych danych systemowych z podglądem dla użytkownika.
"""

from __future__ import annotations

import re
import socket
import getpass
import os
from dataclasses import dataclass, field
from .terminal import _C


@dataclass
class AnonymizationReport:
    """Raport anonimizacji – co zostało zmaskowane."""
    original_length: int = 0
    anonymized_length: int = 0
    replacements: dict[str, int] = field(default_factory=dict)

    def add(self, category: str, count: int = 1):
        self.replacements[category] = self.replacements.get(category, 0) + count

    def summary(self) -> str:
        if not self.replacements:
            return "  Nie znaleziono wrażliwych danych."
        lines = []
        for cat, count in sorted(self.replacements.items()):
            lines.append(f"  ✓ {cat}: {count} wystąpień")
        return "\n".join(lines)


def _get_sensitive() -> dict:
    result = {}
    try:
        result["hostname"] = socket.gethostname()
    except Exception:
        result["hostname"] = None
    try:
        result["username"] = getpass.getuser()
    except Exception:
        result["username"] = None
    try:
        result["home"] = os.path.expanduser("~")
    except Exception:
        result["home"] = None
    return result


# (pattern, replacement, flags, report_label) — applied in order after literal replacements
_REGEX_REPLACEMENTS: list[tuple[str, str, int, str]] = [
    (r"/home/(?!\[USER\])[^\s\"'\\]+",                                    "/home/[USER]/...", 0,           "Ścieżki /home"),
    (r"\b(\d{1,3}\.\d{1,3})\.\d{1,3}\.\d{1,3}\b",                       r"\1.XXX.XXX",     0,           "Adresy IPv4"),
    (r"\b([0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}\b",                      "XX:XX:XX:XX:XX:XX", 0,         "Adresy MAC"),
    (r"(?<![A-Za-z0-9])(?:sk-|xai-|AIzaSy[A-Za-z0-9_-]+|Bearer\s+)[A-Za-z0-9\-_.]{15,}",
                                                                           "[API_TOKEN_REDACTED]", 0,      "Tokeny API"),
    (r"(?i)(password|passwd|secret|token|api_key|apikey|auth)\s*[=:]\s*\S+",
                                                                           r"\1=[REDACTED]", re.IGNORECASE, "Hasła/sekrety"),
    (r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b",
                                                                           "[UUID-REDACTED]", 0,           "UUID (serial/hardware)"),
    (r"\b(?:S/N|Serial|SN)[\s:]+[A-Z0-9]{6,20}\b",                       "Serial: [SERIAL-REDACTED]",
                                                                                              re.IGNORECASE, "Numery seryjne"),
]


def _apply_regex_replacements(data_str: str, report: AnonymizationReport) -> str:
    """Apply all regex-based anonymization patterns from _REGEX_REPLACEMENTS."""
    for pattern, replacement, flags, label in _REGEX_REPLACEMENTS:
        matches = len(re.findall(pattern, data_str, flags))
        if matches:
            data_str = re.sub(pattern, replacement, data_str, flags=flags)
            report.add(label, matches)
    return data_str


def anonymize(data_str: str) -> tuple[str, AnonymizationReport]:
    """
    Anonimizuje wrażliwe dane.

    Returns:
        Tuple (zanonimizowany_string, raport)
    """
    if not isinstance(data_str, str):
        data_str = str(data_str)

    report = AnonymizationReport(original_length=len(data_str))
    sensitive = _get_sensitive()

    # 1. Hostname (literal)
    if sensitive.get("hostname"):
        count = data_str.count(sensitive["hostname"])
        if count:
            data_str = data_str.replace(sensitive["hostname"], "[HOSTNAME]")
            report.add("Hostname", count)

    # 2. Katalog domowy — pełna ścieżka (PRZED zastąpieniem username)
    if sensitive.get("home"):
        count = data_str.count(sensitive["home"])
        if count:
            data_str = data_str.replace(sensitive["home"], "/home/[USER]")
            report.add("Ścieżka domowa", count)

    # 3–10. Regex-based replacements (home paths, IPs, MACs, tokens, etc.)
    data_str = _apply_regex_replacements(data_str, report)

    # Username (konkretna nazwa) — po zastąpieniu ścieżek przez regex
    if sensitive.get("username"):
        pattern = rf"\b{re.escape(sensitive['username'])}\b"
        matches = len(re.findall(pattern, data_str))
        if matches:
            data_str = re.sub(pattern, "[USER]", data_str)
            report.add("Username", matches)

    report.anonymized_length = len(data_str)
    return data_str, report


def display_anonymized_preview(data_str: str, report: AnonymizationReport, max_lines: int = 80):
    """
    Wyświetla użytkownikowi zanonimizowane dane przed wysłaniem do LLM.
    Formatuje jako czytelny markdown z kolorami ANSI.
    """
    line_char = '\u2550' * 65
    print(f"\n{_C.CYAN}{_C.BOLD}{line_char}{_C.RESET}")
    print(f"{_C.CYAN}{_C.BOLD}  📋 DANE DIAGNOSTYCZNE (zanonimizowane) – wysyłane do LLM{_C.RESET}")
    print(f"{_C.CYAN}{_C.BOLD}{line_char}{_C.RESET}")

    formatted = _format_diagnostics_markdown(data_str)

    lines = formatted.splitlines()
    if len(lines) > max_lines:
        half = max_lines // 2
        shown = (
            lines[:half]
            + [f"  {_C.DIM}...{_C.RESET}",
               f"  {_C.DIM}[skrócono – pełne dane wysyłane do LLM]{_C.RESET}",
               f"  {_C.DIM}...{_C.RESET}"]
            + lines[-half:]
        )
    else:
        shown = lines

    max_width = 100
    for line in shown:
        rendered = _colorize_md_line(line)
        # Strip ANSI for length check, truncate raw if needed
        raw_len = len(re.sub(r'\033\[[^m]*m', '', rendered))
        if raw_len > max_width:
            # Truncate the original line (before colorizing) then re-colorize
            rendered = _colorize_md_line(line[:max_width - 3] + "...")
        print(f"  {rendered}")

    dash_char = '\u2500'
    dash_line = f"{_C.DIM}{dash_char * 65}{_C.RESET}"
    print(f"\n{dash_line}")
    print(f"{_C.BOLD}  🔒 Anonimizacja – co zostało ukryte:{_C.RESET}")
    for rep_line in report.summary().splitlines():
        print(f"{_C.GREEN}  {rep_line}{_C.RESET}")
    print(f"  {_C.DIM}Rozmiar: {report.original_length:,} → {report.anonymized_length:,} znaków{_C.RESET}")
    print(dash_line)


def _colorize_md_line(line: str) -> str:
    """Apply ANSI colors to a single markdown-formatted diagnostic line."""
    stripped = line.lstrip()

    # ### Section heading
    if stripped.startswith("### "):
        title = stripped[4:]
        return f"{_C.CYAN}{_C.BOLD}{line[:len(line)-len(stripped)]}### {title}{_C.RESET}"

    # ``` fence lines
    if stripped.startswith("```"):
        return f"{_C.DIM}{line}{_C.RESET}"

    # - **key**: `value`  or  - **key**: value
    if stripped.startswith("- **"):
        # bold key
        line = re.sub(r'\*\*([^*]+)\*\*', lambda m: f"{_C.BOLD}{_C.WHITE}{m.group(1)}{_C.RESET}", line)
        # inline code value
        line = re.sub(r'`([^`]+)`', lambda m: f"{_C.CYAN}`{m.group(1)}`{_C.RESET}", line)
        return line

    # indented code content (inside ``` blocks rendered as plain lines)
    if line.startswith("  ") and stripped and not stripped.startswith("-") and not stripped.startswith("#"):
        return f"{_C.GREEN}{line}{_C.RESET}"

    # ... truncation markers
    if stripped.startswith("..."):
        return f"{_C.DIM}{line}{_C.RESET}"

    # inline code anywhere
    line = re.sub(r'`([^`]+)`', lambda m: f"{_C.CYAN}`{m.group(1)}`{_C.RESET}", line)
    return line


def _format_diagnostics_markdown(data_str: str) -> str:
    """Formatuje dane diagnostyczne jako czytelny markdown."""
    import ast
    
    # Próbuj sparsować jako dict
    try:
        # Usuń 'zanonimizowane' znaczniki jeśli są
        clean = data_str.replace('[HOSTNAME]', 'HOSTNAME').replace('[USER]', 'USER')
        data = ast.literal_eval(clean)
        if isinstance(data, dict):
            return _dict_to_markdown(data)
    except (SyntaxError, ValueError):
        pass
    
    # Fallback: formatuj jako kod
    return f"```\n{data_str}\n```"


def _render_dict_list_value(key: str, value: list, prefix: str) -> list:
    """Render a list value as markdown lines."""
    if value and isinstance(value[0], dict):
        return [f"{prefix}- **{key}**: [{len(value)} elementów]"]
    if len(value) > 10:
        lines = [f"{prefix}- **{key}**:"]
        for item in value[:5]:
            lines.append(f"{prefix}  - {item}")
        lines.append(f"{prefix}  ... ({len(value) - 10} więcej)")
        for item in value[-5:]:
            lines.append(f"{prefix}  - {item}")
        return lines
    return [f"{prefix}- **{key}**: {value}"]


def _render_dict_long_string(key: str, value: str, prefix: str) -> list:
    """Render a long string (>200 chars) as a truncated code block."""
    lines = [f"{prefix}- **{key}**:", f"{prefix}  ```"]
    for line in value.split("\n")[:15]:
        lines.append(f"{prefix}  {line[:80]}")
    if value.count("\n") > 15:
        lines.append(f"{prefix}  ... ({value.count(chr(10)) - 15} więcej linii)")
    lines.append(f"{prefix}  ```")
    return lines


def _render_dict_multiline_string(key: str, value: str, prefix: str) -> list:
    """Render a multiline string as a code block."""
    lines = [f"{prefix}- **{key}**:", f"{prefix}  ```"]
    for line in value.split("\n")[:10]:
        lines.append(f"{prefix}  {line}")
    if value.count("\n") > 10:
        lines.append(f"{prefix}  ... ({value.count(chr(10)) - 10} więcej)")
    lines.append(f"{prefix}  ```")
    return lines


def _dict_to_markdown(data: dict, indent: int = 0) -> str:
    """Rekurencyjnie konwertuje dict na markdown."""
    lines = []
    prefix = "  " * indent

    for key, value in data.items():
        if isinstance(value, dict):
            section_title = _format_key_title(key)
            lines.append(f"\n{prefix}### {section_title}")
            lines.append(_dict_to_markdown(value, indent + 1))
        elif isinstance(value, list):
            lines.extend(_render_dict_list_value(key, value, prefix))
        elif isinstance(value, str) and len(value) > 200:
            lines.extend(_render_dict_long_string(key, value, prefix))
        elif isinstance(value, str) and "\n" in value:
            lines.extend(_render_dict_multiline_string(key, value, prefix))
        else:
            val_str = str(value)
            if len(val_str) > 60:
                val_str = val_str[:57] + "..."
            lines.append(f"{prefix}- **{key}**: `{val_str}`")

    return "\n".join(lines)


def _format_key_title(key: str) -> str:
    """Formatuje klucz dict jako czytelny tytuł."""
    titles = {
        "system": "🖥️ System",
        "audio": "🔊 Dźwięk",
        "thumbnails": "🖼️ Podglądy plików",
        "hardware": "🔧 Sprzęt",
        "disks": "💾 Dyski",
        "top_processes": "📊 Top procesy",
    }
    return titles.get(key, key.replace("_", " ").title())
