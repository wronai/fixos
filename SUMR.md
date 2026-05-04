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
- **version**: `2.2.12`
- **python_requires**: `>=3.10`
- **license**: Apache-2.0
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
  version: 2.2.12;
}

dependencies {
  runtime: "openai>=1.35.0, prompt_toolkit>=3.0.43, psutil>=5.9.0, pyyaml>=6.0, click>=8.1.0, python-dotenv>=1.0.0, rich>=13.0";
  dev: "pytest>=7.4.0, pytest-mock>=3.12.0, pytest-cov>=4.1.0, pytest-xdist>=3.5.0, pytest-timeout>=2.2.0, pytest-sugar>=0.9.7";
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
  step-3: run cmd=.venv/bin/python -m build --parallel -n auto;
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
```

## Call Graph

*139 nodes · 131 edges · 35 modules · CC̄=3.7*

### Hubs (by degree)

| Function | CC | in | out | total |
|----------|----|----|-----|-------|
| `_cmd` *(in fixos.diagnostics.checks._shared)* | 7 | 142 | 3 | **145** |
| `_cleanup_flatpak_detailed` *(in fixos.cli.cleanup_cmd)* | 12 ⚠ | 1 | 111 | **112** |
| `_display_flatpak_status` *(in fixos.cli.cleanup_cmd)* | 9 | 1 | 65 | **66** |
| `_print_welcome` *(in fixos.cli.main)* | 6 | 1 | 61 | **62** |
| `run_llm_shell` *(in fixos.llm_shell)* | 15 ⚠ | 0 | 53 | **53** |
| `diagnose_resources` *(in fixos.diagnostics.checks.resources)* | 13 ⚠ | 0 | 49 | **49** |
| `anonymize` *(in fixos.utils.anonymizer)* | 15 ⚠ | 0 | 48 | **48** |
| `diagnose_system` *(in fixos.diagnostics.checks.system_core)* | 16 ⚠ | 0 | 46 | **46** |

```toon markpact:analysis path=project/calls.toon.yaml
# code2llm call graph | /home/tom/github/wronai/fixOS
# nodes: 139 | edges: 131 | modules: 35
# CC̄=3.7

HUBS[20]:
  fixos.diagnostics.checks._shared._cmd
    CC=7  in:142  out:3  total:145
  fixos.cli.cleanup_cmd._cleanup_flatpak_detailed
    CC=12  in:1  out:111  total:112
  fixos.cli.cleanup_cmd._display_flatpak_status
    CC=9  in:1  out:65  total:66
  fixos.cli.main._print_welcome
    CC=6  in:1  out:61  total:62
  fixos.llm_shell.run_llm_shell
    CC=15  in:0  out:53  total:53
  fixos.diagnostics.checks.resources.diagnose_resources
    CC=13  in:0  out:49  total:49
  fixos.utils.anonymizer.anonymize
    CC=15  in:0  out:48  total:48
  fixos.diagnostics.checks.system_core.diagnose_system
    CC=16  in:0  out:46  total:46
  fixos.utils.anonymizer._dict_to_markdown
    CC=18  in:2  out:43  total:45
  fixos.platform_utils.run_command
    CC=5  in:33  out:4  total:37
  fixos.diagnostics.checks.security.diagnose_security
    CC=4  in:0  out:36  total:36
  fixos.cli.token_cmd.token_set
    CC=7  in:0  out:29  total:29
  fixos.anonymizer.anonymize
    CC=5  in:14  out:14  total:28
  scripts.pyqual-calibrate.calibrate
    CC=14  in:1  out:26  total:27
  fixos.orchestrator.orchestrator.FixOrchestrator.load_from_diagnostics
    CC=5  in:0  out:26  total:26
  fixos.config.FixOsConfig.load
    CC=14  in:0  out:26  total:26
  fixos.diagnostics.checks.audio.diagnose_audio
    CC=1  in:0  out:25  total:25
  fixos.orchestrator.orchestrator.FixOrchestrator._evaluate_and_rediagnose
    CC=10  in:0  out:23  total:23
  fixos.cli.features_cmd._interactive_profile_select
    CC=11  in:1  out:22  total:23
  fixos.cli.ask_cmd._execute_with_llm
    CC=8  in:1  out:21  total:22

MODULES:
  fixos.agent  [1 funcs]
    get_remaining_time  CC=2  out:4
  fixos.agent.autonomous_session  [5 funcs]
    _get_remaining_time  CC=1  out:1
    _handle_exec  CC=4  out:16
    _handle_llm_error  CC=4  out:3
    _handle_search  CC=3  out:8
    _initialize_messages  CC=2  out:3
  fixos.agent.hitl_session  [8 funcs]
    __init__  CC=2  out:5
    _check_low_confidence  CC=7  out:8
    _clear_timeout  CC=1  out:1
    _handle_llm_error  CC=4  out:4
    _initialize_messages  CC=3  out:5
    _process_turn  CC=7  out:16
    _setup_timeout  CC=1  out:3
    remaining  CC=1  out:1
  fixos.agent.session_core  [2 funcs]
    extract_fixes  CC=10  out:19
    extract_search_topic  CC=3  out:4
  fixos.agent.session_handlers  [9 funcs]
    handle_describe_problem  CC=2  out:2
    handle_direct_command  CC=1  out:5
    handle_execute_all  CC=4  out:9
    handle_fix_by_number  CC=2  out:9
    handle_quit  CC=1  out:1
    handle_search  CC=2  out:6
    handle_skip_all  CC=1  out:1
    parse_user_input  CC=9  out:11
    run_single_command  CC=3  out:12
  fixos.agent.session_io  [10 funcs]
    _suspend_timeout  CC=4  out:3
    ask_execute_prompt  CC=1  out:4
    ask_low_confidence_search  CC=1  out:4
    ask_send_data  CC=1  out:4
    ask_user_problem  CC=2  out:11
    fmt_time  CC=1  out:0
    get_user_input  CC=2  out:4
    print_cmd_result  CC=8  out:13
    print_session_header  CC=1  out:8
    print_session_summary  CC=3  out:4
  fixos.anonymizer  [2 funcs]
    anonymize  CC=5  out:14
    get_sensitive_values  CC=4  out:3
  fixos.cli.ask_cmd  [8 funcs]
    _build_output_dict  CC=8  out:0
    _execute_heuristic_command  CC=9  out:12
    _execute_with_llm  CC=8  out:21
    _format_command  CC=3  out:3
    _handle_natural_command  CC=3  out:9
    _match_heuristic_command  CC=18  out:2
    _validate_result_with_llm  CC=14  out:16
    ask  CC=1  out:4
  fixos.cli.cleanup_cmd  [2 funcs]
    _cleanup_flatpak_detailed  CC=12  out:111
    _display_flatpak_status  CC=9  out:65
  fixos.cli.features_cmd  [2 funcs]
    _interactive_profile_select  CC=11  out:22
    features_audit  CC=4  out:18
  fixos.cli.main  [3 funcs]
    _print_welcome  CC=6  out:61
    cli  CC=3  out:5
    main  CC=1  out:1
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
  fixos.diagnostics.checks.hardware  [1 funcs]
    diagnose_hardware  CC=1  out:18
  fixos.diagnostics.checks.resources  [1 funcs]
    diagnose_resources  CC=13  out:49
  fixos.diagnostics.checks.security  [1 funcs]
    diagnose_security  CC=4  out:36
  fixos.diagnostics.checks.system_core  [1 funcs]
    diagnose_system  CC=16  out:46
  fixos.diagnostics.checks.thumbnails  [1 funcs]
    diagnose_thumbnails  CC=1  out:21
  fixos.llm_shell  [1 funcs]
    run_llm_shell  CC=15  out:53
  fixos.orchestrator.orchestrator  [4 funcs]
    _default_confirm  CC=3  out:6
    _default_progress  CC=8  out:8
    _evaluate_and_rediagnose  CC=10  out:23
    load_from_diagnostics  CC=5  out:26
  fixos.platform_utils  [10 funcs]
    _cmd_exists  CC=1  out:1
    cancel_signal_timeout  CC=2  out:1
    elevate_cmd  CC=3  out:2
    get_os_info  CC=5  out:8
    get_package_manager  CC=8  out:3
    install_package_cmd  CC=2  out:2
    is_dangerous  CC=3  out:1
    needs_elevation  CC=5  out:7
    run_command  CC=5  out:4
    setup_signal_timeout  CC=2  out:2
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
  fixos.utils.anonymizer  [6 funcs]
    _dict_to_markdown  CC=18  out:43
    _format_diagnostics_markdown  CC=3  out:5
    _format_key_title  CC=1  out:3
    _get_sensitive  CC=4  out:3
    anonymize  CC=15  out:48
    display_anonymized_preview  CC=5  out:18
  fixos.utils.terminal  [4 funcs]
    print_cmd_block  CC=4  out:6
    print_problem_header  CC=3  out:10
    print_stderr_box  CC=2  out:8
    print_stdout_box  CC=2  out:8
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
  fixos.config.FixOsConfig.load → fixos.config._load_env_files
  fixos.platform_utils.elevate_cmd → fixos.platform_utils.needs_elevation
  fixos.platform_utils.get_package_manager → fixos.platform_utils._cmd_exists
  fixos.platform_utils.install_package_cmd → fixos.platform_utils.get_package_manager
  fixos.system_checks.get_fedora_specific → fixos.system_checks.run_cmd
  fixos.system_checks.get_full_diagnostics → fixos.system_checks.get_cpu_info
  fixos.system_checks.get_full_diagnostics → fixos.system_checks.get_memory_info
  fixos.system_checks.get_full_diagnostics → fixos.system_checks.get_disk_info
  fixos.system_checks.get_full_diagnostics → fixos.system_checks.get_network_info
  fixos.system_checks.get_full_diagnostics → fixos.system_checks.get_top_processes
  fixos.anonymizer.anonymize → fixos.anonymizer.get_sensitive_values
  fixos.llm_shell.run_llm_shell → fixos.anonymizer.anonymize
  fixos.config_interactive.interactive_provider_setup → fixos.config_interactive._print_provider_menu
  fixos.config_interactive.interactive_provider_setup → fixos.config_interactive._get_user_choice
  fixos.config_interactive.interactive_provider_setup → fixos.config_interactive._get_api_key
  fixos.config_interactive.interactive_provider_setup → fixos.config_interactive._save_to_env
  fixos.diagnostics.checks.resources.diagnose_resources → fixos.diagnostics.checks._shared._psutil_required
  fixos.diagnostics.checks.system_core.diagnose_system → fixos.diagnostics.checks._shared._psutil_required
  fixos.diagnostics.checks.system_core.diagnose_system → fixos.diagnostics.checks._shared._cmd
  fixos.diagnostics.checks.audio.diagnose_audio → fixos.diagnostics.checks._shared._cmd
  fixos.diagnostics.checks.security.diagnose_security → fixos.diagnostics.checks._shared._cmd
  fixos.diagnostics.checks.hardware.diagnose_hardware → fixos.diagnostics.checks._shared._cmd
  fixos.diagnostics.checks.thumbnails.diagnose_thumbnails → fixos.diagnostics.checks._shared._cmd
  fixos.agent.session_handlers.handle_execute_all → fixos.anonymizer.anonymize
  fixos.agent.session_handlers.handle_fix_by_number → fixos.anonymizer.anonymize
  fixos.agent.session_handlers.handle_direct_command → fixos.anonymizer.anonymize
  fixos.agent.session_handlers.handle_search → fixos.utils.web_search.search_all
  fixos.agent.session_handlers.handle_search → fixos.utils.web_search.format_results_for_llm
  fixos.agent.session_handlers.run_single_command → fixos.platform_utils.elevate_cmd
  fixos.agent.session_handlers.run_single_command → fixos.platform_utils.is_dangerous
  fixos.agent.session_handlers.run_single_command → fixos.platform_utils.run_command
  fixos.agent.session_handlers.parse_user_input → fixos.agent.session_handlers.handle_quit
  fixos.agent.session_handlers.parse_user_input → fixos.agent.session_handlers.handle_describe_problem
  fixos.agent.session_handlers.parse_user_input → fixos.agent.session_handlers.handle_skip_all
  fixos.agent.session_handlers.parse_user_input → fixos.agent.session_handlers.handle_execute_all
  fixos.agent.session_handlers.parse_user_input → fixos.agent.session_handlers.handle_fix_by_number
  fixos.agent.session_handlers.parse_user_input → fixos.agent.session_handlers.handle_direct_command
  fixos.agent.autonomous_session.AutonomousSession._initialize_messages → fixos.anonymizer.anonymize
  fixos.agent.autonomous_session.AutonomousSession._initialize_messages → fixos.utils.anonymizer.display_anonymized_preview
  fixos.agent.autonomous_session.AutonomousSession._get_remaining_time → fixos.agent.get_remaining_time
  fixos.agent.autonomous_session.AutonomousSession._handle_llm_error → fixos.utils.web_search.search_all
  fixos.agent.autonomous_session.AutonomousSession._handle_llm_error → fixos.utils.web_search.format_results_for_llm
  fixos.agent.autonomous_session.AutonomousSession._handle_search → fixos.utils.web_search.search_all
  fixos.agent.autonomous_session.AutonomousSession._handle_search → fixos.utils.web_search.format_results_for_llm
  fixos.agent.autonomous_session.AutonomousSession._handle_exec → fixos.anonymizer.anonymize
  fixos.agent.hitl_session.HITLSession.__init__ → fixos.platform_utils.get_os_info
  fixos.agent.hitl_session.HITLSession.__init__ → fixos.platform_utils.get_package_manager
  fixos.agent.hitl_session.HITLSession._setup_timeout → fixos.platform_utils.setup_signal_timeout
  fixos.agent.hitl_session.HITLSession._clear_timeout → fixos.platform_utils.cancel_signal_timeout
  fixos.agent.hitl_session.HITLSession.remaining → fixos.agent.get_remaining_time
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
# nodes: 139 | edges: 131 | modules: 35
# CC̄=3.7

HUBS[20]:
  fixos.diagnostics.checks._shared._cmd
    CC=7  in:142  out:3  total:145
  fixos.cli.cleanup_cmd._cleanup_flatpak_detailed
    CC=12  in:1  out:111  total:112
  fixos.cli.cleanup_cmd._display_flatpak_status
    CC=9  in:1  out:65  total:66
  fixos.cli.main._print_welcome
    CC=6  in:1  out:61  total:62
  fixos.llm_shell.run_llm_shell
    CC=15  in:0  out:53  total:53
  fixos.diagnostics.checks.resources.diagnose_resources
    CC=13  in:0  out:49  total:49
  fixos.utils.anonymizer.anonymize
    CC=15  in:0  out:48  total:48
  fixos.diagnostics.checks.system_core.diagnose_system
    CC=16  in:0  out:46  total:46
  fixos.utils.anonymizer._dict_to_markdown
    CC=18  in:2  out:43  total:45
  fixos.platform_utils.run_command
    CC=5  in:33  out:4  total:37
  fixos.diagnostics.checks.security.diagnose_security
    CC=4  in:0  out:36  total:36
  fixos.cli.token_cmd.token_set
    CC=7  in:0  out:29  total:29
  fixos.anonymizer.anonymize
    CC=5  in:14  out:14  total:28
  scripts.pyqual-calibrate.calibrate
    CC=14  in:1  out:26  total:27
  fixos.orchestrator.orchestrator.FixOrchestrator.load_from_diagnostics
    CC=5  in:0  out:26  total:26
  fixos.config.FixOsConfig.load
    CC=14  in:0  out:26  total:26
  fixos.diagnostics.checks.audio.diagnose_audio
    CC=1  in:0  out:25  total:25
  fixos.orchestrator.orchestrator.FixOrchestrator._evaluate_and_rediagnose
    CC=10  in:0  out:23  total:23
  fixos.cli.features_cmd._interactive_profile_select
    CC=11  in:1  out:22  total:23
  fixos.cli.ask_cmd._execute_with_llm
    CC=8  in:1  out:21  total:22

MODULES:
  fixos.agent  [1 funcs]
    get_remaining_time  CC=2  out:4
  fixos.agent.autonomous_session  [5 funcs]
    _get_remaining_time  CC=1  out:1
    _handle_exec  CC=4  out:16
    _handle_llm_error  CC=4  out:3
    _handle_search  CC=3  out:8
    _initialize_messages  CC=2  out:3
  fixos.agent.hitl_session  [8 funcs]
    __init__  CC=2  out:5
    _check_low_confidence  CC=7  out:8
    _clear_timeout  CC=1  out:1
    _handle_llm_error  CC=4  out:4
    _initialize_messages  CC=3  out:5
    _process_turn  CC=7  out:16
    _setup_timeout  CC=1  out:3
    remaining  CC=1  out:1
  fixos.agent.session_core  [2 funcs]
    extract_fixes  CC=10  out:19
    extract_search_topic  CC=3  out:4
  fixos.agent.session_handlers  [9 funcs]
    handle_describe_problem  CC=2  out:2
    handle_direct_command  CC=1  out:5
    handle_execute_all  CC=4  out:9
    handle_fix_by_number  CC=2  out:9
    handle_quit  CC=1  out:1
    handle_search  CC=2  out:6
    handle_skip_all  CC=1  out:1
    parse_user_input  CC=9  out:11
    run_single_command  CC=3  out:12
  fixos.agent.session_io  [10 funcs]
    _suspend_timeout  CC=4  out:3
    ask_execute_prompt  CC=1  out:4
    ask_low_confidence_search  CC=1  out:4
    ask_send_data  CC=1  out:4
    ask_user_problem  CC=2  out:11
    fmt_time  CC=1  out:0
    get_user_input  CC=2  out:4
    print_cmd_result  CC=8  out:13
    print_session_header  CC=1  out:8
    print_session_summary  CC=3  out:4
  fixos.anonymizer  [2 funcs]
    anonymize  CC=5  out:14
    get_sensitive_values  CC=4  out:3
  fixos.cli.ask_cmd  [8 funcs]
    _build_output_dict  CC=8  out:0
    _execute_heuristic_command  CC=9  out:12
    _execute_with_llm  CC=8  out:21
    _format_command  CC=3  out:3
    _handle_natural_command  CC=3  out:9
    _match_heuristic_command  CC=18  out:2
    _validate_result_with_llm  CC=14  out:16
    ask  CC=1  out:4
  fixos.cli.cleanup_cmd  [2 funcs]
    _cleanup_flatpak_detailed  CC=12  out:111
    _display_flatpak_status  CC=9  out:65
  fixos.cli.features_cmd  [2 funcs]
    _interactive_profile_select  CC=11  out:22
    features_audit  CC=4  out:18
  fixos.cli.main  [3 funcs]
    _print_welcome  CC=6  out:61
    cli  CC=3  out:5
    main  CC=1  out:1
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
  fixos.diagnostics.checks.hardware  [1 funcs]
    diagnose_hardware  CC=1  out:18
  fixos.diagnostics.checks.resources  [1 funcs]
    diagnose_resources  CC=13  out:49
  fixos.diagnostics.checks.security  [1 funcs]
    diagnose_security  CC=4  out:36
  fixos.diagnostics.checks.system_core  [1 funcs]
    diagnose_system  CC=16  out:46
  fixos.diagnostics.checks.thumbnails  [1 funcs]
    diagnose_thumbnails  CC=1  out:21
  fixos.llm_shell  [1 funcs]
    run_llm_shell  CC=15  out:53
  fixos.orchestrator.orchestrator  [4 funcs]
    _default_confirm  CC=3  out:6
    _default_progress  CC=8  out:8
    _evaluate_and_rediagnose  CC=10  out:23
    load_from_diagnostics  CC=5  out:26
  fixos.platform_utils  [10 funcs]
    _cmd_exists  CC=1  out:1
    cancel_signal_timeout  CC=2  out:1
    elevate_cmd  CC=3  out:2
    get_os_info  CC=5  out:8
    get_package_manager  CC=8  out:3
    install_package_cmd  CC=2  out:2
    is_dangerous  CC=3  out:1
    needs_elevation  CC=5  out:7
    run_command  CC=5  out:4
    setup_signal_timeout  CC=2  out:2
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
  fixos.utils.anonymizer  [6 funcs]
    _dict_to_markdown  CC=18  out:43
    _format_diagnostics_markdown  CC=3  out:5
    _format_key_title  CC=1  out:3
    _get_sensitive  CC=4  out:3
    anonymize  CC=15  out:48
    display_anonymized_preview  CC=5  out:18
  fixos.utils.terminal  [4 funcs]
    print_cmd_block  CC=4  out:6
    print_problem_header  CC=3  out:10
    print_stderr_box  CC=2  out:8
    print_stdout_box  CC=2  out:8
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
  fixos.config.FixOsConfig.load → fixos.config._load_env_files
  fixos.platform_utils.elevate_cmd → fixos.platform_utils.needs_elevation
  fixos.platform_utils.get_package_manager → fixos.platform_utils._cmd_exists
  fixos.platform_utils.install_package_cmd → fixos.platform_utils.get_package_manager
  fixos.system_checks.get_fedora_specific → fixos.system_checks.run_cmd
  fixos.system_checks.get_full_diagnostics → fixos.system_checks.get_cpu_info
  fixos.system_checks.get_full_diagnostics → fixos.system_checks.get_memory_info
  fixos.system_checks.get_full_diagnostics → fixos.system_checks.get_disk_info
  fixos.system_checks.get_full_diagnostics → fixos.system_checks.get_network_info
  fixos.system_checks.get_full_diagnostics → fixos.system_checks.get_top_processes
  fixos.anonymizer.anonymize → fixos.anonymizer.get_sensitive_values
  fixos.llm_shell.run_llm_shell → fixos.anonymizer.anonymize
  fixos.config_interactive.interactive_provider_setup → fixos.config_interactive._print_provider_menu
  fixos.config_interactive.interactive_provider_setup → fixos.config_interactive._get_user_choice
  fixos.config_interactive.interactive_provider_setup → fixos.config_interactive._get_api_key
  fixos.config_interactive.interactive_provider_setup → fixos.config_interactive._save_to_env
  fixos.diagnostics.checks.resources.diagnose_resources → fixos.diagnostics.checks._shared._psutil_required
  fixos.diagnostics.checks.system_core.diagnose_system → fixos.diagnostics.checks._shared._psutil_required
  fixos.diagnostics.checks.system_core.diagnose_system → fixos.diagnostics.checks._shared._cmd
  fixos.diagnostics.checks.audio.diagnose_audio → fixos.diagnostics.checks._shared._cmd
  fixos.diagnostics.checks.security.diagnose_security → fixos.diagnostics.checks._shared._cmd
  fixos.diagnostics.checks.hardware.diagnose_hardware → fixos.diagnostics.checks._shared._cmd
  fixos.diagnostics.checks.thumbnails.diagnose_thumbnails → fixos.diagnostics.checks._shared._cmd
  fixos.agent.session_handlers.handle_execute_all → fixos.anonymizer.anonymize
  fixos.agent.session_handlers.handle_fix_by_number → fixos.anonymizer.anonymize
  fixos.agent.session_handlers.handle_direct_command → fixos.anonymizer.anonymize
  fixos.agent.session_handlers.handle_search → fixos.utils.web_search.search_all
  fixos.agent.session_handlers.handle_search → fixos.utils.web_search.format_results_for_llm
  fixos.agent.session_handlers.run_single_command → fixos.platform_utils.elevate_cmd
  fixos.agent.session_handlers.run_single_command → fixos.platform_utils.is_dangerous
  fixos.agent.session_handlers.run_single_command → fixos.platform_utils.run_command
  fixos.agent.session_handlers.parse_user_input → fixos.agent.session_handlers.handle_quit
  fixos.agent.session_handlers.parse_user_input → fixos.agent.session_handlers.handle_describe_problem
  fixos.agent.session_handlers.parse_user_input → fixos.agent.session_handlers.handle_skip_all
  fixos.agent.session_handlers.parse_user_input → fixos.agent.session_handlers.handle_execute_all
  fixos.agent.session_handlers.parse_user_input → fixos.agent.session_handlers.handle_fix_by_number
  fixos.agent.session_handlers.parse_user_input → fixos.agent.session_handlers.handle_direct_command
  fixos.agent.autonomous_session.AutonomousSession._initialize_messages → fixos.anonymizer.anonymize
  fixos.agent.autonomous_session.AutonomousSession._initialize_messages → fixos.utils.anonymizer.display_anonymized_preview
  fixos.agent.autonomous_session.AutonomousSession._get_remaining_time → fixos.agent.get_remaining_time
  fixos.agent.autonomous_session.AutonomousSession._handle_llm_error → fixos.utils.web_search.search_all
  fixos.agent.autonomous_session.AutonomousSession._handle_llm_error → fixos.utils.web_search.format_results_for_llm
  fixos.agent.autonomous_session.AutonomousSession._handle_search → fixos.utils.web_search.search_all
  fixos.agent.autonomous_session.AutonomousSession._handle_search → fixos.utils.web_search.format_results_for_llm
  fixos.agent.autonomous_session.AutonomousSession._handle_exec → fixos.anonymizer.anonymize
  fixos.agent.hitl_session.HITLSession.__init__ → fixos.platform_utils.get_os_info
  fixos.agent.hitl_session.HITLSession.__init__ → fixos.platform_utils.get_package_manager
  fixos.agent.hitl_session.HITLSession._setup_timeout → fixos.platform_utils.setup_signal_timeout
  fixos.agent.hitl_session.HITLSession._clear_timeout → fixos.platform_utils.cancel_signal_timeout
  fixos.agent.hitl_session.HITLSession.remaining → fixos.agent.get_remaining_time
```

### Code Analysis (`project/analysis.toon.yaml`)

```toon markpact:analysis path=project/analysis.toon.yaml
# code2llm | 134f 23908L | python:89,yaml:24,txt:3,yml:3,shell:2,toml:1,ini:1 | 2026-05-04
# CC̄=3.7 | critical:26/686 | dups:0 | cycles:0

HEALTH[20]:
  🟡 CC    run_llm_shell CC=15 (limit:15)
  🟡 CC    _find_leftover_data CC=15 (limit:15)
  🟡 CC    _analyze_repo_size CC=15 (limit:15)
  🟡 CC    get_cleanup_recommendations CC=27 (limit:15)
  🟡 CC    _identify_cache_type CC=17 (limit:15)
  🟡 CC    _docker CC=17 (limit:15)
  🟡 CC    _analyze_docker CC=22 (limit:15)
  🟡 CC    _analyze_snap CC=15 (limit:15)
  🟡 CC    diagnose_system CC=16 (limit:15)
  🟡 CC    _detect_de CC=15 (limit:15)
  🟡 CC    _install_package CC=27 (limit:15)
  🟡 CC    _run_disk_analysis CC=18 (limit:15)
  🟡 CC    report CC=16 (limit:15)
  🟡 CC    _match_heuristic_command CC=18 (limit:15)
  🟡 CC    fix CC=18 (limit:15)
  🟡 CC    cleanup_services CC=16 (limit:15)
  🟡 CC    _display_unsafe_services CC=18 (limit:15)
  🟡 CC    _cleanup_full_system CC=172 (limit:15)
  🟡 CC    features_install CC=15 (limit:15)
  🟡 CC    diagnose CC=16 (limit:15)

REFACTOR[1]:
  1. split 20 high-CC methods  (CC>15)

PIPELINES[358]:
  [1] Src [load]: load → _load_env_files
      PURITY: 100% pure
  [2] Src [validate]: validate
      PURITY: 100% pure
  [3] Src [summary]: summary
      PURITY: 100% pure
  [4] Src [get_providers_list]: get_providers_list
      PURITY: 100% pure
  [5] Src [__init__]: __init__
      PURITY: 100% pure

LAYERS:
  scripts/                        CC̄=5.4    ←in:0  →out:0
  │ pyqual-calibrate           299L  0C    7m  CC=14     ←0
  │
  fixos/                          CC̄=5.3    ←in:76  →out:0
  │ !! cleanup_cmd               1246L  0C   14m  CC=172    ←0
  │ !! storage_analyzer          1058L  2C   31m  CC=22     ←0
  │ !! flatpak_analyzer           944L  3C   24m  CC=27     ←0
  │ service_cleanup            473L  1C   10m  CC=14     ←2
  │ !! disk_analyzer              433L  1C   15m  CC=17     ←0
  │ autonomous_session         433L  3C   22m  CC=8      ←0
  │ !! cleanup_planner            417L  4C   12m  CC=18     ←0
  │ dev_project_analyzer       403L  2C   13m  CC=11     ←0
  │ !! orchestrator               382L  2C   11m  CC=17     ←0
  │ !! ask_cmd                    354L  0C    8m  CC=18     ←0
  │ config                     345L  1C    7m  CC=14     ←8
  │ llm_analyzer               333L  2C    8m  CC=13     ←0
  │ !! terminal                   316L  1C    8m  CC=16     ←2
  │ packages.yaml              316L  0C    0m  CC=0.0    ←0
  │ !! anonymizer                 299L  1C    9m  CC=18     ←2
  │ !! fix_cmd                    282L  0C    4m  CC=18     ←0
  │ executor                   271L  4C   11m  CC=11     ←0
  │ !! __init__                   267L  2C   12m  CC=15     ←0
  │ session_io                 258L  0C   26m  CC=8      ←1
  │ web_search                 254L  1C    9m  CC=9      ←3
  │ provider_cmd               250L  0C    3m  CC=9      ←0
  │ service_scanner            249L  3C    8m  CC=7      ←0
  │ !! service_details            242L  1C    7m  CC=17     ←0
  │ !! llm_shell                  240L  0C    4m  CC=15     ←0
  │ session_handlers           227L  0C   10m  CC=9      ←0
  │ hitl_session               214L  1C   12m  CC=7      ←0
  │ !! llm                        206L  2C    6m  CC=15     ←0
  │ !! installer                  196L  1C   11m  CC=27     ←0
  │ !! scan_cmd                   187L  0C    3m  CC=18     ←1
  │ platform_utils             184L  0C   10m  CC=8      ←9
  │ !! features_cmd               176L  0C    6m  CC=15     ←0
  │ !! security                   171L  1C    6m  CC=16     ←0
  │ graph                      163L  2C   11m  CC=13     ←0
  │ rollback                   162L  2C    6m  CC=7      ←2
  │ main                       158L  0C    3m  CC=6      ←0
  │ system_checks              156L  0C    8m  CC=6      ←2
  │ config_interactive         149L  0C    5m  CC=9      ←0
  │ resources                  137L  1C    6m  CC=14     ←0
  │ orchestrate_cmd            132L  0C    1m  CC=13     ←0
  │ hardware                   129L  1C    6m  CC=12     ←0
  │ auditor                    127L  2C    5m  CC=10     ←0
  │ registry                   127L  1C    8m  CC=7      ←0
  │ renderer                   124L  1C    4m  CC=8      ←1
  │ token_cmd                  124L  0C    4m  CC=7      ←0
  │ watch                      120L  1C    5m  CC=12     ←0
  │ catalog                    119L  3C    7m  CC=7      ←1
  │ thumbnails                 118L  1C    5m  CC=10     ←0
  │ !! report_cmd                 115L  0C    1m  CC=16     ←0
  │ disk                       113L  1C    4m  CC=12     ←0
  │ audio                      107L  1C    5m  CC=10     ←0
  │ !! system_core                105L  0C    1m  CC=16     ←0
  │ base                        99L  4C    4m  CC=2      ←0
  │ session_core                92L  1C    2m  CC=10     ←1
  │ resources                   91L  0C    1m  CC=13     ←0
  │ rollback_cmd                90L  0C    4m  CC=7      ←0
  │ profiles                    88L  1C    4m  CC=8      ←1
  │ anonymizer                  86L  0C    2m  CC=5      ←6
  │ security                    84L  0C    1m  CC=4      ←0
  │ config_cmd                  83L  0C    4m  CC=4      ←0
  │ quickfix_cmd                76L  0C    1m  CC=12     ←0
  │ system_checks               73L  0C    1m  CC=7      ←0
  │ schemas                     71L  5C    0m  CC=0.0    ←0
  │ __init__                    65L  1C    3m  CC=4      ←2
  │ thumbnails                  62L  0C    1m  CC=1      ←0
  │ shared                      62L  1C    3m  CC=6      ←0
  │ audio                       60L  0C    1m  CC=1      ←0
  │ profile_cmd                 59L  0C    3m  CC=4      ←0
  │ autonomous                  49L  0C    1m  CC=1      ←0
  │ history_cmd                 49L  0C    1m  CC=5      ←0
  │ watch_cmd                   49L  0C    1m  CC=2      ←0
  │ _shared                     44L  0C    2m  CC=7      ←6
  │ hardware                    42L  0C    1m  CC=1      ←0
  │ __init__                    39L  0C    1m  CC=2      ←3
  │ hitl                        36L  0C    1m  CC=1      ←1
  │ __init__                    20L  0C    0m  CC=0.0    ←0
  │ timeout                     17L  1C    1m  CC=1      ←0
  │ sysadmin.yaml               13L  0C    0m  CC=0.0    ←0
  │ developer.yaml              13L  0C    0m  CC=0.0    ←0
  │ desktop.yaml                12L  0C    0m  CC=0.0    ←0
  │ __init__                    11L  0C    0m  CC=0.0    ←0
  │ server.yaml                 11L  0C    0m  CC=0.0    ←0
  │ developer.yaml              10L  0C    0m  CC=0.0    ←0
  │ office.yaml                  9L  0C    0m  CC=0.0    ←0
  │ __init__                     9L  0C    0m  CC=0.0    ←0
  │ __init__                     8L  0C    0m  CC=0.0    ←0
  │ minimal.yaml                 5L  0C    0m  CC=0.0    ←0
  │ __init__                     4L  0C    0m  CC=0.0    ←0
  │ __init__                     3L  0C    0m  CC=0.0    ←0
  │ __init__                     2L  0C    0m  CC=0.0    ←0
  │ __init__                     2L  0C    0m  CC=0.0    ←0
  │ __init__                     2L  0C    0m  CC=0.0    ←0
  │ __init__                     1L  0C    0m  CC=0.0    ←0
  │ __init__                     0L  0C    0m  CC=0.0    ←0
  │
  docs/                           CC̄=1.0    ←in:0  →out:0
  │ mkdocs.yml                  20L  0C    0m  CC=0.0    ←0
  │ quickstart                  14L  0C    1m  CC=1      ←1
  │ advanced_usage               9L  0C    0m  CC=0.0    ←0
  │
  docker/                         CC̄=0.0    ←in:0  →out:0
  │ docker-compose.yml         161L  0C    0m  CC=0.0    ←0
  │ docker-compose.multi-system.yml   160L  0C    0m  CC=0.0    ←0
  │ test-multi-system.sh       128L  0C    1m  CC=0.0    ←0
  │ Dockerfile                   0L  0C    0m  CC=0.0    ←0
  │ Dockerfile                   0L  0C    0m  CC=0.0    ←0
  │ Dockerfile                   0L  0C    0m  CC=0.0    ←0
  │ Dockerfile                   0L  0C    0m  CC=0.0    ←0
  │ Dockerfile                   0L  0C    0m  CC=0.0    ←0
  │ Dockerfile                   0L  0C    0m  CC=0.0    ←0
  │ Dockerfile                   0L  0C    0m  CC=0.0    ←0
  │ Dockerfile                   0L  0C    0m  CC=0.0    ←0
  │ Dockerfile                   0L  0C    0m  CC=0.0    ←0
  │ Dockerfile                   0L  0C    0m  CC=0.0    ←0
  │
  project/                        CC̄=0.0    ←in:0  →out:0
  │ !! calls.yaml                2141L  0C    0m  CC=0.0    ←0
  │ !! map.toon.yaml              832L  0C  198m  CC=0.0    ←0
  │ calls.toon.yaml            273L  0C    0m  CC=0.0    ←0
  │ analysis.toon.yaml         226L  0C    0m  CC=0.0    ←0
  │ validation.toon.yaml       114L  0C    0m  CC=0.0    ←0
  │ project_refactor.yaml       87L  0C    0m  CC=0.0    ←0
  │ evolution.toon.yaml         82L  0C    0m  CC=0.0    ←0
  │ duplication.toon.yaml       64L  0C    0m  CC=0.0    ←0
  │ project.toon.yaml           64L  0C    0m  CC=0.0    ←0
  │ prompt.txt                  47L  0C    0m  CC=0.0    ←0
  │ validation.toon.yaml        33L  0C    0m  CC=0.0    ←0
  │
  ./                              CC̄=0.0    ←in:0  →out:0
  │ !! planfile.yaml             2450L  0C    0m  CC=0.0    ←0
  │ goal.yaml                  429L  0C    0m  CC=0.0    ←0
  │ pyqual.yaml                121L  0C    0m  CC=0.0    ←0
  │ prefact.yaml                82L  0C    0m  CC=0.0    ←0
  │ pyproject.toml              74L  0C    0m  CC=0.0    ←0
  │ project.sh                  50L  0C    0m  CC=0.0    ←0
  │ setup                       45L  0C    0m  CC=0.0    ←0
  │ requirements.txt            31L  0C    0m  CC=0.0    ←0
  │ requirements-dev.txt        14L  0C    0m  CC=0.0    ←0
  │ pytest.ini                  12L  0C    0m  CC=0.0    ←0
  │ Makefile                     0L  0C    0m  CC=0.0    ←0
  │
  testql-scenarios/               CC̄=0.0    ←in:0  →out:0
  │ generated-cli-tests.testql.toon.yaml    20L  0C    0m  CC=0.0    ←0
  │ generated-from-pytests.testql.toon.yaml    14L  0C    0m  CC=0.0    ←0
  │
  ── zero ──
     Makefile                                  0L
     docker/alpine/Dockerfile                  0L
     docker/arch/Dockerfile                    0L
     docker/base/Dockerfile                    0L
     docker/broken-audio/Dockerfile            0L
     docker/broken-full/Dockerfile             0L
     docker/broken-network/Dockerfile          0L
     docker/broken-thumbnails/Dockerfile       0L
     docker/debian/Dockerfile                  0L
     docker/fedora/Dockerfile                  0L
     docker/ubuntu/Dockerfile                  0L
     fixos/interactive/__init__.py             0L

COUPLING:
                                   fixos           fixos.cli         fixos.agent       fixos.plugins         fixos.utils      fixos.features  fixos.orchestrator       docs.examples   fixos.diagnostics
               fixos                  ──                 ←20                 ←20                 ←32                                                          ←4                                          hub
           fixos.cli                  20                  ──                   1                                                          12                   4                   1                   1  !! fan-out
         fixos.agent                  20                  ←1                  ──                                      14                                                                                  !! fan-out
       fixos.plugins                  32                                                          ──                                                                                                      !! fan-out
         fixos.utils                                                         ←14                                      ──                                      ←4                                          hub
      fixos.features                                     ←12                                                                              ──                                                              hub
  fixos.orchestrator                   4                  ←4                                                           4                                      ──                                          !! fan-out
       docs.examples                                      ←1                                                                                                                      ──                    
   fixos.diagnostics                                      ←1                                                                                                                                          ──
  CYCLES: none
  HUB: fixos.features/ (fan-in=12)
  HUB: fixos.utils/ (fan-in=18)
  HUB: fixos/ (fan-in=76)
  SMELL: fixos.plugins/ fan-out=32 → split needed
  SMELL: fixos.agent/ fan-out=34 → split needed
  SMELL: fixos.orchestrator/ fan-out=8 → split needed
  SMELL: fixos.cli/ fan-out=39 → split needed

EXTERNAL:
  validation: run `vallm batch .` → validation.toon
  duplication: run `redup scan .` → duplication.toon
```

### Duplication (`project/duplication.toon.yaml`)

```toon markpact:analysis path=project/duplication.toon.yaml
# redup/duplication | 3 groups | 90f 15885L | 2026-05-04

SUMMARY:
  files_scanned: 90
  total_lines:   15885
  dup_groups:    3
  dup_fragments: 13
  saved_lines:   38
  scan_ms:       5342

HOTSPOTS[7] (files with most duplication):
  fixos/utils/terminal.py  dup=22L  groups=1  frags=2  (0.1%)
  fixos/agent/session_io.py  dup=18L  groups=1  frags=6  (0.1%)
  fixos/cli/config_cmd.py  dup=3L  groups=1  frags=1  (0.0%)
  fixos/cli/features_cmd.py  dup=3L  groups=1  frags=1  (0.0%)
  fixos/cli/profile_cmd.py  dup=3L  groups=1  frags=1  (0.0%)
  fixos/cli/rollback_cmd.py  dup=3L  groups=1  frags=1  (0.0%)
  fixos/cli/token_cmd.py  dup=3L  groups=1  frags=1  (0.0%)

DUPLICATES[3] (ranked by impact):
  [8967cd01b62426bf]   STRU  print_timeout  L=3 N=6 saved=15 sim=1.00
      fixos/agent/session_io.py:191-193  (print_timeout)
      fixos/agent/session_io.py:196-198  (print_session_ended)
      fixos/agent/session_io.py:201-203  (print_session_interrupted)
      fixos/agent/session_io.py:211-213  (print_no_commands)
      fixos/agent/session_io.py:221-223  (print_no_results)
      fixos/agent/session_io.py:226-228  (print_searching)
  [aaae754bdb04529d]   STRU  config  L=3 N=5 saved=12 sim=1.00
      fixos/cli/config_cmd.py:8-10  (config)
      fixos/cli/features_cmd.py:21-23  (features)
      fixos/cli/profile_cmd.py:8-10  (profile)
      fixos/cli/rollback_cmd.py:9-11  (rollback)
      fixos/cli/token_cmd.py:10-12  (token)
  [21fbbebb19cf00fb]   STRU  print_stdout_box  L=11 N=2 saved=11 sim=1.00
      fixos/utils/terminal.py:183-193  (print_stdout_box)
      fixos/utils/terminal.py:196-206  (print_stderr_box)

REFACTOR[3] (ranked by priority):
  [1] ○ extract_function   → fixos/agent/utils/print_timeout.py
      WHY: 6 occurrences of 3-line block across 1 files — saves 15 lines
      FILES: fixos/agent/session_io.py
  [2] ○ extract_function   → fixos/cli/utils/config.py
      WHY: 5 occurrences of 3-line block across 5 files — saves 12 lines
      FILES: fixos/cli/config_cmd.py, fixos/cli/features_cmd.py, fixos/cli/profile_cmd.py, fixos/cli/rollback_cmd.py, fixos/cli/token_cmd.py
  [3] ○ extract_function   → fixos/utils/utils/print_stdout_box.py
      WHY: 2 occurrences of 11-line block across 1 files — saves 11 lines
      FILES: fixos/utils/terminal.py

QUICK_WINS[3] (low risk, high savings — do first):
  [1] extract_function   saved=15L  → fixos/agent/utils/print_timeout.py
      FILES: session_io.py
  [2] extract_function   saved=12L  → fixos/cli/utils/config.py
      FILES: config_cmd.py, features_cmd.py, profile_cmd.py +2
  [3] extract_function   saved=11L  → fixos/utils/utils/print_stdout_box.py
      FILES: terminal.py

EFFORT_ESTIMATE (total ≈ 1.3h):
  medium print_timeout                       saved=15L  ~30min
  easy   config                              saved=12L  ~24min
  easy   print_stdout_box                    saved=11L  ~22min

METRICS-TARGET:
  dup_groups:  3 → 0
  saved_lines: 38 lines recoverable
```

### Evolution / Churn (`project/evolution.toon.yaml`)

```toon markpact:analysis path=project/evolution.toon.yaml
# code2llm/evolution | 678 func | 75f | 2026-05-04

NEXT[10] (ranked by impact):
  [1] !! SPLIT           fixos/cli/cleanup_cmd.py
      WHY: 1246L, 0 classes, max CC=172
      EFFORT: ~4h  IMPACT: 214312

  [2] !! SPLIT           fixos/diagnostics/flatpak_analyzer.py
      WHY: 944L, 3 classes, max CC=27
      EFFORT: ~4h  IMPACT: 25488

  [3] !! SPLIT           fixos/diagnostics/storage_analyzer.py
      WHY: 1058L, 2 classes, max CC=22
      EFFORT: ~4h  IMPACT: 23276

  [4] !! SPLIT-FUNC      _cleanup_full_system  CC=172  fan=61
      WHY: CC=172 exceeds 15
      EFFORT: ~1h  IMPACT: 10492

  [5] !  SPLIT-FUNC      fix  CC=18  fan=21
      WHY: CC=18 exceeds 15
      EFFORT: ~1h  IMPACT: 378

  [6] !  SPLIT-FUNC      report  CC=16  fan=22
      WHY: CC=16 exceeds 15
      EFFORT: ~1h  IMPACT: 352

  [7] !  SPLIT-FUNC      run_llm_shell  CC=15  fan=23
      WHY: CC=15 exceeds 15
      EFFORT: ~1h  IMPACT: 345

  [8] !  SPLIT-FUNC      diagnose_system  CC=16  fan=19
      WHY: CC=16 exceeds 15
      EFFORT: ~1h  IMPACT: 304

  [9] !  SPLIT-FUNC      render_md  CC=16  fan=19
      WHY: CC=16 exceeds 15
      EFFORT: ~1h  IMPACT: 304

  [10] !! SPLIT-FUNC      FlatpakAnalyzer.get_cleanup_recommendations  CC=27  fan=11
      WHY: CC=27 exceeds 15
      EFFORT: ~1h  IMPACT: 297


RISKS[3]:
  ⚠ Splitting fixos/cli/cleanup_cmd.py may break 14 import paths
  ⚠ Splitting fixos/diagnostics/storage_analyzer.py may break 31 import paths
  ⚠ Splitting fixos/diagnostics/flatpak_analyzer.py may break 24 import paths

METRICS-TARGET:
  CC̄:          3.7 → ≤2.6
  max-CC:      172 → ≤20
  god-modules: 3 → 0
  high-CC(≥15): 26 → ≤13
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
  prev CC̄=3.7 → now CC̄=3.7
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
