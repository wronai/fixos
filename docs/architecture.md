# fixOS — Architecture

> 47 modules | 275 functions | 49 classes

## How It Works

`fixOS` analyzes source code via a multi-stage pipeline:

```
Source files  ──►  code2llm (tree-sitter + AST)  ──►  AnalysisResult
                                                          │
              ┌───────────────────────────────────────────┘
              ▼
    ┌─────────────────────┐
    │   12 Generators     │
    │  ─────────────────  │
    │  README.md          │
    │  docs/api/          │
    │  docs/modules/      │
    │  docs/architecture   │
    │  docs/coverage      │
    │  examples/          │
    │  mkdocs.yml         │
    │  CONTRIBUTING.md    │
    └─────────────────────┘
```

**Analysis algorithms:**

1. **AST parsing** — language-specific parsers (tree-sitter) extract syntax trees
2. **Cyclomatic complexity** — counts independent code paths per function
3. **Fan-in / fan-out** — measures module coupling (how many modules import/are imported by each)
4. **Docstring extraction** — parses Google/NumPy/Sphinx-style docstrings into structured data
5. **Pattern detection** — identifies design patterns (Factory, Singleton, Observer, etc.)
6. **Dependency scanning** — reads pyproject.toml / requirements.txt / setup.py

## Architecture Layers

```mermaid
graph TD
    Other["Other<br/>35 modules"]
    API___CLI["API / CLI<br/>1 modules"]
    Config["Config<br/>1 modules"]
    Analysis["Analysis<br/>3 modules"]
    Core["Core<br/>7 modules"]
    Other --> API___CLI
    API___CLI --> Config
    Config --> Analysis
    Analysis --> Core
```

### Other

- `docs.examples.advanced_usage`
- `docs.examples.quickstart`
- `fixos`
- `fixos.agent`
- `fixos.agent.autonomous`
- `fixos.agent.hitl`
- `fixos.anonymizer`
- `fixos.diagnostics`
- `fixos.diagnostics.system_checks`
- `fixos.fixes`
- `fixos.interactive`
- `fixos.interactive.cleanup_planner`
- `fixos.llm_shell`
- `fixos.orchestrator`
- `fixos.orchestrator.executor`
- `fixos.orchestrator.graph`
- `fixos.orchestrator.orchestrator`
- `fixos.orchestrator.rollback`
- `fixos.plugins`
- `fixos.plugins.builtin`
- `fixos.plugins.builtin.audio`
- `fixos.plugins.builtin.disk`
- `fixos.plugins.builtin.hardware`
- `fixos.plugins.builtin.resources`
- `fixos.plugins.builtin.security`
- `fixos.plugins.builtin.thumbnails`
- `fixos.plugins.registry`
- `fixos.profiles`
- `fixos.providers`
- `fixos.providers.llm`
- `fixos.providers.schemas`
- `fixos.system_checks`
- `fixos.watch`
- `project`
- `setup`

### API / CLI

- `fixos.cli`

### Config

- `fixos.config`

### Analysis

- `fixos.diagnostics.disk_analyzer`
- `fixos.diagnostics.service_scanner`
- `fixos.providers.llm_analyzer`

### Core

- `fixos.platform_utils`
- `fixos.plugins.base`
- `fixos.utils`
- `fixos.utils.anonymizer`
- `fixos.utils.terminal`
- `fixos.utils.timeout`
- `fixos.utils.web_search`

## Module Dependency Graph

```mermaid
graph LR
    note[No internal dependencies detected]
```

## Key Classes

