import json
from pathlib import Path

steps = json.loads(
    Path(__file__).resolve().parent.joinpath("cdp_steps.json").read_text(encoding="utf-8-sig")
)
out = Path(__file__).resolve().parent / "cdp_exprs"
out.mkdir(exist_ok=True)
for i, step in enumerate(steps):
    (out / f"{i}.txt").write_text(step["params"]["expression"], encoding="utf-8")
print(len(steps), "expressions written to", out)
