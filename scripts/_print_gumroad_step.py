import json
import sys
from pathlib import Path

idx = int(sys.argv[1])
path = Path(__file__).resolve().parent / f"_gumroad_zip_step_{idx}.json"
step = json.loads(path.read_text(encoding="utf-8"))
print(json.dumps({"method": step["method"], "params": step["params"], "viewId": step["viewId"]}, ensure_ascii=False))
