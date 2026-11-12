"""Run CDP steps 1-8 by printing payloads; also build combined step for testing."""
import json
import re
import sys
from pathlib import Path

base = Path(__file__).resolve().parent
steps = json.loads((base / "cdp_steps.json").read_text(encoding="utf-8-sig"))
view = sys.argv[1] if len(sys.argv) > 1 else "bbc0af"

if len(sys.argv) > 2 and sys.argv[2] == "combined":
    chunks = []
    for i in range(1, 8):
        expr = steps[i]["params"]["expression"]
        m = re.search(r'\+= "([^"]*)";', expr)
        if not m:
            raise SystemExit(f"chunk not found step {i}")
        chunks.append(m.group(1))
    full = "".join(chunks)
    expr = f"window.__thumbB64 += {json.dumps(full)};"
    payload = {
        "method": "Runtime.evaluate",
        "params": {"expression": expr, "returnByValue": True},
        "viewId": view,
    }
    print(json.dumps(payload))
    sys.exit(0)

step_idx = int(sys.argv[2]) if len(sys.argv) > 2 else None
if step_idx is None:
    for i in range(1, len(steps)):
        payload = {
            "method": steps[i]["method"],
            "params": steps[i]["params"],
            "viewId": view,
        }
        print(json.dumps(payload))
else:
    step = steps[step_idx]
    print(
        json.dumps(
            {"method": step["method"], "params": step["params"], "viewId": view}
        )
    )
