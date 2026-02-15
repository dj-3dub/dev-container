# Dev Toolbox 2026

Personal multi-container engineering toolbox designed for:

-   Infrastructure troubleshooting
-   Network & protocol diagnostics
-   Security & authentication analysis
-   Development runtime environments
-   Monitoring & observability
-   CI/CD experimentation

This environment provides reproducible containers for daily engineering
workflows, incident response testing, and homelab platform engineering.

------------------------------------------------------------------------

## 🚀 Quick Start

Start core development and troubleshooting containers:

make up-dev

Start monitoring stack:

make up-mon

Start entire environment:

make up-all

------------------------------------------------------------------------

## 🧰 Primary Troubleshooting Containers

  Container   Purpose
  ----------- ----------------------------------------------------
  Debian      Primary infrastructure & network triage shell
  Ubuntu      Platform engineering / SRE workspace
  Kali        Security, authentication, and protocol diagnostics
  Netshoot    Baseline network debugging container

### 🐚 Shell Access

make debian-shell make ubuntu-shell make kali-shell make netshoot-shell

------------------------------------------------------------------------

## 💻 Development Runtime Containers

Python, Go, Rust, .NET, PowerShell, Terraform, Ansible, VS Code Server

------------------------------------------------------------------------

## 📊 Monitoring Stack

  Component       Purpose
  --------------- --------------------
  Prometheus      Metrics collection
  Grafana         Visualization
  Node Exporter   Host metrics
  cAdvisor        Container metrics

Grafana → http://localhost:3000\
Prometheus → http://localhost:9091

------------------------------------------------------------------------

## 🚑 Automated Incident Triage

make triage TARGET=service.internal make triage TARGET=service.internal
PORT=8443

Layers tested:

1.  DNS validation
2.  Routing verification
3.  TCP connectivity
4.  TLS inspection
5.  Path quality
6.  HTTP response

Failure domain identification:

  Symptom      Likely Cause
  ------------ --------------------------
  DNS fails    resolver / split horizon
  TCP fails    firewall
  TLS fails    certificate / SNI
  HTTP fails   application
  Latency      routing

Goal: reduce mean-time-to-isolation (MTTI).

------------------------------------------------------------------------

## 🧩 Platform Engineering Philosophy

Tools exist where incidents are analyzed --- not installed during
incidents.

  Container   Role
  ----------- -------------------------
  Netshoot    First responder
  Debian      Infrastructure engineer
  Kali        Security escalation
  Ubuntu      Platform engineer

Workflow: Alert → Isolation → Domain Expert → Resolution

------------------------------------------------------------------------

## 🎯 Design Goals

-   Reproducible engineering environments
-   Rapid troubleshooting access
-   Runtime isolation
-   Minimal host dependency
-   Modular expansion
-   Fast rebuild/reset workflows
