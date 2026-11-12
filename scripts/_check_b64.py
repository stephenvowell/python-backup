import base64
import json
import re
from pathlib import Path

steps = json.loads(Path(__file__).with_name("cdp_steps.json").read_text(encoding="utf-8-sig"))
b = ""
for i in range(1, 8):
    s = steps[i]["params"]["expression"]
    chunk = s.split('+= "', 1)[1].rstrip('";')
    b += chunk
    print(i, len(chunk), "total", len(b))

print("final len", len(b), "mod4", len(b) % 4)
print("valid chars", re.fullmatch(r"[A-Za-z0-9+/=]*", b) is not None)
try:
    data = base64.b64decode(b, validate=True)
    print("decode ok bytes", len(data))
except Exception as e:
    print("decode fail", e)
    data = base64.b64decode(b + "=" * ((4 - len(b) % 4) % 4))
    print("with pad bytes", len(data))
