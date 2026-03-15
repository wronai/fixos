# Getting Started with fixOS

## Prerequisites

- Python >=3.10
- pip (or your preferred package manager)
- 7 dependencies (installed automatically)

## Installation

```bash
pip install fixos
```

To install from source:

```bash
git clone https://github.com/wronai/fixfedora
cd fixOS
pip install -e .
```

## Quick Start

### Command Line

```bash
# Generate full documentation for your project
fixOS ./path/to/your/project

# Preview what would be generated (no file writes)
fixOS ./path/to/your/project --dry-run

# Only regenerate README
fixOS ./path/to/your/project --readme-only
```

### Python API

```python
from fixos.agent.autonomous import run_autonomous_session

# Uruchamia autonomiczny tryb agenta.
result = run_autonomous_session("diagnostics", config=..., show_data=...)
```

## What's Next

- 📖 [API Reference](api.md) — Full function and class documentation
- 🏗️ [Architecture](architecture.md) — System design and module relationships
- 📊 [Coverage Report](coverage.md) — Docstring coverage analysis
- 🔗 [Dependency Graph](dependency-graph.md) — Module dependency visualization
