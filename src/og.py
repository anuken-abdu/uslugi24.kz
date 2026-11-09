# -*- coding: utf-8 -*-
"""Иконки сайта и OG-картинка: python3 src/og.py (нужен собранный dist/), затем снова python3 src/build.py."""
import http.server, socketserver, threading, functools, sys
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright
sys.path.insert(0, str(Path(__file__).parent))
import build as B
ROOT = Path(__file__).resolve().parent.parent; DIST = ROOT / "dist"; A = ROOT / "assets"
tiles = [(i, l, "#", False) if i else ("toolbox", "Все работы", "#", True) for i, l, s in B.HERO_TILES]
OG = f'''<!doctype html><html><head><meta charset="utf-8"><style>{B.CSS}</style><style>
html,body{{margin:0}}.og{{position:relative;width:1200px;height:630px;overflow:hidden;color:#fff;background:radial-gradient(520px 380px at 84% 46%,rgba(58,91,255,.38),transparent 70%),var(--grid-d),var(--ink);background-size:auto,32px 32px,32px 32px,auto}}
.og-in{{position:absolute;inset:0 0 38px;display:grid;grid-template-columns:1fr 430px;gap:50px;align-items:center;padding:0 64px}}
.og h1{{font-size:62px;line-height:1.06}}.og h1 em{{font-style:normal;color:var(--y)}}
.og p{{margin-top:22px;font-size:24px;line-height:1.4;color:rgba(255,255,255,.8)}}
.og .logo{{margin-bottom:34px}}.og .logo-t{{font-size:28px}}.og .logo img{{width:56px;height:56px}}
.og .board{{gap:12px;padding:16px;max-width:none}}.og .bt span{{font-size:13px}}
.og .ph-l{{display:flex;gap:12px;margin-top:30px}}.og .ph-l span{{font:600 19px/1 var(--bf);padding:12px 16px;border-radius:10px;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.14)}}
</style></head><body><div class="og"><div class="og-in"><div>{B.logo(True)}<h1>Мастер на&nbsp;час <em>в&nbsp;Астане</em></h1>
<p>Сборка мебели, сантехник, электрик, навеска телевизоров и&nbsp;люстр. Бесплатный выезд по&nbsp;Астане.</p></div>{B.board(tiles)}</div>{B.tape()}</div></body></html>'''
ICON = '''<!doctype html><html><body style="margin:0;background:transparent"><div style="width:%dpx;height:%dpx;display:grid;place-items:center;background:%s"><img src="/assets/logo-mark.svg" style="width:%dpx;height:%dpx;display:block"></div></body></html>'''
h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(DIST)); http.server.SimpleHTTPRequestHandler.log_message = lambda *a: None
with socketserver.TCPServer(("127.0.0.1", 0), h) as srv:
    port = srv.server_address[1]; threading.Thread(target=srv.serve_forever, daemon=True).start()
    with sync_playwright() as p:
        b = p.chromium.launch()
        def shot(html, w, h, out, transparent=False):
            (DIST / "_x.html").write_text(html, encoding="utf-8")
            pg = b.new_page(viewport={"width": w, "height": h}); pg.goto(f"http://127.0.0.1:{port}/_x.html"); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(200)
            pg.screenshot(path=str(out), omit_background=transparent); pg.close()
        shot(OG, 1200, 630, A / "og.png")
        shot(ICON % (512, 512, "transparent", 512, 512), 512, 512, A / "_mark.png", True)
        shot(ICON % (180, 180, "#fff", 140, 140), 180, 180, A / "apple-touch-icon.png")
        shot(ICON % (512, 512, "#fff", 368, 368), 512, 512, A / "icon-512.png")
        b.close()
    srv.shutdown()
(DIST / "_x.html").unlink(missing_ok=True)
m = Image.open(A / "_mark.png").convert("RGBA")
Image.open(A / "icon-512.png").resize((192, 192), Image.LANCZOS).save(A / "icon-192.png")
m.save(A / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
(A / "_mark.png").unlink()
og = Image.open(A / "og.png").convert("RGB"); og.save(A / "og.png", optimize=True)
print("og.png, favicon.ico, apple-touch-icon.png, icon-192/512.png")
