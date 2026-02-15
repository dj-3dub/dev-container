# ==========================================================
# 🛠️  Dev Toolbox Master Makefile — 2026
# ==========================================================

.PHONY: help \
        ubuntu debian kali build-kali-full build-kali-proxy \
        ubuntu-shell debian-shell kali-shell \
        up-dev up-mon up-all down rebuild nuke \
        check ps logs \
        tf-shell dotnet-shell py-shell go-shell rust-shell \
        doctor doctor-fix doctor-report doctor-docker-cache \
        prune

# ----------------------------------------------------------
# 🧠 Configuration
# ----------------------------------------------------------

UBUNTU_IMAGE := toolbox-ubuntu
DEBIAN_IMAGE := toolbox-debian
KALI_IMAGE := toolbox-kali
KALI_CONTEXT := containers/kali

WORKDIR := /workspace

# ----------------------------------------------------------
# 📖 Help & Discovery
# ----------------------------------------------------------

help:
	@echo ""
	@echo "🌟 Dev Toolbox — SRE / Platform Control Center"
	@echo ""
	@echo "🐧 Ephemeral Shells (local images):"
	@echo "  make ubuntu        - Ubuntu toolbox (zsh)"
	@echo "  make debian        - Debian toolbox (zsh)"
	@echo "  make kali          - Kali (network-focused) interactive shell"
	@echo ""
	@echo "🚀 Long-Running Stacks (docker compose):"
	@echo "  make up-dev        - Dev toolchains"
	@echo "  make up-mon        - Monitoring stack"
	@echo "  make up-all        - Everything"
	@echo "  make down          - Stop all stacks"
	@echo ""
	@echo "🐚 Attach to Running Containers:"
	@echo "  make ubuntu-shell  - Attach to dev-ubuntu"
	@echo "  make debian-shell  - Attach to dev-debian"
	@echo "  make kali-shell    - Attach to dev-kali"
	@echo "  make tf-shell      - Attach to dev-terraform"
	@echo "  make dotnet-shell  - Attach to dev-dotnet"
	@echo ""
	@echo "🩺 Diagnostics & Doctors:"
	@echo "  make check         - Container health overview"
	@echo "  make doctor        - Run vm-doctor"
	@echo "  make doctor-fix    - Auto-remediate issues"
	@echo "  make doctor-report - View latest report"
	@echo ""
	@echo "♻️  Maintenance:"
	@echo "  make prune         - Clean unused Docker resources"
	@echo "  make nuke          - 💥 Destroy all stacks & volumes"
	@echo ""

# ----------------------------------------------------------
# 🐧 Ephemeral Toolbox Shells (Compose-free)
# ----------------------------------------------------------
ubuntu:
	@echo "🐧 Ubuntu toolbox (HOST diagnostics enabled)..."
	docker build -t $(UBUNTU_IMAGE) -f containers/ubuntu/Dockerfile containers/ubuntu
	docker run --rm -it --name dev-ubuntu \
		--privileged \
		--pid=host \
		-v /:/host \
		-v /var/run/docker.sock:/var/run/docker.sock \
		-v "$$(pwd)":$(WORKDIR) -w $(WORKDIR) \
		$(UBUNTU_IMAGE)

debian:
	@echo "🧰 Debian toolbox (HOST diagnostics enabled)..."
	docker build -t $(DEBIAN_IMAGE) -f containers/debian/Dockerfile containers/debian
	docker run --rm -it --name dev-debian \
		--privileged \
		--pid=host \
		-v /:/host \
		-v /var/run/docker.sock:/var/run/docker.sock \
		-v "$$(pwd)":$(WORKDIR) -w $(WORKDIR) \
		$(DEBIAN_IMAGE)

# ----------------------------------------------------------
# 🕵️ Kali Toolbox
# ----------------------------------------------------------
kali:
	@echo "🕵️ Kali toolbox (HOST diagnostics enabled)..."
	docker build -t $(KALI_IMAGE) -f containers/kali/Dockerfile containers/kali
	-@docker rm -f dev-kali 2>/dev/null || true
	docker run --rm -it --name dev-kali \
		--privileged \
		--pid=host \
		-v /:/host \
		-v /var/run/docker.sock:/var/run/docker.sock \
		-v "$$(pwd)":$(WORKDIR) -w $(WORKDIR) \
		$(KALI_IMAGE) /bin/bash

# start Kali in the background (persistent toolbox)
kali-up:
	@echo "🕵️ Starting Kali (background)..."
	docker build -t $(KALI_IMAGE) -f containers/kali/Dockerfile containers/kali
	docker run -d --name dev-kali \
		--privileged \
		--pid=host \
		-v /:/host \
		-v /var/run/docker.sock:/var/run/docker.sock \
		-v "$$(pwd)":$(WORKDIR) -w $(WORKDIR) \
		$(KALI_IMAGE) tail -f /dev/null

