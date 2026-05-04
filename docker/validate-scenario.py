#!/usr/bin/env python3
"""
Validates fixOS scan YAML output against expected scenario conditions.

Usage:
  fixos scan --yaml --modules audio | python3 validate-scenario.py broken-audio
  cat scan-output.yml | python3 validate-scenario.py broken-full

Exit codes:
  0  – all expectations met
  1  – validation failures
  2  – invalid input / unknown scenario
"""

from __future__ import annotations

import sys
from typing import Any

import yaml


# ── Scenario expectations ─────────────────────────────────

SCENARIOS: dict[str, list[dict[str, Any]]] = {
    "broken-audio": [
        {
            "path": "diagnostics.audio.alsa_cards",
            "contains": "no soundcards",
            "desc": "ALSA powinno zgłaszać brak kart dźwiękowych",
        },
        {
            "path": "diagnostics.audio.sof_firmware",
            "contains_any": ["No such file", "not installed", "ERR"],
            "desc": "SOF firmware powinno być niedostępne",
        },
    ],
    "broken-thumbnails": [
        {
            "path": "diagnostics.thumbnails.thumbnail_cache_count",
            "equals": "0",
            "desc": "Cache miniaturek powinien być pusty",
        },
        {
            "path": "diagnostics.thumbnails.ffmpegthumbnailer",
            "contains": "nie zainstalowany",
            "desc": "ffmpegthumbnailer powinien być niezainstalowany",
        },
    ],
    "broken-network": [
        {
            "path": "diagnostics.system.systemctl_failed",
            "contains": "NetworkManager",
            "desc": "NetworkManager powinien być w stanie failed",
        },
    ],
    "broken-full": [
        {
            "path": "diagnostics.audio.alsa_cards",
            "contains": "no soundcards",
            "desc": "ALSA: brak kart dźwiękowych",
        },
        {
            "path": "diagnostics.thumbnails.ffmpegthumbnailer",
            "contains": "nie zainstalowany",
            "desc": "ffmpegthumbnailer niezainstalowany",
        },
    ],
}


def _get_nested(data: dict, path: str) -> Any:
    """Get a nested value from a dict using dot notation."""
    keys = path.split(".")
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return None
    return current


def validate(data: dict, scenario: str) -> list[str]:
    """Validate data against scenario expectations. Returns list of failures."""
    expectations = SCENARIOS.get(scenario)
    if expectations is None:
        return [f"Nieznany scenariusz: '{scenario}'. Dostępne: {', '.join(SCENARIOS.keys())}"]

    failures = []
    for exp in expectations:
        path = exp["path"]
        desc = exp.get("desc", path)
        value = _get_nested(data, path)

        if value is None:
            failures.append(f"  ✗ BRAK KLUCZA: {path} — {desc}")
            continue

        value_str = str(value)

        if "equals" in exp:
            if value_str.strip() != str(exp["equals"]).strip():
                failures.append(f"  ✗ {desc}: oczekiwano '{exp['equals']}', otrzymano '{value_str[:80]}'")

        if "contains" in exp:
            if exp["contains"].lower() not in value_str.lower():
                failures.append(f"  ✗ {desc}: brak '{exp['contains']}' w '{value_str[:80]}'")

        if "contains_any" in exp:
            if not any(term.lower() in value_str.lower() for term in exp["contains_any"]):
                failures.append(
                    f"  ✗ {desc}: brak żadnego z {exp['contains_any']} w '{value_str[:80]}'"
                )

    return failures


def main() -> None:
    if len(sys.argv) < 2:
        print(f"Użycie: {sys.argv[0]} <scenario>", file=sys.stderr)
        print(f"Dostępne scenariusze: {', '.join(SCENARIOS.keys())}", file=sys.stderr)
        sys.exit(2)

    scenario = sys.argv[1]
    if scenario not in SCENARIOS:
        print(f"✗ Nieznany scenariusz: '{scenario}'", file=sys.stderr)
        print(f"  Dostępne: {', '.join(SCENARIOS.keys())}", file=sys.stderr)
        sys.exit(2)

    # Read YAML from stdin
    try:
        raw = sys.stdin.read()
        data = yaml.safe_load(raw)
    except yaml.YAMLError as e:
        print(f"✗ Błąd parsowania YAML: {e}", file=sys.stderr)
        sys.exit(2)

    if not isinstance(data, dict):
        print(f"✗ Oczekiwano dict, otrzymano: {type(data).__name__}", file=sys.stderr)
        sys.exit(2)

    # Validate
    failures = validate(data, scenario)

    if failures:
        print(f"✗ Scenariusz '{scenario}' — {len(failures)} błędów:", file=sys.stderr)
        for f in failures:
            print(f, file=sys.stderr)
        sys.exit(1)
    else:
        expectations_count = len(SCENARIOS[scenario])
        print(f"✓ Scenariusz '{scenario}' — {expectations_count}/{expectations_count} OK", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
