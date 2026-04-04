# ==========================================================
# 🛠️  Dev Toolbox Master Makefile — 2026
# ==========================================================

.DEFAULT_GOAL := help

SHELL := /bin/bash
.SHELLFLAGS := -eu -o pipefail -c

.PHONY: help \
        ubuntu debian rocky kali kali-up rocky-up \
        ubuntu-shell debian-shell kali-shell rocky-shell \
        up-dev up-mon up-all down rebuild nuke \
        check ps logs preflight demo \
        tf-shell dotnet-shell py-shell go-shell rust-shell \
        doctor doctor-fix doctor-report doctor-docker-cache \
        triage prune

# ----------------------------------------------------------
# 🧠 Configuration
# ----------------------------------------------------------

UBUNTU_IMAGE := toolbox-ubuntu
DEBIAN_IMAGE := toolbox-debian
ROCKY_IMAGE := toolbox-rocky
KALI_IMAGE := toolbox-kali
KALI_CONTEXT := containers/kali

WORKDIR := /workspace

COMPOSE_PROFILES := --profile dev --profile monitoring --profile ci --profile dotnet --profile terraform
DEV_PROFILES := --profile dev --profile dotnet --profile terraform

COMMON_DOCKER_ARGS := \
	--privileged \
	--pid=host \
	-v /:/host \
	-v /var/run/docker.sock:/var/run/docker.sock \
	-v "$$(pwd)":$(WORKDIR) \
	-w $(WORKDIR)

# ----------------------------------------------------------
# 📖 Help & Discovery
# ----------------------------------------------------------

help:
	@echo ""
	@echo "🌟 Dev Toolbox — SRE / Platform Control Center"
	@echo ""
	@echo "🧪 Validation:"
	@echo "  make preflight     - Verify Docker / Compose prerequisites"
	@echo "  make doctor        - Run vm-doctor"
	@echo "  make doctor-fix    - Auto-remediate issues"
	@echo "  make doctor-report - View latest doctor report"
	@echo ""
	@echo "🐧 Ephemeral Shells (local images):"
	@echo "  make ubuntu        - Ubuntu toolbox (zsh)"
	@echo "  make debian        - Debian toolbox (zsh)"
	@echo "  make rocky         - Rocky Linux 10 toolbox (zsh)"
	@echo "  make kali          - Kali (network-focused) interactive shell"
	@echo ""
	@echo "🕵️ Background / Triage Shells:"
	@echo "  make kali-up       - Start Kali in the background"
	@echo "  make kali-shell    - Attach to running Kali container"
	@echo "  make rocky-up      - Start Rocky in the background"
	@echo "  make rocky-shell   - Attach to running Rocky container"
	@echo "  make triage TARGET=example.com [PORT=443]"
	@echo ""
	@echo "🚀 Long-Running Stacks (docker compose):"
	@echo "  make up-dev        - Dev toolchains"
	@echo "  make up-mon        - Monitoring stack"
	@echo "  make up-all        - Everything"
	@echo "  make down          - Stop all stacks"
	@echo "  make rebuild       - Rebuild from clean state"
	@echo ""
	@echo "🐚 Attach to Running Containers:"
	@echo "  make tf-shell      - Attach to dev-terraform"
	@echo "  make dotnet-shell  - Attach to dev-dotnet"
	@echo "  make py-shell      - Start Python REPL in dev-python"
	@echo "  make go-shell      - Ephemeral Go shell"
	@echo "  make rust-shell    - Ephemeral Rust shell"
	@echo ""
	@echo "🩺 Health & Observability:"
	@echo "  make check         - Container health overview"
	@echo "  make ps            - docker compose ps"
	@echo "  make logs          - Tail compose logs"
	@echo "  make demo          - Run a quick showcase flow"
	@echo ""
	@echo "♻️  Maintenance:"
	@echo "  make prune         - Clean unused Docker resources"
	@echo "  make nuke          - 💥 Destroy all stacks & volumes (confirmation required)"
	@echo ""

# ----------------------------------------------------------
# ✅ Preflight Checks
# ----------------------------------------------------------

preflight:
	@echo "🔎 Running preflight checks..."
	@command -v docker >/dev/null 2>&1 || { echo "❌ docker not installed"; exit 1; }
	@docker info >/dev/null 2>&1 || { echo "❌ docker daemon not running"; exit 1; }
	@docker compose version >/dev/null 2>&1 || { echo "❌ docker compose not available"; exit 1; }
	@echo "✅ preflight checks passed"

demo:
	@echo "🎬 Running Dev Toolbox demo..."
	@$(MAKE) preflight
	@$(MAKE) check
	@$(MAKE) doctor || true

# ----------------------------------------------------------
# 🐧 Ephemeral Toolbox Shells (Compose-free)
# ----------------------------------------------------------

ubuntu:
	@echo "🐧 Ubuntu toolbox (HOST diagnostics enabled)..."
	docker build -t $(UBUNTU_IMAGE) -f containers/ubuntu/Dockerfile containers/ubuntu
	-@docker rm -f dev-ubuntu 2>/dev/null || true
	docker run --rm -it --name dev-ubuntu $(COMMON_DOCKER_ARGS) $(UBUNTU_IMAGE)

debian:
	@echo "🧰 Debian toolbox (HOST diagnostics enabled)..."
	docker build -t $(DEBIAN_IMAGE) -f containers/debian/Dockerfile containers/debian
	-@docker rm -f dev-debian 2>/dev/null || true
	docker run --rm -it --name dev-debian $(COMMON_DOCKER_ARGS) $(DEBIAN_IMAGE)

