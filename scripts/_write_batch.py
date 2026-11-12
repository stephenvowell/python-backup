"""Write JSONL of half steps 2-14 for agent MCP loop."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
out = BASE / "_half_batch.jsonl"
with out.open("w", encoding="utf-8") as f:
    for i in range(2, 15):
        d = json.loads((BASE / f"_half_{i}.json").read_text(encoding="utf-8"))
        f.write(
            json.dumps(
                {
                    "i": i,
                    "method": d["method"],
                    "params": d["params"],
                    "viewId": d["viewId"],
                },
                ensure_ascii=False,
            )
            + "\n"
        )
print("lines", sum(1 for _ in out.open(encoding="utf-8")))
