"""Shared utilities for diagnostic modules."""

from __future__ import annotations


def format_size(size_bytes: int | float) -> str:
    """Format bytes to human-readable string (B/KB/MB/GB/TB/PB)."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} PB"