rocky:
	@echo "🪨 Rocky Linux 10 toolbox (HOST diagnostics enabled)..."
	docker build -t $(ROCKY_IMAGE) -f containers/rocky/Dockerfile containers/rocky
	-@docker rm -f dev-rocky 2>/dev/null || true
	docker run --rm -it --name dev-rocky $(COMMON_DOCKER_ARGS) $(ROCKY_IMAGE)

# ----------------------------------------------------------
# 🕵️ Kali / Rocky Toolbox
# ----------------------------------------------------------

kali:
	@echo "🕵️ Kali toolbox (HOST diagnostics enabled)..."
	docker build -t $(KALI_IMAGE) -f containers/kali/Dockerfile containers/kali
	-@docker rm -f dev-kali 2>/dev/null || true
	docker run --rm -it --name dev-kali $(COMMON_DOCKER_ARGS) $(KALI_IMAGE) /bin/bash

kali-up:
	@echo "🕵️ Starting Kali (background)..."
	docker build -t $(KALI_IMAGE) -f containers/kali/Dockerfile containers/kali
	-@docker rm -f dev-kali 2>/dev/null || true
	docker run -d --name dev-kali $(COMMON_DOCKER_ARGS) $(KALI_IMAGE) tail -f /dev/null

kali-shell:
	@echo "🔐 Entering Kali shell..."
	docker exec -it dev-kali bash || echo "dev-kali not running. Try: make kali or make kali-up"

rocky-up:
	@echo "🪨 Starting Rocky Linux 10 (background)..."
	docker build -t $(ROCKY_IMAGE) -f containers/rocky/Dockerfile containers/rocky
	-@docker rm -f dev-rocky 2>/dev/null || true
	docker run -d --name dev-rocky $(COMMON_DOCKER_ARGS) $(ROCKY_IMAGE) tail -f /dev/null

rocky-shell:
	@echo "🔐 Entering Rocky shell..."
	docker exec -it dev-rocky zsh || echo "dev-rocky not running. Try: make rocky or make rocky-up"

# ----------------------------------------------------------
# 🚀 Docker Compose Stacks
# ----------------------------------------------------------

up-dev:
	@echo "🚀 Starting Development Stacks..."
	docker compose $(DEV_PROFILES) up -d

up-mon:
	@echo "📊 Starting Monitoring Stack..."
	docker compose --profile monitoring up -d

up-all:
	@echo "🌐 Starting full SRE Jungle..."
	docker compose $(COMPOSE_PROFILES) up -d

down:
	@echo "🛑 Stopping all stacks..."
	docker compose $(COMPOSE_PROFILES) down --remove-orphans

rebuild: nuke
	@echo "🔁 Rebuilding toolbox from clean state..."
	docker compose $(COMPOSE_PROFILES) up -d --build

ps:
	@docker compose ps

logs:
	@docker compose logs --tail=100 -f

# ----------------------------------------------------------
# 🧪 Toolchain-Specific Shells
# ----------------------------------------------------------

tf-shell:
	@if ! docker ps --format '{{.Names}}' | grep -q '^dev-terraform$$'; then \
		echo "dev-terraform not running. Try: make up-dev"; \
		exit 1; \
	fi
	docker exec -it dev-terraform sh

dotnet-shell:
	@echo "🟣 .NET shell..."
	docker exec -it dev-dotnet bash

py-shell:
	@echo "🐍 Python REPL..."
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
	@echo "🏥 Checking Compose service health..."
	@docker compose $(COMPOSE_PROFILES) ps
	@echo ""
	@echo "📦 Ephemeral containers:"
	@for c in dev-ubuntu dev-debian dev-rocky dev-kali; do \
		if docker ps --format '{{.Names}}' | grep -q "^$$c$$"; then \
			echo "✅ $$c: RUNNING"; \
		else \
			echo "⚪ $$c: NOT RUNNING"; \
		fi \
	done

# ----------------------------------------------------------
# 🧑‍⚕️ vm-doctor (Diagnostics Toolkit)
# ----------------------------------------------------------

doctor:
	@./bin/vm-doctor

doctor-fix:
	@./bin/vm-doctor --fix

doctor-docker-cache:
	@./bin/vm-doctor --docker-prune

doctor-report:
	@if [ ! -d "./reports" ]; then \
		echo "❌ reports directory does not exist."; \
		echo "Run: make doctor"; \
		exit 0; \
	fi
	@if ! ls ./reports/vm_doctor_* >/dev/null 2>&1; then \
		echo "❌ No vm-doctor reports found."; \
		echo "Run: make doctor"; \
		exit 0; \
	fi
	@ls -1t ./reports/vm_doctor_* | head -1 | xargs -r less

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
	@if ! docker ps --format '{{.Names}}' | grep -q '^dev-kali$$'; then \
		echo "dev-kali not running — starting background container..."; \
		docker build -t $(KALI_IMAGE) -f containers/kali/Dockerfile containers/kali; \
		docker run -d --name dev-kali $(COMMON_DOCKER_ARGS) $(KALI_IMAGE) tail -f /dev/null; \
	else \
		echo "dev-kali already running"; \
	fi
	docker exec -it dev-kali bash -lc "/workspace/bin/net-triage $(TARGET) ${PORT:-443}"

# ----------------------------------------------------------
# ♻️  Maintenance & Cleanup
# ----------------------------------------------------------

prune:
	@echo "🧹 Removing orphaned Docker resources..."
	docker system prune -f

nuke:
	@echo "☢️  This will destroy containers, volumes, and networks."
	@read -r -p "Type YES to continue: " confirm; \
	if [ "$$confirm" = "YES" ]; then \
		echo "💥 Proceeding with destructive cleanup..."; \
		docker compose $(COMPOSE_PROFILES) down --volumes --remove-orphans; \
	else \
		echo "Aborted."; \
	fi
