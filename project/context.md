# System Architecture Analysis

## Overview

- **Project**: /home/tom/github/wronai/fixOS
- **Primary Language**: python
- **Languages**: python: 74, shell: 1
- **Analysis Mode**: static
- **Total Functions**: 381
- **Total Classes**: 66
- **Modules**: 75
- **Entry Points**: 312

## Architecture by Module

### fixos.agent.autonomous_session
- **Functions**: 22
- **Classes**: 3
- **File**: `autonomous_session.py`

### fixos.agent.hitl_session
- **Functions**: 20
- **Classes**: 2
- **File**: `hitl_session.py`

### fixos.diagnostics.disk_analyzer
- **Functions**: 15
- **Classes**: 1
- **File**: `disk_analyzer.py`

### fixos.diagnostics.flatpak_analyzer
- **Functions**: 12
- **Classes**: 3
- **File**: `flatpak_analyzer.py`

### fixos.features
- **Functions**: 12
- **Classes**: 2
- **File**: `__init__.py`

### fixos.interactive.cleanup_planner
- **Functions**: 12
- **Classes**: 4
- **File**: `cleanup_planner.py`

### fixos.features.installer
- **Functions**: 11
- **Classes**: 1
- **File**: `installer.py`

### fixos.orchestrator.executor
- **Functions**: 11
- **Classes**: 4
- **File**: `executor.py`

### fixos.orchestrator.orchestrator
- **Functions**: 11
- **Classes**: 2
- **File**: `orchestrator.py`

### fixos.orchestrator.graph
- **Functions**: 11
- **Classes**: 2
- **File**: `graph.py`

### fixos.platform_utils
- **Functions**: 10
- **File**: `platform_utils.py`

### fixos.diagnostics.system_checks
- **Functions**: 9
- **File**: `system_checks.py`

### fixos.utils.web_search
- **Functions**: 9
- **Classes**: 1
- **File**: `web_search.py`

### fixos.utils.anonymizer
- **Functions**: 9
- **Classes**: 1
- **File**: `anonymizer.py`

### fixos.system_checks
- **Functions**: 8
- **File**: `system_checks.py`

### fixos.diagnostics.service_cleanup
- **Functions**: 8
- **Classes**: 1
- **File**: `service_cleanup.py`

### fixos.diagnostics.service_scanner
- **Functions**: 8
- **Classes**: 3
- **File**: `service_scanner.py`

### fixos.cli.ask_cmd
- **Functions**: 8
- **File**: `ask_cmd.py`

### fixos.cli.cleanup_cmd
- **Functions**: 8
- **File**: `cleanup_cmd.py`

### fixos.plugins.registry
- **Functions**: 8
- **Classes**: 1
- **File**: `registry.py`

## Key Entry Points

Main execution flows into the system:

### fixos.cli.orchestrate_cmd.orchestrate
> Zaawansowana orkiestracja napraw z grafem problemów.


Różnica od 'fix':
  - Buduje graf kaskadowych zależności między problemami
  - Wykonuje napraw
- **Calls**: click.command, click.option, click.option, click.option, click.option, click.option, FixOsConfig.load, click.echo

### fixos.agent.hitl_session.HITLSession._process_turn
> Process one turn of the HITL session.

Returns False to exit loop, True to continue.
- **Calls**: self.remaining, console.print, console.print, console.print, _render_md, console.print, self._extract_fixes, self._check_low_confidence

### fixos.utils.terminal.render_md
> Print LLM markdown reply to terminal via rich.

Handles:
- ``` code blocks ``` rendered as Syntax panels
- # / ## headings via rich Markdown
- ━━━ / =
- **Calls**: text.splitlines, _flush_md, None.startswith, line.strip, re.match, stripped.startswith, stripped.startswith, stripped.startswith

### fixos.llm_shell.run_llm_shell
> Uruchamia interaktywny shell LLM z przekazanymi danymi diagnostycznymi.

