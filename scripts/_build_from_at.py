import json
import os

base = os.path.dirname(os.path.abspath(__file__))
full = "".join(
    open(os.path.join(base, f"c{i}.txt"), encoding="utf-8").read() for i in range(1, 8)
)
for at in (32000,):
    need = full[at:]
    expr = f'window.__thumbB64 += "{need}"; window.__thumbB64.length'
    json.dump(
        {
            "method": "Runtime.evaluate",
            "params": {"expression": expr, "returnByValue": True},
            "viewId": "bbc0af",
        },
        open(os.path.join(base, f"_append_from_{at}.json"), "w", encoding="utf-8"),
    )
    print(at, len(need), at + len(need))
