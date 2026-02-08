FROM debian:13-slim

ENV DEBIAN_FRONTEND=noninteractive

# 1. Install Build Essentials + SRE Rust Deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    pkg-config \
    libssl-dev \
    # Needed for static linking and eBPF/Low-level work
    cmake \
    clang \
    llvm \
    musl-tools \
    # Debugging & Connectivity
    gdb \
    iputils-ping \
    ca-certificates \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace
ENV HOME=/root

# 2. Install Rustup & Common SRE Targets
RUN curl -sSf https://sh.rustup.rs | sh -s -- -y && \
    /root/.cargo/bin/rustup target add x86_64-unknown-linux-musl

ENV PATH="/root/.cargo/bin:${PATH}"

# 3. Install helpful SRE-focused Cargo subcommands
# cargo-binstall downloads binaries instead of compiling from source (much faster)
RUN curl -L --proto '=https' --tlsv1.2 -sSf https://raw.githubusercontent.com/cargo-bins/cargo-binstall/main/install-from-binstall-release.sh | bash

# Install cargo-expand (for debugging) and cargo-audit (for security/SAA mindset)
RUN cargo binstall -y cargo-expand cargo-audit

RUN echo 'source $HOME/.cargo/env' >> /root/.bashrc

ENTRYPOINT ["tail", "-f", "/dev/null"]
