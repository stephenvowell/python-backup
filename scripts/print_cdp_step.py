import json
import sys
from pathlib import Path

steps = json.loads(
    Path(__file__).resolve().parent.joinpath("cdp_steps.json").read_text(encoding="utf-8-sig")
)
idx = int(sys.argv[1])
print(json.dumps(steps[idx]))
