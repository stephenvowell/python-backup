"""Run one gumroad CDP step file through MCP stdio if configured, else print invoke JSON."""
import json
import os
import sys
from pathlib import Path

idx = int(sys.argv[1])
base = Path(__file__).resolve().parent
path = base / f"_gumroad_zip_step_{idx}.json"
if not path.exists():
    path = base / f"_gumroad_zip_500k_{idx}.json"
step = json.loads(path.read_text(encoding="utf-8"))
print(json.dumps(step, ensure_ascii=False))
