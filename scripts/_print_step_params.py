"""Print step N params JSON for browser_cdp (stdout)."""
import json
import sys
from pathlib import Path

i = int(sys.argv[1])
steps = json.loads(
    (Path(__file__).resolve().parent / "cdp_steps.json").read_text(encoding="utf-8-sig")
)
sys.stdout.write(json.dumps(steps[i]["params"], ensure_ascii=False))
