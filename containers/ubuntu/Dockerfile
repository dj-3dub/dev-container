# ============================
# Ubuntu Toolbox 
# ============================

FROM ubuntu:26.04
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies and Docker
RUN apt-get update && apt-get install -y --no-install-recommends \
    # --- Essentials & Apt setup ---
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    # --- Locale & shell ---
    locales \
    bash-completion \
    zsh \
    git \
    wget \
    fzf \
    # --- SSH ---
    openssh-client \
    # --- Python ---
    python3 \
    python3-pip \
    python3-venv \
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
    # --- Editors ---
    vim \
    nano \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Add Docker's official GPG key and repository for latest CLI tools
RUN install -m 0755 -d /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc && \
    chmod a+r /etc/apt/keyrings/docker.asc && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null && \
    apt-get update && apt-get install -y docker-ce-cli docker-buildx-plugin docker-compose-plugin && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

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

if [ -f /usr/share/doc/fzf/examples/key-bindings.zsh ]; then
  source /usr/share/doc/fzf/examples/key-bindings.zsh
fi
if [ -f /usr/share/doc/fzf/examples/completion.zsh ]; then
  source /usr/share/doc/fzf/examples/completion.zsh
fi
EOF

WORKDIR /workspace
CMD ["zsh", "-l"]
