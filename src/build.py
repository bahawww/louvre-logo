#!/usr/bin/env python3
"""Generates ~/louvre-icon/index.html and 404.html. Run: python3 ~/louvre-icon-src/build.py"""
import html, os, re
ROOT = os.environ.get("LOUVRE_ROOT", "/opt/louvre-logo/site"); A = ROOT + "/assets"
URL = "https://logo.louvre.my.id/"
def e(s): return html.escape(s, quote=True)
# lockup aspect ratio drives every <img> size, so a new wordmark never gets stretched
LK_W, LK_H = map(float, re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', open(A + "/lockup/lockup-ink.svg").read()).groups())
def lkh(w): return round(w * LK_H / LK_W)
def lkw(h): return round(h * LK_W / LK_H)
def T(tag, idt, en, attrs=""):
    return f'<{tag} data-en="{e(en)}"{(" " + attrs) if attrs else ""}>{idt}</{tag}>'
def dl(base, png=None, pdf=True, exts=("svg","png","jpg","webp","pdf")):
    out = []
    for x in exts:
        if x == "pdf" and not pdf: continue
        href = png if (x == "png" and png) else f"{base}.{x}"
        out.append(f'<a href="{href}" download>{x}</a>')
    return " · ".join(out)

# ---------- hero pyramid (9 triangles from the symbol path) ----------
PD = re.search(r' d="([^"]+)"', open(A + "/symbol/symbol-ink.svg").read()).group(1)
tris = ["M" + p for p in PD.split("M")[1:]]
order = [0, 1, 2, 3, 4, 5, 6, 7, 8]
hero_svg = '<svg class="pyr" viewBox="0 0 168 146" role="img" aria-label="Piramida Louvre">' + "".join(
    f'<path class="tri" style="--i:{i}" d="{t}"/>' for i, t in zip(order, tris)) + "</svg>"

# ---------- how-to-draw: construction grid + triangles revealed row by row ----------
_G = [("M84,0L0,146L168,146Z", 0, 0),                                   # step 0: outer triangle
      ("M56,48.67L112,48.67", 1, 0), ("M28,97.33L140,97.33", 1, 1),      # step 1: split each side in three
      ("M56,48.67L112,146", 1, 2), ("M28,97.33L56,146", 1, 3), ("M112,48.67L56,146", 1, 4), ("M140,97.33L112,146", 1, 5)]
_ROW = {0: (2, 0), 1: (3, 0), 6: (3, 1), 2: (3, 2), 3: (4, 0), 7: (4, 1), 4: (4, 2), 8: (4, 3), 5: (4, 4)}  # triangle -> (step, order in row)
draw_svg = ('<svg class="dw" id="draw" viewBox="-8 -8 184 162" role="img" aria-label="Cara menggambar logo Louvre">'
            + "".join(f'<path class="dg" data-s="{st}" style="--d:{k*90}ms" pathLength="1" d="{d}"/>' for d, st, k in _G)
            + "".join(f'<path class="dt" data-s="{_ROW[i][0]}" style="--d:{_ROW[i][1]*110}ms" d="{t}"/>' for i, t in enumerate(tris))
            + "</svg>")
draw_steps = [("Mulai dari satu segitiga besar.", "Start with one large triangle."),
              ("Bagi tiap sisi jadi tiga, lalu tarik garisnya. Terbentuk sembilan segitiga kecil.", "Split each side into three and join the marks. Nine small triangles appear."),
              ("Baris puncak: 1 segitiga.", "Top row: 1 triangle."),
              ("Baris tengah: 3 segitiga, yang tengah terbalik.", "Middle row: 3 triangles, the middle one upside down."),
              ("Baris dasar: 5 segitiga, berselang-seling.", "Bottom row: 5 triangles, alternating."),
              ("Hapus garis bantu. Celah tipis di antara segitiga adalah bagian dari logo.", "Remove the guides. The thin gaps are part of the logo.")]
draw_ol = "".join(f'<li><button type="button" data-i="{i}"><i>{i+1}</i>{T("span", a, b)}</button></li>' for i, (a, b) in enumerate(draw_steps))

# ---------- clear-space diagram ----------
lk = open(A + "/lockup/lockup-ink.svg").read()
vw, vh = map(float, re.search(r'viewBox="([^"]+)"', lk).group(1).split()[2:])
inner = re.search(r"</title>(.*)</svg>", lk, re.S).group(1)
C = vh / 1.9; pad = 0.3 * C; SH = 1.3 * C; x = SH / 3; Wt = vw - 2 * pad
DW, DH = Wt + 2 * x, SH + 2 * x; hw = SH * 84 / 146; cx = x + hw; k = 0.577 * x * 0.8
tri = lambda pts: '<polygon points="%s" fill="#D1D5DB"/>' % " ".join(f"{a:.1f},{b:.1f}" for a, b in pts)
cs = (f'<svg class="cs" viewBox="0 0 {DW:.0f} {DH:.0f}" role="img" aria-label="Diagram ruang aman: x sama dengan tinggi satu segitiga teratas">'
      f'<rect x="1" y="1" width="{DW-2:.0f}" height="{DH-2:.0f}" fill="none" stroke="#9AA0A6" stroke-width="1.5" stroke-dasharray="6 5"/>'
      f'<rect x="{x:.1f}" y="{x:.1f}" width="{Wt:.1f}" height="{SH:.1f}" fill="none" stroke="#D1D5DB" stroke-width="1"/>'
      + tri([(cx - k, x), (cx + k, x), (cx, 2)]) + tri([(cx - k, DH - x), (cx + k, DH - x), (cx, DH - 2)])
      + tri([(x, DH / 2 - k), (x, DH / 2 + k), (2, DH / 2)]) + tri([(DW - x, DH / 2 - k), (DW - x, DH / 2 + k), (DW - 2, DH / 2)])
      + f'<svg x="{x - pad:.1f}" y="{x - pad:.1f}" width="{vw:.1f}" height="{vh:.1f}" viewBox="0 0 {vw:.0f} {vh:.0f}">{inner}</svg>'
      + "".join(f'<text x="{a:.0f}" y="{b:.0f}" font-size="{x*0.42:.0f}" fill="#5D5D5D" text-anchor="middle" font-family="Hanken Grotesk,sans-serif" font-weight="600">x</text>'
                for a, b in ((cx + k + x * .35, x * .62), (cx + k + x * .35, DH - x * .38), (x * .5, DH / 2 - k - 6), (DW - x * .5, DH / 2 - k - 6)))
      + "</svg>")

# ---------- cards ----------
def cap(title_id, title_en, links, extra=""):
    return f'<div class="cap"><b data-en="{e(title_en)}">{title_id}</b><span>{links}</span></div>'
sym_cards = (
 f'<div class="card plate-l"><div class="art"><img src="assets/symbol/symbol-ink.svg" width="150" height="130" alt="Simbol Louvre, tinta"></div>{cap("Simbol · tinta","Symbol · ink",dl("assets/symbol/symbol-ink"))}</div>'
 f'<div class="card plate-d"><div class="art"><img src="assets/symbol/symbol-white.svg" width="150" height="130" alt="Simbol Louvre, putih"></div>{cap("Simbol · putih","Symbol · white",dl("assets/symbol/symbol-white"))}</div>'
 f'<div class="card"><div class="art tint"><img src="assets/symbol/app-icon-dark.svg" width="130" height="130" alt="Ikon aplikasi Louvre, gelap"></div>{cap("Ikon aplikasi · gelap","App icon · dark",dl("assets/symbol/app-icon-dark",png="assets/symbol/app-icon-dark-512.png"))}</div>'
 f'<div class="card"><div class="art tint"><img src="assets/symbol/app-icon-light.svg" width="130" height="130" alt="Ikon aplikasi Louvre, terang"></div>{cap("Ikon aplikasi · terang","App icon · light",dl("assets/symbol/app-icon-light",png="assets/symbol/app-icon-light-512.png"))}</div>'
 f'<div class="card"><div class="art tint"><div class="sizes"><img src="assets/symbol/app-icon-dark.svg" width="64" height="64" alt=""><img src="assets/symbol/app-icon-dark.svg" width="32" height="32" alt=""><img src="assets/symbol/app-icon-dark.svg" width="16" height="16" alt=""></div></div>'
 f'<div class="cap"><b data-en="Small sizes · 64 / 32 / 16 px">Ukuran kecil · 64 / 32 / 16 px</b><span><a href="assets/symbol/favicon.ico" download>favicon.ico</a> · <a href="assets/symbol/apple-touch-icon.png" download>apple-touch</a> · <a href="assets/symbol/maskable-512.png" download>maskable</a></span></div></div>')
lock_cards = ""
for v, nid, nen, kind in (("color", "dua nada", "two-tone", "l"), ("ink", "tinta", "ink", "l"), ("white", "putih", "white", "d")):
    lock_cards += (f'<div class="card plate-{kind}"><img src="assets/lockup/lockup-{v}.svg" width="296" height="{lkh(296)}" alt="Lockup Louvre, {nid}">'
                   f'{cap(f"Lockup · {nid}", f"Lockup · {nen}", dl(f"assets/lockup/lockup-{v}"))}</div>')
mock = [("1-tshirt","Kaos","T-shirt"),("2-app-icon","Ikon aplikasi","App icon"),("3-mug","Mug","Mug"),("8-tumbler","Tumbler","Tumbler"),
        ("4-tote","Tote bag","Tote bag"),("5-dashboard","Dasbor web","Web dashboard"),("6-business-card","Kartu nama","Business card"),("7-social","Profil sosial","Social profile")]
_V_unused = {"1-tshirt": "?v=2", "5-dashboard": "?v=2", "6-business-card": "?v=2", "7-social": "?v=2"}  # cache-bust regenerated mockups
from PIL import Image
for _n, _a, _b in mock:  # 600px WebP grid thumbnails, regenerated when the PNG is newer
    _src, _dst = f"{A}/mockups/{_n}.png", f"{A}/mockups/thumb/{_n}.webp"
    if not os.path.exists(_dst) or os.path.getmtime(_dst) < os.path.getmtime(_src):
        os.makedirs(os.path.dirname(_dst), exist_ok=True)
        Image.open(_src).convert("RGB").resize((600, 450), Image.LANCZOS).save(_dst, "WEBP", quality=80, method=6)
mock_html = "".join(
 f'<figure><a class="lb" href="assets/mockups/{n}.webp" data-dl="assets/mockups/{n}.png"><img src="assets/mockups/thumb/{n}.webp" srcset="assets/mockups/thumb/{n}.webp 600w, assets/mockups/{n}.webp 1200w" sizes="(max-width:700px) 100vw, 400px" alt="Mockup {a}" loading="lazy" decoding="async" width="1200" height="900"></a>'
 f'<figcaption><b data-en="{e(b)}">{a}</b><span>{dl(f"assets/mockups/{n}", exts=("svg","png","jpg","webp"))}</span></figcaption></figure>' for n, a, b in mock)
dont = [("scaleX(1.3)","Jangan diregangkan","Don't stretch",""),("rotate(-14deg)","Jangan diputar","Don't rotate",""),
        ("none","Jangan diwarnai","Don't recolour","filter:invert(.45) sepia(1) saturate(9) hue-rotate(-25deg)"),
        ("none","Jangan diberi efek","Don't add effects","filter:drop-shadow(5px 6px 3px rgba(0,0,0,.45))"),
        ("none","Jangan ditaruh di latar kontras rendah","Don't place on low-contrast backgrounds",""),
        ("skewX(-18deg)","Jangan dimiringkan","Don't skew",""),
        ("none","Jangan dipudarkan","Don't fade","opacity:.3"),
        ("none","Jangan diberi garis tepi","Don't add an outline","filter:drop-shadow(1.5px 0 0 #E11D48) drop-shadow(-1.5px 0 0 #E11D48) drop-shadow(0 1.5px 0 #E11D48) drop-shadow(0 -1.5px 0 #E11D48)")]
dont_html = ""
for i, (tf, a, b, flt) in enumerate(dont):
    bg = "#4A4A4A" if i == 4 else "#fff"
    dont_html += (f'<div class="dn"><div class="dnart" style="background:{bg}"><img src="assets/lockup/lockup-ink.svg" width="124" height="{lkh(124)}" alt="" style="transform:{tf};{flt}"></div>'
                  f'<div class="dncap"><span class="x" aria-hidden="true">✕</span><span data-en="{e(b)}">{a}</span></div></div>')
pal = [("Putih","White","#FFFFFF","#0D0D0D"),("Permukaan","Surface","#F4F4F4","#0D0D0D"),("Garis","Line","#E5E7EB","#0D0D0D"),("Teks 2","Text 2","#5D5D5D","#fff"),("Tinta","Ink","#0D0D0D","#fff")]
pal_rows = [("#FFFFFF","255 · 255 · 255","0 · 0 · 0 · 0","1,0 : 1"),("#F4F4F4","244 · 244 · 244","0 · 0 · 0 · 4","1,1 : 1"),("#E5E7EB","229 · 231 · 235","3 · 2 · 0 · 8","1,2 : 1"),("#5D5D5D","93 · 93 · 93","0 · 0 · 0 · 64","6,6 : 1"),("#0D0D0D","13 · 13 · 13","0 · 0 · 0 · 95","19,4 : 1")]
pal_tbl = ('<div class="tw"><table class="pt2"><thead><tr><th>HEX</th><th>RGB</th><th>CMYK*</th>'
           '<th data-en="Contrast on white">Kontras di atas putih</th></tr></thead><tbody>'
           + "".join(f'<tr><td>{a}</td><td><span class="tl">RGB</span>{b}</td><td><span class="tl">CMYK*</span>{c}</td>'
                     f'<td>{T("span","Kontras","Contrast",'class="tl"')}{d}</td></tr>' for a, b, c, d in pal_rows)
           + '</tbody></table></div>')
pal_html = "".join(f'<button type="button" class="sw" data-hex="{h}" style="background:{h};color:{c}"><span data-en="{e(en)}">{idn}</span><br>{h}</button>' for idn, en, h, c in pal)

# ---------- exporter: fixed variants (no recolouring), padding in units of x ----------
def _vb(path):
    return list(map(float, re.search(r'viewBox="([^"]+)"', open(A + "/" + path).read()).group(1).split()))
ex_vars = [("symbol/symbol-ink.svg", "Simbol · tinta", "Symbol · ink", "s"), ("symbol/symbol-white.svg", "Simbol · putih", "Symbol · white", "s"),
           ("symbol/app-icon-dark.svg", "Ikon aplikasi · gelap", "App icon · dark", "i"), ("symbol/app-icon-light.svg", "Ikon aplikasi · terang", "App icon · light", "i")]
for _v, _vi, _ve in (("color", "dua nada", "two-tone"), ("ink", "tinta", "ink"), ("white", "putih", "white")):
    ex_vars.append((f"lockup/lockup-{_v}.svg", f"Lockup · {_vi}", f"Lockup · {_ve}", "l"))
ex_opts = ""
for _path, _i, _en, _k in ex_vars:
    _w, _h = _vb(_path)[2:]
    if _k == "s":   _x, _pad, _min = _h / 3, 0, 24          # x = top triangle ≈ symbol height / 3
    elif _k == "i": _x, _pad, _min = _h / 6, 0, 16
    else:           _C = _h / 1.9; _x, _pad, _min = 1.3 * _C / 3, 0.3 * _C, 96   # same geometry as the clear-space diagram
    ex_opts += (f'<option value="{os.path.basename(_path)[:-4]}" data-src="assets/{_path}" data-x="{_x:.2f}" data-pad="{_pad:.2f}" '
                f'data-min="{_min}" data-kind="{_k}" data-en="{e(_en)}">{_i}</option>')
EX_HTML = f"""<section id="ekspor">{T("h2","Ekspor & uji latar","Export & background test")}{T("p","Pilih versi, ukuran, dan latar, lalu unduh. Kontras dicek otomatis terhadap latar yang dipilih.","Pick a version, size and background, then download. Contrast is checked against the chosen background.",'class="lead"')}
<div class="ex"><form class="exf" onsubmit="return false">
<label class="fl"><span data-en="Version">Versi</span><select id="ex-v">{ex_opts}</select></label>
<label class="fl"><span data-en="Logo width (px)">Lebar logo (px)</span><input id="ex-w" type="number" inputmode="numeric" min="16" max="4096" step="1" value="1024"></label>
<label class="fl"><span data-en="Clear space (× x)">Ruang aman (× x)</span><span class="rg"><input id="ex-p" type="range" min="1" max="4" step="0.5" value="1"><output id="ex-po">1×</output></span></label>
<fieldset class="fl"><legend data-en="Background">Latar</legend><div class="chips">
<label><input type="radio" name="ex-bg" value="none" checked><span data-en="Transparent">Transparan</span></label>
<label><input type="radio" name="ex-bg" value="#FFFFFF"><span data-en="White">Putih</span></label>
<label><input type="radio" name="ex-bg" value="#0D0D0D"><span data-en="Ink">Tinta</span></label>
<label><input type="radio" name="ex-bg" value="custom"><span data-en="Colour">Warna</span><input id="ex-c" type="color" value="#2F5D8C" aria-label="Warna latar"></label>
<label><input type="radio" name="ex-bg" value="photo"><span data-en="Photo">Foto</span></label></div>
<input id="ex-f" type="file" accept="image/*" hidden></fieldset>
<fieldset class="fl"><legend data-en="Format">Format</legend><div class="chips">
<label><input type="radio" name="ex-fmt" value="png" checked><span>PNG</span></label><label><input type="radio" name="ex-fmt" value="jpg"><span>JPG</span></label>
<label><input type="radio" name="ex-fmt" value="webp"><span>WebP</span></label><label><input type="radio" name="ex-fmt" value="svg"><span>SVG</span></label></div></fieldset>
</form>
<div class="exp"><div class="exc" id="ex-box"><canvas id="ex-cv" width="600" height="300" role="img" aria-label="Pratinjau ekspor"></canvas></div>
<p class="exk" id="ex-k" aria-live="polite"></p><div class="exa"><button type="button" class="btn" id="ex-d" data-en="Download">Unduh</button><p class="exn" id="ex-n" aria-live="polite"></p></div></div></div></section>
"""

CSS = r"""
@font-face{font-family:"Hanken Grotesk";src:url(assets/font/HankenGrotesk-Variable.woff2) format("woff2"),url(assets/font/HankenGrotesk-Variable.ttf) format("truetype");font-weight:100 900;font-display:swap}
:root{--bg:#fff;--surface:#fff;--s2:#F4F4F4;--line:#E5E7EB;--text:#0D0D0D;--t2:#5D5D5D}
:root[data-theme=dark]{--bg:#000;--surface:#0A0A0A;--s2:#1A1A1A;--line:#262626;--text:#fff;--t2:#A3A3A3;color-scheme:dark}
:root[data-theme=light]{color-scheme:light}
@media(prefers-color-scheme:dark){:root:not([data-theme]){--bg:#000;--surface:#0A0A0A;--s2:#1A1A1A;--line:#262626;--text:#fff;--t2:#A3A3A3;color-scheme:dark}}
*{box-sizing:border-box}html{scroll-behavior:smooth}@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
body{margin:0;background:var(--bg);color:var(--text);font:16px/1.6 "Hanken Grotesk",system-ui,-apple-system,"Segoe UI",sans-serif;-webkit-font-smoothing:antialiased}
a{color:inherit}.wrap{max-width:1080px;margin:0 auto;padding:0 20px}
::-webkit-scrollbar{width:10px;height:10px;background:transparent}
::-webkit-scrollbar-track,::-webkit-scrollbar-corner{background:transparent}
::-webkit-scrollbar-button{display:none;width:0;height:0}
::-webkit-scrollbar-thumb{background:color-mix(in srgb,var(--text) 32%,transparent);border-radius:999px;border:3px solid transparent;background-clip:padding-box}
::-webkit-scrollbar-thumb:hover{background:color-mix(in srgb,var(--text) 55%,transparent);background-clip:padding-box}
@supports (-moz-appearance:none){*{scrollbar-width:thin;scrollbar-color:color-mix(in srgb,var(--text) 32%,transparent) transparent}}
::view-transition-old(root),::view-transition-new(root){animation-duration:.4s;animation-timing-function:cubic-bezier(.4,0,.2,1)}
html.tx *,html.tx *::before,html.tx *::after{transition:background-color .38s ease,color .38s ease,border-color .38s ease,fill .38s ease,stroke .38s ease!important}
[data-en]{transition:opacity .17s ease}html.fade [data-en]{opacity:0}
.skip{position:absolute;left:-999px;top:8px;background:var(--text);color:var(--bg);padding:8px 14px;border-radius:999px;z-index:20}.skip:focus{left:12px}
header{position:sticky;top:0;background:color-mix(in srgb,var(--bg) 88%,transparent);backdrop-filter:blur(10px);border-bottom:1px solid var(--line);z-index:5}
header .wrap{display:flex;align-items:center;gap:12px;height:60px}header img{height:24px;width:auto;display:block}header .logo-d{display:none}
:root[data-theme=dark] header .logo-l{display:none}:root[data-theme=dark] header .logo-d{display:block}
@media(prefers-color-scheme:dark){:root:not([data-theme]) header .logo-l{display:none}:root:not([data-theme]) header .logo-d{display:block}}
nav{margin-left:auto;display:flex;gap:2px;overflow-x:auto;scrollbar-width:none}nav a{text-decoration:none;color:var(--t2);padding:6px 12px;border-radius:999px;font-size:14px;white-space:nowrap}nav a:hover{background:var(--s2);color:var(--text)}nav a[aria-current=true]{background:var(--s2);color:var(--text)}
.tg{display:flex;border:1px solid var(--line);border-radius:999px;padding:2px;gap:2px;flex:none}.tg button{font:inherit;font-size:13px;border:0;background:none;color:var(--t2);padding:4px 10px;border-radius:999px;cursor:pointer}.tg button:hover{color:var(--text)}.tg button[aria-pressed=true]{background:var(--s2);color:var(--text);font-weight:600}
:focus-visible{outline:2px solid var(--text);outline-offset:2px}
.hero{display:grid;grid-template-columns:1.3fr .7fr;gap:32px;align-items:center;padding:64px 0 24px}
h1{font-size:clamp(34px,5.4vw,54px);line-height:1.05;font-weight:600;letter-spacing:-.035em;margin:0 0 14px}.hero p{color:var(--t2);margin:0;max-width:52ch;font-size:17px}
.btn{display:inline-block;background:var(--text);color:var(--bg);text-decoration:none;border-radius:999px;padding:10px 20px;font-weight:600;font-size:14px;border:1px solid var(--text);cursor:pointer;font-family:inherit}.btn.o{background:none;color:var(--text);border-color:var(--line)}.btn.o:hover{background:var(--s2)}
.acts{display:flex;gap:10px;flex-wrap:wrap}.hero .acts{margin-top:24px}
.pyr{width:100%;max-width:340px;justify-self:center;fill:var(--text);display:block}.tri{opacity:0;animation:tri .7s cubic-bezier(.2,.7,.2,1) forwards;animation-delay:calc(var(--i)*90ms + 150ms);transform-box:fill-box;transform-origin:center}
@keyframes tri{from{opacity:0;transform:translateY(10px) scale(.92)}to{opacity:1;transform:none}}@media(prefers-reduced-motion:reduce){.tri{animation:none;opacity:1}}
section{padding:56px 0 8px;scroll-margin-top:64px}section:focus,main:focus{outline:none}h2{font-size:clamp(24px,3.4vw,32px);font-weight:600;letter-spacing:-.025em;margin:0 0 6px;line-height:1.2}h3{font-size:17px;font-weight:600;margin:28px 0 4px}.lead{color:var(--t2);margin:0 0 22px;max-width:66ch}
.grid{display:grid;gap:16px;grid-template-columns:repeat(auto-fill,minmax(300px,1fr))}.grid.two{grid-template-columns:repeat(auto-fill,minmax(240px,1fr))}.grid.dn5{grid-template-columns:repeat(auto-fill,minmax(190px,1fr))}
.pts{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(250px,1fr))}.pt{border:1px solid var(--line);border-radius:16px;padding:22px;background:var(--surface)}.pt b{display:block;font-size:17px;margin-bottom:6px}.pt span{color:var(--t2);font-size:15px}.pt i{font-style:normal;display:inline-grid;place-items:center;width:28px;height:28px;border-radius:50%;background:var(--text);color:var(--bg);font-size:13px;font-weight:700;margin-bottom:12px}
.card{border:1px solid var(--line);border-radius:16px;overflow:hidden;background:var(--surface);display:flex;flex-direction:column}
.plate-l{--p:#fff}.plate-d{--p:#0D0D0D}.card .art{background:var(--p);display:flex;align-items:center;justify-content:center;padding:28px 20px;min-height:170px}.card .art.tint{background:var(--s2)}.card>img{background:var(--p);padding:28px 24px;width:100%;display:block;height:auto}
.cap{display:flex;flex-wrap:wrap;justify-content:space-between;gap:4px 8px;padding:12px 16px;font-size:13px;border-top:1px solid var(--line);color:var(--t2)}.cap b{color:var(--text);font-weight:600}.cap a,.cap button.cp{color:var(--t2)}.cap a:hover,.cap button.cp:hover{color:var(--text)}
button.cp{font:inherit;font-size:13px;background:none;border:0;padding:0;cursor:pointer;text-decoration:underline}
.sizes{display:flex;gap:18px;align-items:flex-end}
.gd{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(300px,1fr))}.gd .card .art{min-height:0;padding:24px}.cs{width:100%;max-width:420px;height:auto;display:block}
.ms{display:flex;gap:28px;align-items:flex-end;flex-wrap:wrap;justify-content:center}.ms figure{margin:0;display:grid;gap:8px;justify-items:center;border:0;background:none;font-size:12px;color:#5D5D5D}
.dn{border:1px solid var(--line);border-radius:14px;overflow:hidden;background:var(--surface)}.dnart{height:110px;display:grid;place-items:center;overflow:hidden}.dncap{display:flex;gap:8px;align-items:flex-start;padding:10px 12px;font-size:13px;border-top:1px solid var(--line)}.x{display:inline-grid;place-items:center;flex:none;width:18px;height:18px;border-radius:50%;background:var(--text);color:var(--bg);font-size:10px}
figure.m,.mk figure{margin:0}.mk{display:grid;gap:16px;grid-template-columns:repeat(auto-fill,minmax(300px,1fr))}.mk figure{border:1px solid var(--line);border-radius:16px;overflow:hidden;background:var(--s2)}.mk figure img{display:block;width:100%;height:auto}.mk a.lb{display:block;cursor:zoom-in}
.mk figcaption{display:flex;flex-wrap:wrap;justify-content:space-between;gap:4px 8px;padding:12px 16px;background:var(--surface);font-size:13px;color:var(--t2);border-top:1px solid var(--line)}.mk figcaption b{color:var(--text)}
.spec{padding:28px 24px;display:grid;gap:12px}.spec .big{font:700 clamp(40px,9vw,84px)/1 "Hanken Grotesk",sans-serif;letter-spacing:.03em}.spec .pang{display:grid;gap:4px;font-size:clamp(20px,3.4vw,30px);line-height:1.25;letter-spacing:-.01em}.spec .row{font-size:20px;display:flex;flex-wrap:wrap;gap:6px 22px}.spec .row span{white-space:nowrap}
.card .acts{padding:0 24px 24px}.spec>*{min-width:0}.spec .row span{overflow-wrap:anywhere}.spec .row span[style*="font-weight"]{white-space:nowrap}.spec .row span:not([style]){white-space:normal}
.pal{display:flex;border:1px solid var(--line);border-radius:12px;overflow:hidden}.sw{flex:1;border:0;font:inherit;text-align:left;padding:34px 12px 10px;font-size:12px;line-height:1.4;cursor:pointer;min-width:0}.sw:hover{filter:brightness(.95)}
.tw{overflow-x:auto;margin-top:16px}.pt2{border-collapse:collapse;width:100%;font-size:13px;font-variant-numeric:tabular-nums}.pt2 th,.pt2 td{text-align:left;padding:8px 12px;border-bottom:1px solid var(--line);white-space:nowrap}.pt2 th{color:var(--t2);font-weight:600}
.hint{font-size:13px;color:var(--t2);margin:8px 0 0}
footer{margin-top:64px;border-top:1px solid var(--line);padding:24px 0 56px;color:var(--t2);font-size:13px}footer .wrap{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}
dialog{border:0;padding:0;background:transparent;max-width:min(96vw,1100px);width:100%;color:#fff}dialog::backdrop{background:rgba(0,0,0,.82)}
.lbx{display:grid;gap:10px;justify-items:center}.lbx img{max-width:100%;max-height:76vh;border-radius:12px;background:#fff;display:block}.lbc{font-size:14px;display:flex;gap:14px;align-items:center;flex-wrap:wrap;justify-content:center}.lbc a{color:#fff}
.lbb{position:fixed;top:50%;translate:0 -50%;width:44px;height:44px;border-radius:50%;border:0;background:rgba(255,255,255,.92);color:#000;font-size:20px;cursor:pointer}.lbb.p{left:12px}.lbb.n{right:12px}.lbb.c{top:16px;right:16px;translate:none}
.drw{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:28px;align-items:center}@media(max-width:760px){.drw{grid-template-columns:1fr}}
.drs{border:1px solid var(--line);border-radius:16px;background:var(--surface);padding:28px;display:grid;place-items:center}
.dw{width:100%;max-width:320px;height:auto;overflow:visible}
.dg{fill:none;stroke:var(--t2);stroke-width:.6;stroke-dasharray:1;stroke-dashoffset:1;transition:stroke-dashoffset .7s ease var(--d),opacity .5s ease}
.dg.in{stroke-dashoffset:0}.dw.clean .dg{opacity:0}
.dt{fill:var(--text);opacity:0;transform:scale(.35);transform-box:fill-box;transform-origin:center;transition:opacity .35s ease var(--d),transform .45s cubic-bezier(.3,1.4,.5,1) var(--d)}
.dt.in{opacity:1;transform:none}.dw:not(.clean) .dt.in{fill:color-mix(in srgb,var(--text) 88%,transparent)}
.dsl{list-style:none;margin:0 0 16px;padding:0;display:grid;gap:4px}
.dsl button{display:flex;gap:12px;align-items:flex-start;width:100%;text-align:left;font:inherit;font-size:14px;color:var(--t2);background:none;border:0;border-radius:10px;padding:8px 10px;cursor:pointer}
.dsl button:hover{background:var(--s2)}.dsl i{font-style:normal;font-weight:600;font-size:12px;min-width:22px;height:22px;border-radius:50%;display:grid;place-items:center;border:1px solid var(--line);flex:none}
.dsl li.done button{color:var(--text)}.dsl li.on button{color:var(--text);background:var(--s2)}.dsl li.on i,.dsl li.done i{background:var(--text);color:var(--bg);border-color:var(--text)}
.dct{display:flex;gap:8px}.dct .btn{padding:8px 16px}
@media(prefers-reduced-motion:reduce){.dg,.dt{transition:none}}
.ex{display:grid;grid-template-columns:minmax(0,340px) minmax(0,1fr);gap:24px;align-items:start}@media(max-width:760px){.ex{grid-template-columns:1fr}}
.exf{display:grid;gap:16px}.fl{display:grid;gap:6px;font-size:13px;color:var(--t2);border:0;margin:0;padding:0;min-width:0}.fl legend{padding:0;margin-bottom:6px}
.fl select,.fl input[type=number]{font:inherit;font-size:14px;color:var(--text);background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:9px 10px;width:100%}
.rg{display:flex;align-items:center;gap:10px}.rg input{flex:1;accent-color:var(--text)}.rg output{min-width:3ch;color:var(--text);font-variant-numeric:tabular-nums}
.chips{display:flex;flex-wrap:wrap;gap:6px}.chips label{display:inline-flex;align-items:center;gap:6px;border:1px solid var(--line);border-radius:999px;padding:5px 12px;font-size:13px;color:var(--text);cursor:pointer}
.chips input[type=radio]{position:absolute;opacity:0;width:1px;height:1px}.chips label:has(input:checked){background:var(--text);color:var(--bg);border-color:var(--text)}.chips label:has(input:focus-visible){outline:2px solid var(--text);outline-offset:2px}
.chips label:has(input:disabled){opacity:.4;cursor:not-allowed}.chips input[type=color]{width:20px;height:20px;border:0;padding:0;background:none;border-radius:50%;cursor:pointer}
.exa{display:flex;align-items:center;gap:14px;flex-wrap:wrap}.exn{margin:0;font-size:13px;color:var(--t2);font-variant-numeric:tabular-nums}.exn b{color:var(--text)}
.exp{display:grid;gap:10px}.exc{border:1px solid var(--line);border-radius:16px;min-height:260px;display:grid;place-items:center;padding:20px;
background:conic-gradient(var(--s2) 25%,var(--surface) 0 50%,var(--s2) 0 75%,var(--surface) 0) 0 0/20px 20px}
.exc canvas{max-width:100%;max-height:380px;height:auto;display:block;box-shadow:0 0 0 1px var(--line)}
.exk{margin:0;font-size:13px;display:flex;gap:8px;align-items:center;flex-wrap:wrap}.exk .tag{font-weight:600;border-radius:999px;padding:2px 10px;font-size:12px}
.exk .ok{background:#E7F5EC;color:#14532D}.exk .bad{background:#FDECEC;color:#7F1D1D}
.tl{display:none}
@media (max-width:760px),(pointer:coarse){
.cap,.mk figcaption{flex-direction:column;align-items:flex-start;gap:8px}
.cap span,.mk figcaption span{display:flex;flex-wrap:wrap;gap:6px;font-size:0}
.cap span a,.cap button.cp,.mk figcaption span a{font-size:13px;display:inline-flex;align-items:center;min-height:32px;padding:0 12px;border:1px solid var(--line);border-radius:999px;text-decoration:none;color:var(--text)}
.tg button{min-height:36px;min-width:36px}.chips label{min-height:36px}.rg input{height:32px}
.fl select,.fl input[type=number]{font-size:16px}}
@media(max-width:760px){.grid.dn5{grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}.dnart{height:84px}.dnart img{max-width:78%;height:auto}.dncap{font-size:12px;padding:8px 10px}.pal{flex-direction:column}.sw{display:flex;justify-content:space-between;align-items:center;padding:14px 16px;font-size:13px}.sw br{display:none}.pt2 thead{display:none}.pt2,.pt2 tbody,.pt2 tr,.pt2 td{display:block}.pt2 tr{display:grid;grid-template-columns:minmax(0,1.35fr) minmax(0,1fr) minmax(0,.8fr);font-size:13px;gap:4px 12px;padding:12px 0;border-bottom:1px solid var(--line)}.pt2 td{padding:0;border:0;white-space:nowrap}.pt2 td:first-child{grid-column:1/-1;font-weight:600}.tl{display:block;font-size:11px;color:var(--t2)}}
@media(max-width:359px){header img{height:20px}header .wrap>a{display:flex;align-items:center;min-height:36px}.tg button{min-width:32px;min-height:34px;padding:4px 8px}body header .wrap{gap:8px 6px;padding-left:12px;padding-right:12px}}
.vh{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap}
.totop{position:fixed;right:max(16px,env(safe-area-inset-right));bottom:max(16px,env(safe-area-inset-bottom));width:44px;height:44px;border-radius:50%;display:grid;place-items:center;background:var(--text);color:var(--bg);box-shadow:0 4px 14px rgba(0,0,0,.18);opacity:0;visibility:hidden;translate:0 12px;transition:opacity .2s,translate .2s,visibility .2s;z-index:6}.totop.on{opacity:1;visibility:visible;translate:0 0}.totop:hover{filter:brightness(1.2)}@media(prefers-reduced-motion:reduce){.totop{transition:none}}
.toast{position:fixed;left:50%;bottom:24px;translate:-50% 20px;background:var(--text);color:var(--bg);padding:10px 18px;border-radius:999px;font-size:14px;font-weight:600;opacity:0;pointer-events:none;transition:.25s;z-index:30}.toast.on{opacity:1;translate:-50% 0}
@media(max-width:760px){section{scroll-margin-top:104px}.hero{grid-template-columns:1fr;padding-top:36px}.pyr{max-width:220px;justify-self:center;order:-1}.hero{text-align:center}.hero p{margin-inline:auto}.hero .acts{justify-content:center}header .wrap{flex-wrap:wrap;height:auto;padding:8px 16px 0;gap:8px 8px}nav{order:3;width:calc(100% + 16px);margin:0 -16px 0 -10px;padding-right:24px;-webkit-mask-image:linear-gradient(90deg,#000 calc(100% - 28px),transparent);mask-image:linear-gradient(90deg,#000 calc(100% - 28px),transparent)}nav a{padding:8px 10px;font-size:14px}.tg.l{margin-left:auto}}
@media(max-width:560px){.tg.t button{font-size:0;padding:4px 10px;min-width:34px}.tg.t button::before{font-size:13px}.tg.t button[data-t=auto]::before{content:"A"}.tg.t button[data-t=light]::before{content:"\2600"}.tg.t button[data-t=dark]::before{content:"\263E"}}
@media(max-width:400px){.grid,.mk,.gd{grid-template-columns:1fr}}
"""

JS = r"""
(function(){
var r=document.documentElement,$=function(s,c){return(c||document).querySelector(s)},$$=function(s,c){return Array.prototype.slice.call((c||document).querySelectorAll(s))};
var lang=r.lang==="en"?"en":"id";try{if(lang==="id"&&localStorage.getItem("lang")==="en")lang="en"}catch(e){}
var L={id:{dPlay:"Putar",dPause:"Jeda",dAgain:"Ulangi",dPrev:"Langkah sebelumnya",dNext:"Langkah berikutnya",dAria:"Cara menggambar logo Louvre",exOut:"Hasil",exMin:"Minimum untuk versi ini",exUseIcon:"Di bawah itu, pakai ikon aplikasi.",exCap:"Dibatasi 4096 px",exOk:"Baik",exBad:"Kurang",exCR:"Kontras",exEst:"perkiraan, rata-rata di bawah logo",exTr:"Latar transparan: cek kontras di tempat logo akan dipasang.",exIcon:"Ikon aplikasi punya latar sendiri, jadi aman di latar apa pun.",exTry:"Coba versi",exInk:"tinta",exWhite:"putih",exVer:"",exPick:"Pilih foto",exSvgPhoto:"SVG tidak bisa memuat foto.",exErr:"Gagal memuat logo",exImg:"Gagal membaca gambar",copySvg:"Salin SVG",copied:"Disalin",fail:"Gagal menyalin",dl:"Unduh",close:"Tutup",prev:"Sebelumnya",next:"Berikutnya",open:"Buka ukuran penuh"},
en:{dPlay:"Play",dPause:"Pause",dAgain:"Replay",dPrev:"Previous step",dNext:"Next step",dAria:"How to draw the Louvre logo",exOut:"Output",exMin:"Minimum for this version",exUseIcon:"Below that, use the app icon.",exCap:"Capped at 4096 px",exOk:"Good",exBad:"Too low",exCR:"Contrast",exEst:"estimate, average under the logo",exTr:"Transparent background: check contrast where it will be placed.",exIcon:"The app icon has its own tile, so any background works.",exTry:"Try the",exInk:"ink",exWhite:"white",exVer:"version",exPick:"Choose a photo",exSvgPhoto:"SVG cannot contain a photo.",exErr:"Could not load the logo",exImg:"Could not read the image",copySvg:"Copy SVG",copied:"Copied",fail:"Copy failed",dl:"Download",close:"Close",prev:"Previous",next:"Next",open:"Open full size"}};
var translatable=$$("[data-en]");translatable.forEach(function(el){if(!el.dataset.id)el.dataset.id=el.innerHTML});
var toast=$(".toast"),tt;function say(m){toast.textContent=m;toast.classList.add("on");clearTimeout(tt);tt=setTimeout(function(){toast.classList.remove("on")},1600)}
function labels(){$$(".cap a[download],.mk figcaption a[download]").forEach(function(a){var b=a.parentNode.parentNode.querySelector("b");a.setAttribute("aria-label",L[lang].dl+" "+(b?b.textContent:"")+" ("+a.textContent+")")});
$$("button.cp").forEach(function(b){b.textContent=L[lang].copySvg});$$("a.lb").forEach(function(a){a.setAttribute("aria-label",L[lang].open+": "+(a.querySelector("img").alt))})}
function setLang(l,save){lang=l;r.lang=l;if(typeof exText==="function")setTimeout(exText,0);if(typeof dLabel==="function")setTimeout(dLabel,0);var u=(l==="en"?"/en/":"/")+location.hash;if(location.pathname!==(l==="en"?"/en/":"/"))try{history.replaceState(null,"",u)}catch(e){}document.title=l==="en"?"Louvre — Visual identity":"Louvre — Identitas"+" visual";translatable.forEach(function(el){el.innerHTML=l==="en"?el.dataset.en:el.dataset.id});
$$(".tg.l button").forEach(function(b){b.setAttribute("aria-pressed",b.dataset.l===l)});labels();if(save){try{localStorage.setItem("lang",l)}catch(e){}}}
/* smooth: cross-fade the whole page via View Transitions; fallbacks: colour transition (theme) / text fade (language); none under reduced motion */
function smooth(kind,apply){if(matchMedia("(prefers-reduced-motion:reduce)").matches){apply();return}
if(document.startViewTransition){document.startViewTransition(apply);return}
if(kind==="theme"){r.classList.add("tx");apply();setTimeout(function(){r.classList.remove("tx")},420)}
else{r.classList.add("fade");setTimeout(function(){apply();r.classList.remove("fade")},170)}}
$$(".tg.l button").forEach(function(b){b.addEventListener("click",function(){if(b.dataset.l===lang)return;smooth("lang",function(){setLang(b.dataset.l,true)})})});
/* theme */
var tb=$$(".tg.t button");function paint(){var c=r.dataset.theme||"auto";tb.forEach(function(x){x.setAttribute("aria-pressed",x.dataset.t===c)})}
tb.forEach(function(x){x.addEventListener("click",function(){var t=x.dataset.t;if(t===(r.dataset.theme||"auto"))return;smooth("theme",function(){if(t==="auto")delete r.dataset.theme;else r.dataset.theme=t;try{t==="auto"?localStorage.removeItem("theme"):localStorage.setItem("theme",t)}catch(e){}paint()})})});paint();
/* copy svg */
$$(".card .cap").forEach(function(c){var a=c.querySelector('a[href$=".svg"]');if(!a)return;var s=c.querySelector("span");s.appendChild(document.createTextNode(" · "));var b=document.createElement("button");b.type="button";b.className="cp";b.dataset.svg=a.getAttribute("href");s.appendChild(b)});
document.addEventListener("click",function(ev){var b=ev.target.closest("button.cp");if(!b)return;fetch(b.dataset.svg).then(function(x){return x.text()}).then(function(t){return navigator.clipboard.writeText(t)}).then(function(){say(L[lang].copied)},function(){say(L[lang].fail)})});
/* copy hex */
$$(".sw").forEach(function(s){s.addEventListener("click",function(){navigator.clipboard.writeText(s.dataset.hex).then(function(){say(L[lang].copied+" "+s.dataset.hex)},function(){say(L[lang].fail)})})});
/* lightbox */
var dlg=$("#lb"),li=$("#lb img"),lc=$("#lb .lbn"),lk=$$("a.lb"),idx=0;
function show(i){idx=(i+lk.length)%lk.length;var a=lk[idx],f=a.closest("figure"),t=f.querySelector("b").textContent;li.src=a.getAttribute("href");li.alt=a.querySelector("img").alt;lc.textContent=t;$("#lb .lbd").href=a.dataset.dl||a.getAttribute("href")}
lk.forEach(function(a,i){a.addEventListener("click",function(ev){ev.preventDefault();show(i);if(dlg.showModal)dlg.showModal();else dlg.setAttribute("open","")})});
$("#lb .p").addEventListener("click",function(){show(idx-1)});$("#lb .n").addEventListener("click",function(){show(idx+1)});$("#lb .c").addEventListener("click",function(){dlg.close()});
dlg.addEventListener("click",function(ev){if(ev.target===dlg)dlg.close()});
dlg.addEventListener("keydown",function(ev){if(ev.key==="ArrowLeft")show(idx-1);if(ev.key==="ArrowRight")show(idx+1)});
/* in-page links scroll without writing #hash into the address bar */
var rm=matchMedia("(prefers-reduced-motion:reduce)");
document.addEventListener("click",function(ev){var a=ev.target.closest('a[href^="#"]');if(!a||ev.defaultPrevented||ev.button||ev.metaKey||ev.ctrlKey||ev.shiftKey||ev.altKey)return;
var id=a.getAttribute("href").slice(1),t=id?document.getElementById(id):null;if(id&&!t)return;ev.preventDefault();
if(!t){window.scrollTo({top:0,behavior:rm.matches?"auto":"smooth"});var h=$("header a");if(h)h.focus({preventScroll:true});return}
t.scrollIntoView({behavior:rm.matches?"auto":"smooth",block:"start"});if(!t.hasAttribute("tabindex"))t.setAttribute("tabindex","-1");t.focus({preventScroll:true})});
if(location.hash){var _it=document.getElementById(location.hash.slice(1));history.replaceState(null,"",location.pathname+location.search);if(_it){setTimeout(function(){_it.scrollIntoView({behavior:rm.matches?"auto":"smooth",block:"start"})},50)}}
/* scrollspy: highlight the nav link of the section in view, and keep it visible in the scrollable mobile nav */
var nav=$("header nav"),nl=$$("a",nav),secs=nl.map(function(a){return document.getElementById(a.getAttribute("href").slice(1))}),cur=-1,tick=false;
function spy(){tick=false;var hh=$("header").offsetHeight+24,i=-1,bottom=window.innerHeight+window.scrollY>=document.documentElement.scrollHeight-4;
secs.forEach(function(s,k){if(s&&s.getBoundingClientRect().top<=hh)i=k});if(bottom&&secs.length)i=secs.length-1;if(i===cur)return;cur=i;
nl.forEach(function(a,k){if(k===i)a.setAttribute("aria-current","true");else a.removeAttribute("aria-current")});
if(i<0&&nav.scrollLeft>0)nav.scrollTo({left:0,behavior:"smooth"});if(i>=0&&nav.scrollWidth>nav.clientWidth){var a=nl[i],l=a.getBoundingClientRect().left-nav.getBoundingClientRect().left+nav.scrollLeft;nav.scrollTo({left:Math.max(0,l-(nav.clientWidth-a.offsetWidth)/2),behavior:matchMedia("(prefers-reduced-motion:reduce)").matches?"auto":"smooth"})}}
var tt2=$(".totop");function onScroll(){if(tt2)tt2.classList.toggle("on",window.scrollY>window.innerHeight);if(!tick){tick=true;requestAnimationFrame(spy)}}
addEventListener("scroll",onScroll,{passive:true});addEventListener("resize",onScroll);onScroll();
/* how-to-draw: steps 0..5, autoplays once when scrolled into view */
var dw=$("#draw"),dli=$$("#draw-steps li"),dpl=$("#draw-play"),dStep=-1,dTm=null,dLast=dli.length-1;
function dSet(i){dStep=i;$$("[data-s]",dw).forEach(function(el){el.classList.toggle("in",+el.dataset.s<=i)});dw.classList.toggle("clean",i>=dLast);
dli.forEach(function(li,k){li.classList.toggle("on",k===i);li.classList.toggle("done",k<i);var b=li.firstChild;if(k===i)b.setAttribute("aria-current","step");else b.removeAttribute("aria-current")});dLabel()}
function dLabel(){if(!dpl)return;dpl.textContent=dTm?L[lang].dPause:(dStep>=dLast?L[lang].dAgain:L[lang].dPlay);
$("#draw-prev").setAttribute("aria-label",L[lang].dPrev);$("#draw-next").setAttribute("aria-label",L[lang].dNext);dw.setAttribute("aria-label",L[lang].dAria)}
function dStop(){clearTimeout(dTm);dTm=null;dLabel()}
function dTick(){dSet(dStep+1);if(dStep>=dLast){dStop();return}dTm=setTimeout(dTick,dStep===1?1500:1300);dLabel()}
function dPlay(){if(dTm){dStop();return}if(dStep>=dLast){dSet(-1);}dTm=setTimeout(dTick,dStep<0?150:0);dLabel()}
if(dw){if(rm.matches)dSet(dLast);else dSet(-1);
dpl.addEventListener("click",dPlay);$("#draw-prev").addEventListener("click",function(){dStop();dSet(Math.max(0,dStep-1))});
$("#draw-next").addEventListener("click",function(){dStop();dSet(Math.min(dLast,dStep+1))});
dli.forEach(function(li,k){li.firstChild.addEventListener("click",function(){dStop();dSet(k)})});
if("IntersectionObserver" in window&&!rm.matches){var dio=new IntersectionObserver(function(es){if(es[0].isIntersecting){dio.disconnect();if(dStep<0&&!dTm)dPlay()}},{threshold:.6});dio.observe(dw)}
else if(!rm.matches)dSet(dLast)}

/* exporter + background test: one render() for preview and download */
var exV=$("#ex-v"),exW=$("#ex-w"),exP=$("#ex-p"),exPo=$("#ex-po"),exC=$("#ex-c"),exF=$("#ex-f"),exN=$("#ex-n"),exK=$("#ex-k"),exCv=$("#ex-cv"),exD=$("#ex-d"),svgCache={},photo=null,exState=null;
function rgb(h){h=h.replace("#","");if(h.length===3)h=h.replace(/./g,"$&$&");return[0,2,4].map(function(i){return parseInt(h.substr(i,2),16)})}
function lin(c){c/=255;return c<=.03928?c/12.92:Math.pow((c+.055)/1.055,2.4)}
function lum(c){return .2126*lin(c[0])+.7152*lin(c[1])+.0722*lin(c[2])}
function ratio(a,b){var x=Math.max(a,b),y=Math.min(a,b);return(x+.05)/(y+.05)}
function fmt(n){return n.toFixed(1).replace(".",lang==="id"?",":".")}
function bgMode(){var c=$('input[name="ex-bg"]:checked');return c?c.value:"none"}
function fmtMode(){return $('input[name="ex-fmt"]:checked').value}
function loadSvg(o){var src=o.dataset.src;if(svgCache[src])return svgCache[src];
svgCache[src]=fetch(src).then(function(r){if(!r.ok)throw 0;return r.text()}).then(function(t){var vb=t.match(/viewBox="([^"]+)"/)[1].split(/\s+/).map(Number),
fills=(t.match(/fill="#[0-9A-Fa-f]{3,6}"/g)||[]).map(function(f){return f.slice(6,-1).toUpperCase()}).filter(function(v,i,a){return a.indexOf(v)===i});
var sized=t.replace("<svg ",'<svg width="'+vb[2]+'" height="'+vb[3]+'" ');
return new Promise(function(res,rej){var im=new Image();im.onload=function(){res({img:im,vb:vb,text:t,fills:fills})};im.onerror=rej;im.src="data:image/svg+xml,"+encodeURIComponent(sized)})});
svgCache[src].catch(function(){delete svgCache[src]});return svgCache[src]}
function geom(o,s,want){var x=+o.dataset.x,pad=+o.dataset.pad,cw=s.vb[2]-2*pad,ch=s.vb[3]-2*pad,n=+exP.value,w=Math.max(1,want),k=w/cw,
W=Math.round(w+2*n*x*k),H=Math.round(ch*k+2*n*x*k),capped=false;
if(Math.max(W,H)>4096){var f=4096/Math.max(W,H);k*=f;w*=f;W=Math.round(W*f);H=Math.round(H*f);capped=true}
return{k:k,W:W,H:H,off:n*x*k-pad*k,lw:Math.round(w),capped:capped,box:[n*x*k,n*x*k,cw*k,ch*k]}}
function cover(ctx,img,W,H){var r=Math.max(W/img.width,H/img.height),w=img.width*r,h=img.height*r;ctx.drawImage(img,(W-w)/2,(H-h)/2,w,h)}
function paintBg(ctx,W,H,mode,force){if(mode==="photo"&&photo)cover(ctx,photo,W,H);else if(mode==="none"||mode==="photo"){if(force){ctx.fillStyle="#FFFFFF";ctx.fillRect(0,0,W,H)}}
else{ctx.fillStyle=mode==="custom"?exC.value:mode;ctx.fillRect(0,0,W,H)}}
function render(cv,o,s,g,scale,force){cv.width=Math.max(1,Math.round(g.W*scale));cv.height=Math.max(1,Math.round(g.H*scale));var ctx=cv.getContext("2d");
ctx.clearRect(0,0,cv.width,cv.height);paintBg(ctx,cv.width,cv.height,bgMode(),force);
ctx.drawImage(s.img,g.off*scale,g.off*scale,s.vb[2]*g.k*scale,s.vb[3]*g.k*scale);return ctx}
function bgLum(g,scale){var mode=bgMode();if(mode==="none")return null;if(mode==="photo"){if(!photo)return null;
var c=document.createElement("canvas"),W=Math.max(1,Math.round(g.W*scale)),H=Math.max(1,Math.round(g.H*scale));c.width=W;c.height=H;var x=c.getContext("2d");cover(x,photo,W,H);
var b=g.box.map(function(v){return Math.round(v*scale)}),d=x.getImageData(b[0],b[1],Math.max(1,b[2]),Math.max(1,b[3])).data,sum=0,n=0;
for(var i=0;i<d.length;i+=16){sum+=lum([d[i],d[i+1],d[i+2]]);n++}return{l:sum/n,est:true}}
return{l:lum(rgb(mode==="custom"?exC.value:mode)),est:false}}
function exText(){if(!exState)return;var o=exState.o,s=exState.s,g=exState.g,L2=L[lang],mn=+o.dataset.min,mode=bgMode(),f=fmtMode();
var h=L2.exOut+": <b>"+g.W+" × "+g.H+" px</b>";if(g.capped)h+=" · "+L2.exCap;
if(+exW.value<mn)h+="<br>"+L2.exMin+": "+mn+" px. "+(o.dataset.kind!=="i"?L2.exUseIcon:"");
if(f==="svg"&&mode==="photo")h+="<br>"+L2.exSvgPhoto;exN.innerHTML=h;
exPo.textContent=exP.value+"×";var k="";
if(o.dataset.kind==="i")k=L2.exIcon;else{var bl=bgLum(g,exState.scale);
if(!bl)k=mode==="photo"?L2.exPick+".":L2.exTr;else{var worst=Infinity;s.fills.forEach(function(c){worst=Math.min(worst,ratio(lum(rgb(c)),bl.l))});
var ok=worst>=3;k=L2.exCR+" <b>"+fmt(worst)+" : 1</b> <span class=\"tag "+(ok?"ok":"bad")+"\">"+(ok?L2.exOk:L2.exBad)+"</span>"+(bl.est?" <span>("+L2.exEst+")</span>":"");
if(!ok){var ink=ratio(lum([13,13,13]),bl.l),wh=ratio(1,bl.l);k+=" · "+L2.exTry+" "+(ink>=wh?L2.exInk:L2.exWhite)+(L2.exVer?" "+L2.exVer:"")+"."}}}
exK.innerHTML=k}
var exSeq=0;
function exUpdate(){var o=exV.options[exV.selectedIndex],my=++exSeq;
$$('input[name="ex-fmt"]').forEach(function(i){if(i.value==="svg")i.disabled=bgMode()==="photo"});
if(fmtMode()==="svg"&&bgMode()==="photo")$('input[name="ex-fmt"][value="png"]').checked=true;
loadSvg(o).then(function(s){if(my!==exSeq)return;var g=geom(o,s,Math.min(4096,Math.max(1,+exW.value||1))),box=$("#ex-box"),
scale=Math.min((box.clientWidth-40)*(window.devicePixelRatio||1)/g.W,380*(window.devicePixelRatio||1)/g.H);
render(exCv,o,s,g,scale,false);exState={o:o,s:s,g:g,scale:scale};exText()},function(){exN.textContent=L[lang].exErr})}
function exDownload(){if(!exState)return;var o=exState.o,s=exState.s,g=exState.g,f=fmtMode(),mode=bgMode(),name="louvre-"+o.value+"-"+g.W+"x"+g.H+"."+f;
function save(blob){var u=URL.createObjectURL(blob),a=document.createElement("a");a.href=u;a.download=name;document.body.appendChild(a);a.click();a.remove();setTimeout(function(){URL.revokeObjectURL(u)},4000)}
if(f==="svg"){var fill=mode==="none"?"":'<rect width="100%" height="100%" fill="'+(mode==="custom"?exC.value:mode)+'"/>',
inner=s.text.replace("<svg ",'<svg x="'+g.off.toFixed(2)+'" y="'+g.off.toFixed(2)+'" width="'+(s.vb[2]*g.k).toFixed(2)+'" height="'+(s.vb[3]*g.k).toFixed(2)+'" ');
save(new Blob(['<svg xmlns="http://www.w3.org/2000/svg" width="'+g.W+'" height="'+g.H+'" viewBox="0 0 '+g.W+" "+g.H+'">'+fill+inner+"</svg>"],{type:"image/svg+xml"}));return}
var c=document.createElement("canvas");render(c,o,s,g,1,f==="jpg");c.toBlob(function(b){if(b)save(b)},f==="jpg"?"image/jpeg":f==="webp"?"image/webp":"image/png",.92)}
if(exV){exV.addEventListener("change",function(){exV._u=1;var mn=+exV.options[exV.selectedIndex].dataset.min;if(+exW.value<mn)exW.value=mn;exUpdate()});
[exW,exP].forEach(function(i){i.addEventListener("input",exUpdate)});exC.addEventListener("input",function(){$('input[name="ex-bg"][value="custom"]').checked=true;exUpdate()});
$$('input[name="ex-bg"],input[name="ex-fmt"]').forEach(function(i){i.addEventListener("change",function(){if(i.value==="photo"&&!photo){exF.click()}exUpdate()})});
$('input[name="ex-bg"][value="photo"]').parentNode.addEventListener("click",function(){if(photo&&bgMode()==="photo")exF.click()});
exF.addEventListener("change",function(){var file=exF.files&&exF.files[0];if(!file)return;createImageBitmap(file).then(function(b){photo=b;$('input[name="ex-bg"][value="photo"]').checked=true;exUpdate()},function(){say(L[lang].exImg)})});
exD.addEventListener("click",exDownload);addEventListener("resize",function(){clearTimeout(exV._t);exV._t=setTimeout(exUpdate,150)});
/* until the visitor picks a version, follow the theme: ink symbol on light, white symbol on dark */
var mqD=matchMedia("(prefers-color-scheme:dark)");
function exTheme(){if(exV._u)return;var t=r.dataset.theme,dk=t==="dark"||(t!=="light"&&mqD.matches),want=dk?"symbol-white":"symbol-ink";if(exV.value!==want){exV.value=want;exUpdate()}}
exTheme();if(mqD.addEventListener)mqD.addEventListener("change",exTheme);new MutationObserver(exTheme).observe(r,{attributes:true,attributeFilter:["data-theme"]});
exUpdate()}
setLang(lang,false);
})();
"""

HEAD = f'''<!doctype html><html lang="id"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<script>try{{var t=localStorage.getItem("theme");if(t==="dark"||t==="light")document.documentElement.dataset.theme=t}}catch(e){{}}</script>
<title>Louvre — Identitas visual</title><meta name="description" content="Louvre: piramida kaca dari sembilan segitiga. Simbol, lockup, panduan, dan penerapan identitas visual Louvre.">
<link rel="canonical" href="{URL}"><link rel="alternate" hreflang="id" href="{URL}"><link rel="alternate" hreflang="en" href="{URL}en/"><link rel="alternate" hreflang="x-default" href="{URL}">
<meta property="og:type" content="website"><meta property="og:site_name" content="Louvre"><meta property="og:url" content="{URL}"><meta property="og:title" content="Louvre — Logo yang bisa digambar dari ingatan.">
<meta property="og:description" content="Piramida kaca dari sembilan segitiga. Simbol, lockup, panduan, dan penerapan identitas visual Louvre."><meta property="og:image" content="{URL}assets/og-image-v3.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Logo Louvre putih di atas latar hitam">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="Louvre — Logo yang bisa digambar dari ingatan."><meta name="twitter:description" content="Piramida kaca dari sembilan segitiga. Simbol, lockup, panduan, dan penerapan."><meta name="twitter:image" content="{URL}assets/og-image-v3.png">
<meta name="theme-color" content="#0D0D0D"><link rel="icon" href="assets/symbol/app-icon-dark.svg" type="image/svg+xml"><link rel="icon" href="assets/symbol/favicon.ico" sizes="48x48"><link rel="apple-touch-icon" href="assets/symbol/apple-touch-icon.png"><link rel="manifest" href="manifest.webmanifest">
<link rel="preload" href="assets/font/HankenGrotesk-Variable.woff2" as="font" type="font/woff2" crossorigin><style>{CSS}</style></head><body>'''

BODY = f'''<a class="skip" href="#main" data-en="Skip to content">Lewati ke konten</a>
<header><div class="wrap"><a href="#" aria-label="Louvre"><img class="logo-l" src="assets/lockup/lockup-ink.svg" width="{lkw(24)}" height="24" alt="Louvre"><img class="logo-d" src="assets/lockup/lockup-white.svg" width="{lkw(24)}" height="24" alt="Louvre"></a>
<nav aria-label="Navigasi">{T("a","Cerita","Story",'href="#cerita"')}{T("a","Simbol","Symbol",'href="#symbol"')}{T("a","Lockup","Lockup",'href="#lockup"')}{T("a","Ekspor","Export",'href="#ekspor"')}{T("a","Panduan","Guidelines",'href="#panduan"')}{T("a","Penerapan","In use",'href="#mockup"')}{T("a","Font","Typeface",'href="#font"')}{T("a","Warna","Colour",'href="#warna"')}</nav>
<div class="tg l" role="group" aria-label="Bahasa"><button type="button" data-l="id">ID</button><button type="button" data-l="en">EN</button></div>
<div class="tg t" role="group" aria-label="Tema"><button type="button" data-t="auto">Auto</button><button type="button" data-t="light" data-en="Light">Terang</button><button type="button" data-t="dark" data-en="Dark">Gelap</button></div></div></header>
<main class="wrap" id="main">
<div class="hero"><div>{T("h1","Logo yang bisa<br>digambar dari ingatan.","A logo you can<br>draw from memory.")}
{T("p","Piramida kaca dari sembilan segitiga, dengan celah tipis di antaranya. Satu warna, tanpa efek, terbaca dari favicon sampai papan reklame.","A glass pyramid of nine triangles with thin gaps between them. One colour, no effects, readable from favicon to billboard.")}
<div class="acts">{T("a","Lihat penerapannya","See it in use",'class="btn" href="#mockup"')}{T("a","Lihat simbolnya","See the symbol",'class="btn o" href="#symbol"')}{T("a","Unduh paket logo (.zip)","Download logo kit (.zip)",'class="btn o" href="assets/download/louvre-logo-kit.zip" download')}</div></div>{hero_svg}</div>

<section id="cerita">{T("h2","Di balik bentuknya","Behind the shape")}{T("p","Tiga keputusan di balik bentuknya.","Three decisions behind the shape.",'class="lead"')}
<div class="pts"><div class="pt"><i>1</i>{T("b","Satu bentuk, tiga baris","One shape, three rows")}{T("span","Sembilan segitiga dalam tiga baris: 1, 3, 5. Mudah diingat, mudah digambar ulang.","Nine triangles in three rows: 1, 3, 5. Easy to remember, easy to redraw.")}</div>
<div class="pt"><i>2</i>{T("b","Celahnya transparan","Transparent gaps")}{T("span","Celah di antara segitiga dibiarkan kosong, jadi latar tetap terlihat. Terbaca di atas warna, foto, atau kaca.","The gaps between the triangles stay empty, so the background shows through. Readable on colour, photos or glass.")}</div>
<div class="pt"><i>3</i>{T("b","Satu warna sudah cukup","One colour is enough")}{T("span","Tinta, putih, atau abu. Tanpa gradasi dan efek, jadi tetap konsisten dari favicon sampai papan reklame.","Ink, white or grey. No gradients or effects, so it stays consistent from favicon to billboard.")}</div></div>
<h3>{T("span","Cara menggambarnya","How to draw it")}</h3><div class="drw"><div class="drs">{draw_svg}</div><div><ol class="dsl" id="draw-steps">{draw_ol}</ol><div class="dct"><button type="button" class="btn o" id="draw-prev" aria-label="Langkah sebelumnya">←</button><button type="button" class="btn" id="draw-play">Putar</button><button type="button" class="btn o" id="draw-next" aria-label="Langkah berikutnya">→</button></div></div></div></section>

<section id="symbol">{T("h2","Simbol","Symbol")}{T("p","Piramida sembilan segitiga dalam versi tinta dan putih, plus ikon aplikasi.","The nine-triangle pyramid in ink and white, plus app icons.",'class="lead"')}<div class="grid two">{sym_cards}</div></section>

<section id="lockup">{T("h2","Lockup","Lockup")}{T("p","Simbol di kiri, nama di kanan, dalam tiga versi: dua nada, tinta, dan putih. Namanya selalu ditulis Louvre: L kapital, sisanya huruf kecil.","Symbol on the left, name on the right, in three versions: two-tone, ink and white. The name is always written Louvre: capital L, the rest lowercase.",'class="lead"')}<div class="grid">{lock_cards}</div></section>
{EX_HTML}

<section id="panduan">{T("h2","Panduan pemakaian","Usage guidelines")}{T("p","Tiga aturan dasar: ruang aman, ukuran minimum, dan yang perlu dihindari.","Three basic rules: clear space, minimum size, and what to avoid.",'class="lead"')}
<div class="gd"><div><h3 style="margin-top:0">{T("span","Ruang aman","Clear space")}</h3>{T("p","Sisakan ruang kosong di sekeliling logo setara tinggi segitiga teratas (x).","Keep empty space around the logo equal to the height of the top triangle (x).",'class="lead" style="margin-bottom:12px"')}<div class="card plate-l"><div class="art">{cs}</div></div></div>
<div><h3 style="margin-top:0">{T("span","Ukuran minimum","Minimum size")}</h3>{T("p","Lebar minimum simbol 24 px, lockup 96 px. Di bawah itu, pakai ikon aplikasi.","Minimum width: symbol 24 px, lockup 96 px. Below that, use the app icon.",'class="lead" style="margin-bottom:12px"')}<div class="card plate-l"><div class="art"><div class="ms"><figure><img src="assets/symbol/symbol-ink.svg" width="24" height="21" alt=""><span>24 px</span></figure><figure><img src="assets/lockup/lockup-ink.svg" width="96" height="{lkh(96)}" alt=""><span>96 px</span></figure><figure><img src="assets/lockup/lockup-ink.svg" width="160" height="{lkh(160)}" alt=""><span>160 px</span></figure><figure><img src="assets/symbol/app-icon-dark.svg" width="16" height="16" alt=""><span data-en="16 px · app icon">16 px · ikon</span></figure></div></div></div></div></div>
<h3>{T("span","Yang perlu dihindari","What to avoid")}</h3><div class="grid dn5">{dont_html}</div></section>

<section id="mockup">{T("h2","Penerapan","In use")}{T("p","Contoh logo di kaos, ikon aplikasi, mug, tumbler, tote bag, dasbor web, kartu nama, dan profil sosial.","The logo on a t-shirt, app icon, mug, tumbler, tote bag, web dashboard, business card and social profile.",'class="lead"')}
<p style="margin:-8px 0 20px">{T("a","Unduh semua mockup (.zip)","Download all mockups (.zip)",'class="btn o" href="assets/download/louvre-mockups.zip" download')}</p><div class="mk">{mock_html}</div></section>

<section id="font">{T("h2","Font","Typeface")}{T("p","Hanken Grotesk. Lisensi SIL OFL 1.1: boleh dipakai gratis, termasuk untuk proyek komersial.","Hanken Grotesk. SIL OFL 1.1 licence: free to use, including for commercial projects.",'class="lead"')}
<div class="card"><div class="spec"><div class="big">Louvre</div><div class="pang"><span style="font-weight:700">The lazy dog jumps over the quick brown fox</span><span style="font-weight:400;color:var(--t2)">The lazy dog jumps over the quick brown fox</span></div>
<div class="row"><span style="font-weight:300">Light 300</span><span style="font-weight:400">Regular 400</span><span style="font-weight:500">Medium 500</span><span style="font-weight:600">SemiBold 600</span><span style="font-weight:700">Bold 700</span></div><div class="row" style="font-size:15px;color:var(--t2)"><span>ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz 0123456789</span></div></div>
<div class="acts">{T("a","Unduh font (.zip)","Download font (.zip)",'class="btn" href="assets/font/HankenGrotesk.zip" download')}{T("a","TTF variabel","Variable TTF",'class="btn o" href="assets/font/HankenGrotesk-Variable.ttf" download')}{T("a","Lisensi SIL OFL","SIL OFL licence",'class="btn o" href="assets/font/OFL.txt"')}</div>
<div class="cap">{T("b","Hanken Grotesk 3.013 · variabel 100–900","Hanken Grotesk 3.013 · variable 100–900")}<span>{T("span","© 2021 The Hanken Grotesk Project Authors · ","© 2021 The Hanken Grotesk Project Authors · ")}<a href="https://github.com/marcologous/hanken-grotesk" rel="noopener">{T("span","sumber","source")}</a></span></div></div></section>

<section id="warna">{T("h2","Warna","Colour")}{T("p","Tinta, putih, dan tiga abu. Tidak ada warna aksen.","Ink, white and three greys. No accent colour.",'class="lead"')}
<div class="pal">{pal_html}</div>{T("p","Klik untuk menyalin kode warna.","Click to copy the colour code.",'class="hint"')}{pal_tbl}{T("p","*CMYK hasil konversi sederhana, hanya perkiraan. Untuk cetak, minta proof dari percetakan. Teks di bawah 4,5 : 1 hanya untuk elemen dekoratif.","*CMYK is a simple approximate conversion. For print, ask the printer for a proof. Text below 4.5 : 1 is for decorative elements only.",'class="hint"')}</section>
</main>
<footer><div class="wrap">{T("span","© 2026 Louvre · Font: Hanken Grotesk, SIL OFL 1.1","© 2026 Louvre · Typeface: Hanken Grotesk, SIL OFL 1.1")}</div></footer>
<a class="totop" href="#"><svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path d="M12 19V5M5 12l7-7 7 7" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>{T("span","Kembali ke atas","Back to top",'class="vh"')}</a>
<dialog id="lb" aria-label="Pratinjau mockup"><div class="lbx"><img alt="" src=""><div class="lbc"><b class="lbn"></b><a class="lbd" href="#" download>{T("span","Unduh","Download")}</a></div></div>
<button class="lbb p" type="button" aria-label="Sebelumnya">←</button><button class="lbb n" type="button" aria-label="Berikutnya">→</button><button class="lbb c" type="button" aria-label="Tutup">✕</button></dialog>
<div class="toast" role="status" aria-live="polite"></div>
<script>{JS}</script></body></html>'''

_out = HEAD + BODY
# cache-bust files changed after first publish (Cloudflare edge caches static files for hours; purge not permitted for our token)
# content-hash cache busting: every local asset URL gets ?v=<hash>, so Caddy can cache it immutably
import hashlib
_hc = {}
def _ver(m):
    path = m.group(1)
    fp = os.path.join(ROOT, path)
    if not os.path.isfile(fp): return m.group(0)
    if path not in _hc: _hc[path] = hashlib.sha1(open(fp, "rb").read()).hexdigest()[:8]
    return f"{path}?v={_hc[path]}"
_out = re.sub(r'(assets/[A-Za-z0-9_./-]+\.[a-z0-9]+)', _ver, _out)
# every <img> except the header logo loads lazily
_out = re.sub(r'<img (?![^>]*(?:loading=|class="logo-))', '<img loading="lazy" decoding="async" ', _out)
# root-absolute URLs: the language toggle can rewrite / to /en/ via history.replaceState, so relative paths would break
_out = re.sub(r'(["(,] ?)(assets/|manifest\.webmanifest)', r'\1/\2', _out)
open(ROOT + "/index.html", "w").write(_out)

# ---------- /en/: same page, English text in the HTML so crawlers see it ----------
def _swap(m):
    tag, pre, en, post, inner = m.groups()
    return f'<{tag}{pre} data-en="{en}" data-id="{e(inner)}"{post}>{html.unescape(en)}</{tag}>'
_en = re.sub(r'<(\w+)([^>]*?) data-en="([^"]*)"([^>]*)>(.*?)</\1>', _swap, _out, flags=re.S)
_en = _en.replace('<html lang="id">', '<html lang="en">', 1)
_en = _en.replace(f'<link rel="canonical" href="{URL}">', f'<link rel="canonical" href="{URL}en/">', 1)
_en = _en.replace(f'<meta property="og:url" content="{URL}">', f'<meta property="og:url" content="{URL}en/">', 1)
for _a, _b in ([("Louvre — Identitas visual", "Louvre — Visual identity"),
               ("Louvre: piramida kaca dari sembilan segitiga. Simbol, lockup, panduan, dan penerapan identitas visual Louvre.", "Louvre: a glass pyramid of nine triangles. Symbol, lockup, guidelines and applications of the Louvre visual identity."),
               ("Piramida kaca dari sembilan segitiga. Simbol, lockup, panduan, dan penerapan identitas visual Louvre.", "A glass pyramid of nine triangles. Symbol, lockup, guidelines and applications of the Louvre visual identity."),
               ("Piramida kaca dari sembilan segitiga. Simbol, lockup, panduan, dan penerapan.", "A glass pyramid of nine triangles. Symbol, lockup, guidelines and applications."),
               ("Louvre — Logo yang bisa digambar dari ingatan.", "Louvre — A logo you can draw from memory."),
               ("Logo Louvre putih di atas latar hitam", "White Louvre logo on a black background"),
               ('aria-label="Navigasi"', 'aria-label="Navigation"'), ('aria-label="Bahasa"', 'aria-label="Language"'),
               ('aria-label="Tema"', 'aria-label="Theme"'), ('aria-label="Pratinjau mockup"', 'aria-label="Mockup preview"'),
               ('aria-label="Sebelumnya"', 'aria-label="Previous"'), ('aria-label="Berikutnya"', 'aria-label="Next"'),
               ('aria-label="Tutup"', 'aria-label="Close"'), ('aria-label="Cara menggambar logo Louvre"', 'aria-label="How to draw the Louvre logo"'), ('aria-label="Langkah sebelumnya"', 'aria-label="Previous step"'), ('aria-label="Langkah berikutnya"', 'aria-label="Next step"'), ('id="draw-play">Putar<', 'id="draw-play">Play<'), ('aria-label="Warna latar"', 'aria-label="Background colour"'), ('aria-label="Pratinjau ekspor"', 'aria-label="Export preview"'), ('aria-label="Piramida Louvre"', 'aria-label="Louvre pyramid"'),
               ("Diagram ruang aman: x sama dengan tinggi satu segitiga teratas", "Clear-space diagram: x equals the height of the top triangle"),
               ('alt="Simbol Louvre, tinta"', 'alt="Louvre symbol, ink"'), ('alt="Simbol Louvre, putih"', 'alt="Louvre symbol, white"'),
               ('alt="Ikon aplikasi Louvre, gelap"', 'alt="Louvre app icon, dark"'), ('alt="Ikon aplikasi Louvre, terang"', 'alt="Louvre app icon, light"'),
               (", dua nada\"", ", two-tone\""), (", tinta\"", ", ink\""), (", putih\"", ", white\"")]
    + [(f'alt="Mockup {_a}"', f'alt="Mockup: {_b.lower()}"') for _n, _a, _b in mock]):
    _en = _en.replace(_a, _b)
# relative URLs would resolve under /en/; make them root-absolute
_en = re.sub(r'(["(,] ?)(assets/|manifest\.webmanifest)', r'\1/\2', _en)
os.makedirs(ROOT + "/en", exist_ok=True)
open(ROOT + "/en/index.html", "w").write(_en)

open(ROOT + "/robots.txt", "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {URL}sitemap.xml\n")
import datetime
_d = datetime.date.today().isoformat()
_alt = (f'<xhtml:link rel="alternate" hreflang="id" href="{URL}"/><xhtml:link rel="alternate" hreflang="en" href="{URL}en/"/>'
        f'<xhtml:link rel="alternate" hreflang="x-default" href="{URL}"/>')
open(ROOT + "/sitemap.xml", "w").write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
    + "".join(f"<url><loc>{u}</loc><lastmod>{_d}</lastmod>{_alt}</url>\n" for u in (URL, URL + "en/")) + "</urlset>\n")
