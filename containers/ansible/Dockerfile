# Using Ubuntu 24.04 (Noble Numbat)
FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

# 1. Install System Dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    python3-setuptools \
    ssh \
    git \
    curl \
    vim \
    sshpass \
    # Required for Molecule + Docker testing
    docker.io \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 2. Setup Python Virtual Environment for Ansible (SRE Best Practice)
ENV VIRTUAL_ENV=/opt/ansible-venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# 3. Install Ansible + SRE Tooling via PIP
# Installing through pip gives you access to 'ansible-lint' and 'molecule'
RUN pip install --no-cache-dir \
    ansible \
    ansible-lint \
    molecule \
    molecule-plugins[docker] \
    # Required for AWS Modules
    boto3 \
    botocore

# 4. Install Cloud Collections for AWS SAA Lab Work
RUN ansible-galaxy collection install amazon.aws community.aws community.general

WORKDIR /workspace

# Start by showing versions for sanity check
CMD ["bash", "-c", "ansible --version && ansible-lint --version && molecule --version && tail -f /dev/null"]

