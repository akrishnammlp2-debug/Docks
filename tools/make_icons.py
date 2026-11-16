# Festive home-screen icons: the Docks cat with one small prop per festival, in the icon's own flat style.
# Usage: python3 tools/make_icons.py   (needs playwright)  ->  icons/<theme>-180.png, icons/<theme>-512.png, /tmp/icons-sheet.png
import asyncio, os, re
from playwright.async_api import async_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
base = open(ROOT + '/icon.svg').read()
BG, K = '#ece9e2', '#121316'
def dots(pts, cols, r=7): return ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{cols[i % len(cols)]}"/>' for i, (x, y) in enumerate(pts))
def flag(bands, extra=''):
    h = 54 / len(bands)
    return ('<rect x="404" y="92" width="9" height="212" rx="4" fill="#8a6a45"/><circle cx="408.500" cy="90" r="8" fill="#d9a441"/>'
            + ''.join(f'<rect x="413" y="{104 + i * h:.1f}" width="78" height="{h + .5:.1f}" fill="{c}"/>' for i, c in enumerate(bands)) + extra)
swag = lambda: 'M40 44 Q148 124 256 60 T472 44'
def swag_pts(n):
    out = []
    for i in range(n):
        t = i / (n - 1); x = 40 + 432 * t
        y = (1 - (2 * t if t < .5 else 2 * t - 1)) ** 0 * 0  # placeholder
        u = 2 * t if t <= .5 else 2 * t - 1
        if t <= .5: y = (1 - u) ** 2 * 44 + 2 * (1 - u) * u * 124 + u * u * 60
        else: y = (1 - u) ** 2 * 60 + 2 * (1 - u) * u * (-4) + u * u * 44
        out.append((round(x), round(y)))
    return out
