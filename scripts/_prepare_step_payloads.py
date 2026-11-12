import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
VIEW = sys.argv[1] if len(sys.argv) > 1 else "bbc0af"
START = int(sys.argv[2]) if len(sys.argv) > 2 else 1
END = int(sys.argv[3]) if len(sys.argv) > 3 else 8

for i in range(START, END + 1):
    payload = json.loads((BASE / f"_invoke{i}.json").read_text(encoding="utf-8-sig"))
    out = BASE / f"_step{i}_payload.json"
    out.write_text(
        json.dumps(
            {
                "method": payload["method"],
                "params": payload["params"],
                "viewId": payload.get("viewId", VIEW),
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    print(i, out.stat().st_size)
