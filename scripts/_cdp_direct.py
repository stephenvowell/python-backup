"""Run CDP steps 1-8 by shelling out to node with puppeteer-core if CDP URL in env."""
import json
import os
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
view = sys.argv[1] if len(sys.argv) > 1 else "bbc0af"
start = int(sys.argv[2]) if len(sys.argv) > 2 else 1
end = int(sys.argv[3]) if len(sys.argv) > 3 else 8
cdp_url = os.environ.get("CDP_URL", "")
if not cdp_url:
    print("NO_CDP_URL", file=sys.stderr)
    sys.exit(2)
try:
    import websocket
except ImportError:
    print("NO_WEBSOCKET", file=sys.stderr)
    sys.exit(3)

steps = json.loads((BASE / "cdp_steps.json").read_text(encoding="utf-8-sig"))
ws = websocket.create_connection(cdp_url)
msg_id = 0

def send(method, params=None):
    global msg_id
    msg_id += 1
    ws.send(json.dumps({"id": msg_id, "method": method, "params": params or {}}))
    while True:
        resp = json.loads(ws.recv())
        if resp.get("id") == msg_id:
            return resp

# find page target - simplified
targets = send("Target.getTargets") if False else None
print("use MCP browser_cdp instead", file=sys.stderr)
sys.exit(4)
