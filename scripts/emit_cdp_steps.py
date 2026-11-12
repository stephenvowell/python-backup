"""Run chunked thumbnail CDP steps via stdin JSON lines to stdout."""
import json
import sys
from pathlib import Path

steps = json.loads(
    Path(__file__).resolve().parent.joinpath("cdp_steps.json").read_text(encoding="utf-8-sig")
)
start = int(sys.argv[1]) if len(sys.argv) > 1 else 1
end = int(sys.argv[2]) if len(sys.argv) > 2 else len(steps) - 1
for i in range(start, end + 1):
    print(json.dumps(steps[i]))
