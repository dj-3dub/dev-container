FROM mcr.microsoft.com/dotnet/sdk:10.0-bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV PATH="${PATH}:/root/.dotnet/tools"

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    procps \
    fzf \
    wget \
    ca-certificates \
    bash-completion \
    unzip \
    && wget https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64 -O /usr/bin/yq \
    && chmod +x /usr/bin/yq \
    && dotnet tool install --global dotnet-trace \
    && dotnet tool install --global dotnet-counters \
    && dotnet tool install --global dotnet-dump \
    && dotnet tool install --global dotnet-monitor \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

CMD ["/bin/bash"]
