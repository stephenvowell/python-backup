"""Load step N from cdp_steps.json and print MCP browser_cdp arguments as JSON."""
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
VIEW = sys.argv[2] if len(sys.argv) > 2 else "bbc0af"
i = int(sys.argv[1])
steps = json.loads((BASE / "cdp_steps.json").read_text(encoding="utf-8-sig"))
step = steps[i]
out = {
    "method": step["method"],
    "params": step["params"],
    "viewId": VIEW,
}
sys.stdout.write(json.dumps(out, ensure_ascii=False))
