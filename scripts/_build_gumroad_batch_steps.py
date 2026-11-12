"""Generate batched zip b64 load steps for browser_cdp (~450KB per MCP call)."""
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

SUB = 45000
chunks = [full[i : i + SUB] for i in range(0, len(full), SUB)]
out_steps = [
    {
        "method": "Runtime.evaluate",
        "params": {
            "expression": "window.__zipParts=window.__zipParts||[]; window.__zipB64='';",
            "returnByValue": True,
        },
    }
]
batch = 10
for i in range(0, len(chunks), batch):
    batch_chunks = chunks[i : i + batch]
    expr = "window.__zipParts.push(" + ",".join(json.dumps(c) for c in batch_chunks) + "); window.__zipParts.length"
    out_steps.append(
        {
            "method": "Runtime.evaluate",
            "params": {"expression": expr, "returnByValue": True},
        }
    )
out_steps.append(
    {
        "method": "Runtime.evaluate",
        "params": {
            "expression": "window.__zipB64=window.__zipParts.join(''); ({len: window.__zipB64.length, parts: window.__zipParts.length})",
            "returnByValue": True,
        },
    }
)
out_steps.append(steps[13])
manifest = BASE / "_gumroad_zip_batch_steps.json"
manifest.write_text(json.dumps(out_steps, ensure_ascii=False), encoding="utf-8")
for j, s in enumerate(out_steps):
    payload = {**s, "viewId": "aae20a"}
    (BASE / f"_gumroad_zip_batch_{j}.json").write_text(
        json.dumps(payload, ensure_ascii=False), encoding="utf-8"
    )
    print(j, len(s["params"]["expression"]), (BASE / f"_gumroad_zip_batch_{j}.json").stat().st_size)
