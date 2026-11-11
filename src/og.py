#!/usr/bin/env python3
"""Open Graph image 1200x630: white lockup + tagline on ink. Run: .venv/bin/python src/og.py"""
import os, re, shutil, subprocess, tempfile
H = os.path.dirname(os.path.abspath(__file__)); A = os.path.join(H, "..", "site", "assets")
CH = next(c for c in ("google-chrome", "google-chrome-stable", "chromium") if shutil.which(c))
svg = open(f"{A}/lockup/lockup-white.svg").read().replace("<svg ", '<svg width="640" style="display:block;margin:0 auto" ', 1)
font = "file://" + os.path.abspath(f"{A}/font/HankenGrotesk-Variable.woff2")
page = f'''<!doctype html><meta charset=utf-8><style>@font-face{{font-family:H;src:url({font}) format("woff2");font-weight:100 900}}
html,body{{margin:0;width:1200px;height:630px;background:#0D0D0D;overflow:hidden}}
body{{display:flex;flex-direction:column;justify-content:center;align-items:center;gap:44px}}
p{{margin:0;font:400 36px/1 H,sans-serif;color:#A3A3A3;letter-spacing:-.005em}}</style>{svg}<p>Logo yang bisa digambar dari ingatan.</p>'''
out = os.path.abspath(f"{A}/og-image-v3.png")
with tempfile.TemporaryDirectory() as d:
    hp = os.path.join(d, "og.html"); open(hp, "w").write(page)
    subprocess.run([CH, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run", "--force-device-scale-factor=1",
                    "--allow-file-access-from-files", "--virtual-time-budget=2000", "--window-size=1200,630", f"--screenshot={out}", "file://" + hp],
                   check=True, capture_output=True, timeout=60)
print(out)
