"""Execute gumroad zip batch CDP steps via cursor-ide-browser MCP HTTP bridge."""
from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

BASE = Path(__file__).resolve().parent
VIEW = "aae20a"
START = int(sys.argv[1]) if len(sys.argv) > 1 else 0
END = int(sys.argv[2]) if len(sys.argv) > 2 else 55


def call_cdp(step_idx: int, payload: dict) -> dict:
    body = {
        "jsonrpc": "2.0",
        "id": step_idx,
        "method": "tools/call",
        "params": {
            "name": "browser_cdp",
            "arguments": {
                "method": payload["method"],
                "params": payload["params"],
                "viewId": payload.get("viewId", VIEW),
            },
        },
    }
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        "http://127.0.0.1:20241/mcp",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=300) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main() -> None:
    results = []
    for i in range(START, END + 1):
        path = BASE / f"_gumroad_zip_batch_{i}.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        expr_len = len(payload["params"].get("expression", ""))
        print(f"step {i}: expr_len={expr_len} file_bytes={path.stat().st_size}", flush=True)
        try:
            resp = call_cdp(i, payload)
            results.append({"step": i, "ok": True, "response": resp})
            print(json.dumps({"step": i, "ok": True, "preview": str(resp)[:500]}), flush=True)
        except Exception as e:
            results.append({"step": i, "ok": False, "error": str(e)})
            print(json.dumps({"step": i, "ok": False, "error": str(e)}), flush=True)
            break
    out = BASE / "_gumroad_batch_exec_results.json"
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
