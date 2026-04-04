#!/usr/bin/env python3
"""
Auto-kalibracja progów metryk dla pyqual.
Dostosowuje thresholdy na podstawie aktualnych wyników + margines.
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, Optional


def run_pyqual_json(workdir: Path) -> Optional[Dict]:
    """Uruchamia pyqual run z outputem JSON i zwraca wynik."""
    cmd = [sys.executable, "-m", "pyqual", "run", "--format", "json"]
    try:
        result = subprocess.run(
            cmd,
            cwd=workdir,
            capture_output=True,
            text=True,
            timeout=300
        )
        # Szukamy JSON w output
        for line in result.stdout.splitlines():
            line = line.strip()
            if line.startswith("{"):
                return json.loads(line)
    except Exception as e:
        print(f"⚠️  Błąd uruchamiania pyqual: {e}")
    return None


def parse_pyqual_yaml(config_path: Path) -> str:
    """Odczytuje zawartość pyqual.yaml."""
    return config_path.read_text()


def update_metric(content: str, metric_name: str, new_value, operator: str = None) -> str:
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
    is_upper_limit: bool
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
    force: bool = False
) -> bool:
    """
    Główna funkcja kalibracji.
    
    Args:
        workdir: Katalog z pyqual.yaml
        margin: Procent marginesu (default: 10%)
        dry_run: Tylko pokaż co by się zmieniło
        force: Wymuś kalibrację nawet jeśli gates przechodzą
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
    
    print(f"\n📊 Aktualne progi:")
    for name, value in current_thresholds.items():
        print(f"   {name}: {value}")
    
    # Uruchom pyqual i pobierz aktualne wartości
    print(f"\n🚀 Uruchamiam pyqual run...")
    result = run_pyqual_json(workdir)
    
    if not result:
        print("❌ Nie udało się pobrać wyników z pyqual")
        return False
    
    # Sprawdź czy gates przechodzą
    all_passed = result.get("all_gates_passed", False)
    if all_passed and not force:
        print("✅ Wszystkie bramki przechodzą - kalibracja niepotrzebna")
        print("   Użyj --force aby wymusić kalibrację")
        return True
    
    # Pobierz wartości metryk
    gates = result.get("gates", [])
    actual_metrics = {}
    for gate in gates:
        metric_name = gate.get("metric")
        actual_value = gate.get("value")
        if metric_name and actual_value is not None:
            actual_metrics[metric_name] = actual_value
    
    print(f"\n📈 Aktualne wartości:")
    for name, value in actual_metrics.items():
        print(f"   {name}: {value}")
    
    # Wylicz nowe progi
    changes = []
    new_content = content
    
    # Mapowanie nazw metryk
    metric_mapping = {
        "cc": ("cc_max", True),           # (nazwa_w_yaml, czy_upper_limit)
        "vallm_pass": ("vallm_pass_min", False),
        "coverage": ("coverage_min", False),
    }
    
    for gate_metric, (yaml_metric, is_upper) in metric_mapping.items():
        if gate_metric not in actual_metrics or yaml_metric not in current_thresholds:
            continue
        
        actual = actual_metrics[gate_metric]
        current = current_thresholds[yaml_metric]
        
        new_threshold = calculate_new_threshold(
            actual, current, margin, is_upper
        )
        
        if new_threshold != current:
            changes.append({
                "metric": yaml_metric,
                "old": current,
                "new": new_threshold,
                "actual": actual,
            })
            new_content = update_metric(new_content, yaml_metric, new_threshold)
    
    if not changes:
        print("\n✅ Progi są już optymalne - brak zmian")
        return True
    
    # Pokaż zmiany
    print(f"\n📝 Proponowane zmiany:")
    for change in changes:
        print(f"   {change['metric']}: {change['old']} → {change['new']} "
              f"(aktualna wartość: {change['actual']})")
    
    if dry_run:
        print("\n🏃 Dry-run - nie zapisano zmian")
        return True
    
    # Zapisz zmiany
    config_path.write_text(new_content)
    print(f"\n✅ Zapisano zmiany do {config_path}")
    
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Auto-kalibracja progów metryk pyqual"
    )
    parser.add_argument(
        "--workdir", "-w",
        type=Path,
        default=Path.cwd(),
        help="Katalog z pyqual.yaml (domyślnie: .)"
    )
    parser.add_argument(
        "--margin", "-m",
        type=float,
        default=10.0,
        help="Margines procentowy (default: 10%%)"
    )
    parser.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="Tylko pokaż co by się zmieniło"
    )
    parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Wymuś kalibrację nawet jeśli gates przechodzą"
    )
    
    args = parser.parse_args()
    
    success = calibrate(
        workdir=args.workdir,
        margin=args.margin,
        dry_run=args.dry_run,
        force=args.force
    )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