```mermaid
classDiagram
    class ServiceDataScanner {
        -__init__(self, threshold_mb) None
        +scan_all_services(self) None
        +scan_service(self, service_type) None
        -_analyze_service_path(self, service_type, path) None
        -_get_path_size_mb(self, path) None
        -_get_service_details(self, service_type, path) None
        -_get_conda_details(self) None
        -_get_docker_details(self) None
        ... +9 more
    }
    class DiskAnalyzer {
        -__init__(self, base_path) None
        +analyze_disk_usage(self, path) None
        -_get_disk_status(self, usage_percent) None
        +get_large_files(self, path, min_size_mb) None
        +get_cache_dirs(self, path, max_dirs) None
        +get_log_dirs(self, path, max_dirs) None
        +get_temp_dirs(self, path, max_dirs) None
        +suggest_cleanup_actions(self, path) None
        ... +6 more
    }
    class FixOrchestrator {
        -__init__(self, config, executor) None
        +load_from_diagnostics(self, diagnostics) None
        +load_from_dict(self, problems_data) None
        +run_sync(self, confirm_fn, progress_fn) None
        +run_async(self, confirm_fn, progress_fn) None
        -_evaluate_and_rediagnose(self, problem, result) None
        -_parse_json(self, raw) None
        -_log(self, event, data) None
        ... +3 more
    }
    class CleanupPlanner {
        -__init__(self) None
        +group_by_category(self, suggestions) None
        +prioritize_actions(self, grouped_actions) None
        +create_cleanup_plan(self, suggestions) None
        +interactive_selection(self, plan) None
        -_dict_to_action(self, suggestion) None
        -_action_to_dict(self, action) None
        -_get_category_for_action(self, action) None
        ... +2 more
    }
    class PluginRegistry {
        -__init__(self) None
        +discover(self) None
        -_register_builtins(self) None
        -_register_external(self) None
        +register(self, plugin) None
        +list_plugins(self, runnable_only) None
        +get_plugin(self, name) None
        +run(self, modules, progress_callback) None
        ... +1 more
    }
    class ProblemGraph {
        -__init__(self) None
        +add(self, problem) None
        +get(self, problem_id) None
        +next_actionable(self) None
        +all_done(self) None
        +pending_count(self) None
        +summary(self) None
        +render_tree(self) None
        ... +1 more
    }
    class CommandExecutor {
        -__init__(self, default_timeout, require_confirmation) None
        +is_dangerous(self, command) None
        +needs_sudo(self, command) None
        +add_sudo(self, command) None
        -_make_noninteractive(self, command) None
        +check_idempotent(self, command) None
        +execute_sync(self, command, timeout) None
        +execute(self, command, timeout) None
    }
    class LLMAnalyzer {
        -__init__(self, llm_client) None
        +analyze_disk_issues(self, disk_data) None
        +analyze_failed_action(self, action, error) None
        +analyze_complex_pattern(self, pattern_data) None
        -_sanitize_suggestion(self, suggestion) None
        -_create_fallback_analysis(self, error_message) None
        +enhance_heuristics_with_llm(self, heuristic_suggestions, disk_data) None
    }
    class LLMClient {
        -__init__(self, config) None
        +chat(self, messages) None
        +chat_stream(self, messages) None
        +fixos.providers.llm.LLMClient.total_tokens()
        +chat_structured(self, messages, response_model) None
        -_extract_json(text) None
        +ping(self) None
    }
    class Plugin {
        +diagnose(self) None
        -_check_cpu(self) None
        -_check_ram(self) None
        -_check_top_processes(self) None
        -_check_zombies(self) None
        -_check_swap(self) None
    }
    class Plugin {
        +diagnose(self) None
        -_check_firewall(self) None
        -_check_selinux(self) None
        -_check_open_ports(self) None
        -_check_ssh(self) None
        -_check_fail2ban(self) None
    }
    class Plugin {
        +diagnose(self) None
        -_check_gpu(self) None
        -_check_battery(self) None
        -_check_touchpad(self) None
        -_check_camera(self) None
        -_check_dmi(self) None
    }
    class RollbackSession {
        +record(self, command, rollback_cmd) None
        +get_rollback_commands(self) None
        +rollback_last(self, n, dry_run) None
        -_save(self) None
        +load(cls, session_id) None
        +list_sessions(cls, limit) None
    }
    class WatchDaemon {
        -__init__(self, interval, modules) None
        +run(self) None
        +stop(self) None
        -_check_for_new_issues(self, results) None
        -_notify(message) None
    }
    class Plugin {
        +diagnose(self) None
        -_check_alsa(self) None
        -_check_pipewire(self) None
        -_check_wireplumber(self) None
        -_check_sof(self) None
    }
```

## Detected Patterns

- **recursion__dict_to_markdown** (recursion) — confidence: 90%, functions: `fixos.utils.anonymizer._dict_to_markdown`

## Public Entry Points

