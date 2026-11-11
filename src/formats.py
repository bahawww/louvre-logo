#!/usr/bin/env python3
"""Lockup SVG -> PNG (2400w) + lossless WebP + JPG (flat bg) + PDF. Run: .venv/bin/python src/formats.py"""
import glob, os, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render import render, pdf
A = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "site", "assets")
for svg in sorted(glob.glob(A + "/lockup/lockup-*.svg")):
    base = svg[:-4]; bg = "#0D0D0D" if base.endswith("white") else "#FFFFFF"
    render(svg, base + ".png", 2400)
    im = Image.open(base + ".png").convert("RGBA"); im.save(base + ".png", optimize=True)
    im.save(base + ".webp", "WEBP", lossless=True, quality=100, method=6)
    flat = Image.new("RGB", im.size, bg); flat.paste(im, mask=im.split()[3]); flat.save(base + ".jpg", "JPEG", quality=92, subsampling=0, optimize=True)
    pdf(svg, base + ".pdf"); print("ok", os.path.basename(base), im.size, im.getextrema()[3])
