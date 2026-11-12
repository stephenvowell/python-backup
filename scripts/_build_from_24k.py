import json
import os

base = os.path.dirname(os.path.abspath(__file__))
full = "".join(
    open(os.path.join(base, f"c{i}.txt"), encoding="utf-8").read() for i in range(1, 8)
)
need = full[24000:]
expr = f'window.__thumbB64 += "{need}"; window.__thumbB64.length'
out = {
    "method": "Runtime.evaluate",
    "params": {"expression": expr, "returnByValue": True},
    "viewId": "bbc0af",
}
json.dump(out, open(os.path.join(base, "_append_from_24k.json"), "w", encoding="utf-8"))
print("need", len(need), "final", 24000 + len(need))
