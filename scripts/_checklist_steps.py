"""Run remaining CDP data steps 2-7 then upload step 8 via sequential MCP args files.
Agent: for each n in range(start,end+1), read _exec_step{n}.json and call browser_cdp.
This script only validates files and prints checklist."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
for n in range(2, 9):
    p = BASE / f"_exec_step{n}.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    print(n, d["method"], len(d["params"].get("expression", "")), "await", d["params"].get("awaitPromise"))
