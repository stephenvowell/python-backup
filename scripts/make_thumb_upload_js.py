import base64
from pathlib import Path

from PIL import Image

src = Path(r"C:\Users\Steph\Desktop\PythonBackUp-Gumroad-images\gumroad-thumbnail.png")
img = Image.open(src).convert("RGB").resize((600, 600), Image.LANCZOS)
png = Path(__file__).resolve().parent.parent / "docs" / "thumb-upload.jpg"
img.save(png, format="JPEG", quality=85, optimize=True)
b64 = base64.b64encode(png.read_bytes()).decode()
js = Path(__file__).resolve().parent.parent / "docs" / "upload-thumb.js"
js.write_text(
    f"""(async () => {{
  const b64 = "{b64}";
  const bin = atob(b64);
  const arr = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) arr[i] = bin.charCodeAt(i);
  const blob = new Blob([arr], {{ type: "image/jpeg" }});
  const input = document.querySelectorAll('input[type=file]')[2];
  const file = new File([blob], "gumroad-thumbnail.jpg", {{ type: "image/jpeg" }});
  const dt = new DataTransfer();
  dt.items.add(file);
  input.files = dt.files;
  input.dispatchEvent(new Event("change", {{ bubbles: true }}));
  return "ok";
}})()""",
    encoding="utf-8",
)
print(js.stat().st_size)
