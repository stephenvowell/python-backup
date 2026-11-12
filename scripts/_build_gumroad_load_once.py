"""Build MCP-friendly load-once payload from gumroad_upload_steps.json."""
import json
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent
steps = json.loads((BASE / "gumroad_upload_steps.json").read_text(encoding="utf-8"))
parts = []
for step in steps[1:13]:
    expr = step["params"]["expression"]
    prefix = 'window.__zipB64 += "'
    suffix = '";'
    if not (expr.startswith(prefix) and expr.endswith(suffix)):
        raise SystemExit(f"parse fail: {expr[:80]!r}")
    parts.append(expr[len(prefix) : -len(suffix)])

full = "".join(parts)
chunks = [full[i : i + 50000] for i in range(0, len(full), 50000)]
expr = "window.__zipB64=" + json.dumps(chunks) + ".join(''); window.__zipB64.length"
payload = {
    "method": "Runtime.evaluate",
    "params": {"expression": expr, "returnByValue": True},
    "viewId": "aae20a",
}
(BASE / "_gumroad_zip_load_once.json").write_text(
    json.dumps(payload, ensure_ascii=False), encoding="utf-8"
)
step13 = steps[13]
(BASE / "_gumroad_zip_step_13_only.json").write_text(
    json.dumps(
        {
            "method": step13["method"],
            "params": step13["params"],
            "viewId": "aae20a",
        },
        ensure_ascii=False,
    ),
    encoding="utf-8",
)
print(
    json.dumps(
        {
            "parts_from_file": len(parts),
            "total_b64": len(full),
            "load_chunks": len(chunks),
            "load_bytes": (BASE / "_gumroad_zip_load_once.json").stat().st_size,
            "step13_bytes": (BASE / "_gumroad_zip_step_13_only.json").stat().st_size,
        },
        indent=2,
    )
)
