"""Run all CDP steps 0-8 sequentially via JSON payloads (for manual MCP invoke)."""
import json
from pathlib import Path

base = Path(__file__).resolve().parent
steps = json.loads((base / "cdp_steps.json").read_text(encoding="utf-8-sig"))
view = "bbc0af"
out = base / "cdp_run_results.json"
results = []
for i, step in enumerate(steps):
    payload = {"step": i, "method": step["method"], "params": step["params"], "viewId": view}
    results.append(payload)
out.write_text(json.dumps(results, indent=2), encoding="utf-8")
print(f"Wrote {len(results)} payloads to {out}")
