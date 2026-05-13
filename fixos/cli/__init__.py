"""
fixOS CLI package - refactored structure
"""

from pathlib import Path  # For backward compat with tests

from fixos.cli.main import cli, main

__all__ = ["cli", "main", "Path"]
