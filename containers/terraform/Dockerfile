# Using Debian 13 (Trixie) for a modern base
FROM debian:trixie-slim

ENV DEBIAN_FRONTEND=noninteractive

# 1. Install System Basics
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl unzip git ca-certificates jq && \
    rm -rf /var/lib/apt/lists/*

# 2. Install Terraform CLI (Latest 2026 version)
RUN curl -fsSL https://apt.releases.hashicorp.com/gpg | gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com trixie main" | tee /etc/apt/sources.list.d/hashicorp.list && \
    apt-get update && apt-get install -y terraform

# 3. Install TFLint (Deep validation for AWS/Azure/GCP)
RUN curl -s https://raw.githubusercontent.com/terraform-linters/tflint/master/install_linux.sh | bash

# 4. Install tfsec (Security scanning)
RUN curl -s https://raw.githubusercontent.com/aquasecurity/tfsec/master/scripts/install_linux.sh | bash

# 5. Install Infracost (Cloud Cost Estimates)
RUN curl -fsSL https://raw.githubusercontent.com/infracost/infracost/master/scripts/install.sh | sh

# 6. Install TFSwitch (Version management)
RUN curl -L https://raw.githubusercontent.com/warrensbox/terraform-switcher/release/install.sh | bash

WORKDIR /workspace
CMD ["terraform", "--version"]
