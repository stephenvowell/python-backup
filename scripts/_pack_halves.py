"""Print each half step as single-line JSON for sequential browser_cdp calls."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
start = int(__import__("sys").argv[1]) if len(__import__("sys").argv) > 1 else 2
end = int(__import__("sys").argv[2]) if len(__import__("sys").argv) > 2 else 16
for i in range(start, end + 1):
    d = json.loads((BASE / f"_half_{i}.json").read_text(encoding="utf-8"))
    line = json.dumps({"method": d["method"], "params": d["params"], "viewId": d["viewId"]}, ensure_ascii=False)
    (BASE / f"_mcp_half_{i}.json").write_text(line, encoding="utf-8")
    print(i, len(line))
