"""Generate half-chunk CDP steps (~4KB each) for MCP browser_cdp."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
steps = json.loads((BASE / "cdp_steps.json").read_text(encoding="utf-8-sig"))
half_steps = []
half_steps.append(steps[0])  # reset
for i in range(1, 8):
    expr = steps[i]["params"]["expression"]
    chunk = expr.split('+= "', 1)[1].rstrip('";')
    mid = len(chunk) // 2
    for part in (chunk[:mid], chunk[mid:]):
        half_steps.append(
            {
                "method": "Runtime.evaluate",
                "params": {
                    "expression": f'window.__thumbB64 += "{part}";',
                    "returnByValue": True,
                },
            }
        )
# verify step
half_steps.append(
    {
        "method": "Runtime.evaluate",
        "params": {
            "expression": "window.__thumbB64.length",
            "returnByValue": True,
        },
    }
)
half_steps.append(steps[8])  # upload
(BASE / "cdp_half_steps.json").write_text(
    json.dumps(half_steps, ensure_ascii=False, indent=2), encoding="utf-8"
)
for j, s in enumerate(half_steps):
    ln = len(s["params"].get("expression", ""))
    (BASE / f"_half_{j}.json").write_text(
        json.dumps(
            {"method": s["method"], "params": s["params"], "viewId": "bbc0af"},
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    print(j, ln, (BASE / f"_half_{j}.json").stat().st_size)
