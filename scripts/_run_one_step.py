"""Print one step's MCP arguments as JSON for manual invocation."""
import json
import sys
from pathlib import Path

steps = json.loads(
    Path(r"C:\Users\Steph\Projects\PythonBackUp\scripts\cdp_steps.json").read_text(
        encoding="utf-8-sig"
    )
)
idx = int(sys.argv[1])
step = steps[idx]
out = {
    "method": step["method"],
    "params": step["params"],
    "viewId": "bbc0af",
}
print(json.dumps(out))
