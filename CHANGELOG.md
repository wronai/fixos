## [2.1.23] - 2026-02-26

### Summary

refactor(goal): CLI interface improvements

### Other

- update fixos/cli.py
- update fixos/interactive/cleanup_planner.py


## [2.1.22] - 2026-02-26

### Summary

refactor(docs): code analysis engine

### Docs

- docs: update README
- docs: update TODO.md

### Other

- update fixos/cli.py
- update fixos/diagnostics/disk_analyzer.py
- update fixos/diagnostics/system_checks.py


## [2.1.21] - 2026-02-26

### Summary

refactor(goal): CLI interface improvements

### Other

- update fixos/cli.py
- update fixos/interactive/cleanup_planner.py
- update fixos/orchestrator/orchestrator.py
- update fixos/utils/terminal.py


## [2.1.20] - 2026-02-26

### Summary

fix(goal): CLI interface improvements

### Test

- update test_kwarg.py

### Other

- update fixos/cli.py
- update img.png


## [2.1.19] - 2026-02-26

### Summary

fix(goal): CLI interface improvements

### Other

- update fixos/cli.py


## [2.1.18] - 2026-02-26

### Summary

refactor(goal): code analysis engine

### Test

- update test_click.py
- update test_click2.py

### Other

- update fixos/diagnostics/disk_analyzer.py
- update fixos/interactive/cleanup_planner.py
- update patch_cli.py
- update patch_cli2.py
- update patch_cli3.py
- update patch_cli4.py
- update patch_docs.py
- update patch_parser.py


## [2.1.17] - 2026-02-26

### Summary

fix(goal): code analysis engine

### Docs

- docs: update README

### Test

- update test_click.py
- update test_click2.py

### Other

- update TICKET
- update fixos/cli.py
- update fixos/diagnostics/disk_analyzer.py
- update fixos/interactive/__init__.py
- update fixos/interactive/cleanup_planner.py
- update fixos/providers/llm_analyzer.py
- update patch_cli.py
- update patch_cli2.py
- update patch_cli3.py
- update patch_cli4.py
- ... and 2 more


## [Unreleased]

### Added

- **feat(disk):** Nowa funkcja `--disc` (`--disk`) dla poleceń `fix` i `scan` do analizy zajętości dysku.
- **feat(interactive):** Kreator czyszczenia dysku (CleanupPlanner) z priorytetami (🔴/🟡/🟢).
- **feat(llm):** Fallback LLM dla błędów podczas czyszczenia dysku.
- **fix(cli):** Naprawa parsera grupowego (NaturalLanguageGroup) w celu poprawnego działania komend.
- **refactor(cli):** Usunięto zduplikowany kod ujednolicając funkcje analizy dysku do wspólnego helpera `_run_disk_analysis`.
- **refactor(ui):** Usunięto ikony Unicode z CLI i sformatowano wyjście `stderr` oraz standardowego logowania na czysty kod Markdown dla poprawy czytelności w oknach terminalowych.

## [2.1.25] - 2026-03-15

### Test
- Update test-results/alpine-build.log
- Update test-results/arch-build.log
- Update test-results/arch-scan-help.log
- Update test-results/arch-unit-tests.log
- Update test-results/arch-version.log
- Update test-results/debian-build.log
- Update test-results/debian-scan-help.log
- Update test-results/debian-unit-tests.log
- Update test-results/debian-version.log
- Update test-results/ubuntu-build.log
- ... and 2 more files

### Other
- Update .env.example
- Update docker/debian/Dockerfile
- Update docker/test-multi-system.sh
- Update docker/ubuntu/Dockerfile
- Update fixos/utils/anonymizer.py

## [2.1.24] - 2026-03-15

