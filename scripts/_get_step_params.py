import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
i = int(sys.argv[1])
steps = json.loads((BASE / "cdp_steps.json").read_text(encoding="utf-8-sig"))
print(json.dumps(steps[i]["params"], ensure_ascii=False))
