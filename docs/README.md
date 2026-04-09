<!-- code2docs:start --># fixOS

![version](https://img.shields.io/badge/version-0.1.0-blue) ![python](https://img.shields.io/badge/python-%3E%3D3.10-blue) ![coverage](https://img.shields.io/badge/coverage-unknown-lightgrey) ![functions](https://img.shields.io/badge/functions-485-green)
> **485** functions | **70** classes | **91** files | CC̄ = 5.3

> Auto-generated project documentation from source code analysis.

**Author:** fixos contributors  
**License:** Apache-2.0[(LICENSE)](./LICENSE)  
**Repository:** [https://github.com/wronai/fixfedora](https://github.com/wronai/fixfedora)

## Installation

### From PyPI

```bash
pip install fixOS
```

### From Source

```bash
git clone https://github.com/wronai/fixfedora
cd fixOS
pip install -e .
```

### Optional Extras

```bash
pip install fixOS[dev]    # development tools
```

## Quick Start

### CLI Usage

```bash
# Generate full documentation for your project
fixOS ./my-project

# Only regenerate README
fixOS ./my-project --readme-only

# Preview what would be generated (no file writes)
fixOS ./my-project --dry-run

# Check documentation health
fixOS check ./my-project

# Sync — regenerate only changed modules
fixOS sync ./my-project
```

### Python API

```python
from fixOS import generate_readme, generate_docs, Code2DocsConfig

# Quick: generate README
generate_readme("./my-project")

# Full: generate all documentation
config = Code2DocsConfig(project_name="mylib", verbose=True)
docs = generate_docs("./my-project", config=config)
```

## Generated Output

When you run `fixOS`, the following files are produced:

```
<project>/
├── README.md                 # Main project README (auto-generated sections)
├── docs/
│   ├── api.md               # Consolidated API reference
│   ├── modules.md           # Module documentation with metrics
│   ├── architecture.md      # Architecture overview with diagrams
│   ├── dependency-graph.md  # Module dependency graphs
│   ├── coverage.md          # Docstring coverage report
│   ├── getting-started.md   # Getting started guide
│   ├── configuration.md    # Configuration reference
│   └── api-changelog.md    # API change tracking
├── examples/
│   ├── quickstart.py       # Basic usage examples
│   └── advanced_usage.py   # Advanced usage examples
├── CONTRIBUTING.md         # Contribution guidelines
└── mkdocs.yml             # MkDocs site configuration
```

## Configuration

Create `fixOS.yaml` in your project root (or run `fixOS init`):

```yaml
project:
  name: my-project
  source: ./
  output: ./docs/

readme:
  sections:
    - overview
    - install
    - quickstart
    - api
    - structure
  badges:
    - version
    - python
    - coverage
  sync_markers: true

docs:
  api_reference: true
  module_docs: true
  architecture: true
  changelog: true

examples:
  auto_generate: true
  from_entry_points: true

sync:
  strategy: markers    # markers | full | git-diff
  watch: false
  ignore:
    - "tests/"
    - "__pycache__"
```

## Sync Markers

fixOS can update only specific sections of an existing README using HTML comment markers:

```markdown
<!-- fixOS:start -->
# Project Title
... auto-generated content ...
<!-- fixOS:end -->
```

Content outside the markers is preserved when regenerating. Enable this with `sync_markers: true` in your configuration.

## Architecture

```
fixOS/
├── project        ├── advanced_usage        ├── quickstart    ├── cli/    ├── watch├── setup├── fixos/    ├── platform_utils    ├── system_checks    ├── anonymizer        ├── system_checks    ├── llm_shell    ├── diagnostics/    ├── config_interactive        ├── disk_analyzer        ├── service_cleanup    ├── config        ├── service_details        ├── dev_project_analyzer            ├── resources            ├── system_core            ├── audio            ├── security        ├── checks/            ├── hardware            ├── _shared            ├── thumbnails        ├── hitl        ├── autonomous    ├── agent/        ├── flatpak_analyzer        ├── session_handlers        ├── storage_analyzer        ├── service_scanner        ├── session_core        ├── hitl_session        ├── catalog        ├── session_io        ├── autonomous_session        ├── renderer        ├── profiles        ├── profile_cmd    ├── features/        ├── auditor        ├── installer        ├── quickfix_cmd        ├── report_cmd        ├── orchestrate_cmd        ├── scan_cmd        ├── rollback_cmd        ├── ask_cmd        ├── history_cmd        ├── provider_cmd        ├── watch_cmd        ├── main        ├── token_cmd        ├── features_cmd        ├── config_cmd        ├── fix_cmd        ├── registry    ├── plugins/        ├── base            ├── resources        ├── cleanup_cmd        ├── builtin/            ├── audio            ├── security            ├── thumbnails            ├── disk        ├── shared        ├── llm    ├── providers/    ├── utils/        ├── llm_analyzer        ├── timeout        ├── anonymizer        ├── web_search    ├── fixes/    ├── orchestrator/            ├── hardware        ├── terminal        ├── executor        ├── orchestrator        ├── cleanup_planner    ├── interactive/        ├── graph    ├── profiles/    ├── pyqual-calibrate        ├── rollback        ├── schemas```

## API Overview

### Classes

- **`WatchDaemon`** — Daemon wykonujący cykliczną diagnostykę z powiadomieniami.
- **`DiskAnalyzer`** — Analyzes disk usage and provides cleanup suggestions
- **`ServiceCleaner`** — Plans and executes cleanup of service data.
- **`FixOsConfig`** — —
- **`ServiceDetailsProvider`** — Provides detailed information about service data.
- **`ProjectDependency`** — Represents a dependency folder that can be cleaned
- **`DevProjectAnalyzer`** — Analyze developer projects for dependency folders that can be cleaned.
- **`FlatpakItemType`** — —
- **`FlatpakItemInfo`** — Detailed info about a Flatpak item (app, runtime, or data)
- **`FlatpakAnalyzer`** — Advanced analyzer for Flatpak cleanup decisions
- **`StorageItem`** — Represents a storage item that can be cleaned
- **`StorageAnalyzer`** — Comprehensive storage analyzer for Linux systems.
- **`ServiceType`** — Service types that can be scanned and cleaned.
- **`ServiceDataInfo`** — Information about service data.
- **`ServiceDataScanner`** — Scans for large service data directories and allows cleanup.
- **`CmdResult`** — Result of executed command.
- **`HITLSession`** — Interactive Human-in-the-Loop diagnostic and repair session.
- **`PackageInfo`** — Information about a single package.
- **`PackageCategory`** — A category of packages (e.g., core_utils, dev_tools).
- **`PackageCatalog`** — Manages the package database.
- **`FixAction`** — —
- **`AgentReport`** — —
- **`AutonomousSession`** — Self-directed autonomous diagnostic and repair session.
- **`FeatureRenderer`** — Renders audit results for terminal display.
- **`UserProfile`** — A user profile defining what packages/features they want.
- **`SystemInfo`** — Complete system information snapshot.
- **`SystemDetector`** — Detects system parameters.
- **`AuditResult`** — Result of feature audit - what's installed, what's missing.
- **`FeatureAuditor`** — Compares installed packages with profile requirements.
- **`FeatureInstaller`** — Safely installs packages using native package manager or other backends.
- **`PluginRegistry`** — Registry for diagnostic plugins with autodiscovery.
- **`Severity`** — Severity level for diagnostic findings.
- **`Finding`** — Single finding from a diagnostic plugin.
- **`DiagnosticResult`** — Result of a diagnostic plugin run.
- **`DiagnosticPlugin`** — Bazowa klasa dla pluginów diagnostycznych fixOS.
- **`Plugin`** — —
- **`Plugin`** — —
- **`Plugin`** — —
- **`Plugin`** — —
- **`Plugin`** — —
- **`NaturalLanguageGroup`** — Click group that routes unknown commands to 'ask' command.
- **`LLMError`** — Błąd komunikacji z LLM.
- **`LLMClient`** — Wrapper nad openai.OpenAI kompatybilny z wieloma providerami.
- **`LLMAnalysis`** — Result of LLM analysis
- **`LLMAnalyzer`** — Uses LLM to analyze disk issues when heuristics aren't sufficient
- **`SessionTimeout`** — Wyjątek rzucany po przekroczeniu limitu czasu sesji.
- **`AnonymizationReport`** — Raport anonimizacji – co zostało zmaskowane.
- **`SearchResult`** — —
- **`Plugin`** — —
- **`DangerousCommandError`** — —
- **`CommandTimeoutError`** — —
- **`ExecutionResult`** — —
- **`CommandExecutor`** — Bezpieczny executor komend z:
- **`FixOrchestrator`** — Orkiestrator napraw systemowych.
- **`Priority`** — —
- **`CleanupType`** — —
- **`CleanupAction`** — Represents a cleanup action
- **`CleanupPlanner`** — Interactive cleanup planning and grouping system
- **`Problem`** — —
- **`ProblemGraph`** — DAG problemów systemowych z topological sort do wyznaczania kolejności napraw.
- **`Profile`** — Profil diagnostyczny z zestawem modułów i progów.
- **`RollbackEntry`** — Single recorded operation with its rollback command.
- **`RollbackSession`** — A session of recorded operations that can be rolled back.
- **`RiskLevel`** — —
- **`FixSuggestion`** — Pojedyncza sugestia naprawy od LLM.
- **`LLMDiagnosticResponse`** — Strukturalna odpowiedź LLM na dane diagnostyczne.
- **`NLPIntent`** — Rozpoznana intencja z polecenia NLP.
- **`CommandValidation`** — Wynik walidacji komendy przez LLM.

### Functions

- `run_autonomous_session()` — —
- `get_os_info()` — Returns basic OS information.
- `needs_elevation(cmd)` — Returns True if command likely needs admin/sudo.
- `elevate_cmd(cmd)` — Adds sudo (Linux/Mac) or wraps in PowerShell -Verb RunAs (Windows).
- `is_dangerous(cmd)` — Returns reason string if command is dangerous, None if safe.
- `run_command(cmd, timeout, shell)` — Runs a command cross-platform.
- `get_package_manager()` — Detects the system package manager.
- `install_package_cmd(package)` — Returns the install command for the detected package manager.
- `setup_signal_timeout(seconds, handler)` — Sets up a timeout signal. Returns True if supported (POSIX only).
- `cancel_signal_timeout()` — Cancels the timeout signal (POSIX only).
- `run_cmd(cmd, timeout)` — Uruchamia komendę shell i zwraca output. Bezpieczny fallback przy błędzie.
- `get_cpu_info()` — Metryki CPU.
- `get_memory_info()` — Metryki RAM i SWAP.
- `get_disk_info()` — Metryki dysków dla wszystkich partycji.
- `get_network_info()` — Statystyki sieciowe (bez wrażliwych danych - anonimizacja jest osobno).
- `get_top_processes(n)` — Lista TOP N procesów według zużycia CPU.
- `get_fedora_specific()` — Komendy specyficzne dla system: dnf, journalctl, systemctl.
- `get_full_diagnostics()` — Zbiera kompletne dane diagnostyczne systemu system.
- `get_sensitive_values()` — Zbiera aktualne wrażliwe wartości systemowe do zamaskowania.
- `anonymize(data_str)` — Anonimizuje wrażliwe dane w stringu.
- `get_full_diagnostics(modules, progress_callback)` — Zbiera diagnostykę z wybranych modułów.
- `format_time(seconds)` — —
- `execute_command(cmd)` — Wykonuje komendę systemową z potwierdzeniem użytkownika.
- `run_llm_shell(diagnostics_data, token, model, timeout)` — Uruchamia interaktywny shell LLM z przekazanymi danymi diagnostycznymi.
- `interactive_provider_setup()` — Interaktywny wybór providera gdy brak konfiguracji.
- `main()` — Test the disk analyzer
- `detect_provider_from_key(key)` — Wykrywa provider na podstawie prefiksu klucza API.
- `interactive_provider_setup()` — Interaktywny wybór providera gdy brak konfiguracji.
- `get_providers_list()` — Zwraca listę providerów jako listę słowników.
- `diagnose_resources()` — Diagnostyka zasobów systemowych.
- `diagnose_system()` — System metrics – cross-platform: CPU, RAM, disks, processes.
- `diagnose_audio()` — Diagnostyka dźwięku (ALSA/PipeWire/PulseAudio/SOF).
- `diagnose_security()` — Diagnostyka bezpieczeństwa systemu i sieci.
- `diagnose_hardware()` — Diagnostyka sprzętu laptopa/desktopa (ACPI, kamera, touchpad, DMI).
- `diagnose_thumbnails()` — Diagnostyka podglądów plików (thumbnails) w system.
- `run_hitl_session(diagnostics, config, show_data)` — Run interactive HITL session with full transparency.
- `run_autonomous_session(diagnostics, config, show_data, max_fixes)` — Uruchamia autonomiczny tryb agenta.
- `get_remaining_time(session)` — Calculate remaining session time in seconds.
- `analyze_flatpak_for_cleanup()` — Convenience function to run full Flatpak analysis
- `handle_quit()` — Handle [Q] Quit command. Returns False to exit loop.
- `handle_skip_all(messages)` — Handle [S] Skip all command.
- `handle_describe_problem(messages, ask_fn)` — Handle [D] Describe own problem command.
- `handle_execute_all(fixes, messages, executed, run_cmd_fn)` — Handle [A] Execute all commands.
- `handle_fix_by_number(user_in, fixes, messages, executed)` — Handle [N] Execute specific fix by number.
- `handle_direct_command(user_in, messages, executed, run_cmd_fn)` — Handle [!cmd] Direct command execution.
- `handle_search(user_in, messages, serpapi_key)` — Handle [search <q>] Web search command.
- `handle_free_text(user_in, messages)` — Handle free text input → send to LLM.
- `run_single_command(cmd, comment)` — Run a command with full transparency and safety checks.
- `parse_user_input(user_in, fixes, messages, executed)` — Parse user input and execute appropriate handler.
- `main()` — Test the service data scanner.
- `extract_fixes(reply)` — Extract (command, comment) pairs from LLM reply.
- `extract_search_topic(llm_reply)` — Extract search keywords from LLM reply.
- `run_hitl_session(diagnostics, config, show_data)` — Run interactive HITL session (backward compatible wrapper).
- `print_session_header(os_info, pkg_manager, model, timeout)` — Print session header with system info.
- `fmt_time(s)` — Format seconds as HH:MM:SS.
- `print_action_menu(fixes, remaining, total_tokens)` — Print the interactive numbered action menu.
- `ask_user_problem()` — Interactively asks the user to describe their problem.
- `print_cmd_preview(cmd, comment)` — Shows command in a clear block before execution.
- `print_cmd_result(result)` — Shows command result with colorized markdown.
- `print_session_summary(messages_count, elapsed, total_tokens, executed)` — Print session summary.
- `print_thinking()` — Print 'Analyzing...' indicator.
- `clear_thinking()` — Clear the 'Analyzing...' indicator.
- `print_llm_reply(reply)` — Render LLM reply with markdown formatting.
- `print_llm_error(e)` — Print LLM error message.
- `print_blocked_command(cmd, reason)` — Print blocked dangerous command warning.
- `print_timeout()` — Print session timeout message.
- `print_session_ended()` — Print session ended message.
- `print_session_interrupted()` — Print session interrupted message.
- `print_executing_all(count)` — Print executing all commands message.
- `print_no_commands()` — Print no commands available message.
- `print_invalid_option(user_in, max_option)` — Print invalid option message.
- `print_no_results()` — Print no search results message.
- `print_searching()` — Print searching message.
- `ask_execute_prompt()` — Ask user if they want to execute a command.
- `ask_low_confidence_search()` — Ask user if they want to search when LLM is uncertain.
- `ask_send_data()` — Ask user if they want to send data to LLM.
- `get_user_input(remaining)` — Get user input with prompt.
- `run_autonomous_session(diagnostics, config, show_data, max_fixes)` — Run autonomous session (backward compatible wrapper).
- `profile()` — Zarządzanie profilami diagnostycznymi.
- `profile_list()` — Pokaż dostępne profile diagnostyczne.
- `profile_show(name)` — Pokaż szczegóły profilu diagnostycznego.
- `quickfix(dry_run, modules)` — Natychmiastowe naprawy bez API — baza znanych bugów.
- `report(output_format, output, modules, profile)` — Eksport wyników diagnostyki do raportu HTML/Markdown/JSON.
- `orchestrate(provider, token, model, no_banner)` — Zaawansowana orkiestracja napraw z grafem problemów.
- `scan(modules, output, show_raw, no_banner)` — Przeprowadza diagnostykę systemu.
- `rollback()` — Zarządzanie cofaniem operacji fixOS.
- `rollback_list(limit)` — Pokaż historię sesji naprawczych.
- `rollback_show(session_id)` — Pokaż szczegóły sesji rollback.
- `rollback_undo(session_id, last, dry_run)` — Cofnij operacje z podanej sesji.
- `ask(prompt, dry_run)` — Wykonaj polecenie w języku naturalnym.
- `history(limit, json_output)` — Historia napraw fixOS.
- `llm_providers(free)` — Lista dostępnych providerów LLM.
- `providers()` — Lista providerów LLM z oznaczeniem FREE/PAID.
- `test_llm(provider, token, model, no_banner)` — Test połączenia z LLM.
- `watch(interval, modules, alert_on, max_iterations)` — Monitorowanie systemu w tle z powiadomieniami.
- `cli(ctx, dry_run, version)` — fixos – AI-powered diagnostyka i naprawa Linux, Windows, macOS.
- `main()` — Entry point for fixOS CLI.
- `token()` — Zarządzanie tokenem API.
- `token_set(key, provider, env_file)` — Zapisz token API do pliku .env.
- `token_show()` — Pokaż obecny token (masked).
- `token_clear(env_file)` — Usuń token z pliku .env.
- `features()` — Zarządzanie pakietami komfortu systemu.
- `features_audit(profile, json_output)` — Sprawdź brakujące pakiety dla profilu.
- `features_install(profile, dry_run, yes, category)` — Zainstaluj brakujące pakiety dla profilu.
- `features_profiles()` — Lista dostępnych profili.
- `features_system()` — Pokaż wykryty system.
- `config()` — Zarządzanie konfiguracją fixOS.
- `config_show()` — Pokaż aktualną konfigurację.
- `config_init(force)` — Zainicjalizuj plik konfiguracyjny .env.
- `config_set(key, value)` — Ustaw wartość konfiguracyjną w .env.
- `fix(provider, token, model, no_banner)` — Przeprowadza pełną diagnostykę i uruchamia sesję naprawczą z LLM.
- `handle_disk_cleanup_mode(disk_analysis, cfg, dry_run, interactive)` — Handle disk cleanup mode with interactive planning
- `execute_cleanup_actions(actions, cfg, llm_fallback)` — Execute cleanup actions with safety checks
- `try_llm_fallback_for_failures(failed_actions, cfg)` — Try to fix failed actions using LLM
- `cleanup_services(threshold, services, json_output, cleanup)` — Skanuje i czyści dane usług przekraczające próg.
- `add_common_options(fn)` — Decorator adding common LLM options to a Click command.
- `add_shared_options(func)` — Shared options for both scan and fix commands.
- `main()` — Test the LLM analyzer
- `timeout_handler(signum, frame)` — Signal handler dla SIGALRM — rzuca SessionTimeout.
- `anonymize(data_str)` — Anonimizuje wrażliwe dane.
- `display_anonymized_preview(data_str, report, max_lines)` — Wyświetla użytkownikowi zanonimizowane dane przed wysłaniem do LLM.
- `search_fedora_bugzilla(query, max_results)` — Szuka w Linux Bugzilla przez REST API.
- `search_ask_fedora(query, max_results)` — Szuka w Linux forums przez Discourse API.
- `search_arch_wiki(query, max_results)` — Arch Wiki – doskonałe źródło dla problemów Linux (nie tylko Arch).
- `search_github_issues(query, max_results)` — GitHub Issues – linuxhardware, ALSA, PipeWire, PulseAudio repos.
- `search_serpapi(query, api_key, max_results)` — SerpAPI – Google/Bing search (wymaga klucza API).
- `search_ddg(query, max_results)` — DuckDuckGo Instant Answer API (bez klucza, ograniczone).
- `search_all(query, serpapi_key, max_per_source)` — Przeszukuje wszystkie dostępne źródła wiedzy.
- `format_results_for_llm(results)` — Formatuje wyniki wyszukiwania do wklejenia w prompt LLM.
- `colorize(line)` — Return line unchanged – rich handles markup in render_md().
- `render_md(text)` — Print LLM markdown reply to terminal via rich.
- `print_cmd_block(cmd, comment, dry_run)` — Print a framed command preview panel.
- `print_stdout_box(stdout, max_lines)` — Print stdout in a rich Panel.
- `print_stderr_box(stderr, max_lines)` — Print stderr in a rich Panel.
- `print_problem_header(problem_id, description, severity, status)` — Print a colored problem header panel.
- `render_tree_colored(nodes, execution_order)` — Render a ProblemGraph as a rich-markup string.
- `main()` — Test the cleanup planner
- `read_last_metrics_from_db(workdir)` — Czyta ostatnie metryki z pipeline.db pyqual.
- `parse_pyqual_yaml(config_path)` — Odczytuje zawartość pyqual.yaml.
- `update_metric(content, metric_name, new_value)` — Aktualizuje wartość metryki w YAML.
- `calculate_new_threshold(actual_value, current_threshold, margin_percent, is_upper_limit)` — Wylicza nowy próg z marginesem.
- `extract_current_metrics(content)` — Wyciąga aktualne progi z YAML.
- `calibrate(workdir, margin, dry_run, force)` — Główna funkcja kalibracji.
- `main()` — —


## Project Structure

📄 `docs.examples.advanced_usage`
📄 `docs.examples.quickstart` (1 functions)
📦 `fixos`
📦 `fixos.agent` (1 functions)
📄 `fixos.agent.autonomous` (1 functions)
📄 `fixos.agent.autonomous_session` (22 functions, 3 classes)
📄 `fixos.agent.hitl` (1 functions)
📄 `fixos.agent.hitl_session` (12 functions, 1 classes)
📄 `fixos.agent.session_core` (2 functions, 1 classes)
📄 `fixos.agent.session_handlers` (10 functions)
📄 `fixos.agent.session_io` (24 functions)
📄 `fixos.anonymizer` (2 functions)
📦 `fixos.cli`
📄 `fixos.cli.ask_cmd` (8 functions)
📄 `fixos.cli.cleanup_cmd` (14 functions)
📄 `fixos.cli.config_cmd` (4 functions)
📄 `fixos.cli.features_cmd` (6 functions)
📄 `fixos.cli.fix_cmd` (4 functions)
📄 `fixos.cli.history_cmd` (1 functions)
📄 `fixos.cli.main` (3 functions)
📄 `fixos.cli.orchestrate_cmd` (1 functions)
📄 `fixos.cli.profile_cmd` (3 functions)
📄 `fixos.cli.provider_cmd` (3 functions)
📄 `fixos.cli.quickfix_cmd` (1 functions)
📄 `fixos.cli.report_cmd` (1 functions)
📄 `fixos.cli.rollback_cmd` (4 functions)
📄 `fixos.cli.scan_cmd` (3 functions)
📄 `fixos.cli.shared` (3 functions, 1 classes)
📄 `fixos.cli.token_cmd` (4 functions)
📄 `fixos.cli.watch_cmd` (1 functions)
📄 `fixos.config` (7 functions, 1 classes)
📄 `fixos.config_interactive` (5 functions)
📦 `fixos.diagnostics`
📦 `fixos.diagnostics.checks`
📄 `fixos.diagnostics.checks._shared` (2 functions)
📄 `fixos.diagnostics.checks.audio` (1 functions)
📄 `fixos.diagnostics.checks.hardware` (1 functions)
📄 `fixos.diagnostics.checks.resources` (1 functions)
📄 `fixos.diagnostics.checks.security` (1 functions)
📄 `fixos.diagnostics.checks.system_core` (1 functions)
📄 `fixos.diagnostics.checks.thumbnails` (1 functions)
📄 `fixos.diagnostics.dev_project_analyzer` (13 functions, 2 classes)
📄 `fixos.diagnostics.disk_analyzer` (15 functions, 1 classes)
📄 `fixos.diagnostics.flatpak_analyzer` (24 functions, 3 classes)
📄 `fixos.diagnostics.service_cleanup` (10 functions, 1 classes)
📄 `fixos.diagnostics.service_details` (7 functions, 1 classes)
📄 `fixos.diagnostics.service_scanner` (8 functions, 3 classes)
📄 `fixos.diagnostics.storage_analyzer` (32 functions, 2 classes)
📄 `fixos.diagnostics.system_checks` (1 functions)
📦 `fixos.features` (12 functions, 2 classes)
📄 `fixos.features.auditor` (5 functions, 2 classes)
📄 `fixos.features.catalog` (7 functions, 3 classes)
📄 `fixos.features.installer` (11 functions, 1 classes)
📄 `fixos.features.profiles` (4 functions, 1 classes)
📄 `fixos.features.renderer` (4 functions, 1 classes)
📦 `fixos.fixes`
📦 `fixos.interactive`
📄 `fixos.interactive.cleanup_planner` (12 functions, 4 classes)
📄 `fixos.llm_shell` (4 functions)
📦 `fixos.orchestrator`
📄 `fixos.orchestrator.executor` (11 functions, 4 classes)
📄 `fixos.orchestrator.graph` (11 functions, 2 classes)
📄 `fixos.orchestrator.orchestrator` (11 functions, 2 classes)
📄 `fixos.orchestrator.rollback` (6 functions, 2 classes)
📄 `fixos.platform_utils` (10 functions)
📦 `fixos.plugins`
📄 `fixos.plugins.base` (4 functions, 4 classes)
📦 `fixos.plugins.builtin`
📄 `fixos.plugins.builtin.audio` (5 functions, 1 classes)
📄 `fixos.plugins.builtin.disk` (4 functions, 1 classes)
📄 `fixos.plugins.builtin.hardware` (6 functions, 1 classes)
📄 `fixos.plugins.builtin.resources` (6 functions, 1 classes)
📄 `fixos.plugins.builtin.security` (6 functions, 1 classes)
📄 `fixos.plugins.builtin.thumbnails` (5 functions, 1 classes)
📄 `fixos.plugins.registry` (8 functions, 1 classes)
📦 `fixos.profiles` (3 functions, 1 classes)
📦 `fixos.providers`
📄 `fixos.providers.llm` (6 functions, 2 classes)
📄 `fixos.providers.llm_analyzer` (8 functions, 2 classes)
📄 `fixos.providers.schemas` (5 classes)
📄 `fixos.system_checks` (8 functions)
📦 `fixos.utils`
📄 `fixos.utils.anonymizer` (9 functions, 1 classes)
📄 `fixos.utils.terminal` (8 functions, 1 classes)
📄 `fixos.utils.timeout` (1 functions, 1 classes)
📄 `fixos.utils.web_search` (9 functions, 1 classes)
📄 `fixos.watch` (5 functions, 1 classes)
📄 `project`
📄 `scripts.pyqual-calibrate` (7 functions)
📄 `setup`

## Requirements

- Python >= >=3.10
- openai >=1.35.0- prompt_toolkit >=3.0.43- psutil >=5.9.0- pyyaml >=6.0- click >=8.1.0- python-dotenv >=1.0.0- rich >=13.0

## Contributing

**Contributors:**
- Tom Sapletta

We welcome contributions! Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/wronai/fixfedora
cd fixOS

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest
```

## Documentation

- 📖 [Full Documentation](https://github.com/wronai/fixfedora/tree/main/docs) — API reference, module docs, architecture
- 🚀 [Getting Started](https://github.com/wronai/fixfedora/blob/main/docs/getting-started.md) — Quick start guide
- 📚 [API Reference](https://github.com/wronai/fixfedora/blob/main/docs/api.md) — Complete API documentation
- 🔧 [Configuration](https://github.com/wronai/fixfedora/blob/main/docs/configuration.md) — Configuration options
- 💡 [Examples](./examples) — Usage examples and code samples

### Generated Files

| Output | Description | Link |
|--------|-------------|------|
| `README.md` | Project overview (this file) | — |
| `docs/api.md` | Consolidated API reference | [View](./docs/api.md) |
| `docs/modules.md` | Module reference with metrics | [View](./docs/modules.md) |
| `docs/architecture.md` | Architecture with diagrams | [View](./docs/architecture.md) |
| `docs/dependency-graph.md` | Dependency graphs | [View](./docs/dependency-graph.md) |
| `docs/coverage.md` | Docstring coverage report | [View](./docs/coverage.md) |
| `docs/getting-started.md` | Getting started guide | [View](./docs/getting-started.md) |
| `docs/configuration.md` | Configuration reference | [View](./docs/configuration.md) |
| `docs/api-changelog.md` | API change tracking | [View](./docs/api-changelog.md) |
| `CONTRIBUTING.md` | Contribution guidelines | [View](./CONTRIBUTING.md) |
| `examples/` | Usage examples | [Browse](./examples) |
| `mkdocs.yml` | MkDocs configuration | — |

<!-- code2docs:end -->