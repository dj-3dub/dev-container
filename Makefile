# ==========================================
# 🛠️  Dev Toolbox Master Makefile - 2026
# ==========================================

.PHONY: help up-dev up-mon up-all down ps nuke check \
        debian-shell ubuntu-shell dotnet-shell tf-shell \
        py-shell go-shell arcane-logs prune

# -------------------------
# 📖 Help & Discovery
# -------------------------
help:
	@echo "🌟 Dev Toolbox - SRE Control Center"
	@echo ""
	@echo "🚀 Launchers:"
	@echo "  make up-dev       - Start core Dev tools (Arcane, Python, Go, etc.)"
	@echo "  make up-mon       - Start Monitoring (Prom/Grafana/cAdvisor)"
	@echo "  make up-all       - Start everything (Dev + Mon + CI)"
	@echo ""
	@echo "🐚 Shell Access:"
	@echo "  make debian-shell - Primary Troubleshooter (btop/nmap)"
	@echo "  make tf-shell     - Terraform CLI Workspace"
	@echo "  make dotnet-shell - .NET 10 environment"
	@echo ""
	@echo "🩺 Maintenance:"
	@echo "  make check        - Health & Memory audit for ALL containers"
	@echo "  make prune        - 🧹 Clean orphaned resources"

# -------------------------
# 🩺 Health & Verification
# -------------------------

check:
	@echo "🏥 Checking Jungle Health..."
	@echo "--------------------------------"
	@for container in arcane dev-debian dev-ubuntu dev-python dev-go dev-dotnet dev-rust dev-terraform dev-aws dev-powershell dev-ansible dev-wireshark monitoring-prometheus monitoring-grafana monitoring-node-exporter monitoring-cadvisor; do \
		if docker ps --format '{{.Names}}' | grep -q "$$container"; then \
			echo "✅ $$container: RUNNING"; \
		else \
			echo "❌ $$container: NOT RUNNING"; \
		fi \
	done
	@echo "--------------------------------"
	@echo "📊 Resource Overview:"
	@docker stats --no-stream --format "table {{.Name}}\t{{.MemUsage}}\t{{.MemPerc}}\t{{.CPUPerc}}"

# -------------------------
# 🛰️  Deployment Commands
# -------------------------

up-dev:
	@echo "🚀 Starting Development Stacks..."
	docker compose --profile dev --profile dotnet --profile terraform up -d

up-mon:
	@echo "📊 Starting Monitoring Stack..."
	docker compose --profile monitoring up -d

up-all:
	@echo "🌐 Starting full SRE Jungle..."
	docker compose --profile dev --profile monitoring --profile ci --profile dotnet --profile terraform up -d

# -------------------------
# 🐚 Tool Shells
# -------------------------

debian-shell:
	docker exec -it dev-debian bash

ubuntu-shell:
	docker exec -it dev-ubuntu bash

dotnet-shell:
	docker exec -it dev-dotnet bash

tf-shell:
	@echo "🏗️  Entering Terraform Workspace..."
	docker exec -it dev-terraform sh

py-shell:
	docker exec -it dev-python python3

arcane-logs:
	docker logs -f arcane

# -------------------------
# ♻️  Maintenance & Cleanup
# -------------------------

prune:
	@echo "🧹 Removing orphaned containers and unused networks..."
	docker system prune -f

down:
	docker compose --profile dev --profile monitoring --profile ci --profile dotnet --profile terraform stop

nuke:
	@echo "☢️  NUKING ALL DATA (Volumes included)..."
	docker compose --profile dev --profile monitoring --profile ci --profile dotnet --profile terraform down --volumes --remove-orphans

rebuild: nuke
	docker compose --profile dev --profile monitoring up -d --build
