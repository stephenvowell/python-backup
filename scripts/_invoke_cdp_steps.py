"""Invoke CDP steps 1-8 by printing JSON lines for external MCP runner."""
import json
import sys
from pathlib import Path

base = Path(__file__).resolve().parent
steps = json.loads((base / "cdp_steps.json").read_text(encoding="utf-8-sig"))
view = sys.argv[1] if len(sys.argv) > 1 else "bbc0af"
start = int(sys.argv[2]) if len(sys.argv) > 2 else 1
end = int(sys.argv[3]) if len(sys.argv) > 3 else 8
for i in range(start, end + 1):
    step = steps[i]
    line = json.dumps(
        {"method": step["method"], "params": step["params"], "viewId": view},
        ensure_ascii=False,
    )
    sys.stdout.write(line + "\n")
    sys.stdout.flush()
