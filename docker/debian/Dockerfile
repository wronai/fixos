FROM debian:12-slim

# Podstawowe narzędzia systemowe
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-psutil \
    python3-venv \
    systemd \
    procps \
    util-linux \
    alsa-utils \
    pipewire \
    wireplumber \
    findutils \
    lsof \
    dbus \
    udev \
    sudo \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Zainstaluj fixos w virtual environment
WORKDIR /app
COPY . /app
RUN python3 -m venv /app/venv && \
    /app/venv/bin/pip install -e ".[dev]" --quiet && \
    ln -sf /app/venv/bin/fixos /usr/local/bin/fixos && \
    ln -sf /app/venv/bin/python /usr/local/bin/python

# Ustaw env testowy
ENV FIXOS_TEST_MODE=1
ENV LLM_PROVIDER=gemini
ENV PATH="/app/venv/bin:$PATH"

CMD ["/bin/bash"]
