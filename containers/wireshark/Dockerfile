# Using Debian 13 (Trixie) for the latest 2026 protocol support
FROM debian:trixie-slim

ENV DEBIAN_FRONTEND=noninteractive

# 1. Install Analysis Suite
RUN apt-get update && apt-get install -y --no-install-recommends \
    tshark \
    termshark \
    tcpdump \
    ngrep \
    tcpick \
    # Basic utilities for the SRE toolbox
    iproute2 \
    curl \
    git \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# 2. Configure TShark permissions
# This allows the 'tshark' user to capture without being root (Security best practice)
RUN groupadd -r wireshark && \
    usermod -aG wireshark root && \
    chgrp wireshark /usr/bin/dumpcap && \
    chmod 750 /usr/bin/dumpcap && \
    setcap cap_net_raw,cap_net_admin=eip /usr/bin/dumpcap

WORKDIR /captures

# Default to TShark version check
CMD ["tshark", "--version"]
