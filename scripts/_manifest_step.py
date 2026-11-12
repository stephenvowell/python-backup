"""Execute one CDP step N via cursor-ide-browser MCP using stdio if CURSOR_MCP env set."""
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
n = int(sys.argv[1])
view = sys.argv[2] if len(sys.argv) > 2 else "bbc0af"
payload = json.loads((BASE / f"_runstep{n}.json").read_text(encoding="utf-8"))
# Agent reads this manifest
manifest = {
    "server": "cursor-ide-browser",
    "toolName": "browser_cdp",
    "arguments": {
        "method": payload["method"],
        "params": payload["params"],
        "viewId": view,
    },
}
print(json.dumps(manifest, ensure_ascii=False))
