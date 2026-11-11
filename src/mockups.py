#!/usr/bin/env python3
"""Swap the lockup nested in each mockup SVG for the current lockup, then render PNG/JPG/WebP.
Keeps the rendered height (so the symbol keeps its size); left-aligned placements keep x, the rest keep their centre.
Run: .venv/bin/python src/mockups.py"""
import glob, os, re, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render import render
A = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "site", "assets")
LEFT = ("5-dashboard", "6-business-card")
NEST = re.compile(r'<svg x="([\d.]+)" y="([\d.]+)" width="([\d.]+)" height="([\d.]+)" viewBox="0 0 [\d.]+ [\d.]+">(.*?)</svg>', re.S)

def lock_parts(variant):
    t = open(f"{A}/lockup/lockup-{variant}.svg").read()
    vb = re.search(r'viewBox="([^"]+)"', t).group(1); vw, vh = map(float, vb.split()[2:])
    return vb, vw, vh, re.search(r"</title>(.*)</svg>", t, re.S).group(1)

for svg in sorted(glob.glob(A + "/mockups/*.svg")):
    name = os.path.basename(svg)[:-4]; t = open(svg).read(); n = 0
    def swap(m):
        global n
        x, y, w, h, inner = float(m[1]), float(m[2]), float(m[3]), float(m[4]), m[5]
        fill = re.findall(r'fill="(#[0-9A-Fa-f]+)"', inner)[-1].upper()   # wordmark colour picks the variant
        variant = "white" if fill == "#FFFFFF" else ("color" if re.findall(r'fill="(#[0-9A-Fa-f]+)"', inner)[0].upper() == "#5D5D5D" else "ink")
        vb, vw, vh, new = lock_parts(variant); nw = h * vw / vh
        nx = x if name in LEFT else x + w / 2 - nw / 2
        n += 1
        return f'<svg x="{nx:.1f}" y="{y:.1f}" width="{nw:.1f}" height="{h:.1f}" viewBox="{vb}">{new}</svg>'
    t2 = NEST.sub(swap, t)
    if n:
        open(svg, "w").write(t2)
    png = svg[:-4] + ".png"; render(svg, png, 1200)
    im = Image.open(png).convert("RGB"); im.save(png, optimize=True)
    im.save(svg[:-4] + ".jpg", "JPEG", quality=92, optimize=True); im.save(svg[:-4] + ".webp", "WEBP", quality=90, method=6)
    print(name, "lockups swapped:", n, im.size)