### Docs
- Update docker/README.md
- Update docs/CONTRIBUTING.md
- Update docs/README.md
- Update docs/api-changelog.md
- Update docs/api.md
- Update docs/architecture.md
- Update docs/configuration.md
- Update docs/coverage.md
- Update docs/dependency-graph.md
- Update docs/examples/advanced_usage.py
- ... and 6 more files

### Test
- Update test-results/debian-build.log
- Update test-results/debian-scan-help.log
- Update test-results/fedora-build.log
- Update test-results/fedora-scan-help.log
- Update test-results/fedora-unit-tests.log
- Update test-results/fedora-version.log
- Update test-results/ubuntu-build.log
- Update test-results/ubuntu-scan-help.log
- Update test-results/ubuntu-unit-tests.log
- Update test-results/ubuntu-version.log
- ... and 1 more files

### Other
- Update Makefile
- Update docker/alpine/Dockerfile
- Update docker/arch/Dockerfile
- Update docker/debian/Dockerfile
- Update docker/docker-compose.multi-system.yml
- Update docker/fedora/Dockerfile
- Update docker/test-multi-system.sh
- Update docker/ubuntu/Dockerfile
- Update fixos/cli.py
- Update fixos/diagnostics/service_scanner.py
- ... and 17 more files

## [2.1.16] - 2026-02-26

### Summary

feat(build): deep code analysis engine with 2 supporting modules

### Ci

- config: update ci.yml


## [2.1.15] - 2026-02-22

### Summary

fix(goal): CLI interface improvements

### Other

- update fixos/cli.py


## [2.1.14] - 2026-02-22

### Summary

fix(goal): CLI interface improvements

### Other

- update fixos/cli.py


## [2.1.13] - 2026-02-22

### Summary

fix(goal): CLI interface improvements

### Build

- update pyproject.toml

### Other

- update fixos/cli.py


## [2.1.12] - 2026-02-22

### Summary

feat(config): core module improvements

### Build

- update setup.py


## [2.1.11] - 2026-02-22

### Summary

fix(docs): CLI interface improvements

### Docs

- docs: update README
- docs: update TODO.md

### Other

- update fixos/cli.py


## [2.1.10] - 2026-02-22

### Summary

docs(docs): deep code analysis engine with 3 supporting modules

### Docs

- docs: update README
- docs: update TODO.md


## [2.1.9] - 2026-02-18

### Summary

refactor(goal): CLI interface improvements

### Other

- update fixos/agent/hitl.py
- update fixos/cli.py
- update fixos/orchestrator/orchestrator.py
- update fixos/utils/terminal.py
- update requirements.txt


## [2.1.8] - 2026-02-18

### Summary

feat(tests): CLI interface improvements

### Docs

- docs: update README

### Test

- update tests/conftest.py
- update tests/e2e/test_executor.py
- update tests/unit/test_executor.py

### Other

- docker: update docker-compose.yml
- update fixos/agent/hitl.py
- update fixos/cli.py
- update fixos/config.py
- update fixos/diagnostics/system_checks.py
- update fixos/orchestrator/orchestrator.py
- update fixos/utils/anonymizer.py
- update fixos/utils/terminal.py


## [2.1.7] - 2026-02-18

### Summary

fix(tests): CLI interface improvements

### Docs

- docs: update README

### Test

- update tests/e2e/test_cli.py
- update tests/e2e/test_executor.py
- update tests/e2e/test_network_broken.py
- update tests/unit/test_anonymizer.py
- update tests/unit/test_executor.py

### Other

- docker: update Dockerfile


## [2.1.6] - 2026-02-18

### Summary

feat(goal): CLI interface improvements

### Other

- update fixos/agent/hitl.py
- update fixos/cli.py
- update fixos/config.py


## [2.2.0] - 2026-02-18

### Naprawione błędy (Bug Fixes)

- **fix(diagnostics):** `NameError: name '_IS_LINUX' is not defined` w `diagnose_system()` –
  dodano brakujący import `IS_LINUX/IS_WINDOWS/IS_MAC/SYSTEM` z `platform_utils`
