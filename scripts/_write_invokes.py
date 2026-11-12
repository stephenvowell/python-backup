"""Run CDP steps 1-7 by printing step index after each invoke file is ready."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
steps = json.loads((BASE / "cdp_steps.json").read_text(encoding="utf-8-sig"))
for i in range(1, 8):
    expr = steps[i]["params"]["expression"]
    out = BASE / f"_invoke{i}.json"
    payload = {
        "method": "Runtime.evaluate",
        "params": {"expression": expr, "returnByValue": True},
        "viewId": "bbc0af",
    }
    out.write_text(json.dumps(payload), encoding="utf-8")
    chunk = expr.split('+= "', 1)[1].rstrip('";')
    print(i, "chunk", len(chunk), "file", out.stat().st_size)
