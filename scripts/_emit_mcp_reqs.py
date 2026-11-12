"""Run cdp_steps.json steps via browser_cdp by writing per-step MCP request files."""
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
VIEW = sys.argv[1] if len(sys.argv) > 1 else "bbc0af"
START = int(sys.argv[2]) if len(sys.argv) > 2 else 0
END = int(sys.argv[3]) if len(sys.argv) > 3 else 8

steps = json.loads((BASE / "cdp_steps.json").read_text(encoding="utf-8-sig"))
for i in range(START, END + 1):
    req = {
        "server": "cursor-ide-browser",
        "toolName": "browser_cdp",
        "arguments": {
            "method": steps[i]["method"],
            "params": steps[i]["params"],
            "viewId": VIEW,
        },
    }
    out = BASE / f"_mcp_req_{i}.json"
    out.write_text(json.dumps(req, ensure_ascii=False), encoding="utf-8")
    expr = steps[i]["params"].get("expression", "")
    preview = expr[:40] if expr else ""
    print(f"{i}\t{out.stat().st_size}\t{preview!r}")
