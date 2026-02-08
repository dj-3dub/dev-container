# Kali Rolling (kept current, good tool coverage)
FROM kalilinux/kali-rolling:latest

ENV DEBIAN_FRONTEND=noninteractive
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# ---- Optional: choose tool "level" at build time ----
# default: broad toolbox (recommended)
# full: heavier (still not "everything", but big)
ARG TOOLSET=default

RUN apt-get update && \
    # --- Base / Shell / QoL ---
    apt-get install -y --no-install-recommends \
      ca-certificates \
      locales \
      bash-completion \
      curl \
      wget \
      git \
      jq \
      vim \
      nano \
      tmux \
      less \
      unzip \
      zip \
      gnupg \
      lsof \
      procps \
      psmisc \
      iproute2 \
      iputils-ping \
      dnsutils \
      net-tools \
      tcpdump \
      tshark \
      nmap \
      traceroute \
      mtr-tiny \
      netcat-openbsd \
      socat \
      openssl \
      whois \
      ethtool \
      arping \
      fping \
      iperf3 \
      iftop \
      nethogs \
      tcpflow \
      ngrep \
      ipcalc \
      sipcalc \
      ndisc6 \
      conntrack \
      nftables \
      iptables \
      && \
    \
    # --- Kali Tool Metapackages (broad, but not "everything") ---
    if [[ "${TOOLSET}" == "default" ]]; then \
      apt-get install -y --no-install-recommends \
        kali-tools-top10 \
        kali-tools-information-gathering \
        kali-tools-vulnerability \
        kali-tools-web \
        kali-tools-passwords \
        kali-tools-post-exploitation \
        kali-tools-wireless \
        wordlists \
        seclists \
        ; \
    elif [[ "${TOOLSET}" == "full" ]]; then \
      apt-get install -y --no-install-recommends \
        kali-linux-headless \
        kali-tools-top10 \
        kali-tools-information-gathering \
        kali-tools-vulnerability \
        kali-tools-web \
        kali-tools-passwords \
        kali-tools-post-exploitation \
        kali-tools-wireless \
        kali-tools-sniffing-spoofing \
        kali-tools-forensics \
        kali-tools-reverse-engineering \
        wordlists \
        seclists \
        ; \
    else \
      echo "Unknown TOOLSET='${TOOLSET}' (use default|full)" && exit 1; \
    fi && \
    \
    # --- Locale ---
    sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen && \
    \
    # --- Cleanup ---
    apt-get clean && rm -rf /var/lib/apt/lists/*

ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

WORKDIR /workspace
CMD ["tail", "-f", "/dev/null"]
