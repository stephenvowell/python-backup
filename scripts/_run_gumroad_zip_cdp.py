"""Execute gumroad_upload_steps.json via sequential browser_cdp MCP calls."""
from __future__ import annotations

import json
import sys
from pathlib import Path

STEPS_FILE = Path(__file__).resolve().parent / "gumroad_upload_steps.json"
VIEW = sys.argv[1] if len(sys.argv) > 1 else "aae20a"
START = int(sys.argv[2]) if len(sys.argv) > 2 else 0
END = int(sys.argv[3]) if len(sys.argv) > 3 else -1

steps = json.loads(STEPS_FILE.read_text(encoding="utf-8"))
if END < 0:
    END = len(steps) - 1

results_path = Path(__file__).resolve().parent / "_gumroad_zip_cdp_results.json"
results: list[dict] = []
if results_path.exists():
    results = json.loads(results_path.read_text(encoding="utf-8"))

for i in range(START, END + 1):
    step = steps[i]
    payload = {
        "step": i,
        "method": step["method"],
        "params": step["params"],
        "viewId": VIEW,
        "expr_len": len(step["params"].get("expression", "")),
    }
    out = Path(__file__).resolve().parent / f"_gumroad_zip_invoke_{i}.json"
    out.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"ready": i, "expr_len": payload["expr_len"], "invoke": str(out)}))
