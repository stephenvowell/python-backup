"""Print half-step payloads for sequential MCP invocation."""
import json
import os
import sys

base = os.path.dirname(os.path.abspath(__file__))
start = int(sys.argv[1]) if len(sys.argv) > 1 else 7
end = int(sys.argv[2]) if len(sys.argv) > 2 else 14

for n in range(start, end + 1):
    path = os.path.join(base, f"_h{n}_len.json")
    if not os.path.exists(path):
        d = json.load(open(os.path.join(base, f"_half_{n}.json"), encoding="utf-8"))
        e = d["params"]["expression"].rstrip().rstrip(";") + "; window.__thumbB64.length"
        payload = {
            "method": "Runtime.evaluate",
            "params": {"expression": e, "returnByValue": True},
            "viewId": "bbc0af",
        }
    else:
        payload = json.load(open(path, encoding="utf-8"))
    out = os.path.join(base, f"_mcp_half_{n}.json")
    json.dump(payload, open(out, "w", encoding="utf-8"))
    print(n, payload["params"]["expression"][:40], len(payload["params"]["expression"]))
