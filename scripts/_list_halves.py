"""Emit shell-invokable summary of half steps for sequential MCP execution."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
for i in range(17):
    p = BASE / f"_half_{i}.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    print(f"{i}\t{len(d['params'].get('expression',''))}\t{p.name}")
