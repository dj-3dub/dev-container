FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

# Basic tools + Python + Ansible
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    ssh \
    git \
    curl \
    vim \
    ansible \
    && rm -rf /var/lib/apt/lists/*

# Helpful: show Ansible version at container start (for sanity)
CMD ["bash", "-lc", "ansible --version && tail -f /dev/null"]
