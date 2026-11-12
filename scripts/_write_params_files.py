import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
steps = json.loads((BASE / "cdp_steps.json").read_text(encoding="utf-8-sig"))
for i in range(2, 9):
    (BASE / f"_params{i}.json").write_text(
        json.dumps(steps[i]["params"], ensure_ascii=False), encoding="utf-8"
    )
    print(i, (BASE / f"_params{i}.json").stat().st_size)
