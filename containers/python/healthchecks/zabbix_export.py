#!/usr/bin/env python3
from pathlib import Path
from typing import List, Dict, Any

SENDER_FILE = Path("/workspace/healthchecks/zabbix_sender.txt")


def write_sender_file(host: str, metrics: List[Dict[str, Any]]) -> None:
    """
    metrics: list of dicts:
      { "key": "custom.health.ok", "value": 1 }
    Writes in zabbix_sender friendly format:
      <host> <key> <value>
    """
    lines = []
    for m in metrics:
        key = m["key"]
        value = m["value"]
        lines.append(f"{host} {key} {value}")
    SENDER_FILE.write_text("\n".join(lines), encoding="utf-8")