- `fixos.platform_utils.install_package_cmd` — Returns the install command for the detected package manager.
- `fixos.llm_shell.run_llm_shell` — Uruchamia interaktywny shell LLM z przekazanymi danymi diagnostycznymi.
- `fixos.diagnostics.system_checks.diagnose_audio` — Diagnostyka dźwięku (ALSA/PipeWire/PulseAudio/SOF).
- `fixos.diagnostics.system_checks.diagnose_thumbnails` — Diagnostyka podglądów plików (thumbnails) w system.
- `fixos.diagnostics.system_checks.diagnose_hardware` — Diagnostyka sprzętu laptopa/desktopa (ACPI, kamera, touchpad, DMI).
- `fixos.diagnostics.system_checks.diagnose_system` — System metrics – cross-platform: CPU, RAM, disks, processes.
- `fixos.diagnostics.system_checks.diagnose_security` — Diagnostyka bezpieczeństwa systemu i sieci.
- `fixos.diagnostics.system_checks.diagnose_resources` — Diagnostyka zasobów systemowych.
- `fixos.diagnostics.system_checks.get_full_diagnostics` — Zbiera diagnostykę z wybranych modułów.
- `fixos.diagnostics.disk_analyzer.main` — Test the disk analyzer
- `fixos.cli.add_common_options`
- `fixos.cli.add_shared_options` — Shared options for both scan and fix commands
- `fixos.cli.ask` — Wykonaj polecenie w języku naturalnym.
- `fixos.cli.scan` — Przeprowadza diagnostykę systemu.
- `fixos.cli.fix` — Przeprowadza pełną diagnostykę i uruchamia sesję naprawczą z LLM.
- `fixos.cli.token` — Zarządzanie tokenami API LLM.
- `fixos.cli.token_set` — Zapisuje token API do pliku .env.
- `fixos.cli.token_show` — Pokazuje aktualnie skonfigurowany token (zamaskowany).
- `fixos.cli.token_clear` — Usuwa token z pliku .env.
- `fixos.cli.config` — Zarządzanie konfiguracją fixos.
- `fixos.cli.config_show` — Wyświetla aktualną konfigurację.
- `fixos.cli.config_init` — Tworzy plik .env na podstawie szablonu .env.example.
- `fixos.cli.config_set` — Ustawia wartość w pliku .env.
- `fixos.cli.llm_providers` — Lista providerów LLM z linkami do generowania kluczy API.
- `fixos.cli.providers` — Lista dostępnych providerów LLM (skrócona). Użyj 'fixos llm' po więcej.
- `fixos.cli.test_llm` — Testuje połączenie z wybranym providerem LLM.
- `fixos.cli.orchestrate` — Orkiestracja napraw z grafem kaskadowych problemów.
- `fixos.cli.cleanup_services` — Skanuje i czyści dane usług przekraczające próg.
- `fixos.cli.rollback` — Zarządzanie cofaniem operacji fixOS.
- `fixos.cli.rollback_list` — Pokaż historię sesji naprawczych.
- `fixos.cli.rollback_show` — Pokaż szczegóły sesji rollback.
- `fixos.cli.rollback_undo` — Cofnij operacje z podanej sesji.
- `fixos.cli.watch` — Monitorowanie systemu w tle z powiadomieniami.
- `fixos.cli.profile` — Zarządzanie profilami diagnostycznymi.
- `fixos.cli.profile_list` — Pokaż dostępne profile diagnostyczne.
- `fixos.cli.profile_show` — Pokaż szczegóły profilu diagnostycznego.
- `fixos.cli.quickfix` — Natychmiastowe naprawy bez API — baza znanych bugów.
- `fixos.cli.report` — Eksport wyników diagnostyki do raportu HTML/Markdown/JSON.
- `fixos.cli.history` — Historia napraw fixOS.
- `fixos.cli.main`
- `fixos.config.detect_provider_from_key` — Wykrywa provider na podstawie prefiksu klucza API.
- `fixos.providers.llm_analyzer.main` — Test the LLM analyzer
- `fixos.utils.anonymizer.anonymize` — Anonimizuje wrażliwe dane.
- `fixos.utils.timeout.timeout_handler` — Signal handler dla SIGALRM — rzuca SessionTimeout.
- `fixos.diagnostics.service_scanner.main` — Test the service data scanner
- `fixos.utils.terminal.colorize` — Return line unchanged – rich handles markup in render_md().
- `fixos.utils.terminal.render_md` — Print LLM markdown reply to terminal via rich.
- `fixos.interactive.cleanup_planner.main` — Test the cleanup planner

## Metrics Summary

| Metric | Value |
|--------|-------|
| Modules | 47 |
| Functions | 275 |
| Classes | 49 |
| CFG Nodes | 1684 |
| Patterns | 1 |
| Avg Complexity | 5.6 |
| Analysis Time | 4.1s |
