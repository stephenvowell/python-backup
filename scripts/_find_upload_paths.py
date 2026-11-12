import re
import requests

url = "https://assets.gumroad.com/vite/assets/entrypoints/base.ts-D6ge9Xcv.js"
text = requests.get(url, timeout=60).text
for pat in [r"/api/[^\"']+", r"presign", r"evaporat", r"upload", r"signed_blob", r"file_upload"]:
    hits = sorted(set(re.findall(pat, text, re.I)))
    print(f"\n=== {pat} ({len(hits)}) ===")
    for h in hits[:25]:
        print(h)
