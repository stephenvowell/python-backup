"""Execute gumroad CDP steps by posting MCP-style JSON to Cursor extension host."""
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

BASE = Path(__file__).resolve().parent
STEPS = json.loads((BASE / "gumroad_upload_steps.json").read_text(encoding="utf-8"))
VIEW = sys.argv[1] if len(sys.argv) > 1 else "aae20a"
START = int(sys.argv[2]) if len(sys.argv) > 2 else 0
END = int(sys.argv[3]) if len(sys.argv) > 3 else len(STEPS) - 1

# Try common local bridge paths (best-effort)
URLS = [
    "http://127.0.0.1:20241/mcp",
    "http://127.0.0.1:18765/mcp",
    "http://127.0.0.1:20241/cursor/mcp",
]


def post_mcp(url: str, payload: dict) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))


def call_browser_cdp(step_idx: int, method: str, params: dict) -> dict:
    body = {
        "jsonrpc": "2.0",
        "id": step_idx,
        "method": "tools/call",
        "params": {
            "name": "browser_cdp",
            "arguments": {"method": method, "params": params, "viewId": VIEW},
        },
    }
    last_err = None
    for url in URLS:
        try:
            return {"url": url, "response": post_mcp(url, body)}
        except Exception as e:
            last_err = str(e)
    raise RuntimeError(last_err or "no MCP endpoint")


if __name__ == "__main__":
    results = []
    for i in range(START, END + 1):
        step = STEPS[i]
        try:
            r = call_browser_cdp(i, step["method"], step["params"])
            results.append({"step": i, "ok": True, "result": r})
            print(json.dumps({"step": i, "ok": True}))
        except Exception as e:
            results.append({"step": i, "ok": False, "error": str(e)})
            print(json.dumps({"step": i, "ok": False, "error": str(e)}))
            break
    out = BASE / "_gumroad_cdp_run_results.json"
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
