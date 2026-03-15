# fixOS — Module Reference

> 32 modules | 203 functions | 31 classes

## Module Overview

| Module | Lines | Functions | Classes | CC avg | Description | Source |
|--------|-------|-----------|---------|--------|-------------|--------|
| `fixos.agent.autonomous` | 350 | 6 | 3 | 6.1 | Tryb autonomiczny – agent sam diagnozuje i naprawia system. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/agent/autonomous.py) |
| `fixos.agent.hitl` | 462 | 10 | 2 | 6.8 | Tryb Human-in-the-Loop (HITL) – użytkownik zatwierdza każdą  | [source](https://github.com/wronai/fixfedora/blob/main/fixos/agent/hitl.py) |
| `fixos.anonymizer` | 86 | 2 | 0 | 4.5 | Moduł anonimizacji wrażliwych danych systemowych. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/anonymizer.py) |
| `fixos.cli` | 1589 | 29 | 1 | 9.2 | fixos CLI – wielopoziomowe komendy | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli.py) |
| `fixos.config` | 422 | 4 | 1 | 9.7 | Zarządzanie konfiguracją fixos. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/config.py) |
| `fixos.diagnostics.disk_analyzer` | 419 | 1 | 1 | 7.1 | Disk Analyzer Module for fixOS | [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/disk_analyzer.py) |
| `fixos.diagnostics.service_scanner` | 895 | 1 | 3 | 4.8 | Service Data Scanner for fixOS | [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/service_scanner.py) |
| `fixos.diagnostics.system_checks` | 512 | 9 | 0 | 5.4 | Diagnostyka systemu – rozszerzona o: | [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/system_checks.py) |
| `fixos.interactive.cleanup_planner` | 417 | 1 | 4 | 6.0 | Interactive Cleanup Planner for fixOS | [source](https://github.com/wronai/fixfedora/blob/main/fixos/interactive/cleanup_planner.py) |
| `fixos.llm_shell` | 241 | 4 | 1 | 6.8 | Interaktywny shell LLM do diagnostyki i naprawy systemu syst | [source](https://github.com/wronai/fixfedora/blob/main/fixos/llm_shell.py) |
| `fixos.orchestrator.executor` | 272 | 0 | 4 | 3.9 | CommandExecutor – bezpieczne wykonywanie komend systemowych. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/orchestrator/executor.py) |
| `fixos.orchestrator.graph` | 163 | 0 | 2 | 3.5 | Problem Graph – model danych dla kaskadowych problemów syste | [source](https://github.com/wronai/fixfedora/blob/main/fixos/orchestrator/graph.py) |
| `fixos.orchestrator.orchestrator` | 382 | 0 | 2 | 5.2 | FixOrchestrator – główna pętla egzekucji napraw. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/orchestrator/orchestrator.py) |
| `fixos.platform_utils` | 184 | 10 | 0 | 3.6 | Cross-platform utilities for fixos. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/platform_utils.py) |
| `fixos.providers.llm` | 142 | 0 | 2 | 6.2 | Ujednolicony klient LLM obsługujący wiele providerów przez O | [source](https://github.com/wronai/fixfedora/blob/main/fixos/providers/llm.py) |
| `fixos.providers.llm_analyzer` | 333 | 1 | 2 | 5.2 | LLM Analyzer for fixOS - Fallback analysis when heuristics a | [source](https://github.com/wronai/fixfedora/blob/main/fixos/providers/llm_analyzer.py) |
| `fixos.system_checks` | 156 | 8 | 0 | 2.6 | Moduł zbierający dane diagnostyczne z systemu system. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/system_checks.py) |
| `fixos.utils.anonymizer` | 299 | 7 | 1 | 6.6 | Anonimizacja wrażliwych danych systemowych z podglądem dla u | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/anonymizer.py) |
| `fixos.utils.terminal` | 316 | 8 | 1 | 5.2 | Terminal rendering utilities – shared between hitl, orchestr | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/terminal.py) |
| `fixos.utils.web_search` | 254 | 9 | 1 | 4.9 | Zewnętrzne źródła wiedzy – fallback gdy LLM nie zna rozwiąza | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/web_search.py) |

