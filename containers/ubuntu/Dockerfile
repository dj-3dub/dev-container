# ============================
# Ubuntu Toolbox 
# ============================

FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    # --- Locale & shell ---
    locales \
    bash-completion \
    zsh \
    git \
    curl \
    wget \
    fzf \
    # --- SSH ---
    openssh-client \
    # --- Python (apt) ---
    python3 \
    python3-pip \
    python3-venv \
    # --- Docker CLI ---
    docker.io \
    # --- Monitoring ---
    procps \
    htop \
    btop \
    atop \
    sysstat \
    # --- Networking ---
    iproute2 \
    iputils-ping \
    dnsutils \
    net-tools \
    nmap \
    tcpdump \
    # --- Storage / perf ---
    iotop \
    stress-ng \
    # --- Essentials ---
    vim \
    nano \
    ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Locale
RUN locale-gen en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8

# Oh-My-Zsh (root)
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended

# Zsh plugins
RUN git clone --depth=1 https://github.com/zsh-users/zsh-autosuggestions \
      /root/.oh-my-zsh/custom/plugins/zsh-autosuggestions && \
    git clone --depth=1 https://github.com/zsh-users/zsh-syntax-highlighting \
      /root/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting && \
    git clone --depth=1 https://github.com/zsh-users/zsh-history-substring-search \
      /root/.oh-my-zsh/custom/plugins/zsh-history-substring-search

# Zsh config (identical to Debian)
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

# Aliases
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'

# fzf keybindings (safe for Debian/Ubuntu)
if [ -f /usr/share/doc/fzf/examples/key-bindings.zsh ]; then
  source /usr/share/doc/fzf/examples/key-bindings.zsh
fi
if [ -f /usr/share/doc/fzf/examples/completion.zsh ]; then
  source /usr/share/doc/fzf/examples/completion.zsh
fi
EOF

WORKDIR /workspace
CMD ["zsh", "-l"]
