# fixOS TODO & Roadmap

**Wersja projektu**: 2.1.9  
**Ostatnia aktualizacja**: 2026-02-22

---

## 🎯 Roadmap (Planowane funkcje)

### v2.3 – Heurystyki bez LLM (NADCHODZĄCE)
- [ ] `fixos quickfix` – natychmiastowe naprawy bez API (baza 30+ znanych bugów)
- [ ] Dopasowanie heurystyczne diagnostyki do znanych wzorców
- [ ] Działa offline, zero tokenów

### v2.4 – Raporty i historia
- [ ] `fixos report` – eksport sesji do HTML/PDF/Markdown
- [ ] `fixos history` – historia napraw z wynikami
- [ ] Porównanie stanu przed/po naprawie

### v2.5 – Integracje
- [ ] `fixos watch` – monitoring w tle, powiadomienia przy problemach
- [ ] Webhook do Slack/Discord przy wykryciu błędów krytycznych
- [ ] Integracja z Prometheus/Grafana (metryki diagnostyczne)

### v3.0 – Multi-agent
- [ ] Równoległe agenty dla różnych modułów (audio, sieć, dysk)
- [ ] Koordynator z priorytetyzacją problemów
- [ ] Uczenie się z historii napraw (fine-tuning lokalnych modeli)

---

## ✅ Aktualne zadania (TODO)

### Dokumentacja
- [x] Przenieść roadmap z README do TODO.md
- [x] Dodać sekcję "Jak używać" do README
- [ ] Zaktualizować przykłady użycia CLI
- [ ] Dodać FAQ dla nowych użytkowników

### Rozwój funkcji
- [ ] Implementacja `fixos quickfix` (v2.3)
- [ ] Implementacja `fixos report` (v2.4)
- [ ] Implementacja `fixos watch` (v2.5)

### Testy
- [ ] Testy dla nowych komend CLI
- [ ] Testy integracyjne dla webhooków

### DevOps
- [ ] GitHub Actions workflow
- [ ] Automatyczny release na PyPI

### Nowe funkcje (Docker)
- [ ] Komenda `fixos docker stop` - zatrzymaj wszystkie kontenery
- [ ] Komenda `fixos docker rm` - usuń wszystkie kontenery
- [ ] Komenda `fixos docker ps` - lista kontenerów

### Nowe funkcje (Natural Language)
- [x] Komenda `fixos ask "polecenie"` - wykonaj polecenie w języku naturalnym
- [x] Przykład: `fixos ask "wylacz wszystkie kontenery docker"` → wykonuje docker stop
- [x] Przykład: `fixos ask "zlap bledy w systemie"` → wykonuje fixos scan
- [x] Mapowanie słów kluczowych na komendy systemowe
- [ ] Parser LLM do rozumienia bardziej złożonych poleceń

---

## 🚀 Szybki start (Quick Start)

```bash
# 1. Instalacja
pip install -e ".[dev]"

# 2. Konfiguracja
fixos config init                    # Utwórz .env
fixos token set YOUR_API_KEY         # Ustaw klucz API

# 3. Użycie
fixos                                # Ekran powitalny
fixos scan                           # Diagnostyka systemu
fixos fix                            # Napraw z AI (HITL)
fixos fix --mode autonomous          # Napraw automatycznie
```

---

## 📋 Komendy CLI

| Komenda | Opis |
|:--|:--|
| `fixos` | Ekran powitalny |
| `fixos fix` | Diagnoza + naprawa AI (HITL) |
| `fixos scan` | Diagnostyka systemu |
| `fixos orchestrate` | Orkiestracja z grafem DAG |
| `fixos llm` | Lista providerów LLM |
| `fixos token set KEY` | Ustaw klucz API |
| `fixos config show` | Pokaż konfigurację |
| `fixos test-llm` | Testuj połączenie LLM |

---

## 🔧 Przydatne flagi

```bash
# Tryb autonomiczny (bez pytania)
fixos fix --mode autonomous --max-fixes 5

# Tylko konkretne moduły
fixos fix --modules audio,network

# Timeout 30 minut
fixos fix --timeout 1800

# Dry-run (podgląd)
fixos orchestrate --dry-run

# Tylko darmowe providery
fixos llm --free
```

---

## 📞 Support

- GitHub: https://github.com/wronai/fixos
- Email: tom@sapletta.com

---

*Ten plik jest generowany automatycznie. Zmiany wprowadzaj ręcznie w sekcjach TODO.*
