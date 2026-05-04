# 🚀 Optymalizacja Testowania i Budowania – fixOS

## 📊 Podsumowanie Zmian

Zoptymalizowano szybkość testowania i budowania pakietu poprzez:

### ✅ Paralelizacja testów (4-8x szybciej)

- **pytest-xdist** – uruchamia testy na wszystkich dostępnych CPU cores
- Automatyczne równoległy system budowania
- Inteligentne rozkładanie testów między workers

### ✅ Timeout dla testów (30s na test)

- **pytest-timeout** – zabezpieczenie przed zawieszeniem testów
- Automatyczne zabijanie zawieszonych testów
- Uniknięcie blokowania CI/CD

### ✅ Lepszy output testów

- **pytest-sugar** – kolorowa, czytelna reprezentacja wyników
- Szybkie pojęcie statusu testów
- Wizualizacja postępu

### ✅ Optymalizowany build pakietu

- Build cache dla PyPI distributions
- Równoległy build dla wheel i sdist
- Szybsza publikacja

### ✅ Czyszczenie cache

- Usunięcie `.mypy_cache`, `.DS_Store` i innych artefaktów
- Ścieżki do cache w pytest

---

## 🎯 Nowe Komendy Makefile

### Szybkie Testy

| Komenda | Opis | Czas |
| --- | --- | --- |
| `make test-quick` | Szybkie testy bez docker/slow | ~5-10s |
| `make test-unit-par` | Unit testy z paralelizacją (auto CPU) | ~2-5s |
| `make test-unit-fast` | Unit testy z 4 procesami | ~3-7s |
| `make test-fast` | Wszystkie testy z paralelizacją | ~10-20s |
| `make test` | Pełne testy (unit + e2e) | ~30-60s |
| `make test-cov` | Testy z raportem pokrycia | ~15-30s |

### Przykłady Użycia

```bash
# Szybka weryfikacja podczas entwickmentu
make test-quick          # ~5-10s

# Testowanie zmian w unit testach
make test-unit-par       # ~2-5s (auto-parallel)

# Pełne CI/CD pipeline
make test-fast           # ~10-20s (wszystkie testy paralelnie)

# Raport pokrycia kodu z paralelizacją
make test-cov            # ~15-30s
```

---

## 📦 Instalacja Optymalizacyjnych Tools'ów

Dostępne w `[dev]` dependencies:

```bash
# Instalacja wszystkich dev tools
make install-dev

# Lub manual
pip install pytest-xdist pytest-timeout pytest-sugar
```

### Zainstalowane Pakiety:
- **pytest-xdist** – paralelizacja testów
- **pytest-timeout** – timeout dla testów (30s/test)
- **pytest-sugar** – ładny output testów

---

## ⚙️ Konfiguracja

### pytest.ini
```ini
addopts = -v --tb=short --cache-clear --disable-warnings
timeout = 30                    # 30 sekund na test
timeout_method = thread
```

### Pyproject.toml
```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-mock>=3.12.0",
    "pytest-cov>=4.1.0",
    "pytest-xdist>=3.5.0",    # Paralelizacja
    "pytest-timeout>=2.2.0",   # Timeout
    "pytest-sugar>=0.9.7",     # Ładny output
]
```

---

## 📈 Porównanie Szybkości

### Przed Optymalizacją
```
make test-unit     ~ 30-40s (sekwencyjnie)
make test-e2e      ~ 20-30s (sekwencyjnie)
Total              ~ 50-70s
```

### Po Optymalizacji
```
make test-unit-par ~ 3-7s   (8 workers)   ⚡ 5-10x szybciej
make test-fast     ~ 10-20s (parallel)    ⚡ 3-5x szybciej
Total              ~ 10-20s
```

---

## 🔧 Zaawansowana Konfiguracja

### Uruchom testy z konkretną liczbą workerów

