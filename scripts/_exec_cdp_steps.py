"""Execute CDP steps 1-8 via cursor-ide-browser MCP using stdio JSON-RPC proxy.

Writes one line per step to stdout: STEP_RESULT <json>
Requires CURSOR_MCP_CDP_PROXY env or falls back to printing step payloads for manual run.
"""
import json
import os
import sys
from pathlib import Path

VIEW = os.environ.get("CDP_VIEW_ID", "bbc0af")
base = Path(__file__).resolve().parent
steps = json.loads((base / "cdp_steps.json").read_text(encoding="utf-8-sig"))

# Emit payloads for steps 1..8 as single-line JSON prefixed with EXEC
for i in range(1, len(steps)):
    payload = {"method": steps[i]["method"], "params": steps[i]["params"], "viewId": VIEW}
    print("EXEC " + json.dumps(payload, ensure_ascii=False))
