#!/usr/bin/env python3
import sys
import ssl
import urllib.request
import urllib.error
import time
from typing import List, Dict, Any

import yaml

# Optional import: this writes Zabbix sender format to a file
# Make sure you have python/healthchecks/zabbix_export.py created as we discussed.
try:
    from zabbix_export import write_sender_file
except ImportError:
    write_sender_file = None  # Fallback if the helper doesn't exist yet


def load_checks(path: str) -> List[Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data.get("checks", [])


def run_http_check(
    name: str,
    url: str,
    timeout: float,
    expect_status: List[int],
    verify_tls: bool,
) -> Dict[str, Any]:
    start = time.time()
    ctx = None

    if url.lower().startswith("https") and not verify_tls:
        ctx = ssl._create_unverified_context()

    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            status = resp.getcode()
            elapsed_ms = (time.time() - start) * 1000.0
            result: Dict[str, Any] = {
                "name": name,
                "url": url,
                "status": status,
                "elapsed_ms": round(elapsed_ms, 1),
            }
            if status in expect_status:
                result["ok"] = True
                result["message"] = (
                    f"OK (status={status}, {result['elapsed_ms']} ms)"
                )
            else:
                result["ok"] = False
                result["message"] = (
                    f"FAIL (status={status}, {result['elapsed_ms']} ms, "
                    f"expected one of {expect_status})"
                )
            return result
    except urllib.error.URLError as e:
        return {
            "name": name,
            "url": url,
            "ok": False,
            "status": None,
            "elapsed_ms": None,
            "message": f"ERROR: {e}",
        }
    except Exception as e:
        return {
            "name": name,
            "url": url,
            "ok": False,
            "status": None,
            "elapsed_ms": None,
            "message": f"ERROR: {e}",
        }


def main() -> None:
    # Config path
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
    else:
        config_path = "/workspace/healthchecks/checks.yaml"

    print(f"Using config: {config_path}")
    checks = load_checks(config_path)
    if not checks:
        print("No checks defined in YAML.")
        sys.exit(2)

    # Run checks
    results: List[Dict[str, Any]] = []
    for item in checks:
        name = item.get("name", "unnamed-check")
        url = item["url"]
        timeout = float(item.get("timeout", 3))
        expect_status = item.get("expect_status", [200])
        verify_tls = bool(item.get("verify_tls", True))

        print(f"\n=== Running check: {name} ===")
        print(f"URL: {url}")
        res = run_http_check(name, url, timeout, expect_status, verify_tls)
        print(res["message"])
        results.append(res)

    # Summary
    total = len(results)
    ok_count = sum(1 for r in results if r.get("ok"))
    fail_count = total - ok_count

    print("\n=== HTTP Health Summary ===")
    print(f"Total checks: {total}")
    print(f"OK:          {ok_count}")
    print(f"Failed:      {fail_count}")

    # ---- Zabbix integration hook ----
    # If zabbix_export.write_sender_file exists, write a sender file with summary metrics
    if write_sender_file is not None:
        try:
            overall_ok = 1 if fail_count == 0 else 0
            metrics = [
                {"key": "lab.http_checks.total", "value": total},
                {"key": "lab.http_checks.fail", "value": fail_count},
                {"key": "lab.http_health.ok", "value": overall_ok},
            ]
            # "lab-health" is the Zabbix host you will define in the UI
            write_sender_file("lab-health", metrics)
            print("Zabbix sender file written for host 'lab-health'.")
        except Exception as e:
            print(f"Warning: failed to write Zabbix sender file: {e}")

    # Exit code: 0 if all OK, 1 otherwise
    sys.exit(0 if fail_count == 0 else 1)


if __name__ == "__main__":
    main()
