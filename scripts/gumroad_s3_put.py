import json
from pathlib import Path

import requests

ZIP = Path(__file__).resolve().parent.parent / "dist" / "PythonBackUp-windows.zip"
META = Path(__file__).resolve().parent / "gumroad_presign.json"


def main() -> None:
    meta = json.loads(META.read_text(encoding="utf-8"))
    data = ZIP.read_bytes()
    headers = dict(meta["direct_upload"]["headers"])
    headers["Content-Length"] = str(len(data))
    print(f"Uploading {len(data)} bytes to S3...")
    resp = requests.put(
        meta["direct_upload"]["url"],
        data=data,
        headers=headers,
        timeout=300,
    )
    print("PUT status:", resp.status_code)
    print("ETag:", resp.headers.get("ETag"))
    if not resp.ok:
        print(resp.text[:500])
        raise SystemExit(1)
    print("signed_id:", meta["signed_id"])


if __name__ == "__main__":
    main()
