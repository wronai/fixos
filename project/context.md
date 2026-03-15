# System Architecture Analysis

## Overview

- **Project**: fixOS
- **Language**: python
- **Files**: 20
- **Lines**: 11252
- **Functions**: 203
- **Classes**: 31
- **Avg CC**: 6.0
- **Critical (CC≥10)**: 41

## Architecture

### fixos/ (7 files, 2680L, 61 functions)

- `cli.py` — 1589L, 30 methods, CC↑37
- `config.py` — 422L, 7 methods, CC↑24
- `llm_shell.py` — 241L, 4 methods, CC↑15
- `platform_utils.py` — 184L, 10 methods, CC↑8
- `system_checks.py` — 156L, 8 methods, CC↑6
- _2 more files_

### fixos/agent/ (3 files, 815L, 17 functions)

- `hitl.py` — 462L, 10 methods, CC↑34
- `autonomous.py` — 350L, 7 methods, CC↑21
- `__init__.py` — 3L, 0 methods, CC↑0

### fixos/diagnostics/ (4 files, 1828L, 42 functions)

- `service_scanner.py` — 895L, 18 methods, CC↑18
- `disk_analyzer.py` — 419L, 15 methods, CC↑17
- `system_checks.py` — 512L, 9 methods, CC↑14
- `__init__.py` — 2L, 0 methods, CC↑0

### fixos/fixes/ (1 files, 4L, 0 functions)

- `__init__.py` — 4L, 0 methods, CC↑0

### fixos/interactive/ (2 files, 417L, 12 functions)

- `cleanup_planner.py` — 417L, 12 methods, CC↑18
- `__init__.py` — 0L, 0 methods, CC↑0

### fixos/orchestrator/ (4 files, 826L, 33 functions)

- `orchestrator.py` — 382L, 11 methods, CC↑17
- `graph.py` — 163L, 11 methods, CC↑13
- `executor.py` — 272L, 11 methods, CC↑11
- `__init__.py` — 9L, 0 methods, CC↑0

### fixos/providers/ (3 files, 477L, 12 functions)

- `llm.py` — 142L, 4 methods, CC↑15
- `llm_analyzer.py` — 333L, 8 methods, CC↑13
- `__init__.py` — 2L, 0 methods, CC↑0

### fixos/utils/ (4 files, 871L, 26 functions)

- `anonymizer.py` — 298L, 9 methods, CC↑18
- `terminal.py` — 316L, 8 methods, CC↑16
- `web_search.py` — 254L, 9 methods, CC↑9
- `__init__.py` — 3L, 0 methods, CC↑0

### root/ (2 files, 59L, 0 functions)

- `project.sh` — 14L, 0 methods, CC↑0
- `setup.py` — 45L, 0 methods, CC↑0

## Key Exports

- **NaturalLanguageGroup** (class, CC̄=6.0)
- **fix** (function, CC=18) ⚠ split
- **execute_cleanup_actions** (function, CC=24) ⚠ split
- **token_set** (function, CC=18) ⚠ split
- **cleanup_services** (function, CC=33) ⚠ split
- **run_hitl_session** (function, CC=34) ⚠ split
- **FixOsConfig** (class, CC̄=8.3)
- **interactive_provider_setup** (function, CC=24) ⚠ split
- **run_autonomous_session** (function, CC=21) ⚠ split
- **ServiceDataScanner** (class, CC̄=5.0)
  - `_get_docker_details` CC=18 ⚠ split
- **CleanupPlanner** (class, CC̄=6.9)
  - `_generate_recommendations` CC=18 ⚠ split
- **anonymize** (function, CC=15) ⚠ split
- **DiskAnalyzer** (class, CC̄=7.5)
  - `_identify_cache_type` CC=17 ⚠ split
- **FixOrchestrator** (class, CC̄=5.2)
  - `run_sync` CC=17 ⚠ split
- **render_md** (function, CC=16) ⚠ split
- **run_llm_shell** (function, CC=15) ⚠ split
- **LLMClient** (class, CC̄=6.2)
  - `chat` CC=15 ⚠ split
- **LLMAnalyzer** (class, CC̄=5.9)

## Hotspots (High Fan-Out)

- **run_hitl_session** — fan-out=42: Runs interactive HITL session with full transparency.
- **orchestrate** — fan-out=30: Orkiestracja napraw z grafem kaskadowych problemów.


Różnica od 'fix':
  - Bud
- **run_autonomous_session** — fan-out=28: Uruchamia autonomiczny tryb agenta.
- **run_llm_shell** — fan-out=23: Uruchamia interaktywny shell LLM z przekazanymi danymi diagnostycznymi.

Args:
 
- **interactive_provider_setup** — fan-out=23: Interaktywny wybór providera gdy brak konfiguracji.
Wyświetla numerowaną listę p
- **token_set** — fan-out=23: Zapisuje token API do pliku .env.


Przykłady:
  fixos token set AIzaSy...     
- **fix** — fan-out=21: Przeprowadza pełną diagnostykę i uruchamia sesję naprawczą z LLM.


Tryby:
  hi

## Refactoring Priorities

| # | Action | Impact | Effort |
|---|--------|--------|--------|
| 1 | Split run_hitl_session (CC=34 → target CC<10) | high | low |
| 2 | Split _handle_natural_command (CC=37 → target CC<10) | high | low |
| 3 | Split cleanup_services (CC=33 → target CC<10) | high | low |
| 4 | Split god module fixos/cli.py (1589L, 1 classes) | high | high |
| 5 | Split god module fixos/diagnostics/service_scanner.py (895L, 3 classes) | high | high |
| 6 | Split god module fixos/diagnostics/system_checks.py (512L, 0 classes) | high | high |
| 7 | Split run_llm_shell (CC=15 → target CC<10) | medium | low |
| 8 | Split DiskAnalyzer._identify_cache_type (CC=17 → target CC<10) | medium | low |
| 9 | Split interactive_provider_setup (CC=24 → target CC<10) | medium | low |
| 10 | Split LLMClient.chat (CC=15 → target CC<10) | medium | low |

## Context for LLM

When suggesting changes:
1. Start from hotspots and high-CC functions
2. Follow refactoring priorities above
3. Maintain public API surface — keep backward compatibility
4. Prefer minimal, incremental changes