# Deco drawn OVER the cat unless noted
OVER = {
 'christmas': dots([(70, 90), (120, 200), (440, 70), (462, 190), (60, 250), (420, 250), (150, 60)], ['#ffffff'], 6) +
   '<path d="M196 112 C 214 40 300 18 352 62 C 384 90 392 124 388 150 L 356 150 C 352 120 340 108 318 128 Z" fill="#d8343a"/>'
   '<g transform="rotate(8 258 116)"><rect x="186" y="100" width="146" height="32" rx="16" fill="#ffffff"/></g>'
   '<circle cx="374" cy="158" r="20" fill="#ffffff"/>',
 'newyear': dots([(80, 80), (130, 170), (60, 230), (430, 90), (455, 200), (390, 150), (160, 50), (360, 50)], ['#f2c14e', '#e2557a', '#4aa3df', '#5fbf77'], 7) +
   '<path d="M256 12 L212 104 Q256 122 300 104 Z" fill="#7a5cc7"/><path d="M241 44 L271 44 L283 70 L229 70 Z" fill="#f2c14e"/><circle cx="256" cy="14" r="12" fill="#f2c14e"/>',
 'sankranti': '<path d="M404 150 C 380 200 420 230 396 262" fill="none" stroke="#8a6a45" stroke-width="4" stroke-linecap="round"/>'
   '<path d="M404 34 L456 92 L404 150 L352 92 Z" fill="#f2a541"/><path d="M404 34 L456 92 L404 92 Z" fill="#e25555"/><path d="M404 92 L404 150 L352 92 Z" fill="#5fbf77"/>'
   '<path d="M388 262 l16 -8 l-2 16 z" fill="#e25555"/>',
 'india': flag(['#ff9933', '#ffffff', '#138808'], '<rect x="413" y="104" width="78" height="54" fill="none" stroke="#c9c4b8" stroke-width="2"/><circle cx="452" cy="131" r="7" fill="none" stroke="#1a3a8a" stroke-width="2.5"/>'),
 'rajyotsava': flag(['#ffd400', '#e2231a']),
 'eid': '<circle cx="410" cy="100" r="46" fill="#e0a526"/><circle cx="428" cy="88" r="40" fill="%s"/>' % BG +
   '<path d="M436 96 l6 14 15 1 -12 10 4 15 -13 -8 -13 8 4 -15 -12 -10 15 -1 z" fill="#e0a526"/>' + dots([(90, 90), (130, 190), (70, 240)], ['#e0a526'], 5),
 'holi': '<circle cx="96" cy="110" r="38" fill="#ff6fb5"/><circle cx="130" cy="150" r="16" fill="#ff6fb5"/><circle cx="420" cy="84" r="34" fill="#4ac3f0"/><circle cx="452" cy="122" r="14" fill="#4ac3f0"/>'
   '<circle cx="86" cy="236" r="22" fill="#ffd23f"/><circle cx="438" cy="214" r="24" fill="#6fd97f"/><circle cx="150" cy="56" r="12" fill="#ffd23f"/><circle cx="366" cy="44" r="12" fill="#b07cf0"/>'
   '<circle cx="216" cy="196" r="13" fill="#ff6fb5"/><circle cx="298" cy="122" r="11" fill="#4ac3f0"/><circle cx="252" cy="262" r="12" fill="#ffd23f"/>',
 'ugadi': f'<path d="{swag()}" fill="none" stroke="#8a6a45" stroke-width="5" stroke-linecap="round"/>' +
   ''.join(f'<path d="M{x} {y} q-15 26 0 56 q15 -30 0 -56z" fill="{"#3f9b57" if i % 2 else "#5fbf77"}"/>' for i, (x, y) in enumerate(swag_pts(11)) if not 200 < x < 312),
 'dasara': f'<path d="{swag()}" fill="none" stroke="#5a8a3c" stroke-width="5" stroke-linecap="round"/>' +
   dots([p for p in swag_pts(15)], ['#f28c28', '#ffc93c'], 15),
 'janmashtami': '<g transform="rotate(24 300 110)"><path d="M300 150 L300 44" stroke="#3f8f6a" stroke-width="6" stroke-linecap="round"/>'
   '<ellipse cx="300" cy="40" rx="30" ry="42" fill="#3fae7a"/><ellipse cx="300" cy="44" rx="20" ry="28" fill="#f2c14e"/><ellipse cx="300" cy="48" rx="14" ry="19" fill="#2f7fd0"/><ellipse cx="300" cy="52" rx="8" ry="10" fill="#1b2a6b"/></g>'
   '<rect x="204" y="100" width="104" height="14" rx="7" fill="#f2c14e"/>',
 'ganesha': '<path d="M208 110 L216 52 L238 84 L256 40 L274 84 L296 52 L304 110 Z" fill="#f2b632"/><rect x="204" y="100" width="104" height="16" rx="8" fill="#d9952a"/>'
   '<circle cx="256" cy="74" r="8" fill="#d8343a"/><circle cx="256" cy="124" r="6" fill="#d8343a"/>'
   '<path d="M130 296 C 100 296 104 262 130 232 C 156 262 160 296 130 296 Z" fill="#fff6e6"/><path d="M130 232 v-10" stroke="#fff6e6" stroke-width="5" stroke-linecap="round"/>',
 'diwali': '<circle cx="134" cy="256" r="40" fill="#ffd36b" opacity=".35"/><path d="M134 222 C 150 244 146 262 134 268 C 122 262 118 244 134 222 Z" fill="#ffb629"/><path d="M134 244 C 141 254 139 262 134 266 C 129 262 127 254 134 244 Z" fill="#fff3c4"/>'
   '<path d="M96 272 Q134 312 172 272 Z" fill="#c9772b"/><rect x="94" y="266" width="80" height="10" rx="5" fill="#a85d1c"/>' +
   dots([(70, 80), (120, 140), (430, 80), (456, 180), (160, 50), (372, 46), (60, 190)], ['#ffd36b', '#f2a541'], 6),
}
def build(theme): return base.replace('</svg>', OVER[theme] + '</svg>')
async def main():
    os.makedirs(ROOT + '/icons', exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for t in OVER:
            for sz in (180, 512):
                pg = await b.new_page(viewport={'width': sz, 'height': sz})
                await pg.set_content(f'<body style="margin:0">{build(t).replace("<svg ", f"<svg width={sz} height={sz} ", 1)}</body>')
                await pg.screenshot(path=f'{ROOT}/icons/{t}-{sz}.png'); await pg.close()
        pg = await b.new_page(viewport={'width': 4 * 200 + 20, 'height': 3 * 226 + 20})
        cells = ''.join(f'<div style="display:inline-block;margin:10px;font:13px sans-serif;text-align:center"><div style="width:180px;height:180px;border-radius:40px;overflow:hidden">{build(t).replace("<svg ", "<svg width=180 height=180 ", 1)}</div>{t}</div>' for t in OVER)
        await pg.set_content(f'<body style="margin:0;background:#333;color:#fff">{cells}</body>'); await pg.screenshot(path='/tmp/icons-sheet.png'); await b.close()
asyncio.run(main())
