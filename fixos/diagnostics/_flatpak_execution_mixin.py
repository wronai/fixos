"""Cleanup execution methods for FlatpakAnalyzer."""

from __future__ import annotations

import os
import shutil
import subprocess
from typing import Dict, List, Any

from fixos.constants import DEFAULT_COMMAND_TIMEOUT

# Vacuum can take longer than the default timeout.
_VACUUM_TIMEOUT = DEFAULT_COMMAND_TIMEOUT * 2


class _FlatpakExecutionMixin:
    """Mixin providing cleanup execution methods for FlatpakAnalyzer."""

    def ask_user_and_cleanup(
        self, auto_confirm_low_risk: bool = False
    ) -> Dict[str, Any]:
        """
        Pytaj użytkownika o zgodę i wykonaj czyszczenie.

        Args:
            auto_confirm_low_risk: Jeśli True, automatycznie wykonuje operacje niskiego ryzyka

        Returns:
            Dict z wynikami wykonanych operacji
        """
        results = {
            "executed": [],
            "skipped": [],
            "failed": [],
            "space_reclaimed": 0,
        }

        recommendations = self.get_cleanup_recommendations()

        if not recommendations:
            print("✅ Brak rekomendacji czyszczenia - Flatpak jest w dobrym stanie.")
            return results

        print("\n" + "=" * 60)
        print("🔧 FLATPAK CLEANUP RECOMMENDATIONS")
        print("=" * 60 + "\n")

        for i, rec in enumerate(recommendations, 1):
            print(f"\n[{i}/{len(recommendations)}] {rec['description']}")
            print(f"   Komenda: {rec['action']}")
            print(f"   Szacowane odzyskanie: {rec['estimated_savings']}")
            print(f"   Ryzyko: {rec['risk'].upper()}")
            print(f"\n   {rec['explanation']}")

            should_execute = False

            if rec["risk"] == "none":
                should_execute = True
                print("\n   ▶️ Wykonuję automatycznie (brak ryzyka)...")
            elif rec["risk"] == "low" and auto_confirm_low_risk:
                should_execute = True
                print("\n   ▶️ Wykonuję automatycznie (niskie ryzyko, auto-confirm)...")
            else:
                print("\n   ❓ Czy wykonać? [y/N] ", end="")
                try:
                    response = input().strip().lower()
                    should_execute = response in ["y", "yes", "t", "tak"]
                except (EOFError, KeyboardInterrupt):
                    print("\n   ⏭️ Pomijam...")
                    should_execute = False

            if should_execute:
                print(f"\n   🚀 Wykonuję: {rec['action']}")
                result = self._execute_cleanup_action(rec)

                if result["success"]:
                    results["executed"].append(
                        {
                            "action": rec["action"],
                            "output": result.get("output", ""),
                        }
                    )
                    results["space_reclaimed"] += result.get("bytes_reclaimed", 0)
                    print("   ✅ Sukces")
                else:
                    results["failed"].append(
                        {
                            "action": rec["action"],
                            "error": result.get("error", "Unknown error"),
                        }
                    )
                    print(f"   ❌ Błąd: {result.get('error', 'Unknown error')}")
            else:
                results["skipped"].append(rec["action"])
                print("   ⏭️ Pominięto")

        print("\n" + "=" * 60)
        print("📊 PODSUMOWANIE")
        print("=" * 60)
        print(f"   Wykonano: {len(results['executed'])}")
        print(f"   Pominięto: {len(results['skipped'])}")
        print(f"   Błędy: {len(results['failed'])}")
        print(f"   Odzyskano: {self._format_size(results['space_reclaimed'])}")
        print("=" * 60 + "\n")

        return results

    def _execute_cleanup_action(self, rec: Dict[str, Any]) -> Dict[str, Any]:
        """Wykonaj pojedynczą akcję czyszczenia"""
        action = rec["action"]

        try:
            if action == "flatpak uninstall --unused -y":
                return self._execute_flatpak_uninstall_unused()
            elif action == "flatpak repair --vacuum":
                return self._execute_flatpak_vacuum()
            elif action == "flatpak repair":
                return self._execute_flatpak_repair()
            elif action.startswith("flatpak uninstall --all"):
                return self._execute_flatpak_uninstall_all()
            elif "rm -rf" in action and ".var/app" in action:
                return self._execute_leftover_data_cleanup(rec.get("items", []))
            else:
                result = subprocess.run(
                    action.split(),
                    capture_output=True,
                    text=True,
                    timeout=DEFAULT_COMMAND_TIMEOUT,
                )
                return {
                    "success": result.returncode == 0,
                    "output": result.stdout,
                    "error": result.stderr if result.returncode != 0 else None,
                    "bytes_reclaimed": 0,
                }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Timeout (300s)"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _execute_flatpak_uninstall_unused(self) -> Dict[str, Any]:
        """Wykonaj flatpak uninstall --unused"""
        analysis = self.analyze()
        bytes_before = analysis["total_size_unused"]

        result = subprocess.run(
            ["flatpak", "uninstall", "--unused", "-y"],
            capture_output=True,
            text=True,
            timeout=DEFAULT_COMMAND_TIMEOUT,
        )

        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr if result.returncode != 0 else None,
            "bytes_reclaimed": bytes_before,
        }

    def _execute_flatpak_repair(self) -> Dict[str, Any]:
        """Wykonaj flatpak repair"""
        result = subprocess.run(
            ["flatpak", "repair"],
            capture_output=True,
            text=True,
            timeout=DEFAULT_COMMAND_TIMEOUT,
        )

        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr if result.returncode != 0 else None,
            "bytes_reclaimed": 0,
        }

    def _execute_flatpak_vacuum(self) -> Dict[str, Any]:
        """Wykonaj flatpak repair --vacuum (czyści repo ze starych obiektów)"""
        bytes_before = self.repo_bloat.get("wasted_size", 0)

        result = subprocess.run(
            ["flatpak", "repair", "--vacuum"],
            capture_output=True,
            text=True,
            timeout=_VACUUM_TIMEOUT,
        )

        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr if result.returncode != 0 else None,
            "bytes_reclaimed": bytes_before,
        }

    def _execute_flatpak_uninstall_all(self) -> Dict[str, Any]:
        """Wykonaj flatpak uninstall --all (hard reset)"""
        analysis = self.analyze()
        bytes_before = sum(a.size_bytes for a in self.installed_apps) + sum(
            r.size_bytes for r in self.installed_runtimes
        )

        result = subprocess.run(
            ["flatpak", "uninstall", "--all", "-y"],
            capture_output=True,
            text=True,
            timeout=DEFAULT_COMMAND_TIMEOUT,
        )

        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr if result.returncode != 0 else None,
            "bytes_reclaimed": bytes_before,
        }

    def _execute_leftover_data_cleanup(self, items: List[Dict]) -> Dict[str, Any]:
        """Usuń leftover data directories"""
        total_bytes = 0
        errors = []

        for item in items:
            cleanup_cmd = item.get("cleanup_command", "")
            if "rm -rf" in cleanup_cmd:
                path = cleanup_cmd.replace("rm -rf ", "").strip()
                if path.startswith("~/.var/app/") or path.startswith("/home/"):
                    try:
                        expanded_path = (
                            os.path.expanduser(path) if path.startswith("~") else path
                        )
                        if os.path.exists(expanded_path):
                            shutil.rmtree(expanded_path)
                            total_bytes += item.get("size_bytes", 0)
                    except Exception as e:
                        errors.append(f"{path}: {e}")

        return {
            "success": len(errors) == 0,
            "output": f"Removed {len(items)} directories",
            "error": "; ".join(errors) if errors else None,
            "bytes_reclaimed": total_bytes,
        }
