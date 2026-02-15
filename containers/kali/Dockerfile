# containers/kali/Dockerfile
FROM kalilinux/kali-rolling:latest

# keep noninteractive and robust shell
ENV DEBIAN_FRONTEND=noninteractive
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Selectable toolset:
# - network (default): curated, network-heavy toolset for diagnosis & packet analysis
# - full: fallback to heavy Kali metapackages (slow)
ARG TOOLSET=network
ARG APT_PROXY

# Optionally use an apt proxy if provided at build time
RUN if [ -n "${APT_PROXY}" ]; then \
      echo "Acquire::http::Proxy \"${APT_PROXY}\";" > /etc/apt/apt.conf.d/02proxy; \
    fi

# --- Core base layer (kept small, cached separately) ---
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      ca-certificates locales bash-completion curl wget git jq vim nano tmux less unzip zip gnupg \
      python3 python3-pip python3-venv ruby-full openjdk-11-jre-headless \
      lsof procps psmisc iproute2 iputils-ping dnsutils net-tools netcat-openbsd \
    && sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && locale-gen \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# --- Network-heavy toolset (in its own layer for caching) ---
RUN apt-get update && \
    if [ "${TOOLSET}" = "network" ]; then \
      apt-get install -y --no-install-recommends \
        # reconnaissance & scanning
        nmap masscan arp-scan \
        # active probing / crafted packets
        hping3 nping tcpreplay tcptraceroute \
        # throughput & latency
        iperf3 iperf \
        # sniffing / packet capture & analysis
        tcpdump tshark wireshark-cli dumpcap \
        # live analysis / wifi & wireless
        aircrack-ng wireless-tools || true \
        # traffic replay / manipulation
        bettercap mitmproxy ettercap-text-only || true \
        # DNS / SIP / VoIP / telecom
        sipgrep sipvicious || true \
        # web enumeration (handy for network-facing web apps)
        gobuster nikto sqlmap || true \
        # brute / auth / misc helpers
        hydra ncrack || true \
        # traffic helpers and viewers
        iftop nethogs iptraf-ng bmon tcptrack || true \
        # low-level utilities
        ethtool arping fping ipcalc sipcalc ndisc6 conntrack nftables iptables iptables-persistent || true \
        # protocol-specific utilities
        ngrep tcpflow netcat socat ssldump || true \
        # helpful libraries & helpers
        python3-scapy python3-pexpect python3-requests || true \
        # wordlists & corpora
        wordlists seclists \
        # capabilities utility so dumpcap can be given capture rights
        libcap2-bin \
      ; \
    elif [ "${TOOLSET}" = "full" ]; then \
      apt-get install -y --no-install-recommends \
        kali-linux-headless kali-tools-top10 kali-tools-information-gathering kali-tools-vulnerability \
        kali-tools-web kali-tools-passwords kali-tools-post-exploitation kali-tools-wireless \
        wordlists seclists; \
    else \
      echo "Unknown TOOLSET='${TOOLSET}' (use network|full)" && exit 1; \
    fi && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Give dumpcap the necessary capabilities (so tshark/dumpcap can capture non-root)
# If dumpcap path differs, this will harmlessly fail (we fallback to running as root).
RUN setcap cap_net_raw,cap_net_admin=eip /usr/bin/dumpcap || true

ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8
WORKDIR /workspace

# Keep container alive by default so we can docker exec into it
# For interactive dev runs you will override with /bin/bash
CMD ["tail", "-f", "/dev/null"]
