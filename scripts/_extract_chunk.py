import json
import sys
from pathlib import Path

steps = json.loads(
    Path(__file__).resolve().parent.joinpath("gumroad_upload_steps.json").read_text(
        encoding="utf-8"
    )
)
step_idx = int(sys.argv[1])
expr = steps[step_idx]["params"]["expression"]
prefix = 'window.__zipB64 += "'
suffix = '";'
chunk = expr[len(prefix) : -len(suffix)]
print(len(chunk))
if len(sys.argv) > 2:
    n = int(sys.argv[2])
    print(chunk[:n])
