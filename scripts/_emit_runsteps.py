"""Print one line per step: index|method|viewId|params_json for agent MCP loop."""
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
view = sys.argv[1] if len(sys.argv) > 1 else "bbc0af"
start = int(sys.argv[2]) if len(sys.argv) > 2 else 0
end = int(sys.argv[3]) if len(sys.argv) > 3 else 8
steps = json.loads((BASE / "cdp_steps.json").read_text(encoding="utf-8-sig"))
for i in range(start, end + 1):
    step = steps[i]
    payload = {"method": step["method"], "params": step["params"], "viewId": view}
    (BASE / f"_runstep{i}.json").write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    print(i, step["method"], len(step["params"].get("expression", "")), (BASE / f"_runstep{i}.json").name)