# attach to a running Kali container
kali-shell:
	@echo "🔐 Entering Kali shell..."
	docker exec -it dev-kali bash || echo "dev-kali not running. Try: make kali or make kali-up"
# ----------------------------------------------------------
# 🚀 Docker Compose Stacks
# ----------------------------------------------------------

up-dev:
	@echo "🚀 Starting Development Stacks..."
	docker compose --profile dev --profile dotnet --profile terraform up -d

up-mon:
	@echo "📊 Starting Monitoring Stack..."
	docker compose --profile monitoring up -d

up-all:
	@echo "🌐 Starting full SRE Jungle..."
	docker compose --profile dev --profile monitoring --profile ci --profile dotnet --profile terraform up -d

down:
	docker compose --profile dev --profile monitoring --profile ci --profile dotnet --profile terraform stop

rebuild: nuke
	docker compose --profile dev --profile monitoring up -d --build

# ----------------------------------------------------------
# 🧪 Toolchain-Specific Shells
# ----------------------------------------------------------

tf-shell:
	@echo "🏗️  Terraform workspace..."
	docker exec -it dev-terraform sh

dotnet-shell:
	docker exec -it dev-dotnet bash

py-shell:
	docker exec -it dev-python python3

go-shell:
	@echo "🐹 Go shell (ephemeral)..."
	docker compose --profile dev run --rm --entrypoint bash go

rust-shell:
	@echo "🦀 Rust shell (ephemeral)..."
	docker compose --profile dev run --rm --entrypoint bash rust

# ----------------------------------------------------------
# 🩺 Health, Diagnostics & Observability
# ----------------------------------------------------------

check:
	@echo "🏥 Checking Jungle Health..."
	@echo "--------------------------------"
	@for c in arcane dev-debian dev-ubuntu dev-kali dev-python dev-go dev-dotnet dev-rust dev-terraform dev-aws dev-powershell dev-ansible dev-wireshark monitoring-prometheus monitoring-grafana monitoring-node-exporter monitoring-cadvisor; do \
		if docker ps --format '{{.Names}}' | grep -q "$$c"; then \
			echo "✅ $$c: RUNNING"; \
		else \
			echo "❌ $$c: NOT RUNNING"; \
		fi \
	done
	@echo "--------------------------------"
	@docker stats --no-stream --format "table {{.Name}}\t{{.MemUsage}}\t{{.MemPerc}}\t{{.CPUPerc}}"

# ----------------------------------------------------------
# 🧑‍⚕️ vm-doctor (Diagnostics Toolkit)
# ----------------------------------------------------------

doctor:
	@./bin/vm-doctor

doctor-fix:
	@./bin/vm-doctor -fix

doctor-docker-cache:
	@./bin/vm-doctor -docker-cache-prune

doctor-report:
	@ls -1t $$HOME/vm-doctor-reports/vm_doctor_*.txt | head -1 | xargs -r less
# ----------------------------------------------------------
# 🔍 Triage — run bin/net-triage inside dev-kali (auto-starts Kali if needed)
# Usage:
#   make triage TARGET=example.com
#   make triage TARGET=example.com PORT=8443
# ----------------------------------------------------------
triage:
	@if [ -z "$(TARGET)" ]; then \
		echo "Usage: make triage TARGET=example.com [PORT=443]"; \
		exit 1; \
	fi
	@echo "🚑 Running triage for $(TARGET):${PORT:-443}"
	# start background dev-kali if not running
	@if ! docker ps --format '{{.Names}}' | grep -q '^dev-kali$$'; then \
		echo "dev-kali not running — starting background container..."; \
		docker build -t $(KALI_IMAGE) -f containers/kali/Dockerfile containers/kali; \
		docker run -d --name dev-kali --privileged --pid=host -v /:/host -v /var/run/docker.sock:/var/run/docker.sock -v "$$(pwd)":$(WORKDIR) -w $(WORKDIR) $(KALI_IMAGE) tail -f /dev/null; \
	else \
		echo "dev-kali already running"; \
	fi
	# run the triage script inside Kali
	docker exec -it dev-kali bash -lc "/workspace/bin/net-triage $(TARGET) ${PORT:-443}"
# ----------------------------------------------------------
# ♻️  Maintenance & Cleanup
# ----------------------------------------------------------

prune:
	@echo "🧹 Removing orphaned Docker resources..."
	docker system prune -f

nuke:
	@echo "☢️  NUKING ALL DATA (containers, volumes, networks)..."
	docker compose --profile dev --profile monitoring --profile ci --profile dotnet --profile terraform down --volumes --remove-orphans
