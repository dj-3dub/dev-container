# 1. Use .NET 10 SDK (LTS) - Current as of Jan 2026
FROM mcr.microsoft.com/dotnet/sdk:10.0-bookworm-slim AS build

# Prevent interactive prompts during apt install
ENV DEBIAN_FRONTEND=noninteractive

# 2. Install "Platform Glue" and System Dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    procps \
    fzf \
    # yq is essential for Platform Engineers to manage YAML (K8s/AWS)
    wget && \
    wget https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64 -O /usr/bin/yq && \
    chmod +x /usr/bin/yq && \
    # Clean up
    apt-get clean && rm -rf /var/lib/apt/lists/*

# 3. Install .NET Diagnostic Tools (The SRE Power Suite)
# These allow you to debug running processes on RHEL VMs or AWS Nodes
RUN dotnet tool install --global dotnet-trace && \
    dotnet tool install --global dotnet-counters && \
    dotnet tool install --global dotnet-dump && \
    dotnet tool install --global dotnet-monitor

# Ensure tools are in the PATH
ENV PATH="${PATH}:/root/.dotnet/tools"

WORKDIR /app

# 4. Optional: Pre-prime the NuGet cache for faster builds
# COPY *.sln .
# RUN dotnet restore

# Default to bash for an interactive troubleshooting session
CMD ["/bin/bash"]
