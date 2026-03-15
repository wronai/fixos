FROM archlinux:base

# Podstawowe narzędzia systemowe
RUN pacman -Syu --noconfirm && pacman -S --noconfirm \
    python \
    python-pip \
    python-psutil \
    systemd \
    procps-ng \
    util-linux \
    alsa-utils \
    pipewire \
    wireplumber \
    findutils \
    lsof \
    dbus \
    sudo \
    curl \
    base-devel \
    && pacman -Sc --noconfirm

# Zainstaluj fixos
WORKDIR /app
COPY . /app
RUN pip3 install -e ".[dev]" --quiet --break-system-packages

# Ustaw env testowy
ENV FIXOS_TEST_MODE=1
ENV LLM_PROVIDER=gemini

CMD ["/bin/bash"]
