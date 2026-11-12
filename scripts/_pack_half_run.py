"""Run half steps START..END via sequential browser_cdp using cursor_sdk if available."""
import json
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
start = int(sys.argv[1]) if len(sys.argv) > 1 else 3
end = int(sys.argv[2]) if len(sys.argv) > 2 else 14
view = sys.argv[3] if len(sys.argv) > 3 else "bbc0af"

results = []
for i in range(start, end + 1):
    d = json.loads((BASE / f"_half_{i}.json").read_text(encoding="utf-8"))
    payload = {
        "step": i,
        "method": d["method"],
        "params": d["params"],
        "viewId": view,
        "expr_len": len(d["params"]["expression"]),
    }
    results.append(payload)
    print(i, payload["expr_len"])

out = BASE / f"_half_run_{start}_{end}.json"
out.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
print("wrote", out)
