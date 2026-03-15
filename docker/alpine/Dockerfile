FROM alpine:3.19

# Podstawowe narzędzia systemowe (busybox + python)
RUN apk add --no-cache \
    python3 \
    py3-pip \
    py3-psutil \
    procps \
    util-linux-misc \
    alsa-utils \
    pipewire \
    wireplumber \
    findutils \
    lsof \
    dbus \
    sudo \
    bash \
    curl

# Zainstaluj fixos
WORKDIR /app
COPY . /app
RUN pip3 install -e ".[dev]" --quiet --break-system-packages

# Ustaw env testowy
ENV FIXOS_TEST_MODE=1
ENV LLM_PROVIDER=gemini

CMD ["/bin/bash"]
