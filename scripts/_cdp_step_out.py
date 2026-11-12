"""Execute CDP steps 0-8 by printing exact MCP args JSON to stdout (one step index)."""
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
steps = json.loads((BASE / "cdp_steps.json").read_text(encoding="utf-8-sig"))
n = int(sys.argv[1])
view = sys.argv[2] if len(sys.argv) > 2 else "bbc0af"
step = steps[n]
print(
    json.dumps(
        {"method": step["method"], "params": step["params"], "viewId": view},
        ensure_ascii=False,
    )
)
