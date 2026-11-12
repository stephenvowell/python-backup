"""Execute invoke JSON files via cursor-ide-browser if run inside agent with MCP."""
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
start = int(sys.argv[1]) if len(sys.argv) > 1 else 1
end = int(sys.argv[2]) if len(sys.argv) > 2 else 7
for i in range(start, end + 1):
    p = BASE / f"_invoke{i}.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    out = BASE / f"_mcp_call_{i}.json"
    out.write_text(
        json.dumps(
            {
                "server": "cursor-ide-browser",
                "toolName": "browser_cdp",
                "arguments": {
                    "method": d["method"],
                    "params": d["params"],
                    "viewId": d["viewId"],
                },
            }
        ),
        encoding="utf-8",
    )
    print("wrote", out.name, "expr_len", len(d["params"]["expression"]))