- **fix(anonymizer):** ścieżki `/home/user/.pyenv/versions/...` nie były anonimizowane –
  regex `/home/[^\s/\"']+` dopasowywał tylko jeden segment; naprawiono na pełną ścieżkę;
  zmieniono kolejność zastąpień (home path → regex → username)
- **fix(executor):** `apt-get install` bez flagi `-y` powodował interaktywny prompt i abort –
  dodano metodę `_make_noninteractive()` automatycznie wstrzykującą `-y` dla apt/apt-get/dnf/yum
- **fix(executor):** `sudo systemctl --user` powodował błąd DBUS (`$DBUS_SESSION_BUS_ADDRESS not defined`) –
  `needs_sudo()` teraz pomija `systemctl --user` (user-scope nie wymaga sudo)

### Dodane (Added)

- **feat(cli):** `fixos` bez argumentów wyświetla stylizowany ekran powitalny z listą komend,
  aktualnym statusem (provider, API key, .env) i kontekstowymi wskazówkami
- **feat(cli):** nowa komenda `fixos llm` – lista 12 providerów LLM z:
  - opisem, modelem domyślnym, zmienną env
  - klikalnym URL do strony generowania klucza API
  - oznaczeniami FREE/PAID i aktywnym providerem (`◀ aktywny`)
  - gotowymi komendami do skopiowania
  - flagą `--free` filtrującą tylko darmowe providery
- **feat(config):** rozszerzono `PROVIDER_DEFAULTS` z 5 do 12 providerów:
  anthropic, mistral, groq, together, cohere, deepseek, cerebras
- **feat(token):** auto-detekcja providera po prefiksie klucza rozszerzona o `sk-ant-` (Anthropic) i `gsk_` (Groq)
- **feat(hitl):** koloryzowany markdown output odpowiedzi LLM (ANSI):
  - 🔴/🟡/🟢 severity z kolorami
  - `` `inline code` `` → cyan, `**bold**` → biały bold
  - bloki kodu z ramkami box-drawing (`┌─ bash ─┐` / `│` / `└─┘`)
  - stdout/stderr z kolorowymi ramkami i tłem
- **feat(cli):** nowe logo ASCII fixOS zastępuje stare `fixfedora`
- **feat(providers):** `fixos providers` zaktualizowany do nowego formatu z FREE/PAID badge

### Testy (Tests)

- Dodano testy jednostkowe dla nowych funkcji anonymizera (pyenv paths, kolejność zastąpień)
- Dodano testy jednostkowe dla `CommandExecutor._make_noninteractive()` i `needs_sudo()`
- Dodano testy e2e dla scenariusza broken-network
- Dodano testy e2e dla CLI (welcome screen, llm command, token set)
- Dodano testy e2e dla executora (apt-get -y injection, systemctl --user bez sudo)
- Dodano Docker environment `broken-network`

## [2.1.5] - 2026-02-18

### Summary

fix(build): configuration management system

### Docs

- docs: update README

### Test

- update tests/test_fixos.py

### Build

- update setup.py

### Other

- update .gitignore
- update LICENSE
- update MANIFEST.in
- build: update Makefile
- docker: update Dockerfile
- docker: update Dockerfile
- docker: update Dockerfile
- docker: update Dockerfile
- docker: update docker-compose.yml
- update fixos.conf.example
- ... and 6 more


## [2.1.4] - 2026-02-18

### Summary

fix(goal): CLI interface improvements

### Other

- update fixos/cli.py
- update fixos/llm_shell.py


## [2.1.3] - 2026-02-18

### Summary

refactor(docs): CLI interface improvements

### Docs

- docs: update CONTRIBUTING.md
- docs: update INSTALL.md
- docs: update README

### Other

- update LICENSE
- update fixos/agent/autonomous.py
- update fixos/cli.py
- update fixos/diagnostics/system_checks.py
- update fixos/llm_shell.py
- update fixos/system_checks.py
- update fixos/utils/web_search.py


