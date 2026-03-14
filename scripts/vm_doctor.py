#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import os
import re
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
    return subprocess.call(
        f"command -v {shlex.quote(cmd)} >/dev/null 2>&1",
        shell=True,
    ) == 0


def ssh_wrap(host: str, remote_cmd: str) -> str:
    # -o BatchMode=yes avoids hanging on password prompts; remove if you want interactive auth.
    return (
        f"ssh -o BatchMode=yes -o StrictHostKeyChecking=accept-new "
        f"{shlex.quote(host)} {shlex.quote(remote_cmd)}"
    )


def collect(cmds: List[Tuple[str, str]], via_ssh_host: str = "") -> Dict[str, Any]:
    results = {}
    for key, cmd in cmds:
        final_cmd = ssh_wrap(via_ssh_host, cmd) if via_ssh_host else cmd
        results[key] = run(final_cmd, timeout=60)
    return results


def parse_size_to_bytes(size_str: str) -> int:
    """
    Convert Docker-style sizes like '15.2GB', '829MB', '32B' into bytes.
    """
    s = (size_str or "").strip().upper()
    m = re.match(r"^([0-9]*\.?[0-9]+)\s*([KMGTP]?B)$", s)
    if not m:
        return 0

    value = float(m.group(1))
    unit = m.group(2)
    factors = {
        "B": 1,
        "KB": 1024,
        "MB": 1024**2,
        "GB": 1024**3,
        "TB": 1024**4,
        "PB": 1024**5,
    }
    return int(value * factors.get(unit, 1))


