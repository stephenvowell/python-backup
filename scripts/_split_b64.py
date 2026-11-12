import json
from pathlib import Path

steps = json.loads(
    Path(r"C:\Users\Steph\Projects\PythonBackUp\scripts\cdp_steps.json").read_text(
        encoding="utf-8-sig"
    )
)
b64 = ""
for i in range(1, 8):
    e = steps[i]["params"]["expression"]
    b64 += e.split('+= "', 1)[1].rstrip('";')
print("total", len(b64), len(b64) % 4)
mid = len(b64) // 2
mid -= mid % 4
h1, h2 = b64[:mid], b64[mid:]
for name, half in [("h1", h1), ("h2", h2)]:
    if name == "h1":
        assign = f'window.__thumbB64 = "{half}"; window.__thumbB64.length'
    else:
        assign = f'window.__thumbB64 += "{half}"; window.__thumbB64.length'
    p = Path(rf"C:\Users\Steph\Projects\PythonBackUp\scripts\_{name}_expr.txt")
    p.write_text(assign, encoding="utf-8")
    print(name, len(half), "expr", len(assign))
