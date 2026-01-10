# homelab-helper

`homelab-helper` is a lightweight Rust-based command-line tool for performing service, network, and HTTP health checks inside a homelab environment. It’s designed to be fast, portable, and easy to integrate into DevContainers, Makefiles, automation pipelines, and monitoring scripts.

The tool runs inside your `dev-rust` development container but works against any LAN or public host. It complements Python- and Ansible-based checks for a full observability toolkit.

---

## 🚀 Features

### ✔ ICMP Ping  
Uses your system `ping` binary for reliable packet-level reachability checks.

### ✔ TCP Port checks  
Quickly validate if commonly used ports (SSH, HTTP, HTTPS, custom ports) are open.

### ✔ HTTP / HTTPS checks  
Uses `curl` to return high-level service health (status codes, TLS status, etc.).

### ✔ DNS lookup  
Resolves hostnames → IP addresses using Rust’s built-in resolver.

### ✔ Port scanning  
Scan a numerical range (e.g., ports 20 → 30).

### ✔ Full health bundle (`check`)  
Runs the following in sequence:

1. DNS lookup  
2. ICMP ping  
3. Common port checks (22, 80, 443)  
4. HTTP & HTTPS status checks  

### ✔ Lightweight + dependency-free  
No external crates like `reqwest` or `trust-dns` needed — just system tools and standard library.

---

## 📦 Installation (Dev Container)

If you're using the Dev Containers workflow:

```bash
make rust-build
