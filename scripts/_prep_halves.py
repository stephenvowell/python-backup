"""Run remaining half chunks + upload via sequential MCP-like CDP eval files."""
import json
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))

def load_half(n):
    return json.load(open(os.path.join(BASE, f"_half_{n}.json"), encoding="utf-8"))

def main():
    start = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    end = int(sys.argv[2]) if len(sys.argv) > 2 else 14
    for n in range(start, end + 1):
        d = load_half(n)
        expr = d["params"]["expression"]
        out = os.path.join(BASE, f"_run_half_{n}.json")
        json.dump({"method": "Runtime.evaluate", "params": d["params"], "viewId": "bbc0af"}, open(out, "w", encoding="utf-8"))
        print(n, len(expr))

if __name__ == "__main__":
    main()
