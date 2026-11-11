#!/usr/bin/env python3
"""Rebuilds assets/download/louvre-logo-kit.zip (lockup entries) and louvre-mockups.zip from the current assets.
Symbol/app-icon entries of the kit are carried over from the existing zip. Run: .venv/bin/python src/kits.py"""
import glob, io, os, re, zipfile
from PIL import Image
A = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "site", "assets"); D = A + "/download"

def png_bytes(im, quant):
    if quant: im = im.quantize(256, method=Image.Quantize.FASTOCTREE)
    b = io.BytesIO(); im.save(b, "PNG", optimize=True); return b.getvalue()
def jpg_bytes(path):
    b = io.BytesIO(); Image.open(path).save(b, "JPEG", quality=85, optimize=True, progressive=True); return b.getvalue()

# --- logo kit ---
old = zipfile.ZipFile(f"{D}/louvre-logo-kit.zip")
keep = [(i.filename, old.read(i)) for i in old.infolist() if not i.is_dir() and not re.search(r"(upper|lower|lockup)-", i.filename)]
new = []
for v in ("color", "ink", "white"):
    b = f"{A}/lockup/lockup-{v}"
    new += [(f"svg/lockup-{v}.svg", open(b + ".svg", "rb").read()), (f"pdf/lockup-{v}.pdf", open(b + ".pdf", "rb").read()),
            (f"jpg/lockup-{v}.jpg", jpg_bytes(b + ".jpg")), (f"webp/lockup-{v}.webp", open(b + ".webp", "rb").read())]
    src = Image.open(b + ".png").convert("RGBA")
    for w in (800, 1600, 2400):
        im = src if w == src.width else src.resize((w, round(src.height * w / src.width)), Image.LANCZOS)
        new.append((f"png/lockup-{v}-{w}w.png", png_bytes(im, True)))
tmp = f"{D}/louvre-logo-kit.zip.tmp"
with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for n, data in sorted(keep + new): z.writestr(n, data)
os.replace(tmp, f"{D}/louvre-logo-kit.zip")

# --- mockups ---
tmp = f"{D}/louvre-mockups.zip.tmp"
with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for f in sorted(glob.glob(A + "/mockups/*.*")):
        n, ext = os.path.basename(f), f.rsplit(".", 1)[1]
        data = png_bytes(Image.open(f), False) if ext == "png" else jpg_bytes(f) if ext == "jpg" else open(f, "rb").read()
        z.writestr(f"{ext}/{n}", data)
os.replace(tmp, f"{D}/louvre-mockups.zip")
for z in ("louvre-logo-kit.zip", "louvre-mockups.zip"): print(z, os.path.getsize(f"{D}/{z}"))
