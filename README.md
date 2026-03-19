# 🛠️ Dev Toolbox 2026 — Containerized Platform for Diagnostics, Automation & Recovery

## 🚀 Overview

Dev Toolbox is a **containerized engineering platform** designed to provide fast, consistent access to diagnostic, development, and operational tooling across Linux environments.

It enables engineers to:
- rapidly spin up reproducible environments  
- standardize troubleshooting workflows  
- reduce manual setup and configuration drift  
- respond to incidents with minimal friction  

The platform is built around an **“EMT-style” operational model**:

> Tools are not installed during an incident — they are already deployed, standardized, and ready to use.

---

## 🎯 Problem

In many environments:

- Tooling is inconsistent across systems  
- Engineers lose time installing dependencies  
- Troubleshooting workflows are ad hoc  
- Diagnosing issues requires excessive setup  
- Context switching slows down incident response  

This introduces unnecessary **toil**, increases mean-time-to-resolution, and creates operational risk.

---

## 💡 Solution

Dev Toolbox provides a **self-contained, container-based platform** that:

- Delivers pre-configured environments for common engineering tasks  
- Standardizes access through a unified control interface (Makefile)  
- Enables reproducible workflows across systems  
- Integrates diagnostics, observability, and triage tooling  
- Reduces setup time from minutes → seconds  

The result is a **portable, repeatable, and operationally-ready platform** for engineering and incident response.

---

## 🚀 Quick Start

Start core development and troubleshooting environments:

```
make up-dev
```

Start monitoring stack:

```
make up-mon
```

Start full platform:

```
make up-all
```

---

## 🧰 Core Troubleshooting Environments

| Container | Role |
|----------|------|
| Debian   | Primary infrastructure & network triage |
| Ubuntu   | Platform engineering / SRE workspace |
| Kali     | Security, authentication, and protocol diagnostics |
| Netshoot | Baseline network debugging |

---

### 🐚 Shell Access

```
make debian-shell
make ubuntu-shell
make kali-shell
make netshoot-shell
```

---

## 💻 Development Runtime Environments

Pre-built, containerized runtimes for:

- Python  
- Go  
- Rust  
- .NET  
- PowerShell  
- Terraform  
- Ansible  
- VS Code Server  

These environments are:
- isolated  
- reproducible  
- consistent across hosts  

---

## 📊 Monitoring & Observability Stack

| Component     | Purpose |
|--------------|--------|
| Prometheus   | Metrics collection |
| Grafana      | Visualization |
| Node Exporter| Host-level metrics |
| cAdvisor     | Container metrics |

Access:

- Grafana → http://localhost:3000  
- Prometheus → http://localhost:9091  

---

## 🚑 Automated Incident Triage

Run structured troubleshooting workflows:

```
make triage TARGET=service.internal
make triage TARGET=service.internal PORT=8443
```

### 🔍 Diagnostic Layers

1. DNS validation  
2. Routing verification  
3. TCP connectivity  
4. TLS inspection  
5. Path quality  
6. HTTP response  

---

### 🧠 Failure Domain Identification

| Symptom   | Likely Cause |
|----------|-------------|
| DNS fails | Resolver / split horizon |
| TCP fails | Firewall / network ACL |
| TLS fails | Certificate / SNI |
| HTTP fails | Application layer |
| Latency | Routing / path issues |

**Goal:** Reduce mean-time-to-isolation (MTTI) and accelerate root cause identification.

---

## 🧩 Platform Operating Model

Dev Toolbox is designed around **role-based troubleshooting flows**:

| Container | Role |
|----------|------|
| Netshoot | First responder |
| Debian   | Infrastructure engineer |
| Kali     | Security escalation |
| Ubuntu   | Platform engineer |

---

### 🔄 Workflow

**Alert → Isolation → Domain Ownership → Resolution**

This model ensures:
- faster triage  
- clearer ownership boundaries  
- reduced cognitive load during incidents  

---

## 🎯 Design Principles

- **Reproducibility** — environments are consistent and version-controlled  
- **Speed** — tools are available instantly, without setup overhead  
- **Isolation** — workloads are containerized and non-invasive  
- **Operational Readiness** — built for real-world troubleshooting scenarios  
- **Automation First** — manual steps are minimized  
- **Modularity** — components can be extended without breaking the system  

---

## 🔥 Why This Matters

This project reflects modern platform engineering practices:

- Building **internal tooling to reduce friction**  
- Creating **standardized environments (“golden paths”)**  
- Embedding **observability into workflows**  
- Automating repetitive operational tasks  

It demonstrates the shift from:

> “manually running tools”

to:

> “building systems that make tools fast, reliable, and repeatable”

---

## 🛣️ Roadmap

- Expanded automation workflows  
- Enhanced observability and reporting  
- CI/CD integration for container validation  
- Additional runtime environments  

---

## 💬 Final Thought

> When something breaks, you shouldn’t waste time preparing to fix it —  
> you should already have everything you need.

---

## 🧑‍💻 Author

Tim Heverin  
Senior Systems Engineer → Platform Engineering Focus  
