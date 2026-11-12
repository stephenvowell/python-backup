import json
import os

base = os.path.dirname(os.path.abspath(__file__))
c3 = open(os.path.join(base, "c3.txt"), encoding="utf-8").read()
need = c3[4000:]
for i in range(4, 8):
    need += open(os.path.join(base, f"c{i}.txt"), encoding="utf-8").read()

expr = f'window.__thumbB64 += "{need}"; window.__thumbB64.length'
out = {
    "method": "Runtime.evaluate",
    "params": {"expression": expr, "returnByValue": True},
    "viewId": "bbc0af",
}
json.dump(out, open(os.path.join(base, "_append_remain.json"), "w", encoding="utf-8"))
print("need_len", len(need), "expected_final", 20000 + len(need))
