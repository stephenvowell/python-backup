import json
from pathlib import Path

steps = json.loads(Path(__file__).with_name("cdp_steps.json").read_text(encoding="utf-8-sig"))
e6 = steps[6]["params"]["expression"]
e7 = steps[7]["params"]["expression"]
chunk7 = e7.split('+= "', 1)[1].rstrip('";')
combined = e6.rstrip('";') + chunk7 + '";'
out = Path(__file__).with_name("_combined_6_7.txt")
out.write_text(combined, encoding="utf-8")
print("len", len(combined))
