# System Architecture Analysis

## Overview

- **Project**: fixOS
- **Language**: python
- **Files**: 59
- **Lines**: 15339
- **Functions**: 379
- **Classes**: 66
- **Avg CC**: 5.0
- **Critical (CC≥10)**: 56

## Architecture

### fixos/ (7 files, 1210L, 36 functions)

- `config.py` — 422L, 7 methods, CC↑24
- `llm_shell.py` — 240L, 4 methods, CC↑15
- `watch.py` — 120L, 5 methods, CC↑12
- `platform_utils.py` — 184L, 10 methods, CC↑8
- `system_checks.py` — 156L, 8 methods, CC↑6
- _2 more files_

### fixos/agent/ (5 files, 1045L, 44 functions)

- `hitl_session.py` — 509L, 20 methods, CC↑20
- `autonomous_session.py` — 429L, 22 methods, CC↑8
- `autonomous.py` — 49L, 1 methods, CC↑1
- `hitl.py` — 36L, 1 methods, CC↑1
- `__init__.py` — 22L, 0 methods, CC↑0

### fixos/cli/ (18 files, 2625L, 58 functions)

- `cleanup_cmd.py` — 371L, 8 methods, CC↑23
- `ask_cmd.py` — 354L, 8 methods, CC↑18
- `fix_cmd.py` — 282L, 4 methods, CC↑18
- `scan_cmd.py` — 187L, 3 methods, CC↑18
- `report_cmd.py` — 115L, 1 methods, CC↑16
- _13 more files_

### fixos/diagnostics/ (7 files, 2111L, 59 functions)

- `disk_analyzer.py` — 419L, 15 methods, CC↑17
- `service_details.py` — 242L, 7 methods, CC↑17
- `flatpak_analyzer.py` — 332L, 12 methods, CC↑15
- `service_cleanup.py` — 355L, 8 methods, CC↑14
- `system_checks.py` — 512L, 9 methods, CC↑14
- _2 more files_

### fixos/features/ (6 files, 927L, 43 functions)

- `installer.py` — 202L, 11 methods, CC↑27
- `__init__.py` — 267L, 12 methods, CC↑15
- `auditor.py` — 127L, 5 methods, CC↑10
- `profiles.py` — 88L, 4 methods, CC↑8
- `renderer.py` — 124L, 4 methods, CC↑8
- _1 more files_

### fixos/fixes/ (1 files, 4L, 0 functions)

- `__init__.py` — 4L, 0 methods, CC↑0

### fixos/interactive/ (2 files, 417L, 12 functions)

- `cleanup_planner.py` — 417L, 12 methods, CC↑18
- `__init__.py` — 0L, 0 methods, CC↑0

### fixos/orchestrator/ (5 files, 988L, 39 functions)

- `orchestrator.py` — 382L, 11 methods, CC↑17
- `graph.py` — 163L, 11 methods, CC↑13
- `executor.py` — 272L, 11 methods, CC↑11
- `rollback.py` — 162L, 6 methods, CC↑7
- `__init__.py` — 9L, 0 methods, CC↑0

### fixos/plugins/ (3 files, 237L, 12 functions)

- `registry.py` — 127L, 8 methods, CC↑7
- `base.py` — 99L, 4 methods, CC↑2
- `__init__.py` — 11L, 0 methods, CC↑0

### fixos/plugins/builtin/ (7 files, 776L, 32 functions)

- `security.py` — 171L, 6 methods, CC↑16
- `resources.py` — 137L, 6 methods, CC↑14
- `disk.py` — 113L, 4 methods, CC↑12
- `hardware.py` — 129L, 6 methods, CC↑12
- `audio.py` — 107L, 5 methods, CC↑10
- _2 more files_

### fixos/profiles/ (1 files, 65L, 3 functions)

- `__init__.py` — 65L, 3 methods, CC↑4

### fixos/providers/ (4 files, 612L, 14 functions)

- `llm.py` — 206L, 6 methods, CC↑15
- `llm_analyzer.py` — 333L, 8 methods, CC↑13
- `__init__.py` — 2L, 0 methods, CC↑0
- `schemas.py` — 71L, 0 methods, CC↑0

### fixos/utils/ (5 files, 889L, 27 functions)

- `anonymizer.py` — 299L, 9 methods, CC↑18
- `terminal.py` — 316L, 8 methods, CC↑16
- `web_search.py` — 254L, 9 methods, CC↑9
- `timeout.py` — 17L, 1 methods, CC↑1
- `__init__.py` — 3L, 0 methods, CC↑0

