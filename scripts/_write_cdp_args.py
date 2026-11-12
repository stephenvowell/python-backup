"""Run steps 1-7 by loading JSON and printing MCP-ready args path for agent."""
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
view = "bbc0af"
start = int(sys.argv[1]) if len(sys.argv) > 1 else 1
end = int(sys.argv[2]) if len(sys.argv) > 2 else 7
for i in range(start, end + 1):
    d = json.loads((BASE / f"_runstep{i}.json").read_text(encoding="utf-8"))
    args = {"method": d["method"], "params": d["params"], "viewId": view}
    out = BASE / f"_cdp_args_{i}.json"
    out.write_text(json.dumps(args), encoding="utf-8")
print("done", start, end)
