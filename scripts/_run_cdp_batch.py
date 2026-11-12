"""Load CDP step params for sequential MCP browser_cdp calls."""
import json
import sys
from pathlib import Path

base = Path(__file__).resolve().parent
idx = int(sys.argv[1])
call = json.loads((base / f"mcp_call_{idx}.json").read_text(encoding="utf-8"))
print(json.dumps({"method": call["method"], "params": call["params"], "viewId": call["viewId"]}))
