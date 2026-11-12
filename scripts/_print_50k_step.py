import json
import sys
from pathlib import Path

idx = int(sys.argv[1])
p = Path(__file__).resolve().parent / f"_gumroad_zip_50k_{idx}.json"
d = json.loads(p.read_text(encoding="utf-8"))
print(json.dumps({"method": d["method"], "params": d["params"], "viewId": d.get("viewId", "aae20a")}))
