import json
import sys
from pathlib import Path

i = int(sys.argv[1])
d = json.loads(
    (Path(__file__).parent / f"_invoke{i}.json").read_text(encoding="utf-8")
)
# stdout: method, params keys only for agent; full payload written for reference
(Path(__file__).parent / f"_step{i}_params_only.json").write_text(
    json.dumps(d["params"]), encoding="utf-8"
)
print(json.dumps({"method": d["method"], "viewId": d["viewId"], "expr_len": len(d["params"]["expression"])}))
