import json
import sys
from pathlib import Path

idx = int(sys.argv[1])
path = Path(__file__).resolve().parent / f"_gumroad_zip_500k_{idx}.json"
print(path.read_text(encoding="utf-8"))
