"""Write compact step payloads with viewId for MCP browser_cdp."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
view = "bbc0af"  # fallback; agent may override
steps = json.loads((BASE / "cdp_steps.json").read_text(encoding="utf-8-sig"))
for i, step in enumerate(steps):
    out = {
        "method": step["method"],
        "params": step["params"],
        "viewId": view,
    }
    p = BASE / f"_step{i}_out.json"
    p.write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
    print(i, "expr_len", len(step["params"].get("expression", "")), "->", p.name)