## fixos

### `fixos.agent.autonomous` [source](https://github.com/wronai/fixfedora/blob/main/fixos/agent/autonomous.py)

Tryb autonomiczny – agent sam diagnozuje i naprawia system.

**`AgentReport`** [source](https://github.com/wronai/fixfedora/blob/main/fixos/agent/autonomous.py#L77)

| Method | Args | Returns | CC |
|--------|------|---------|----|
| `summary` | `` | `—` | 4 |

**`FixAction`** [source](https://github.com/wronai/fixfedora/blob/main/fixos/agent/autonomous.py#L68)

**`SessionTimeout`** (Exception) [source](https://github.com/wronai/fixfedora/blob/main/fixos/agent/autonomous.py#L100)

- `run_autonomous_session(diagnostics, config, show_data, max_fixes)` — Uruchamia autonomiczny tryb agenta. [source](https://github.com/wronai/fixfedora/blob/main/fixos/agent/autonomous.py#L140)

### `fixos.agent.hitl` [source](https://github.com/wronai/fixfedora/blob/main/fixos/agent/hitl.py)

Tryb Human-in-the-Loop (HITL) – użytkownik zatwierdza każdą akcję.

**`CmdResult`** [source](https://github.com/wronai/fixfedora/blob/main/fixos/agent/hitl.py#L76)

**`SessionTimeout`** (Exception) [source](https://github.com/wronai/fixfedora/blob/main/fixos/agent/hitl.py#L67)

- `run_hitl_session(diagnostics, config, show_data)` — Runs interactive HITL session with full transparency. [source](https://github.com/wronai/fixfedora/blob/main/fixos/agent/hitl.py#L226)

### `fixos.anonymizer` [source](https://github.com/wronai/fixfedora/blob/main/fixos/anonymizer.py)

Moduł anonimizacji wrażliwych danych systemowych.

- `anonymize(data_str)` — Anonimizuje wrażliwe dane w stringu. [source](https://github.com/wronai/fixfedora/blob/main/fixos/anonymizer.py#L30)
- `get_sensitive_values()` — Zbiera aktualne wrażliwe wartości systemowe do zamaskowania. [source](https://github.com/wronai/fixfedora/blob/main/fixos/anonymizer.py#L12)

### `fixos.cli` [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli.py)

fixos CLI – wielopoziomowe komendy

**`NaturalLanguageGroup`** (click.Group) [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli.py#L81)

| Method | Args | Returns | CC |
|--------|------|---------|----|
| `resolve_command` | `ctx, args` | `—` | 6 |

- `add_common_options(fn)` [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli.py#L50)
- `add_shared_options(func)` — Shared options for both scan and fix commands [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli.py#L55)
- `ask(prompt, dry_run)` — Wykonaj polecenie w języku naturalnym. [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli.py#L121)
- `cleanup_services(threshold, services, json_output, cleanup, dry_run, list_only)` — Skanuje i czyści dane usług przekraczające próg. [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli.py#L1435)
- `cli(ctx, dry_run)` — fixos – AI-powered diagnostyka i naprawa Linux, Windows, macOS. [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli.py#L92)
- `config()` — Zarządzanie konfiguracją fixos. [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli.py#L1071)
- `config_init(force)` — Tworzy plik .env na podstawie szablonu .env.example. [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli.py#L1091)
- `config_set(key, value)` — Ustawia wartość w pliku .env. [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli.py#L1123)
- `config_show()` — Wyświetla aktualną konfigurację. [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli.py#L1077)
- `execute_cleanup_actions(actions, cfg, llm_fallback)` — Execute cleanup actions with safety checks [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli.py#L851)
- `fix(provider, token, model, no_banner, mode, timeout, modules, no_show_data, output, max_fixes, disc, dry_run, interactive, json_output, llm_fallback)` — Przeprowadza pełną diagnostykę i uruchamia sesję naprawczą z LLM. [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli.py#L665)
- `handle_disk_cleanup_mode(disk_analysis, cfg, dry_run, interactive, json_output, llm_fallback)` — Handle disk cleanup mode with interactive planning [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli.py#L781)
- `llm_providers(free)` — Lista providerów LLM z linkami do generowania kluczy API. [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli.py#L1155)
- `main()` [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli.py#L1584)
- `orchestrate(provider, token, model, no_banner, mode, modules, dry_run, max_iterations, output)` — Orkiestracja napraw z grafem kaskadowych problemów. [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli.py#L1295)
- `providers()` — Lista dostępnych providerów LLM (skrócona). Użyj 'fixos llm' po więcej. [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli.py#L1231)
- `scan(modules, output, show_raw, no_banner, disc, dry_run, interactive, json_output, llm_fallback)` — Przeprowadza diagnostykę systemu. [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli.py#L494)
- `test_llm(provider, token, model, no_banner)` — Testuje połączenie z wybranym providerem LLM. [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli.py#L1251)
- `token()` — Zarządzanie tokenami API LLM. [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli.py#L966)
- `token_clear(env_file)` — Usuwa token z pliku .env. [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli.py#L1052)
- `token_set(key, provider, env_file)` — Zapisuje token API do pliku .env. [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli.py#L975)
- `token_show()` — Pokazuje aktualnie skonfigurowany token (zamaskowany). [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli.py#L1037)
- `try_llm_fallback_for_failures(failed_actions, cfg)` — Use LLM to analyze and suggest fixes for failed cleanup actions [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli.py#L937)

### `fixos.config` [source](https://github.com/wronai/fixfedora/blob/main/fixos/config.py)

Zarządzanie konfiguracją fixos.

**`FixOsConfig`** [source](https://github.com/wronai/fixfedora/blob/main/fixos/config.py#L156)

| Method | Args | Returns | CC |
|--------|------|---------|----|
| `load` | `cls` | `—` | 14 |
| `validate` | `` | `—` | 4 |
| `summary` | `` | `—` | 7 |

- `detect_provider_from_key(key)` — Wykrywa provider na podstawie prefiksu klucza API. [source](https://github.com/wronai/fixfedora/blob/main/fixos/config.py#L309)
- `get_providers_list()` — Zwraca listę providerów jako listę słowników. [source](https://github.com/wronai/fixfedora/blob/main/fixos/config.py#L410)
- `interactive_provider_setup()` — Interaktywny wybór providera gdy brak konfiguracji. [source](https://github.com/wronai/fixfedora/blob/main/fixos/config.py#L317)

### `fixos.diagnostics.disk_analyzer` [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/disk_analyzer.py)

Disk Analyzer Module for fixOS

**`DiskAnalyzer`** [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/disk_analyzer.py#L15)
: Analyzes disk usage and provides cleanup suggestions

| Method | Args | Returns | CC |
|--------|------|---------|----|
| `analyze_disk_usage` | `path` | `—` | 4 |
| `get_large_files` | `path, min_size_mb, max_files` | `—` | 7 |
| `get_cache_dirs` | `path, max_dirs` | `—` | 10 |
| `get_log_dirs` | `path, max_dirs` | `—` | 9 |
| `get_temp_dirs` | `path, max_dirs` | `—` | 9 |
| `suggest_cleanup_actions` | `path` | `—` | 13 |

- `main()` — Test the disk analyzer [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/disk_analyzer.py#L411)

### `fixos.diagnostics.service_scanner` [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/service_scanner.py)

Service Data Scanner for fixOS

**`ServiceDataInfo`** [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/service_scanner.py#L70)
: Information about service data

**`ServiceDataScanner`** [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/service_scanner.py#L87)
: Scans for large service data directories and allows cleanup

| Method | Args | Returns | CC |
|--------|------|---------|----|
| `scan_all_services` | `` | `—` | 3 |
| `scan_service` | `service_type` | `—` | 7 |
| `get_cleanup_plan` | `selected_services` | `—` | 14 |
| `cleanup_service` | `service_type, dry_run` | `—` | 4 |

**`ServiceType`** (Enum) [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/service_scanner.py#L17)

- `main()` — Test the service data scanner [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/service_scanner.py#L887)

### `fixos.diagnostics.system_checks` [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/system_checks.py)

Diagnostyka systemu – rozszerzona o:

- `diagnose_audio()` — Diagnostyka dźwięku (ALSA/PipeWire/PulseAudio/SOF). [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/system_checks.py#L49)
- `diagnose_hardware()` — Diagnostyka sprzętu laptopa/desktopa (ACPI, kamera, touchpad, DMI). [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/system_checks.py#L165)
- `diagnose_resources()` — Diagnostyka zasobów systemowych. [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/system_checks.py#L384)
- `diagnose_security()` — Diagnostyka bezpieczeństwa systemu i sieci. [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/system_checks.py#L303)
- `diagnose_system()` — System metrics – cross-platform: CPU, RAM, disks, processes. [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/system_checks.py#L204)
- `diagnose_thumbnails()` — Diagnostyka podglądów plików (thumbnails) w system. [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/system_checks.py#L106)
- `get_full_diagnostics(modules, progress_callback)` — Zbiera diagnostykę z wybranych modułów. [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/system_checks.py#L482)

### `fixos.interactive.cleanup_planner` [source](https://github.com/wronai/fixfedora/blob/main/fixos/interactive/cleanup_planner.py)

Interactive Cleanup Planner for fixOS

**`CleanupAction`** [source](https://github.com/wronai/fixfedora/blob/main/fixos/interactive/cleanup_planner.py#L32)
: Represents a cleanup action

**`CleanupPlanner`** [source](https://github.com/wronai/fixfedora/blob/main/fixos/interactive/cleanup_planner.py#L52)
: Interactive cleanup planning and grouping system

| Method | Args | Returns | CC |
|--------|------|---------|----|
| `group_by_category` | `suggestions` | `—` | 5 |
| `prioritize_actions` | `grouped_actions` | `—` | 11 |
| `create_cleanup_plan` | `suggestions` | `—` | 12 |
| `interactive_selection` | `plan` | `—` | 5 |

**`CleanupType`** (Enum) [source](https://github.com/wronai/fixfedora/blob/main/fixos/interactive/cleanup_planner.py#L20)

**`Priority`** (Enum) [source](https://github.com/wronai/fixfedora/blob/main/fixos/interactive/cleanup_planner.py#L13)

- `main()` — Test the cleanup planner [source](https://github.com/wronai/fixfedora/blob/main/fixos/interactive/cleanup_planner.py#L385)

### `fixos.llm_shell` [source](https://github.com/wronai/fixfedora/blob/main/fixos/llm_shell.py)

Interaktywny shell LLM do diagnostyki i naprawy systemu system.

**`SessionTimeout`** (Exception) [source](https://github.com/wronai/fixfedora/blob/main/fixos/llm_shell.py#L51)

- `execute_command(cmd)` — Wykonuje komendę systemową z potwierdzeniem użytkownika. [source](https://github.com/wronai/fixfedora/blob/main/fixos/llm_shell.py#L67)
- `format_time(seconds)` [source](https://github.com/wronai/fixfedora/blob/main/fixos/llm_shell.py#L59)
- `run_llm_shell(diagnostics_data, token, model, timeout, verbose, base_url)` — Uruchamia interaktywny shell LLM z przekazanymi danymi diagnostycznymi. [source](https://github.com/wronai/fixfedora/blob/main/fixos/llm_shell.py#L101)

### `fixos.orchestrator.executor` [source](https://github.com/wronai/fixfedora/blob/main/fixos/orchestrator/executor.py)

CommandExecutor – bezpieczne wykonywanie komend systemowych.

**`CommandExecutor`** [source](https://github.com/wronai/fixfedora/blob/main/fixos/orchestrator/executor.py#L85)
: Bezpieczny executor komend z:

| Method | Args | Returns | CC |
|--------|------|---------|----|
| `is_dangerous` | `command` | `—` | 3 |
| `needs_sudo` | `command` | `—` | 5 |
| `add_sudo` | `command` | `—` | 2 |
| `check_idempotent` | `command` | `—` | 4 |
| `execute_sync` | `command, timeout, add_sudo` | `—` | 11 |
| `execute` | `command, timeout, add_sudo` | `—` | 9 |

**`CommandTimeoutError`** (Exception) [source](https://github.com/wronai/fixfedora/blob/main/fixos/orchestrator/executor.py#L23)

**`DangerousCommandError`** (Exception) [source](https://github.com/wronai/fixfedora/blob/main/fixos/orchestrator/executor.py#L16)

**`ExecutionResult`** [source](https://github.com/wronai/fixfedora/blob/main/fixos/orchestrator/executor.py#L31)

| Method | Args | Returns | CC |
|--------|------|---------|----|
| `to_context` | `` | `—` | 1 |

### `fixos.orchestrator.graph` [source](https://github.com/wronai/fixfedora/blob/main/fixos/orchestrator/graph.py)

Problem Graph – model danych dla kaskadowych problemów systemowych.

**`Problem`** [source](https://github.com/wronai/fixfedora/blob/main/fixos/orchestrator/graph.py#L19)

| Method | Args | Returns | CC |
|--------|------|---------|----|
| `is_actionable` | `` | `—` | 2 |
| `to_summary` | `` | `—` | 1 |

**`ProblemGraph`** [source](https://github.com/wronai/fixfedora/blob/main/fixos/orchestrator/graph.py#L46)
: DAG problemów systemowych z topological sort do wyznaczania kolejności napraw.

| Method | Args | Returns | CC |
|--------|------|---------|----|
| `add` | `problem` | `—` | 1 |
| `get` | `problem_id` | `—` | 1 |
| `next_actionable` | `` | `—` | 6 |
| `all_done` | `` | `—` | 2 |
| `pending_count` | `` | `—` | 3 |
| `summary` | `` | `—` | 2 |
| `render_tree` | `` | `—` | 7 |

### `fixos.orchestrator.orchestrator` [source](https://github.com/wronai/fixfedora/blob/main/fixos/orchestrator/orchestrator.py)

FixOrchestrator – główna pętla egzekucji napraw.

**`FixOrchestrator`** [source](https://github.com/wronai/fixfedora/blob/main/fixos/orchestrator/orchestrator.py#L83)
: Orkiestrator napraw systemowych.

| Method | Args | Returns | CC |
|--------|------|---------|----|
| `load_from_diagnostics` | `diagnostics` | `—` | 5 |
| `load_from_dict` | `problems_data` | `—` | 3 |
| `run_sync` | `confirm_fn, progress_fn` | `—` | 17 |
| `run_async` | `confirm_fn, progress_fn` | `—` | 1 |

### `fixos.platform_utils` [source](https://github.com/wronai/fixfedora/blob/main/fixos/platform_utils.py)

Cross-platform utilities for fixos.

- `cancel_signal_timeout()` — Cancels the timeout signal (POSIX only). [source](https://github.com/wronai/fixfedora/blob/main/fixos/platform_utils.py#L180)
- `elevate_cmd(cmd)` — Adds sudo (Linux/Mac) or wraps in PowerShell -Verb RunAs (Windows). [source](https://github.com/wronai/fixfedora/blob/main/fixos/platform_utils.py#L61)
- `get_os_info()` — Returns basic OS information. [source](https://github.com/wronai/fixfedora/blob/main/fixos/platform_utils.py#L22)
- `get_package_manager()` — Detects the system package manager. [source](https://github.com/wronai/fixfedora/blob/main/fixos/platform_utils.py#L123)
- `install_package_cmd(package)` — Returns the install command for the detected package manager. [source](https://github.com/wronai/fixfedora/blob/main/fixos/platform_utils.py#L141)
- `is_dangerous(cmd)` — Returns reason string if command is dangerous, None if safe. [source](https://github.com/wronai/fixfedora/blob/main/fixos/platform_utils.py#L72)
- `needs_elevation(cmd)` — Returns True if command likely needs admin/sudo. [source](https://github.com/wronai/fixfedora/blob/main/fixos/platform_utils.py#L41)
- `run_command(cmd, timeout, shell)` — Runs a command cross-platform. [source](https://github.com/wronai/fixfedora/blob/main/fixos/platform_utils.py#L91)
- `setup_signal_timeout(seconds, handler)` — Sets up a timeout signal. Returns True if supported (POSIX only). [source](https://github.com/wronai/fixfedora/blob/main/fixos/platform_utils.py#L167)

### `fixos.providers.llm` [source](https://github.com/wronai/fixfedora/blob/main/fixos/providers/llm.py)

Ujednolicony klient LLM obsługujący wiele providerów przez OpenAI-compatible API.

**`LLMClient`** [source](https://github.com/wronai/fixfedora/blob/main/fixos/providers/llm.py#L25)
: Wrapper nad openai.OpenAI kompatybilny z wieloma providerami.

| Method | Args | Returns | CC |
|--------|------|---------|----|
| `chat` | `messages` | `—` | 15 |
| `chat_stream` | `messages` | `—` | 5 |
| `ping` | `` | `—` | 2 |

**`LLMError`** (Exception) [source](https://github.com/wronai/fixfedora/blob/main/fixos/providers/llm.py#L20)
: Błąd komunikacji z LLM.

### `fixos.providers.llm_analyzer` [source](https://github.com/wronai/fixfedora/blob/main/fixos/providers/llm_analyzer.py)

LLM Analyzer for fixOS - Fallback analysis when heuristics aren't sufficient

**`LLMAnalysis`** [source](https://github.com/wronai/fixfedora/blob/main/fixos/providers/llm_analyzer.py#L12)
: Result of LLM analysis

**`LLMAnalyzer`** [source](https://github.com/wronai/fixfedora/blob/main/fixos/providers/llm_analyzer.py#L20)
: Uses LLM to analyze disk issues when heuristics aren't sufficient

| Method | Args | Returns | CC |
|--------|------|---------|----|
| `analyze_disk_issues` | `disk_data` | `—` | 5 |
| `analyze_failed_action` | `action, error` | `—` | 4 |
| `analyze_complex_pattern` | `pattern_data` | `—` | 5 |
| `enhance_heuristics_with_llm` | `heuristic_suggestions, disk_data` | `—` | 13 |

- `main()` — Test the LLM analyzer [source](https://github.com/wronai/fixfedora/blob/main/fixos/providers/llm_analyzer.py#L326)

### `fixos.system_checks` [source](https://github.com/wronai/fixfedora/blob/main/fixos/system_checks.py)

Moduł zbierający dane diagnostyczne z systemu system.

- `get_cpu_info()` — Metryki CPU. [source](https://github.com/wronai/fixfedora/blob/main/fixos/system_checks.py#L32)
- `get_disk_info()` — Metryki dysków dla wszystkich partycji. [source](https://github.com/wronai/fixfedora/blob/main/fixos/system_checks.py#L60)
- `get_fedora_specific()` — Komendy specyficzne dla system: dnf, journalctl, systemctl. [source](https://github.com/wronai/fixfedora/blob/main/fixos/system_checks.py#L107)
- `get_full_diagnostics()` — Zbiera kompletne dane diagnostyczne systemu system. [source](https://github.com/wronai/fixfedora/blob/main/fixos/system_checks.py#L128)
- `get_memory_info()` — Metryki RAM i SWAP. [source](https://github.com/wronai/fixfedora/blob/main/fixos/system_checks.py#L45)
- `get_network_info()` — Statystyki sieciowe (bez wrażliwych danych - anonimizacja jest osobno). [source](https://github.com/wronai/fixfedora/blob/main/fixos/system_checks.py#L79)
- `get_top_processes(n)` — Lista TOP N procesów według zużycia CPU. [source](https://github.com/wronai/fixfedora/blob/main/fixos/system_checks.py#L95)
- `run_cmd(cmd, timeout)` — Uruchamia komendę shell i zwraca output. Bezpieczny fallback przy błędzie. [source](https://github.com/wronai/fixfedora/blob/main/fixos/system_checks.py#L12)

### `fixos.utils.anonymizer` [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/anonymizer.py)

Anonimizacja wrażliwych danych systemowych z podglądem dla użytkownika.

**`AnonymizationReport`** [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/anonymizer.py#L16)
: Raport anonimizacji – co zostało zmaskowane.

| Method | Args | Returns | CC |
|--------|------|---------|----|
| `add` | `category, count` | `—` | 1 |
| `summary` | `` | `—` | 3 |

- `anonymize(data_str)` — Anonimizuje wrażliwe dane. [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/anonymizer.py#L51)
- `display_anonymized_preview(data_str, report, max_lines)` — Wyświetla użytkownikowi zanonimizowane dane przed wysłaniem do LLM. [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/anonymizer.py#L139)

### `fixos.utils.terminal` [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/terminal.py)

Terminal rendering utilities – shared between hitl, orchestrator, cli.

- `colorize(line)` — Return line unchanged – rich handles markup in render_md(). [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/terminal.py#L55)
- `print_cmd_block(cmd, comment, dry_run)` — Print a framed command preview panel. [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/terminal.py#L167)
- `print_problem_header(problem_id, description, severity, status, attempts, max_attempts)` — Print a colored problem header panel. [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/terminal.py#L231)
- `print_stderr_box(stderr, max_lines)` — Print stderr in a rich Panel. [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/terminal.py#L196)
- `print_stdout_box(stdout, max_lines)` — Print stdout in a rich Panel. [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/terminal.py#L183)
- `render_md(text)` — Print LLM markdown reply to terminal via rich. [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/terminal.py#L62)
- `render_tree_colored(nodes, execution_order)` — Render a ProblemGraph as a rich-markup string. [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/terminal.py#L258)

### `fixos.utils.web_search` [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/web_search.py)

Zewnętrzne źródła wiedzy – fallback gdy LLM nie zna rozwiązania.

**`SearchResult`** [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/web_search.py#L19)

- `format_results_for_llm(results)` — Formatuje wyniki wyszukiwania do wklejenia w prompt LLM. [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/web_search.py#L245)
- `search_all(query, serpapi_key, max_per_source)` — Przeszukuje wszystkie dostępne źródła wiedzy. [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/web_search.py#L206)
- `search_arch_wiki(query, max_results)` — Arch Wiki – doskonałe źródło dla problemów Linux (nie tylko Arch). [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/web_search.py#L87)
- `search_ask_fedora(query, max_results)` — Szuka w Linux forums przez Discourse API. [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/web_search.py#L65)
- `search_ddg(query, max_results)` — DuckDuckGo Instant Answer API (bez klucza, ograniczone). [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/web_search.py#L174)
- `search_fedora_bugzilla(query, max_results)` — Szuka w Linux Bugzilla przez REST API. [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/web_search.py#L39)
- `search_github_issues(query, max_results)` — GitHub Issues – linuxhardware, ALSA, PipeWire, PulseAudio repos. [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/web_search.py#L115)
- `search_serpapi(query, api_key, max_results)` — SerpAPI – Google/Bing search (wymaga klucza API). [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/web_search.py#L150)
