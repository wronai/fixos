# fixOS v2.2.6 🔧🤖

AI-powered Linux/Windows diagnostics and repair – audio, hardware, system issues

## Contents

- [Metadata](#metadata)
- [Architecture](#architecture)
- [Interfaces](#interfaces)
- [Workflows](#workflows)
- [Quality Pipeline (`pyqual.yaml`)](#quality-pipeline-pyqualyaml)
- [Configuration](#configuration)
- [Dependencies](#dependencies)
- [Deployment](#deployment)
- [Environment Variables (`.env.example`)](#environment-variables-envexample)
- [Release Management (`goal.yaml`)](#release-management-goalyaml)
- [Makefile Targets](#makefile-targets)
- [Code Analysis](#code-analysis)
- [Call Graph](#call-graph)
- [Test Contracts](#test-contracts)
- [Intent](#intent)

## Metadata

- **name**: `fixos`
- **version**: `2.2.16`
- **python_requires**: `>=3.10`
- **license**: {'text': 'Apache-2.0'}
- **ai_model**: `openrouter/qwen/qwen3-coder-next`
- **ecosystem**: SUMD + DOQL + testql + taskfile
- **generated_from**: pyproject.toml, requirements-dev.txt, requirements.txt, Makefile, testql(2), app.doql.less, pyqual.yaml, goal.yaml, .env.example, docker-compose.yml, project/(2 analysis files)

## Architecture

```
SUMD (description) → DOQL/source (code) → taskfile (automation) → testql (verification)
```

### DOQL Application Declaration (`app.doql.less`)

```less markpact:doql path=app.doql.less
// LESS format — define @variables here as needed

app {
  name: fixos;
  version: 2.2.16;
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

## Interfaces

### CLI Entry Points

- `fixos`

### testql Scenarios

#### `testql-scenarios/generated-cli-tests.testql.toon.yaml`

```toon markpact:testql path=testql-scenarios/generated-cli-tests.testql.toon.yaml
# SCENARIO: CLI Command Tests
# TYPE: cli
# GENERATED: true

CONFIG[2]{key, value}:
  cli_command, python -m fixOS
  timeout_ms, 10000

# Test 1: CLI help command
SHELL "python -m fixOS --help" 5000
ASSERT_EXIT_CODE 0
ASSERT_STDOUT_CONTAINS "usage"

# Test 2: CLI version command
SHELL "python -m fixOS --version" 5000
ASSERT_EXIT_CODE 0

# Test 3: CLI main workflow (dry-run)
SHELL "python -m fixOS --help" 10000
ASSERT_EXIT_CODE 0
```

#### `testql-scenarios/generated-from-pytests.testql.toon.yaml`

```toon markpact:testql path=testql-scenarios/generated-from-pytests.testql.toon.yaml
# SCENARIO: Auto-generated from Python Tests
# TYPE: integration
# GENERATED: true

CONFIG[2]{key, value}:
  base_url, ${api_url:-http://localhost:8101}
  timeout_ms, 10000

# Converted 4 assertions from pytest
ASSERT[4]{field, operator, expected}:
  result.exit_code, ==, 0
  result.exit_code, ==, 0
  result.exit_code, ==, 0
  result.exit_code, ==, 0
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

## Configuration

```yaml
project:
  name: fixos
  version: 2.2.16
  env: local
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

## Deployment

```bash markpact:run
pip install fixos

# development install
pip install -e .[dev]
```

### Requirements Files

#### `requirements-dev.txt`

- `pytest>=7.4.0`
- `pytest-mock>=3.12.0`
- `pytest-cov>=4.1.0`
- `ruff>=0.4.0`
- `black>=24.0.0`

#### `requirements.txt`

- `openai>=1.35.0`
- `prompt_toolkit>=3.0.43`
- `psutil>=5.9.0`
- `pyyaml>=6.0`
- `click>=8.1.0`
- `python-dotenv>=1.0.0`
- `rich>=13.0`
- `pydantic>=2.0`

### Docker Compose (`docker-compose.yml`)

- **base** image=`fixos-base:latest`
- **broken-audio** image=`fixos-broken-audio:latest`
- **broken-thumbnails** image=`fixos-broken-thumbnails:latest`
- **broken-network** image=`fixos-broken-network:latest`
- **broken-full** image=`fixos-broken-full:latest`
- **e2e-tests** image=`{'context': '..', 'dockerfile': 'docker/base/Dockerfile'}`
- **unit-tests** image=`{'context': '..', 'dockerfile': 'docker/base/Dockerfile'}`
- **cli-tests** image=`{'context': '..', 'dockerfile': 'docker/base/Dockerfile'}`

## Environment Variables (`.env.example`)

| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_PROVIDER` | `gemini` | Dostępne: gemini, openai, xai, openrouter, ollama |
| `GEMINI_API_KEY` | `AIzaSy_TWOJ_KLUCZ_GEMINI` | Utwórz klucz: https://aistudio.google.com/apikey |
| `GEMINI_MODEL` | `gemini-2.5-flash-preview-04-17` |  |
| `GEMINI_BASE_URL` | `https://generativelanguage.googleapis.com/v1beta/openai/` |  |
| `OPENAI_API_KEY` | `sk-TWOJ_KLUCZ_OPENAI` | ── OpenAI (opcjonalny) ─────────────────────────────────── |
| `OPENAI_MODEL` | `gpt-4o-mini` |  |
| `OPENAI_BASE_URL` | `https://api.openai.com/v1` |  |
| `XAI_API_KEY` | `xai-TWOJ_KLUCZ_XAI` | ── xAI Grok (opcjonalny) ───────────────────────────────── |
| `XAI_MODEL` | `grok-beta` |  |
| `XAI_BASE_URL` | `https://api.x.ai/v1` |  |
| `OPENROUTER_API_KEY` | `sk-or-TWOJ_KLUCZ` | ── OpenRouter (opcjonalny, daje dostęp do wielu modeli) ── |
| `OPENROUTER_MODEL` | `google/gemini-2.0-flash-exp:free` |  |
| `OPENROUTER_BASE_URL` | `https://openrouter.ai/api/v1` |  |
| `OLLAMA_BASE_URL` | `http://localhost:11434/v1` | ── Ollama (lokalny, bez klucza) ────────────────────────── |
| `OLLAMA_MODEL` | `llama3.2` |  |
| `AGENT_MODE` | `hitl` | autonomous = autonomiczny (wykonuje automatycznie) |
| `SESSION_TIMEOUT` | `3600` | ── Timeout sesji (sekundy) ─────────────────────────────── |
| `ENABLE_WEB_SEARCH` | `true` | Używane gdy LLM nie znajdzie rozwiązania |
| `SERPAPI_KEY` | `*(not set)*` | SerpAPI (opcjonalny, lepsza jakość) |
| `SHOW_ANONYMIZED_DATA` | `true` | Pokaż zanonimizowane dane użytkownikowi przed wysłaniem do LLM |
| `SAVE_REPORTS` | `false` | Zapisuj raporty diagnostyczne |
| `REPORTS_DIR` | `/tmp/fixos-reports` |  |
| `TEST_DOCKER_COMPOSE` | `docker/docker-compose.yml` | Używane przez testy e2e |

## Release Management (`goal.yaml`)

- **versioning**: `semver`
- **commits**: `conventional` scope=`fixfedora`
- **changelog**: `keep-a-changelog`
- **build strategies**: `python`, `nodejs`, `rust`
- **version files**: `VERSION`, `pyproject.toml:version`, `setup.py:version`, `fixos/__init__.py:__version__`

## Makefile Targets

- `help` — ── Domyślna komenda ──────────────────────────────────────
- `install` — ── Instalacja ────────────────────────────────────────────
- `install-dev`
- `test` — ── Testy ─────────────────────────────────────────────────
- `test-fast`
- `test-quick`
- `test-unit`
- `test-unit-fast`
- `test-unit-par`
- `test-e2e`
- `test-real`
- `test-cov`
- `lint` — ── Jakość kodu ───────────────────────────────────────────
- `format`
- `docker-build` — ── Docker ───────────────────────────────────────────────
- `docker-audio`
- `docker-thumb`
- `docker-full`
- `docker-e2e`
- `docker-test-fedora` — ── Multi-System Docker Tests ────────────────────────────
- `docker-test-ubuntu`
- `docker-test-debian`
- `docker-test-arch`
- `docker-test-alpine`
- `docker-test-all`
- `config-init` — ── Uruchomienie ──────────────────────────────────────────
- `run-scan`
- `run-fix`
- `build` — ── Paczka ───────────────────────────────────────────────
- `publish`
- `clean`

## Code Analysis

### `project/map.toon.yaml`

```toon markpact:analysis path=project/map.toon.yaml
# fixOS | 114f 19756L | python:111,shell:2,less:1 | 2026-05-04
# stats: 256 func | 123 cls | 114 mod | CC̄=4.4 | critical:26 | cycles:0
# alerts[5]: CC _match_heuristic_command=18; CC _handle_snap_management=18; CC _cleanup_full_system=18; CC cleanup_services=16; CC _select_cleanup_items_by_filter=16
# hotspots[5]: orchestrate fan=24; diagnose_system fan=20; _cleanup_flatpak_detailed fan=19; _handle_home_analysis fan=18; token_set fan=18
# evolution: baseline
# Keys: M=modules, D=details, i=imports, e=exports, c=classes, f=functions, m=methods
M[114]:
  app.doql.less,232
  docker/test-multi-system.sh,129
  docs/examples/advanced_usage.py,10
  docs/examples/quickstart.py,14
  fixos/__init__.py,3
  fixos/agent/__init__.py,39
  fixos/agent/autonomous.py,50
  fixos/agent/autonomous_session.py,434
  fixos/agent/hitl.py,37
  fixos/agent/hitl_session.py,221
  fixos/agent/session_core.py,94
  fixos/agent/session_handlers.py,229
  fixos/agent/session_io.py,259
  fixos/anonymizer.py,87
  fixos/cli/__init__.py,9
  fixos/cli/ask_cmd.py,355
  fixos/cli/cleanup_cmd.py,1209
  fixos/cli/config_cmd.py,84
  fixos/cli/features_cmd.py,177
  fixos/cli/fix_cmd.py,285
  fixos/cli/history_cmd.py,50
  fixos/cli/main.py,159
  fixos/cli/orchestrate_cmd.py,133
  fixos/cli/profile_cmd.py,60
  fixos/cli/provider_cmd.py,251
  fixos/cli/quickfix_cmd.py,77
  fixos/cli/report_cmd.py,119
  fixos/cli/rollback_cmd.py,91
  fixos/cli/scan_cmd.py,195
  fixos/cli/shared.py,63
  fixos/cli/token_cmd.py,125
  fixos/cli/watch_cmd.py,50
  fixos/cli.py,96
  fixos/config.py,346
  fixos/config_interactive.py,150
  fixos/constants.py,28
  fixos/diagnostics/__init__.py,3
  fixos/diagnostics/checks/__init__.py,21
  fixos/diagnostics/checks/_shared.py,45
  fixos/diagnostics/checks/audio.py,61
  fixos/diagnostics/checks/hardware.py,43
  fixos/diagnostics/checks/resources.py,92
  fixos/diagnostics/checks/security.py,85
  fixos/diagnostics/checks/system_core.py,119
  fixos/diagnostics/checks/thumbnails.py,63
  fixos/diagnostics/dev_project_analyzer.py,404
  fixos/diagnostics/disk_analyzer.py,431
  fixos/diagnostics/flatpak_analyzer.py,941
  fixos/diagnostics/service_cleanup.py,474
  fixos/diagnostics/service_details.py,231
  fixos/diagnostics/service_scanner.py,250
  fixos/diagnostics/storage_analyzer.py,1087
  fixos/diagnostics/system_checks.py,74
  fixos/features/__init__.py,261
  fixos/features/auditor.py,128
  fixos/features/catalog.py,120
  fixos/features/installer.py,197
  fixos/features/profiles.py,89
  fixos/features/renderer.py,125
  fixos/fixes/__init__.py,5
  fixos/interactive/__init__.py,1
  fixos/interactive/cleanup_planner.py,414
  fixos/llm_shell.py,237
  fixos/orchestrator/__init__.py,10
  fixos/orchestrator/executor.py,272
  fixos/orchestrator/graph.py,164
  fixos/orchestrator/orchestrator.py,396
  fixos/orchestrator/rollback.py,163
  fixos/platform_utils.py,185
  fixos/plugins/__init__.py,12
  fixos/plugins/base.py,100
  fixos/plugins/builtin/__init__.py,2
  fixos/plugins/builtin/audio.py,108
  fixos/plugins/builtin/disk.py,114
  fixos/plugins/builtin/hardware.py,130
  fixos/plugins/builtin/resources.py,138
  fixos/plugins/builtin/security.py,172
  fixos/plugins/builtin/thumbnails.py,119
  fixos/plugins/registry.py,128
  fixos/profiles/__init__.py,66
  fixos/providers/__init__.py,3
  fixos/providers/llm.py,212
  fixos/providers/llm_analyzer.py,334
  fixos/providers/schemas.py,72
  fixos/system_checks.py,157
  fixos/utils/__init__.py,4
  fixos/utils/anonymizer.py,289
  fixos/utils/terminal.py,327
  fixos/utils/timeout.py,18
  fixos/utils/web_search.py,255
  fixos/watch.py,121
  project.sh,50
  scripts/pyqual-calibrate.py,300
  setup.py,46
  test_kwarg.py,10
  test_timeout_fix.py,68
  tests/__init__.py,1
  tests/conftest.py,225
  tests/e2e/__init__.py,1
  tests/e2e/test_anonymization_layers.py,592
  tests/e2e/test_audio_broken.py,240
  tests/e2e/test_cli.py,279
  tests/e2e/test_executor.py,227
  tests/e2e/test_multi_system.py,170
  tests/e2e/test_network_broken.py,284
  tests/e2e/test_thumbnails_broken.py,249
  tests/test_fixos.py,12
  tests/unit/__init__.py,1
  tests/unit/test_anonymizer.py,199
  tests/unit/test_core.py,125
  tests/unit/test_executor.py,239
  tests/unit/test_orchestrator.py,314
  tests/unit/test_service_cleanup.py,68
  tests/unit/test_service_scanner.py,34
D:
  docs/examples/advanced_usage.py:
  docs/examples/quickstart.py:
    e: run_autonomous_session
    run_autonomous_session()
  fixos/__init__.py:
  fixos/agent/__init__.py:
    e: get_remaining_time
    get_remaining_time(session)
  fixos/agent/autonomous.py:
    e: run_autonomous_session
    run_autonomous_session(diagnostics;config;show_data;max_fixes)
  fixos/agent/autonomous_session.py:
    e: run_autonomous_session,FixAction,AgentReport,AutonomousSession
    FixAction:
    AgentReport: summary(0)
    AutonomousSession: __init__(4),_setup_timeout(0),_clear_timeout(0),_confirm_start(0),_initialize_messages(0),_get_remaining_time(0),_check_timeout(0),_query_llm(0),_handle_llm_error(0),_parse_action(1),_is_forbidden(1),_add_sudo(1),_execute_command(1),_handle_search(1),_handle_exec(1),_handle_skip(1),_handle_done(0),_process_turn(0),run(0),_print_report(0)  # Self-directed autonomous diagnostic and repair session.
    run_autonomous_session(diagnostics;config;show_data;max_fixes)
  fixos/agent/hitl.py:
    e: run_hitl_session
    run_hitl_session(diagnostics;config;show_data)
  fixos/agent/hitl_session.py:
    e: run_hitl_session,HITLSession
    HITLSession: __init__(3),_setup_timeout(0),_clear_timeout(0),remaining(0),_initialize_messages(0),_print_header(0),_handle_llm_error(0),_check_low_confidence(1),_process_turn(0),run(0),_print_summary(0)  # Interactive Human-in-the-Loop diagnostic and repair session.
    run_hitl_session(diagnostics;config;show_data)
  fixos/agent/session_core.py:
    e: extract_fixes,extract_search_topic,CmdResult
    CmdResult:  # Result of executed command.
    extract_fixes(reply)
    extract_search_topic(llm_reply)
  fixos/agent/session_handlers.py:
    e: handle_quit,handle_skip_all,handle_describe_problem,handle_execute_all,handle_fix_by_number,handle_direct_command,handle_search,handle_free_text,run_single_command,parse_user_input
    handle_quit()
    handle_skip_all(messages)
    handle_describe_problem(messages;ask_fn)
    handle_execute_all(fixes;messages;executed;run_cmd_fn)
    handle_fix_by_number(user_in;fixes;messages;executed;run_cmd_fn)
    handle_direct_command(user_in;messages;executed;run_cmd_fn)
    handle_search(user_in;messages;serpapi_key)
    handle_free_text(user_in;messages)
    run_single_command(cmd;comment)
    parse_user_input(user_in;fixes;messages;executed;serpapi_key)
  fixos/agent/session_io.py:
    e: _suspend_timeout,_setup_timeout_ref,print_session_header,fmt_time,print_action_menu,ask_user_problem,print_cmd_preview,print_cmd_result,print_session_summary,print_thinking,clear_thinking,print_llm_reply,print_llm_error,print_blocked_command,print_timeout,print_session_ended,print_session_interrupted,print_executing_all,print_no_commands,print_invalid_option,print_no_results,print_searching,ask_execute_prompt,ask_low_confidence_search,ask_send_data,get_user_input
    _suspend_timeout()
    _setup_timeout_ref(session;seconds;handler)
    print_session_header(os_info;pkg_manager;model;timeout;remaining_fn)
    fmt_time(s)
    print_action_menu(fixes;remaining;total_tokens)
    ask_user_problem()
    print_cmd_preview(cmd;comment)
    print_cmd_result(result)
    print_session_summary(messages_count;elapsed;total_tokens;executed)
    print_thinking()
    clear_thinking()
    print_llm_reply(reply)
    print_llm_error(e)
    print_blocked_command(cmd;reason)
    print_timeout()
    print_session_ended()
    print_session_interrupted()
    print_executing_all(count)
    print_no_commands()
    print_invalid_option(user_in;max_option)
    print_no_results()
    print_searching()
    ask_execute_prompt()
    ask_low_confidence_search()
    ask_send_data()
    get_user_input(remaining)
  fixos/anonymizer.py:
    e: get_sensitive_values,anonymize
    get_sensitive_values()
    anonymize(data_str)
  fixos/cli/__init__.py:
  fixos/cli/ask_cmd.py:
    e: ask,_match_heuristic_command,_format_command,_build_output_dict,_execute_heuristic_command,_execute_with_llm,_handle_natural_command,_validate_result_with_llm
    ask(prompt;dry_run)
    _match_heuristic_command(prompt_lower)
    _format_command(matched_cmd)
    _build_output_dict(status;prompt;source;command;exit_code;stdout;stderr;llm;reason;message;error)
    _execute_heuristic_command(cmd_str;prompt;dry_run;cfg)
    _execute_with_llm(prompt;dry_run;cfg)
    _handle_natural_command(prompt;dry_run)
    _validate_result_with_llm(prompt;cmd_str;result;cfg)
  fixos/cli/cleanup_cmd.py:
    e: cleanup_services,_display_cleanup_summary,_display_service_item,_execute_safe_cleanup,_format_hint_line,_display_service_group,_display_unsafe_services,_cleanup_single_service,_cleanup_flatpak_detailed,_display_flatpak_status,_display_detailed_recommendations,_parse_selection,_parse_size_to_bytes,_format_bytes,_build_dep_types,_display_full_system_menu,_snap_fetch_packages,_snap_remove_packages,_handle_snap_management,_parse_numeric_range_set,_display_home_items,_resolve_home_selection,_remove_home_items,_handle_home_analysis,_show_home_item_info,_query_info,_query_path,_query_cmd,_query_filter,_handle_select_query,_handle_interactive_select,_filter_by_age,_filter_by_prefix_top,_filter_by_prefix_category,_filter_by_prefix_type,_select_cleanup_items_by_filter,_execute_full_cleanup,_cleanup_full_system,_parse_size_to_gb
    cleanup_services(threshold;services;json_output;cleanup;dry_run;list_only;full_analysis)
    _display_cleanup_summary(plan;threshold)
    _display_service_item(svc)
    _execute_safe_cleanup(services;scanner)
    _format_hint_line(hint)
    _display_service_group(service_type;svcs;type_map)
    _display_unsafe_services(services)
    _cleanup_single_service(service_name;scanner;json_output;dry_run)
    _cleanup_flatpak_detailed(scanner;json_output;dry_run)
    _display_flatpak_status(analysis)
    _display_detailed_recommendations(recommendations)
    _parse_selection(selection;max_count)
    _parse_size_to_bytes(size_str)
    _format_bytes(size_bytes)
    _build_dep_types(items)
    _display_full_system_menu(analyzer;analysis;safe_items;medium_items;dry_run)
    _snap_fetch_packages(analyzer)
    _snap_remove_packages(packages_to_remove)
    _handle_snap_management(analyzer;dry_run)
    _parse_numeric_range_set(nums)
    _display_home_items(large_files;large_dirs)
    _resolve_home_selection(nums;large_files;large_dirs)
    _remove_home_items(items_to_remove)
    _handle_home_analysis(analyzer;dry_run)
    _show_home_item_info(nums;large_files;large_dirs;total_items)
    _query_info(nums;analyzer)
    _query_path(nums;analyzer)
    _query_cmd(nums;analyzer)
    _query_filter(nums;analyzer)
    _handle_select_query(nums;analyzer)
    _handle_interactive_select(analyzer;dry_run)
    _filter_by_age(analyzer;days;label)
    _filter_by_prefix_top(selection;analyzer)
    _filter_by_prefix_category(selection;analyzer)
    _filter_by_prefix_type(selection;analyzer)
    _select_cleanup_items_by_filter(selection;analyzer;safe_items)
    _execute_full_cleanup(items_to_clean;dry_run)
    _cleanup_full_system(json_output;dry_run)
    _parse_size_to_gb(size_str)
  fixos/cli/config_cmd.py:
    e: config,config_show,config_init,config_set
    config()
    config_show()
    config_init(force)
    config_set(key;value)
  fixos/cli/features_cmd.py:
    e: features,features_audit,features_install,features_profiles,features_system,_interactive_profile_select
    features()
    features_audit(profile;json_output)
    features_install(profile;dry_run;yes;category)
    features_profiles()
    features_system()
    _interactive_profile_select()
  fixos/cli/fix_cmd.py:
    e: _collect_diagnostics,_run_agent_session,fix,handle_disk_cleanup_mode,execute_cleanup_actions,try_llm_fallback_for_failures
    _collect_diagnostics(modules;disc;json_output;output)
    _run_agent_session(cfg;data;max_fixes)
    fix(provider;token;model;no_banner;mode;timeout;modules;no_show_data;output;max_fixes;disc;dry_run;interactive;json_output;llm_fallback;show_raw)
    handle_disk_cleanup_mode(disk_analysis;cfg;dry_run;interactive;json_output;llm_fallback)
    execute_cleanup_actions(actions;cfg;llm_fallback)
    try_llm_fallback_for_failures(failed_actions;cfg)
  fixos/cli/history_cmd.py:
    e: history
    history(limit;json_output)
  fixos/cli/main.py:
    e: cli,_print_welcome,main
    cli(ctx;dry_run;version)
    _print_welcome()
    main()
  fixos/cli/orchestrate_cmd.py:
    e: orchestrate
    orchestrate(provider;token;model;no_banner;mode;modules;dry_run;max_iterations;output)
  fixos/cli/profile_cmd.py:
    e: profile,profile_list,profile_show
    profile()
    profile_list()
    profile_show(name)
  fixos/cli/provider_cmd.py:
    e: llm_providers,providers,test_llm
    llm_providers(free)
    providers()
    test_llm(provider;token;model;no_banner)
  fixos/cli/quickfix_cmd.py:
    e: quickfix
    quickfix(dry_run;modules)
  fixos/cli/report_cmd.py:
    e: _render_report_json,_render_report_markdown,_render_report_html,report
    _render_report_json(results;timestamp)
    _render_report_markdown(results;timestamp)
    _render_report_html(results;timestamp)
    report(output_format;output;modules;profile)
  fixos/cli/rollback_cmd.py:
    e: rollback,rollback_list,rollback_show,rollback_undo
    rollback()
    rollback_list(limit)
    rollback_show(session_id)
    rollback_undo(session_id;last;dry_run)
  fixos/cli/scan_cmd.py:
    e: scan,_display_disk_fix_mode,_display_disk_scan_mode,_run_disk_analysis,_print_quick_issues
    scan(modules;output;show_raw;no_banner;disc;dry_run;interactive;json_output;llm_fallback;profile)
    _display_disk_fix_mode(disk_analysis)
    _display_disk_scan_mode(disk_analysis)
    _run_disk_analysis(data;json_output;is_fix_mode)
    _print_quick_issues(data)
  fixos/cli/shared.py:
    e: add_common_options,add_shared_options,NaturalLanguageGroup
    NaturalLanguageGroup: resolve_command(2)  # Click group that routes unknown commands to 'ask' command.
    add_common_options(fn)
    add_shared_options(func)
  fixos/cli/token_cmd.py:
    e: token,token_set,token_show,token_clear
    token()
    token_set(key;provider;env_file)
    token_show()
    token_clear(env_file)
  fixos/cli/watch_cmd.py:
    e: watch
    watch(interval;modules;alert_on;max_iterations)
  fixos/cli.py:
  fixos/config.py:
    e: _load_env_files,detect_provider_from_key,interactive_provider_setup,get_providers_list,FixOsConfig
    FixOsConfig: load(1),validate(0),summary(0)
    _load_env_files()
    detect_provider_from_key(key)
    interactive_provider_setup()
    get_providers_list()
  fixos/config_interactive.py:
    e: _print_provider_menu,_get_user_choice,_get_api_key,_save_to_env,interactive_provider_setup
    _print_provider_menu()
    _get_user_choice(num_map)
    _get_api_key(provider)
    _save_to_env(provider;key;key_env)
    interactive_provider_setup()
  fixos/constants.py:
  fixos/diagnostics/__init__.py:
  fixos/diagnostics/checks/__init__.py:
  fixos/diagnostics/checks/_shared.py:
    e: _psutil_required,_cmd
    _psutil_required()
    _cmd(cmd;timeout)
  fixos/diagnostics/checks/audio.py:
    e: diagnose_audio
    diagnose_audio()
  fixos/diagnostics/checks/hardware.py:
    e: diagnose_hardware
    diagnose_hardware()
  fixos/diagnostics/checks/resources.py:
    e: diagnose_resources
    diagnose_resources()
  fixos/diagnostics/checks/security.py:
    e: diagnose_security
    diagnose_security()
  fixos/diagnostics/checks/system_core.py:
    e: _collect_os_info,_collect_platform_details,diagnose_system
    _collect_os_info()
    _collect_platform_details()
    diagnose_system()
  fixos/diagnostics/checks/thumbnails.py:
    e: diagnose_thumbnails
    diagnose_thumbnails()
  fixos/diagnostics/dev_project_analyzer.py:
    e: ProjectDependency,DevProjectAnalyzer
    ProjectDependency: to_dict(0),_format_size(1)  # Represents a dependency folder that can be cleaned
    DevProjectAnalyzer: __init__(1),analyze(1),_scan_directory(3),_check_dependency_folder(1),_create_dependency(3),_get_dir_size(1),_check_can_recreate(2),get_old_dependencies(1),get_large_dependencies(1),get_summary(0),get_cleanup_commands(0)  # Analyze developer projects for dependency folders that can b
  fixos/diagnostics/disk_analyzer.py:
    e: main,DiskAnalyzer
    DiskAnalyzer: __init__(1),analyze_disk_usage(1),_get_disk_status(1),get_large_files(3),get_cache_dirs(2),get_log_dirs(2),get_temp_dirs(2),suggest_cleanup_actions(1),_get_dir_size_mb(1),_categorize_file(1),_identify_cache_type(1),_identify_temp_type(1),_get_oldest_file_date(1),_get_newest_file_date(1)  # Analyzes disk usage and provides cleanup suggestions
    main()
  fixos/diagnostics/flatpak_analyzer.py:
    e: analyze_flatpak_for_cleanup,FlatpakItemType,FlatpakItemInfo,FlatpakAnalyzer
    FlatpakItemType:
    FlatpakItemInfo: to_dict(0)  # Detailed info about a Flatpak item (app, runtime, or data)
    FlatpakAnalyzer: __init__(0),analyze(0),_run_flatpak_command(1),_parse_size(1),_format_size(1),_load_installed_refs(0),_find_unused_runtimes(0),_dir_total_size(1),_find_leftover_data(0),_find_orphaned_apps(0),_find_duplicate_apps(0),_get_dir_size_du(1),_get_dir_size_walk(1),_measure_path_size(1),_analyze_repo_size(0),_get_flatpak_size_note(3),get_largest_apps(1),get_cleanup_summary(0),_rec_repo_bloat(0),_rec_duplicates(0),_rec_unused_runtimes(0),_rec_large_apps(0),_rec_leftover_and_orphaned(0),_rec_hard_reset(0),get_cleanup_recommendations(0),ask_user_and_cleanup(1),_execute_cleanup_action(1),_execute_flatpak_uninstall_unused(0),_execute_flatpak_repair(0),_execute_flatpak_vacuum(0),_execute_flatpak_uninstall_all(0),_execute_leftover_data_cleanup(1)  # Advanced analyzer for Flatpak cleanup decisions
    analyze_flatpak_for_cleanup()
  fixos/diagnostics/service_cleanup.py:
    e: ServiceCleaner
    ServiceCleaner: __init__(1),get_cleanup_plan(1),cleanup_service(2),_service_to_dict(1),is_safe_cleanup(2),get_cleanup_hints(2),get_service_description(1),get_cleanup_command(2),_chrome_cleanup_command(1),get_preview_command(2)  # Plans and executes cleanup of service data.
  fixos/diagnostics/service_details.py:
    e: ServiceDetailsProvider
    ServiceDetailsProvider: get_details(2),_parse_docker_system_df(1),_get_docker_counts(1),_docker(0),_ollama(0),_conda(0),_package_cache(1),_flatpak(0),_parse_size_bytes(1)  # Provides detailed information about service data.
  fixos/diagnostics/service_scanner.py:
    e: main,ServiceType,ServiceDataInfo,ServiceDataScanner
    ServiceType:  # Service types that can be scanned and cleaned.
    ServiceDataInfo:  # Information about service data.
    ServiceDataScanner: __init__(1),scan_all_services(0),scan_service(1),_analyze_service_path(2),_get_path_size_mb(1),get_cleanup_plan(1),cleanup_service(2)  # Scans for large service data directories and allows cleanup.
    main()
  fixos/diagnostics/storage_analyzer.py:
    e: StorageItem,StorageAnalyzer
    StorageItem: to_dict(0),_format_size(1)  # Represents a storage item that can be cleaned
    StorageAnalyzer: __init__(0),analyze_full(0),_get_dir_size(1),_get_file_size(1),_run_command(1),_analyze_dnf_cache(0),_analyze_old_kernels(0),_analyze_journal_logs(0),_parse_size_static(1),_detect_docker_section(1),_parse_docker_df_output(1),_add_dangling_images_item(2),_add_build_cache_item(1),_add_docker_total_item(2),_analyze_docker(0),_analyze_podman(0),_analyze_user_cache(0),_analyze_browser_cache(0),_analyze_btrfs_snapshots(0),_analyze_coredumps(0),_analyze_orphaned_packages(0),_analyze_browser_profiles(0),_analyze_flatpak_user_data(0),_analyze_ostree_repo(0),_analyze_dev_projects(0),_analyze_system_logs(0),_analyze_home_directory(0),_find_large_files(2),_find_large_home_dirs(2),get_large_directories(1),_parse_snap_line(1),_add_snap_items(2),_analyze_snap(0),_analyze_btrfs_snapshots(0),_analyze_var_cache(0),_parse_size(1),_get_recommendations(0),get_summary(0)  # Comprehensive storage analyzer for Linux systems.
  fixos/diagnostics/system_checks.py:
    e: get_full_diagnostics
    get_full_diagnostics(modules;progress_callback)
  fixos/features/__init__.py:
    e: SystemInfo,SystemDetector
    SystemInfo:  # Complete system information snapshot.
    SystemDetector: detect(0),_detect_os_family(0),_detect_distro(0),_detect_distro_version(0),_detect_id_like(0),_detect_de(0),_detect_display_server(0),_detect_gpu_vendor(0),_detect_gpu_model(0),_detect_pkg_manager(0),_get_installed_packages(1),_get_installed_flatpaks(0)  # Detects system parameters.
  fixos/features/auditor.py:
    e: AuditResult,FeatureAuditor
    AuditResult: completion_pct(0),total_packages(0),to_dict(0)  # Result of feature audit - what's installed, what's missing.
    FeatureAuditor: __init__(2),audit(1),_check_conditions(1),_is_installed(1)  # Compares installed packages with profile requirements.
  fixos/features/catalog.py:
    e: PackageInfo,PackageCategory,PackageCatalog
    PackageInfo: get_distro_name(1),is_available_on(1)  # Information about a single package.
    PackageCategory:  # A category of packages (e.g., core_utils, dev_tools).
    PackageCatalog: __init__(0),load(2),get_package(1),get_packages_by_category(1),list_categories(0)  # Manages the package database.
  fixos/features/installer.py:
    e: FeatureInstaller
    FeatureInstaller: __init__(2),install(1),_install_package(1),_install_repo(1),_install_native(1),_install_flatpak(1),_install_pip(1),_install_cargo(1),_install_npm(1),_run_script(1),get_rollback_commands(1)  # Safely installs packages using native package manager or oth
  fixos/features/profiles.py:
    e: UserProfile
    UserProfile: load(3),list_available(2),resolve_packages(2),to_dict(0)  # A user profile defining what packages/features they want.
  fixos/features/renderer.py:
    e: FeatureRenderer
    FeatureRenderer: render_audit(1),_get_source_info(2),render_package_list(2),render_system_info(1)  # Renders audit results for terminal display.
  fixos/fixes/__init__.py:
  fixos/interactive/__init__.py:
  fixos/interactive/cleanup_planner.py:
    e: main,Priority,CleanupType,CleanupAction,CleanupPlanner
    Priority:
    CleanupType:
    CleanupAction: __post_init__(0)  # Represents a cleanup action
    CleanupPlanner: __init__(0),group_by_category(1),prioritize_actions(1),create_cleanup_plan(1),interactive_selection(1),_dict_to_action(1),_action_to_dict(1),_get_category_for_action(1),_priority_score(1),_rec_safe_high_impact(1),_rec_cache(1),_rec_logs(1),_rec_manual(1),_generate_recommendations(2)  # Interactive cleanup planning and grouping system
    main()
  fixos/llm_shell.py:
    e: _timeout_handler,format_time,execute_command,_llm_call,_handle_user_turn,run_llm_shell
    _timeout_handler(signum;frame)
    format_time(seconds)
    execute_command(cmd)
    _llm_call(client;model;messages)
    _handle_user_turn(session;messages;remaining;verbose)
    run_llm_shell(diagnostics_data;token;model;timeout;verbose;base_url)
  fixos/orchestrator/__init__.py:
  fixos/orchestrator/executor.py:
    e: DangerousCommandError,CommandTimeoutError,ExecutionResult,CommandExecutor
    DangerousCommandError: __init__(2)
    CommandTimeoutError: __init__(2)
    ExecutionResult: success(0),to_context(0)
    CommandExecutor: __init__(3),is_dangerous(1),needs_sudo(1),add_sudo(1),_make_noninteractive(1),check_idempotent(1),execute_sync(4),execute(3)  # Bezpieczny executor komend z:
  fixos/orchestrator/graph.py:
    e: Problem,ProblemGraph
    Problem: is_actionable(0),to_summary(0)
    ProblemGraph: __init__(0),add(1),get(1),next_actionable(0),all_done(0),pending_count(0),summary(0),render_tree(0),_recalculate_order(0)  # DAG problemów systemowych z topological sort do wyznaczania 
  fixos/orchestrator/orchestrator.py:
    e: _SkipAll,FixOrchestrator
    _SkipAll:  # Rzucany gdy user wpisuje 's' – pomija wszystkie komendy bież
    FixOrchestrator: __init__(3),load_from_diagnostics(1),load_from_dict(1),_process_fix_commands(3),_process_rediagnose(2),run_sync(2),run_async(2),_evaluate_and_rediagnose(2),_parse_json(1),_log(2),_session_summary(0),_default_confirm(2),_default_progress(2)  # Orkiestrator napraw systemowych.
  fixos/orchestrator/rollback.py:
    e: RollbackEntry,RollbackSession
    RollbackEntry:  # Single recorded operation with its rollback command.
    RollbackSession: record(6),get_rollback_commands(0),rollback_last(2),_save(0),load(2),list_sessions(2)  # A session of recorded operations that can be rolled back.
  fixos/platform_utils.py:
    e: get_os_info,needs_elevation,elevate_cmd,is_dangerous,run_command,get_package_manager,install_package_cmd,_cmd_exists,setup_signal_timeout,cancel_signal_timeout
    get_os_info()
    needs_elevation(cmd)
    elevate_cmd(cmd)
    is_dangerous(cmd)
    run_command(cmd;timeout;shell)
    get_package_manager()
    install_package_cmd(package)
    _cmd_exists(cmd)
    setup_signal_timeout(seconds;handler)
    cancel_signal_timeout()
  fixos/plugins/__init__.py:
  fixos/plugins/base.py:
    e: Severity,Finding,DiagnosticResult,DiagnosticPlugin
    Severity:  # Severity level for diagnostic findings.
    Finding:  # Single finding from a diagnostic plugin.
    DiagnosticResult: to_dict(0)  # Result of a diagnostic plugin run.
    DiagnosticPlugin: diagnose(0),can_run(0),get_metadata(0)  # Bazowa klasa dla pluginów diagnostycznych fixOS.
  fixos/plugins/builtin/__init__.py:
  fixos/plugins/builtin/audio.py:
    e: Plugin
    Plugin: diagnose(0),_check_alsa(0),_check_pipewire(0),_check_wireplumber(0),_check_sof(0)
  fixos/plugins/builtin/disk.py:
    e: Plugin
    Plugin: diagnose(0),_check_usage(0),_check_inodes(0),_check_readonly(0)
  fixos/plugins/builtin/hardware.py:
    e: Plugin
    Plugin: diagnose(0),_check_gpu(0),_check_battery(0),_check_touchpad(0),_check_camera(0),_check_dmi(0)
  fixos/plugins/builtin/resources.py:
    e: Plugin
    Plugin: diagnose(0),_check_cpu(0),_check_ram(0),_check_top_processes(0),_check_zombies(0),_check_swap(0)
  fixos/plugins/builtin/security.py:
    e: Plugin
    Plugin: diagnose(0),_check_firewall(0),_check_selinux(0),_check_open_ports(0),_check_ssh(0),_check_fail2ban(0)
  fixos/plugins/builtin/thumbnails.py:
    e: Plugin
    Plugin: diagnose(0),_check_cache(0),_check_ffmpegthumbnailer(0),_check_totem(0),_check_gstreamer(0)
  fixos/plugins/registry.py:
    e: PluginRegistry
    PluginRegistry: __init__(0),discover(0),_register_builtins(0),_register_external(0),register(1),list_plugins(1),get_plugin(1),run(2),last_results(0)  # Registry for diagnostic plugins with autodiscovery.
  fixos/profiles/__init__.py:
    e: Profile
    Profile: load(2),list_available(1),to_dict(0)  # Profil diagnostyczny z zestawem modułów i progów.
  fixos/providers/__init__.py:
  fixos/providers/llm.py:
    e: LLMError,LLMClient
    LLMError:  # Błąd komunikacji z LLM.
    LLMClient: __init__(1),_handle_api_error(2),chat(1),chat_stream(1),total_tokens(0),chat_structured(2),_extract_json(1),ping(0)  # Wrapper nad openai.OpenAI kompatybilny z wieloma providerami
  fixos/providers/llm_analyzer.py:
    e: main,LLMAnalysis,LLMAnalyzer
    LLMAnalysis:  # Result of LLM analysis
    LLMAnalyzer: __init__(1),analyze_disk_issues(1),analyze_failed_action(2),analyze_complex_pattern(1),_sanitize_suggestion(1),_create_fallback_analysis(1),enhance_heuristics_with_llm(2)  # Uses LLM to analyze disk issues when heuristics aren't suffi
    main()
  fixos/providers/schemas.py:
    e: RiskLevel,FixSuggestion,LLMDiagnosticResponse,NLPIntent,CommandValidation
    RiskLevel:
    FixSuggestion:  # Pojedyncza sugestia naprawy od LLM.
    LLMDiagnosticResponse:  # Strukturalna odpowiedź LLM na dane diagnostyczne.
    NLPIntent:  # Rozpoznana intencja z polecenia NLP.
    CommandValidation:  # Wynik walidacji komendy przez LLM.
  fixos/system_checks.py:
    e: run_cmd,get_cpu_info,get_memory_info,get_disk_info,get_network_info,get_top_processes,get_fedora_specific,get_full_diagnostics
    run_cmd(cmd;timeout)
    get_cpu_info()
    get_memory_info()
    get_disk_info()
    get_network_info()
    get_top_processes(n)
    get_fedora_specific()
    get_full_diagnostics()
  fixos/utils/__init__.py:
  fixos/utils/anonymizer.py:
    e: _get_sensitive,_apply_regex_replacements,anonymize,display_anonymized_preview,_colorize_md_line,_format_diagnostics_markdown,_render_dict_list_value,_render_dict_long_string,_render_dict_multiline_string,_dict_to_markdown,_format_key_title,AnonymizationReport
    AnonymizationReport: add(2),summary(0)  # Raport anonimizacji – co zostało zmaskowane.
    _get_sensitive()
    _apply_regex_replacements(data_str;report)
    anonymize(data_str)
    display_anonymized_preview(data_str;report;max_lines)
    _colorize_md_line(line)
    _format_diagnostics_markdown(data_str)
    _render_dict_list_value(key;value;prefix)
    _render_dict_long_string(key;value;prefix)
    _render_dict_multiline_string(key;value;prefix)
    _dict_to_markdown(data;indent)
    _format_key_title(key)
  fixos/utils/terminal.py:
    e: colorize,_is_divider_line,_handle_divider_line,_get_severity_style,render_md,print_cmd_block,print_stdout_box,print_stderr_box,print_problem_header,render_tree_colored,_wrap,_C
    _C:  # No-op stubs – kept so existing callers don't break at import
    colorize(line)
    _is_divider_line(stripped)
    _handle_divider_line(stripped)
    _get_severity_style(stripped)
    render_md(text)
    print_cmd_block(cmd;comment;dry_run)
    print_stdout_box(stdout;max_lines)
    print_stderr_box(stderr;max_lines)
    print_problem_header(problem_id;description;severity;status;attempts;max_attempts)
    render_tree_colored(nodes;execution_order)
    _wrap(text;width)
  fixos/utils/timeout.py:
    e: timeout_handler,SessionTimeout
    SessionTimeout:  # Wyjątek rzucany po przekroczeniu limitu czasu sesji.
    timeout_handler(signum;frame)
  fixos/utils/web_search.py:
    e: _http_get,search_fedora_bugzilla,search_ask_fedora,search_arch_wiki,search_github_issues,search_serpapi,search_ddg,search_all,format_results_for_llm,SearchResult
    SearchResult:
    _http_get(url;timeout)
    search_fedora_bugzilla(query;max_results)
    search_ask_fedora(query;max_results)
    search_arch_wiki(query;max_results)
    search_github_issues(query;max_results)
    search_serpapi(query;api_key;max_results)
    search_ddg(query;max_results)
    search_all(query;serpapi_key;max_per_source)
    format_results_for_llm(results)
  fixos/watch.py:
    e: WatchDaemon
    WatchDaemon: __init__(4),run(0),stop(0),_check_for_new_issues(1),_notify(1)  # Daemon wykonujący cykliczną diagnostykę z powiadomieniami.
  scripts/pyqual-calibrate.py:
    e: read_last_metrics_from_db,parse_pyqual_yaml,update_metric,calculate_new_threshold,extract_current_metrics,calibrate,main
    read_last_metrics_from_db(workdir)
    parse_pyqual_yaml(config_path)
    update_metric(content;metric_name;new_value)
    calculate_new_threshold(actual_value;current_threshold;margin_percent;is_upper_limit)
    extract_current_metrics(content)
    calibrate(workdir;margin;dry_run;force;provided_metrics)
    main()
  setup.py:
  test_kwarg.py:
    e: cli
    cli(disc)
  test_timeout_fix.py:
    e: timeout_handler,suspend_timeout,setup_timeout_ref
    timeout_handler(signum;frame)
    suspend_timeout()
    setup_timeout_ref(seconds;handler)
  tests/__init__.py:
  tests/conftest.py:
    e: _env,_has_real_token,real_api_available,test_config,mock_config,mock_llm_client,broken_audio_diagnostics,broken_thumbnails_diagnostics,full_broken_diagnostics,broken_network_diagnostics,broken_dns_diagnostics
    _env(key;default)
    _has_real_token()
    real_api_available()
    test_config()
    mock_config()
    mock_llm_client(mock_config)
    broken_audio_diagnostics()
    broken_thumbnails_diagnostics()
    full_broken_diagnostics(broken_audio_diagnostics;broken_thumbnails_diagnostics)
    broken_network_diagnostics()
    broken_dns_diagnostics()
  tests/e2e/__init__.py:
  tests/e2e/test_anonymization_layers.py:
    e: _assert_no_sensitive,mock_cfg,_make_sensitive_string,TestAnonymizePatterns,TestDiagnosticsAnonymization,TestHITLAnonymizationLayer,TestAutonomousAnonymizationLayer,TestOrchestratorAnonymizationLayer,TestLLMBoundaryNoLeaks
    TestAnonymizePatterns: test_hostname_replaced(0),test_username_replaced(0),test_home_path_replaced(0),test_home_slash_pattern(0),test_ipv4_last_octets_masked(0),test_ipv4_preserves_first_two_octets(0),test_mac_replaced(0),test_sk_token_replaced(0),test_openrouter_token_replaced(0),test_xai_token_replaced(0),test_gemini_token_replaced(0),test_password_replaced(0),test_uuid_replaced(0),test_serial_replaced(0),test_multiple_occurrences(0),test_non_sensitive_unchanged(0),test_empty_string(0),test_dict_input(0),test_localhost_not_masked(0),test_ipv6_not_broken(0),test_report_size_tracking(0)
    TestDiagnosticsAnonymization: _make_diag(0),test_hostname_not_in_anonymized(0),test_username_not_in_anonymized(0),test_home_path_not_in_anonymized(0),test_pactl_info_anonymized(0),test_journal_errors_anonymized(0),test_full_diag_no_leaks(0)
    TestHITLAnonymizationLayer: test_llm_prompt_no_hostname(2),test_llm_prompt_no_username(2),test_user_rejects_send_no_llm_call(1)
    TestAutonomousAnonymizationLayer: test_command_output_anonymized(0),test_exec_output_anonymized_before_llm(2)
    TestOrchestratorAnonymizationLayer: test_diagnostics_anonymized_in_prompt(2),test_stdout_stderr_anonymized_in_evaluate(2)
    TestLLMBoundaryNoLeaks: test_anonymize_before_any_llm_call(0),test_anonymize_idempotent(0),test_anonymize_preserves_technical_info(0),test_nested_sensitive_in_dict(0),test_multiline_journal_log_anonymized(0),test_dmesg_output_anonymized(0),test_env_file_content_anonymized(0),test_sensor_output_not_anonymized(0),test_anonymization_report_summary_format(0)  # Testy granicy LLM – weryfikacja że żadne surowe dane nie tra
    _assert_no_sensitive(text;label)
    mock_cfg()
    _make_sensitive_string()
  tests/e2e/test_audio_broken.py:
    e: TestAudioAnonymization,TestAudioDiagnosticsDetection,TestAudioDiagnosticsMockLLM,TestAudioDiagnosticsReal
    TestAudioAnonymization: test_anonymize_hostname(1),test_anonymize_ipv4(0),test_anonymize_mac(0),test_anonymize_api_token(0),test_anonymize_home_path(0),test_anonymize_uuid(0)  # Testy anonimizacji danych audio.
    TestAudioDiagnosticsDetection: test_detect_missing_sof_firmware(1),test_detect_no_alsa_cards(1),test_detect_pipewire_failed(1),test_detect_lenovo_hardware(1),test_kernel_dmesg_sof_error(1)  # Testy wykrywania problemów audio z danych diagnostycznych.
    TestAudioDiagnosticsMockLLM: test_llm_receives_anonymized_data(2),test_anonymization_report_not_empty(1),test_llm_called_with_sof_context(3),test_llm_rate_limit_retry(2)  # Testy z mock LLM – weryfikacja że dane są poprawnie przesyła
    TestAudioDiagnosticsReal: test_real_llm_analyzes_audio(2)  # Testy z prawdziwym API – uruchamiane tylko gdy token dostępn
  tests/e2e/test_cli.py:
    e: runner,tmp_env,TestWelcomeScreen,TestLlmCommand,TestTokenCommands,TestProvidersCommand,TestConfigCommands
    TestWelcomeScreen: test_welcome_shows_banner(1),test_welcome_shows_commands(1),test_welcome_shows_status_section(1),test_welcome_shows_tip_when_no_key(1)  # Testy ekranu powitalnego (fixos bez argumentów).
    TestLlmCommand: test_llm_shows_all_providers(1),test_llm_shows_urls(1),test_llm_shows_free_paid_badges(1),test_llm_free_filter(1),test_llm_shows_token_set_commands(1),test_llm_shows_env_vars(1),test_llm_marks_active_provider(1),test_llm_shows_12_providers(1)  # Testy komendy fixos llm.
    TestTokenCommands: test_token_set_gemini_auto_detect(2),test_token_set_openai_auto_detect(2),test_token_set_openrouter_auto_detect(2),test_token_set_anthropic_auto_detect(2),test_token_set_groq_auto_detect(2),test_token_set_xai_auto_detect(2),test_token_set_explicit_provider(2),test_token_set_masked_in_output(2),test_token_set_file_permissions(2),test_token_set_replaces_existing(2),test_token_clear(2)  # Testy komend fixos token set/show/clear.
    TestProvidersCommand: test_providers_shows_list(1),test_providers_shows_free_paid(1),test_providers_suggests_llm_command(1)  # Testy komendy fixos providers.
    TestConfigCommands: test_config_show_runs(1),test_config_init_creates_env(2),test_config_set_writes_value(2)  # Testy komend fixos config.
    runner()
    tmp_env(tmp_path)
  tests/e2e/test_executor.py:
    e: ex_live,ex_dry,TestNonInteractiveInjection,TestSudoLogic,TestDangerousCommandBlocking,TestLiveExecution,TestIdempotencyCheck
    TestNonInteractiveInjection: test_apt_get_install_y_injected(1),test_apt_install_y_injected(1),test_dnf_install_y_injected(1),test_dnf_upgrade_y_injected(1),test_apt_get_upgrade_y_injected(1),test_already_y_not_duplicated(1),test_non_pkg_cmd_unchanged(1),test_sudo_apt_get_y_injected(1)  # Testy wstrzykiwania -y do komend pakietów.
    TestSudoLogic: test_systemctl_user_no_sudo(1),test_systemctl_user_start_no_sudo(1),test_systemctl_system_gets_sudo(1),test_dnf_gets_sudo(1),test_echo_no_sudo(1)  # Testy logiki sudo w executor.
    TestDangerousCommandBlocking: test_rm_rf_root_blocked(1),test_mkfs_blocked(1),test_wget_pipe_sh_blocked(1),test_fork_bomb_blocked(1),test_safe_echo_not_blocked(1)  # Testy blokowania niebezpiecznych komend.
    TestLiveExecution: test_echo_executes_correctly(1),test_false_command_returns_nonzero(1),test_uname_returns_output(1),test_timeout_handling(0),test_nonexistent_command_fails_gracefully(1),test_stdout_captured(1),test_stderr_captured_on_error(1)  # Testy faktycznego wykonania bezpiecznych komend.
    TestIdempotencyCheck: test_mkdir_skipped_if_exists(1),test_mkdir_executed_if_not_exists(1)  # Testy sprawdzania idempotentności przed wykonaniem.
    ex_live()
    ex_dry()
  tests/e2e/test_multi_system.py:
    e: TestMultiSystemBasic,TestSystemDetection,TestCliCommands,TestDockerEnvironment,TestSystemServices
    TestMultiSystemBasic: test_fixos_import(0),test_fixos_cli_exists(0),test_config_load(0),test_diagnostics_import(0)  # Podstawowe testy działające na każdym systemie.
    TestSystemDetection: test_os_detection(0),test_distro_detection(0),test_python_version(0)  # Testy detekcji systemu operacyjnego.
    TestCliCommands: fixos_path(0),test_help_command(1),test_scan_help(1),test_config_show(1)  # Testy CLI fixos - wymagają zainstalowanego pakietu.
    TestDockerEnvironment: test_docker_environment_detected(0),test_required_commands_available(0),test_disk_space_available(0)  # Testy specyficzne dla środowiska Docker.
    TestSystemServices: test_systemd_or_init(0),test_dbus_availability(0)  # Testy usług systemowych (tylko w Docker).
  tests/e2e/test_network_broken.py:
    e: broken_network_diagnostics,broken_dns_diagnostics,TestNetworkProblemsDetection,TestNetworkAnonymization,TestNetworkMockLLM,TestNetworkExecutorIntegration,TestNetworkRealLLM
    TestNetworkProblemsDetection: test_detect_networkmanager_failed(1),test_detect_dns_failure(1),test_detect_rfkill_blocked(1),test_detect_no_wifi_device(1),test_detect_network_unreachable(1),test_detect_systemd_resolved_failed(1),test_detect_multiple_failed_services(1)  # Testy wykrywania problemów sieciowych z danych diagnostyczny
    TestNetworkAnonymization: test_ip_in_network_data_masked(0),test_mac_in_network_data_masked(0),test_hostname_in_network_data_masked(0),test_private_ip_range_masked(0)  # Testy anonimizacji danych sieciowych.
    TestNetworkMockLLM: test_llm_suggests_rfkill_unblock(3),test_llm_suggests_dns_fix(3),test_llm_network_commands_no_sudo_for_rfkill(3)  # Testy z mock LLM dla scenariusza broken-network.
    TestNetworkExecutorIntegration: test_systemctl_user_network_no_sudo(0),test_networkmanager_restart_gets_sudo(0),test_ip_command_no_sudo(0),test_rfkill_no_sudo(0),test_firewall_cmd_needs_sudo(0)  # Testy integracji executor + network commands.
    TestNetworkRealLLM: test_real_llm_analyzes_network(2)  # Testy z prawdziwym API – tylko gdy token dostępny.
    broken_network_diagnostics()
    broken_dns_diagnostics()
  tests/e2e/test_thumbnails_broken.py:
    e: TestThumbnailsDetection,TestThumbnailsAnonymization,TestThumbnailsMockLLM,TestWebSearchFallback,TestFullBrokenScenario
    TestThumbnailsDetection: test_detect_missing_ffmpegthumbnailer(1),test_detect_missing_totem_thumbnailer(1),test_detect_empty_thumbnail_cache(1),test_detect_high_fail_count(1),test_detect_missing_thumbnailer_packages(1),test_detect_missing_thumbnailer_configs(1)  # Testy wykrywania problemów z thumbnails.
    TestThumbnailsAnonymization: test_home_path_in_cache_anonymized(1),test_xdg_cache_path_anonymized(0)  # Testy anonimizacji danych thumbnails.
    TestThumbnailsMockLLM: test_llm_suggests_ffmpegthumbnailer(3),test_llm_suggests_cache_clear(3)  # Testy z mock LLM dla scenariusza thumbnails.
    TestWebSearchFallback: test_search_arch_wiki_thumbnails(0),test_search_fedora_bugzilla_audio(0),test_format_results_for_llm(0),test_empty_results_handled(0)  # Testy wyszukiwania zewnętrznego jako fallback.
    TestFullBrokenScenario: test_all_modules_detected(1),test_combined_issues_anonymized(1),test_full_scenario_llm_comprehensive(3),test_real_llm_full_scenario(2)  # Testy pełnego scenariusza (audio + thumbnails + inne problem
  tests/test_fixos.py:
    e: test_placeholder,test_import
    test_placeholder()
    test_import()
  tests/unit/__init__.py:
  tests/unit/test_anonymizer.py:
    e: TestHomePaths,TestAnonymizerOrder,TestAnonymizerEdgeCases
    TestHomePaths: test_pyenv_full_path_anonymized(0),test_deep_nested_home_path(0),test_multiple_home_paths_all_masked(0),test_home_path_with_spaces_in_context(0),test_home_path_in_error_message(0),test_home_path_already_anonymized_not_double_replaced(0),test_non_home_paths_not_affected(0),test_literal_home_dir_replaced_first(0),test_username_replaced_after_paths(0)  # Testy anonimizacji ścieżek /home – fix v2.2.
    TestAnonymizerOrder: test_hostname_replaced_before_username(0),test_home_path_replaced_before_username_word(0),test_report_categories_present(0),test_report_summary_format(0)  # Testy kolejności zastąpień – fix v2.2.
    TestAnonymizerEdgeCases: test_empty_string(0),test_none_converted_to_string(0),test_dict_converted_to_string(0),test_very_long_path(0),test_path_with_special_chars(0),test_api_token_sk_or_masked(0),test_api_token_gemini_masked(0),test_uuid_hardware_masked(0),test_mac_address_masked(0),test_ipv4_partial_octets_preserved(0),test_password_in_env_masked(0)  # Testy przypadków brzegowych.
  tests/unit/test_core.py:
    e: TestConfig,TestAnonymizer,TestWebSearch
    TestConfig: test_default_provider_is_gemini(0),test_model_default_gemini(0),test_invalid_provider_fallback(0),test_validate_missing_key(0),test_validate_ollama_no_key_needed(0),test_agent_mode_from_env(0),test_summary_masks_key(0)
    TestAnonymizer: test_empty_string(0),test_non_string_input(0),test_no_sensitive_data(0),test_ipv6_not_mangled(0),test_multiple_ips_all_masked(0),test_password_in_env_masked(0)
    TestWebSearch: test_format_empty_results(0),test_format_single_result(0),test_http_get_timeout(0)
  tests/unit/test_executor.py:
    e: ex,TestMakeNoninteractive,TestNeedsSudo,TestAddSudo,TestIsDangerous,TestCheckIdempotent,TestExecuteSyncDryRun
    TestMakeNoninteractive: test_apt_get_install_gets_y(1),test_apt_install_gets_y(1),test_dnf_install_gets_y(1),test_yum_install_gets_y(1),test_apt_get_upgrade_gets_y(1),test_dnf_update_gets_y(1),test_already_has_y_not_duplicated(1),test_already_has_yes_not_duplicated(1),test_non_package_cmd_unchanged(1),test_echo_unchanged(1),test_apt_get_without_sudo_gets_y(1),test_package_name_preserved(1),test_dist_upgrade_gets_y(1)  # Testy _make_noninteractive() – fix v2.2.
    TestNeedsSudo: test_systemctl_user_no_sudo(1),test_systemctl_user_start_no_sudo(1),test_systemctl_user_stop_no_sudo(1),test_systemctl_system_needs_sudo(1),test_systemctl_enable_needs_sudo(1),test_dnf_needs_sudo(1),test_apt_get_no_sudo_in_needs_sudo(1),test_already_sudo_no_double(1),test_echo_no_sudo(1),test_modprobe_needs_sudo(1),test_mount_needs_sudo(1)  # Testy needs_sudo() – fix v2.2 (systemctl --user).
    TestAddSudo: test_systemctl_user_no_sudo_added(1),test_dnf_gets_sudo(1),test_already_sudo_unchanged(1)  # Testy add_sudo() – integracja z needs_sudo.
    TestIsDangerous: test_rm_rf_root_blocked(1),test_mkfs_blocked(1),test_fork_bomb_blocked(1),test_wget_pipe_sh_blocked(1),test_curl_pipe_sh_blocked(1),test_safe_dnf_install_ok(1),test_safe_systemctl_ok(1),test_safe_echo_ok(1),test_rm_rf_system_dir_blocked(1),test_chmod_777_root_blocked(1)  # Testy is_dangerous() – walidacja niebezpiecznych komend.
    TestCheckIdempotent: test_dnf_install_has_check(1),test_systemctl_enable_has_check(1),test_systemctl_start_has_check(1),test_mkdir_has_check(1),test_echo_no_check(1),test_apt_get_no_check(1)  # Testy check_idempotent() – sprawdzanie stanu przed wykonanie
    TestExecuteSyncDryRun: test_dry_run_returns_preview(1),test_dangerous_command_raises(1),test_apt_get_gets_y_in_dry_run(1),test_systemctl_user_no_sudo_in_dry_run(1)  # Testy execute_sync() w trybie dry-run.
    ex()
  tests/unit/test_orchestrator.py:
    e: TestProblem,TestProblemGraph,TestCommandExecutor,TestFixOrchestrator
    TestProblem: test_is_actionable_pending(0),test_is_actionable_resolved(0),test_is_actionable_max_attempts(0),test_to_summary_keys(0)
    TestProblemGraph: test_add_and_get(0),test_next_actionable_no_deps(0),test_next_actionable_blocked_by_dep(0),test_next_actionable_dep_resolved(0),test_all_done_when_all_resolved(0),test_all_done_false_when_pending(0),test_pending_count(0),test_render_tree_not_empty(0),test_topological_order_critical_first(0),test_child_linked_to_parent(0)
    TestCommandExecutor: test_is_dangerous_rm_rf_root(0),test_is_dangerous_safe_command(0),test_is_dangerous_dd_disk(0),test_is_dangerous_fork_bomb(0),test_needs_sudo_dnf(0),test_needs_sudo_systemctl(0),test_needs_sudo_already_has_sudo(0),test_needs_sudo_echo(0),test_add_sudo(0),test_dry_run_returns_preview(0),test_execute_sync_safe_command(0),test_execute_sync_raises_on_dangerous(0),test_execution_result_success(0),test_execution_result_failure(0),test_execution_result_not_executed(0),test_to_context_keys(0)
    TestFixOrchestrator: mock_cfg(0),test_load_from_dict(1),test_graph_render_after_load(1),test_run_sync_dry_run_no_confirm(1),test_load_from_diagnostics_mock_llm(2),test_parse_json_clean(1),test_parse_json_with_markdown_fence(1),test_parse_json_invalid_raises(1)
  tests/unit/test_service_cleanup.py:
    e: TestChromeCleanup
    TestChromeCleanup: test_chrome_cleanup_command_targets_scanned_profile(0),test_cleanup_service_reports_freed_space_for_chrome(1)
  tests/unit/test_service_scanner.py:
    e: TestChromeSafetyClassification
    TestChromeSafetyClassification: test_chrome_profile_is_marked_for_review(1),test_chrome_cache_path_is_marked_safe(1)
```

## Call Graph

*174 nodes · 161 edges · 40 modules · CC̄=3.3*

### Hubs (by degree)

| Function | CC | in | out | total |
|----------|----|----|-----|-------|
| `_cmd` *(in fixos.diagnostics.checks._shared)* | 7 | 142 | 3 | **145** |
| `_cleanup_flatpak_detailed` *(in fixos.cli.cleanup_cmd)* | 12 ⚠ | 1 | 111 | **112** |
| `_display_full_system_menu` *(in fixos.cli.cleanup_cmd)* | 12 ⚠ | 1 | 79 | **80** |
| `_display_flatpak_status` *(in fixos.cli.cleanup_cmd)* | 9 | 1 | 65 | **66** |
| `_print_welcome` *(in fixos.cli.main)* | 6 | 1 | 61 | **62** |
| `_handle_home_analysis` *(in fixos.cli.cleanup_cmd)* | 11 ⚠ | 1 | 49 | **50** |
| `diagnose_resources` *(in fixos.diagnostics.checks.resources)* | 13 ⚠ | 0 | 49 | **49** |
| `_handle_snap_management` *(in fixos.cli.cleanup_cmd)* | 18 ⚠ | 1 | 44 | **45** |

```toon markpact:analysis path=project/calls.toon.yaml
# code2llm call graph | /home/tom/github/wronai/fixOS
# nodes: 174 | edges: 161 | modules: 40
# CC̄=3.3

HUBS[20]:
  fixos.diagnostics.checks._shared._cmd
    CC=7  in:142  out:3  total:145
  fixos.cli.cleanup_cmd._cleanup_flatpak_detailed
    CC=12  in:1  out:111  total:112
  fixos.cli.cleanup_cmd._display_full_system_menu
    CC=12  in:1  out:79  total:80
  fixos.cli.cleanup_cmd._display_flatpak_status
    CC=9  in:1  out:65  total:66
  fixos.cli.main._print_welcome
    CC=6  in:1  out:61  total:62
  fixos.cli.cleanup_cmd._handle_home_analysis
    CC=11  in:1  out:49  total:50
  fixos.diagnostics.checks.resources.diagnose_resources
    CC=13  in:0  out:49  total:49
  fixos.cli.cleanup_cmd._handle_snap_management
    CC=18  in:1  out:44  total:45
  fixos.platform_utils.run_command
    CC=5  in:33  out:4  total:37
  fixos.diagnostics.checks.security.diagnose_security
    CC=4  in:0  out:36  total:36
  fixos.llm_shell.run_llm_shell
    CC=8  in:0  out:34  total:34
  fixos.cli.cleanup_cmd._format_bytes
    CC=3  in:33  out:0  total:33
  fixos.cli.cleanup_cmd._cleanup_full_system
    CC=18  in:1  out:30  total:31
  fixos.utils.terminal.render_md
    CC=9  in:0  out:30  total:30
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

MODULES:
  docs.examples.quickstart  [1 funcs]
    run_autonomous_session  CC=1  out:0
  fixos.agent  [1 funcs]
    get_remaining_time  CC=2  out:4
  fixos.agent.autonomous_session  [5 funcs]
    _get_remaining_time  CC=1  out:1
    _handle_exec  CC=4  out:16
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
  fixos.cli.cleanup_cmd  [20 funcs]
    _build_dep_types  CC=4  out:2
    _cleanup_flatpak_detailed  CC=12  out:111
    _cleanup_full_system  CC=18  out:30
    _display_flatpak_status  CC=9  out:65
    _display_full_system_menu  CC=12  out:79
    _display_home_items  CC=7  out:17
    _display_service_group  CC=8  out:15
    _display_unsafe_services  CC=4  out:10
    _filter_by_age  CC=6  out:8
    _filter_by_prefix_category  CC=6  out:12
  fixos.cli.features_cmd  [2 funcs]
    _interactive_profile_select  CC=11  out:22
    features_audit  CC=4  out:18
  fixos.cli.fix_cmd  [2 funcs]
    _collect_diagnostics  CC=7  out:14
    _run_agent_session  CC=2  out:2
  fixos.cli.main  [3 funcs]
    _print_welcome  CC=6  out:61
    cli  CC=3  out:5
    main  CC=1  out:1
  fixos.cli.scan_cmd  [3 funcs]
    _display_disk_fix_mode  CC=6  out:11
    _display_disk_scan_mode  CC=4  out:12
    _run_disk_analysis  CC=8  out:15
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
  fixos.diagnostics.checks.system_core  [3 funcs]
    _collect_os_info  CC=3  out:9
    _collect_platform_details  CC=3  out:14
    diagnose_system  CC=11  out:23
  fixos.diagnostics.checks.thumbnails  [1 funcs]
    diagnose_thumbnails  CC=1  out:21
  fixos.llm_shell  [3 funcs]
    _handle_user_turn  CC=8  out:16
    execute_command  CC=10  out:14
    run_llm_shell  CC=8  out:34
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
  fixos.utils.anonymizer  [8 funcs]
    _apply_regex_replacements  CC=3  out:4
    _dict_to_markdown  CC=9  out:20
    _format_diagnostics_markdown  CC=3  out:5
    _format_key_title  CC=1  out:3
    _get_sensitive  CC=4  out:3
    _render_dict_list_value  CC=6  out:7
    anonymize  CC=8  out:21
    display_anonymized_preview  CC=5  out:18
  fixos.utils.terminal  [7 funcs]
    _get_severity_style  CC=3  out:1
    _is_divider_line  CC=1  out:2
    print_cmd_block  CC=4  out:6
    print_problem_header  CC=3  out:10
    print_stderr_box  CC=2  out:8
    print_stdout_box  CC=2  out:8
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
  project.map.toon  [1 funcs]
    display_anonymized_preview  CC=0  out:0
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
  fixos.config_interactive.interactive_provider_setup → fixos.config_interactive._print_provider_menu
  fixos.config_interactive.interactive_provider_setup → fixos.config_interactive._get_user_choice
  fixos.config_interactive.interactive_provider_setup → fixos.config_interactive._get_api_key
  fixos.config_interactive.interactive_provider_setup → fixos.config_interactive._save_to_env
  fixos.diagnostics.checks.resources.diagnose_resources → fixos.diagnostics.checks._shared._psutil_required
  fixos.diagnostics.checks.system_core._collect_os_info → fixos.diagnostics.checks._shared._cmd
  fixos.diagnostics.checks.system_core._collect_platform_details → fixos.diagnostics.checks._shared._cmd
  fixos.diagnostics.checks.system_core.diagnose_system → fixos.diagnostics.checks.system_core._collect_os_info
  fixos.diagnostics.checks.system_core.diagnose_system → fixos.diagnostics.checks._shared._psutil_required
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
  fixos.agent.autonomous_session.AutonomousSession._initialize_messages → project.map.toon.display_anonymized_preview
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
```

## Test Contracts

*Scenarios as contract signatures — what the system guarantees.*

### Cli (1)

**`CLI Command Tests`**

### Integration (1)

**`Auto-generated from Python Tests`**

## Intent

AI-powered Linux/Windows diagnostics and repair – audio, hardware, system issues
