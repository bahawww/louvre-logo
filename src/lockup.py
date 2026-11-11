#!/usr/bin/env python3
"""Generates the Louvre lockup SVGs (symbol + wordmark) from Hanken Grotesk 700.
Run: .venv/bin/python src/lockup.py [--text LOUVRE --track 6 --no-kern --out DIR]
Output structure is relied on by build.py: viewBox, <title>, symbol <path>, wordmark <path>; height = 1.9 x cap height."""
import argparse, math, os
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, "..", "site", "assets", "font", "HankenGrotesk-Variable.ttf")
INK, GREY, WHITE = "#0D0D0D", "#5D5D5D", "#FFFFFF"
VARIANTS = (("color", GREY, INK), ("ink", INK, INK), ("white", WHITE, WHITE))

def advances(text, kern):
    """Per-glyph x advance in font units; with kern=True, HarfBuzz applies the font's own GPOS kerning."""
    if not kern:
        return None
    import uharfbuzz as hb
    blob = hb.Blob.from_file_path(FONT); face = hb.Face(blob); font = hb.Font(face)
    font.set_variations({"wght": 700})
    buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
    hb.shape(font, buf, {"kern": True, "liga": False})
    return [p.x_advance for p in buf.glyph_positions]

def word(f, text, track, kern):
    gs = f.getGlyphSet(); cm = f.getBestCmap(); k = 200 / f["head"].unitsPerEm
    adv = advances(text, kern)
    x = 0; d = []; y0, y1 = 1e9, -1e9
    for i, ch in enumerate(text):
        g = gs[cm[ord(ch)]]; pen = SVGPathPen(gs); g.draw(TransformPen(pen, (k, 0, 0, -k, x, 0))); d.append(pen.getCommands())
        bp = BoundsPen(gs); g.draw(bp)
        if bp.bounds: y0 = min(y0, -bp.bounds[3] * k); y1 = max(y1, -bp.bounds[1] * k)
        x += (adv[i] if adv else g.width) * k + track
    return " ".join(d), x - track, y0, y1

def pyramid(hw, H, gap):
    a = 2 * hw / 3; h = H / 3
    P = lambda r, c: ((c - r / 2) * a, r * h)
    tris = [(P(r, c), P(r + 1, c), P(r + 1, c + 1)) for r in range(3) for c in range(r + 1)] + \
           [(P(r, c), P(r, c + 1), P(r + 1, c + 1)) for r in (1, 2) for c in range(r)]
    rin = a / (2 * math.sqrt(3)); s = (rin - gap / 2) / rin; out = ""
    for t in tris:
        cx = sum(p[0] for p in t) / 3; cy = sum(p[1] for p in t) / 3
        out += "M" + "L".join(f"{cx + (x - cx) * s:.2f},{cy + (y - cy) * s:.2f}" for x, y in t) + "Z"
    return out

def lockup(f, text, track, kern, symc, txtc):
    d, w, y0, y1 = word(f, text, track, kern); C = y1 - y0
    SH = C * 1.3; hw = SH / 146 * 84; PW = 2 * hw; gap = C * 0.42; pad = C * 0.3
    pyr = pyramid(hw, SH, gap=SH * 0.034)
    cyc = (y0 + y1) / 2
    W = PW + gap + w + 2 * pad; Ht = SH + 2 * pad
    tx = pad + PW + gap; ty = pad + SH / 2 - cyc
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {Ht:.0f}"><title>Louvre</title>'
            f'<path fill="{symc}" transform="translate({pad + hw:.2f},{pad:.2f})" d="{pyr}"/>'
            f'<path fill="{txtc}" transform="translate({tx:.2f},{ty:.2f})" d="{d}"/></svg>\n')

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--text", default="Louvre"); ap.add_argument("--track", type=float, default=3)
    ap.add_argument("--no-kern", action="store_true"); ap.add_argument("--prefix", default="lockup")
    ap.add_argument("--out", default=os.path.join(HERE, "..", "site", "assets", "lockup"))
    a = ap.parse_args()
    f = instantiateVariableFont(TTFont(FONT), {"wght": 700})
    for v, sc, tc in VARIANTS:
        p = os.path.join(a.out, f"{a.prefix}-{v}.svg"); open(p, "w").write(lockup(f, a.text, a.track, not a.no_kern, sc, tc)); print(p)
