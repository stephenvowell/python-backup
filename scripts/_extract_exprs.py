import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
for n in range(2, 9):
    d = json.loads((BASE / f"_exec_step{n}.json").read_text(encoding="utf-8"))
    (BASE / f"_expr_step{n}.txt").write_text(d["params"]["expression"], encoding="utf-8")
    print(n, len(d["params"]["expression"]))
