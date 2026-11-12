"""Inject Gumroad thumbnail via browser CDP (reads upload-thumb.js)."""
import json
import sys
from pathlib import Path

js_path = Path(__file__).resolve().parent.parent / "docs" / "upload-thumb.js"
expression = js_path.read_text(encoding="utf-8")
payload = {
    "method": "Runtime.evaluate",
    "params": {"expression": expression, "awaitPromise": True, "returnByValue": True},
}
sys.stdout.write(json.dumps(payload))
