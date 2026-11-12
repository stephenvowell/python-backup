"""Generate 50KB append steps + upload from gumroad_upload_steps.json."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
steps = json.loads((BASE / "gumroad_upload_steps.json").read_text(encoding="utf-8"))
prefix = 'window.__zipB64 += "'
suffix = '";'
parts = []
for step in steps[1:13]:
    expr = step["params"]["expression"]
    parts.append(expr[len(prefix) : -len(suffix)])
full = "".join(parts)
CHUNK = 50000
chunks = [full[i : i + CHUNK] for i in range(0, len(full), CHUNK)]
out = [
    {
        "method": "Runtime.evaluate",
        "params": {
            "expression": "window.__zipB64=''; window.__zipMeta=null;",
            "returnByValue": True,
        },
        "viewId": "aae20a",
    }
]
for chunk in chunks:
    out.append(
        {
            "method": "Runtime.evaluate",
            "params": {
                "expression": f"window.__zipB64 += {json.dumps(chunk)}; window.__zipB64.length",
                "returnByValue": True,
            },
            "viewId": "aae20a",
        }
    )
out.append(
    {
        "method": steps[13]["method"],
        "params": steps[13]["params"],
        "viewId": "aae20a",
    }
)
(BASE / "_gumroad_zip_50k_manifest.json").write_text(
    json.dumps({"count": len(out), "expected_b64": len(full)}, indent=2), encoding="utf-8"
)
for j, s in enumerate(out):
    (BASE / f"_gumroad_zip_50k_{j}.json").write_text(
        json.dumps(s, ensure_ascii=False), encoding="utf-8"
    )
print(len(out), "steps", "expected_b64", len(full))
