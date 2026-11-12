"""Execute gumroad_upload_steps.json steps via browser_cdp MCP (agent helper).

Prints one JSON object per line: {"step": i, "method": ..., "params": ..., "viewId": "aae20a"}
Agent should CallMcpTool browser_cdp for each line sequentially.
"""
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
steps = json.loads((BASE / "gumroad_upload_steps.json").read_text(encoding="utf-8"))
view = sys.argv[1] if len(sys.argv) > 1 else "aae20a"
start = int(sys.argv[2]) if len(sys.argv) > 2 else 0
end = int(sys.argv[3]) if len(sys.argv) > 3 else len(steps) - 1

for i in range(start, end + 1):
    step = steps[i]
    out = {"step": i, "method": step["method"], "params": step["params"], "viewId": view}
    path = BASE / f"_gumroad_invoke_step_{i}.json"
    path.write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"step": i, "file": str(path), "expr_len": len(step["params"].get("expression", ""))}))