### root/ (2 files, 59L, 0 functions)

- `project.sh` — 14L, 0 methods, CC↑0
- `setup.py` — 45L, 0 methods, CC↑0

## Key Exports

- **FeatureInstaller** (class, CC̄=4.9)
  - `_install_package` CC=27 ⚠ split
- **FixOsConfig** (class, CC̄=8.3)
- **interactive_provider_setup** (function, CC=24) ⚠ split
- **cleanup_services** (function, CC=15) ⚠ split
- **HITLSession** (class, CC̄=4.3)
  - `_process_turn` CC=20 ⚠ split
- **fix** (function, CC=18) ⚠ split
- **CleanupPlanner** (class, CC̄=6.9)
  - `_generate_recommendations` CC=18 ⚠ split
- **anonymize** (function, CC=15) ⚠ split
- **DiskAnalyzer** (class, CC̄=7.5)
  - `_identify_cache_type` CC=17 ⚠ split
- **ServiceDetailsProvider** (class, CC̄=6.9)
  - `_docker` CC=17 ⚠ split
- **FixOrchestrator** (class, CC̄=5.2)
  - `run_sync` CC=17 ⚠ split
- **report** (function, CC=16) ⚠ split
- **Plugin** (class, CC̄=7.7)
  - `diagnose` CC=16 ⚠ split
- **render_md** (function, CC=16) ⚠ split
- **features_install** (function, CC=15) ⚠ split
- **FlatpakAnalyzer** (class, CC̄=7.0)
  - `_find_leftover_data` CC=15 ⚠ split
- **SystemDetector** (class, CC̄=5.8)
  - `_detect_de` CC=15 ⚠ split
- **run_llm_shell** (function, CC=15) ⚠ split
- **LLMClient** (class, CC̄=5.5)
  - `chat` CC=15 ⚠ split
- **LLMAnalyzer** (class, CC̄=5.9)
- **Plugin** (class, CC̄=7.2)
- **Plugin** (class, CC̄=5.2)
- **FeatureAuditor** (class, CC̄=5.2)
- **FeatureRenderer** (class, CC̄=5.0)
- **NaturalLanguageGroup** (class, CC̄=6.0)

## Hotspots (High Fan-Out)

- **HITLSession._process_turn** — fan-out=28: Analysis pipeline, 28 stages
- **orchestrate** — fan-out=24: Zaawansowana orkiestracja napraw z grafem problemów.


Różnica od 'fix':
  - Bu
- **_cleanup_flatpak_detailed** — fan-out=24: Detailed interactive Flatpak cleanup showing unused runtimes, 
leftover data, an
- **run_llm_shell** — fan-out=23: Uruchamia interaktywny shell LLM z przekazanymi danymi diagnostycznymi.

Args:
 
- **interactive_provider_setup** — fan-out=23: Interaktywny wybór providera gdy brak konfiguracji.
Wyświetla numerowaną listę p
- **report** — fan-out=22: Eksport wyników diagnostyki do raportu HTML/Markdown/JSON.


Przykłady:
  fixos
- **fix** — fan-out=21: Przeprowadza pełną diagnostykę i uruchamia sesję naprawczą z LLM.


Tryby:
  hi

## Refactoring Priorities

| # | Action | Impact | Effort |
|---|--------|--------|--------|
| 1 | Split FeatureInstaller._install_package (CC=27 → target CC<10) | high | low |
| 2 | Split god module fixos/agent/hitl_session.py (509L, 2 classes) | high | high |
| 3 | Split god module fixos/diagnostics/system_checks.py (512L, 0 classes) | high | high |
| 4 | Split run_llm_shell (CC=15 → target CC<10) | medium | low |
| 5 | Split DiskAnalyzer._identify_cache_type (CC=17 → target CC<10) | medium | low |
| 6 | Split ServiceDetailsProvider._docker (CC=17 → target CC<10) | medium | low |
| 7 | Split interactive_provider_setup (CC=24 → target CC<10) | medium | low |
| 8 | Split FlatpakAnalyzer._find_leftover_data (CC=15 → target CC<10) | medium | low |
| 9 | Split HITLSession._process_turn (CC=20 → target CC<10) | medium | low |
| 10 | Split SystemDetector._detect_de (CC=15 → target CC<10) | medium | low |

## Context for LLM

When suggesting changes:
1. Start from hotspots and high-CC functions
2. Follow refactoring priorities above
3. Maintain public API surface — keep backward compatibility
4. Prefer minimal, incremental changes

