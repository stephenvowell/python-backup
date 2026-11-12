#!/usr/bin/env python3
"""Run half-chunk CDP steps via websocket if CDP_URL env is set."""
import json
import os
import sys

try:
    import websocket
except ImportError:
    sys.exit("pip install websocket-client")

BASE = os.path.dirname(os.path.abspath(__file__))
CDP_URL = os.environ.get("CDP_URL", "")


def cdp(ws, method, params=None, msg_id=1):
    ws.send(json.dumps({"id": msg_id, "method": method, "params": params or {}}))
    while True:
        raw = ws.recv()
        data = json.loads(raw)
        if data.get("id") == msg_id:
            if "error" in data:
                raise RuntimeError(data["error"])
            return data.get("result")


def eval_expr(ws, expression, msg_id):
    r = cdp(
        ws,
        "Runtime.evaluate",
        {"expression": expression, "returnByValue": True, "awaitPromise": "awaitPromise" in expression},
        msg_id,
    )
    val = r.get("result", {})
    return val.get("value")


def main():
    if not CDP_URL:
        print("Set CDP_URL to websocket debugger URL", file=sys.stderr)
        sys.exit(2)

    ws = websocket.create_connection(CDP_URL)
    msg_id = 1

    for n in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
        path = os.path.join(BASE, f"_half_{n}.json")
        step = json.load(open(path, encoding="utf-8"))
        expr = step["params"]["expression"]
        msg_id += 1
        result = eval_expr(ws, expr, msg_id)
        if isinstance(result, (int, float)):
            print(f"half_{n}: len={result}")
        else:
            print(f"half_{n}: ok type={type(result).__name__}")

    msg_id += 1
    length = eval_expr(ws, "window.__thumbB64.length", msg_id)
    print(f"final_len={length}")

    ws.close()


if __name__ == "__main__":
    main()
