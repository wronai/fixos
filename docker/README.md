# Testy wielosystemowe dla fixos

## Szybki start

```bash
# Testuj wszystkie systemy
./docker/test-multi-system.sh

# Testuj konkretny system
./docker/test-multi-system.sh fedora ubuntu

# Lub przez docker-compose
docker compose -f docker/docker-compose.multi-system.yml run test-fedora
docker compose -f docker/docker-compose.multi-system.yml run test-ubuntu
docker compose -f docker/docker-compose.multi-system.yml run test-debian
docker compose -f docker/docker-compose.multi-system.yml run test-arch
docker compose -f docker/docker-compose.multi-system.yml run test-alpine
```

## Obsługiwane systemy

| System | Dockerfile | Status |
|--------|-----------|--------|
| **Fedora 40** | `docker/fedora/Dockerfile` | ✅ Podstawowy |
| **Ubuntu 24.04** | `docker/ubuntu/Dockerfile` | ✅ Wspierany |
| **Debian 12** | `docker/debian/Dockerfile` | ✅ Wspierany |
| **Arch Linux** | `docker/arch/Dockerfile` | ✅ Wspierany |
| **Alpine 3.19** | `docker/alpine/Dockerfile` | ⚠️ Minimalny |

## Struktura testów

```
docker/
├── fedora/Dockerfile           # Fedora 40
├── ubuntu/Dockerfile           # Ubuntu 24.04 LTS
├── debian/Dockerfile           # Debian 12 (Bookworm)
├── arch/Dockerfile             # Arch Linux (rolling)
├── alpine/Dockerfile           # Alpine 3.19 (minimal)
├── docker-compose.multi-system.yml  # Multi-system orchestration
└── test-multi-system.sh        # Skrypt test runner
```

## Co jest testowane

Każdy system przechodzi następujące testy:

1. **Build** - Czy Docker image buduje się poprawnie
2. **CLI** - Czy `fixos --version` i `fixos scan --help` działają
3. **Unit tests** - Czy testy jednostkowe przechodzą
4. **Importy** - Czy wszystkie moduły się importują

## Wymagania

- Docker 20.10+
- Docker Compose 2.0+
- Bash 4.0+

## Debugowanie

```bash
# Wejdź do kontenera dla debugowania
docker run -it fixos-test:fedora bash

# Zobacz logi
ls -la test-results/
cat test-results/fedora-build.log

# Ręczne uruchomienie testów
docker run fixos-test:ubuntu bash -c "
  cd /app &&
  python -m pytest tests/unit/ -v
"
```

## CI/CD

Testy automatycznie uruchamiają się w GitHub Actions dla każdego PR.

### Lokalne uruchomienie (symulacja CI):

```bash
# Zbuduj wszystkie obrazy
make docker-build-all

# Uruchom wszystkie testy
make docker-test-all
```

## Dodawanie nowego systemu

1. Utwórz `docker/<system>/Dockerfile`
2. Dodaj service do `docker/docker-compose.multi-system.yml`
3. Dodaj system do listy w `docker/test-multi-system.sh`
4. Uruchom testy: `./docker/test-multi-system.sh <system>`

## Znane problemy

### Alpine Linux
- Alpine używa `musl` zamiast `glibc` - niektóre funkcje mogą działać inaczej
- Busybox zamiast GNU coreutils - testowane komendy mogą mieć inne opcje

### Arch Linux
- Rolling release - wersje pakietów zmieniają się codziennie
- Może wymagać aktualizacji Dockerfile co jakiś czas

## Rozszerzenia

Możliwe przyszłe systemy do dodania:
- openSUSE
- Gentoo
- NixOS
- Clear Linux

## Więcej informacji

- [Dockerfile reference](https://docs.docker.com/engine/reference/builder/)
- [Docker Compose](https://docs.docker.com/compose/)
