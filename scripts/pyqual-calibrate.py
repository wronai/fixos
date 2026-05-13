#!/usr/bin/env python3
"""
Auto-kalibracja progów metryk dla pyqual.
Dostosowuje thresholdy na podstawie aktualnych wyników + margines.

Użycie:
  # Na podstawie ostatniego pyqual run (z pliku pipeline.db)
  python3 scripts/pyqual-calibrate.py

  # Z wyraźnie podanymi wartościami
  python3 scripts/pyqual-calibrate.py --cc 5.0 --vallm 65 --coverage 32.9

  # Z marginesem 15%
  python3 scripts/pyqual-calibrate.py --margin 15 --dry-run
"""

import argparse
import re
import sqlite3
import sys
from pathlib import Path
from typing import Dict, Optional


def read_last_metrics_from_db(workdir: Path) -> Optional[Dict[str, float]]:
    """Czyta ostatnie metryki z pipeline.db pyqual."""
    db_path = workdir / ".pyqual" / "pipeline.db"
    if not db_path.exists():
        return None

    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()

        # Szukamy ostatniego run z metrykami
        cursor.execute("""
            SELECT metric, value, threshold 
            FROM gates 
            WHERE run_id = (SELECT MAX(run_id) FROM runs)
            ORDER BY metric
        """)

        metrics = {}
        for row in cursor.fetchall():
            metric_name, value, threshold = row
            metrics[metric_name] = float(value) if value else 0.0

        conn.close()
        return metrics if metrics else None

    except Exception as e:
        print(f"⚠️  Błąd czytania bazy: {e}")
        return None


def parse_pyqual_yaml(config_path: Path) -> str:
    """Odczytuje zawartość pyqual.yaml."""
    return config_path.read_text()


def update_metric(content: str, metric_name: str, new_value) -> str:
    """Aktualizuje wartość metryki w YAML."""
    # Dla cc_max (górny limit)
    if metric_name == "cc_max":
        pattern = r"(cc_max:\s*)\d+(\.\d+)?"
        replacement = f"\\g<1>{new_value}"
        content = re.sub(pattern, replacement, content)
    # Dla vallm_pass_min (dolny limit)
    elif metric_name == "vallm_pass_min":
        pattern = r"(vallm_pass_min:\s*)\d+(\.\d+)?"
        replacement = f"\\g<1>{new_value}"
        content = re.sub(pattern, replacement, content)
    # Dla coverage_min (dolny limit)
    elif metric_name == "coverage_min":
        pattern = r"(coverage_min:\s*)\d+(\.\d+)?"
        replacement = f"\\g<1>{new_value}"
        content = re.sub(pattern, replacement, content)
    return content


def calculate_new_threshold(
    actual_value: float,
    current_threshold: float,
    margin_percent: float,
    is_upper_limit: bool,
) -> float:
    """
    Wylicza nowy próg z marginesem.

    Dla upper limit (cc_max): threshold >= actual * (1 + margin)
    Dla lower limit (coverage_min, vallm_pass_min): threshold <= actual * (1 - margin)
    """
    if is_upper_limit:
        # Górny limit: musi być >= aktualnej wartości + margines
        new_threshold = actual_value * (1 + margin_percent / 100)
        # Zaokrąglij w górę
        new_threshold = int(new_threshold) + (1 if new_threshold % 1 > 0 else 0)
        # Nie obniżaj progu (zabezpieczenie)
        return max(new_threshold, current_threshold)
    else:
        # Dolny limit: może być <= aktualnej wartości - margines
        new_threshold = actual_value * (1 - margin_percent / 100)
        # Zaokrąglij w dół
        new_threshold = int(new_threshold)
        # Nie podnoś progu powyżej aktualnej wartości
        return min(max(new_threshold, 0), actual_value)


def extract_current_metrics(content: str) -> Dict[str, float]:
    """Wyciąga aktualne progi z YAML."""
    metrics = {}

    cc_match = re.search(r"cc_max:\s*(\d+(?:\.\d+)?)", content)
    if cc_match:
        metrics["cc_max"] = float(cc_match.group(1))

    vallm_match = re.search(r"vallm_pass_min:\s*(\d+(?:\.\d+)?)", content)
    if vallm_match:
        metrics["vallm_pass_min"] = float(vallm_match.group(1))

    cov_match = re.search(r"coverage_min:\s*(\d+(?:\.\d+)?)", content)
    if cov_match:
        metrics["coverage_min"] = float(cov_match.group(1))

    return metrics


