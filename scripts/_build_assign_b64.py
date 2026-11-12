import json
from pathlib import Path

steps = json.loads(Path(__file__).with_name("cdp_steps.json").read_text(encoding="utf-8-sig"))
b = ""
for i in range(1, 8):
    s = steps[i]["params"]["expression"]
    chunk = s.split('+= "', 1)[1].rstrip('";')
    b += chunk

expr = f'window.__thumbB64 = "{b}"; window.__thumbB64.length'
out = Path(__file__).with_name("_assign_b64_expr.txt")
out.write_text(expr, encoding="utf-8")
print("b64 len", len(b), "expr len", len(expr))
