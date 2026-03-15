<!-- code2docs:start --># fixOS

![version](https://img.shields.io/badge/version-0.1.0-blue) ![python](https://img.shields.io/badge/python-%3E%3D3.10-blue) ![coverage](https://img.shields.io/badge/coverage-unknown-lightgrey) ![functions](https://img.shields.io/badge/functions-291-green)
> **291** functions | **52** classes | **48** files | CC̄ = 5.7

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
├── setup    ├── watch    ├── platform_utils├── fixos/    ├── anonymizer    ├── system_checks    ├── llm_shell        ├── system_checks    ├── diagnostics/    ├── cli        ├── disk_analyzer    ├── config        ├── autonomous    ├── agent/        ├── flatpak_analyzer        ├── registry    ├── plugins/        ├── llm        ├── llm_analyzer        ├── base    ├── providers/    ├── utils/        ├── service_scanner        ├── timeout        ├── web_search        ├── anonymizer    ├── fixes/    ├── orchestrator/        ├── hitl        ├── terminal        ├── orchestrator        ├── graph        ├── cleanup_planner    ├── interactive/    ├── profiles/            ├── resources            ├── audio        ├── rollback        ├── builtin/            ├── security            ├── hardware            ├── disk        ├── quickstart        ├── advanced_usage├── project            ├── thumbnails        ├── executor        ├── schemas```

## API Overview

### Classes

- **`WatchDaemon`** — Daemon wykonujący cykliczną diagnostykę z powiadomieniami.
- **`NaturalLanguageGroup`** — —
- **`DiskAnalyzer`** — Analyzes disk usage and provides cleanup suggestions
- **`FixOsConfig`** — —
- **`FixAction`** — —
- **`AgentReport`** — —
- **`FlatpakItemType`** — —
- **`FlatpakItemInfo`** — Detailed info about a Flatpak item (app, runtime, or data)
- **`FlatpakAnalyzer`** — Advanced analyzer for Flatpak cleanup decisions
- **`PluginRegistry`** — Registry for diagnostic plugins with autodiscovery.
- **`LLMError`** — Błąd komunikacji z LLM.
- **`LLMClient`** — Wrapper nad openai.OpenAI kompatybilny z wieloma providerami.
- **`LLMAnalysis`** — Result of LLM analysis
- **`LLMAnalyzer`** — Uses LLM to analyze disk issues when heuristics aren't sufficient
- **`Severity`** — Severity level for diagnostic findings.
- **`Finding`** — Single finding from a diagnostic plugin.
- **`DiagnosticResult`** — Result of a diagnostic plugin run.
- **`DiagnosticPlugin`** — Bazowa klasa dla pluginów diagnostycznych fixOS.
- **`ServiceType`** — —
- **`ServiceDataInfo`** — Information about service data
- **`ServiceDataScanner`** — Scans for large service data directories and allows cleanup
- **`SessionTimeout`** — Wyjątek rzucany po przekroczeniu limitu czasu sesji.
- **`SearchResult`** — —
- **`AnonymizationReport`** — Raport anonimizacji – co zostało zmaskowane.
- **`CmdResult`** — —
- **`FixOrchestrator`** — Orkiestrator napraw systemowych.
- **`Problem`** — —
- **`ProblemGraph`** — DAG problemów systemowych z topological sort do wyznaczania kolejności napraw.
- **`Priority`** — —
- **`CleanupType`** — —
- **`CleanupAction`** — Represents a cleanup action
- **`CleanupPlanner`** — Interactive cleanup planning and grouping system
- **`Profile`** — Profil diagnostyczny z zestawem modułów i progów.
- **`Plugin`** — —
- **`Plugin`** — —
- **`RollbackEntry`** — Single recorded operation with its rollback command.
- **`RollbackSession`** — A session of recorded operations that can be rolled back.
- **`Plugin`** — —
- **`Plugin`** — —
- **`Plugin`** — —
- **`Plugin`** — —
- **`DangerousCommandError`** — —
- **`CommandTimeoutError`** — —
- **`ExecutionResult`** — —
- **`CommandExecutor`** — Bezpieczny executor komend z:
- **`RiskLevel`** — —
- **`FixSuggestion`** — Pojedyncza sugestia naprawy od LLM.
- **`LLMDiagnosticResponse`** — Strukturalna odpowiedź LLM na dane diagnostyczne.
- **`NLPIntent`** — Rozpoznana intencja z polecenia NLP.
- **`CommandValidation`** — Wynik walidacji komendy przez LLM.

### Functions

- `get_os_info()` — Returns basic OS information.
- `needs_elevation(cmd)` — Returns True if command likely needs admin/sudo.
- `elevate_cmd(cmd)` — Adds sudo (Linux/Mac) or wraps in PowerShell -Verb RunAs (Windows).
- `is_dangerous(cmd)` — Returns reason string if command is dangerous, None if safe.
- `run_command(cmd, timeout, shell)` — Runs a command cross-platform.
- `get_package_manager()` — Detects the system package manager.
- `install_package_cmd(package)` — Returns the install command for the detected package manager.
- `setup_signal_timeout(seconds, handler)` — Sets up a timeout signal. Returns True if supported (POSIX only).
- `cancel_signal_timeout()` — Cancels the timeout signal (POSIX only).
- `get_sensitive_values()` — Zbiera aktualne wrażliwe wartości systemowe do zamaskowania.
- `anonymize(data_str)` — Anonimizuje wrażliwe dane w stringu.
- `run_cmd(cmd, timeout)` — Uruchamia komendę shell i zwraca output. Bezpieczny fallback przy błędzie.
- `get_cpu_info()` — Metryki CPU.
- `get_memory_info()` — Metryki RAM i SWAP.
- `get_disk_info()` — Metryki dysków dla wszystkich partycji.
- `get_network_info()` — Statystyki sieciowe (bez wrażliwych danych - anonimizacja jest osobno).
- `get_top_processes(n)` — Lista TOP N procesów według zużycia CPU.
- `get_fedora_specific()` — Komendy specyficzne dla system: dnf, journalctl, systemctl.
- `get_full_diagnostics()` — Zbiera kompletne dane diagnostyczne systemu system.
- `format_time(seconds)` — —
- `execute_command(cmd)` — Wykonuje komendę systemową z potwierdzeniem użytkownika.
- `run_llm_shell(diagnostics_data, token, model, timeout)` — Uruchamia interaktywny shell LLM z przekazanymi danymi diagnostycznymi.
- `diagnose_audio()` — Diagnostyka dźwięku (ALSA/PipeWire/PulseAudio/SOF).
- `diagnose_thumbnails()` — Diagnostyka podglądów plików (thumbnails) w system.
- `diagnose_hardware()` — Diagnostyka sprzętu laptopa/desktopa (ACPI, kamera, touchpad, DMI).
- `diagnose_system()` — System metrics – cross-platform: CPU, RAM, disks, processes.
- `diagnose_security()` — Diagnostyka bezpieczeństwa systemu i sieci.
- `diagnose_resources()` — Diagnostyka zasobów systemowych.
- `get_full_diagnostics(modules, progress_callback)` — Zbiera diagnostykę z wybranych modułów.
- `add_common_options(fn)` — —
- `add_shared_options(func)` — Shared options for both scan and fix commands
- `cli(ctx, dry_run, version)` — fixos – AI-powered diagnostyka i naprawa Linux, Windows, macOS.
- `ask(prompt, dry_run)` — Wykonaj polecenie w języku naturalnym.
- `scan(modules, output, show_raw, no_banner)` — Przeprowadza diagnostykę systemu.
- `fix(provider, token, model, no_banner)` — Przeprowadza pełną diagnostykę i uruchamia sesję naprawczą z LLM.
- `handle_disk_cleanup_mode(disk_analysis, cfg, dry_run, interactive)` — Handle disk cleanup mode with interactive planning
- `execute_cleanup_actions(actions, cfg, llm_fallback)` — Execute cleanup actions with safety checks
- `try_llm_fallback_for_failures(failed_actions, cfg)` — Use LLM to analyze and suggest fixes for failed cleanup actions
- `token()` — Zarządzanie tokenami API LLM.
- `token_set(key, provider, env_file)` — Zapisuje token API do pliku .env.
- `token_show()` — Pokazuje aktualnie skonfigurowany token (zamaskowany).
- `token_clear(env_file)` — Usuwa token z pliku .env.
- `config()` — Zarządzanie konfiguracją fixos.
- `config_show()` — Wyświetla aktualną konfigurację.
- `config_init(force)` — Tworzy plik .env na podstawie szablonu .env.example.
- `config_set(key, value)` — Ustawia wartość w pliku .env.
- `llm_providers(free)` — Lista providerów LLM z linkami do generowania kluczy API.
- `providers()` — Lista dostępnych providerów LLM (skrócona). Użyj 'fixos llm' po więcej.
- `test_llm(provider, token, model, no_banner)` — Testuje połączenie z wybranym providerem LLM.
- `orchestrate(provider, token, model, no_banner)` — Orkiestracja napraw z grafem kaskadowych problemów.
- `cleanup_services(threshold, services, json_output, cleanup)` — Skanuje i czyści dane usług przekraczające próg.
- `rollback()` — Zarządzanie cofaniem operacji fixOS.
- `rollback_list(limit)` — Pokaż historię sesji naprawczych.
- `rollback_show(session_id)` — Pokaż szczegóły sesji rollback.
- `rollback_undo(session_id, last, dry_run)` — Cofnij operacje z podanej sesji.
- `watch(interval, modules, alert_on, max_iterations)` — Monitorowanie systemu w tle z powiadomieniami.
- `profile()` — Zarządzanie profilami diagnostycznymi.
- `profile_list()` — Pokaż dostępne profile diagnostyczne.
- `profile_show(name)` — Pokaż szczegóły profilu diagnostycznego.
- `quickfix(dry_run, modules)` — Natychmiastowe naprawy bez API — baza znanych bugów.
- `report(output_format, output, modules, profile)` — Eksport wyników diagnostyki do raportu HTML/Markdown/JSON.
- `history(limit, json_output)` — Historia napraw fixOS.
- `main()` — —
- `main()` — Test the disk analyzer
- `detect_provider_from_key(key)` — Wykrywa provider na podstawie prefiksu klucza API.
- `interactive_provider_setup()` — Interaktywny wybór providera gdy brak konfiguracji.
- `get_providers_list()` — Zwraca listę providerów jako listę słowników.
- `run_autonomous_session(diagnostics, config, show_data, max_fixes)` — Uruchamia autonomiczny tryb agenta.
- `analyze_flatpak_for_cleanup()` — Convenience function to run full Flatpak analysis
- `main()` — Test the LLM analyzer
- `main()` — Test the service data scanner
- `timeout_handler(signum, frame)` — Signal handler dla SIGALRM — rzuca SessionTimeout.
- `search_fedora_bugzilla(query, max_results)` — Szuka w Linux Bugzilla przez REST API.
- `search_ask_fedora(query, max_results)` — Szuka w Linux forums przez Discourse API.
- `search_arch_wiki(query, max_results)` — Arch Wiki – doskonałe źródło dla problemów Linux (nie tylko Arch).
- `search_github_issues(query, max_results)` — GitHub Issues – linuxhardware, ALSA, PipeWire, PulseAudio repos.
- `search_serpapi(query, api_key, max_results)` — SerpAPI – Google/Bing search (wymaga klucza API).
- `search_ddg(query, max_results)` — DuckDuckGo Instant Answer API (bez klucza, ograniczone).
- `search_all(query, serpapi_key, max_per_source)` — Przeszukuje wszystkie dostępne źródła wiedzy.
- `format_results_for_llm(results)` — Formatuje wyniki wyszukiwania do wklejenia w prompt LLM.
- `anonymize(data_str)` — Anonimizuje wrażliwe dane.
- `display_anonymized_preview(data_str, report, max_lines)` — Wyświetla użytkownikowi zanonimizowane dane przed wysłaniem do LLM.
- `run_hitl_session(diagnostics, config, show_data)` — Runs interactive HITL session with full transparency.
- `colorize(line)` — Return line unchanged – rich handles markup in render_md().
- `render_md(text)` — Print LLM markdown reply to terminal via rich.
- `print_cmd_block(cmd, comment, dry_run)` — Print a framed command preview panel.
- `print_stdout_box(stdout, max_lines)` — Print stdout in a rich Panel.
- `print_stderr_box(stderr, max_lines)` — Print stderr in a rich Panel.
- `print_problem_header(problem_id, description, severity, status)` — Print a colored problem header panel.
- `render_tree_colored(nodes, execution_order)` — Render a ProblemGraph as a rich-markup string.
- `main()` — Test the cleanup planner


## Project Structure

📄 `docs.examples.advanced_usage`
📄 `docs.examples.quickstart`
📦 `fixos`
📦 `fixos.agent`
📄 `fixos.agent.autonomous` (7 functions, 2 classes)
📄 `fixos.agent.hitl` (10 functions, 1 classes)
📄 `fixos.anonymizer` (2 functions)
📄 `fixos.cli` (43 functions, 1 classes)
📄 `fixos.config` (7 functions, 1 classes)
📦 `fixos.diagnostics`
📄 `fixos.diagnostics.disk_analyzer` (15 functions, 1 classes)
📄 `fixos.diagnostics.flatpak_analyzer` (12 functions, 3 classes)
📄 `fixos.diagnostics.service_scanner` (20 functions, 3 classes)
📄 `fixos.diagnostics.system_checks` (9 functions)
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