## [2.1.1] - 2026-02-18

### Breaking Changes

- **Package renamed**: `fixfedora` → `fixos`
- **Cross-platform support**: Linux, Windows, macOS

### Added

- **Cross-platform diagnostics** for Linux/Windows/macOS
- **platform_utils.py** module with OS detection, elevation commands, package manager detection
- **Interactive action menu** in HITL mode: `[D]` describe problem, `[1-N]` select fix, `[A]` all, `[S]` skip, `[!cmd]` run command
- **Markdown-formatted output** for command results (stdout/stderr in code blocks)
- **OS-specific diagnostics**: WMI (Windows), system_profiler (macOS), systemd/journal (Linux)

### Changed

- Class `FixFedoraConfig` → `FixOsConfig`
- CLI command `fixfedora` → `fixos`
- All imports updated from `fixfedora` to `fixos`
- Documentation updated for cross-platform support
- LLM exception handling now mock-safe (type-name matching instead of hardcoded classes)

### Removed

- Duplicate `fixfedora/` package directory
- Duplicate `fixfedora.egg-info/`
- Old `.venv/` (keeping `venv/`)

---

# Changelog

Wszystkie istentne zmiany projektu fixos.
Format oparty na [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [2.0.0] – 2025-06

### Dodane
- Moduł diagnostyki **audio** (ALSA, PipeWire, SOF firmware, mikrofon)
- Moduł diagnostyki **thumbnails** (ffmpegthumbnailer, totem-nautilus, cache ~/.cache/thumbnails)
- Moduł diagnostyki **hardware** (DMI, BIOS, GPU, touchpad, ACPI, czujniki)
- Tryb agenta **Human-in-the-Loop** (HITL) – użytkownik zatwierdza każdą akcję
- Tryb agenta **Autonomous** – protokół JSON (`EXEC`/`SEARCH`/`SKIP`/`DONE`), lista zabronionych komend
- Obsługa wielu **providerów LLM**: Google Gemini (domyślny), OpenAI, xAI, OpenRouter, Ollama
- Domyślny model: **gemini-2.5-flash-preview-04-17**
- **Zewnętrzne źródła wiedzy** jako fallback: Bugzilla, fora, Arch Wiki, GitHub Issues, DuckDuckGo, SerpAPI
- Podgląd **zanonimizowanych danych** dla użytkownika przed wysłaniem do LLM + raport co zamaskowano
- Nowe komendy CLI: `token set/show/clear`, `config show/init/set`, `providers`, `test-llm`, `scan`, `fix`
- Konfiguracja przez **plik .env** (python-dotenv)
- **3 środowiska Docker** dla testów: `broken-audio`, `broken-thumbnails`, `broken-full`
- **Testy e2e i unit** z fixtures i mock LLM (pytest + pytest-mock)
- `pyproject.toml` jako standard pakietowania

### Zmienione
- Przepisana architektura na moduły: `agent/`, `diagnostics/`, `providers/`, `utils/`
- Anonimizacja teraz zwraca `tuple(anon_str, AnonymizationReport)` z kategoryzacją
- LLMClient z retry logic (3 próby), obsługą rate limit, streamingiem
- Timeout sesji przez `signal.SIGALRM` z graceful shutdown (Linux/macOS)

### Usunięte
- Monolityczny `diagnose.py` i `llm_shell.py` z v1.0
- Zależność od `tabulate` (zbędna)

---

## [1.0.0] – 2025-05

### Dodane
- Podstawowa diagnostyka systemu (CPU, RAM, dyski, usługi)
- Anonimizacja IP, hostname, ścieżek
- Interaktywny shell LLM z timeoutem 1h
- CLI: `fixos --token sk-...`
- Obsługa OpenAI API
- `setup.py`, `requirements.txt`
