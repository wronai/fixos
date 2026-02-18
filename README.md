# fixfedora 🔧🤖

**AI-powered diagnostyka i naprawa systemu Fedora Linux z anonimizacją danych**

```
  __  _      ___        __       _
 / _|(_)_ __/ __| ___  / _| ___ | |_  ___  _ _ __ _
|  _|| | \ \ (__/ -_) |  _|/ -_)|  _|/ _ \| '_/ _` |
|_|  |_|_/_/\_,_\___| |_|  \___| \__|\/\__/|_| \__,_|
```

## Co robi fixfedora?

1. **Zbiera metryki systemowe** – CPU, RAM, dyski, sieć, procesy, `dnf`, `journalctl`, `systemctl`
2. **Anonimizuje wrażliwe dane** – maskuje IP, ścieżki `/home/<user>`, hostname, tokeny API
3. **Wysyła dane do LLM** – w sposób jawny, bez ukrytego przetwarzania
4. **Interaktywny shell** – rozmowa z AI o problemach i decyzjach naprawczych (max 1h)
5. **Bezpieczne wykonanie komend** – każda operacja wymaga potwierdzenia `Y/n`

---

## Instalacja

### Wymagania systemowe (Fedora)

```bash
sudo dnf install python3-psutil python3-pyyaml python3-requests
```

### Instalacja paczki

```bash
# Ze źródeł (development)
git clone https://github.com/wronai/fixfedora.git
cd fixfedora
pip install -e .

# Lub przez pip (po publikacji na PyPI)
pip install fixfedora
```

---

## Przykładowe użycie

### 1. Podstawowe – pełna diagnostyka + LLM

```bash
fixfedora --token sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

**Przykładowa sesja:**

```
  __  _      ___        __       _
 / _|(_)_ __/ __| ___  / _| ___ | |_  ___  _ _ __ _
...

🔍 Zbieranie diagnostyki systemu Fedora...
  → Fedora (dnf/systemd/journal)...
✅ Diagnostyka zebrana i zanonimizowana.

⏰ Uruchamianie sesji LLM (model: gpt-4o-mini, timeout: 3600s)...
  Tip: wpisz '!<komenda>' aby wykonać komendę (np. !dnf check-update)
  Tip: wpisz 'q' aby zakończyć sesję

════════════════════════════════════════════════════════════
  🤖 fixfedora LLM Shell  |  Model: gpt-4o-mini
  ⏰ Sesja: max 01:00:00  |  Wpisz 'q' aby wyjść
════════════════════════════════════════════════════════════

────────────────────────────────────────────────────────────
🔍 DIAGNOZA: Wykryto 3 problemy wymagające uwagi

Wykryte problemy:
1. 🔴 15 pakietów do aktualizacji (dnf check-update)
   → Komenda: `sudo dnf upgrade -y`
2. 🟡 Usługa bluetooth.service failed (systemctl --failed)
   → Komenda: `sudo systemctl restart bluetooth`
3. 🟡 70% użycia dysku /var (psutil)
   → Komenda: `sudo dnf clean all && sudo journalctl --vacuum-size=500M`

Co naprawiamy? (numer/all/skip/q)
────────────────────────────────────────────────────────────
  ⏰ Pozostały czas: 00:59:47

fixfedora [00:59:47] ❯ 1

🧠 LLM analizuje... 
────────────────────────────────────────────────────────────
Wykonuję aktualizację systemu. To bezpieczna operacja, jednak zalecam
wcześniejsze wykonanie snapshotu jeśli używasz LVM/Btrfs.

Komenda: `sudo dnf upgrade -y`
────────────────────────────────────────────────────────────

fixfedora [00:59:31] ❯ !sudo dnf upgrade -y

  [exec] sudo dnf upgrade -y
  Potwierdź wykonanie (Y/n): Y
  ✅ Sukces
```

---

### 2. Tylko diagnostyka – zapis do pliku JSON

```bash
fixfedora --diagnose-only --output /tmp/fedora-report.json
# Token nie jest wymagany w trybie --diagnose-only
```

### 3. Z alternatywnym API – xAI Grok

```bash
fixfedora \
  --token xai-TWOJ_KLUCZ \
  --base-url https://api.x.ai/v1 \
  --model grok-beta
```

### 4. Sesja 30-minutowa z verbose

```bash
fixfedora --token sk-... --timeout 1800 --verbose
```

### 5. Z plikiem konfiguracyjnym

```bash
# Utwórz plik konfiguracyjny
cp fixfedora.conf.example ~/.fixfedora.conf
nano ~/.fixfedora.conf          # Wstaw swój klucz API
chmod 600 ~/.fixfedora.conf     # Ogranicz uprawnienia

# Uruchom bez jawnego tokena
fixfedora
```

---

## Bezpieczeństwo

### Co jest anonimizowane?

| Dane wrażliwe | Zamiennik |
|:--|:--|
| Adresy IP (`192.168.1.100`) | `192.168.XXX.XXX` |
| Ścieżki użytkownika (`/home/jan`) | `/home/[USER]` |
| Aktualny hostname | `[HOSTNAME]` |
| Nazwa użytkownika | `[USER]` |
| Tokeny API (`sk-abc123...`) | `sk-[REDACTED]` |
| Hasła w zmiennych (`PASSWORD=xyz`) | `PASSWORD=[REDACTED]` |

### Co NIE jest robione

- ❌ Dane nie są trwale zapisywane (brak logów po sesji)
- ❌ Skrypt nie zbiera haseł ani zawartości plików domowych
- ❌ Brak automatycznego wykonywania komend bez potwierdzenia

---

## Struktura projektu

```
fixfedora/
├── fixfedora/
│   ├── __init__.py          # Eksporty publiczne paczki
│   ├── cli.py               # Punkt wejścia CLI (Click)
│   ├── llm_shell.py         # Interaktywny shell LLM (timeout 1h)
│   └── utils/
│       ├── __init__.py
│       ├── anonymizer.py    # Anonimizacja wrażliwych danych
│       └── system_checks.py # Zbieranie metryk Fedora
├── setup.py                 # Konfiguracja paczki PyPI
├── requirements.txt         # Zależności Python
├── fixfedora.conf.example   # Przykładowy plik konfiguracyjny
└── README.md
```

---

## Zależności

| Biblioteka | Wersja | Zastosowanie |
|:--|:--|:--|
| `openai` | ≥1.35.0 | Klient API LLM (OpenAI, xAI, Ollama) |
| `prompt_toolkit` | ≥3.0.43 | Interaktywny shell z historią i kolorami |
| `psutil` | ≥5.9.0 | Metryki CPU, RAM, dyski, sieć, procesy |
| `pyyaml` | ≥6.0 | Parsowanie konfiguracji YAML |
| `click` | ≥8.1.0 | Profesjonalne CLI z helpem i opcjami |
| `tabulate` | ≥0.9.0 | Formatowanie tabel w terminalu |

---

## Komendy wewnątrz sesji

| Wpisz | Akcja |
|:--|:--|
| `1`, `2`, `3`... | Napraw problem o danym numerze |
| `all` | Napraw wszystkie wykryte problemy |
| `skip` | Pomiń aktualny krok |
| `!<komenda>` | Wykonaj komendę systemową (z potwierdzeniem) |
| `q` / `quit` | Zakończ sesję |

---

## Licencja

MIT License – używaj swobodnie, modyfikuj, dystrybuuj.

## License

Apache License 2.0 - see [LICENSE](LICENSE) for details.

## Author

Created by **Tom Sapletta** - [tom@sapletta.com](mailto:tom@sapletta.com)