def calibrate(
    workdir: Path,
    margin: float = 10.0,
    dry_run: bool = False,
    force: bool = False,
    provided_metrics: Optional[Dict[str, float]] = None,
) -> bool:
    """
    Główna funkcja kalibracji.

    Args:
        workdir: Katalog z pyqual.yaml
        margin: Procent marginesu (default: 10%)
        dry_run: Tylko pokaż co by się zmieniło
        force: Wymuś kalibrację nawet jeśli gates przechodzą
        provided_metrics: Opcjonalnie podane metryki (zamiast czytać z DB)
    """
    config_path = workdir / "pyqual.yaml"
    if not config_path.exists():
        print(f"❌ Nie znaleziono {config_path}")
        return False

    print(f"🔧 Kalibracja progów pyqual (margines: {margin}%)")
    print(f"📁 Workdir: {workdir}")

    # Odczytaj aktualną konfigurację
    content = parse_pyqual_yaml(config_path)
    current_thresholds = extract_current_metrics(content)

    print("\n📊 Aktualne progi w config:")
    for name, value in current_thresholds.items():
        print(f"   {name}: {value}")

    # Pobierz aktualne wartości metryk
    if provided_metrics:
        actual_metrics = provided_metrics
        print("\n📈 Podane wartości:")
    else:
        # Spróbuj odczytać z bazy
        actual_metrics = read_last_metrics_from_db(workdir)
        if actual_metrics:
            print("\n📈 Odczytane wartości z pipeline.db:")
        else:
            print("❌ Nie znaleziono danych w .pyqual/pipeline.db")
            print("   Użyj --cc, --vallm, --coverage aby podać wartości ręcznie")
            return False

    for name, value in actual_metrics.items():
        print(f"   {name}: {value}")

    # Wylicz nowe progi
    changes = []
    new_content = content

    # Mapowanie nazw metryk pyqual -> nazwy w YAML
    metric_mapping = {
        "cc": ("cc_max", True),  # (nazwa_w_yaml, czy_upper_limit)
        "cc_max": ("cc_max", True),
        "vallm_pass": ("vallm_pass_min", False),
        "vallm_pass_min": ("vallm_pass_min", False),
        "coverage": ("coverage_min", False),
        "coverage_min": ("coverage_min", False),
    }

    for gate_metric, (yaml_metric, is_upper) in metric_mapping.items():
        if gate_metric not in actual_metrics or yaml_metric not in current_thresholds:
            continue

        actual = actual_metrics[gate_metric]
        current = current_thresholds[yaml_metric]

        new_threshold = calculate_new_threshold(actual, current, margin, is_upper)

        if new_threshold != current or force:
            changes.append(
                {
                    "metric": yaml_metric,
                    "old": current,
                    "new": new_threshold,
                    "actual": actual,
                }
            )
            new_content = update_metric(new_content, yaml_metric, new_threshold)

    if not changes:
        print("\n✅ Progi są już optymalne - brak zmian")
        return True

    # Pokaż zmiany
    print("\n📝 Proponowane zmiany:")
    for change in changes:
        print(
            f"   {change['metric']}: {change['old']} → {change['new']} "
            f"(aktualna wartość: {change['actual']})"
        )

    if dry_run:
        print("\n🏃 Dry-run - nie zapisano zmian")
        return True

    # Zapisz zmiany
    config_path.write_text(new_content)
    print(f"\n✅ Zapisano zmiany do {config_path}")

    return True


def main():
    parser = argparse.ArgumentParser(description="Auto-kalibracja progów metryk pyqual")
    parser.add_argument(
        "--workdir",
        "-w",
        type=Path,
        default=Path.cwd(),
        help="Katalog z pyqual.yaml (domyślnie: .)",
    )
    parser.add_argument(
        "--margin",
        "-m",
        type=float,
        default=10.0,
        help="Margines procentowy (default: 10%%)",
    )
    parser.add_argument(
        "--dry-run", "-n", action="store_true", help="Tylko pokaż co by się zmieniło"
    )
    parser.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="Wymuś kalibrację nawet jeśli gates przechodzą",
    )
    # Opcje do ręcznego podawania metryk
    parser.add_argument(
        "--cc", type=float, help="Aktualna wartość cyclomatic complexity"
    )
    parser.add_argument("--vallm", type=float, help="Aktualna wartość vallm_pass (%)")
    parser.add_argument("--coverage", type=float, help="Aktualna wartość coverage (%)")

    args = parser.parse_args()

    # Przygotuj podane metryki
    provided_metrics = {}
    if args.cc is not None:
        provided_metrics["cc"] = args.cc
    if args.vallm is not None:
        provided_metrics["vallm_pass"] = args.vallm
    if args.coverage is not None:
        provided_metrics["coverage"] = args.coverage

    success = calibrate(
        workdir=args.workdir,
        margin=args.margin,
        dry_run=args.dry_run,
        force=args.force,
        provided_metrics=provided_metrics if provided_metrics else None,
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
