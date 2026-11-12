"""Split cdp_steps b64 chunks into c1.txt..c7.txt for fetch-based upload."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
steps = json.loads((BASE / "cdp_steps.json").read_text(encoding="utf-8-sig"))
total = 0
for i in range(1, 8):
    expr = steps[i]["params"]["expression"]
    chunk = expr.split('+= "', 1)[1].rstrip('";')
    (BASE / f"c{i}.txt").write_text(chunk, encoding="utf-8")
    total += len(chunk)
    print(i, len(chunk), (BASE / f"c{i}.txt").name)
print("total", total)
