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

``` bash
make up-dev
```

Start monitoring stack:

``` bash
make up-mon
```

Start entire environment:

``` bash
make up-all
```

------------------------------------------------------------------------

## 🧰 Primary Troubleshooting Containers

  Container   Purpose
  ----------- ----------------------------------------------------
  Debian      Primary infrastructure & network triage shell
  Ubuntu      Platform engineering / SRE workspace
  Kali        Security, authentication, and protocol diagnostics
  Netshoot    Baseline network debugging container

------------------------------------------------------------------------

### 🐚 Shell Access

``` bash
make debian-shell
make ubuntu-shell
make kali-shell
make netshoot-shell
```

------------------------------------------------------------------------

## 💻 Development Runtime Containers

The toolbox provides isolated runtime environments for automation,
scripting, and application development:

-   Python
-   Go
-   Rust
-   .NET
-   PowerShell
-   Terraform
-   Ansible
-   VS Code Server

------------------------------------------------------------------------

## 📊 Monitoring Stack

  Component       Purpose
  --------------- -------------------------------
  Prometheus      Metrics collection
  Grafana         Visualization & dashboards
  Node Exporter   Host system metrics
  cAdvisor        Container performance metrics

### Monitoring URLs

-   Grafana → http://localhost:3000
-   Prometheus → http://localhost:9091

------------------------------------------------------------------------

## 🔧 Maintenance Commands

Rebuild troubleshooting containers:

``` bash
make rebuild-toolbox
```

Rebuild entire stack without deleting volumes:

``` bash
make rebuild-soft
```

Full reset (including volumes):

``` bash
make nuke
```

Stop all services:

``` bash
make down
```

Check container health and resource usage:

``` bash
make check
```

------------------------------------------------------------------------

## 🧪 Container Architecture

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

------------------------------------------------------------------------

## 🔐 Environment Configuration

Create a `.env` file in the repository root:

``` bash
UID=1000
GID=1000
VSCODE_PORT=8443
VSCODE_PASSWORD=admin
```

------------------------------------------------------------------------

## 🧭 Troubleshooting Workflows

### Network Connectivity Triage

Recommended workflow:

1.  Start with Netshoot for baseline diagnostics
2.  Use Debian container for deep network analysis
3.  Validate routing, DNS, firewall, and port reachability
4.  Escalate to Kali if authentication or security controls are
    suspected

------------------------------------------------------------------------

### Authentication & Identity Troubleshooting

Use Kali container for:

-   Kerberos validation
-   LDAP / Active Directory enumeration
-   SMB authentication testing
-   TLS certificate inspection
-   SSO and reverse proxy validation

------------------------------------------------------------------------

### Platform / Infrastructure Debugging

Use Ubuntu container for:

-   Automation scripting
-   Terraform testing
-   Configuration validation
-   DevOps workflow testing
-   Application runtime debugging

------------------------------------------------------------------------

## 🎯 Design Goals

-   Reproducible engineering environments
-   Rapid troubleshooting container access
-   Runtime isolation between tooling environments
-   Minimal host dependency footprint
-   Modular container expansion capability
-   Fast environment rebuild and reset workflows

------------------------------------------------------------------------

## 🧪 Personal Workflow Notes

Typical usage pattern:

  Task                        Recommended Container
  --------------------------- ------------------------------
  Network triage              Netshoot → Debian
  Identity / authentication   Kali
  Automation / scripting      Ubuntu
  Development runtimes        Language-specific containers
  Observability testing       Monitoring stack

------------------------------------------------------------------------

## 📝 Notes

This toolbox is a personal engineering environment and evolves alongside
homelab development, platform engineering experimentation, and
infrastructure reliability testing.

Tooling, containers, and workflows are regularly refined as new
requirements and technologies are explored.
