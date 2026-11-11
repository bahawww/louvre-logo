#!/usr/bin/env python3
"""SVG -> PNG with headless Chrome (transparent background). Run: python3 src/render.py in.svg out.png WIDTH [--bg #hex]"""
import os, re, shutil, subprocess, sys, tempfile
CH = next(c for c in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser") if shutil.which(c))

def vb(svg_text):
    return tuple(map(float, re.search(r'viewBox="([^"]+)"', svg_text).group(1).split()[2:]))

def render(svg_path, out, width, bg=None, height=None):
    t = open(svg_path).read(); w, h = vb(t); H = height or round(width * h / w)
    body = re.sub(r"<svg ", f'<svg width="{width}" height="{H}" style="display:block" ', t.split("?>")[-1], count=1)
    with tempfile.TemporaryDirectory() as d:
        hp = os.path.join(d, "p.html")
        open(hp, "w").write(f'<!doctype html><meta charset=utf-8><style>html,body{{margin:0;background:{bg or "transparent"};overflow:hidden}}</style>{body}')
        subprocess.run([CH, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run", "--force-device-scale-factor=1",
                        "--default-background-color=00000000", f"--window-size={width},{H}", f"--screenshot={os.path.abspath(out)}", "file://" + hp],
                       check=True, capture_output=True, timeout=60)
    return width, H

def pdf(svg_path, out, page_w=800):
    t = open(svg_path).read(); w, h = vb(t); h = h * page_w / w; w = page_w
    body = re.sub(r"<svg ", f'<svg width="{w:.0f}" height="{h:.0f}" style="display:block" ', t.split("?>")[-1], count=1)
    with tempfile.TemporaryDirectory() as d:
        hp = os.path.join(d, "p.html")
        open(hp, "w").write(f'<!doctype html><meta charset=utf-8><style>@page{{size:{w:.0f}px {h:.0f}px;margin:0}}html,body{{margin:0;background:none}}</style>{body}')
        subprocess.run([CH, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--no-first-run", f"--print-to-pdf={os.path.abspath(out)}", "file://" + hp],
                       check=True, capture_output=True, timeout=60)

if __name__ == "__main__":
    a = sys.argv[1:]; bg = a[a.index("--bg") + 1] if "--bg" in a else None
    print(render(a[0], a[1], int(a[2]), bg))
