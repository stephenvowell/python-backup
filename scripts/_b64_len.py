import json
import re
from pathlib import Path

steps = json.loads(Path(__file__).resolve().parent.joinpath("cdp_steps.json").read_text(encoding="utf-8-sig"))
total = 0
for i in range(1, 8):
    expr = steps[i]["params"]["expression"]
    m = re.search(r'\+= "([^"]*)"', expr)
    if m:
        total += len(m.group(1))
print("total_b64", total)
