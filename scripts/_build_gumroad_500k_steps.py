"""Generate ~500KB append steps from gumroad_upload_steps.json b64 data."""
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
CHUNK = 500000
chunks = [full[i : i + CHUNK] for i in range(0, len(full), CHUNK)]
out = []
out.append(
    {
        "method": "Runtime.evaluate",
        "params": {
            "expression": "window.__zipB64=''; window.__zipMeta=null;",
            "returnByValue": True,
        },
        "viewId": "aae20a",
    }
)
for i, chunk in enumerate(chunks, 1):
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
upload = steps[13]
out.append(
    {
        "method": upload["method"],
        "params": upload["params"],
        "viewId": "aae20a",
    }
)
manifest = BASE / "_gumroad_zip_500k_steps.json"
manifest.write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
for j, s in enumerate(out):
    p = BASE / f"_gumroad_zip_500k_{j}.json"
    p.write_text(json.dumps(s, ensure_ascii=False), encoding="utf-8")
    print(j, len(s["params"].get("expression", "")), p.stat().st_size)
