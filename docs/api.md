# fixOS — API Reference

> 75 modules | 379 functions | 66 classes

## Contents

- [Core](#core) (1 modules)
- [fixos](#fixos) (69 modules)

## Core

### `fixos` [source](https://github.com/wronai/fixfedora/blob/main/fixos/__init__.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `AgentReport` | 1 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/agent/autonomous_session.py#L74) |
| `AutonomousSession` | 1 | Self-directed autonomous diagnostic and repair session. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/agent/autonomous_session.py#L97) |
| `FixAction` | 0 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/agent/autonomous_session.py#L65) |
| `CmdResult` | 0 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/agent/hitl_session.py#L60) |
| `HITLSession` | 3 | Interactive Human-in-the-Loop diagnostic and repair session. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/agent/hitl_session.py#L71) |
| `NaturalLanguageGroup` | 1 | Click group that routes unknown commands to 'ask' command. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/shared.py#L54) |
| `FixOsConfig` | 3 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/config.py#L156) |
| `DiskAnalyzer` | 6 | Analyzes disk usage and provides cleanup suggestions | [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/disk_analyzer.py#L15) |
| `FlatpakAnalyzer` | 2 | Advanced analyzer for Flatpak cleanup decisions | [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/flatpak_analyzer.py#L62) |
| `FlatpakItemInfo` | 1 | Detailed info about a Flatpak item (app, runtime, or data) | [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/flatpak_analyzer.py#L28) |
| `FlatpakItemType` | 0 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/flatpak_analyzer.py#L21) |
| `ServiceCleaner` | 6 | Plans and executes cleanup of service data. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/service_cleanup.py#L10) |
| `ServiceDetailsProvider` | 1 | Provides detailed information about service data. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/service_details.py#L18) |
| `ServiceDataInfo` | 0 | Information about service data. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/service_scanner.py#L75) |
| `ServiceDataScanner` | 4 | Scans for large service data directories and allows cleanup. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/service_scanner.py#L92) |
| `ServiceType` | 0 | Service types that can be scanned and cleaned. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/service_scanner.py#L21) |
| `SystemDetector` | 1 | Detects system parameters. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/features/__init__.py#L50) |
| `SystemInfo` | 0 | Complete system information snapshot. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/features/__init__.py#L16) |
| `AuditResult` | 3 | Result of feature audit - what's installed, what's missing. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/features/auditor.py#L15) |
| `FeatureAuditor` | 1 | Compares installed packages with profile requirements. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/features/auditor.py#L52) |
| `PackageCatalog` | 4 | Manages the package database. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/features/catalog.py#L48) |
| `PackageCategory` | 0 | A category of packages (e.g., core_utils, dev_tools). | [source](https://github.com/wronai/fixfedora/blob/main/fixos/features/catalog.py#L40) |
| `PackageInfo` | 2 | Information about a single package. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/features/catalog.py#L12) |
| `FeatureInstaller` | 2 | Safely installs packages using native package manager or other backends. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/features/installer.py#L14) |
| `UserProfile` | 4 | A user profile defining what packages/features they want. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/features/profiles.py#L14) |
| `FeatureRenderer` | 3 | Renders audit results for terminal display. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/features/renderer.py#L18) |
| `CleanupAction` | 0 | Represents a cleanup action | [source](https://github.com/wronai/fixfedora/blob/main/fixos/interactive/cleanup_planner.py#L32) |
| `CleanupPlanner` | 4 | Interactive cleanup planning and grouping system | [source](https://github.com/wronai/fixfedora/blob/main/fixos/interactive/cleanup_planner.py#L52) |
| `CleanupType` | 0 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/interactive/cleanup_planner.py#L20) |
| `Priority` | 0 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/interactive/cleanup_planner.py#L13) |
| `CommandExecutor` | 6 | Bezpieczny executor komend z: | [source](https://github.com/wronai/fixfedora/blob/main/fixos/orchestrator/executor.py#L85) |
| `CommandTimeoutError` | 0 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/orchestrator/executor.py#L23) |
| `DangerousCommandError` | 0 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/orchestrator/executor.py#L16) |
| `ExecutionResult` | 2 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/orchestrator/executor.py#L31) |
| `Problem` | 2 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/orchestrator/graph.py#L19) |
| `ProblemGraph` | 7 | DAG problemów systemowych z topological sort do wyznaczania kolejności napraw. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/orchestrator/graph.py#L46) |
| `FixOrchestrator` | 4 | Orkiestrator napraw systemowych. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/orchestrator/orchestrator.py#L83) |
| `RollbackEntry` | 0 | Single recorded operation with its rollback command. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/orchestrator/rollback.py#L20) |
| `RollbackSession` | 5 | A session of recorded operations that can be rolled back. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/orchestrator/rollback.py#L32) |
| `DiagnosticPlugin` | 3 | Bazowa klasa dla pluginów diagnostycznych fixOS. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/plugins/base.py#L64) |
| `DiagnosticResult` | 1 | Result of a diagnostic plugin run. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/plugins/base.py#L36) |
| `Finding` | 0 | Single finding from a diagnostic plugin. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/plugins/base.py#L25) |
| `Severity` | 0 | Severity level for diagnostic findings. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/plugins/base.py#L16) |
| `Plugin` | 1 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/plugins/builtin/audio.py#L9) |
| `Plugin` | 1 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/plugins/builtin/disk.py#L9) |
| `Plugin` | 1 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/plugins/builtin/hardware.py#L9) |
| `Plugin` | 1 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/plugins/builtin/resources.py#L9) |
| `Plugin` | 1 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/plugins/builtin/security.py#L9) |
| `Plugin` | 1 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/plugins/builtin/thumbnails.py#L9) |
| `PluginRegistry` | 6 | Registry for diagnostic plugins with autodiscovery. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/plugins/registry.py#L21) |
| `Profile` | 3 | Profil diagnostyczny z zestawem modułów i progów. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/profiles/__init__.py#L21) |
| `LLMClient` | 5 | Wrapper nad openai.OpenAI kompatybilny z wieloma providerami. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/providers/llm.py#L26) |
| `LLMError` | 0 | Błąd komunikacji z LLM. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/providers/llm.py#L21) |
| `LLMAnalysis` | 0 | Result of LLM analysis | [source](https://github.com/wronai/fixfedora/blob/main/fixos/providers/llm_analyzer.py#L12) |
| `LLMAnalyzer` | 4 | Uses LLM to analyze disk issues when heuristics aren't sufficient | [source](https://github.com/wronai/fixfedora/blob/main/fixos/providers/llm_analyzer.py#L20) |
| `CommandValidation` | 0 | Wynik walidacji komendy przez LLM. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/providers/schemas.py#L66) |
| `FixSuggestion` | 0 | Pojedyncza sugestia naprawy od LLM. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/providers/schemas.py#L21) |
| `LLMDiagnosticResponse` | 0 | Strukturalna odpowiedź LLM na dane diagnostyczne. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/providers/schemas.py#L41) |
| `NLPIntent` | 0 | Rozpoznana intencja z polecenia NLP. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/providers/schemas.py#L58) |
| `RiskLevel` | 0 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/providers/schemas.py#L15) |
| `AnonymizationReport` | 2 | Raport anonimizacji – co zostało zmaskowane. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/anonymizer.py#L16) |
| `SessionTimeout` | 0 | Wyjątek rzucany po przekroczeniu limitu czasu sesji. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/timeout.py#L10) |
| `SearchResult` | 0 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/web_search.py#L19) |
| `WatchDaemon` | 2 | Daemon wykonujący cykliczną diagnostykę z powiadomieniami. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/watch.py#L22) |

**`HITLSession` methods:**

- `remaining()` — Get remaining session time in seconds.
- `fmt_time(s)` — Format seconds as HH:MM:SS.
- `run()` — Run the HITL session.

**`FixOsConfig` methods:**

- `load(cls)` — Tworzy konfigurację z połączonych źródeł.
- `validate()` — Zwraca listę błędów walidacji (pusta = OK).
- `summary()` — Krótkie podsumowanie konfiguracji (bez klucza API).

**`DiskAnalyzer` methods:**

- `analyze_disk_usage(path)` — Comprehensive disk usage analysis
- `get_large_files(path, min_size_mb, max_files)` — Find large files
- `get_cache_dirs(path, max_dirs)` — Find cache directories
- `get_log_dirs(path, max_dirs)` — Find log directories
- `get_temp_dirs(path, max_dirs)` — Find temporary directories
- `suggest_cleanup_actions(path)` — Generate cleanup suggestions using heuristics

**`FlatpakAnalyzer` methods:**

- `analyze()` — Run full Flatpak analysis
- `get_cleanup_summary()` — Get human-readable summary of cleanup opportunities

**`ServiceCleaner` methods:**

- `get_cleanup_plan(selected_services)` — Generate cleanup plan for services.
- `cleanup_service(service_type, dry_run)` — Execute cleanup for a specific service.
- `is_safe_cleanup(service_type)` — Determine if cleanup is generally safe (cache-only, not user data).
- `get_service_description(service_type)` — Get description for service type.
- `get_cleanup_command(service_type, path)` — Get cleanup command for service.
- `get_preview_command(service_type, path)` — Get preview command for service.

**`ServiceDataScanner` methods:**

- `scan_all_services()` — Scan all known services for data above threshold.
- `scan_service(service_type)` — Scan specific service type for data.
- `get_cleanup_plan(selected_services)` — Generate cleanup plan for services.
- `cleanup_service(service_type, dry_run)` — Execute cleanup for a specific service.

**`PackageCatalog` methods:**

- `load(cls, data_dir)` — Load package catalog from YAML files.
- `get_package(pkg_id)` — Get package by ID.
- `get_packages_by_category(category)` — Get all packages in a category.
- `list_categories()` — List all category IDs.

**`PackageInfo` methods:**

- `get_distro_name(distro)` — Get package name for specific distro.
- `is_available_on(distro)` — Check if package is available on given distro.

**`FeatureInstaller` methods:**

- `install(packages)` — Install a list of packages.
- `get_rollback_commands(installed_packages)` — Generate rollback commands for installed packages.

**`UserProfile` methods:**

- `load(cls, profile_name, data_dir)` — Load a profile from YAML file.
- `list_available(cls, data_dir)` — List available profile names.
- `resolve_packages(catalog, system_info)` — Resolve all packages for this profile based on system.
- `to_dict()` — Convert to dictionary.

**`FeatureRenderer` methods:**

- `render_audit(result)` — Render complete audit results.
- `render_package_list(packages, title)` — Render a list of packages.
- `render_system_info(system)` — Render system information.

**`CleanupPlanner` methods:**

- `group_by_category(suggestions)` — Group cleanup suggestions by category
- `prioritize_actions(grouped_actions)` — Create prioritized list of all actions
- `create_cleanup_plan(suggestions)` — Create comprehensive cleanup plan
- `interactive_selection(plan)` — Interactive selection process (simulated for now)

**`CommandExecutor` methods:**

- `is_dangerous(command)` — Sprawdza czy komenda jest potencjalnie destruktywna.
- `needs_sudo(command)`
- `add_sudo(command)`
- `check_idempotent(command)` — Zwraca komendę sprawdzającą stan (jeśli znana), None jeśli nie dotyczy.
- `execute_sync(command, timeout, add_sudo, check_idempotent)` — Synchroniczne wykonanie komendy.
- `execute(command, timeout, add_sudo)` — Asynchroniczne wykonanie komendy.

**`Problem` methods:**

- `is_actionable()`
- `to_summary()`

**`ProblemGraph` methods:**

- `add(problem)`
- `get(problem_id)`
- `next_actionable()` — Zwraca pierwszy problem bez nierozwiązanych zależności.
- `all_done()`
- `pending_count()`
- `summary()`
- `render_tree()` — Renderuje drzewo problemów jako tekst.

**`FixOrchestrator` methods:**

- `load_from_diagnostics(diagnostics)` — Parsuje dane diagnostyczne przez LLM i buduje graf problemów.
- `load_from_dict(problems_data)` — Ładuje problemy bezpośrednio z listy dict (bez LLM).
- `run_sync(confirm_fn, progress_fn)` — Synchroniczna pętla napraw (dla trybu HITL).
- `run_async(confirm_fn, progress_fn)` — Asynchroniczna wersja run_sync.

**`RollbackSession` methods:**

- `record(command, rollback_cmd, stdout, stderr, ...)` — Zapisz wykonaną operację.
- `get_rollback_commands()` — Zwraca listę (komenda, rollback) w odwróconej kolejności.
- `rollback_last(n, dry_run)` — Cofnij ostatnich n operacji.
- `load(cls, session_id)` — Załaduj sesję z pliku.
- `list_sessions(cls, limit)` — Lista ostatnich sesji rollback.

**`DiagnosticPlugin` methods:**

- `diagnose()` — Wykonaj diagnostykę i zwróć wynik.
- `can_run()` — Czy plugin może działać na aktualnej platformie?
- `get_metadata()`

**`PluginRegistry` methods:**

- `discover()` — Odkrywanie pluginów przez builtin + entry_points.
- `register(plugin)` — Ręczna rejestracja pluginu.
- `list_plugins(runnable_only)` — Lista zarejestrowanych pluginów.
- `get_plugin(name)` — Pobierz plugin po nazwie.
- `run(modules, progress_callback)` — Uruchom diagnostykę dla wybranych (lub wszystkich) modułów.

**`Profile` methods:**

- `load(cls, name)` — Załaduj profil — najpierw user, potem builtin.
- `list_available(cls)` — Lista dostępnych profili (builtin + user).
- `to_dict()`

**`LLMClient` methods:**

- `chat(messages)` — Wysyła wiadomości do LLM i zwraca odpowiedź jako string.
- `chat_stream(messages)` — Generator streamujący tokeny odpowiedzi.
- `chat_structured(messages, response_model)` — Wywołanie LLM z wymuszonym schematem JSON (Pydantic model).
- `ping()` — Sprawdza czy API odpowiada (krótki test).

**`LLMAnalyzer` methods:**

- `analyze_disk_issues(disk_data)` — Use LLM to analyze disk issues when heuristics are insufficient
- `analyze_failed_action(action, error)` — Analyze failed cleanup action and suggest alternatives
- `analyze_complex_pattern(pattern_data)` — Analyze complex disk usage patterns that heuristics can't categorize
- `enhance_heuristics_with_llm(heuristic_suggestions, disk_data)` — Enhance heuristic suggestions with LLM insights

**`AnonymizationReport` methods:**

- `add(category, count)`
- `summary()`

**`WatchDaemon` methods:**

- `run()` — Główna pętla monitorowania.
- `stop()` — Zatrzymaj daemon.

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `run_autonomous_session` | `run_autonomous_session(diagnostics, config, show_data, max_fixes)` | 1 | Uruchamia autonomiczny tryb agenta. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/agent/autonomous.py#L31) |
| `run_autonomous_session` | `run_autonomous_session(diagnostics, config, show_data, max_fixes)` | 1 | Run autonomous session (backward compatible wrapper). | [source](https://github.com/wronai/fixfedora/blob/main/fixos/agent/autonomous_session.py#L416) |
| `run_hitl_session` | `run_hitl_session(diagnostics, config, show_data)` | 1 | Run interactive HITL session with full transparency. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/agent/hitl.py#L24) |
| `run_hitl_session` | `run_hitl_session(diagnostics, config, show_data)` | 1 | Run interactive HITL session (backward compatible wrapper). | [source](https://github.com/wronai/fixfedora/blob/main/fixos/agent/hitl_session.py#L498) |
| `anonymize` | `anonymize(data_str)` | 5 | Anonimizuje wrażliwe dane w stringu. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/anonymizer.py#L30) |
| `get_sensitive_values` | `get_sensitive_values()` | 4 | Zbiera aktualne wrażliwe wartości systemowe do zamaskowania. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/anonymizer.py#L12) |
| `ask` | `ask(prompt, dry_run)` | 1 | Wykonaj polecenie w języku naturalnym. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/ask_cmd.py#L10) |
| `cleanup_services` | `cleanup_services(threshold, services, json_output, cleanup, ...)` | 15 ⚠️ | Skanuje i czyści dane usług przekraczające próg. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/cleanup_cmd.py#L24) |
| `config` | `config()` | 1 | Zarządzanie konfiguracją fixOS. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/config_cmd.py#L8) |
| `config_init` | `config_init(force)` | 3 | Zainicjalizuj plik konfiguracyjny .env. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/config_cmd.py#L40) |
| `config_set` | `config_set(key, value)` | 2 | Ustaw wartość konfiguracyjną w .env. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/config_cmd.py#L72) |
| `config_show` | `config_show()` | 4 | Pokaż aktualną konfigurację. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/config_cmd.py#L14) |
| `features` | `features()` | 1 | Zarządzanie pakietami komfortu systemu. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/features_cmd.py#L21) |
| `features_audit` | `features_audit(profile, json_output)` | 4 | Sprawdź brakujące pakiety dla profilu. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/features_cmd.py#L29) |
| `features_install` | `features_install(profile, dry_run, yes, category)` | 15 ⚠️ | Zainstaluj brakujące pakiety dla profilu. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/features_cmd.py#L58) |
| `features_profiles` | `features_profiles()` | 3 | Lista dostępnych profili. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/features_cmd.py#L112) |
| `features_system` | `features_system()` | 1 | Pokaż wykryty system. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/features_cmd.py#L131) |
| `execute_cleanup_actions` | `execute_cleanup_actions(actions, cfg, llm_fallback)` | 6 | Execute cleanup actions with safety checks | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/fix_cmd.py#L219) |
| `fix` | `fix(provider, token, model, no_banner, ...)` | 18 ⚠️ | Przeprowadza pełną diagnostykę i uruchamia sesję naprawczą z LLM. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/fix_cmd.py#L28) |
| `handle_disk_cleanup_mode` | `handle_disk_cleanup_mode(disk_analysis, cfg, dry_run, interactive, ...)` | 13 ⚠️ | Handle disk cleanup mode with interactive planning | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/fix_cmd.py#L149) |
| `try_llm_fallback_for_failures` | `try_llm_fallback_for_failures(failed_actions, cfg)` | 3 | Try to fix failed actions using LLM | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/fix_cmd.py#L260) |
| `history` | `history(limit, json_output)` | 5 | Historia napraw fixOS. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/history_cmd.py#L10) |
| `cli` | `cli(ctx, dry_run, version)` | 3 | fixos – AI-powered diagnostyka i naprawa Linux, Windows, macOS. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/main.py#L13) |
| `main` | `main()` | 1 | Entry point for fixOS CLI. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/main.py#L120) |
| `orchestrate` | `orchestrate(provider, token, model, no_banner, ...)` | 13 ⚠️ | Zaawansowana orkiestracja napraw z grafem problemów. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/orchestrate_cmd.py#L23) |
| `profile` | `profile()` | 1 | Zarządzanie profilami diagnostycznymi. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/profile_cmd.py#L8) |
| `profile_list` | `profile_list()` | 4 | Pokaż dostępne profile diagnostyczne. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/profile_cmd.py#L14) |
| `profile_show` | `profile_show(name)` | 4 | Pokaż szczegóły profilu diagnostycznego. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/profile_cmd.py#L41) |
| `llm_providers` | `llm_providers(free)` | 6 | Lista dostępnych providerów LLM. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/provider_cmd.py#L109) |
| `providers` | `providers()` | 4 | Lista providerów LLM z oznaczeniem FREE/PAID. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/provider_cmd.py#L154) |
| `test_llm` | `test_llm(provider, token, model, no_banner)` | 9 | Test połączenia z LLM. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/provider_cmd.py#L192) |
| `quickfix` | `quickfix(dry_run, modules)` | 12 ⚠️ | Natychmiastowe naprawy bez API — baza znanych bugów. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/quickfix_cmd.py#L12) |
| `report` | `report(output_format, output, modules, profile)` | 16 ⚠️ | Eksport wyników diagnostyki do raportu HTML/Markdown/JSON. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/report_cmd.py#L14) |
| `rollback` | `rollback()` | 1 | Zarządzanie cofaniem operacji fixOS. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/rollback_cmd.py#L9) |
| `rollback_list` | `rollback_list(limit)` | 3 | Pokaż historię sesji naprawczych. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/rollback_cmd.py#L16) |
| `rollback_show` | `rollback_show(session_id)` | 5 | Pokaż szczegóły sesji rollback. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/rollback_cmd.py#L37) |
| `rollback_undo` | `rollback_undo(session_id, last, dry_run)` | 7 | Cofnij operacje z podanej sesji. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/rollback_cmd.py#L63) |
| `scan` | `scan(modules, output, show_raw, no_banner, ...)` | 12 ⚠️ | Przeprowadza diagnostykę systemu. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/scan_cmd.py#L18) |
| `add_common_options` | `add_common_options(fn)` | 2 | Decorator adding common LLM options to a Click command. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/shared.py#L26) |
| `add_shared_options` | `add_shared_options(func)` | 1 | Shared options for both scan and fix commands. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/shared.py#L33) |
| `token` | `token()` | 1 | Zarządzanie tokenem API. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/token_cmd.py#L10) |
| `token_clear` | `token_clear(env_file)` | 3 | Usuń token z pliku .env. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/token_cmd.py#L106) |
| `token_set` | `token_set(key, provider, env_file)` | 7 | Zapisz token API do pliku .env. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/token_cmd.py#L19) |
| `token_show` | `token_show()` | 2 | Pokaż obecny token (masked). | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/token_cmd.py#L90) |
| `watch` | `watch(interval, modules, alert_on, max_iterations)` | 2 | Monitorowanie systemu w tle z powiadomieniami. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/watch_cmd.py#L18) |
| `detect_provider_from_key` | `detect_provider_from_key(key)` | 3 | Wykrywa provider na podstawie prefiksu klucza API. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/config.py#L309) |
| `get_providers_list` | `get_providers_list()` | 3 | Zwraca listę providerów jako listę słowników. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/config.py#L410) |
| `interactive_provider_setup` | `interactive_provider_setup()` | 24 ⚠️ | Interaktywny wybór providera gdy brak konfiguracji. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/config.py#L317) |
| `main` | `main()` | 1 | Test the disk analyzer | [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/disk_analyzer.py#L411) |
| `analyze_flatpak_for_cleanup` | `analyze_flatpak_for_cleanup()` | 1 | Convenience function to run full Flatpak analysis | [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/flatpak_analyzer.py#L329) |
| `main` | `main()` | 1 | Test the service data scanner. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/service_scanner.py#L241) |
| `diagnose_audio` | `diagnose_audio()` | 1 | Diagnostyka dźwięku (ALSA/PipeWire/PulseAudio/SOF). | [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/system_checks.py#L49) |
| `diagnose_hardware` | `diagnose_hardware()` | 1 | Diagnostyka sprzętu laptopa/desktopa (ACPI, kamera, touchpad, DMI). | [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/system_checks.py#L165) |
| `diagnose_resources` | `diagnose_resources()` | 13 ⚠️ | Diagnostyka zasobów systemowych. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/system_checks.py#L384) |
| `diagnose_security` | `diagnose_security()` | 4 | Diagnostyka bezpieczeństwa systemu i sieci. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/system_checks.py#L303) |
| `diagnose_system` | `diagnose_system()` | 14 ⚠️ | System metrics – cross-platform: CPU, RAM, disks, processes. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/system_checks.py#L204) |
| `diagnose_thumbnails` | `diagnose_thumbnails()` | 1 | Diagnostyka podglądów plików (thumbnails) w system. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/system_checks.py#L106) |
| `get_full_diagnostics` | `get_full_diagnostics(modules, progress_callback)` | 7 | Zbiera diagnostykę z wybranych modułów. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/system_checks.py#L482) |
| `main` | `main()` | 1 | Test the cleanup planner | [source](https://github.com/wronai/fixfedora/blob/main/fixos/interactive/cleanup_planner.py#L385) |
| `execute_command` | `execute_command(cmd)` | 10 | Wykonuje komendę systemową z potwierdzeniem użytkownika. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/llm_shell.py#L66) |
| `format_time` | `format_time(seconds)` | 1 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/llm_shell.py#L58) |
| `run_llm_shell` | `run_llm_shell(diagnostics_data, token, model, timeout, ...)` | 15 ⚠️ | Uruchamia interaktywny shell LLM z przekazanymi danymi diagnostycznymi. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/llm_shell.py#L100) |
| `cancel_signal_timeout` | `cancel_signal_timeout()` | 2 | Cancels the timeout signal (POSIX only). | [source](https://github.com/wronai/fixfedora/blob/main/fixos/platform_utils.py#L180) |
| `elevate_cmd` | `elevate_cmd(cmd)` | 3 | Adds sudo (Linux/Mac) or wraps in PowerShell -Verb RunAs (Windows). | [source](https://github.com/wronai/fixfedora/blob/main/fixos/platform_utils.py#L61) |
| `get_os_info` | `get_os_info()` | 5 | Returns basic OS information. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/platform_utils.py#L22) |
| `get_package_manager` | `get_package_manager()` | 8 | Detects the system package manager. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/platform_utils.py#L123) |
| `install_package_cmd` | `install_package_cmd(package)` | 2 | Returns the install command for the detected package manager. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/platform_utils.py#L141) |
| `is_dangerous` | `is_dangerous(cmd)` | 3 | Returns reason string if command is dangerous, None if safe. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/platform_utils.py#L72) |
| `needs_elevation` | `needs_elevation(cmd)` | 5 | Returns True if command likely needs admin/sudo. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/platform_utils.py#L41) |
| `run_command` | `run_command(cmd, timeout, shell)` | 5 | Runs a command cross-platform. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/platform_utils.py#L91) |
| `setup_signal_timeout` | `setup_signal_timeout(seconds, handler)` | 2 | Sets up a timeout signal. Returns True if supported (POSIX only). | [source](https://github.com/wronai/fixfedora/blob/main/fixos/platform_utils.py#L167) |
| `main` | `main()` | 1 | Test the LLM analyzer | [source](https://github.com/wronai/fixfedora/blob/main/fixos/providers/llm_analyzer.py#L326) |
| `get_cpu_info` | `get_cpu_info()` | 2 | Metryki CPU. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/system_checks.py#L32) |
| `get_disk_info` | `get_disk_info()` | 3 | Metryki dysków dla wszystkich partycji. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/system_checks.py#L60) |
| `get_fedora_specific` | `get_fedora_specific()` | 1 | Komendy specyficzne dla system: dnf, journalctl, systemctl. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/system_checks.py#L107) |
| `get_full_diagnostics` | `get_full_diagnostics()` | 1 | Zbiera kompletne dane diagnostyczne systemu system. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/system_checks.py#L128) |
| `get_memory_info` | `get_memory_info()` | 1 | Metryki RAM i SWAP. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/system_checks.py#L45) |
| `get_network_info` | `get_network_info()` | 4 | Statystyki sieciowe (bez wrażliwych danych - anonimizacja jest osobno). | [source](https://github.com/wronai/fixfedora/blob/main/fixos/system_checks.py#L79) |
| `get_top_processes` | `get_top_processes(n)` | 3 | Lista TOP N procesów według zużycia CPU. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/system_checks.py#L95) |
| `run_cmd` | `run_cmd(cmd, timeout)` | 6 | Uruchamia komendę shell i zwraca output. Bezpieczny fallback przy błędzie. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/system_checks.py#L12) |
| `anonymize` | `anonymize(data_str)` | 15 ⚠️ | Anonimizuje wrażliwe dane. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/anonymizer.py#L51) |
| `display_anonymized_preview` | `display_anonymized_preview(data_str, report, max_lines)` | 5 | Wyświetla użytkownikowi zanonimizowane dane przed wysłaniem do LLM. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/anonymizer.py#L139) |
| `colorize` | `colorize(line)` | 1 | Return line unchanged – rich handles markup in render_md(). | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/terminal.py#L55) |
| `print_cmd_block` | `print_cmd_block(cmd, comment, dry_run)` | 4 | Print a framed command preview panel. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/terminal.py#L167) |
| `print_problem_header` | `print_problem_header(problem_id, description, severity, status, ...)` | 3 | Print a colored problem header panel. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/terminal.py#L231) |
| `print_stderr_box` | `print_stderr_box(stderr, max_lines)` | 2 | Print stderr in a rich Panel. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/terminal.py#L196) |
| `print_stdout_box` | `print_stdout_box(stdout, max_lines)` | 2 | Print stdout in a rich Panel. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/terminal.py#L183) |
| `render_md` | `render_md(text)` | 16 ⚠️ | Print LLM markdown reply to terminal via rich. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/terminal.py#L62) |
| `render_tree_colored` | `render_tree_colored(nodes, execution_order)` | 8 | Render a ProblemGraph as a rich-markup string. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/terminal.py#L258) |
| `timeout_handler` | `timeout_handler(signum, frame)` | 1 | Signal handler dla SIGALRM — rzuca SessionTimeout. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/timeout.py#L15) |
| `format_results_for_llm` | `format_results_for_llm(results)` | 3 | Formatuje wyniki wyszukiwania do wklejenia w prompt LLM. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/web_search.py#L245) |
| `search_all` | `search_all(query, serpapi_key, max_per_source)` | 5 | Przeszukuje wszystkie dostępne źródła wiedzy. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/web_search.py#L206) |
| `search_arch_wiki` | `search_arch_wiki(query, max_results)` | 9 | Arch Wiki – doskonałe źródło dla problemów Linux (nie tylko Arch). | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/web_search.py#L87) |
| `search_ask_fedora` | `search_ask_fedora(query, max_results)` | 4 | Szuka w Linux forums przez Discourse API. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/web_search.py#L65) |
| `search_ddg` | `search_ddg(query, max_results)` | 8 | DuckDuckGo Instant Answer API (bez klucza, ograniczone). | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/web_search.py#L174) |
| `search_fedora_bugzilla` | `search_fedora_bugzilla(query, max_results)` | 4 | Szuka w Linux Bugzilla przez REST API. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/web_search.py#L39) |
| `search_github_issues` | `search_github_issues(query, max_results)` | 4 | GitHub Issues – linuxhardware, ALSA, PipeWire, PulseAudio repos. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/web_search.py#L115) |
| `search_serpapi` | `search_serpapi(query, api_key, max_results)` | 5 | SerpAPI – Google/Bing search (wymaga klucza API). | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/web_search.py#L150) |

## fixos

### `fixos.agent` [source](https://github.com/wronai/fixfedora/blob/main/fixos/agent/__init__.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `AgentReport` | 1 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/agent/autonomous_session.py#L74) |
| `AutonomousSession` | 1 | Self-directed autonomous diagnostic and repair session. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/agent/autonomous_session.py#L97) |
| `FixAction` | 0 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/agent/autonomous_session.py#L65) |
| `CmdResult` | 0 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/agent/hitl_session.py#L60) |
| `HITLSession` | 3 | Interactive Human-in-the-Loop diagnostic and repair session. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/agent/hitl_session.py#L71) |

**`HITLSession` methods:**

- `remaining()` — Get remaining session time in seconds.
- `fmt_time(s)` — Format seconds as HH:MM:SS.
- `run()` — Run the HITL session.

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `run_autonomous_session` | `run_autonomous_session(diagnostics, config, show_data, max_fixes)` | 1 | Uruchamia autonomiczny tryb agenta. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/agent/autonomous.py#L31) |
| `run_autonomous_session` | `run_autonomous_session(diagnostics, config, show_data, max_fixes)` | 1 | Run autonomous session (backward compatible wrapper). | [source](https://github.com/wronai/fixfedora/blob/main/fixos/agent/autonomous_session.py#L416) |
| `run_hitl_session` | `run_hitl_session(diagnostics, config, show_data)` | 1 | Run interactive HITL session with full transparency. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/agent/hitl.py#L24) |
| `run_hitl_session` | `run_hitl_session(diagnostics, config, show_data)` | 1 | Run interactive HITL session (backward compatible wrapper). | [source](https://github.com/wronai/fixfedora/blob/main/fixos/agent/hitl_session.py#L498) |

### `fixos.agent.autonomous` [source](https://github.com/wronai/fixfedora/blob/main/fixos/agent/autonomous.py)

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `run_autonomous_session` | `run_autonomous_session(diagnostics, config, show_data, max_fixes)` | 1 | Uruchamia autonomiczny tryb agenta. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/agent/autonomous.py#L31) |

### `fixos.agent.autonomous_session` [source](https://github.com/wronai/fixfedora/blob/main/fixos/agent/autonomous_session.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `AgentReport` | 1 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/agent/autonomous_session.py#L74) |
| `AutonomousSession` | 1 | Self-directed autonomous diagnostic and repair session. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/agent/autonomous_session.py#L97) |
| `FixAction` | 0 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/agent/autonomous_session.py#L65) |

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `run_autonomous_session` | `run_autonomous_session(diagnostics, config, show_data, max_fixes)` | 1 | Run autonomous session (backward compatible wrapper). | [source](https://github.com/wronai/fixfedora/blob/main/fixos/agent/autonomous_session.py#L416) |

### `fixos.agent.hitl` [source](https://github.com/wronai/fixfedora/blob/main/fixos/agent/hitl.py)

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `run_hitl_session` | `run_hitl_session(diagnostics, config, show_data)` | 1 | Run interactive HITL session with full transparency. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/agent/hitl.py#L24) |

### `fixos.agent.hitl_session` [source](https://github.com/wronai/fixfedora/blob/main/fixos/agent/hitl_session.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `CmdResult` | 0 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/agent/hitl_session.py#L60) |
| `HITLSession` | 3 | Interactive Human-in-the-Loop diagnostic and repair session. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/agent/hitl_session.py#L71) |

**`HITLSession` methods:**

- `remaining()` — Get remaining session time in seconds.
- `fmt_time(s)` — Format seconds as HH:MM:SS.
- `run()` — Run the HITL session.

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `run_hitl_session` | `run_hitl_session(diagnostics, config, show_data)` | 1 | Run interactive HITL session (backward compatible wrapper). | [source](https://github.com/wronai/fixfedora/blob/main/fixos/agent/hitl_session.py#L498) |

### `fixos.anonymizer` [source](https://github.com/wronai/fixfedora/blob/main/fixos/anonymizer.py)

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `anonymize` | `anonymize(data_str)` | 5 | Anonimizuje wrażliwe dane w stringu. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/anonymizer.py#L30) |
| `get_sensitive_values` | `get_sensitive_values()` | 4 | Zbiera aktualne wrażliwe wartości systemowe do zamaskowania. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/anonymizer.py#L12) |

### `fixos.cli` [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/__init__.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `NaturalLanguageGroup` | 1 | Click group that routes unknown commands to 'ask' command. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/shared.py#L54) |

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `ask` | `ask(prompt, dry_run)` | 1 | Wykonaj polecenie w języku naturalnym. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/ask_cmd.py#L10) |
| `cleanup_services` | `cleanup_services(threshold, services, json_output, cleanup, ...)` | 15 ⚠️ | Skanuje i czyści dane usług przekraczające próg. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/cleanup_cmd.py#L24) |
| `config` | `config()` | 1 | Zarządzanie konfiguracją fixOS. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/config_cmd.py#L8) |
| `config_init` | `config_init(force)` | 3 | Zainicjalizuj plik konfiguracyjny .env. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/config_cmd.py#L40) |
| `config_set` | `config_set(key, value)` | 2 | Ustaw wartość konfiguracyjną w .env. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/config_cmd.py#L72) |
| `config_show` | `config_show()` | 4 | Pokaż aktualną konfigurację. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/config_cmd.py#L14) |
| `features` | `features()` | 1 | Zarządzanie pakietami komfortu systemu. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/features_cmd.py#L21) |
| `features_audit` | `features_audit(profile, json_output)` | 4 | Sprawdź brakujące pakiety dla profilu. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/features_cmd.py#L29) |
| `features_install` | `features_install(profile, dry_run, yes, category)` | 15 ⚠️ | Zainstaluj brakujące pakiety dla profilu. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/features_cmd.py#L58) |
| `features_profiles` | `features_profiles()` | 3 | Lista dostępnych profili. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/features_cmd.py#L112) |
| `features_system` | `features_system()` | 1 | Pokaż wykryty system. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/features_cmd.py#L131) |
| `execute_cleanup_actions` | `execute_cleanup_actions(actions, cfg, llm_fallback)` | 6 | Execute cleanup actions with safety checks | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/fix_cmd.py#L219) |
| `fix` | `fix(provider, token, model, no_banner, ...)` | 18 ⚠️ | Przeprowadza pełną diagnostykę i uruchamia sesję naprawczą z LLM. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/fix_cmd.py#L28) |
| `handle_disk_cleanup_mode` | `handle_disk_cleanup_mode(disk_analysis, cfg, dry_run, interactive, ...)` | 13 ⚠️ | Handle disk cleanup mode with interactive planning | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/fix_cmd.py#L149) |
| `try_llm_fallback_for_failures` | `try_llm_fallback_for_failures(failed_actions, cfg)` | 3 | Try to fix failed actions using LLM | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/fix_cmd.py#L260) |
| `history` | `history(limit, json_output)` | 5 | Historia napraw fixOS. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/history_cmd.py#L10) |
| `cli` | `cli(ctx, dry_run, version)` | 3 | fixos – AI-powered diagnostyka i naprawa Linux, Windows, macOS. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/main.py#L13) |
| `main` | `main()` | 1 | Entry point for fixOS CLI. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/main.py#L120) |
| `orchestrate` | `orchestrate(provider, token, model, no_banner, ...)` | 13 ⚠️ | Zaawansowana orkiestracja napraw z grafem problemów. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/orchestrate_cmd.py#L23) |
| `profile` | `profile()` | 1 | Zarządzanie profilami diagnostycznymi. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/profile_cmd.py#L8) |
| `profile_list` | `profile_list()` | 4 | Pokaż dostępne profile diagnostyczne. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/profile_cmd.py#L14) |
| `profile_show` | `profile_show(name)` | 4 | Pokaż szczegóły profilu diagnostycznego. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/profile_cmd.py#L41) |
| `llm_providers` | `llm_providers(free)` | 6 | Lista dostępnych providerów LLM. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/provider_cmd.py#L109) |
| `providers` | `providers()` | 4 | Lista providerów LLM z oznaczeniem FREE/PAID. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/provider_cmd.py#L154) |
| `test_llm` | `test_llm(provider, token, model, no_banner)` | 9 | Test połączenia z LLM. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/provider_cmd.py#L192) |
| `quickfix` | `quickfix(dry_run, modules)` | 12 ⚠️ | Natychmiastowe naprawy bez API — baza znanych bugów. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/quickfix_cmd.py#L12) |
| `report` | `report(output_format, output, modules, profile)` | 16 ⚠️ | Eksport wyników diagnostyki do raportu HTML/Markdown/JSON. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/report_cmd.py#L14) |
| `rollback` | `rollback()` | 1 | Zarządzanie cofaniem operacji fixOS. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/rollback_cmd.py#L9) |
| `rollback_list` | `rollback_list(limit)` | 3 | Pokaż historię sesji naprawczych. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/rollback_cmd.py#L16) |
| `rollback_show` | `rollback_show(session_id)` | 5 | Pokaż szczegóły sesji rollback. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/rollback_cmd.py#L37) |
| `rollback_undo` | `rollback_undo(session_id, last, dry_run)` | 7 | Cofnij operacje z podanej sesji. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/rollback_cmd.py#L63) |
| `scan` | `scan(modules, output, show_raw, no_banner, ...)` | 12 ⚠️ | Przeprowadza diagnostykę systemu. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/scan_cmd.py#L18) |
| `add_common_options` | `add_common_options(fn)` | 2 | Decorator adding common LLM options to a Click command. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/shared.py#L26) |
| `add_shared_options` | `add_shared_options(func)` | 1 | Shared options for both scan and fix commands. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/shared.py#L33) |
| `token` | `token()` | 1 | Zarządzanie tokenem API. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/token_cmd.py#L10) |
| `token_clear` | `token_clear(env_file)` | 3 | Usuń token z pliku .env. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/token_cmd.py#L106) |
| `token_set` | `token_set(key, provider, env_file)` | 7 | Zapisz token API do pliku .env. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/token_cmd.py#L19) |
| `token_show` | `token_show()` | 2 | Pokaż obecny token (masked). | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/token_cmd.py#L90) |
| `watch` | `watch(interval, modules, alert_on, max_iterations)` | 2 | Monitorowanie systemu w tle z powiadomieniami. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/watch_cmd.py#L18) |

### `fixos.cli.ask_cmd` [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/ask_cmd.py)

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `ask` | `ask(prompt, dry_run)` | 1 | Wykonaj polecenie w języku naturalnym. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/ask_cmd.py#L10) |

### `fixos.cli.cleanup_cmd` [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/cleanup_cmd.py)

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `cleanup_services` | `cleanup_services(threshold, services, json_output, cleanup, ...)` | 15 ⚠️ | Skanuje i czyści dane usług przekraczające próg. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/cleanup_cmd.py#L24) |

### `fixos.cli.config_cmd` [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/config_cmd.py)

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `config` | `config()` | 1 | Zarządzanie konfiguracją fixOS. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/config_cmd.py#L8) |
| `config_init` | `config_init(force)` | 3 | Zainicjalizuj plik konfiguracyjny .env. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/config_cmd.py#L40) |
| `config_set` | `config_set(key, value)` | 2 | Ustaw wartość konfiguracyjną w .env. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/config_cmd.py#L72) |
| `config_show` | `config_show()` | 4 | Pokaż aktualną konfigurację. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/config_cmd.py#L14) |

### `fixos.cli.features_cmd` [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/features_cmd.py)

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `features` | `features()` | 1 | Zarządzanie pakietami komfortu systemu. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/features_cmd.py#L21) |
| `features_audit` | `features_audit(profile, json_output)` | 4 | Sprawdź brakujące pakiety dla profilu. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/features_cmd.py#L29) |
| `features_install` | `features_install(profile, dry_run, yes, category)` | 15 ⚠️ | Zainstaluj brakujące pakiety dla profilu. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/features_cmd.py#L58) |
| `features_profiles` | `features_profiles()` | 3 | Lista dostępnych profili. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/features_cmd.py#L112) |
| `features_system` | `features_system()` | 1 | Pokaż wykryty system. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/features_cmd.py#L131) |

### `fixos.cli.fix_cmd` [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/fix_cmd.py)

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `execute_cleanup_actions` | `execute_cleanup_actions(actions, cfg, llm_fallback)` | 6 | Execute cleanup actions with safety checks | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/fix_cmd.py#L219) |
| `fix` | `fix(provider, token, model, no_banner, ...)` | 18 ⚠️ | Przeprowadza pełną diagnostykę i uruchamia sesję naprawczą z LLM. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/fix_cmd.py#L28) |
| `handle_disk_cleanup_mode` | `handle_disk_cleanup_mode(disk_analysis, cfg, dry_run, interactive, ...)` | 13 ⚠️ | Handle disk cleanup mode with interactive planning | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/fix_cmd.py#L149) |
| `try_llm_fallback_for_failures` | `try_llm_fallback_for_failures(failed_actions, cfg)` | 3 | Try to fix failed actions using LLM | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/fix_cmd.py#L260) |

### `fixos.cli.history_cmd` [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/history_cmd.py)

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `history` | `history(limit, json_output)` | 5 | Historia napraw fixOS. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/history_cmd.py#L10) |

### `fixos.cli.main` [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/main.py)

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `cli` | `cli(ctx, dry_run, version)` | 3 | fixos – AI-powered diagnostyka i naprawa Linux, Windows, macOS. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/main.py#L13) |
| `main` | `main()` | 1 | Entry point for fixOS CLI. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/main.py#L120) |

### `fixos.cli.orchestrate_cmd` [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/orchestrate_cmd.py)

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `orchestrate` | `orchestrate(provider, token, model, no_banner, ...)` | 13 ⚠️ | Zaawansowana orkiestracja napraw z grafem problemów. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/orchestrate_cmd.py#L23) |

### `fixos.cli.profile_cmd` [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/profile_cmd.py)

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `profile` | `profile()` | 1 | Zarządzanie profilami diagnostycznymi. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/profile_cmd.py#L8) |
| `profile_list` | `profile_list()` | 4 | Pokaż dostępne profile diagnostyczne. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/profile_cmd.py#L14) |
| `profile_show` | `profile_show(name)` | 4 | Pokaż szczegóły profilu diagnostycznego. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/profile_cmd.py#L41) |

### `fixos.cli.provider_cmd` [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/provider_cmd.py)

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `llm_providers` | `llm_providers(free)` | 6 | Lista dostępnych providerów LLM. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/provider_cmd.py#L109) |
| `providers` | `providers()` | 4 | Lista providerów LLM z oznaczeniem FREE/PAID. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/provider_cmd.py#L154) |
| `test_llm` | `test_llm(provider, token, model, no_banner)` | 9 | Test połączenia z LLM. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/provider_cmd.py#L192) |

### `fixos.cli.quickfix_cmd` [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/quickfix_cmd.py)

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `quickfix` | `quickfix(dry_run, modules)` | 12 ⚠️ | Natychmiastowe naprawy bez API — baza znanych bugów. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/quickfix_cmd.py#L12) |

### `fixos.cli.report_cmd` [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/report_cmd.py)

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `report` | `report(output_format, output, modules, profile)` | 16 ⚠️ | Eksport wyników diagnostyki do raportu HTML/Markdown/JSON. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/report_cmd.py#L14) |

### `fixos.cli.rollback_cmd` [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/rollback_cmd.py)

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `rollback` | `rollback()` | 1 | Zarządzanie cofaniem operacji fixOS. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/rollback_cmd.py#L9) |
| `rollback_list` | `rollback_list(limit)` | 3 | Pokaż historię sesji naprawczych. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/rollback_cmd.py#L16) |
| `rollback_show` | `rollback_show(session_id)` | 5 | Pokaż szczegóły sesji rollback. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/rollback_cmd.py#L37) |
| `rollback_undo` | `rollback_undo(session_id, last, dry_run)` | 7 | Cofnij operacje z podanej sesji. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/rollback_cmd.py#L63) |

### `fixos.cli.scan_cmd` [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/scan_cmd.py)

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `scan` | `scan(modules, output, show_raw, no_banner, ...)` | 12 ⚠️ | Przeprowadza diagnostykę systemu. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/scan_cmd.py#L18) |

### `fixos.cli.shared` [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/shared.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `NaturalLanguageGroup` | 1 | Click group that routes unknown commands to 'ask' command. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/shared.py#L54) |

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `add_common_options` | `add_common_options(fn)` | 2 | Decorator adding common LLM options to a Click command. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/shared.py#L26) |
| `add_shared_options` | `add_shared_options(func)` | 1 | Shared options for both scan and fix commands. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/shared.py#L33) |

### `fixos.cli.token_cmd` [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/token_cmd.py)

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `token` | `token()` | 1 | Zarządzanie tokenem API. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/token_cmd.py#L10) |
| `token_clear` | `token_clear(env_file)` | 3 | Usuń token z pliku .env. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/token_cmd.py#L106) |
| `token_set` | `token_set(key, provider, env_file)` | 7 | Zapisz token API do pliku .env. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/token_cmd.py#L19) |
| `token_show` | `token_show()` | 2 | Pokaż obecny token (masked). | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/token_cmd.py#L90) |

### `fixos.cli.watch_cmd` [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/watch_cmd.py)

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `watch` | `watch(interval, modules, alert_on, max_iterations)` | 2 | Monitorowanie systemu w tle z powiadomieniami. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/cli/watch_cmd.py#L18) |

### `fixos.config` [source](https://github.com/wronai/fixfedora/blob/main/fixos/config.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `FixOsConfig` | 3 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/config.py#L156) |

**`FixOsConfig` methods:**

- `load(cls)` — Tworzy konfigurację z połączonych źródeł.
- `validate()` — Zwraca listę błędów walidacji (pusta = OK).
- `summary()` — Krótkie podsumowanie konfiguracji (bez klucza API).

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `detect_provider_from_key` | `detect_provider_from_key(key)` | 3 | Wykrywa provider na podstawie prefiksu klucza API. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/config.py#L309) |
| `get_providers_list` | `get_providers_list()` | 3 | Zwraca listę providerów jako listę słowników. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/config.py#L410) |
| `interactive_provider_setup` | `interactive_provider_setup()` | 24 ⚠️ | Interaktywny wybór providera gdy brak konfiguracji. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/config.py#L317) |

### `fixos.diagnostics` [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/__init__.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `DiskAnalyzer` | 6 | Analyzes disk usage and provides cleanup suggestions | [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/disk_analyzer.py#L15) |
| `FlatpakAnalyzer` | 2 | Advanced analyzer for Flatpak cleanup decisions | [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/flatpak_analyzer.py#L62) |
| `FlatpakItemInfo` | 1 | Detailed info about a Flatpak item (app, runtime, or data) | [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/flatpak_analyzer.py#L28) |
| `FlatpakItemType` | 0 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/flatpak_analyzer.py#L21) |
| `ServiceCleaner` | 6 | Plans and executes cleanup of service data. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/service_cleanup.py#L10) |
| `ServiceDetailsProvider` | 1 | Provides detailed information about service data. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/service_details.py#L18) |
| `ServiceDataInfo` | 0 | Information about service data. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/service_scanner.py#L75) |
| `ServiceDataScanner` | 4 | Scans for large service data directories and allows cleanup. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/service_scanner.py#L92) |
| `ServiceType` | 0 | Service types that can be scanned and cleaned. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/service_scanner.py#L21) |

**`DiskAnalyzer` methods:**

- `analyze_disk_usage(path)` — Comprehensive disk usage analysis
- `get_large_files(path, min_size_mb, max_files)` — Find large files
- `get_cache_dirs(path, max_dirs)` — Find cache directories
- `get_log_dirs(path, max_dirs)` — Find log directories
- `get_temp_dirs(path, max_dirs)` — Find temporary directories
- `suggest_cleanup_actions(path)` — Generate cleanup suggestions using heuristics

**`FlatpakAnalyzer` methods:**

- `analyze()` — Run full Flatpak analysis
- `get_cleanup_summary()` — Get human-readable summary of cleanup opportunities

**`ServiceCleaner` methods:**

- `get_cleanup_plan(selected_services)` — Generate cleanup plan for services.
- `cleanup_service(service_type, dry_run)` — Execute cleanup for a specific service.
- `is_safe_cleanup(service_type)` — Determine if cleanup is generally safe (cache-only, not user data).
- `get_service_description(service_type)` — Get description for service type.
- `get_cleanup_command(service_type, path)` — Get cleanup command for service.
- `get_preview_command(service_type, path)` — Get preview command for service.

**`ServiceDataScanner` methods:**

- `scan_all_services()` — Scan all known services for data above threshold.
- `scan_service(service_type)` — Scan specific service type for data.
- `get_cleanup_plan(selected_services)` — Generate cleanup plan for services.
- `cleanup_service(service_type, dry_run)` — Execute cleanup for a specific service.

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `main` | `main()` | 1 | Test the disk analyzer | [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/disk_analyzer.py#L411) |
| `analyze_flatpak_for_cleanup` | `analyze_flatpak_for_cleanup()` | 1 | Convenience function to run full Flatpak analysis | [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/flatpak_analyzer.py#L329) |
| `main` | `main()` | 1 | Test the service data scanner. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/service_scanner.py#L241) |
| `diagnose_audio` | `diagnose_audio()` | 1 | Diagnostyka dźwięku (ALSA/PipeWire/PulseAudio/SOF). | [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/system_checks.py#L49) |
| `diagnose_hardware` | `diagnose_hardware()` | 1 | Diagnostyka sprzętu laptopa/desktopa (ACPI, kamera, touchpad, DMI). | [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/system_checks.py#L165) |
| `diagnose_resources` | `diagnose_resources()` | 13 ⚠️ | Diagnostyka zasobów systemowych. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/system_checks.py#L384) |
| `diagnose_security` | `diagnose_security()` | 4 | Diagnostyka bezpieczeństwa systemu i sieci. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/system_checks.py#L303) |
| `diagnose_system` | `diagnose_system()` | 14 ⚠️ | System metrics – cross-platform: CPU, RAM, disks, processes. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/system_checks.py#L204) |
| `diagnose_thumbnails` | `diagnose_thumbnails()` | 1 | Diagnostyka podglądów plików (thumbnails) w system. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/system_checks.py#L106) |
| `get_full_diagnostics` | `get_full_diagnostics(modules, progress_callback)` | 7 | Zbiera diagnostykę z wybranych modułów. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/system_checks.py#L482) |

### `fixos.diagnostics.disk_analyzer` [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/disk_analyzer.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `DiskAnalyzer` | 6 | Analyzes disk usage and provides cleanup suggestions | [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/disk_analyzer.py#L15) |

**`DiskAnalyzer` methods:**

- `analyze_disk_usage(path)` — Comprehensive disk usage analysis
- `get_large_files(path, min_size_mb, max_files)` — Find large files
- `get_cache_dirs(path, max_dirs)` — Find cache directories
- `get_log_dirs(path, max_dirs)` — Find log directories
- `get_temp_dirs(path, max_dirs)` — Find temporary directories
- `suggest_cleanup_actions(path)` — Generate cleanup suggestions using heuristics

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `main` | `main()` | 1 | Test the disk analyzer | [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/disk_analyzer.py#L411) |

### `fixos.diagnostics.flatpak_analyzer` [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/flatpak_analyzer.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `FlatpakAnalyzer` | 2 | Advanced analyzer for Flatpak cleanup decisions | [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/flatpak_analyzer.py#L62) |
| `FlatpakItemInfo` | 1 | Detailed info about a Flatpak item (app, runtime, or data) | [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/flatpak_analyzer.py#L28) |
| `FlatpakItemType` | 0 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/flatpak_analyzer.py#L21) |

**`FlatpakAnalyzer` methods:**

- `analyze()` — Run full Flatpak analysis
- `get_cleanup_summary()` — Get human-readable summary of cleanup opportunities

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `analyze_flatpak_for_cleanup` | `analyze_flatpak_for_cleanup()` | 1 | Convenience function to run full Flatpak analysis | [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/flatpak_analyzer.py#L329) |

### `fixos.diagnostics.service_cleanup` [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/service_cleanup.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `ServiceCleaner` | 6 | Plans and executes cleanup of service data. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/service_cleanup.py#L10) |

**`ServiceCleaner` methods:**

- `get_cleanup_plan(selected_services)` — Generate cleanup plan for services.
- `cleanup_service(service_type, dry_run)` — Execute cleanup for a specific service.
- `is_safe_cleanup(service_type)` — Determine if cleanup is generally safe (cache-only, not user data).
- `get_service_description(service_type)` — Get description for service type.
- `get_cleanup_command(service_type, path)` — Get cleanup command for service.
- `get_preview_command(service_type, path)` — Get preview command for service.

### `fixos.diagnostics.service_details` [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/service_details.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `ServiceDetailsProvider` | 1 | Provides detailed information about service data. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/service_details.py#L18) |

### `fixos.diagnostics.service_scanner` [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/service_scanner.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `ServiceDataInfo` | 0 | Information about service data. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/service_scanner.py#L75) |
| `ServiceDataScanner` | 4 | Scans for large service data directories and allows cleanup. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/service_scanner.py#L92) |
| `ServiceType` | 0 | Service types that can be scanned and cleaned. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/service_scanner.py#L21) |

**`ServiceDataScanner` methods:**

- `scan_all_services()` — Scan all known services for data above threshold.
- `scan_service(service_type)` — Scan specific service type for data.
- `get_cleanup_plan(selected_services)` — Generate cleanup plan for services.
- `cleanup_service(service_type, dry_run)` — Execute cleanup for a specific service.

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `main` | `main()` | 1 | Test the service data scanner. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/service_scanner.py#L241) |

### `fixos.diagnostics.system_checks` [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/system_checks.py)

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `diagnose_audio` | `diagnose_audio()` | 1 | Diagnostyka dźwięku (ALSA/PipeWire/PulseAudio/SOF). | [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/system_checks.py#L49) |
| `diagnose_hardware` | `diagnose_hardware()` | 1 | Diagnostyka sprzętu laptopa/desktopa (ACPI, kamera, touchpad, DMI). | [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/system_checks.py#L165) |
| `diagnose_resources` | `diagnose_resources()` | 13 ⚠️ | Diagnostyka zasobów systemowych. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/system_checks.py#L384) |
| `diagnose_security` | `diagnose_security()` | 4 | Diagnostyka bezpieczeństwa systemu i sieci. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/system_checks.py#L303) |
| `diagnose_system` | `diagnose_system()` | 14 ⚠️ | System metrics – cross-platform: CPU, RAM, disks, processes. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/system_checks.py#L204) |
| `diagnose_thumbnails` | `diagnose_thumbnails()` | 1 | Diagnostyka podglądów plików (thumbnails) w system. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/system_checks.py#L106) |
| `get_full_diagnostics` | `get_full_diagnostics(modules, progress_callback)` | 7 | Zbiera diagnostykę z wybranych modułów. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/diagnostics/system_checks.py#L482) |

### `fixos.features` [source](https://github.com/wronai/fixfedora/blob/main/fixos/features/__init__.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `SystemDetector` | 1 | Detects system parameters. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/features/__init__.py#L50) |
| `SystemInfo` | 0 | Complete system information snapshot. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/features/__init__.py#L16) |
| `AuditResult` | 3 | Result of feature audit - what's installed, what's missing. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/features/auditor.py#L15) |
| `FeatureAuditor` | 1 | Compares installed packages with profile requirements. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/features/auditor.py#L52) |
| `PackageCatalog` | 4 | Manages the package database. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/features/catalog.py#L48) |
| `PackageCategory` | 0 | A category of packages (e.g., core_utils, dev_tools). | [source](https://github.com/wronai/fixfedora/blob/main/fixos/features/catalog.py#L40) |
| `PackageInfo` | 2 | Information about a single package. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/features/catalog.py#L12) |
| `FeatureInstaller` | 2 | Safely installs packages using native package manager or other backends. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/features/installer.py#L14) |
| `UserProfile` | 4 | A user profile defining what packages/features they want. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/features/profiles.py#L14) |
| `FeatureRenderer` | 3 | Renders audit results for terminal display. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/features/renderer.py#L18) |

**`PackageCatalog` methods:**

- `load(cls, data_dir)` — Load package catalog from YAML files.
- `get_package(pkg_id)` — Get package by ID.
- `get_packages_by_category(category)` — Get all packages in a category.
- `list_categories()` — List all category IDs.

**`PackageInfo` methods:**

- `get_distro_name(distro)` — Get package name for specific distro.
- `is_available_on(distro)` — Check if package is available on given distro.

**`FeatureInstaller` methods:**

- `install(packages)` — Install a list of packages.
- `get_rollback_commands(installed_packages)` — Generate rollback commands for installed packages.

**`UserProfile` methods:**

- `load(cls, profile_name, data_dir)` — Load a profile from YAML file.
- `list_available(cls, data_dir)` — List available profile names.
- `resolve_packages(catalog, system_info)` — Resolve all packages for this profile based on system.
- `to_dict()` — Convert to dictionary.

**`FeatureRenderer` methods:**

- `render_audit(result)` — Render complete audit results.
- `render_package_list(packages, title)` — Render a list of packages.
- `render_system_info(system)` — Render system information.

### `fixos.features.auditor` [source](https://github.com/wronai/fixfedora/blob/main/fixos/features/auditor.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `AuditResult` | 3 | Result of feature audit - what's installed, what's missing. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/features/auditor.py#L15) |
| `FeatureAuditor` | 1 | Compares installed packages with profile requirements. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/features/auditor.py#L52) |

### `fixos.features.catalog` [source](https://github.com/wronai/fixfedora/blob/main/fixos/features/catalog.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `PackageCatalog` | 4 | Manages the package database. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/features/catalog.py#L48) |
| `PackageCategory` | 0 | A category of packages (e.g., core_utils, dev_tools). | [source](https://github.com/wronai/fixfedora/blob/main/fixos/features/catalog.py#L40) |
| `PackageInfo` | 2 | Information about a single package. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/features/catalog.py#L12) |

**`PackageCatalog` methods:**

- `load(cls, data_dir)` — Load package catalog from YAML files.
- `get_package(pkg_id)` — Get package by ID.
- `get_packages_by_category(category)` — Get all packages in a category.
- `list_categories()` — List all category IDs.

**`PackageInfo` methods:**

- `get_distro_name(distro)` — Get package name for specific distro.
- `is_available_on(distro)` — Check if package is available on given distro.

### `fixos.features.installer` [source](https://github.com/wronai/fixfedora/blob/main/fixos/features/installer.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `FeatureInstaller` | 2 | Safely installs packages using native package manager or other backends. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/features/installer.py#L14) |

**`FeatureInstaller` methods:**

- `install(packages)` — Install a list of packages.
- `get_rollback_commands(installed_packages)` — Generate rollback commands for installed packages.

### `fixos.features.profiles` [source](https://github.com/wronai/fixfedora/blob/main/fixos/features/profiles.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `UserProfile` | 4 | A user profile defining what packages/features they want. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/features/profiles.py#L14) |

**`UserProfile` methods:**

- `load(cls, profile_name, data_dir)` — Load a profile from YAML file.
- `list_available(cls, data_dir)` — List available profile names.
- `resolve_packages(catalog, system_info)` — Resolve all packages for this profile based on system.
- `to_dict()` — Convert to dictionary.

### `fixos.features.renderer` [source](https://github.com/wronai/fixfedora/blob/main/fixos/features/renderer.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `FeatureRenderer` | 3 | Renders audit results for terminal display. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/features/renderer.py#L18) |

**`FeatureRenderer` methods:**

- `render_audit(result)` — Render complete audit results.
- `render_package_list(packages, title)` — Render a list of packages.
- `render_system_info(system)` — Render system information.

### `fixos.interactive` [source](https://github.com/wronai/fixfedora/blob/main/fixos/interactive/__init__.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `CleanupAction` | 0 | Represents a cleanup action | [source](https://github.com/wronai/fixfedora/blob/main/fixos/interactive/cleanup_planner.py#L32) |
| `CleanupPlanner` | 4 | Interactive cleanup planning and grouping system | [source](https://github.com/wronai/fixfedora/blob/main/fixos/interactive/cleanup_planner.py#L52) |
| `CleanupType` | 0 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/interactive/cleanup_planner.py#L20) |
| `Priority` | 0 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/interactive/cleanup_planner.py#L13) |

**`CleanupPlanner` methods:**

- `group_by_category(suggestions)` — Group cleanup suggestions by category
- `prioritize_actions(grouped_actions)` — Create prioritized list of all actions
- `create_cleanup_plan(suggestions)` — Create comprehensive cleanup plan
- `interactive_selection(plan)` — Interactive selection process (simulated for now)

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `main` | `main()` | 1 | Test the cleanup planner | [source](https://github.com/wronai/fixfedora/blob/main/fixos/interactive/cleanup_planner.py#L385) |

### `fixos.interactive.cleanup_planner` [source](https://github.com/wronai/fixfedora/blob/main/fixos/interactive/cleanup_planner.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `CleanupAction` | 0 | Represents a cleanup action | [source](https://github.com/wronai/fixfedora/blob/main/fixos/interactive/cleanup_planner.py#L32) |
| `CleanupPlanner` | 4 | Interactive cleanup planning and grouping system | [source](https://github.com/wronai/fixfedora/blob/main/fixos/interactive/cleanup_planner.py#L52) |
| `CleanupType` | 0 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/interactive/cleanup_planner.py#L20) |
| `Priority` | 0 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/interactive/cleanup_planner.py#L13) |

**`CleanupPlanner` methods:**

- `group_by_category(suggestions)` — Group cleanup suggestions by category
- `prioritize_actions(grouped_actions)` — Create prioritized list of all actions
- `create_cleanup_plan(suggestions)` — Create comprehensive cleanup plan
- `interactive_selection(plan)` — Interactive selection process (simulated for now)

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `main` | `main()` | 1 | Test the cleanup planner | [source](https://github.com/wronai/fixfedora/blob/main/fixos/interactive/cleanup_planner.py#L385) |

### `fixos.llm_shell` [source](https://github.com/wronai/fixfedora/blob/main/fixos/llm_shell.py)

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `execute_command` | `execute_command(cmd)` | 10 | Wykonuje komendę systemową z potwierdzeniem użytkownika. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/llm_shell.py#L66) |
| `format_time` | `format_time(seconds)` | 1 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/llm_shell.py#L58) |
| `run_llm_shell` | `run_llm_shell(diagnostics_data, token, model, timeout, ...)` | 15 ⚠️ | Uruchamia interaktywny shell LLM z przekazanymi danymi diagnostycznymi. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/llm_shell.py#L100) |

### `fixos.orchestrator` [source](https://github.com/wronai/fixfedora/blob/main/fixos/orchestrator/__init__.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `CommandExecutor` | 6 | Bezpieczny executor komend z: | [source](https://github.com/wronai/fixfedora/blob/main/fixos/orchestrator/executor.py#L85) |
| `CommandTimeoutError` | 0 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/orchestrator/executor.py#L23) |
| `DangerousCommandError` | 0 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/orchestrator/executor.py#L16) |
| `ExecutionResult` | 2 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/orchestrator/executor.py#L31) |
| `Problem` | 2 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/orchestrator/graph.py#L19) |
| `ProblemGraph` | 7 | DAG problemów systemowych z topological sort do wyznaczania kolejności napraw. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/orchestrator/graph.py#L46) |
| `FixOrchestrator` | 4 | Orkiestrator napraw systemowych. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/orchestrator/orchestrator.py#L83) |
| `RollbackEntry` | 0 | Single recorded operation with its rollback command. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/orchestrator/rollback.py#L20) |
| `RollbackSession` | 5 | A session of recorded operations that can be rolled back. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/orchestrator/rollback.py#L32) |

**`CommandExecutor` methods:**

- `is_dangerous(command)` — Sprawdza czy komenda jest potencjalnie destruktywna.
- `needs_sudo(command)`
- `add_sudo(command)`
- `check_idempotent(command)` — Zwraca komendę sprawdzającą stan (jeśli znana), None jeśli nie dotyczy.
- `execute_sync(command, timeout, add_sudo, check_idempotent)` — Synchroniczne wykonanie komendy.
- `execute(command, timeout, add_sudo)` — Asynchroniczne wykonanie komendy.

**`Problem` methods:**

- `is_actionable()`
- `to_summary()`

**`ProblemGraph` methods:**

- `add(problem)`
- `get(problem_id)`
- `next_actionable()` — Zwraca pierwszy problem bez nierozwiązanych zależności.
- `all_done()`
- `pending_count()`
- `summary()`
- `render_tree()` — Renderuje drzewo problemów jako tekst.

**`FixOrchestrator` methods:**

- `load_from_diagnostics(diagnostics)` — Parsuje dane diagnostyczne przez LLM i buduje graf problemów.
- `load_from_dict(problems_data)` — Ładuje problemy bezpośrednio z listy dict (bez LLM).
- `run_sync(confirm_fn, progress_fn)` — Synchroniczna pętla napraw (dla trybu HITL).
- `run_async(confirm_fn, progress_fn)` — Asynchroniczna wersja run_sync.

**`RollbackSession` methods:**

- `record(command, rollback_cmd, stdout, stderr, ...)` — Zapisz wykonaną operację.
- `get_rollback_commands()` — Zwraca listę (komenda, rollback) w odwróconej kolejności.
- `rollback_last(n, dry_run)` — Cofnij ostatnich n operacji.
- `load(cls, session_id)` — Załaduj sesję z pliku.
- `list_sessions(cls, limit)` — Lista ostatnich sesji rollback.

### `fixos.orchestrator.executor` [source](https://github.com/wronai/fixfedora/blob/main/fixos/orchestrator/executor.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `CommandExecutor` | 6 | Bezpieczny executor komend z: | [source](https://github.com/wronai/fixfedora/blob/main/fixos/orchestrator/executor.py#L85) |
| `CommandTimeoutError` | 0 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/orchestrator/executor.py#L23) |
| `DangerousCommandError` | 0 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/orchestrator/executor.py#L16) |
| `ExecutionResult` | 2 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/orchestrator/executor.py#L31) |

**`CommandExecutor` methods:**

- `is_dangerous(command)` — Sprawdza czy komenda jest potencjalnie destruktywna.
- `needs_sudo(command)`
- `add_sudo(command)`
- `check_idempotent(command)` — Zwraca komendę sprawdzającą stan (jeśli znana), None jeśli nie dotyczy.
- `execute_sync(command, timeout, add_sudo, check_idempotent)` — Synchroniczne wykonanie komendy.
- `execute(command, timeout, add_sudo)` — Asynchroniczne wykonanie komendy.

### `fixos.orchestrator.graph` [source](https://github.com/wronai/fixfedora/blob/main/fixos/orchestrator/graph.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `Problem` | 2 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/orchestrator/graph.py#L19) |
| `ProblemGraph` | 7 | DAG problemów systemowych z topological sort do wyznaczania kolejności napraw. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/orchestrator/graph.py#L46) |

**`Problem` methods:**

- `is_actionable()`
- `to_summary()`

**`ProblemGraph` methods:**

- `add(problem)`
- `get(problem_id)`
- `next_actionable()` — Zwraca pierwszy problem bez nierozwiązanych zależności.
- `all_done()`
- `pending_count()`
- `summary()`
- `render_tree()` — Renderuje drzewo problemów jako tekst.

### `fixos.orchestrator.orchestrator` [source](https://github.com/wronai/fixfedora/blob/main/fixos/orchestrator/orchestrator.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `FixOrchestrator` | 4 | Orkiestrator napraw systemowych. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/orchestrator/orchestrator.py#L83) |

**`FixOrchestrator` methods:**

- `load_from_diagnostics(diagnostics)` — Parsuje dane diagnostyczne przez LLM i buduje graf problemów.
- `load_from_dict(problems_data)` — Ładuje problemy bezpośrednio z listy dict (bez LLM).
- `run_sync(confirm_fn, progress_fn)` — Synchroniczna pętla napraw (dla trybu HITL).
- `run_async(confirm_fn, progress_fn)` — Asynchroniczna wersja run_sync.

### `fixos.orchestrator.rollback` [source](https://github.com/wronai/fixfedora/blob/main/fixos/orchestrator/rollback.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `RollbackEntry` | 0 | Single recorded operation with its rollback command. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/orchestrator/rollback.py#L20) |
| `RollbackSession` | 5 | A session of recorded operations that can be rolled back. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/orchestrator/rollback.py#L32) |

**`RollbackSession` methods:**

- `record(command, rollback_cmd, stdout, stderr, ...)` — Zapisz wykonaną operację.
- `get_rollback_commands()` — Zwraca listę (komenda, rollback) w odwróconej kolejności.
- `rollback_last(n, dry_run)` — Cofnij ostatnich n operacji.
- `load(cls, session_id)` — Załaduj sesję z pliku.
- `list_sessions(cls, limit)` — Lista ostatnich sesji rollback.

### `fixos.platform_utils` [source](https://github.com/wronai/fixfedora/blob/main/fixos/platform_utils.py)

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `cancel_signal_timeout` | `cancel_signal_timeout()` | 2 | Cancels the timeout signal (POSIX only). | [source](https://github.com/wronai/fixfedora/blob/main/fixos/platform_utils.py#L180) |
| `elevate_cmd` | `elevate_cmd(cmd)` | 3 | Adds sudo (Linux/Mac) or wraps in PowerShell -Verb RunAs (Windows). | [source](https://github.com/wronai/fixfedora/blob/main/fixos/platform_utils.py#L61) |
| `get_os_info` | `get_os_info()` | 5 | Returns basic OS information. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/platform_utils.py#L22) |
| `get_package_manager` | `get_package_manager()` | 8 | Detects the system package manager. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/platform_utils.py#L123) |
| `install_package_cmd` | `install_package_cmd(package)` | 2 | Returns the install command for the detected package manager. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/platform_utils.py#L141) |
| `is_dangerous` | `is_dangerous(cmd)` | 3 | Returns reason string if command is dangerous, None if safe. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/platform_utils.py#L72) |
| `needs_elevation` | `needs_elevation(cmd)` | 5 | Returns True if command likely needs admin/sudo. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/platform_utils.py#L41) |
| `run_command` | `run_command(cmd, timeout, shell)` | 5 | Runs a command cross-platform. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/platform_utils.py#L91) |
| `setup_signal_timeout` | `setup_signal_timeout(seconds, handler)` | 2 | Sets up a timeout signal. Returns True if supported (POSIX only). | [source](https://github.com/wronai/fixfedora/blob/main/fixos/platform_utils.py#L167) |

### `fixos.plugins` [source](https://github.com/wronai/fixfedora/blob/main/fixos/plugins/__init__.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `DiagnosticPlugin` | 3 | Bazowa klasa dla pluginów diagnostycznych fixOS. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/plugins/base.py#L64) |
| `DiagnosticResult` | 1 | Result of a diagnostic plugin run. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/plugins/base.py#L36) |
| `Finding` | 0 | Single finding from a diagnostic plugin. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/plugins/base.py#L25) |
| `Severity` | 0 | Severity level for diagnostic findings. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/plugins/base.py#L16) |
| `Plugin` | 1 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/plugins/builtin/audio.py#L9) |
| `Plugin` | 1 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/plugins/builtin/disk.py#L9) |
| `Plugin` | 1 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/plugins/builtin/hardware.py#L9) |
| `Plugin` | 1 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/plugins/builtin/resources.py#L9) |
| `Plugin` | 1 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/plugins/builtin/security.py#L9) |
| `Plugin` | 1 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/plugins/builtin/thumbnails.py#L9) |
| `PluginRegistry` | 6 | Registry for diagnostic plugins with autodiscovery. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/plugins/registry.py#L21) |

**`DiagnosticPlugin` methods:**

- `diagnose()` — Wykonaj diagnostykę i zwróć wynik.
- `can_run()` — Czy plugin może działać na aktualnej platformie?
- `get_metadata()`

**`PluginRegistry` methods:**

- `discover()` — Odkrywanie pluginów przez builtin + entry_points.
- `register(plugin)` — Ręczna rejestracja pluginu.
- `list_plugins(runnable_only)` — Lista zarejestrowanych pluginów.
- `get_plugin(name)` — Pobierz plugin po nazwie.
- `run(modules, progress_callback)` — Uruchom diagnostykę dla wybranych (lub wszystkich) modułów.

### `fixos.plugins.base` [source](https://github.com/wronai/fixfedora/blob/main/fixos/plugins/base.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `DiagnosticPlugin` | 3 | Bazowa klasa dla pluginów diagnostycznych fixOS. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/plugins/base.py#L64) |
| `DiagnosticResult` | 1 | Result of a diagnostic plugin run. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/plugins/base.py#L36) |
| `Finding` | 0 | Single finding from a diagnostic plugin. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/plugins/base.py#L25) |
| `Severity` | 0 | Severity level for diagnostic findings. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/plugins/base.py#L16) |

**`DiagnosticPlugin` methods:**

- `diagnose()` — Wykonaj diagnostykę i zwróć wynik.
- `can_run()` — Czy plugin może działać na aktualnej platformie?
- `get_metadata()`

### `fixos.plugins.builtin` [source](https://github.com/wronai/fixfedora/blob/main/fixos/plugins/builtin/__init__.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `Plugin` | 1 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/plugins/builtin/audio.py#L9) |
| `Plugin` | 1 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/plugins/builtin/disk.py#L9) |
| `Plugin` | 1 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/plugins/builtin/hardware.py#L9) |
| `Plugin` | 1 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/plugins/builtin/resources.py#L9) |
| `Plugin` | 1 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/plugins/builtin/security.py#L9) |
| `Plugin` | 1 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/plugins/builtin/thumbnails.py#L9) |

### `fixos.plugins.builtin.audio` [source](https://github.com/wronai/fixfedora/blob/main/fixos/plugins/builtin/audio.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `Plugin` | 1 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/plugins/builtin/audio.py#L9) |

### `fixos.plugins.builtin.disk` [source](https://github.com/wronai/fixfedora/blob/main/fixos/plugins/builtin/disk.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `Plugin` | 1 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/plugins/builtin/disk.py#L9) |

### `fixos.plugins.builtin.hardware` [source](https://github.com/wronai/fixfedora/blob/main/fixos/plugins/builtin/hardware.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `Plugin` | 1 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/plugins/builtin/hardware.py#L9) |

### `fixos.plugins.builtin.resources` [source](https://github.com/wronai/fixfedora/blob/main/fixos/plugins/builtin/resources.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `Plugin` | 1 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/plugins/builtin/resources.py#L9) |

### `fixos.plugins.builtin.security` [source](https://github.com/wronai/fixfedora/blob/main/fixos/plugins/builtin/security.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `Plugin` | 1 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/plugins/builtin/security.py#L9) |

### `fixos.plugins.builtin.thumbnails` [source](https://github.com/wronai/fixfedora/blob/main/fixos/plugins/builtin/thumbnails.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `Plugin` | 1 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/plugins/builtin/thumbnails.py#L9) |

### `fixos.plugins.registry` [source](https://github.com/wronai/fixfedora/blob/main/fixos/plugins/registry.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `PluginRegistry` | 6 | Registry for diagnostic plugins with autodiscovery. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/plugins/registry.py#L21) |

**`PluginRegistry` methods:**

- `discover()` — Odkrywanie pluginów przez builtin + entry_points.
- `register(plugin)` — Ręczna rejestracja pluginu.
- `list_plugins(runnable_only)` — Lista zarejestrowanych pluginów.
- `get_plugin(name)` — Pobierz plugin po nazwie.
- `run(modules, progress_callback)` — Uruchom diagnostykę dla wybranych (lub wszystkich) modułów.

### `fixos.profiles` [source](https://github.com/wronai/fixfedora/blob/main/fixos/profiles/__init__.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `Profile` | 3 | Profil diagnostyczny z zestawem modułów i progów. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/profiles/__init__.py#L21) |

**`Profile` methods:**

- `load(cls, name)` — Załaduj profil — najpierw user, potem builtin.
- `list_available(cls)` — Lista dostępnych profili (builtin + user).
- `to_dict()`

### `fixos.providers` [source](https://github.com/wronai/fixfedora/blob/main/fixos/providers/__init__.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `LLMClient` | 5 | Wrapper nad openai.OpenAI kompatybilny z wieloma providerami. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/providers/llm.py#L26) |
| `LLMError` | 0 | Błąd komunikacji z LLM. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/providers/llm.py#L21) |
| `LLMAnalysis` | 0 | Result of LLM analysis | [source](https://github.com/wronai/fixfedora/blob/main/fixos/providers/llm_analyzer.py#L12) |
| `LLMAnalyzer` | 4 | Uses LLM to analyze disk issues when heuristics aren't sufficient | [source](https://github.com/wronai/fixfedora/blob/main/fixos/providers/llm_analyzer.py#L20) |
| `CommandValidation` | 0 | Wynik walidacji komendy przez LLM. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/providers/schemas.py#L66) |
| `FixSuggestion` | 0 | Pojedyncza sugestia naprawy od LLM. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/providers/schemas.py#L21) |
| `LLMDiagnosticResponse` | 0 | Strukturalna odpowiedź LLM na dane diagnostyczne. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/providers/schemas.py#L41) |
| `NLPIntent` | 0 | Rozpoznana intencja z polecenia NLP. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/providers/schemas.py#L58) |
| `RiskLevel` | 0 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/providers/schemas.py#L15) |

**`LLMClient` methods:**

- `chat(messages)` — Wysyła wiadomości do LLM i zwraca odpowiedź jako string.
- `chat_stream(messages)` — Generator streamujący tokeny odpowiedzi.
- `chat_structured(messages, response_model)` — Wywołanie LLM z wymuszonym schematem JSON (Pydantic model).
- `ping()` — Sprawdza czy API odpowiada (krótki test).

**`LLMAnalyzer` methods:**

- `analyze_disk_issues(disk_data)` — Use LLM to analyze disk issues when heuristics are insufficient
- `analyze_failed_action(action, error)` — Analyze failed cleanup action and suggest alternatives
- `analyze_complex_pattern(pattern_data)` — Analyze complex disk usage patterns that heuristics can't categorize
- `enhance_heuristics_with_llm(heuristic_suggestions, disk_data)` — Enhance heuristic suggestions with LLM insights

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `main` | `main()` | 1 | Test the LLM analyzer | [source](https://github.com/wronai/fixfedora/blob/main/fixos/providers/llm_analyzer.py#L326) |

### `fixos.providers.llm` [source](https://github.com/wronai/fixfedora/blob/main/fixos/providers/llm.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `LLMClient` | 5 | Wrapper nad openai.OpenAI kompatybilny z wieloma providerami. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/providers/llm.py#L26) |
| `LLMError` | 0 | Błąd komunikacji z LLM. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/providers/llm.py#L21) |

**`LLMClient` methods:**

- `chat(messages)` — Wysyła wiadomości do LLM i zwraca odpowiedź jako string.
- `chat_stream(messages)` — Generator streamujący tokeny odpowiedzi.
- `chat_structured(messages, response_model)` — Wywołanie LLM z wymuszonym schematem JSON (Pydantic model).
- `ping()` — Sprawdza czy API odpowiada (krótki test).

### `fixos.providers.llm_analyzer` [source](https://github.com/wronai/fixfedora/blob/main/fixos/providers/llm_analyzer.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `LLMAnalysis` | 0 | Result of LLM analysis | [source](https://github.com/wronai/fixfedora/blob/main/fixos/providers/llm_analyzer.py#L12) |
| `LLMAnalyzer` | 4 | Uses LLM to analyze disk issues when heuristics aren't sufficient | [source](https://github.com/wronai/fixfedora/blob/main/fixos/providers/llm_analyzer.py#L20) |

**`LLMAnalyzer` methods:**

- `analyze_disk_issues(disk_data)` — Use LLM to analyze disk issues when heuristics are insufficient
- `analyze_failed_action(action, error)` — Analyze failed cleanup action and suggest alternatives
- `analyze_complex_pattern(pattern_data)` — Analyze complex disk usage patterns that heuristics can't categorize
- `enhance_heuristics_with_llm(heuristic_suggestions, disk_data)` — Enhance heuristic suggestions with LLM insights

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `main` | `main()` | 1 | Test the LLM analyzer | [source](https://github.com/wronai/fixfedora/blob/main/fixos/providers/llm_analyzer.py#L326) |

### `fixos.providers.schemas` [source](https://github.com/wronai/fixfedora/blob/main/fixos/providers/schemas.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `CommandValidation` | 0 | Wynik walidacji komendy przez LLM. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/providers/schemas.py#L66) |
| `FixSuggestion` | 0 | Pojedyncza sugestia naprawy od LLM. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/providers/schemas.py#L21) |
| `LLMDiagnosticResponse` | 0 | Strukturalna odpowiedź LLM na dane diagnostyczne. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/providers/schemas.py#L41) |
| `NLPIntent` | 0 | Rozpoznana intencja z polecenia NLP. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/providers/schemas.py#L58) |
| `RiskLevel` | 0 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/providers/schemas.py#L15) |

### `fixos.system_checks` [source](https://github.com/wronai/fixfedora/blob/main/fixos/system_checks.py)

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `get_cpu_info` | `get_cpu_info()` | 2 | Metryki CPU. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/system_checks.py#L32) |
| `get_disk_info` | `get_disk_info()` | 3 | Metryki dysków dla wszystkich partycji. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/system_checks.py#L60) |
| `get_fedora_specific` | `get_fedora_specific()` | 1 | Komendy specyficzne dla system: dnf, journalctl, systemctl. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/system_checks.py#L107) |
| `get_full_diagnostics` | `get_full_diagnostics()` | 1 | Zbiera kompletne dane diagnostyczne systemu system. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/system_checks.py#L128) |
| `get_memory_info` | `get_memory_info()` | 1 | Metryki RAM i SWAP. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/system_checks.py#L45) |
| `get_network_info` | `get_network_info()` | 4 | Statystyki sieciowe (bez wrażliwych danych - anonimizacja jest osobno). | [source](https://github.com/wronai/fixfedora/blob/main/fixos/system_checks.py#L79) |
| `get_top_processes` | `get_top_processes(n)` | 3 | Lista TOP N procesów według zużycia CPU. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/system_checks.py#L95) |
| `run_cmd` | `run_cmd(cmd, timeout)` | 6 | Uruchamia komendę shell i zwraca output. Bezpieczny fallback przy błędzie. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/system_checks.py#L12) |

### `fixos.utils` [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/__init__.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `AnonymizationReport` | 2 | Raport anonimizacji – co zostało zmaskowane. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/anonymizer.py#L16) |
| `SessionTimeout` | 0 | Wyjątek rzucany po przekroczeniu limitu czasu sesji. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/timeout.py#L10) |
| `SearchResult` | 0 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/web_search.py#L19) |

**`AnonymizationReport` methods:**

- `add(category, count)`
- `summary()`

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `anonymize` | `anonymize(data_str)` | 15 ⚠️ | Anonimizuje wrażliwe dane. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/anonymizer.py#L51) |
| `display_anonymized_preview` | `display_anonymized_preview(data_str, report, max_lines)` | 5 | Wyświetla użytkownikowi zanonimizowane dane przed wysłaniem do LLM. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/anonymizer.py#L139) |
| `colorize` | `colorize(line)` | 1 | Return line unchanged – rich handles markup in render_md(). | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/terminal.py#L55) |
| `print_cmd_block` | `print_cmd_block(cmd, comment, dry_run)` | 4 | Print a framed command preview panel. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/terminal.py#L167) |
| `print_problem_header` | `print_problem_header(problem_id, description, severity, status, ...)` | 3 | Print a colored problem header panel. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/terminal.py#L231) |
| `print_stderr_box` | `print_stderr_box(stderr, max_lines)` | 2 | Print stderr in a rich Panel. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/terminal.py#L196) |
| `print_stdout_box` | `print_stdout_box(stdout, max_lines)` | 2 | Print stdout in a rich Panel. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/terminal.py#L183) |
| `render_md` | `render_md(text)` | 16 ⚠️ | Print LLM markdown reply to terminal via rich. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/terminal.py#L62) |
| `render_tree_colored` | `render_tree_colored(nodes, execution_order)` | 8 | Render a ProblemGraph as a rich-markup string. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/terminal.py#L258) |
| `timeout_handler` | `timeout_handler(signum, frame)` | 1 | Signal handler dla SIGALRM — rzuca SessionTimeout. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/timeout.py#L15) |
| `format_results_for_llm` | `format_results_for_llm(results)` | 3 | Formatuje wyniki wyszukiwania do wklejenia w prompt LLM. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/web_search.py#L245) |
| `search_all` | `search_all(query, serpapi_key, max_per_source)` | 5 | Przeszukuje wszystkie dostępne źródła wiedzy. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/web_search.py#L206) |
| `search_arch_wiki` | `search_arch_wiki(query, max_results)` | 9 | Arch Wiki – doskonałe źródło dla problemów Linux (nie tylko Arch). | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/web_search.py#L87) |
| `search_ask_fedora` | `search_ask_fedora(query, max_results)` | 4 | Szuka w Linux forums przez Discourse API. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/web_search.py#L65) |
| `search_ddg` | `search_ddg(query, max_results)` | 8 | DuckDuckGo Instant Answer API (bez klucza, ograniczone). | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/web_search.py#L174) |
| `search_fedora_bugzilla` | `search_fedora_bugzilla(query, max_results)` | 4 | Szuka w Linux Bugzilla przez REST API. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/web_search.py#L39) |
| `search_github_issues` | `search_github_issues(query, max_results)` | 4 | GitHub Issues – linuxhardware, ALSA, PipeWire, PulseAudio repos. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/web_search.py#L115) |
| `search_serpapi` | `search_serpapi(query, api_key, max_results)` | 5 | SerpAPI – Google/Bing search (wymaga klucza API). | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/web_search.py#L150) |

### `fixos.utils.anonymizer` [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/anonymizer.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `AnonymizationReport` | 2 | Raport anonimizacji – co zostało zmaskowane. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/anonymizer.py#L16) |

**`AnonymizationReport` methods:**

- `add(category, count)`
- `summary()`

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `anonymize` | `anonymize(data_str)` | 15 ⚠️ | Anonimizuje wrażliwe dane. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/anonymizer.py#L51) |
| `display_anonymized_preview` | `display_anonymized_preview(data_str, report, max_lines)` | 5 | Wyświetla użytkownikowi zanonimizowane dane przed wysłaniem do LLM. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/anonymizer.py#L139) |

### `fixos.utils.terminal` [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/terminal.py)

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `colorize` | `colorize(line)` | 1 | Return line unchanged – rich handles markup in render_md(). | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/terminal.py#L55) |
| `print_cmd_block` | `print_cmd_block(cmd, comment, dry_run)` | 4 | Print a framed command preview panel. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/terminal.py#L167) |
| `print_problem_header` | `print_problem_header(problem_id, description, severity, status, ...)` | 3 | Print a colored problem header panel. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/terminal.py#L231) |
| `print_stderr_box` | `print_stderr_box(stderr, max_lines)` | 2 | Print stderr in a rich Panel. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/terminal.py#L196) |
| `print_stdout_box` | `print_stdout_box(stdout, max_lines)` | 2 | Print stdout in a rich Panel. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/terminal.py#L183) |
| `render_md` | `render_md(text)` | 16 ⚠️ | Print LLM markdown reply to terminal via rich. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/terminal.py#L62) |
| `render_tree_colored` | `render_tree_colored(nodes, execution_order)` | 8 | Render a ProblemGraph as a rich-markup string. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/terminal.py#L258) |

### `fixos.utils.timeout` [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/timeout.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `SessionTimeout` | 0 | Wyjątek rzucany po przekroczeniu limitu czasu sesji. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/timeout.py#L10) |

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `timeout_handler` | `timeout_handler(signum, frame)` | 1 | Signal handler dla SIGALRM — rzuca SessionTimeout. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/timeout.py#L15) |

### `fixos.utils.web_search` [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/web_search.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `SearchResult` | 0 | — | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/web_search.py#L19) |

| Function | Signature | CC | Description | Source |
|----------|-----------|----|-----------  |--------|
| `format_results_for_llm` | `format_results_for_llm(results)` | 3 | Formatuje wyniki wyszukiwania do wklejenia w prompt LLM. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/web_search.py#L245) |
| `search_all` | `search_all(query, serpapi_key, max_per_source)` | 5 | Przeszukuje wszystkie dostępne źródła wiedzy. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/web_search.py#L206) |
| `search_arch_wiki` | `search_arch_wiki(query, max_results)` | 9 | Arch Wiki – doskonałe źródło dla problemów Linux (nie tylko Arch). | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/web_search.py#L87) |
| `search_ask_fedora` | `search_ask_fedora(query, max_results)` | 4 | Szuka w Linux forums przez Discourse API. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/web_search.py#L65) |
| `search_ddg` | `search_ddg(query, max_results)` | 8 | DuckDuckGo Instant Answer API (bez klucza, ograniczone). | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/web_search.py#L174) |
| `search_fedora_bugzilla` | `search_fedora_bugzilla(query, max_results)` | 4 | Szuka w Linux Bugzilla przez REST API. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/web_search.py#L39) |
| `search_github_issues` | `search_github_issues(query, max_results)` | 4 | GitHub Issues – linuxhardware, ALSA, PipeWire, PulseAudio repos. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/web_search.py#L115) |
| `search_serpapi` | `search_serpapi(query, api_key, max_results)` | 5 | SerpAPI – Google/Bing search (wymaga klucza API). | [source](https://github.com/wronai/fixfedora/blob/main/fixos/utils/web_search.py#L150) |

### `fixos.watch` [source](https://github.com/wronai/fixfedora/blob/main/fixos/watch.py)

| Class | Methods | Description | Source |
|-------|---------|-------------|--------|
| `WatchDaemon` | 2 | Daemon wykonujący cykliczną diagnostykę z powiadomieniami. | [source](https://github.com/wronai/fixfedora/blob/main/fixos/watch.py#L22) |

**`WatchDaemon` methods:**

- `run()` — Główna pętla monitorowania.
- `stop()` — Zatrzymaj daemon.
