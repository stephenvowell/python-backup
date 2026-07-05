"""Build Gumroad cover + thumbnail from docs/screenshot.png."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageFilter

BG = (13, 21, 40)
DOCS = Path(__file__).resolve().parent.parent / "docs"


def _shadow(size: tuple[int, int], radius: int = 28) -> Image.Image:
    w, h = size
    layer = Image.new("RGBA", (w + radius * 2, h + radius * 2), (0, 0, 0, 0))
    core = Image.new("RGBA", (w, h), (0, 0, 0, 180))
    core = core.filter(ImageFilter.GaussianBlur(radius // 2))
    layer.paste(core, (radius, radius), core)
    return layer


def _fit(img: Image.Image, max_w: int, max_h: int) -> Image.Image:
    scale = min(max_w / img.width, max_h / img.height)
    nw, nh = max(1, int(img.width * scale)), max(1, int(img.height * scale))
    return img.resize((nw, nh), Image.LANCZOS)


def _compose(app: Image.Image, canvas_w: int, canvas_h: int, margin: int) -> Image.Image:
    canvas = Image.new("RGB", (canvas_w, canvas_h), BG)
    fitted = _fit(app, canvas_w - margin * 2, canvas_h - margin * 2)
    shadow = _shadow(fitted.size)
    x = (canvas_w - fitted.width) // 2
    y = (canvas_h - fitted.height) // 2 + 8
    canvas.paste(shadow, (x - 18, y - 6), shadow)
    canvas.paste(fitted, (x, y))
    return canvas


def main() -> None:
    src = DOCS / "screenshot.png"
    if not src.exists():
        raise SystemExit(f"Missing {src} — run: python backup_v2.py --marketing-shot")

    app = Image.open(src).convert("RGB")
    DOCS.mkdir(parents=True, exist_ok=True)
    _compose(app, 1280, 720, margin=72).save(DOCS / "gumroad-cover.png", optimize=True)
    _compose(app, 1200, 1200, margin=96).save(DOCS / "gumroad-thumbnail.png", optimize=True)

    desktop = Path.home() / "Desktop" / "PythonBackUp-Gumroad-images"
    desktop.mkdir(exist_ok=True)
    import shutil

    for name in ("screenshot.png", "gumroad-cover.png", "gumroad-thumbnail.png"):
        shutil.copy2(DOCS / name, desktop / name)

    print(f"Wrote {DOCS / 'gumroad-cover.png'}")
    print(f"Wrote {DOCS / 'gumroad-thumbnail.png'}")
    print(f"Copied to {desktop}")


if __name__ == "__main__":
    main()
