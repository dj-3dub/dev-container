FROM debian:13-slim

ENV DEBIAN_FRONTEND=noninteractive

# Base tools, build deps, and ping
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    pkg-config \
    libssl-dev \
    iputils-ping \
    ca-certificates \
    git \
    && rm -rf /var/lib/apt/lists/*

# Work in /workspace as root
WORKDIR /workspace
ENV HOME=/root

# Install Rust toolchain via rustup (stable)
RUN curl -sSf https://sh.rustup.rs | sh -s -- -y

# Make sure Rust is always on PATH and env is sourced in shells
ENV PATH="/root/.cargo/bin:${PATH}"
RUN echo 'source $HOME/.cargo/env' >> /root/.bashrc

# Keep container alive for interactive dev
ENTRYPOINT ["tail", "-f", "/dev/null"]
