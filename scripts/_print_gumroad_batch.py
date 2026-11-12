import json
import sys
from pathlib import Path

idx = int(sys.argv[1])
path = Path(__file__).resolve().parent / f"_gumroad_zip_batch_{idx}.json"
step = json.loads(path.read_text(encoding="utf-8"))
print(json.dumps(step, ensure_ascii=False))