Args:
    diagnostics_data: Słownik z danymi diagnostycznymi (przed anonimiza
- **Calls**: fixos.anonymizer.anonymize, openai.OpenAI, signal.signal, signal.alarm, time.time, Style.from_dict, PromptSession, print

### fixos.diagnostics.system_checks.diagnose_resources
> Diagnostyka zasobów systemowych.
Sprawdza: dysk (co zajmuje miejsce), pamięć (co ją żre),
procesy startujące automatycznie, usługi w tle.
- **Calls**: psutil.process_iter, top_cpu.sort, top_mem.sort, fixos.diagnostics.system_checks._psutil_required, len, round, result.update, round

### fixos.cli.fix_cmd.fix
> Przeprowadza pełną diagnostykę i uruchamia sesję naprawczą z LLM.


Tryby:
  hitl        – Human-in-the-Loop (pyta o każdą akcję) [domyślny]
  autono
- **Calls**: click.command, click.option, click.option, click.option, click.option, click.option, click.option, FixOsConfig.load

### fixos.utils.anonymizer.anonymize
> Anonimizuje wrażliwe dane.

Returns:
    Tuple (zanonimizowany_string, raport)
- **Calls**: AnonymizationReport, fixos.utils.anonymizer._get_sensitive, sensitive.get, sensitive.get, len, sensitive.get, len, len

### fixos.diagnostics.system_checks.diagnose_system
> System metrics – cross-platform: CPU, RAM, disks, processes.
- **Calls**: psutil.virtual_memory, psutil.swap_memory, psutil.disk_partitions, psutil.process_iter, procs.sort, fixos.diagnostics.system_checks._psutil_required, fixos.diagnostics.system_checks._cmd, fixos.diagnostics.system_checks._cmd

### fixos.cli.report_cmd.report
> Eksport wyników diagnostyki do raportu HTML/Markdown/JSON.


Przykłady:
  fixos report                           # HTML do stdout
  fixos report -o r
- **Calls**: click.command, click.option, click.option, click.option, click.option, PluginRegistry, registry.discover, click.echo

### fixos.cli.scan_cmd._print_quick_issues
> Wyświetla szybki przegląd problemów z zebranych danych.
- **Calls**: click.echo, data.get, data.get, None.strip, data.get, None.strip, click.style, issues.append

### fixos.cli.features_cmd.features_install
> Zainstaluj brakujące pakiety dla profilu.
- **Calls**: features.command, click.option, click.option, click.option, click.option, None.detect, PackageCatalog.load, FeatureAuditor

### fixos.diagnostics.system_checks.diagnose_security
> Diagnostyka bezpieczeństwa systemu i sieci.
Sprawdza: firewall, otwarte porty, usługi sieciowe, SELinux/AppArmor,
aktualizacje bezpieczeństwa, nieauto
- **Calls**: result.update, result.update, fixos.diagnostics.system_checks._cmd, fixos.diagnostics.system_checks._cmd, fixos.diagnostics.system_checks._cmd, fixos.diagnostics.system_checks._cmd, fixos.diagnostics.system_checks._cmd, fixos.diagnostics.system_checks._cmd

### fixos.plugins.builtin.security.Plugin.diagnose
- **Calls**: self._check_firewall, self._check_selinux, self._check_open_ports, self._check_ssh, self._check_fail2ban, any, DiagnosticResult, fw.get

### fixos.cli.provider_cmd.test_llm
> Test połączenia z LLM.


Wysyła proste zapytanie "Hello" i wyświetla odpowiedź.
Sprawdza czy token działa i provider jest dostępny.


Przykłady:
  f
- **Calls**: click.command, click.option, click.option, click.option, click.option, FixOsConfig.load, click.echo, click.echo

### fixos.cli.quickfix_cmd.quickfix
> Natychmiastowe naprawy bez API — baza znanych bugów.


Działa offline, zero tokenów. Używa wbudowanych heurystyk
do naprawy typowych problemów.


Pr
- **Calls**: click.command, click.option, click.option, PluginRegistry, registry.discover, click.echo, registry.run, click.echo

### fixos.cli.scan_cmd.scan
> Przeprowadza diagnostykę systemu.


Nowe opcje:
  --disc          – Analiza zajętości dysku
  --dry-run       – Symulacja (dla kompatybilności)
  --i
- **Calls**: click.command, click.option, click.option, click.option, click.option, click.option, click.option, click.option

### fixos.cli.provider_cmd.llm_providers
> Lista dostępnych providerów LLM.


Pokazuje wszystkich providerów z linkami do kluczy API.
Użyj --free aby zobaczyć tylko darmowe opcje.
- **Calls**: click.command, click.option, FixOsConfig.load, click.echo, click.echo, click.echo, PROVIDERS_INFO.items, click.echo

### fixos.cli.token_cmd.token_set
> Zapisz token API do pliku .env.


Przykłady:
  fixos token set AIzaSy...                    # auto-detect provider
  fixos token set sk-... --provide
- **Calls**: token.command, click.argument, click.option, click.option, fixos.config.detect_provider_from_key, None.resolve, provider_env_vars.get, click.echo

### fixos.plugins.builtin.resources.Plugin.diagnose
- **Calls**: self._check_cpu, self._check_ram, self._check_top_processes, self._check_zombies, self._check_swap, any, DiagnosticResult, cpu.get

### fixos.diagnostics.flatpak_analyzer.FlatpakAnalyzer._load_installed_refs
> Load all installed apps and runtimes with metadata
- **Calls**: self._run_flatpak_command, self._run_flatpak_command, json.loads, json.loads, FlatpakItemInfo, self._parse_size, self.installed_apps.append, FlatpakItemInfo

### fixos.features.renderer.FeatureRenderer.render_audit
> Render complete audit results.
- **Calls**: console.print, console.print, len, len, len, console.print, console.print, console.print

### fixos.config.FixOsConfig.load
> Tworzy konfigurację z połączonych źródeł.
- **Calls**: fixos.config._load_env_files, cls, None.lower, pdef.get, None.lower, None.lower, os.environ.get, None.lower

### fixos.orchestrator.orchestrator.FixOrchestrator.load_from_diagnostics
> Parsuje dane diagnostyczne przez LLM i buduje graf problemów.
- **Calls**: fixos.anonymizer.anonymize, None.get, fixos.anonymizer.anonymize, DIAGNOSE_PROMPT.format, str, p.to_summary, self.llm.chat, self._parse_json

### fixos.diagnostics.system_checks.diagnose_audio
> Diagnostyka dźwięku (ALSA/PipeWire/PulseAudio/SOF).
Typowe problemy po aktualizacji system:
- SOF (Sound Open Firmware) - brak karty dźwiękowej
- Pipe
- **Calls**: fixos.diagnostics.system_checks._cmd, fixos.diagnostics.system_checks._cmd, fixos.diagnostics.system_checks._cmd, fixos.diagnostics.system_checks._cmd, fixos.diagnostics.system_checks._cmd, fixos.diagnostics.system_checks._cmd, fixos.diagnostics.system_checks._cmd, fixos.diagnostics.system_checks._cmd

### fixos.diagnostics.flatpak_analyzer.FlatpakAnalyzer.get_cleanup_summary
> Get human-readable summary of cleanup opportunities
- **Calls**: self.analyze, lines.append, None.join, lines.append, sorted, lines.append, lines.append, lines.append

### fixos.features.catalog.PackageCatalog.load
> Load package catalog from YAML files.
- **Calls**: cls, data.items, packages_file.exists, open, yaml.safe_load, cat_id.startswith, PackageCategory, cat_data.get

### fixos.agent.hitl_session.HITLSession._print_action_menu
> Print the interactive numbered action menu.
- **Calls**: console.print, console.print, console.print, console.print, console.print, console.print, console.print, console.print

### fixos.cli.provider_cmd.providers
> Lista providerów LLM z oznaczeniem FREE/PAID.
- **Calls**: click.command, FixOsConfig.load, click.echo, click.echo, click.echo, PROVIDERS_INFO.items, click.echo, click.echo

### fixos.cli.cleanup_cmd.cleanup_services
> Skanuje i czyści dane usług przekraczające próg.


Wyszukuje dane usług (Docker, Ollama, npm, pip, yarn, pnpm, conda,
gradle, cargo, go, flutter, and
- **Calls**: click.command, click.option, click.option, click.option, click.option, click.option, click.option, ServiceDataScanner

### fixos.features.SystemDetector.detect
> Detect complete system information.
- **Calls**: SystemInfo, self._detect_id_like, self._detect_de, self._detect_display_server, self._detect_gpu_vendor, self._detect_gpu_model, None.exists, self._detect_pkg_manager

## Process Flows

Key execution flows identified:

### Flow 1: orchestrate
```
orchestrate [fixos.cli.orchestrate_cmd]
```

### Flow 2: _process_turn
```
_process_turn [fixos.agent.hitl_session.HITLSession]
```

### Flow 3: render_md
```
render_md [fixos.utils.terminal]
```

### Flow 4: run_llm_shell
```
run_llm_shell [fixos.llm_shell]
  └─ →> anonymize
      └─> get_sensitive_values
```

### Flow 5: diagnose_resources
```
diagnose_resources [fixos.diagnostics.system_checks]
  └─> _psutil_required
```

### Flow 6: fix
```
fix [fixos.cli.fix_cmd]
```

### Flow 7: anonymize
```
anonymize [fixos.utils.anonymizer]
  └─> _get_sensitive
```

### Flow 8: diagnose_system
```
diagnose_system [fixos.diagnostics.system_checks]
```

### Flow 9: report
```
report [fixos.cli.report_cmd]
```

### Flow 10: _print_quick_issues
```
_print_quick_issues [fixos.cli.scan_cmd]
```

## Key Classes

### fixos.agent.autonomous_session.AutonomousSession
> Self-directed autonomous diagnostic and repair session.
- **Methods**: 20
- **Key Methods**: fixos.agent.autonomous_session.AutonomousSession.__init__, fixos.agent.autonomous_session.AutonomousSession._setup_timeout, fixos.agent.autonomous_session.AutonomousSession._clear_timeout, fixos.agent.autonomous_session.AutonomousSession._confirm_start, fixos.agent.autonomous_session.AutonomousSession._initialize_messages, fixos.agent.autonomous_session.AutonomousSession._get_remaining_time, fixos.agent.autonomous_session.AutonomousSession._check_timeout, fixos.agent.autonomous_session.AutonomousSession._query_llm, fixos.agent.autonomous_session.AutonomousSession._handle_llm_error, fixos.agent.autonomous_session.AutonomousSession._parse_action

### fixos.agent.hitl_session.HITLSession
> Interactive Human-in-the-Loop diagnostic and repair session.
- **Methods**: 19
- **Key Methods**: fixos.agent.hitl_session.HITLSession.__init__, fixos.agent.hitl_session.HITLSession._setup_timeout, fixos.agent.hitl_session.HITLSession._clear_timeout, fixos.agent.hitl_session.HITLSession.remaining, fixos.agent.hitl_session.HITLSession.fmt_time, fixos.agent.hitl_session.HITLSession._initialize_messages, fixos.agent.hitl_session.HITLSession._print_header, fixos.agent.hitl_session.HITLSession._extract_fixes, fixos.agent.hitl_session.HITLSession._extract_search_topic, fixos.agent.hitl_session.HITLSession._print_action_menu

### fixos.diagnostics.disk_analyzer.DiskAnalyzer
> Analyzes disk usage and provides cleanup suggestions
- **Methods**: 14
- **Key Methods**: fixos.diagnostics.disk_analyzer.DiskAnalyzer.__init__, fixos.diagnostics.disk_analyzer.DiskAnalyzer.analyze_disk_usage, fixos.diagnostics.disk_analyzer.DiskAnalyzer._get_disk_status, fixos.diagnostics.disk_analyzer.DiskAnalyzer.get_large_files, fixos.diagnostics.disk_analyzer.DiskAnalyzer.get_cache_dirs, fixos.diagnostics.disk_analyzer.DiskAnalyzer.get_log_dirs, fixos.diagnostics.disk_analyzer.DiskAnalyzer.get_temp_dirs, fixos.diagnostics.disk_analyzer.DiskAnalyzer.suggest_cleanup_actions, fixos.diagnostics.disk_analyzer.DiskAnalyzer._get_dir_size_mb, fixos.diagnostics.disk_analyzer.DiskAnalyzer._categorize_file

### fixos.features.SystemDetector
> Detects system parameters.
- **Methods**: 12
- **Key Methods**: fixos.features.SystemDetector.detect, fixos.features.SystemDetector._detect_os_family, fixos.features.SystemDetector._detect_distro, fixos.features.SystemDetector._detect_distro_version, fixos.features.SystemDetector._detect_id_like, fixos.features.SystemDetector._detect_de, fixos.features.SystemDetector._detect_display_server, fixos.features.SystemDetector._detect_gpu_vendor, fixos.features.SystemDetector._detect_gpu_model, fixos.features.SystemDetector._detect_pkg_manager

### fixos.features.installer.FeatureInstaller
> Safely installs packages using native package manager or other backends.
- **Methods**: 11
- **Key Methods**: fixos.features.installer.FeatureInstaller.__init__, fixos.features.installer.FeatureInstaller.install, fixos.features.installer.FeatureInstaller._install_package, fixos.features.installer.FeatureInstaller._install_repo, fixos.features.installer.FeatureInstaller._install_native, fixos.features.installer.FeatureInstaller._install_flatpak, fixos.features.installer.FeatureInstaller._install_pip, fixos.features.installer.FeatureInstaller._install_cargo, fixos.features.installer.FeatureInstaller._install_npm, fixos.features.installer.FeatureInstaller._run_script

### fixos.orchestrator.orchestrator.FixOrchestrator
> Orkiestrator napraw systemowych.

Tryby:
- hitl: każda komenda wymaga potwierdzenia użytkownika
- au
- **Methods**: 11
- **Key Methods**: fixos.orchestrator.orchestrator.FixOrchestrator.__init__, fixos.orchestrator.orchestrator.FixOrchestrator.load_from_diagnostics, fixos.orchestrator.orchestrator.FixOrchestrator.load_from_dict, fixos.orchestrator.orchestrator.FixOrchestrator.run_sync, fixos.orchestrator.orchestrator.FixOrchestrator.run_async, fixos.orchestrator.orchestrator.FixOrchestrator._evaluate_and_rediagnose, fixos.orchestrator.orchestrator.FixOrchestrator._parse_json, fixos.orchestrator.orchestrator.FixOrchestrator._log, fixos.orchestrator.orchestrator.FixOrchestrator._session_summary, fixos.orchestrator.orchestrator.FixOrchestrator._default_confirm

### fixos.diagnostics.flatpak_analyzer.FlatpakAnalyzer
> Advanced analyzer for Flatpak cleanup decisions
- **Methods**: 10
- **Key Methods**: fixos.diagnostics.flatpak_analyzer.FlatpakAnalyzer.__init__, fixos.diagnostics.flatpak_analyzer.FlatpakAnalyzer.analyze, fixos.diagnostics.flatpak_analyzer.FlatpakAnalyzer._run_flatpak_command, fixos.diagnostics.flatpak_analyzer.FlatpakAnalyzer._parse_size, fixos.diagnostics.flatpak_analyzer.FlatpakAnalyzer._format_size, fixos.diagnostics.flatpak_analyzer.FlatpakAnalyzer._load_installed_refs, fixos.diagnostics.flatpak_analyzer.FlatpakAnalyzer._find_unused_runtimes, fixos.diagnostics.flatpak_analyzer.FlatpakAnalyzer._find_leftover_data, fixos.diagnostics.flatpak_analyzer.FlatpakAnalyzer._find_orphaned_apps, fixos.diagnostics.flatpak_analyzer.FlatpakAnalyzer.get_cleanup_summary

### fixos.interactive.cleanup_planner.CleanupPlanner
> Interactive cleanup planning and grouping system
- **Methods**: 10
- **Key Methods**: fixos.interactive.cleanup_planner.CleanupPlanner.__init__, fixos.interactive.cleanup_planner.CleanupPlanner.group_by_category, fixos.interactive.cleanup_planner.CleanupPlanner.prioritize_actions, fixos.interactive.cleanup_planner.CleanupPlanner.create_cleanup_plan, fixos.interactive.cleanup_planner.CleanupPlanner.interactive_selection, fixos.interactive.cleanup_planner.CleanupPlanner._dict_to_action, fixos.interactive.cleanup_planner.CleanupPlanner._action_to_dict, fixos.interactive.cleanup_planner.CleanupPlanner._get_category_for_action, fixos.interactive.cleanup_planner.CleanupPlanner._priority_score, fixos.interactive.cleanup_planner.CleanupPlanner._generate_recommendations

### fixos.plugins.registry.PluginRegistry
> Registry for diagnostic plugins with autodiscovery.
- **Methods**: 9
- **Key Methods**: fixos.plugins.registry.PluginRegistry.__init__, fixos.plugins.registry.PluginRegistry.discover, fixos.plugins.registry.PluginRegistry._register_builtins, fixos.plugins.registry.PluginRegistry._register_external, fixos.plugins.registry.PluginRegistry.register, fixos.plugins.registry.PluginRegistry.list_plugins, fixos.plugins.registry.PluginRegistry.get_plugin, fixos.plugins.registry.PluginRegistry.run, fixos.plugins.registry.PluginRegistry.last_results

### fixos.orchestrator.graph.ProblemGraph
> DAG problemów systemowych z topological sort do wyznaczania kolejności napraw.
Problemy bez nierozwi
- **Methods**: 9
- **Key Methods**: fixos.orchestrator.graph.ProblemGraph.__init__, fixos.orchestrator.graph.ProblemGraph.add, fixos.orchestrator.graph.ProblemGraph.get, fixos.orchestrator.graph.ProblemGraph.next_actionable, fixos.orchestrator.graph.ProblemGraph.all_done, fixos.orchestrator.graph.ProblemGraph.pending_count, fixos.orchestrator.graph.ProblemGraph.summary, fixos.orchestrator.graph.ProblemGraph.render_tree, fixos.orchestrator.graph.ProblemGraph._recalculate_order

### fixos.diagnostics.service_cleanup.ServiceCleaner
> Plans and executes cleanup of service data.
- **Methods**: 8
- **Key Methods**: fixos.diagnostics.service_cleanup.ServiceCleaner.__init__, fixos.diagnostics.service_cleanup.ServiceCleaner.get_cleanup_plan, fixos.diagnostics.service_cleanup.ServiceCleaner.cleanup_service, fixos.diagnostics.service_cleanup.ServiceCleaner._service_to_dict, fixos.diagnostics.service_cleanup.ServiceCleaner.is_safe_cleanup, fixos.diagnostics.service_cleanup.ServiceCleaner.get_service_description, fixos.diagnostics.service_cleanup.ServiceCleaner.get_cleanup_command, fixos.diagnostics.service_cleanup.ServiceCleaner.get_preview_command

### fixos.orchestrator.executor.CommandExecutor
> Bezpieczny executor komend z:
- walidacją niebezpiecznych wzorców
- automatycznym sudo dla komend sy
- **Methods**: 8
- **Key Methods**: fixos.orchestrator.executor.CommandExecutor.__init__, fixos.orchestrator.executor.CommandExecutor.is_dangerous, fixos.orchestrator.executor.CommandExecutor.needs_sudo, fixos.orchestrator.executor.CommandExecutor.add_sudo, fixos.orchestrator.executor.CommandExecutor._make_noninteractive, fixos.orchestrator.executor.CommandExecutor.check_idempotent, fixos.orchestrator.executor.CommandExecutor.execute_sync, fixos.orchestrator.executor.CommandExecutor.execute

### fixos.diagnostics.service_details.ServiceDetailsProvider
> Provides detailed information about service data.
- **Methods**: 7
- **Key Methods**: fixos.diagnostics.service_details.ServiceDetailsProvider.get_details, fixos.diagnostics.service_details.ServiceDetailsProvider._docker, fixos.diagnostics.service_details.ServiceDetailsProvider._ollama, fixos.diagnostics.service_details.ServiceDetailsProvider._conda, fixos.diagnostics.service_details.ServiceDetailsProvider._package_cache, fixos.diagnostics.service_details.ServiceDetailsProvider._flatpak, fixos.diagnostics.service_details.ServiceDetailsProvider._parse_size_bytes

### fixos.diagnostics.service_scanner.ServiceDataScanner
> Scans for large service data directories and allows cleanup.
- **Methods**: 7
- **Key Methods**: fixos.diagnostics.service_scanner.ServiceDataScanner.__init__, fixos.diagnostics.service_scanner.ServiceDataScanner.scan_all_services, fixos.diagnostics.service_scanner.ServiceDataScanner.scan_service, fixos.diagnostics.service_scanner.ServiceDataScanner._analyze_service_path, fixos.diagnostics.service_scanner.ServiceDataScanner._get_path_size_mb, fixos.diagnostics.service_scanner.ServiceDataScanner.get_cleanup_plan, fixos.diagnostics.service_scanner.ServiceDataScanner.cleanup_service

### fixos.providers.llm.LLMClient
> Wrapper nad openai.OpenAI kompatybilny z wieloma providerami.
Obsługuje retry, streaming i zbieranie
- **Methods**: 7
- **Key Methods**: fixos.providers.llm.LLMClient.__init__, fixos.providers.llm.LLMClient.chat, fixos.providers.llm.LLMClient.chat_stream, fixos.providers.llm.LLMClient.total_tokens, fixos.providers.llm.LLMClient.chat_structured, fixos.providers.llm.LLMClient._extract_json, fixos.providers.llm.LLMClient.ping

### fixos.providers.llm_analyzer.LLMAnalyzer
> Uses LLM to analyze disk issues when heuristics aren't sufficient
- **Methods**: 7
- **Key Methods**: fixos.providers.llm_analyzer.LLMAnalyzer.__init__, fixos.providers.llm_analyzer.LLMAnalyzer.analyze_disk_issues, fixos.providers.llm_analyzer.LLMAnalyzer.analyze_failed_action, fixos.providers.llm_analyzer.LLMAnalyzer.analyze_complex_pattern, fixos.providers.llm_analyzer.LLMAnalyzer._sanitize_suggestion, fixos.providers.llm_analyzer.LLMAnalyzer._create_fallback_analysis, fixos.providers.llm_analyzer.LLMAnalyzer.enhance_heuristics_with_llm

### fixos.plugins.builtin.resources.Plugin
- **Methods**: 6
- **Key Methods**: fixos.plugins.builtin.resources.Plugin.diagnose, fixos.plugins.builtin.resources.Plugin._check_cpu, fixos.plugins.builtin.resources.Plugin._check_ram, fixos.plugins.builtin.resources.Plugin._check_top_processes, fixos.plugins.builtin.resources.Plugin._check_zombies, fixos.plugins.builtin.resources.Plugin._check_swap
- **Inherits**: DiagnosticPlugin

### fixos.plugins.builtin.security.Plugin
- **Methods**: 6
- **Key Methods**: fixos.plugins.builtin.security.Plugin.diagnose, fixos.plugins.builtin.security.Plugin._check_firewall, fixos.plugins.builtin.security.Plugin._check_selinux, fixos.plugins.builtin.security.Plugin._check_open_ports, fixos.plugins.builtin.security.Plugin._check_ssh, fixos.plugins.builtin.security.Plugin._check_fail2ban
- **Inherits**: DiagnosticPlugin

### fixos.plugins.builtin.hardware.Plugin
- **Methods**: 6
- **Key Methods**: fixos.plugins.builtin.hardware.Plugin.diagnose, fixos.plugins.builtin.hardware.Plugin._check_gpu, fixos.plugins.builtin.hardware.Plugin._check_battery, fixos.plugins.builtin.hardware.Plugin._check_touchpad, fixos.plugins.builtin.hardware.Plugin._check_camera, fixos.plugins.builtin.hardware.Plugin._check_dmi
- **Inherits**: DiagnosticPlugin

### fixos.orchestrator.rollback.RollbackSession
> A session of recorded operations that can be rolled back.
- **Methods**: 6
- **Key Methods**: fixos.orchestrator.rollback.RollbackSession.record, fixos.orchestrator.rollback.RollbackSession.get_rollback_commands, fixos.orchestrator.rollback.RollbackSession.rollback_last, fixos.orchestrator.rollback.RollbackSession._save, fixos.orchestrator.rollback.RollbackSession.load, fixos.orchestrator.rollback.RollbackSession.list_sessions

## Data Transformation Functions

Key functions that process and transform data:

### fixos.system_checks.get_top_processes
> Lista TOP N procesów według zużycia CPU.
- **Output to**: psutil.process_iter, processes.sort, processes.append, x.get

### fixos.llm_shell.format_time

### fixos.diagnostics.service_details.ServiceDetailsProvider._parse_size_bytes
> Parse human-readable size to bytes.
- **Output to**: None.upper, sorted, multipliers.items, size_str.endswith, int

### fixos.config.FixOsConfig.validate
> Zwraca listę błędów walidacji (pusta = OK).
- **Output to**: errors.append, errors.append, None.get

### fixos.diagnostics.flatpak_analyzer.FlatpakAnalyzer._parse_size
> Parse human-readable size to bytes
- **Output to**: None.upper, sorted, multipliers.items, size_str.endswith, int

### fixos.diagnostics.flatpak_analyzer.FlatpakAnalyzer._format_size
> Format bytes to human-readable string

### fixos.agent.autonomous_session.AutonomousSession._parse_action
> Parse JSON action from LLM reply.
- **Output to**: re.search, json.loads, reply.strip, json.loads, m.group

### fixos.agent.autonomous_session.AutonomousSession._process_turn
> Process one turn of the autonomous session.

Returns False if session should end, True to continue.
- **Output to**: self._check_timeout, self._get_remaining_time, print, self._query_llm, self.messages.append

### fixos.agent.hitl_session.HITLSession._process_turn
> Process one turn of the HITL session.

Returns False to exit loop, True to continue.
- **Output to**: self.remaining, console.print, console.print, console.print, _render_md

### fixos.cli.ask_cmd._format_command
> Convert matched command to string format.
- **Output to**: isinstance, None.join, len

### fixos.cli.ask_cmd._validate_result_with_llm
> Validate command result using LLM - generates check command and assesses outcome.
- **Output to**: LLMClient, llm.chat, None.strip, None.strip, subprocess.run

### fixos.cli.cleanup_cmd._parse_size_to_gb
> Parse human-readable size to GB
- **Output to**: None.upper, sorted, multipliers.items, size_str.endswith, size_str.strip

### fixos.plugins.builtin.resources.Plugin._check_top_processes
- **Output to**: fixos.platform_utils.run_command

### fixos.utils.web_search.format_results_for_llm
> Formatuje wyniki wyszukiwania do wklejenia w prompt LLM.
- **Output to**: enumerate, None.join, lines.append, lines.append, lines.append

### fixos.utils.anonymizer._format_diagnostics_markdown
> Formatuje dane diagnostyczne jako czytelny markdown.
- **Output to**: None.replace, ast.literal_eval, isinstance, fixos.utils.anonymizer._dict_to_markdown, data_str.replace

### fixos.utils.anonymizer._format_key_title
> Formatuje klucz dict jako czytelny tytuł.
- **Output to**: titles.get, None.title, key.replace

### fixos.orchestrator.orchestrator.FixOrchestrator._parse_json
> Parsuje JSON z odpowiedzi LLM (usuwa markdown code fences).
- **Output to**: raw.strip, text.startswith, text.splitlines, None.join, json.loads

## Behavioral Patterns

### recursion__dict_to_markdown
- **Type**: recursion
- **Confidence**: 0.90
- **Functions**: fixos.utils.anonymizer._dict_to_markdown

## Public API Surface

Functions exposed as public API (no underscore prefix):

- `fixos.cli.orchestrate_cmd.orchestrate` - 63 calls
- `fixos.utils.terminal.render_md` - 55 calls
- `fixos.llm_shell.run_llm_shell` - 53 calls
- `fixos.config.interactive_provider_setup` - 53 calls
- `fixos.diagnostics.system_checks.diagnose_resources` - 49 calls
- `fixos.cli.fix_cmd.fix` - 49 calls
- `fixos.utils.anonymizer.anonymize` - 48 calls
- `fixos.diagnostics.system_checks.diagnose_system` - 46 calls
- `fixos.cli.fix_cmd.handle_disk_cleanup_mode` - 41 calls
- `fixos.cli.report_cmd.report` - 39 calls
- `fixos.cli.features_cmd.features_install` - 37 calls
- `fixos.diagnostics.system_checks.diagnose_security` - 36 calls
- `fixos.plugins.builtin.security.Plugin.diagnose` - 36 calls
- `fixos.cli.provider_cmd.test_llm` - 34 calls
- `fixos.cli.quickfix_cmd.quickfix` - 31 calls
- `fixos.cli.scan_cmd.scan` - 31 calls
- `fixos.cli.provider_cmd.llm_providers` - 29 calls
- `fixos.cli.token_cmd.token_set` - 29 calls
- `fixos.plugins.builtin.resources.Plugin.diagnose` - 29 calls
- `fixos.features.renderer.FeatureRenderer.render_audit` - 27 calls
- `fixos.config.FixOsConfig.load` - 26 calls
- `fixos.orchestrator.orchestrator.FixOrchestrator.load_from_diagnostics` - 26 calls
- `fixos.diagnostics.system_checks.diagnose_audio` - 25 calls
- `fixos.diagnostics.flatpak_analyzer.FlatpakAnalyzer.get_cleanup_summary` - 25 calls
- `fixos.features.catalog.PackageCatalog.load` - 24 calls
- `fixos.cli.provider_cmd.providers` - 24 calls
- `fixos.cli.cleanup_cmd.cleanup_services` - 24 calls
- `fixos.features.SystemDetector.detect` - 23 calls
- `fixos.cli.fix_cmd.execute_cleanup_actions` - 23 calls
- `fixos.plugins.builtin.thumbnails.Plugin.diagnose` - 23 calls
- `fixos.plugins.builtin.hardware.Plugin.diagnose` - 23 calls
- `fixos.cli.rollback_cmd.rollback_undo` - 22 calls
- `fixos.plugins.builtin.audio.Plugin.diagnose` - 22 calls
- `fixos.diagnostics.system_checks.diagnose_thumbnails` - 21 calls
- `fixos.plugins.builtin.disk.Plugin.diagnose` - 21 calls
- `fixos.providers.llm_analyzer.LLMAnalyzer.analyze_failed_action` - 21 calls
- `fixos.interactive.cleanup_planner.CleanupPlanner.create_cleanup_plan` - 21 calls
- `fixos.orchestrator.orchestrator.FixOrchestrator.run_sync` - 20 calls
- `fixos.diagnostics.system_checks.diagnose_hardware` - 18 calls
- `fixos.diagnostics.disk_analyzer.DiskAnalyzer.analyze_disk_usage` - 18 calls

## System Interactions

How components interact:

```mermaid
graph TD
    orchestrate --> command
    orchestrate --> option
    _process_turn --> remaining
    _process_turn --> print
    _process_turn --> _render_md
    render_md --> splitlines
    render_md --> _flush_md
    render_md --> startswith
    render_md --> strip
    render_md --> match
    run_llm_shell --> anonymize
    run_llm_shell --> OpenAI
    run_llm_shell --> signal
    run_llm_shell --> alarm
    run_llm_shell --> time
    diagnose_resources --> process_iter
    diagnose_resources --> sort
    diagnose_resources --> _psutil_required
    diagnose_resources --> len
    fix --> command
    fix --> option
    anonymize --> AnonymizationReport
    anonymize --> _get_sensitive
    anonymize --> get
    anonymize --> len
    diagnose_system --> virtual_memory
    diagnose_system --> swap_memory
    diagnose_system --> disk_partitions
    diagnose_system --> process_iter
    diagnose_system --> sort
```

## Reverse Engineering Guidelines

1. **Entry Points**: Start analysis from the entry points listed above
2. **Core Logic**: Focus on classes with many methods
3. **Data Flow**: Follow data transformation functions
4. **Process Flows**: Use the flow diagrams for execution paths
5. **API Surface**: Public API functions reveal the interface

## Context for LLM

Maintain the identified architectural patterns and public API surface when suggesting changes.