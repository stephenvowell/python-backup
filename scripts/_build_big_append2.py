import json
import os

base = os.path.dirname(os.path.abspath(__file__))
need = ""
for i in range(3, 8):
    need += open(os.path.join(base, f"c{i}.txt"), encoding="utf-8").read()

expr = f'window.__thumbB64 += "{need}"; window.__thumbB64.length'
out = {
    "method": "Runtime.evaluate",
    "params": {"expression": expr, "returnByValue": True},
    "viewId": "bbc0af",
}
json.dump(out, open(os.path.join(base, "_big_append2.json"), "w", encoding="utf-8"))
print("need_len", len(need))
print("expr_len", len(expr))
