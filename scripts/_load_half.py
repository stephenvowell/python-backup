"""Load half step N and print JSON args for browser_cdp (agent reads stdout)."""
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
n = int(sys.argv[1])
d = json.loads((BASE / f"_half_{n}.json").read_text(encoding="utf-8"))
print(json.dumps({"method": d["method"], "params": d["params"], "viewId": d["viewId"]}, ensure_ascii=False))