open(ROOT + "/404.html", "w").write('''<!doctype html><html lang="id"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>404 — Louvre</title>
<style>@font-face{font-family:"Hanken Grotesk";src:url(/assets/font/HankenGrotesk-Variable.woff2) format("woff2");font-weight:100 900;font-display:swap}
body{margin:0;min-height:100vh;display:grid;place-items:center;background:#fff;color:#0D0D0D;font:16px/1.6 "Hanken Grotesk",system-ui,sans-serif;text-align:center;padding:24px}@media(prefers-color-scheme:dark){body{background:#000;color:#fff}.l{filter:invert(1)}}
h1{font-size:64px;margin:16px 0 4px;letter-spacing:-.04em}p{color:#5D5D5D;margin:0 0 20px}a{display:inline-block;background:#0D0D0D;color:#fff;text-decoration:none;border-radius:999px;padding:10px 20px;font-weight:600;font-size:14px}@media(prefers-color-scheme:dark){a{background:#fff;color:#000}}</style></head>
<body><div><img class="l" src="/assets/symbol/symbol-ink.svg" width="72" height="62" alt=""><h1>404</h1><p>Halaman ini tidak ada.<br>This page doesn't exist.</p><a href="/">Kembali / Back</a></div></body></html>''')
print("built", os.path.getsize(ROOT + "/index.html"), "bytes")
