import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
start = int(sys.argv[1]) if len(sys.argv) > 1 else 3
end = int(sys.argv[2]) if len(sys.argv) > 2 else 7
steps = json.loads((BASE / "cdp_steps.json").read_text(encoding="utf-8-sig"))
chunks = []
for i in range(start, end + 1):
    e = steps[i]["params"]["expression"]
    inner = e.split('+= "', 1)[1].rsplit('";', 1)[0]
    chunks.append(inner)
combined = 'window.__thumbB64 += "' + "".join(chunks) + '";'
out = BASE / f"_combined_{start}_{end}_expr.txt"
out.write_text(combined, encoding="utf-8")
print(out, len(combined), sum(len(c) for c in chunks))
