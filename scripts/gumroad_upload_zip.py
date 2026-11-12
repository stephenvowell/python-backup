"""Upload release zip to Gumroad via browser CDP (Active Storage direct upload)."""
import base64
import hashlib
import json
import re
from pathlib import Path

ZIP = Path(__file__).resolve().parent.parent / "dist" / "PythonBackUp-windows.zip"
CHUNK = 2_000_000  # base64 chars per CDP step


def md5_b64(data: bytes) -> str:
    return base64.b64encode(hashlib.md5(data).digest()).decode("ascii")


def main() -> None:
    data = ZIP.read_bytes()
    b64 = base64.b64encode(data).decode("ascii")
    checksum = md5_b64(data)
    print(json.dumps({
        "zip": str(ZIP),
        "byte_size": len(data),
        "checksum": checksum,
        "b64_len": len(b64),
        "steps": (len(b64) + CHUNK - 1) // CHUNK + 2,
    }, indent=2))

    steps = [
        {
            "method": "Runtime.evaluate",
            "params": {
                "expression": "window.__zipB64=''; window.__zipMeta=null;",
                "returnByValue": True,
            },
        }
    ]
    for i in range(0, len(b64), CHUNK):
        part = b64[i : i + CHUNK]
        steps.append(
            {
                "method": "Runtime.evaluate",
                "params": {
                    "expression": f"window.__zipB64 += {json.dumps(part)};",
                    "returnByValue": True,
                },
            }
        )

    upload_expr = f"""
(async () => {{
  const page = JSON.parse(document.getElementById('app').dataset.page);
  const token = page.props.authenticity_token;
  const productId = page.props.id;
  const bin = atob(window.__zipB64);
  const content = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) content[i] = bin.charCodeAt(i);
  const filename = 'PythonBackUp-windows.zip';
  const byteSize = {len(data)};
  const checksum = {json.dumps(checksum)};
  const fd = new FormData();
  fd.append('blob[filename]', filename);
  fd.append('blob[content_type]', 'application/zip');
  fd.append('blob[byte_size]', String(byteSize));
  fd.append('blob[checksum]', checksum);
  const presign = await fetch('/rails/active_storage/direct_uploads', {{
    method: 'POST', credentials: 'include', headers: {{'X-CSRF-Token': token}}, body: fd
  }}).then(r => r.json());
  if (!presign.direct_upload) return {{ ok: false, step: 'presign', presign }};
  const put = await fetch(presign.direct_upload.url, {{
    method: 'PUT', headers: presign.direct_upload.headers, body: content
  }});
  if (!put.ok) return {{ ok: false, step: 'put', status: put.status, text: await put.text() }};
  const signedId = presign.signed_id;
  const uid = crypto.randomUUID();
  const richContent = [{{
    title: 'Page 1',
    description: {{
      type: 'doc',
      content: [{{
        type: 'fileEmbed',
        attrs: {{ id: uid, uid, name: filename, size: byteSize, signed_id: signedId }}
      }}]
    }}
  }}];
  const save = await fetch(`/products/${{page.props.unique_permalink}}`, {{
    method: 'PUT',
    credentials: 'include',
    headers: {{
      'X-CSRF-Token': token,
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'X-Inertia': 'true',
      'X-Requested-With': 'XMLHttpRequest'
    }},
    body: JSON.stringify({{ rich_content: richContent, public_files: [{{ signed_id: signedId, name: filename }}] }})
  }});
  const saveText = await save.text();
  return {{
    ok: put.ok && save.ok,
    putStatus: put.status,
    saveStatus: save.status,
    savePreview: saveText.slice(0, 500),
    signedId: signedId?.slice(0, 80),
    b64Len: window.__zipB64.length
  }};
}})()
"""
    steps.append(
        {
            "method": "Runtime.evaluate",
            "params": {
                "expression": upload_expr,
                "awaitPromise": True,
                "returnByValue": True,
            },
        }
    )

    out = Path(__file__).resolve().parent / "gumroad_upload_steps.json"
    out.write_text(json.dumps(steps), encoding="utf-8")
    print(f"Wrote {len(steps)} steps to {out}")


if __name__ == "__main__":
    main()
