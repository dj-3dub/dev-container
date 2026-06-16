# ============================
# Rocky Linux 10 Toolbox (Stable)
# ============================

FROM rockylinux/rockylinux:10-ubi-init

ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

# --- Base + repos ---
RUN dnf -y install \
    glibc-langpack-en \
    ca-certificates \
    dnf-plugins-core \
    && dnf config-manager --set-enabled crb \
    && dnf -y install epel-release \
    # Add official Docker repository
    && dnf config-manager --add-repo https://download.docker.com/linux/rhel/docker-ce.repo \
    && dnf -y upgrade

# --- Core tools & Docker ---
RUN dnf -y install \
    bash-completion \
    zsh \
    git \
    curl \
    wget \
    tmux \
    fzf \
    ripgrep \
    fd-find \
    jq \
    yq \
    tree \
    ncdu \
    openssh-clients \
    python3 \
    python3-pip \
    procps-ng \
    htop \
    iotop \
    sysstat \
    perf \
    psmisc \
    dstat \
    nmap-ncat \
    iperf3 \
    ethtool \
    smartmontools \
    hdparm \
    parted \
    lvm2 \
    bat \
    bpftrace \
    podman \
    buildah \
    skopeo \
    # Docker CLI tools
    docker-ce-cli \
    docker-buildx-plugin \
    docker-compose-plugin \
    iproute \
    iputils \
    bind-utils \
    net-tools \
    nmap \
    tcpdump \
    socat \
    mtr \
    traceroute \
    vim-enhanced \
    nano \
    less \
    which \
    findutils \
    util-linux \
    hostname \
    file \
    lsof \
    strace \
    tar \
    gzip \
    unzip \
    rsync \
    rpm \
    && dnf clean all \
    && rm -rf /var/cache/dnf

# Oh-My-Zsh
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended

# Plugins
RUN git clone --depth=1 https://github.com/zsh-users/zsh-autosuggestions \
      /root/.oh-my-zsh/custom/plugins/zsh-autosuggestions && \
    git clone --depth=1 https://github.com/zsh-users/zsh-syntax-highlighting \
      /root/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting && \
    git clone --depth=1 https://github.com/zsh-users/zsh-history-substring-search \
      /root/.oh-my-zsh/custom/plugins/zsh-history-substring-search

# Zsh config
RUN cat > /root/.zshrc <<'EOF'
export ZSH="$HOME/.oh-my-zsh"
ZSH_THEME="robbyrussell"

plugins=(
  git
  docker
  zsh-autosuggestions
  zsh-history-substring-search
  zsh-syntax-highlighting
)

source "$ZSH/oh-my-zsh.sh"

alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias cls='clear'
EOF

WORKDIR /workspace
CMD ["zsh", "-l"]
