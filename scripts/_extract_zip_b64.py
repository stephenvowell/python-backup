"""Extract combined base64 from gumroad_upload_steps.json steps 1-12."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
steps = json.loads((BASE / "gumroad_upload_steps.json").read_text(encoding="utf-8"))
parts = []
prefix = 'window.__zipB64 += "'
suffix = '";'
for step in steps[1:13]:
    expr = step["params"]["expression"]
    if not (expr.startswith(prefix) and expr.endswith(suffix)):
        raise SystemExit(f"unexpected expression prefix: {expr[:60]!r}")
    parts.append(expr[len(prefix) : -len(suffix)])

full = "".join(parts)
out = BASE / "_zip_payload.b64"
out.write_text(full, encoding="ascii")
print(json.dumps({"path": str(out), "len": len(full), "parts": len(parts)}))
