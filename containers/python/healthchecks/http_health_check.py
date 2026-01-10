#!/usr/bin/env python3
import sys
import urllib.request
import urllib.error

def main():
    if len(sys.argv) < 2:
        print("Usage: http_health_check.py URL [TIMEOUT_SECONDS]", file=sys.stderr)
        sys.exit(2)

    url = sys.argv[1]
    timeout = float(sys.argv[2]) if len(sys.argv) > 2 else 3.0

    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            status = resp.getcode()
            if 200 <= status < 300:
                print(f"OK: {url} responded with status {status}")
                sys.exit(0)
            else:
                print(f"FAIL: {url} responded with status {status}")
                sys.exit(1)
    except urllib.error.URLError as e:
        print(f"ERROR: {url} unreachable: {e}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"ERROR: {url} unexpected error: {e}", file=sys.stderr)
        sys.exit(2)

if __name__ == "__main__":
    main()
