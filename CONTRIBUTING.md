# Wkład do projektu fixos

## Zgłaszanie błędów

Otwórz issue na GitHub z:
- Systemem operacyjnym (`cat /etc/os-release` lub wersja Windows/macOS)
- Modelem sprzętu (dla problemów audio/hardware)
- Zanonimizowanym outputem `fixos scan --output report.json`
- Treścią błędu

## Dodawanie modułów diagnostycznych

Nowe moduły dodaj w `fixos/diagnostics/system_checks.py`:

```python
def diagnose_moj_modul() -> dict:
    result = {}
    if _IS_LINUX:
        result["linux_check"] = _cmd("linux-command")
    elif _IS_WINDOWS:
        result["windows_check"] = _cmd("powershell -Command '...'")
    elif _IS_MAC:
        result["mac_check"] = _cmd("macos-command")
    return result

# Zarejestruj w DIAGNOSTIC_MODULES:
DIAGNOSTIC_MODULES["moj_modul"] = ("🔧 Opis modułu", diagnose_moj_modul)
```

## Cross-platform guidelines

- Używaj `_IS_LINUX`, `_IS_WINDOWS`, `_IS_MAC` do warunkowego wykonywania komend
- Używaj `platform_utils.py` dla komend cross-platform
- Testuj zmiany na wszystkich wspieranych systemach (lub użyj CI)

## Uruchamianie testów

```bash
make install-dev
make test           # unit + e2e mock
make test-real      # wymaga tokena w .env
```

## Styl kodu

- Python 3.10+, type hints gdzie możliwe
- `black` do formatowania, `ruff` do lintingu
- Docstringi po polsku (projekt skierowany do polskich użytkowników)
- Cross-platform: Linux, Windows, macOS
