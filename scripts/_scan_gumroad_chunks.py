import re
import requests

BASE = "https://assets.gumroad.com/vite/assets/"
root = requests.get(BASE + "entrypoints/base.ts-D6ge9Xcv.js", timeout=60).text
chunks = sorted(set(re.findall(r"assets/[^\"']+\.js", root)))
print("chunks", len(chunks))
needles = ("presign", "evaporat", "upload", "signed_blob", "multipart", "s3", "file_url", "/files")
for chunk in chunks:
    url = BASE + chunk.split("assets/", 1)[-1]
    try:
        text = requests.get(url, timeout=30).text
    except Exception as exc:
        print("fail", chunk, exc)
        continue
    hits = [n for n in needles if n.lower() in text.lower()]
    if hits:
        print("\n", chunk, hits)
        for pat in [r"/[a-zA-Z0-9_./-]*(?:presign|upload|files|signed_blob)[a-zA-Z0-9_./-]*", r"https://[^\"']+s3[^\"']*"]:
            for m in sorted(set(re.findall(pat, text)))[:8]:
                print(" ", m)
