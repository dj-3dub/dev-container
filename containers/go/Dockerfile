# 1. Using the current stable version for 2026
FROM golang:1.25-bookworm AS dev

ENV DEBIAN_FRONTEND=noninteractive

# Install System Dependencies for CGO and SRE tooling
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl git gcc libc6-dev ca-certificates \
    # Clean up
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 2. Go 1.25 Specific Optimizations for SREs
# Go 1.25 now respects cgroup CPU limits automatically for GOMAXPROCS.
# We set this to ensure our automation doesn't "fight" with the kernel.
ENV GOEXPERIMENT=greenteagc,jsonv2

# 3. Install SRE/Platform Engineering Tools
# Delve for debugging hung processes in your RHEL lab
RUN go install github.com/go-delve/delve/cmd/dlv@latest

# golangci-lint for code quality
RUN curl -sSfL https://raw.githubusercontent.com/golangci/golangci-lint/master/install.sh | sh -s -- -b $(go env GOPATH)/bin v1.61.0

WORKDIR /workspace

# Copy dependency files
COPY go.mod go.sum* ./
RUN go mod download

# Default to bash for your toolbox
CMD ["/bin/bash"]
