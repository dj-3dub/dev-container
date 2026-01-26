#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import os
import shlex
import subprocess
import sys
from typing import Dict, Any, List, Tuple

def run(cmd: str, timeout: int = 30) -> Dict[str, Any]:
    """Run a shell command and capture stdout/stderr/rc."""
    p = subprocess.run(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=timeout,
    )
    return {
        "cmd": cmd,
        "rc": p.returncode,
        "stdout": (p.stdout or "").strip(),
        "stderr": (p.stderr or "").strip(),
    }

def have(cmd: str) -> bool:
    return subprocess.call(f"command -v {shlex.quote(cmd)} >/dev/null 2>&1", shell=True) == 0

def ssh_wrap(host: str, remote_cmd: str) -> str:
    # -o BatchMode=yes avoids hanging on password prompts; remove if you want interactive auth.
    return f"ssh -o BatchMode=yes -o StrictHostKeyChecking=accept-new {shlex.quote(host)} {shlex.quote(remote_cmd)}"

def collect(cmds: List[Tuple[str, str]], via_ssh_host: str = "") -> Dict[str, Any]:
    results = {}
    for key, cmd in cmds:
        final_cmd = ssh_wrap(via_ssh_host, cmd) if via_ssh_host else cmd
        results[key] = run(final_cmd, timeout=60)
    return results

def main():
    ap = argparse.ArgumentParser(description="Ubuntu VM hygiene audit (disk/RAM/docker/apt/journal).")
    ap.add_argument("--host", help="Run checks remotely via SSH, e.g. tim@192.168.2.51", default="")
    ap.add_argument("--outdir", help="Output directory", default="reports")
    ap.add_argument("--fix", action="store_true", help="Run safe cleanup actions (apt clean/autoremove, journal vacuum).")
    ap.add_argument("--docker-prune", action="store_true", help="Also run docker system prune -af --volumes (DANGEROUS).")
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    target = args.host if args.host else "localhost"
    safe_target = target.replace("@", "_").replace(":", "_").replace("/", "_")

    # Core read-only checks
    cmds = [
        ("date", "date"),
        ("uptime", "uptime"),
        ("df", "df -hT"),
        ("lsblk", "lsblk -f"),
        ("free", "free -h"),
        ("swap", "swapon --show || true"),
        ("top_mem", "ps aux --sort=-%mem | head -25"),
        ("top_cpu", "ps aux --sort=-%cpu | head -25"),
        ("du_root", "sudo du -xh / --max-depth=1 2>/dev/null | sort -h"),
        ("du_var", "sudo du -xh /var --max-depth=2 2>/dev/null | sort -h | tail -80"),
        ("big_files", "sudo find / -xdev -type f -size +500M -printf '%10s  %p\\n' 2>/dev/null | sort -n | tail -60"),
        ("journal_usage", "sudo journalctl --disk-usage || true"),
        ("log_sizes", "sudo du -sh /var/log/* 2>/dev/null | sort -h | tail -40"),
        ("apt_cache", "sudo du -sh /var/cache/apt/archives 2>/dev/null || true"),
        ("apt_autoremove_dry", "sudo apt-get -s autoremove --purge | sed -n '1,160p' || true"),
        ("largest_pkgs", "dpkg-query -Wf '${Installed-Size}\\t${Package}\\n' | sort -n | tail -60 || true"),
        ("recent_dpkg", "grep -E 'install |upgrade ' /var/log/dpkg.log | tail -120 || true"),
        ("running_services", "systemctl --type=service --state=running | sed -n '1,220p' || true"),
    ]

    # Docker checks (only if docker exists on target)
    docker_cmds = [
        ("docker_ps", "docker ps -a --format 'table {{.Names}}\\t{{.Status}}\\t{{.Image}}'"),
        ("docker_df", "docker system df -v"),
        ("docker_exited", "docker ps -a --filter status=exited --format 'table {{.Names}}\\t{{.Status}}\\t{{.Image}}'"),
        ("docker_dangling_images", "docker images -f dangling=true --format 'table {{.Repository}}\\t{{.Tag}}\\t{{.ID}}\\t{{.Size}}'"),
        ("docker_dangling_vols", "docker volume ls -f dangling=true"),
        ("docker_prune_dry", "docker system prune -a --volumes --dry-run"),
    ]

    results: Dict[str, Any] = {}
    results["meta"] = {"target": target, "timestamp": stamp, "fix": args.fix, "docker_prune": args.docker_prune}

    # Determine docker availability (local or remote)
    if args.host:
        # Remote check for docker
        docker_present = run(ssh_wrap(args.host, "command -v docker >/dev/null 2>&1; echo $?"))["stdout"].strip() == "0"
    else:
        docker_present = have("docker")

    results["meta"]["docker_present"] = docker_present

    results["checks"] = collect(cmds, via_ssh_host=args.host)

    if docker_present:
        results["docker"] = collect(docker_cmds, via_ssh_host=args.host)
    else:
        results["docker"] = {"note": "docker not found on target"}

    # Optional SAFE fixes
    fixes = []
    if args.fix:
        fix_cmds = [
            ("apt_clean", "sudo apt-get clean"),
            ("apt_autoremove", "sudo apt-get autoremove --purge -y"),
            ("journal_vacuum_7d", "sudo journalctl --vacuum-time=7d || true"),
        ]
        fixes = list(collect(fix_cmds, via_ssh_host=args.host).items())

    # Optional DANGEROUS docker prune
    docker_prune_result = None
    if args.docker_prune and docker_present:
        docker_prune_result = run(ssh_wrap(args.host, "docker system prune -af --volumes") if args.host else "docker system prune -af --volumes", timeout=600)

    # Write outputs
    json_path = os.path.join(args.outdir, f"vm_doctor_{safe_target}_{stamp}.json")
    txt_path = os.path.join(args.outdir, f"vm_doctor_{safe_target}_{stamp}.txt")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    # Human report
    def section(title: str, block: Dict[str, Any]) -> str:
        s = [f"\n== {title} =="]
        if isinstance(block, dict) and "stdout" in block:
            s.append(block["stdout"])
            if block.get("stderr"):
                s.append("\n-- stderr --\n" + block["stderr"])
            s.append(f"\n(rc={block.get('rc')})")
        else:
            s.append(str(block))
        return "\n".join(s)

    lines = []
    lines.append(f"VM DOCTOR REPORT: {target} @ {stamp}")
    lines.append(f"docker_present={docker_present} fix={args.fix} docker_prune={args.docker_prune}")

    for k, v in results["checks"].items():
        lines.append(section(k, v))

    if docker_present:
        for k, v in results.get("docker", {}).items():
            lines.append(section(f"docker/{k}", v))

    if args.fix:
        lines.append("\n== FIXES ==")
        for k, v in fixes:
            lines.append(section(k, v))

    if docker_prune_result:
        lines.append(section("docker_prune", docker_prune_result))

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"Wrote:\n  {txt_path}\n  {json_path}")

if __name__ == "__main__":
    sys.exit(main())