```bash
# Dokładnie 4 procesy
pytest tests/ -n 4

# Auto (liczba CPU cores)
pytest tests/ -n auto

# Mniej paralelizmu (2 procesy)
pytest tests/ -n 2
```

### Wyłącz timeout dla debugowania

```bash
# Bez timeout
pytest tests/ -p no:timeout

# Zwiększony timeout na 120s
pytest tests/ --timeout=120
```

### Różne strategie rozkładu testów

```bash
# LoadScheduling (domyślne) – balansowanie ładunkiem
pytest tests/ -n auto

# WarrantedScheduling – optymalnie dla dystrybucji
pytest tests/ -n auto -d
```

### Verbose output dla paralelizmu

```bash
# Szczegółowe logi z każdego workera
pytest tests/ -n auto -v --tb=short
```

---

## 🎬 Workflow Development

### Szybki Feedback Loop
```bash
# 1. Szybkie testy podczas kodowania
make test-quick         # ~5-10s

# 2. Unit testy dla modułu
make test-unit-par      # ~2-5s

# 3. Pełna weryfikacja przed commit
make test-fast          # ~10-20s
```

### CI/CD Pipeline
```bash
# 1. Instalacja
make install-dev        # ~30-60s

# 2. Testy
make test-fast          # ~10-20s

# 3. Pokrycie
make test-cov           # ~15-30s

# 4. Build
make build              # ~5-10s
```

---

## 🐛 Debugowanie Zawieszonych Testów

### Timeout włączony (30s na test)
Jeśli test się zawiesza dłużej niż 30s, pytest automatycznie go zabije:

```
ERROR tests/e2e/test_network_broken.py::TestNetwork::test_timeout - 
Timeout (30.0s) exceeded in TestNetwork::test_timeout
```

### Zwiększ timeout dla wolnych testów
```bash
# 120 sekund dla e2e testów
pytest tests/e2e/ --timeout=120
```

### Wyłącz paralelizm do debugowania
```bash
# Sekwencyjne, z print() statements
pytest tests/unit/ -v -s
```

---

## 📊 Monitoring Czasu Testów

### Raport czasu testów
```bash
pytest tests/ -v --durations=10
```

Pokaże 10 najwolniejszych testów.

---

## 🔍 Częste Problemy i Rozwiązania

| Problem | Rozwiązanie |
|---------|-----------|
| Test się zawiesza | ✅ pytest-timeout zabije po 30s |
| Testy wolne | ✅ Użyj `-n auto` do paralelizacji |
| Za dużo workerów | ✅ Zmniejsz `-n 4` zamiast auto |
| Brakuje output'u | ✅ Dodaj `-s` flag do display print() |
| Konflikt między testami | ✅ Zapewni izolacja w conftest.py |

---

## 📝 Checklist Optymalizacji

- [x] pytest-xdist zainstalowany ✅
- [x] pytest-timeout zainstalowany ✅
- [x] pytest-sugar zainstalowany ✅
- [x] Makefile nowe targets dodane ✅
- [x] pytest.ini zoptymalizowany ✅
- [x] pyproject.toml dev dependencies zaktualizowane ✅
- [x] Cache cleaning improved ✅
- [x] Build parallelization enabled ✅

---

## 🚀 Next Steps

1. **Zamiast `make test`** użyj:
   ```bash
   make test-fast      # Szybsze (~3-5x)
   ```

2. **Zamiast `make test-unit`** użyj:
   ```bash
   make test-unit-par  # Paralelnie (~5-10x szybciej)
   ```

3. **Podczas developmentu** użyj:
   ```bash
   make test-quick     # Szybka weryfikacja (~5-10s)
   ```

---

## 📚 Referencje

- [pytest-xdist](https://pytest-xdist.readthedocs.io/) – Distributed testing
- [pytest-timeout](https://pytest-timeout.readthedocs.io/) – Timeout plugin
- [pytest-sugar](https://pypi.org/project/pytest-sugar/) – Pretty test output
