"""Hybrid Gumroad zip upload: presign in browser, PUT via Python, attach via POST /links/{permalink}."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
from pathlib import Path

import requests

ZIP = Path(__file__).resolve().parent.parent / "dist" / "PythonBackUp-windows.zip"
PRESIGN = Path(__file__).resolve().parent / "gumroad_presign.json"


def md5_b64(data: bytes) -> str:
    return base64.b64encode(hashlib.md5(data).digest()).decode("ascii")


def put_to_s3(presign_path: Path = PRESIGN, zip_path: Path = ZIP) -> dict:
    meta = json.loads(presign_path.read_text(encoding="utf-8"))
    data = zip_path.read_bytes()
    headers = dict(meta["direct_upload"]["headers"])
    headers["Content-Length"] = str(len(data))
    resp = requests.put(meta["direct_upload"]["url"], data=data, headers=headers, timeout=300)
    resp.raise_for_status()
    return meta


def presign_js(byte_size: int, checksum: str, filename: str = "PythonBackUp-windows.zip") -> str:
    return f"""
(async () => {{
  const page = JSON.parse(document.getElementById('app').dataset.page);
  const token = page.props.authenticity_token;
  const fd = new FormData();
  fd.append('blob[filename]', {json.dumps(filename)});
  fd.append('blob[content_type]', 'application/zip');
  fd.append('blob[byte_size]', String({byte_size}));
  fd.append('blob[checksum]', {json.dumps(checksum)});
  const presign = await fetch('/rails/active_storage/direct_uploads', {{
    method: 'POST', credentials: 'include', headers: {{'X-CSRF-Token': token}}, body: fd
  }}).then(r => r.json());
  return presign;
}})()
"""


def attach_js(signed_id: str, permalink: str = "tbmyl") -> str:
    return f"""
(async () => {{
  const signedBlobId = {json.dumps(signed_id)};
  const page = JSON.parse(document.getElementById('app').dataset.page);
  const token = page.props.authenticity_token;
  const productId = page.props.id;
  window.__lastSaveBody = null;
  const orig = window.fetch;
  window.fetch = async (...args) => {{
    const [input, init] = args;
    const url = typeof input === 'string' ? input : input.url;
    if (url.includes('/links/{permalink}') && init?.body) window.__lastSaveBody = init.body;
    return orig(...args);
  }};
  [...document.querySelectorAll('button')].find(b => b.textContent?.trim() === 'Save changes')?.click();
  await new Promise(r => setTimeout(r, 2500));
  const attach = await fetch('/internal/product_public_files', {{
    method: 'POST', credentials: 'include',
    headers: {{'X-CSRF-Token': token, 'Content-Type': 'application/json', 'Accept': 'application/json'}},
    body: JSON.stringify({{ signed_blob_id: signedBlobId, product_id: productId }})
  }});
  const body = JSON.parse(window.__lastSaveBody || '{{}}');
  const pageId = body.rich_content?.[0]?.page_id || 'jqFxd0gs4iGBPvS-CzpBeQ==';
  const uid = crypto.randomUUID();
  body.rich_content = [{{ id: pageId, page_id: pageId, title: 'Page 1', description: {{ type: 'doc', content: [{{ type: 'fileEmbed', attrs: {{ id: uid, uid, name: 'PythonBackUp-windows.zip', size: {ZIP.stat().st_size if ZIP.exists() else 0}, signed_id: signedBlobId }} }}] }} }}];
  const save = await fetch('/links/{permalink}', {{
    method: 'POST', credentials: 'include',
    headers: {{'X-CSRF-Token': token, 'Content-Type': 'application/json', 'Accept': 'application/json'}},
    body: JSON.stringify(body)
  }});
  return {{
    attachStatus: attach.status,
    attachBody: await attach.text(),
    saveStatus: save.status,
    saveBody: (await save.text()).slice(0, 200)
  }};
}})()
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--zip", type=Path, default=ZIP)
    parser.add_argument("--put-only", action="store_true")
    args = parser.parse_args()
    data = args.zip.read_bytes()
    checksum = md5_b64(data)
    print(json.dumps({"zip": str(args.zip), "byte_size": len(data), "checksum": checksum}, indent=2))
    print("\n1) Run presign_js in Gumroad editor (logged in), save JSON to gumroad_presign.json")
    print(presign_js(len(data), checksum))
    if args.put_only:
        meta = put_to_s3()
        print("S3 PUT OK, signed_id:", meta["signed_id"])
        print("\n2) Run attach_js in Gumroad editor:")
        print(attach_js(meta["signed_id"]))


if __name__ == "__main__":
    main()
