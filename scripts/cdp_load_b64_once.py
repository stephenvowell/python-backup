"""Single CDP evaluate: load full thumbnail b64 from parts array."""
import json
import re
from pathlib import Path

js = Path(__file__).resolve().parent.parent / "docs" / "upload-thumb.js"
text = js.read_text(encoding="utf-8")
m = re.search(r'const b64 = "([^"]+)"', text)
b64 = m.group(1)
parts = [b64[i : i + 8000] for i in range(0, len(b64), 8000)]
expr = f"window.__thumbB64 = {json.dumps(parts)}.join(''); window.__thumbB64.length"
print(json.dumps({"method": "Runtime.evaluate", "params": {"expression": expr, "returnByValue": True}}))
