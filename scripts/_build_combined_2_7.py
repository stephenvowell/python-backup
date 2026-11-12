import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
steps = json.loads((BASE / "cdp_steps.json").read_text(encoding="utf-8-sig"))
chunks = []
for i in range(2, 8):
    e = steps[i]["params"]["expression"]
    inner = e.split('+= "', 1)[1].rsplit('";', 1)[0]
    chunks.append(inner)
combined = 'window.__thumbB64 += "' + "".join(chunks) + '";'
(BASE / "_combined_2_7_expr.txt").write_text(combined, encoding="utf-8")
print("combined_expr_len", len(combined))
print("chunk_total", sum(len(c) for c in chunks))
print("expected_total_b64", 8001 + sum(len(c) for c in chunks))
