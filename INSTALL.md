# Instalacja fixos

## Wymagania systemowe

- **Linux** (Fedora 38+, Ubuntu 22.04+, Arch) / **Windows** 10/11 / **macOS** 12+
- Python 3.10+
- Dostęp do internetu (do API LLM)
- Klucz API jednego z providerów (patrz niżej)

---

## 1. Zależności systemowe

### Linux (Fedora/RHEL)
```bash
sudo dnf install python3-pip python3-psutil python3-pyyaml
```

### Linux (Ubuntu/Debian)
```bash
sudo apt install python3-pip python3-psutil python3-yaml
```

### Windows
```powershell
# PowerShell (jako Administrator)
winget install Python.Python.3.10
pip install psutil pyyaml
```

### macOS
```bash
brew install python@3.10
pip3 install psutil pyyaml
```

---

## 2. Instalacja paczki

### Ze źródeł (zalecane podczas development)

```bash
git clone https://github.com/wronai/fixos.git
cd fixos
pip install -e ".[dev]"    # z zależnościami testowymi
# lub
pip install -e .           # tylko runtime
```

### Z archiwum ZIP

```bash
unzip fixos-2.1.1.zip
cd fixos-2.1.1
pip install -e ".[dev]"
```

### Z PyPI (po publikacji)

```bash
pip install fixos
```

---

## 3. Konfiguracja tokena API

### Google Gemini (domyślny, darmowy tier)

1. Wejdź na https://aistudio.google.com/apikey
2. Kliknij "Create API Key"
3. Skopiuj klucz (`AIzaSy...`)

```bash
fixos token set AIzaSyTWOJKLUCZGEMINI
```

### OpenAI

```bash
fixos token set sk-TWOJKLUCZ --provider openai
```

### xAI (Grok)

```bash
fixos token set xai-TWOJKLUCZ --provider xai
```

### Ollama (lokalny, bez klucza)

```bash
# Zainstaluj Ollama: https://ollama.ai
ollama pull llama3.2
fixos config set LLM_PROVIDER ollama
```

---

## 4. Inicjalizacja pliku konfiguracyjnego

```bash
fixos config init      # tworzy .env z szablonu
nano .env              # opcjonalne dostosowanie
```

Lub ręcznie:

```bash
cp .env.example .env
chmod 600 .env         # ogranicz dostęp!
# Edytuj .env i wstaw klucz API
```

---

## 5. Weryfikacja

```bash
fixos test-llm         # test połączenia z LLM
fixos config show      # pokaż konfigurację
fixos scan             # testowa diagnostyka (bez LLM)
```

---

## 6. Pierwsze uruchomienie

```bash
fixos fix              # pełna diagnostyka + sesja naprawcza
```

---

## Rozwiązywanie problemów instalacji

**`ModuleNotFoundError: No module named 'openai'`**
```bash
pip install openai>=1.35.0
```

**`ModuleNotFoundError: No module named 'psutil'`**
```bash
# Linux
sudo dnf install python3-psutil   # Fedora
sudo apt install python3-psutil   # Ubuntu
# lub
pip install psutil

# Windows/macOS
pip install psutil
```

**`fixos: command not found`**
```bash
# Linux/macOS - dodaj ~/.local/bin do PATH
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Windows - dodaj do PATH w System Properties
```

**`Permission denied` przy wykonaniu komend systemowych**
```bash
# Linux/macOS - fixos automatycznie dodaje sudo dla komend systemowych
sudo -v

# Windows - uruchom PowerShell jako Administrator
```
