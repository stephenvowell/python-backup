"""Print CDP Runtime.evaluate steps for thumbnail upload (chunked b64)."""
import json
import re
from pathlib import Path

js = Path(__file__).resolve().parent.parent / "docs" / "upload-thumb.js"
text = js.read_text(encoding="utf-8")
m = re.search(r'const b64 = "([^"]+)"', text)
if not m:
    raise SystemExit("b64 not found")
b64 = m.group(1)

steps = [{"method": "Runtime.evaluate", "params": {"expression": "window.__thumbB64=''; window.__thumbDone=null;", "returnByValue": True}}]
chunk = 8000
for i in range(0, len(b64), chunk):
    part = b64[i : i + chunk]
    steps.append(
        {
            "method": "Runtime.evaluate",
            "params": {
                "expression": f"window.__thumbB64 += {json.dumps(part)};",
                "returnByValue": True,
            },
        }
    )

upload_expr = """
(async () => {
  const b64 = window.__thumbB64;
  const bin = atob(b64);
  const arr = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) arr[i] = bin.charCodeAt(i);
  const blob = new Blob([arr], { type: "image/jpeg" });
  const inputs = [...document.querySelectorAll('input[type=file]')].filter(i => i.accept && i.accept.includes('jpeg'));
  const input = inputs[inputs.length - 1] || document.querySelectorAll('input[type=file]')[2];
  const file = new File([blob], "gumroad-thumbnail.jpg", { type: "image/jpeg" });
  const dt = new DataTransfer();
  dt.items.add(file);
  input.files = dt.files;
  input.dispatchEvent(new Event("change", { bubbles: true }));
  input.dispatchEvent(new Event("input", { bubbles: true }));
  await new Promise(r => setTimeout(r, 500));
  return { ok: true, files: input.files.length, inputIndex: [...document.querySelectorAll('input[type=file]')].indexOf(input) };
})()
"""
steps.append(
    {
        "method": "Runtime.evaluate",
        "params": {"expression": upload_expr, "awaitPromise": True, "returnByValue": True},
    }
)
print(json.dumps(steps))
