# containers/kali/Dockerfile
FROM kalilinux/kali-rolling:latest

# keep noninteractive and robust shell
ENV DEBIAN_FRONTEND=noninteractive
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Selectable toolset
ARG TOOLSET=network
ARG APT_PROXY

# Optionally use an apt proxy
RUN if [ -n "${APT_PROXY}" ]; then \
      echo "Acquire::http::Proxy \"${APT_PROXY}\";" > /etc/apt/apt.conf.d/02proxy; \
    fi

# --- Core base layer (includes Docker CLI setup) ---
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      ca-certificates locales bash-completion curl wget git jq vim nano tmux less unzip zip gnupg \
      python3 python3-pip python3-venv ruby-full openjdk-11-jre-headless \
      lsof procps psmisc iproute2 iputils-ping dnsutils net-tools netcat-openbsd \
      lsb-release \
    && sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && locale-gen \
    # Add official Docker repository
    && install -m 0755 -d /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc && \
    chmod a+r /etc/apt/keyrings/docker.asc && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian trixie stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null && \
    apt-get update && apt-get install -y docker-ce-cli docker-buildx-plugin docker-compose-plugin \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# --- Network-heavy toolset (in its own layer for caching) ---
RUN apt-get update && \
    if [ "${TOOLSET}" = "network" ]; then \
      apt-get install -y --no-install-recommends \
        nmap masscan arp-scan hping3 nping tcpreplay tcptraceroute iperf3 iperf \
        tcpdump tshark wireshark-cli dumpcap aircrack-ng wireless-tools bettercap \
        mitmproxy ettercap-text-only sipgrep sipvicious gobuster nikto sqlmap \
        hydra ncrack iftop nethogs iptraf-ng bmon tcptrack ethtool arping fping \
        ipcalc sipcalc ndisc6 conntrack nftables iptables iptables-persistent \
        ngrep tcpflow netcat socat ssldump python3-scapy python3-pexpect \
        python3-requests wordlists seclists libcap2-bin || true \
    ; elif [ "${TOOLSET}" = "full" ]; then \
      apt-get install -y --no-install-recommends \
        kali-linux-headless kali-tools-top10 kali-tools-information-gathering \
        kali-tools-vulnerability kali-tools-web kali-tools-passwords \
        kali-tools-post-exploitation kali-tools-wireless wordlists seclists; \
    else \
      echo "Unknown TOOLSET='${TOOLSET}' (use network|full)" && exit 1; \
    fi && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN setcap cap_net_raw,cap_net_admin=eip /usr/bin/dumpcap || true

ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8
WORKDIR /workspace

CMD ["tail", "-f", "/dev/null"]
