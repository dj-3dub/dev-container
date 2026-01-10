# Using Ubuntu 24.04 LTS (Noble Numbat)
FROM ubuntu:24.04

# Prevent interactive prompts during build
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

# Ubuntu-specific locale generation
RUN locale-gen en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

WORKDIR /workspace
# Default to btop for a quick "Dashboard" view
CMD ["btop"]