def docker_health_summary(results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Build a lightweight Docker health summary from collected command output.
    """
    summary: Dict[str, Any] = {
        "build_cache_bytes": 0,
        "build_cache_human": "0B",
        "exited_containers": 0,
        "large_images": [],
        "warnings": [],
    }

    docker_df = results.get("docker", {}).get("docker_df", {}).get("stdout", "")
    docker_exited = results.get("docker", {}).get("docker_exited", {}).get("stdout", "")

    # Parse build cache usage from `docker system df -v`
    for line in docker_df.splitlines():
        if "Build cache usage:" in line:
            human = line.split("Build cache usage:", 1)[1].strip()
            summary["build_cache_human"] = human
            summary["build_cache_bytes"] = parse_size_to_bytes(human)
            break

    # Count exited containers
    exited_lines = [ln for ln in docker_exited.splitlines()[1:] if ln.strip()]
    summary["exited_containers"] = len(exited_lines)

    # Parse large images from "Images space usage" section
    in_images_section = False
    for line in docker_df.splitlines():
        stripped = line.strip()

        if stripped == "Images space usage:":
            in_images_section = True
            continue

        if in_images_section and stripped == "":
            break

        if not in_images_section:
            continue

        if stripped.startswith("REPOSITORY"):
            continue

        parts = line.split()
        if len(parts) >= 6:
            repo = parts[0]
            tag = parts[1]
            size = parts[5]
            size_bytes = parse_size_to_bytes(size)
            if size_bytes >= 1024**3:  # 1GB+
                summary["large_images"].append(
                    {
                        "image": f"{repo}:{tag}",
                        "size": size,
                    }
                )

    # Warnings
    if summary["build_cache_bytes"] >= 5 * 1024**3:
        summary["warnings"].append(
            f"Large Docker build cache detected: {summary['build_cache_human']}"
        )

    if summary["exited_containers"] >= 3:
        summary["warnings"].append(
            f"Multiple exited containers detected: {summary['exited_containers']}"
        )

    if len(summary["large_images"]) >= 3:
        summary["warnings"].append(
            f"Several large Docker images detected: {len(summary['large_images'])}"
        )

    return summary


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Cross-distro VM hygiene audit (disk/RAM/docker/packages/journal)."
    )
    ap.add_argument("--host", help="Run checks remotely via SSH, e.g. tim@192.168.2.51", default="")
    ap.add_argument("--outdir", help="Output directory", default="reports")
    ap.add_argument(
        "--fix",
        action="store_true",
        help="Run safe cleanup actions (package clean/autoremove, journal vacuum).",
    )
    ap.add_argument(
        "--docker-prune",
        action="store_true",
        help="Also run docker system prune -af --volumes (DANGEROUS).",
    )
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    target = args.host if args.host else "localhost"
    safe_target = target.replace("@", "_").replace(":", "_").replace("/", "_")

    # Detect OS family
    os_release_cmd = "source /etc/os-release 2>/dev/null && echo ${ID:-unknown}"
    os_id_result = run(ssh_wrap(args.host, os_release_cmd) if args.host else os_release_cmd)
    os_id = (os_id_result.get("stdout") or "unknown").strip().lower()

    is_debian = os_id in ("ubuntu", "debian")
    is_rhel = os_id in ("rhel", "centos", "rocky", "almalinux", "fedora")

    # Core read-only checks
    cmds: List[Tuple[str, str]] = [
        ("date", "date"),
        ("uptime", "uptime"),
        ("os_release", "cat /etc/os-release 2>/dev/null || true"),
        ("df", "df -hT"),
        ("lsblk", "lsblk -f"),
        ("free", "free -h"),
        ("swap", "swapon --show || true"),
        ("top_mem", "ps aux --sort=-%mem | head -25"),
        ("top_cpu", "ps aux --sort=-%cpu | head -25"),
        ("du_root", "sudo du -xh / --max-depth=1 2>/dev/null | sort -h"),
        ("du_var", "sudo du -xh /var --max-depth=2 2>/dev/null | sort -h | tail -80"),
        (
            "big_files",
            "sudo find / -xdev -type f -size +500M -printf '%10s  %p\\n' 2>/dev/null | sort -n | tail -60",
        ),
        ("journal_usage", "sudo journalctl --disk-usage || true"),
        ("log_sizes", "sudo du -sh /var/log/* 2>/dev/null | sort -h | tail -40"),
        (
            "pkg_cache",
            "sudo du -sh /var/cache/apt/archives 2>/dev/null || "
            "sudo du -sh /var/cache/dnf 2>/dev/null || true",
        ),
        (
            "pkg_autoremove_dry",
            "(sudo apt-get -s autoremove --purge 2>/dev/null || "
            "sudo dnf repoquery --unneeded 2>/dev/null) | sed -n '1,160p' || true",
        ),
        (
            "largest_pkgs",
            "(dpkg-query -Wf '${Installed-Size}\\t${Package}\\n' 2>/dev/null || "
            "rpm -qa --queryformat '%{SIZE}\\t%{NAME}\\n' 2>/dev/null) | sort -n | tail -60 || true",
        ),
        (
            "recent_pkgs",
            "(grep -E 'install |upgrade ' /var/log/dpkg.log 2>/dev/null || "
            "sudo dnf history list 2>/dev/null) | head -120 || true",
        ),
        ("running_services", "systemctl --type=service --state=running | sed -n '1,220p' || true"),
    ]

    # Docker checks (only if docker exists on target)
    docker_cmds: List[Tuple[str, str]] = [
        ("docker_ps", "docker ps -a --format 'table {{.Names}}\\t{{.Status}}\\t{{.Image}}'"),
        ("docker_df", "docker system df -v"),
        (
            "docker_exited",
            "docker ps -a --filter status=exited --format 'table {{.Names}}\\t{{.Status}}\\t{{.Image}}'",
        ),
        (
            "docker_dangling_images",
            "docker images -f dangling=true --format 'table {{.Repository}}\\t{{.Tag}}\\t{{.ID}}\\t{{.Size}}'",
        ),
        ("docker_dangling_vols", "docker volume ls -f dangling=true"),
        ("docker_prune_candidate", "docker system df -v"),
    ]

    results: Dict[str, Any] = {}
    results["meta"] = {
        "target": target,
        "timestamp": stamp,
        "fix": args.fix,
        "docker_prune": args.docker_prune,
        "os_id": os_id,
        "is_debian": is_debian,
        "is_rhel": is_rhel,
    }

    # Determine docker availability (local or remote)
    if args.host:
        docker_present = (
            run(ssh_wrap(args.host, "command -v docker >/dev/null 2>&1; echo $?"))["stdout"].strip() == "0"
        )
    else:
        docker_present = have("docker")

    results["meta"]["docker_present"] = docker_present

    results["checks"] = collect(cmds, via_ssh_host=args.host)

    if docker_present:
        results["docker"] = collect(docker_cmds, via_ssh_host=args.host)
        results["docker_health"] = docker_health_summary(results)
    else:
        results["docker"] = {"note": "docker not found on target"}
        results["docker_health"] = {"note": "docker not found on target"}

    # Optional SAFE fixes
    fixes = []
    if args.fix:
        fix_cmds: List[Tuple[str, str]] = []

        if is_debian:
            fix_cmds.extend(
                [
                    ("pkg_clean", "sudo apt-get clean"),
                    ("pkg_autoremove", "sudo apt-get autoremove --purge -y"),
                ]
            )
        elif is_rhel:
            fix_cmds.extend(
                [
                    ("pkg_clean", "sudo dnf clean all"),
                    ("pkg_autoremove", "sudo dnf autoremove -y || true"),
                ]
            )
        else:
            fix_cmds.append(("pkg_clean", "echo 'No supported package cleanup for this distro'"))

        fix_cmds.append(("journal_vacuum_7d", "sudo journalctl --vacuum-time=7d || true"))

        fixes = list(collect(fix_cmds, via_ssh_host=args.host).items())

    # Optional DANGEROUS docker prune
    docker_prune_result = None
    if args.docker_prune and docker_present:
        prune_cmd = "docker system prune -af --volumes"
        docker_prune_result = run(
            ssh_wrap(args.host, prune_cmd) if args.host else prune_cmd,
            timeout=600,
        )

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

    lines: List[str] = []
    lines.append(f"VM DOCTOR REPORT: {target} @ {stamp}")
    lines.append(
        f"docker_present={docker_present} fix={args.fix} docker_prune={args.docker_prune} "
        f"os_id={os_id}"
    )

    for k, v in results["checks"].items():
        lines.append(section(k, v))

    if docker_present:
        for k, v in results.get("docker", {}).items():
            lines.append(section(f"docker/{k}", v))

        lines.append("\n== docker/health_summary ==")
        dh = results.get("docker_health", {})
        lines.append(f"build_cache={dh.get('build_cache_human', '0B')}")
        lines.append(f"exited_containers={dh.get('exited_containers', 0)}")

        large_images = dh.get("large_images", [])
        if large_images:
            lines.append("\nLarge images:")
            for item in large_images:
                lines.append(f"  - {item['image']} ({item['size']})")

        warnings = dh.get("warnings", [])
        if warnings:
            lines.append("\nWarnings:")
            for w in warnings:
                lines.append(f"  - {w}")
        else:
            lines.append("\nWarnings:")
            lines.append("  - none")

    if args.fix:
        lines.append("\n== FIXES ==")
        for k, v in fixes:
            lines.append(section(k, v))

    if docker_prune_result:
        lines.append(section("docker_prune", docker_prune_result))

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"Wrote:\n  {txt_path}\n  {json_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
