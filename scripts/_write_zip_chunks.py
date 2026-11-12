"""Write per-step b64 chunk files from gumroad_upload_steps.json."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
steps = json.loads((BASE / "gumroad_upload_steps.json").read_text(encoding="utf-8"))
prefix = 'window.__zipB64 += "'
suffix = '";'
meta = []
for i, step in enumerate(steps[1:13], 1):
    expr = step["params"]["expression"]
    chunk = expr[len(prefix) : -len(suffix)]
    path = BASE / f"_zip_chunk_{i}.b64"
    path.write_text(chunk, encoding="ascii")
    meta.append({"i": i, "len": len(chunk), "path": str(path)})
print(json.dumps(meta, indent=2))
