"""Recommendation generation methods for FlatpakAnalyzer."""

from __future__ import annotations

from typing import Dict, List, Any

from fixos.constants import (
    FLATPAK_LEFTOVER_THRESHOLD_MB,
    MAX_DUPLICATE_APPS_SHOW,
    MAX_LARGE_APPS_SHOW,
)


class _FlatpakRecommendationsMixin:
    """Mixin providing cleanup recommendation methods for FlatpakAnalyzer."""

    def get_largest_apps(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get list of largest installed apps (for removal recommendations)"""
        sorted_apps = sorted(self.installed_apps, key=lambda x: -x.size_bytes)

        return [
            {
                "name": app.name,
                "ref": app.ref,
                "size": app.size_bytes,
                "size_human": app.size_human,
                "cleanup_command": f"flatpak uninstall {app.ref} -y",
            }
            for app in sorted_apps[:limit]
        ]

    def get_cleanup_summary(self) -> str:
        """Get human-readable summary of cleanup opportunities"""
        analysis = self.analyze()

        lines = [
            "=== Flatpak Cleanup Analysis ===",
            "",
        ]

        if self.unused_runtimes:
            lines.append(
                f"Unused Runtimes ({len(self.unused_runtimes)} items, {self._format_size(analysis['total_size_unused'])}):"
            )
            for rt in sorted(self.unused_runtimes, key=lambda x: -x.size_bytes):
                lines.append(f"  - {rt.name} ({rt.size_human})")
            lines.append("")

        if self.leftover_data:
            lines.append(
                f"Leftover App Data ({len(self.leftover_data)} items, {self._format_size(analysis['total_size_leftover'])}):"
            )
            for data in sorted(self.leftover_data, key=lambda x: -x.size_bytes)[:10]:
                lines.append(f"  - {data.name} ({data.size_human})")
            if len(self.leftover_data) > 10:
                lines.append(f"  ... and {len(self.leftover_data) - 10} more")
            lines.append("")

        if self.orphaned_apps:
            lines.append(
                f"Orphaned Apps ({len(self.orphaned_apps)} items, {self._format_size(analysis['total_size_orphaned'])}):"
            )
            for app in sorted(self.orphaned_apps, key=lambda x: -x.size_bytes):
                lines.append(
                    f"  - {app.name} ({app.size_human}) - origin: {app.origin}"
                )
            lines.append("")

        total_reclaimable = (
            analysis["total_size_unused"]
            + analysis["total_size_leftover"]
            + analysis["total_size_orphaned"]
        )
        lines.append(f"Total reclaimable space: {self._format_size(total_reclaimable)}")

        return "\n".join(lines)

    def _rec_repo_bloat(self) -> List[Dict[str, Any]]:
        """Recommendations for repo bloat status."""
        recs: List[Dict[str, Any]] = []
        if self.repo_bloat.get("actual_disk_usage", 0) <= 0:
            return recs
        ratio = self.repo_bloat.get("ratio", 0)
        note = self.repo_bloat.get("note", "")
        if self.repo_bloat.get("bloat_detected"):
            if self.repo_bloat.get("wasted_size", 0) > 1024**3:
                recs.append(
                    {
                        "priority": "medium",
                        "action": "flatpak repair --vacuum",
                        "description": "💣 Wyczyść repo Flatpak (potencjalne śmieci)",
                        "explanation": (
                            f"Rzeczywiste użycie dysku: {self.repo_bloat.get('actual_disk_usage_human', '?')}\n"
                            f"Rozmiar raportowany przez flatpak: {self.repo_bloat.get('reported_size_human', '?')}\n"
                            f"Ratio: {ratio:.1f}x (normalne: 1-1.5x)\n\n{note}\n\n"
                            "⚠️ UWAGA: Jeśli już uruchamiałeś 'flatpak repair --vacuum',\n"
                            "to po prostu masz dużo aplikacji - to normalne."
                        ),
                        "estimated_savings": self.repo_bloat.get(
                            "wasted_size_human", "?"
                        ),
                        "risk": "low",
                        "requires_confirmation": True,
                    }
                )
        elif ratio > 1.0:
            recs.append(
                {
                    "priority": "info",
                    "action": "# Brak potrzeby czyszczenia",
                    "description": f"📊 Flatpak: {self.repo_bloat.get('actual_disk_usage_human', '?')} (normalne dla {len(self.installed_apps)} aplikacji)",
                    "explanation": (
                        f"Rzeczywiste użycie: {self.repo_bloat.get('actual_disk_usage_human', '?')}\n"
                        f"Rozmiar aplikacji: {self.repo_bloat.get('reported_size_human', '?')}\n"
                        f"Ratio: {ratio:.1f}x - {note}\n\n"
                        "✅ Twój Flatpak jest w dobrym stanie.\nOverhead jest normalny dla OSTree."
                    ),
                    "estimated_savings": "0 B",
                    "risk": "none",
                    "requires_confirmation": False,
                }
            )
        return recs

    def _rec_duplicates(self) -> List[Dict[str, Any]]:
        """Recommendations for duplicate apps."""
        recs: List[Dict[str, Any]] = []
        if not self.duplicate_apps:
            return recs
        total_dup_size = sum(d.get("total_size", 0) for d in self.duplicate_apps)
        if total_dup_size > FLATPAK_LEFTOVER_THRESHOLD_MB * 1024 * 1024:
            dup_names = [
                d["name"] for d in self.duplicate_apps[:MAX_DUPLICATE_APPS_SHOW]
            ]
            recs.append(
                {
                    "priority": "high",
                    "action": "flatpak uninstall <duplicate_app>",
                    "description": f"🔄 Usuń duplikaty aplikacji ({len(self.duplicate_apps)} znalezionych)",
                    "explanation": (
                        f"Masz zainstalowane wielokrotne wersje tych samych aplikacji:\n"
                        f"  {', '.join(dup_names)}\n\n"
                        "Możesz bezpiecznie usunąć starsze wersje:\n"
                        "  flatpak uninstall com.microsoft.EdgeDev\n"
                        "  flatpak uninstall synergy\n\n"
                        f"💰 Realne odzyskanie: {self._format_size(total_dup_size)}"
                    ),
                    "estimated_savings": self._format_size(total_dup_size),
                    "risk": "low",
                    "requires_confirmation": True,
                    "items": self.duplicate_apps,
                }
            )
        return recs

    def _rec_unused_runtimes(self) -> List[Dict[str, Any]]:
        """Recommendations for unused runtimes."""
        recs: List[Dict[str, Any]] = []
        total_unused = sum(r.size_bytes for r in self.unused_runtimes)
        if total_unused > FLATPAK_LEFTOVER_THRESHOLD_MB * 1024 * 1024:
            recs.append(
                {
                    "priority": "high",
                    "action": "flatpak uninstall --unused -y",
                    "description": "Usuń nieużywane runtime'y i stare wersje",
                    "explanation": (
                        "Ta komenda jest BEZPIECZNA - nie usuwa używanych aplikacji.\n"
                        "Usuwa:\n  - runtime'y nie wymagane przez żadną aplikację\n"
                        "  - stare wersje aplikacji\n  - nieużywane SDK\n\n"
                        f"💰 Realne odzyskanie: {self._format_size(total_unused)}"
                    ),
                    "estimated_savings": self._format_size(total_unused),
                    "risk": "low",
                    "requires_confirmation": True,
                }
            )
        return recs

    def _rec_large_apps(self) -> List[Dict[str, Any]]:
        """Recommendations for large apps."""
        recs: List[Dict[str, Any]] = []
        largest_apps = self.get_largest_apps(MAX_LARGE_APPS_SHOW)
        if not largest_apps:
            return recs
        total_large = sum(a["size"] for a in largest_apps)
        if total_large > 500 * 1024 * 1024:
            recs.append(
                {
                    "priority": "medium",
                    "action": "flatpak uninstall <app>",
                    "description": "📱 Usuń duże aplikacje (opcjonalnie)",
                    "explanation": (
                        "Największe aplikacje w Twoim systemie:\n"
                        + "\n".join(
                            f"  • {a['name']} - {a['size_human']}"
                            for a in largest_apps[:MAX_LARGE_APPS_SHOW]
                        )
                        + "\n\n💡 Jeśli nie używasz którejś, możesz ją usunąć:\n"
                        + f"  flatpak uninstall {largest_apps[0]['ref']}\n\n"
                        + f"💰 Potencjalne odzyskanie: do {self._format_size(total_large)}"
                    ),
                    "estimated_savings": f"do {self._format_size(total_large)}",
                    "risk": "medium",
                    "requires_confirmation": True,
                    "items": largest_apps,
                }
            )
        return recs

    def _rec_leftover_and_orphaned(self) -> List[Dict[str, Any]]:
        """Recommendations for leftover data and orphaned apps."""
        recs: List[Dict[str, Any]] = []
        total_leftover = sum(d.size_bytes for d in self.leftover_data)
        if total_leftover > FLATPAK_LEFTOVER_THRESHOLD_MB * 1024 * 1024:
            recs.append(
                {
                    "priority": "medium",
                    "action": "rm -rf ~/.var/app/<unused_app>",
                    "description": "Usuń dane po odinstalowanych aplikacjach",
                    "explanation": (
                        "Katalog ~/.var/app zawiera dane aplikacji.\n"
                        "Niektóre aplikacje zostały usunięte, ale dane zostały."
                    ),
                    "estimated_savings": self._format_size(total_leftover),
                    "risk": "medium",
                    "requires_confirmation": True,
                    "items": [
                        d.to_dict()
                        for d in sorted(
                            self.leftover_data, key=lambda x: -x.size_bytes
                        )[:10]
                    ],
                }
            )
        if self.orphaned_apps:
            recs.append(
                {
                    "priority": "low",
                    "action": "flatpak uninstall <orphaned_app>",
                    "description": "Usuń aplikacje z niedostępnymi remotes",
                    "explanation": (
                        "Te aplikacje pochodzą z remotes, które już nie istnieją.\n"
                        "Nie można ich zaktualizować."
                    ),
                    "estimated_savings": self._format_size(
                        sum(a.size_bytes for a in self.orphaned_apps)
                    ),
                    "risk": "medium",
                    "requires_confirmation": True,
                    "items": [a.to_dict() for a in self.orphaned_apps],
                }
            )
        return recs

    def _rec_hard_reset(self) -> List[Dict[str, Any]]:
        """Recommendation for full hard reset (only if > 50 GB)."""
        total = sum(a.size_bytes for a in self.installed_apps) + sum(
            r.size_bytes for r in self.installed_runtimes
        )
        if total > 50 * 1024 * 1024 * 1024:
            return [
                {
                    "priority": "low",
                    "action": "flatpak uninstall --all",
                    "description": "Hard reset - usuń WSZYSTKIE Flatpaki",
                    "explanation": (
                        "⚠️ OSTRZEŻENIE: To usuwa WSZYSTKIE aplikacje Flatpak!\n"
                        "Użyj tylko jeśli:\n  - masz mało ważnych aplikacji\n"
                        "  - chcesz zacząć od zera\nPotem instalujesz tylko to, czego potrzebujesz."
                    ),
                    "estimated_savings": self._format_size(total),
                    "risk": "high",
                    "requires_confirmation": True,
                }
            ]
        return []

    def get_cleanup_recommendations(self) -> List[Dict[str, Any]]:
        """Get list of cleanup recommendations with explanations"""
        recs: List[Dict[str, Any]] = []
        recs.extend(self._rec_repo_bloat())
        recs.extend(self._rec_duplicates())
        recs.extend(self._rec_unused_runtimes())
        recs.extend(self._rec_large_apps())
        if self.unused_runtimes or self.repo_bloat.get("bloat_detected"):
            recs.append(
                {
                    "priority": "low",
                    "action": "flatpak repair",
                    "description": "Napraw instalację Flatpak (opcjonalnie)",
                    "explanation": "Weryfikuje integralność instalacji.\nNie odzyskuje miejsca, ale naprawia błędy.",
                    "estimated_savings": "0 B",
                    "risk": "none",
                    "requires_confirmation": False,
                }
            )
        recs.extend(self._rec_leftover_and_orphaned())
        recs.extend(self._rec_hard_reset())
        return recs
