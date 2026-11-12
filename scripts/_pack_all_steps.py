"""Run all CDP steps via stdin JSON lines to an external MCP caller (agent uses CallMcpTool)."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
VIEW = "bbc0af"
steps = json.loads((BASE / "cdp_steps.json").read_text(encoding="utf-8-sig"))
results = []
for i, step in enumerate(steps):
    results.append(
        {
            "step": i,
            "method": step["method"],
            "params": step["params"],
            "viewId": VIEW,
        }
    )
(BASE / "_all_steps_mcp.json").write_text(json.dumps(results, ensure_ascii=False), encoding="utf-8")
print("wrote", len(results), "steps to _all_steps_mcp.json")
