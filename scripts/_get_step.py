"""Load cdp_steps.json step N and print compact JSON for MCP browser_cdp args."""
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
steps = json.loads((BASE / "cdp_steps.json").read_text(encoding="utf-8-sig"))
n = int(sys.argv[1])
view = sys.argv[2] if len(sys.argv) > 2 else "bbc0af"
step = steps[n]
out = {
    "method": step["method"],
    "params": step["params"],
    "viewId": view,
}
print(json.dumps(out, ensure_ascii=False))
