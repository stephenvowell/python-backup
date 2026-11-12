import json
import subprocess
import sys
from pathlib import Path

# Load assign expression and emit compact JSON for MCP (used by manual step)
expr = Path(r"C:\Users\Steph\Projects\PythonBackUp\scripts\_assign_b64_expr.txt").read_text(
    encoding="utf-8"
)
payload = {
    "method": "Runtime.evaluate",
    "params": {"expression": expr, "returnByValue": True},
    "viewId": "bbc0af",
}
Path(r"C:\Users\Steph\Projects\PythonBackUp\scripts\_assign_payload.json").write_text(
    json.dumps(payload), encoding="utf-8"
)
print(len(expr))
