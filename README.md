Dev Toolbox 2026

Personal multi-container engineering toolbox used for:

Infrastructure troubleshooting

Network & protocol diagnostics

Security & authentication analysis

Development runtimes

Monitoring & observability

CI/CD experimentation

This environment provides reproducible containers for daily engineering workflows and incident response testing.

🚀 Quick Start

Start core development and troubleshooting containers:

make up-dev


Start monitoring stack:

make up-mon


Start entire environment:

make up-all

🧰 Primary Troubleshooting Containers
Container	Purpose
Debian	Primary infrastructure & network triage shell
Ubuntu	Platform engineering / SRE workspace
Kali	Security, authentication, and protocol diagnostics
Netshoot	Baseline network debugging container
Shell Access
make debian-shell
make ubuntu-shell
make kali-shell
make netshoot-shell

💻 Development Runtime Containers

Python

Go

Rust

.NET

PowerShell

Terraform

Ansible

VS Code Server

📊 Monitoring Stack
Component	Purpose
Prometheus	Metrics collection
Grafana	Visualization & dashboards
Node Exporter	Host metrics
cAdvisor	Container metrics
Monitoring URLs

Grafana → http://localhost:3000

Prometheus → http://localhost:9091

🔧 Maintenance Commands

Rebuild troubleshooting containers:

make rebuild-toolbox


Rebuild entire stack without deleting volumes:

make rebuild-soft


Full reset (including volumes):

make nuke

🧪 Container Architecture
Host
 ├ Docker Compose
 │
 ├ Troubleshooters
 │    ├ Debian
 │    ├ Ubuntu
 │    ├ Kali
 │    └ Netshoot
 │
 ├ Dev Runtimes
 │    ├ Python / Go / Rust / .NET
 │    ├ Terraform / Ansible
 │    ├ PowerShell
 │
 ├ Monitoring
 │    ├ Prometheus
 │    ├ Grafana
 │    ├ Node Exporter
 │    └ cAdvisor
 │
 └ CI
      └ Jenkins

🔐 Environment Configuration

Create .env file:

UID=1000
GID=1000
VSCODE_PORT=8443
VSCODE_PASSWORD=admin

🎯 Design Goals

Reproducible engineering environments

Rapid troubleshooting container access

Separation of runtime tooling by container

Minimal host dependency footprint

Modular expansion capability

📝 Notes

This toolbox is a personal engineering environment and evolves alongside homelab, platform engineering, and infrastructure reliability experiments.
