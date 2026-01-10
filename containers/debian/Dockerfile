# Using Debian 13 (Trixie) Slim
FROM debian:trixie-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    # --- 0. The UTF-8 & Shell Fix ---
    locales \
    bash-completion \
    # --- 1. Docker CLI (To manage the host from the container) ---
    docker.io \
    # --- 2. Monitoring & Analysis ---
    htop \
    btop \
    atop \
    procps \
    psmisc \
    strace \
    lsof \
    sysstat \
    # --- 3. Networking ---
    iproute2 \
    iputils-ping \
    dnsutils \
    net-tools \
    curl \
    wget \
    nmap \
    tcpdump \
    # --- 4. Storage & Performance ---
    iotop \
    stress-ng \
    # --- 5. Essentials ---
    vim \
    nano \
    ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Configure Locales
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen

ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

WORKDIR /workspace
CMD ["btop"]
