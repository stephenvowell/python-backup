import json
from pathlib import Path

expr = Path(r"C:\Users\Steph\Projects\PythonBackUp\scripts\_assign_b64_expr.txt").read_text(
    encoding="utf-8"
)
payload = {
    "method": "Runtime.evaluate",
    "params": {"expression": expr, "returnByValue": True},
    "viewId": "bbc0af",
}
out = Path(r"C:\Users\Steph\Projects\PythonBackUp\scripts\_assign_mcp.json")
out.write_text(json.dumps(payload), encoding="utf-8")
print("written", out, "expr len", len(expr), "json len", out.stat().st_size)
