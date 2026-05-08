# fixOS v2.2.6 🔧🤖

SUMD - Structured Unified Markdown Descriptor for AI-aware project refactorization

## Contents

- [Metadata](#metadata)
- [Architecture](#architecture)
- [Workflows](#workflows)
- [Quality Pipeline (`pyqual.yaml`)](#quality-pipeline-pyqualyaml)
- [Dependencies](#dependencies)
- [Call Graph](#call-graph)
- [Test Contracts](#test-contracts)
- [Refactoring Analysis](#refactoring-analysis)
- [Intent](#intent)

## Metadata

- **name**: `fixos`
- **version**: `2.2.28`
- **python_requires**: `>=3.10`
- **license**: {'text': 'Apache-2.0'}
- **ai_model**: `openrouter/qwen/qwen3-coder-next`
- **ecosystem**: SUMD + DOQL + testql + taskfile
- **generated_from**: pyproject.toml, requirements-dev.txt, requirements.txt, Makefile, testql(2), app.doql.less, pyqual.yaml, goal.yaml, .env.example, docker-compose.yml, project/(6 analysis files)

## Architecture

```
SUMD (description) → DOQL/source (code) → taskfile (automation) → testql (verification)
```

### DOQL Application Declaration (`app.doql.less`)

```less markpact:doql path=app.doql.less
// LESS format — define @variables here as needed

app {
  name: fixos;
  version: 2.2.28;
}

dependencies {
  runtime: "openai>=1.35.0, prompt_toolkit>=3.0.43, psutil>=5.9.0, pyyaml>=6.0, click>=8.1.0, python-dotenv>=1.0.0, rich>=13.0";
  dev: "pytest>=7.4.0, pytest-mock>=3.12.0, pytest-cov>=4.1.0, pytest-xdist>=3.5.0, pytest-timeout>=2.2.0, pytest-sugar>=0.9.7, goal>=2.1.0, costs>=0.1.20, pfix>=0.1.60";
}

entity[name="FixSuggestion"] {
  command: string!;
  description: string!;
  risk_level: RiskLevel!;
  requires_sudo: bool!;
  idempotent: bool!;
  check_command: string;
  rollback_command: string;
}

entity[name="NLPIntent"] {
  intent_type: string!;
  target: string;
  parameters: json!;
  confidence: float!;
}

entity[name="CommandValidation"] {
  success: bool!;
  interpretation: string!;
  user_intent_met: bool!;
  suggestion: string;
}

interface[type="cli"] {
  framework: click;
}
interface[type="cli"] page[name="fixos"] {

}

workflow[name="install"] {
  trigger: manual;
  step-1: run cmd=pip install -e .;
}

workflow[name="install-dev"] {
  trigger: manual;
  step-1: run cmd=pip install -e ".[dev]";
  step-2: run cmd=echo "✅ Zainstalowano z zależnościami dev";
}

workflow[name="test"] {
  trigger: manual;
  step-1: depend target=test-unit;
  step-2: depend target=test-e2e;
}

workflow[name="test-fast"] {
  trigger: manual;
  step-1: run cmd=echo "⚡ Testy z paralelizacją (4 procesy)...";
  step-2: run cmd=pytest tests/ -v --tb=short -n auto -m "not slow and not docker";
}

workflow[name="test-quick"] {
  trigger: manual;
  step-1: run cmd=echo "⚡ Szybkie testy (bez slow/docker)...";
  step-2: run cmd=pytest tests/unit tests/e2e/test_anonymization_layers.py tests/e2e/test_executor.py -v --tb=short -m "not slow and not docker";
}

workflow[name="test-unit"] {
  trigger: manual;
  step-1: run cmd=echo "🧪 Unit testy...";
  step-2: run cmd=pytest tests/unit/ -v --tb=short;
}

workflow[name="test-unit-fast"] {
  trigger: manual;
  step-1: run cmd=echo "🧪 Unit testy (paralelizacja - 4 procesy)...";
  step-2: run cmd=pytest tests/unit/ -v --tb=short -n 4;
}

workflow[name="test-unit-par"] {
  trigger: manual;
  step-1: run cmd=echo "🧪 Unit testy (paralelizacja - auto, = CPU count)...";
  step-2: run cmd=pytest tests/unit/ -v --tb=short -n auto;
}

workflow[name="test-e2e"] {
  trigger: manual;
  step-1: run cmd=echo "🧪 E2E testy (mock LLM)...";
  step-2: run cmd=pytest tests/e2e/ -v --tb=short -k "not real_llm" -m "not slow and not docker";
}

workflow[name="test-real"] {
  trigger: manual;
  step-1: run cmd=echo "🧪 E2E testy (prawdziwe API – wymaga .env)...";
  step-2: run cmd=pytest tests/e2e/ -v --tb=short -k "real_llm";
}

workflow[name="test-cov"] {
  trigger: manual;
  step-1: run cmd=echo "📊 Testy + raport pokrycia (z paralelizacją)...";
  step-2: run cmd=pytest tests/ -v --tb=short --cov=fixos --cov-report=term-missing --cov-report=html:htmlcov -n auto -m "not slow";
  step-3: run cmd=echo "📊 Raport pokrycia: htmlcov/index.html";
}

workflow[name="lint"] {
  trigger: manual;
  step-1: run cmd=ruff check fixos/ tests/ || true;
}

workflow[name="format"] {
  trigger: manual;
  step-1: run cmd=black fixos/ tests/;
}

workflow[name="docker-build"] {
  trigger: manual;
  step-1: run cmd=docker compose -f docker/docker-compose.yml build;
}

workflow[name="docker-audio"] {
  trigger: manual;
  step-1: run cmd=docker compose -f docker/docker-compose.yml run --rm broken-audio;
}

workflow[name="docker-thumb"] {
  trigger: manual;
  step-1: run cmd=docker compose -f docker/docker-compose.yml run --rm broken-thumbnails;
}

workflow[name="docker-full"] {
  trigger: manual;
  step-1: run cmd=docker compose -f docker/docker-compose.yml run --rm broken-full;
}

workflow[name="docker-e2e"] {
  trigger: manual;
  step-1: run cmd=docker compose -f docker/docker-compose.yml run --rm e2e-tests;
}

workflow[name="docker-test-fedora"] {
  trigger: manual;
  step-1: run cmd=echo "🐧 Testing on Fedora...";
  step-2: run cmd=docker compose -f docker/docker-compose.multi-system.yml run --rm test-fedora;
}

workflow[name="docker-test-ubuntu"] {
  trigger: manual;
  step-1: run cmd=echo "🐧 Testing on Ubuntu...";
  step-2: run cmd=docker compose -f docker/docker-compose.multi-system.yml run --rm test-ubuntu;
}

workflow[name="docker-test-debian"] {
  trigger: manual;
  step-1: run cmd=echo "🐧 Testing on Debian...";
  step-2: run cmd=docker compose -f docker/docker-compose.multi-system.yml run --rm test-debian;
}

workflow[name="docker-test-arch"] {
  trigger: manual;
  step-1: run cmd=echo "🐧 Testing on Arch Linux...";
  step-2: run cmd=docker compose -f docker/docker-compose.multi-system.yml run --rm test-arch;
}

workflow[name="docker-test-alpine"] {
  trigger: manual;
  step-1: run cmd=echo "🐧 Testing on Alpine...";
  step-2: run cmd=docker compose -f docker/docker-compose.multi-system.yml run --rm test-alpine;
}

workflow[name="docker-test-all"] {
  trigger: manual;
  step-1: run cmd=echo "🐧 Testing on all systems...";
  step-2: run cmd=./docker/test-multi-system.sh;
}

workflow[name="config-init"] {
  trigger: manual;
  step-1: run cmd=fixos config init;
}

workflow[name="run-scan"] {
  trigger: manual;
  step-1: run cmd=fixos scan;
}

workflow[name="run-fix"] {
  trigger: manual;
  step-1: run cmd=fixos fix;
}

workflow[name="build"] {
  trigger: manual;
  step-1: run cmd=echo "🔨 Budowanie paczki (cache enabled)...";
  step-2: run cmd=.venv/bin/pip install --quiet --upgrade build;
  step-3: run cmd=.venv/bin/python -m build;
  step-4: run cmd=echo "✅ Paczka gotowa w dist/";
}

workflow[name="publish"] {
  trigger: manual;
  step-1: run cmd=echo "📦 Publikowanie na PyPI...";
  step-2: run cmd=.venv/bin/pip install --quiet --upgrade twine;
  step-3: run cmd=.venv/bin/twine upload dist/*;
  step-4: run cmd=echo "✅ Opublikowano na PyPI";
}

workflow[name="clean"] {
  trigger: manual;
  step-1: run cmd=echo "🧹 Czyszczenie cache i artefaktów...";
  step-2: run cmd=rm -rf build/ dist/ *.egg-info/ .pytest_cache/ .coverage htmlcov/ __pycache__ .mypy_cache/;
  step-3: run cmd=find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true;
  step-4: run cmd=find . -type f -name "*.pyc" -delete 2>/dev/null || true;
  step-5: run cmd=find . -type f -name ".DS_Store" -delete 2>/dev/null || true;
  step-6: run cmd=echo "✅ Wyczyszczono";
}

deploy {
  target: docker-compose;
  compose_file: docker/docker-compose.yml;
}

environment[name="local"] {
  runtime: docker-compose;
  env_file: .env;
  python_version: >=3.10;
}
```

## Workflows

## Quality Pipeline (`pyqual.yaml`)

```yaml markpact:pyqual path=pyqual.yaml
pipeline:
  name: quality-loop-with-llx

  # Quality gates — pipeline iterates until ALL pass
  metrics:
    cc_max: 6           # cyclomatic complexity per function
    vallm_pass_min: 65   # vallm validation pass rate (%)
    coverage_min: 27      # test coverage (%)

  # Custom tool definitions
  custom_tools:
    - name: code2llm_vallm
      binary: code2llm
      command: >-
        code2llm {workdir} -f toon -o ./project --no-chunk
        --exclude .git venv dist __pycache__ .pytest_cache .mypy_cache .ruff_cache
        .code2llm_cache build *.egg-info
      output: ""
      allow_failure: false

    - name: vallm_src
      binary: vallm
      command: >-
        vallm batch {workdir}/fixos --recursive --format toon --output ./project
        --exclude .git,venv,dist,__pycache__,.pytest_cache,.mypy_cache,.ruff_cache,
        .code2llm_cache,build,*.egg-info
      output: ""
      allow_failure: false

    - name: vallm_verify
      binary: vallm
      command: >-
        vallm batch {workdir}/fixos --recursive --no-complexity --format toon --output ./project/verify
        --exclude .git,venv,dist,__pycache__,.pytest_cache,.mypy_cache,.ruff_cache,
        .code2llm_cache,build,*.egg-info
      output: ""
      allow_failure: false

  # Pipeline stages
  stages:
    - name: setup
      run: |
        set -e
        echo "=== pyqual dependency check ==="
        for pkg in code2llm vallm prefact llx pytest-cov goal; do
          if python -m pip show "$pkg" >/dev/null 2>&1; then
            echo "  ✓ $pkg"
          else
            echo "  ✗ $pkg — installing…"
            pip install -q "$pkg" || echo "  ⚠ $pkg install failed (optional)"
          fi
        done
        if command -v claude >/dev/null 2>&1; then
          echo "  ✓ claude $(claude --version 2>/dev/null)"
        else
          echo "  ✗ claude — not installed"
        fi
        echo "=== setup done ==="
      when: first_iteration
      timeout: 300

    - name: lint
      tool: ruff
      optional: true

    - name: test
      run: .venv/bin/python -m pytest -q --tb=short --cov=fixos --cov-report=term-missing --cov-report=json:.pyqual/coverage.json
      when: always

    - name: prefact
      tool: prefact
      optional: true
      when: metrics_fail
      timeout: 900

    - name: fix
      tool: llx-fix
      optional: true
      when: metrics_fail
      timeout: 1800

    - name: verify
      tool: vallm_verify
      optional: true
      when: after_fix
      timeout: 300

    - name: push
      run: |
        if [ -n "$(git status --porcelain)" ]; then
          git add -A
          git commit -m "chore: pyqual auto-commit [skip ci]" 2>/dev/null || true
          git push origin HEAD
        else
          echo "No changes to push"
        fi
      when: metrics_pass
      optional: true
      timeout: 120

    - name: publish
      run: make publish
      when: metrics_pass
      timeout: 300

    - name: markdown_report
      run: python3 -m pyqual.report_generator
      when: always
      optional: true
      timeout: 30

  # Loop behavior
  loop:
    max_iterations: 3
    on_fail: report

  # Environment
  env:
    LLM_MODEL: openrouter/x-ai/grok-code-fast-1
    LLX_DEFAULT_TIER: balanced
    LLX_VERBOSE: true
```

## Dependencies

### Runtime

```text markpact:deps python
openai>=1.35.0
prompt_toolkit>=3.0.43
psutil>=5.9.0
pyyaml>=6.0
click>=8.1.0
python-dotenv>=1.0.0
rich>=13.0
```

### Development

```text markpact:deps python scope=dev
pytest>=7.4.0
pytest-mock>=3.12.0
pytest-cov>=4.1.0
pytest-xdist>=3.5.0
pytest-timeout>=2.2.0
pytest-sugar>=0.9.7
goal>=2.1.0
costs>=0.1.20
pfix>=0.1.60
```

## Call Graph

*225 nodes · 227 edges · 50 modules · CC̄=4.3*

### Hubs (by degree)

| Function | CC | in | out | total |
|----------|----|----|-----|-------|
| `_cmd` *(in fixos.diagnostics.checks._shared)* | 7 | 241 | 3 | **244** |
| `_cleanup_flatpak_detailed` *(in fixos.cli._cleanup_flatpak)* | 12 ⚠ | 1 | 111 | **112** |
| `_display_full_system_menu` *(in fixos.cli._cleanup_system)* | 12 ⚠ | 1 | 79 | **80** |
| `_display_flatpak_status` *(in fixos.cli._cleanup_flatpak)* | 9 | 1 | 65 | **66** |
| `_print_welcome` *(in fixos.cli.main)* | 6 | 1 | 61 | **62** |
| `_handle_interactive_select` *(in fixos.cli._cleanup_system)* | 14 ⚠ | 1 | 52 | **53** |
| `_handle_home_analysis` *(in fixos.cli._cleanup_home)* | 11 ⚠ | 1 | 49 | **50** |
| `diagnose_resources` *(in fixos.diagnostics.checks.resources)* | 13 ⚠ | 0 | 49 | **49** |

```toon markpact:analysis path=project/calls.toon.yaml
# code2llm call graph | /home/tom/github/wronai/fixOS
# generated in 0.10s
# nodes: 225 | edges: 227 | modules: 50
# CC̄=4.3

HUBS[20]:
  fixos.diagnostics.checks._shared._cmd
    CC=7  in:241  out:3  total:244
  fixos.cli._cleanup_flatpak._cleanup_flatpak_detailed
    CC=12  in:1  out:111  total:112
  fixos.cli._cleanup_system._display_full_system_menu
    CC=12  in:1  out:79  total:80
  fixos.cli._cleanup_flatpak._display_flatpak_status
    CC=9  in:1  out:65  total:66
  fixos.cli.main._print_welcome
    CC=6  in:1  out:61  total:62
  fixos.cli._cleanup_system._handle_interactive_select
    CC=14  in:1  out:52  total:53
  fixos.cli._cleanup_home._handle_home_analysis
    CC=11  in:1  out:49  total:50
  fixos.diagnostics.checks.resources.diagnose_resources
    CC=13  in:0  out:49  total:49
  fixos.cli._cleanup_system._execute_full_cleanup
    CC=8  in:1  out:37  total:38
  fixos.cli.config_cmd.config_model
    CC=8  in:0  out:38  total:38
  fixos.platform_utils.run_command
    CC=5  in:33  out:4  total:37
  fixos.diagnostics.checks.security.diagnose_security
    CC=4  in:0  out:36  total:36
  fixos.llm_shell.run_llm_shell
    CC=8  in:0  out:34  total:34
  fixos.cli._cleanup_utils._format_bytes
    CC=1  in:32  out:1  total:33
  fixos.utils.terminal.render_md
    CC=9  in:0  out:30  total:30
  fixos.cli.token_cmd.token_set
    CC=7  in:0  out:29  total:29
  fixos.anonymizer.anonymize
    CC=5  in:14  out:14  total:28
  docker.validate-scenario.main
    CC=7  in:0  out:27  total:27
  scripts.pyqual-calibrate.calibrate
    CC=14  in:1  out:26  total:27
  fixos.config.FixOsConfig.load
    CC=14  in:0  out:26  total:26

MODULES:
  docker.validate-scenario  [3 funcs]
    _get_nested  CC=4  out:2
    main  CC=7  out:27
    validate  CC=11  out:18
  docs.examples.quickstart  [1 funcs]
    run_autonomous_session  CC=1  out:0
  fixos.agent  [1 funcs]
    get_remaining_time  CC=2  out:4
  fixos.agent.autonomous_session  [5 funcs]
    _get_remaining_time  CC=1  out:1
    _handle_exec  CC=4  out:17
    _handle_llm_error  CC=4  out:3
    _handle_search  CC=3  out:8
    _initialize_messages  CC=2  out:3
  fixos.agent.hitl  [1 funcs]
    run_hitl_session  CC=1  out:2
  fixos.agent.hitl_session  [8 funcs]
    __init__  CC=2  out:5
    _check_low_confidence  CC=7  out:8
    _clear_timeout  CC=1  out:1
    _handle_llm_error  CC=4  out:4
    _initialize_messages  CC=3  out:5
    _process_turn  CC=8  out:17
    _setup_timeout  CC=1  out:3
    remaining  CC=1  out:1
  fixos.agent.session_core  [10 funcs]
    _deduplicate  CC=5  out:4
    _extract_co_robi  CC=2  out:3
    _is_diagnostic_only_command  CC=3  out:2
    _is_part_diagnostic_only  CC=6  out:6
    _pattern_backticks  CC=3  out:6
    _pattern_fallbacks  CC=6  out:13
    _pattern_no_backticks  CC=3  out:7
    _pattern_strict_bold  CC=4  out:6
    extract_fixes  CC=4  out:5
    extract_search_topic  CC=3  out:4
  fixos.agent.session_handlers  [11 funcs]
    _resolve_command_timeout  CC=6  out:6
    _sort_fixes_by_priority  CC=1  out:6
    handle_describe_problem  CC=2  out:2
    handle_direct_command  CC=1  out:5
    handle_execute_all  CC=4  out:10
    handle_fix_by_number  CC=2  out:9
    handle_quit  CC=1  out:1
    handle_search  CC=2  out:6
    handle_skip_all  CC=1  out:1
    parse_user_input  CC=9  out:11
  fixos.agent.session_io  [10 funcs]
    ask_execute_prompt  CC=1  out:4
    ask_low_confidence_search  CC=1  out:4
    ask_send_data  CC=1  out:4
    ask_user_problem  CC=2  out:11
    fmt_time  CC=1  out:0
    get_user_input  CC=2  out:4
    print_cmd_result  CC=8  out:13
    print_session_header  CC=1  out:8
    print_session_summary  CC=3  out:4
    suspend_timeout  CC=4  out:3
  fixos.anonymizer  [2 funcs]
    anonymize  CC=5  out:14
    get_sensitive_values  CC=4  out:3
  fixos.cli._cleanup_flatpak  [2 funcs]
    _cleanup_flatpak_detailed  CC=12  out:111
    _display_flatpak_status  CC=9  out:65
  fixos.cli._cleanup_home  [3 funcs]
    _display_home_items  CC=7  out:17
    _handle_home_analysis  CC=11  out:49
    _resolve_home_selection  CC=4  out:8
  fixos.cli._cleanup_snap  [6 funcs]
    _handle_snap_management  CC=9  out:21
    _snap_display_packages  CC=3  out:12
    _snap_fetch_packages  CC=6  out:8
    _snap_remove_packages  CC=4  out:10
    _snap_select_packages  CC=5  out:9
    _snap_warn_dangerous  CC=5  out:5
  fixos.cli._cleanup_system  [12 funcs]
    _cleanup_full_system  CC=8  out:12
    _dispatch_system_selection  CC=6  out:6
    _display_full_system_menu  CC=12  out:79
    _execute_full_cleanup  CC=8  out:37
    _filter_by_age  CC=6  out:8
    _filter_by_prefix_category  CC=6  out:12
    _filter_by_prefix_top  CC=3  out:7
    _filter_by_prefix_type  CC=10  out:14
    _filter_large  CC=4  out:5
    _handle_interactive_select  CC=14  out:52
  fixos.cli._cleanup_utils  [3 funcs]
    _build_dep_types  CC=4  out:2
    _format_bytes  CC=1  out:1
    _parse_numeric_range_set  CC=5  out:10
  fixos.cli.ask_cmd  [9 funcs]
    _build_output_dict  CC=8  out:0
    _execute_heuristic_command  CC=9  out:12
    _execute_with_llm  CC=8  out:21
    _format_command  CC=5  out:7
    _handle_natural_command  CC=3  out:9
    _match_heuristic_command  CC=7  out:3
    _object_based_match  CC=4  out:1
    _validate_result_with_llm  CC=14  out:16
    ask  CC=1  out:4
  fixos.cli.cleanup_cmd  [4 funcs]
    _display_service_group  CC=8  out:15
    _display_unsafe_services  CC=4  out:10
    _execute_safe_cleanup  CC=3  out:8
    _run_interactive_cleanup  CC=9  out:8
  fixos.cli.config_cmd  [7 funcs]
    _display_provider_menu  CC=5  out:21
    _env_path  CC=3  out:5
    _prompt_provider_choice  CC=5  out:10
    _save_provider_choice  CC=6  out:22
    _set_env_key  CC=5  out:10
    config_model  CC=8  out:38
    config_provider  CC=6  out:9
  fixos.cli.features_cmd  [2 funcs]
    _interactive_profile_select  CC=11  out:22
    features_audit  CC=4  out:18
  fixos.cli.fix_cmd  [2 funcs]
    _collect_diagnostics  CC=7  out:11
    _run_agent_session  CC=2  out:2
  fixos.cli.main  [3 funcs]
    _print_welcome  CC=6  out:61
    cli  CC=3  out:5
    main  CC=1  out:1
  fixos.cli.scan_cmd  [2 funcs]
    _display_disk_fix_mode  CC=6  out:11
    _run_disk_analysis  CC=12  out:20
  fixos.cli.token_cmd  [1 funcs]
    token_set  CC=7  out:29
  fixos.config  [3 funcs]
    load  CC=14  out:26
    _load_env_files  CC=13  out:14
    detect_provider_from_key  CC=3  out:1
  fixos.config_interactive  [5 funcs]
    _get_api_key  CC=4  out:9
    _get_user_choice  CC=6  out:7
    _print_provider_menu  CC=9  out:19
    _save_to_env  CC=8  out:13
    interactive_provider_setup  CC=5  out:10
  fixos.diagnostics.checks._shared  [2 funcs]
    _cmd  CC=7  out:3
    _psutil_required  CC=1  out:0
  fixos.diagnostics.checks.audio  [1 funcs]
    diagnose_audio  CC=1  out:25
  fixos.diagnostics.checks.file_analysis  [6 funcs]
    _find_archive_candidates  CC=1  out:6
    _find_downloads_cleanup  CC=1  out:3
    _find_duplicates  CC=1  out:4
    _find_large_files  CC=1  out:5
    _find_media_files  CC=1  out:10
    diagnose_files  CC=4  out:14
  fixos.diagnostics.checks.hardware  [1 funcs]
    diagnose_hardware  CC=1  out:18
  fixos.diagnostics.checks.packages  [6 funcs]
    _diagnose_desktop_apps  CC=1  out:4
    _diagnose_duplicates  CC=1  out:1
    _diagnose_flatpak  CC=1  out:5
    _diagnose_rpm_dnf  CC=1  out:16
    _diagnose_snap  CC=1  out:3
    diagnose_packages  CC=4  out:18
  fixos.diagnostics.checks.resources  [1 funcs]
    diagnose_resources  CC=13  out:49
  fixos.diagnostics.checks.security  [1 funcs]
    diagnose_security  CC=4  out:36
  fixos.diagnostics.checks.storage_optimization  [6 funcs]
    _diagnose_btrfs  CC=1  out:8
    _diagnose_filesystem_health  CC=1  out:5
    _diagnose_lvm  CC=1  out:3
    _diagnose_partitions  CC=1  out:7
    _diagnose_swap_optimization  CC=1  out:5
    diagnose_storage  CC=4  out:18
  fixos.diagnostics.checks.system_core  [3 funcs]
    _collect_os_info  CC=3  out:9
    _collect_platform_details  CC=3  out:14
    diagnose_system  CC=11  out:23
  fixos.diagnostics.checks.thumbnails  [1 funcs]
    diagnose_thumbnails  CC=1  out:21
  fixos.diagnostics.storage_analyzer  [1 funcs]
    _format_size  CC=1  out:1
  fixos.llm_shell  [3 funcs]
    _handle_user_turn  CC=8  out:16
    execute_command  CC=10  out:14
    run_llm_shell  CC=8  out:34
  fixos.orchestrator.orchestrator  [4 funcs]
    _default_confirm  CC=3  out:6
    _default_progress  CC=8  out:8
    _evaluate_and_rediagnose  CC=10  out:23
    load_from_diagnostics  CC=5  out:26
  fixos.platform_utils  [11 funcs]
    _cmd_exists  CC=1  out:1
    cancel_signal_timeout  CC=2  out:1
    elevate_cmd  CC=3  out:2
    get_os_info  CC=5  out:8
    get_package_manager  CC=8  out:3
    install_package_cmd  CC=2  out:2
    is_dangerous  CC=3  out:1
    is_interactive_blocker  CC=3  out:1
    needs_elevation  CC=5  out:7
    run_command  CC=5  out:4
  fixos.plugins.builtin.audio  [4 funcs]
    _check_alsa  CC=6  out:5
    _check_pipewire  CC=2  out:2
    _check_sof  CC=2  out:2
    _check_wireplumber  CC=2  out:2
  fixos.plugins.builtin.disk  [3 funcs]
    _check_inodes  CC=6  out:8
    _check_readonly  CC=5  out:5
    _check_usage  CC=6  out:8
  fixos.plugins.builtin.hardware  [5 funcs]
    _check_battery  CC=8  out:16
    _check_camera  CC=3  out:3
    _check_dmi  CC=3  out:4
    _check_gpu  CC=3  out:2
    _check_touchpad  CC=2  out:2
  fixos.plugins.builtin.resources  [3 funcs]
    _check_cpu  CC=5  out:5
    _check_top_processes  CC=2  out:1
    _check_zombies  CC=3  out:5
  fixos.plugins.builtin.security  [5 funcs]
    _check_fail2ban  CC=4  out:4
    _check_firewall  CC=8  out:8
    _check_open_ports  CC=7  out:8
    _check_selinux  CC=3  out:4
    _check_ssh  CC=8  out:8
  fixos.plugins.builtin.thumbnails  [4 funcs]
    _check_cache  CC=5  out:11
    _check_ffmpegthumbnailer  CC=2  out:3
    _check_gstreamer  CC=4  out:4
    _check_totem  CC=2  out:3
  fixos.system_checks  [8 funcs]
    get_cpu_info  CC=2  out:8
    get_disk_info  CC=3  out:5
    get_fedora_specific  CC=1  out:15
    get_full_diagnostics  CC=1  out:16
    get_memory_info  CC=1  out:7
    get_network_info  CC=4  out:3
    get_top_processes  CC=3  out:4
    run_cmd  CC=6  out:3
  fixos.utils.anonymizer  [9 funcs]
    _apply_regex_replacements  CC=3  out:4
    _dict_to_markdown  CC=9  out:20
    _format_diagnostics_markdown  CC=3  out:5
    _format_key_title  CC=1  out:3
    _get_sensitive  CC=4  out:3
    _render_dict_list_value  CC=6  out:7
    anonymize  CC=8  out:21
    deanonymize  CC=5  out:8
    display_anonymized_preview  CC=5  out:18
  fixos.utils.terminal  [8 funcs]
    _get_severity_style  CC=3  out:1
    _is_divider_line  CC=1  out:2
    _print_output_box  CC=2  out:8
    print_cmd_block  CC=4  out:6
    print_problem_header  CC=3  out:10
    print_stderr_box  CC=1  out:1
    print_stdout_box  CC=1  out:1
    render_md  CC=9  out:30
  fixos.utils.web_search  [9 funcs]
    _http_get  CC=2  out:4
    format_results_for_llm  CC=3  out:5
    search_all  CC=5  out:15
    search_arch_wiki  CC=9  out:11
    search_ask_fedora  CC=4  out:11
    search_ddg  CC=8  out:15
    search_fedora_bugzilla  CC=4  out:8
    search_github_issues  CC=4  out:12
    search_serpapi  CC=5  out:9
  scripts.pyqual-calibrate  [4 funcs]
    calibrate  CC=14  out:26
    extract_current_metrics  CC=4  out:9
    main  CC=6  out:12
    parse_pyqual_yaml  CC=1  out:1

EDGES:
  fixos.platform_utils.elevate_cmd → fixos.platform_utils.needs_elevation
  fixos.platform_utils.get_package_manager → fixos.platform_utils._cmd_exists
  fixos.platform_utils.install_package_cmd → fixos.platform_utils.get_package_manager
  fixos.config_interactive.interactive_provider_setup → fixos.config_interactive._print_provider_menu
  fixos.config_interactive.interactive_provider_setup → fixos.config_interactive._get_user_choice
  fixos.config_interactive.interactive_provider_setup → fixos.config_interactive._get_api_key
  fixos.config_interactive.interactive_provider_setup → fixos.config_interactive._save_to_env
  fixos.system_checks.get_fedora_specific → fixos.system_checks.run_cmd
  fixos.system_checks.get_full_diagnostics → fixos.system_checks.get_cpu_info
  fixos.system_checks.get_full_diagnostics → fixos.system_checks.get_memory_info
  fixos.system_checks.get_full_diagnostics → fixos.system_checks.get_disk_info
  fixos.system_checks.get_full_diagnostics → fixos.system_checks.get_network_info
  fixos.system_checks.get_full_diagnostics → fixos.system_checks.get_top_processes
  docker.validate-scenario.validate → docker.validate-scenario._get_nested
  docker.validate-scenario.main → docker.validate-scenario.validate
  fixos.diagnostics.checks.audio.diagnose_audio → fixos.diagnostics.checks._shared._cmd
  fixos.diagnostics.checks.resources.diagnose_resources → fixos.diagnostics.checks._shared._psutil_required
  fixos.diagnostics.checks.system_core._collect_os_info → fixos.diagnostics.checks._shared._cmd
  fixos.diagnostics.checks.system_core._collect_platform_details → fixos.diagnostics.checks._shared._cmd
  fixos.diagnostics.checks.system_core.diagnose_system → fixos.diagnostics.checks.system_core._collect_os_info
  fixos.diagnostics.checks.system_core.diagnose_system → fixos.diagnostics.checks._shared._psutil_required
  fixos.diagnostics.checks.hardware.diagnose_hardware → fixos.diagnostics.checks._shared._cmd
  fixos.diagnostics.checks.security.diagnose_security → fixos.diagnostics.checks._shared._cmd
  fixos.diagnostics.checks.thumbnails.diagnose_thumbnails → fixos.diagnostics.checks._shared._cmd
  fixos.diagnostics.checks.file_analysis.diagnose_files → fixos.diagnostics.checks.file_analysis._find_large_files
  fixos.diagnostics.checks.file_analysis.diagnose_files → fixos.diagnostics.checks.file_analysis._find_duplicates
  fixos.diagnostics.checks.file_analysis.diagnose_files → fixos.diagnostics.checks.file_analysis._find_media_files
  fixos.diagnostics.checks.file_analysis.diagnose_files → fixos.diagnostics.checks.file_analysis._find_archive_candidates
  fixos.diagnostics.checks.file_analysis.diagnose_files → fixos.diagnostics.checks.file_analysis._find_downloads_cleanup
  fixos.diagnostics.checks.file_analysis._find_large_files → fixos.diagnostics.checks._shared._cmd
  fixos.diagnostics.checks.file_analysis._find_duplicates → fixos.diagnostics.checks._shared._cmd
  fixos.diagnostics.checks.file_analysis._find_media_files → fixos.diagnostics.checks._shared._cmd
  fixos.diagnostics.checks.file_analysis._find_archive_candidates → fixos.diagnostics.checks._shared._cmd
  fixos.diagnostics.checks.file_analysis._find_downloads_cleanup → fixos.diagnostics.checks._shared._cmd
  fixos.diagnostics.checks.storage_optimization.diagnose_storage → fixos.diagnostics.checks.storage_optimization._diagnose_partitions
  fixos.diagnostics.checks.storage_optimization.diagnose_storage → fixos.diagnostics.checks.storage_optimization._diagnose_btrfs
  fixos.diagnostics.checks.storage_optimization.diagnose_storage → fixos.diagnostics.checks.storage_optimization._diagnose_lvm
  fixos.diagnostics.checks.storage_optimization.diagnose_storage → fixos.diagnostics.checks.storage_optimization._diagnose_swap_optimization
  fixos.diagnostics.checks.storage_optimization.diagnose_storage → fixos.diagnostics.checks.storage_optimization._diagnose_filesystem_health
  fixos.diagnostics.checks.storage_optimization._diagnose_partitions → fixos.diagnostics.checks._shared._cmd
  fixos.diagnostics.checks.storage_optimization._diagnose_btrfs → fixos.diagnostics.checks._shared._cmd
  fixos.diagnostics.checks.storage_optimization._diagnose_lvm → fixos.diagnostics.checks._shared._cmd
  fixos.diagnostics.checks.storage_optimization._diagnose_swap_optimization → fixos.diagnostics.checks._shared._cmd
  fixos.diagnostics.checks.storage_optimization._diagnose_filesystem_health → fixos.diagnostics.checks._shared._cmd
  fixos.diagnostics.checks.packages.diagnose_packages → fixos.diagnostics.checks.packages._diagnose_rpm_dnf
  fixos.diagnostics.checks.packages.diagnose_packages → fixos.diagnostics.checks.packages._diagnose_flatpak
  fixos.diagnostics.checks.packages.diagnose_packages → fixos.diagnostics.checks.packages._diagnose_snap
  fixos.diagnostics.checks.packages.diagnose_packages → fixos.diagnostics.checks.packages._diagnose_duplicates
  fixos.diagnostics.checks.packages.diagnose_packages → fixos.diagnostics.checks.packages._diagnose_desktop_apps
  fixos.diagnostics.checks.packages._diagnose_rpm_dnf → fixos.diagnostics.checks._shared._cmd
```

## Test Contracts

*Scenarios as contract signatures — what the system guarantees.*

### Cli (1)

**`CLI Command Tests`**

### Integration (1)

**`Auto-generated from Python Tests`**

## Refactoring Analysis

*Pre-refactoring snapshot — use this section to identify targets. Generated from `project/` toon files.*

### Call Graph & Complexity (`project/calls.toon.yaml`)

```toon markpact:analysis path=project/calls.toon.yaml
# code2llm call graph | /home/tom/github/wronai/fixOS
# generated in 0.10s
# nodes: 225 | edges: 227 | modules: 50
# CC̄=4.3

HUBS[20]:
  fixos.diagnostics.checks._shared._cmd
    CC=7  in:241  out:3  total:244
  fixos.cli._cleanup_flatpak._cleanup_flatpak_detailed
    CC=12  in:1  out:111  total:112
  fixos.cli._cleanup_system._display_full_system_menu
    CC=12  in:1  out:79  total:80
  fixos.cli._cleanup_flatpak._display_flatpak_status
    CC=9  in:1  out:65  total:66
  fixos.cli.main._print_welcome
    CC=6  in:1  out:61  total:62
  fixos.cli._cleanup_system._handle_interactive_select
    CC=14  in:1  out:52  total:53
  fixos.cli._cleanup_home._handle_home_analysis
    CC=11  in:1  out:49  total:50
  fixos.diagnostics.checks.resources.diagnose_resources
    CC=13  in:0  out:49  total:49
  fixos.cli._cleanup_system._execute_full_cleanup
    CC=8  in:1  out:37  total:38
  fixos.cli.config_cmd.config_model
    CC=8  in:0  out:38  total:38
  fixos.platform_utils.run_command
    CC=5  in:33  out:4  total:37
  fixos.diagnostics.checks.security.diagnose_security
    CC=4  in:0  out:36  total:36
  fixos.llm_shell.run_llm_shell
    CC=8  in:0  out:34  total:34
  fixos.cli._cleanup_utils._format_bytes
    CC=1  in:32  out:1  total:33
  fixos.utils.terminal.render_md
    CC=9  in:0  out:30  total:30
  fixos.cli.token_cmd.token_set
    CC=7  in:0  out:29  total:29
  fixos.anonymizer.anonymize
    CC=5  in:14  out:14  total:28
  docker.validate-scenario.main
    CC=7  in:0  out:27  total:27
  scripts.pyqual-calibrate.calibrate
    CC=14  in:1  out:26  total:27
  fixos.config.FixOsConfig.load
    CC=14  in:0  out:26  total:26

MODULES:
  docker.validate-scenario  [3 funcs]
    _get_nested  CC=4  out:2
    main  CC=7  out:27
    validate  CC=11  out:18
  docs.examples.quickstart  [1 funcs]
    run_autonomous_session  CC=1  out:0
  fixos.agent  [1 funcs]
    get_remaining_time  CC=2  out:4
  fixos.agent.autonomous_session  [5 funcs]
    _get_remaining_time  CC=1  out:1
    _handle_exec  CC=4  out:17
    _handle_llm_error  CC=4  out:3
    _handle_search  CC=3  out:8
    _initialize_messages  CC=2  out:3
  fixos.agent.hitl  [1 funcs]
    run_hitl_session  CC=1  out:2
  fixos.agent.hitl_session  [8 funcs]
    __init__  CC=2  out:5
    _check_low_confidence  CC=7  out:8
    _clear_timeout  CC=1  out:1
    _handle_llm_error  CC=4  out:4
    _initialize_messages  CC=3  out:5
    _process_turn  CC=8  out:17
    _setup_timeout  CC=1  out:3
    remaining  CC=1  out:1
  fixos.agent.session_core  [10 funcs]
    _deduplicate  CC=5  out:4
    _extract_co_robi  CC=2  out:3
    _is_diagnostic_only_command  CC=3  out:2
    _is_part_diagnostic_only  CC=6  out:6
    _pattern_backticks  CC=3  out:6
    _pattern_fallbacks  CC=6  out:13
    _pattern_no_backticks  CC=3  out:7
    _pattern_strict_bold  CC=4  out:6
    extract_fixes  CC=4  out:5
    extract_search_topic  CC=3  out:4
  fixos.agent.session_handlers  [11 funcs]
    _resolve_command_timeout  CC=6  out:6
    _sort_fixes_by_priority  CC=1  out:6
    handle_describe_problem  CC=2  out:2
    handle_direct_command  CC=1  out:5
    handle_execute_all  CC=4  out:10
    handle_fix_by_number  CC=2  out:9
    handle_quit  CC=1  out:1
    handle_search  CC=2  out:6
    handle_skip_all  CC=1  out:1
    parse_user_input  CC=9  out:11
  fixos.agent.session_io  [10 funcs]
    ask_execute_prompt  CC=1  out:4
    ask_low_confidence_search  CC=1  out:4
    ask_send_data  CC=1  out:4
    ask_user_problem  CC=2  out:11
    fmt_time  CC=1  out:0
    get_user_input  CC=2  out:4
    print_cmd_result  CC=8  out:13
    print_session_header  CC=1  out:8
    print_session_summary  CC=3  out:4
    suspend_timeout  CC=4  out:3
  fixos.anonymizer  [2 funcs]
    anonymize  CC=5  out:14
    get_sensitive_values  CC=4  out:3
  fixos.cli._cleanup_flatpak  [2 funcs]
    _cleanup_flatpak_detailed  CC=12  out:111
    _display_flatpak_status  CC=9  out:65
  fixos.cli._cleanup_home  [3 funcs]
    _display_home_items  CC=7  out:17
    _handle_home_analysis  CC=11  out:49
    _resolve_home_selection  CC=4  out:8
  fixos.cli._cleanup_snap  [6 funcs]
    _handle_snap_management  CC=9  out:21
    _snap_display_packages  CC=3  out:12
    _snap_fetch_packages  CC=6  out:8
    _snap_remove_packages  CC=4  out:10
    _snap_select_packages  CC=5  out:9
    _snap_warn_dangerous  CC=5  out:5
  fixos.cli._cleanup_system  [12 funcs]
    _cleanup_full_system  CC=8  out:12
    _dispatch_system_selection  CC=6  out:6
    _display_full_system_menu  CC=12  out:79
    _execute_full_cleanup  CC=8  out:37
    _filter_by_age  CC=6  out:8
    _filter_by_prefix_category  CC=6  out:12
    _filter_by_prefix_top  CC=3  out:7
    _filter_by_prefix_type  CC=10  out:14
    _filter_large  CC=4  out:5
    _handle_interactive_select  CC=14  out:52
  fixos.cli._cleanup_utils  [3 funcs]
    _build_dep_types  CC=4  out:2
    _format_bytes  CC=1  out:1
    _parse_numeric_range_set  CC=5  out:10
  fixos.cli.ask_cmd  [9 funcs]
    _build_output_dict  CC=8  out:0
    _execute_heuristic_command  CC=9  out:12
    _execute_with_llm  CC=8  out:21
    _format_command  CC=5  out:7
    _handle_natural_command  CC=3  out:9
    _match_heuristic_command  CC=7  out:3
    _object_based_match  CC=4  out:1
    _validate_result_with_llm  CC=14  out:16
    ask  CC=1  out:4
  fixos.cli.cleanup_cmd  [4 funcs]
    _display_service_group  CC=8  out:15
    _display_unsafe_services  CC=4  out:10
    _execute_safe_cleanup  CC=3  out:8
    _run_interactive_cleanup  CC=9  out:8
  fixos.cli.config_cmd  [7 funcs]
    _display_provider_menu  CC=5  out:21
    _env_path  CC=3  out:5
    _prompt_provider_choice  CC=5  out:10
    _save_provider_choice  CC=6  out:22
    _set_env_key  CC=5  out:10
    config_model  CC=8  out:38
    config_provider  CC=6  out:9
  fixos.cli.features_cmd  [2 funcs]
    _interactive_profile_select  CC=11  out:22
    features_audit  CC=4  out:18
  fixos.cli.fix_cmd  [2 funcs]
    _collect_diagnostics  CC=7  out:11
    _run_agent_session  CC=2  out:2
  fixos.cli.main  [3 funcs]
    _print_welcome  CC=6  out:61
    cli  CC=3  out:5
    main  CC=1  out:1
  fixos.cli.scan_cmd  [2 funcs]
    _display_disk_fix_mode  CC=6  out:11
    _run_disk_analysis  CC=12  out:20
  fixos.cli.token_cmd  [1 funcs]
    token_set  CC=7  out:29
  fixos.config  [3 funcs]
    load  CC=14  out:26
    _load_env_files  CC=13  out:14
    detect_provider_from_key  CC=3  out:1
  fixos.config_interactive  [5 funcs]
    _get_api_key  CC=4  out:9
    _get_user_choice  CC=6  out:7
    _print_provider_menu  CC=9  out:19
    _save_to_env  CC=8  out:13
    interactive_provider_setup  CC=5  out:10
  fixos.diagnostics.checks._shared  [2 funcs]
    _cmd  CC=7  out:3
    _psutil_required  CC=1  out:0
  fixos.diagnostics.checks.audio  [1 funcs]
    diagnose_audio  CC=1  out:25
  fixos.diagnostics.checks.file_analysis  [6 funcs]
    _find_archive_candidates  CC=1  out:6
    _find_downloads_cleanup  CC=1  out:3
    _find_duplicates  CC=1  out:4
    _find_large_files  CC=1  out:5
    _find_media_files  CC=1  out:10
    diagnose_files  CC=4  out:14
  fixos.diagnostics.checks.hardware  [1 funcs]
    diagnose_hardware  CC=1  out:18
  fixos.diagnostics.checks.packages  [6 funcs]
    _diagnose_desktop_apps  CC=1  out:4
    _diagnose_duplicates  CC=1  out:1
    _diagnose_flatpak  CC=1  out:5
    _diagnose_rpm_dnf  CC=1  out:16
    _diagnose_snap  CC=1  out:3
    diagnose_packages  CC=4  out:18
  fixos.diagnostics.checks.resources  [1 funcs]
    diagnose_resources  CC=13  out:49
  fixos.diagnostics.checks.security  [1 funcs]
    diagnose_security  CC=4  out:36
  fixos.diagnostics.checks.storage_optimization  [6 funcs]
    _diagnose_btrfs  CC=1  out:8
    _diagnose_filesystem_health  CC=1  out:5
    _diagnose_lvm  CC=1  out:3
    _diagnose_partitions  CC=1  out:7
    _diagnose_swap_optimization  CC=1  out:5
    diagnose_storage  CC=4  out:18
  fixos.diagnostics.checks.system_core  [3 funcs]
    _collect_os_info  CC=3  out:9
    _collect_platform_details  CC=3  out:14
    diagnose_system  CC=11  out:23
  fixos.diagnostics.checks.thumbnails  [1 funcs]
    diagnose_thumbnails  CC=1  out:21
  fixos.diagnostics.storage_analyzer  [1 funcs]
    _format_size  CC=1  out:1
  fixos.llm_shell  [3 funcs]
    _handle_user_turn  CC=8  out:16
    execute_command  CC=10  out:14
    run_llm_shell  CC=8  out:34
  fixos.orchestrator.orchestrator  [4 funcs]
    _default_confirm  CC=3  out:6
    _default_progress  CC=8  out:8
    _evaluate_and_rediagnose  CC=10  out:23
    load_from_diagnostics  CC=5  out:26
  fixos.platform_utils  [11 funcs]
    _cmd_exists  CC=1  out:1
    cancel_signal_timeout  CC=2  out:1
    elevate_cmd  CC=3  out:2
    get_os_info  CC=5  out:8
    get_package_manager  CC=8  out:3
    install_package_cmd  CC=2  out:2
    is_dangerous  CC=3  out:1
    is_interactive_blocker  CC=3  out:1
    needs_elevation  CC=5  out:7
    run_command  CC=5  out:4
  fixos.plugins.builtin.audio  [4 funcs]
    _check_alsa  CC=6  out:5
    _check_pipewire  CC=2  out:2
    _check_sof  CC=2  out:2
    _check_wireplumber  CC=2  out:2
  fixos.plugins.builtin.disk  [3 funcs]
    _check_inodes  CC=6  out:8
    _check_readonly  CC=5  out:5
    _check_usage  CC=6  out:8
  fixos.plugins.builtin.hardware  [5 funcs]
    _check_battery  CC=8  out:16
    _check_camera  CC=3  out:3
    _check_dmi  CC=3  out:4
    _check_gpu  CC=3  out:2
    _check_touchpad  CC=2  out:2
  fixos.plugins.builtin.resources  [3 funcs]
    _check_cpu  CC=5  out:5
    _check_top_processes  CC=2  out:1
    _check_zombies  CC=3  out:5
  fixos.plugins.builtin.security  [5 funcs]
    _check_fail2ban  CC=4  out:4
    _check_firewall  CC=8  out:8
    _check_open_ports  CC=7  out:8
    _check_selinux  CC=3  out:4
    _check_ssh  CC=8  out:8
  fixos.plugins.builtin.thumbnails  [4 funcs]
    _check_cache  CC=5  out:11
    _check_ffmpegthumbnailer  CC=2  out:3
    _check_gstreamer  CC=4  out:4
    _check_totem  CC=2  out:3
  fixos.system_checks  [8 funcs]
    get_cpu_info  CC=2  out:8
    get_disk_info  CC=3  out:5
    get_fedora_specific  CC=1  out:15
    get_full_diagnostics  CC=1  out:16
    get_memory_info  CC=1  out:7
    get_network_info  CC=4  out:3
    get_top_processes  CC=3  out:4
    run_cmd  CC=6  out:3
  fixos.utils.anonymizer  [9 funcs]
    _apply_regex_replacements  CC=3  out:4
    _dict_to_markdown  CC=9  out:20
    _format_diagnostics_markdown  CC=3  out:5
    _format_key_title  CC=1  out:3
    _get_sensitive  CC=4  out:3
    _render_dict_list_value  CC=6  out:7
    anonymize  CC=8  out:21
    deanonymize  CC=5  out:8
    display_anonymized_preview  CC=5  out:18
  fixos.utils.terminal  [8 funcs]
    _get_severity_style  CC=3  out:1
    _is_divider_line  CC=1  out:2
    _print_output_box  CC=2  out:8
    print_cmd_block  CC=4  out:6
    print_problem_header  CC=3  out:10
    print_stderr_box  CC=1  out:1
    print_stdout_box  CC=1  out:1
    render_md  CC=9  out:30
  fixos.utils.web_search  [9 funcs]
    _http_get  CC=2  out:4
    format_results_for_llm  CC=3  out:5
    search_all  CC=5  out:15
    search_arch_wiki  CC=9  out:11
    search_ask_fedora  CC=4  out:11
    search_ddg  CC=8  out:15
    search_fedora_bugzilla  CC=4  out:8
    search_github_issues  CC=4  out:12
    search_serpapi  CC=5  out:9
  scripts.pyqual-calibrate  [4 funcs]
    calibrate  CC=14  out:26
    extract_current_metrics  CC=4  out:9
    main  CC=6  out:12
    parse_pyqual_yaml  CC=1  out:1

EDGES:
  fixos.platform_utils.elevate_cmd → fixos.platform_utils.needs_elevation
  fixos.platform_utils.get_package_manager → fixos.platform_utils._cmd_exists
  fixos.platform_utils.install_package_cmd → fixos.platform_utils.get_package_manager
  fixos.config_interactive.interactive_provider_setup → fixos.config_interactive._print_provider_menu
  fixos.config_interactive.interactive_provider_setup → fixos.config_interactive._get_user_choice
  fixos.config_interactive.interactive_provider_setup → fixos.config_interactive._get_api_key
  fixos.config_interactive.interactive_provider_setup → fixos.config_interactive._save_to_env
  fixos.system_checks.get_fedora_specific → fixos.system_checks.run_cmd
  fixos.system_checks.get_full_diagnostics → fixos.system_checks.get_cpu_info
  fixos.system_checks.get_full_diagnostics → fixos.system_checks.get_memory_info
  fixos.system_checks.get_full_diagnostics → fixos.system_checks.get_disk_info
  fixos.system_checks.get_full_diagnostics → fixos.system_checks.get_network_info
  fixos.system_checks.get_full_diagnostics → fixos.system_checks.get_top_processes
  docker.validate-scenario.validate → docker.validate-scenario._get_nested
  docker.validate-scenario.main → docker.validate-scenario.validate
  fixos.diagnostics.checks.audio.diagnose_audio → fixos.diagnostics.checks._shared._cmd
  fixos.diagnostics.checks.resources.diagnose_resources → fixos.diagnostics.checks._shared._psutil_required
  fixos.diagnostics.checks.system_core._collect_os_info → fixos.diagnostics.checks._shared._cmd
  fixos.diagnostics.checks.system_core._collect_platform_details → fixos.diagnostics.checks._shared._cmd
  fixos.diagnostics.checks.system_core.diagnose_system → fixos.diagnostics.checks.system_core._collect_os_info
  fixos.diagnostics.checks.system_core.diagnose_system → fixos.diagnostics.checks._shared._psutil_required
  fixos.diagnostics.checks.hardware.diagnose_hardware → fixos.diagnostics.checks._shared._cmd
  fixos.diagnostics.checks.security.diagnose_security → fixos.diagnostics.checks._shared._cmd
  fixos.diagnostics.checks.thumbnails.diagnose_thumbnails → fixos.diagnostics.checks._shared._cmd
  fixos.diagnostics.checks.file_analysis.diagnose_files → fixos.diagnostics.checks.file_analysis._find_large_files
  fixos.diagnostics.checks.file_analysis.diagnose_files → fixos.diagnostics.checks.file_analysis._find_duplicates
  fixos.diagnostics.checks.file_analysis.diagnose_files → fixos.diagnostics.checks.file_analysis._find_media_files
  fixos.diagnostics.checks.file_analysis.diagnose_files → fixos.diagnostics.checks.file_analysis._find_archive_candidates
  fixos.diagnostics.checks.file_analysis.diagnose_files → fixos.diagnostics.checks.file_analysis._find_downloads_cleanup
  fixos.diagnostics.checks.file_analysis._find_large_files → fixos.diagnostics.checks._shared._cmd
  fixos.diagnostics.checks.file_analysis._find_duplicates → fixos.diagnostics.checks._shared._cmd
  fixos.diagnostics.checks.file_analysis._find_media_files → fixos.diagnostics.checks._shared._cmd
  fixos.diagnostics.checks.file_analysis._find_archive_candidates → fixos.diagnostics.checks._shared._cmd
  fixos.diagnostics.checks.file_analysis._find_downloads_cleanup → fixos.diagnostics.checks._shared._cmd
  fixos.diagnostics.checks.storage_optimization.diagnose_storage → fixos.diagnostics.checks.storage_optimization._diagnose_partitions
  fixos.diagnostics.checks.storage_optimization.diagnose_storage → fixos.diagnostics.checks.storage_optimization._diagnose_btrfs
  fixos.diagnostics.checks.storage_optimization.diagnose_storage → fixos.diagnostics.checks.storage_optimization._diagnose_lvm
  fixos.diagnostics.checks.storage_optimization.diagnose_storage → fixos.diagnostics.checks.storage_optimization._diagnose_swap_optimization
  fixos.diagnostics.checks.storage_optimization.diagnose_storage → fixos.diagnostics.checks.storage_optimization._diagnose_filesystem_health
  fixos.diagnostics.checks.storage_optimization._diagnose_partitions → fixos.diagnostics.checks._shared._cmd
  fixos.diagnostics.checks.storage_optimization._diagnose_btrfs → fixos.diagnostics.checks._shared._cmd
  fixos.diagnostics.checks.storage_optimization._diagnose_lvm → fixos.diagnostics.checks._shared._cmd
  fixos.diagnostics.checks.storage_optimization._diagnose_swap_optimization → fixos.diagnostics.checks._shared._cmd
  fixos.diagnostics.checks.storage_optimization._diagnose_filesystem_health → fixos.diagnostics.checks._shared._cmd
  fixos.diagnostics.checks.packages.diagnose_packages → fixos.diagnostics.checks.packages._diagnose_rpm_dnf
  fixos.diagnostics.checks.packages.diagnose_packages → fixos.diagnostics.checks.packages._diagnose_flatpak
  fixos.diagnostics.checks.packages.diagnose_packages → fixos.diagnostics.checks.packages._diagnose_snap
  fixos.diagnostics.checks.packages.diagnose_packages → fixos.diagnostics.checks.packages._diagnose_duplicates
  fixos.diagnostics.checks.packages.diagnose_packages → fixos.diagnostics.checks.packages._diagnose_desktop_apps
  fixos.diagnostics.checks.packages._diagnose_rpm_dnf → fixos.diagnostics.checks._shared._cmd
```

### Code Analysis (`project/analysis.toon.yaml`)

```toon markpact:analysis path=project/analysis.toon.yaml
# code2llm | 142f 22670L | python:107,yaml:14,shell:3,yml:3,txt:2,toml:1,ini:1 | 2026-05-08
# generated in 0.03s
# CC̄=4.3 | critical:0/632 | dups:0 | cycles:0

HEALTH[0]: ok

REFACTOR[0]: none needed

PIPELINES[419]:
  [1] Src [install_package_cmd]: install_package_cmd → get_package_manager → _cmd_exists
      PURITY: 100% pure
  [2] Src [get_largest_apps]: get_largest_apps
      PURITY: 100% pure
  [3] Src [get_cleanup_summary]: get_cleanup_summary
      PURITY: 100% pure
  [4] Src [_rec_repo_bloat]: _rec_repo_bloat
      PURITY: 100% pure
  [5] Src [_rec_duplicates]: _rec_duplicates
      PURITY: 100% pure

LAYERS:
  scripts/                        CC̄=5.4    ←in:0  →out:0
  │ pyqual-calibrate           299L  0C    7m  CC=14     ←0
  │
  fixos/                          CC̄=4.4    ←in:62  →out:0
  │ service_cleanup            474L  1C   10m  CC=14     ←0
  │ _cleanup_system            444L  0C   17m  CC=14     ←1
  │ autonomous_session         441L  3C   22m  CC=8      ←0
  │ disk_analyzer              429L  1C   15m  CC=13     ←0
  │ config                     425L  1C    7m  CC=14     ←1
  │ cleanup_planner            413L  4C   16m  CC=12     ←0
  │ dev_project_analyzer       407L  2C   13m  CC=11     ←0
  │ orchestrator               395L  2C   13m  CC=10     ←0
  │ ask_cmd                    354L  0C    9m  CC=14     ←0
  │ _storage_user_mixin        348L  1C   11m  CC=13     ←0
  │ file_analysis              334L  0C    6m  CC=4      ←0
  │ llm_analyzer               333L  2C    8m  CC=13     ←0
  │ terminal                   321L  1C   12m  CC=9      ←2
  │ packages.yaml              316L  0C    0m  CC=0.0    ←0
  │ session_handlers           315L  0C   12m  CC=9      ←0
  │ anonymizer                 315L  1C   14m  CC=9      ←3
  │ fix_cmd                    306L  0C    6m  CC=13     ←0
  │ _flatpak_analysis_mixin    298L  1C   11m  CC=14     ←0
  │ executor                   288L  4C   12m  CC=10     ←0
  │ storage_analyzer           274L  2C   11m  CC=11     ←1
  │ __init__                   260L  2C   12m  CC=13     ←0
  │ _flatpak_recommendations_mixin   259L  1C    9m  CC=8      ←0
  │ _storage_system_mixin      259L  1C   10m  CC=7      ←0
  │ session_io                 258L  0C   26m  CC=8      ←0
  │ web_search                 254L  1C    9m  CC=9      ←3
  │ scan_cmd                   252L  0C    6m  CC=14     ←1
  │ cleanup_cmd                250L  0C    9m  CC=11     ←0
  │ service_scanner            250L  3C    8m  CC=7      ←0
  │ provider_cmd               250L  0C    3m  CC=9      ←0
  │ llm_shell                  236L  0C    6m  CC=10     ←0
  │ session_core               234L  1C   10m  CC=6      ←1
  │ config_cmd                 234L  0C   11m  CC=8      ←0
  │ _flatpak_execution_mixin   232L  1C    7m  CC=10     ←0
  │ service_details            230L  1C    9m  CC=9      ←0
  │ _cleanup_flatpak           229L  0C    3m  CC=12     ←1
  │ storage_optimization       224L  0C    6m  CC=4      ←0
  │ hitl_session               221L  1C   12m  CC=8      ←0
  │ packages                   220L  0C    6m  CC=4      ←0
  │ llm                        211L  2C    7m  CC=10     ←0
  │ platform_utils             202L  0C   11m  CC=8      ←9
  │ security                   184L  1C    9m  CC=8      ←0
  │ features_cmd               183L  0C    8m  CC=11     ←0
  │ installer                  178L  1C   12m  CC=11     ←0
  │ graph                      163L  2C   11m  CC=13     ←0
  │ rollback                   162L  2C    6m  CC=7      ←0
  │ flatpak_analyzer           161L  3C    7m  CC=10     ←0
  │ main                       158L  0C    3m  CC=6      ←0
  │ output_formatter           158L  2C   12m  CC=3      ←0
  │ system_checks              156L  0C    8m  CC=6      ←2
  │ _storage_container_mixin   155L  1C    7m  CC=13     ←0
  │ config_interactive         149L  0C    5m  CC=9      ←1
  │ resources                  137L  1C    6m  CC=14     ←0
  │ orchestrate_cmd            132L  0C    1m  CC=13     ←0
  │ _cleanup_home              132L  0C    5m  CC=11     ←1
  │ report_cmd                 130L  0C    5m  CC=5      ←0
  │ hardware                   129L  1C    6m  CC=12     ←0
  │ registry                   127L  1C    8m  CC=7      ←0
  │ auditor                    127L  2C    5m  CC=10     ←0
  │ system_core                124L  0C    3m  CC=11     ←0
  │ renderer                   124L  1C    4m  CC=8      ←0
  │ token_cmd                  124L  0C    4m  CC=7      ←0
  │ constants                  121L  0C    0m  CC=0.0    ←0
  │ watch                      120L  1C    5m  CC=12     ←0
  │ catalog                    119L  3C    7m  CC=7      ←0
  │ thumbnails                 118L  1C    5m  CC=10     ←0
  │ _cleanup_snap              116L  0C    6m  CC=9      ←1
  │ _cleanup_utils             114L  0C    6m  CC=9      ←4
  │ disk                       113L  1C    4m  CC=12     ←0
  │ audio                      107L  1C    5m  CC=10     ←0
  │ resources                   99L  0C    1m  CC=13     ←0
  │ base                        99L  4C    4m  CC=2      ←0
  │ security                    92L  0C    1m  CC=4      ←0
  │ rollback_cmd                90L  0C    4m  CC=7      ←0
  │ profiles                    88L  1C    4m  CC=8      ←0
  │ anonymizer                  86L  0C    2m  CC=5      ←6
  │ system_checks               82L  0C    1m  CC=7      ←0
  │ quickfix_cmd                76L  0C    1m  CC=12     ←0
  │ schemas                     71L  5C    0m  CC=0.0    ←0
  │ __init__                    65L  1C    3m  CC=4      ←0
  │ thumbnails                  62L  0C    1m  CC=1      ←0
  │ shared                      62L  1C    3m  CC=6      ←0
  │ audio                       61L  0C    1m  CC=1      ←0
  │ profile_cmd                 59L  0C    3m  CC=4      ←0
  │ autonomous                  49L  0C    1m  CC=1      ←0
  │ history_cmd                 49L  0C    1m  CC=5      ←0
  │ watch_cmd                   49L  0C    1m  CC=2      ←0
  │ _shared                     45L  0C    2m  CC=7      ←9
  │ hardware                    42L  0C    1m  CC=1      ←0
  │ __init__                    38L  0C    1m  CC=2      ←3
  │ hitl                        36L  0C    1m  CC=1      ←1
  │ __init__                    26L  0C    0m  CC=0.0    ←0
  │ timeout                     17L  1C    1m  CC=1      ←0
  │ sysadmin.yaml               13L  0C    0m  CC=0.0    ←0
  │ developer.yaml              13L  0C    0m  CC=0.0    ←0
  │ utils                       12L  0C    1m  CC=3      ←0
  │ desktop.yaml                12L  0C    0m  CC=0.0    ←0
  │ __init__                    11L  0C    0m  CC=0.0    ←0
  │ server.yaml                 11L  0C    0m  CC=0.0    ←0
  │ developer.yaml              10L  0C    0m  CC=0.0    ←0
  │ office.yaml                  9L  0C    0m  CC=0.0    ←0
  │ __init__                     9L  0C    0m  CC=0.0    ←0
  │ __init__                     8L  0C    0m  CC=0.0    ←0
  │ minimal.yaml                 5L  0C    0m  CC=0.0    ←0
  │ __init__                     3L  0C    0m  CC=0.0    ←0
  │ __init__                     2L  0C    0m  CC=0.0    ←0
  │ __init__                     2L  0C    0m  CC=0.0    ←0
  │ __init__                     2L  0C    0m  CC=0.0    ←0
  │ __init__                     2L  0C    0m  CC=0.0    ←0
  │ __init__                     1L  0C    0m  CC=0.0    ←0
  │ __init__                     0L  0C    0m  CC=0.0    ←0
  │
  docker/                         CC̄=3.1    ←in:0  →out:0
  │ docker-compose.yml         176L  0C    0m  CC=0.0    ←0
  │ docker-compose.multi-system.yml   160L  0C    0m  CC=0.0    ←0
  │ validate-scenario          158L  0C    3m  CC=11     ←0
  │ test-scenarios.sh          147L  0C    3m  CC=0.0    ←0
  │ test-multi-system.sh       128L  0C    1m  CC=0.0    ←0
  │ Dockerfile                  78L  0C    0m  CC=0.0    ←0
  │ Dockerfile                  63L  0C    0m  CC=0.0    ←0
  │ Dockerfile                  48L  0C    0m  CC=0.0    ←0
  │ Dockerfile                  38L  0C    0m  CC=0.0    ←0
  │ Dockerfile                  36L  0C    0m  CC=0.0    ←0
  │ Dockerfile                  33L  0C    0m  CC=0.0    ←0
  │ Dockerfile                  33L  0C    0m  CC=0.0    ←0
  │ Dockerfile                  31L  0C    0m  CC=0.0    ←0
  │ Dockerfile                  31L  0C    0m  CC=0.0    ←0
  │ Dockerfile                  29L  0C    0m  CC=0.0    ←0
  │
  docs/                           CC̄=1.0    ←in:0  →out:0
  │ mkdocs.yml                  20L  0C    0m  CC=0.0    ←0
  │ quickstart                  14L  0C    1m  CC=1      ←1
  │ advanced_usage               9L  0C    0m  CC=0.0    ←0
  │
  ./                              CC̄=0.0    ←in:0  →out:0
  │ !! planfile.yaml             2450L  0C    0m  CC=0.0    ←0
  │ goal.yaml                  429L  0C    0m  CC=0.0    ←0
  │ Makefile                   179L  0C    0m  CC=0.0    ←0
  │ pyqual.yaml                121L  0C    0m  CC=0.0    ←0
  │ pyproject.toml             108L  0C    0m  CC=0.0    ←0
  │ prefact.yaml                82L  0C    0m  CC=0.0    ←0
  │ project.sh                  50L  0C    0m  CC=0.0    ←0
  │ setup                       45L  0C    0m  CC=0.0    ←0
  │ requirements.txt            31L  0C    0m  CC=0.0    ←0
  │ requirements-dev.txt        14L  0C    0m  CC=0.0    ←0
  │ pytest.ini                  12L  0C    0m  CC=0.0    ←0
  │
  testql-scenarios/               CC̄=0.0    ←in:0  →out:0
  │ generated-cli-tests.testql.toon.yaml    20L  0C    0m  CC=0.0    ←0
  │ generated-from-pytests.testql.toon.yaml    14L  0C    0m  CC=0.0    ←0
  │
  ── zero ──
     fixos/interactive/__init__.py             0L

COUPLING:
                                   fixos         fixos.agent       fixos.plugins         fixos.utils           fixos.cli  fixos.orchestrator       docs.examples   fixos.diagnostics
               fixos                  ──                 ←21                 ←32                                      ←5                  ←4                                          hub
         fixos.agent                  21                  ──                                      17                  ←1                                                              !! fan-out
       fixos.plugins                  32                                      ──                                                                                                      !! fan-out
         fixos.utils                                     ←17                                      ──                                      ←4                                          hub
           fixos.cli                   5                   1                                                          ──                                       1                   1  !! fan-out
  fixos.orchestrator                   4                                                           4                                      ──                                          !! fan-out
       docs.examples                                                                                                  ←1                                      ──                    
   fixos.diagnostics                                                                                                  ←1                                                          ──
  CYCLES: none
  HUB: fixos.utils/ (fan-in=21)
  HUB: fixos/ (fan-in=62)
  SMELL: fixos.plugins/ fan-out=32 → split needed
  SMELL: fixos.orchestrator/ fan-out=8 → split needed
  SMELL: fixos.cli/ fan-out=8 → split needed
  SMELL: fixos.agent/ fan-out=38 → split needed

EXTERNAL:
  validation: run `vallm batch .` → validation.toon
  duplication: run `redup scan .` → duplication.toon
```

### Duplication (`project/duplication.toon.yaml`)

```toon markpact:analysis path=project/duplication.toon.yaml
# redup/duplication | 6 groups | 108f 17815L | 2026-05-08

SUMMARY:
  files_scanned: 108
  total_lines:   17815
  dup_groups:    6
  dup_fragments: 20
  saved_lines:   125
  scan_ms:       2963

HOTSPOTS[7] (files with most duplication):
  fixos/diagnostics/checks/storage_optimization.py  dup=72L  groups=2  frags=3  (0.4%)
  fixos/diagnostics/checks/file_analysis.py  dup=31L  groups=1  frags=1  (0.2%)
  fixos/agent/session_io.py  dup=18L  groups=1  frags=6  (0.1%)
  fixos/diagnostics/checks/packages.py  dup=13L  groups=1  frags=1  (0.1%)
  fixos/utils/terminal.py  dup=12L  groups=2  frags=3  (0.1%)
  fixos/config.py  dup=6L  groups=1  frags=1  (0.0%)
  fixos/cli/config_cmd.py  dup=3L  groups=1  frags=1  (0.0%)

DUPLICATES[6] (ranked by impact):
  [d99fe7887f5bb9b3] ! STRU  _find_downloads_cleanup  L=31 N=3 saved=62 sim=1.00
      fixos/diagnostics/checks/file_analysis.py:304-334  (_find_downloads_cleanup)
      fixos/diagnostics/checks/packages.py:157-169  (_diagnose_snap)
      fixos/diagnostics/checks/storage_optimization.py:149-166  (_diagnose_lvm)
  [7044c2beaaab5aff]   STRU  _diagnose_swap_optimization  L=27 N=2 saved=27 sim=1.00
      fixos/diagnostics/checks/storage_optimization.py:169-195  (_diagnose_swap_optimization)
      fixos/diagnostics/checks/storage_optimization.py:198-224  (_diagnose_filesystem_health)
  [8967cd01b62426bf]   STRU  print_timeout  L=3 N=6 saved=15 sim=1.00
      fixos/agent/session_io.py:191-193  (print_timeout)
      fixos/agent/session_io.py:196-198  (print_session_ended)
      fixos/agent/session_io.py:201-203  (print_session_interrupted)
      fixos/agent/session_io.py:211-213  (print_no_commands)
      fixos/agent/session_io.py:221-223  (print_no_results)
      fixos/agent/session_io.py:226-228  (print_searching)
  [90e6c0a8cb78d015]   STRU  config  L=3 N=5 saved=12 sim=1.00
      fixos/cli/config_cmd.py:34-36  (config)
      fixos/cli/features_cmd.py:21-23  (features)
      fixos/cli/profile_cmd.py:8-10  (profile)
      fixos/cli/rollback_cmd.py:9-11  (rollback)
      fixos/cli/token_cmd.py:10-12  (token)
  [153ba9750386f724]   STRU  detect_provider_from_key  L=6 N=2 saved=6 sim=1.00
      fixos/config.py:395-400  (detect_provider_from_key)
      fixos/utils/terminal.py:87-92  (_get_severity_style)
  [b3fdeb0b589def20]   STRU  print_stdout_box  L=3 N=2 saved=3 sim=1.00
      fixos/utils/terminal.py:204-206  (print_stdout_box)
      fixos/utils/terminal.py:209-211  (print_stderr_box)

REFACTOR[6] (ranked by priority):
  [1] ◐ extract_function   → fixos/diagnostics/checks/utils/_find_downloads_cleanup.py
      WHY: 3 occurrences of 31-line block across 3 files — saves 62 lines
      FILES: fixos/diagnostics/checks/file_analysis.py, fixos/diagnostics/checks/packages.py, fixos/diagnostics/checks/storage_optimization.py
  [2] ○ extract_function   → fixos/diagnostics/checks/utils/_diagnose_swap_optimization.py
      WHY: 2 occurrences of 27-line block across 1 files — saves 27 lines
      FILES: fixos/diagnostics/checks/storage_optimization.py
  [3] ○ extract_function   → fixos/agent/utils/print_timeout.py
      WHY: 6 occurrences of 3-line block across 1 files — saves 15 lines
      FILES: fixos/agent/session_io.py
  [4] ○ extract_function   → fixos/cli/utils/config.py
      WHY: 5 occurrences of 3-line block across 5 files — saves 12 lines
      FILES: fixos/cli/config_cmd.py, fixos/cli/features_cmd.py, fixos/cli/profile_cmd.py, fixos/cli/rollback_cmd.py, fixos/cli/token_cmd.py
  [5] ○ extract_function   → fixos/utils/detect_provider_from_key.py
      WHY: 2 occurrences of 6-line block across 2 files — saves 6 lines
      FILES: fixos/config.py, fixos/utils/terminal.py
  [6] ○ extract_function   → fixos/utils/utils/print_stdout_box.py
      WHY: 2 occurrences of 3-line block across 1 files — saves 3 lines
      FILES: fixos/utils/terminal.py

QUICK_WINS[4] (low risk, high savings — do first):
  [2] extract_function   saved=27L  → fixos/diagnostics/checks/utils/_diagnose_swap_optimization.py
      FILES: storage_optimization.py
  [3] extract_function   saved=15L  → fixos/agent/utils/print_timeout.py
      FILES: session_io.py
  [4] extract_function   saved=12L  → fixos/cli/utils/config.py
      FILES: config_cmd.py, features_cmd.py, profile_cmd.py +2
  [5] extract_function   saved=6L  → fixos/utils/detect_provider_from_key.py
      FILES: config.py, terminal.py

EFFORT_ESTIMATE (total ≈ 5.2h):
  hard   _find_downloads_cleanup             saved=62L  ~186min
  medium _diagnose_swap_optimization         saved=27L  ~54min
  medium print_timeout                       saved=15L  ~30min
  easy   config                              saved=12L  ~24min
  easy   detect_provider_from_key            saved=6L  ~12min
  easy   print_stdout_box                    saved=3L  ~6min

METRICS-TARGET:
  dup_groups:  6 → 0
  saved_lines: 125 lines recoverable
```

### Evolution / Churn (`project/evolution.toon.yaml`)

```toon markpact:analysis path=project/evolution.toon.yaml
# code2llm/evolution | 624 func | 92f | 2026-05-08
# generated in 0.00s

NEXT[1] (ranked by impact):
  [1] !! SPLIT           planfile.yaml
      WHY: 2450L, 0 classes, max CC=0
      EFFORT: ~4h  IMPACT: 0


RISKS[1]:
  ⚠ Splitting planfile.yaml may break 0 import paths

METRICS-TARGET:
  CC̄:          4.3 → ≤3.0
  max-CC:      14 → ≤7
  god-modules: 1 → 0
  high-CC(≥15): 0 → ≤0
  hub-types:   0 → ≤0

PATTERNS (language parser shared logic):
  _extract_declarations() in base.py — unified extraction for:
    - TypeScript: interfaces, types, classes, functions, arrow funcs
    - PHP: namespaces, traits, classes, functions, includes
    - Ruby: modules, classes, methods, requires
    - C++: classes, structs, functions, #includes
    - C#: classes, interfaces, methods, usings
    - Java: classes, interfaces, methods, imports
    - Go: packages, functions, structs
    - Rust: modules, functions, traits, use statements

  Shared regex patterns per language:
    - import: language-specific import/require/using patterns
    - class: class/struct/trait declarations with inheritance
    - function: function/method signatures with visibility
    - brace_tracking: for C-family languages ({ })
    - end_keyword_tracking: for Ruby (module/class/def...end)

  Benefits:
    - Consistent extraction logic across all languages
    - Reduced code duplication (~70% reduction in parser LOC)
    - Easier maintenance: fix once, apply everywhere
    - Standardized FunctionInfo/ClassInfo models

HISTORY:
  prev CC̄=3.1 → now CC̄=4.3
```

### Validation (`project/validation.toon.yaml`)

```toon markpact:analysis path=project/validation.toon.yaml
# vallm batch | 183f | 121✓ 19⚠ 4✗ | 2026-04-09

SUMMARY:
  scanned: 183  passed: 121 (66.1%)  warnings: 19  errors: 4  unsupported: 58

WARNINGS[19]{path,score}:
  fixos/cli/cleanup_cmd.py,0.83
    issues[9]{rule,severity,message,line}:
      complexity.cyclomatic,warning,cleanup_services has cyclomatic complexity 16 (max: 15),39
      complexity.cyclomatic,warning,_display_unsafe_services has cyclomatic complexity 18 (max: 15),170
      complexity.cyclomatic,warning,_cleanup_full_system has cyclomatic complexity 172 (max: 15),539
      complexity.maintainability,warning,Low maintainability index: 0.0 (threshold: 20),
      complexity.lizard_cc,warning,cleanup_services: CC=16 exceeds limit 15,39
      complexity.lizard_cc,warning,_display_unsafe_services: CC=18 exceeds limit 15,170
      complexity.lizard_length,warning,_cleanup_flatpak_detailed: 102 lines exceeds limit 100,259
      complexity.lizard_cc,warning,_cleanup_full_system: CC=172 exceeds limit 15,539
      complexity.lizard_length,warning,_cleanup_full_system: 519 lines exceeds limit 100,539
  fixos/diagnostics/flatpak_analyzer.py,0.93
    issues[4]{rule,severity,message,line}:
      complexity.cyclomatic,warning,get_cleanup_recommendations has cyclomatic complexity 27 (max: 15),529
      complexity.maintainability,warning,Low maintainability index: 12.4 (threshold: 20),
      complexity.lizard_cc,warning,get_cleanup_recommendations: CC=27 exceeds limit 15,529
      complexity.lizard_length,warning,get_cleanup_recommendations: 163 lines exceeds limit 100,529
  fixos/llm_shell.py,0.93
    issues[2]{rule,severity,message,line}:
      complexity.lizard_cc,warning,run_llm_shell: CC=16 exceeds limit 15,100
      complexity.lizard_length,warning,run_llm_shell: 103 lines exceeds limit 100,100
  fixos/diagnostics/storage_analyzer.py,0.96
    issues[3]{rule,severity,message,line}:
      complexity.cyclomatic,warning,_analyze_docker has cyclomatic complexity 22 (max: 15),259
      complexity.maintainability,warning,Low maintainability index: 8.7 (threshold: 20),
      complexity.lizard_cc,warning,_analyze_docker: CC=22 exceeds limit 15,259
  fixos/cli/ask_cmd.py,0.97
    issues[2]{rule,severity,message,line}:
      complexity.cyclomatic,warning,_match_heuristic_command has cyclomatic complexity 18 (max: 15),31
      complexity.lizard_cc,warning,_match_heuristic_command: CC=18 exceeds limit 15,31
  fixos/cli/fix_cmd.py,0.97
    issues[2]{rule,severity,message,line}:
      complexity.cyclomatic,warning,fix has cyclomatic complexity 18 (max: 15),28
      complexity.lizard_cc,warning,fix: CC=18 exceeds limit 15,28
  fixos/cli/report_cmd.py,0.97
    issues[2]{rule,severity,message,line}:
      complexity.cyclomatic,warning,report has cyclomatic complexity 16 (max: 15),14
      complexity.lizard_cc,warning,report: CC=16 exceeds limit 15,14
  fixos/diagnostics/checks/system_core.py,0.97
    issues[2]{rule,severity,message,line}:
      complexity.cyclomatic,warning,diagnose_system has cyclomatic complexity 16 (max: 15),13
      complexity.lizard_cc,warning,diagnose_system: CC=16 exceeds limit 15,13
  fixos/diagnostics/disk_analyzer.py,0.97
    issues[2]{rule,severity,message,line}:
      complexity.cyclomatic,warning,_identify_cache_type has cyclomatic complexity 17 (max: 15),359
      complexity.lizard_cc,warning,_identify_cache_type: CC=17 exceeds limit 15,359
  fixos/diagnostics/service_details.py,0.97
    issues[2]{rule,severity,message,line}:
      complexity.cyclomatic,warning,_docker has cyclomatic complexity 17 (max: 15),47
      complexity.lizard_cc,warning,_docker: CC=17 exceeds limit 15,47
  fixos/features/installer.py,0.97
    issues[2]{rule,severity,message,line}:
      complexity.cyclomatic,warning,_install_package has cyclomatic complexity 27 (max: 15),47
      complexity.lizard_cc,warning,_install_package: CC=27 exceeds limit 15,47
  fixos/interactive/cleanup_planner.py,0.97
    issues[2]{rule,severity,message,line}:
      complexity.cyclomatic,warning,_generate_recommendations has cyclomatic complexity 18 (max: 15),321
      complexity.lizard_cc,warning,_generate_recommendations: CC=18 exceeds limit 15,321
  fixos/orchestrator/orchestrator.py,0.97
    issues[2]{rule,severity,message,line}:
      complexity.cyclomatic,warning,run_sync has cyclomatic complexity 17 (max: 15),165
      complexity.lizard_cc,warning,run_sync: CC=17 exceeds limit 15,165
  fixos/utils/anonymizer.py,0.97
    issues[2]{rule,severity,message,line}:
      complexity.cyclomatic,warning,_dict_to_markdown has cyclomatic complexity 18 (max: 15),236
      complexity.lizard_cc,warning,_dict_to_markdown: CC=18 exceeds limit 15,236
  fixos/utils/terminal.py,0.97
    issues[2]{rule,severity,message,line}:
      complexity.cyclomatic,warning,render_md has cyclomatic complexity 16 (max: 15),62
      complexity.lizard_cc,warning,render_md: CC=16 exceeds limit 15,62
  fixos/cli/scan_cmd.py,0.98
    issues[1]{rule,severity,message,line}:
      complexity.cyclomatic,warning,_run_disk_analysis has cyclomatic complexity 18 (max: 15),88
  fixos/plugins/builtin/security.py,0.98
    issues[1]{rule,severity,message,line}:
      complexity.cyclomatic,warning,diagnose has cyclomatic complexity 16 (max: 15),14
  tests/e2e/test_anonymization_layers.py,0.98
    issues[1]{rule,severity,message,line}:
      complexity.maintainability,warning,Low maintainability index: 14.2 (threshold: 20),
  tests/unit/test_executor.py,0.98
    issues[1]{rule,severity,message,line}:
      complexity.maintainability,warning,Low maintainability index: 16.7 (threshold: 20),

ERRORS[4]{path,score}:
  planfile.yaml,0.00
    issues[1]{rule,severity,message,line}:
      syntax.tree_sitter,error,tree-sitter found 1 parse error(s) in yaml,
  fixos/fixes/__init__.py,0.57
    issues[2]{rule,severity,message,line}:
      python.import.relative.resolvable,error,Relative import 'knowledge_base' not found,1
      python.import.relative.resolvable,error,Relative import 'heuristics' not found,2
  docs/examples/quickstart.py,0.79
    issues[4]{rule,severity,message,line}:
      python.import.relative.resolvable,error,Relative import 'hitl' not found,1
      python.import.relative.resolvable,error,Relative import 'autonomous' not found,2
      python.import.relative.resolvable,error,Relative import 'autonomous_session' not found,3
      python.import.relative.resolvable,error,Relative import 'autonomous_session' not found,6
  setup.py,0.79
    issues[1]{rule,severity,message,line}:
      python.import.resolvable,error,Module 'setuptools' not found,1

UNSUPPORTED[6]{bucket,count}:
  *.md,25
  Dockerfile*,10
  *.txt,3
  *.yml,3
  *.example,2
  other,15
```

## Intent

AI-powered Linux/Windows diagnostics and repair – audio, hardware, system issues
