#!/usr/bin/env python3
"""
JALEP Corporação — brag video frame renderer (brag-slim path).
Every frame is a pure function of t (seconds). 1920x1080 @ 30fps, 21.0s.
Scene plan + beat locks in brag-plan.md / composition-brief.md.
"""
import os, math
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops

W, H = 1920, 1080
FPS = 30
DUR = 21.0
ROOT = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(ROOT, "assets", "fonts")

# ---- palette (from site CSS :root) ----
BG      = (14, 16, 25)       # #0E1019
CARD    = (24, 29, 50)       # #181D32
CARD2   = (30, 36, 64)       # #1E2440
PRIM    = (130, 177, 255)    # #82B1FF
PRIM_DIM= (130, 177, 255, 31)
CYAN    = (24, 255, 255)     # #18FFFF
VIOLET  = (179, 136, 255)    # #B388FF
GREEN   = (105, 240, 174)    # #69F0AE
AMBER   = (255, 215, 64)     # #FFD740
RED     = (255, 138, 128)    # #FF8A80
TXT     = (232, 236, 246)    # #E8ECF6
TXT2    = (144, 152, 184)    # #9098B8
MUT     = (92, 98, 128)      # #5C6280
BORDER  = (255, 255, 255, 15)

_font_cache = {}
def F(path, size):
    key = (path, size)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(os.path.join(FONTS, path), size)
    return _font_cache[key]

def sans(size):  return F("GoogleSansFlex-700.ttf", size)
def sans600(size): return F("GoogleSansFlex-600.ttf", size)
def sans500(size): return F("GoogleSansFlex-500.ttf", size)
def mono(size): return F("JetBrainsMono-700.ttf", size)
def mono600(size): return F("JetBrainsMono-600.ttf", size)
def mono500(size): return F("JetBrainsMono-500.ttf", size)
def mono400(size): return F("JetBrainsMono-400.ttf", size)
def icon(size): return F("MaterialSymbols.ttf", size)

ICONS = {  # name -> codepoint (from font cmap)
  "build":0xf8cd, "calendar":0xe935, "verified":0xef76, "school":0xe80c,
  "block":0xf08c, "up":0xe5d8, "laptop":0xe320, "desktop":0xe30c,
  "phone":0xe326, "trouble":0xe1d2, "more":0xe5d3, "spark":0xe65f,
  "calc":0xea5f, "dash":0xe871, "inv":0xe1a1, "chat":0xe0c9,
  "graph":0xef3e, "gear":0xe8b8, "sci":0xea4b, "chip":0xe322,
  "term":0xeb8e, "check":0xe668, "radio":0xe836, "person":0xf0d3,
}
def draw_icon(dr, name, cx, cy, size, fill):
    f = icon(int(size))
    ch = chr(ICONS[name])
    bb = dr.textbbox((0, 0), ch, font=f)
    w, h = bb[2]-bb[0], bb[3]-bb[1]
    dr.text((cx - w/2 - bb[0], cy - h/2 - bb[1]), ch, font=f, fill=fill)

# ---- easing ----
def clamp01(x): return max(0.0, min(1.0, x))
def ease_out(x): x = clamp01(x); return 1 - (1 - x) ** 3
def ease_in(x): x = clamp01(x); return x * x * x
def ease_io(x): x = clamp01(x); return 3*x*x - 2*x*x*x
def seg(t, t0, t1): return clamp01((t - t0) / max(1e-9, (t1 - t0)))
def lerp(a, b, u): return a + (b - a) * u
def lerp3(c1, c2, u): return tuple(int(round(lerp(a, b, u))) for a, b in zip(c1, c2))

# ---- helpers ----
def rr(dr, box, radius, **kw):
    dr.rounded_rectangle(box, radius=radius, **kw)

def text_center(dr, s, cx, cy, f, fill, anchor="mm"):
    dr.text((cx, cy), s, font=f, fill=fill, anchor=anchor)

def glow_dot(dr, cx, cy, r, color=PRIM, glow=8):
    for i in range(3, 0, -1):
        gr = r + i * glow / 2
        a = int(38 / i)
        dr.ellipse([cx-gr, cy-gr, cx+gr, cy+gr], fill=color + (a,))
    dr.ellipse([cx-r, cy-r, cx+r, cy+r], fill=color)

# RGBA overlay composited each frame (kept cheap: only where needed)
class Layer:
    def __init__(self, size=(W, H)):
        self.im = Image.new("RGBA", size, (0, 0, 0, 0))
        self.dr = ImageDraw.Draw(self.im)
    def composite(self, base):
        return Image.alpha_composite(base.convert("RGBA"), self.im)

def screen_paste(base, overlay_img, pos, alpha=1.0):
    """Screen-blend an RGB image (glyph on black) onto base at pos."""
    x, y = pos
    w, h = overlay_img.size
    region = base.crop((x, y, x+w, y+h))
    scr = ImageChops.screen(region, overlay_img)
    if alpha < 1:
        scr = Image.blend(region, scr, alpha)
    base.paste(scr, (x, y))

# ---- backgrounds ----
def base_bg(t):
    im = Image.new("RGBA", (W, H), BG + (255,))
    dr = ImageDraw.Draw(im)
    # faint grid — the site's tech aesthetic, breathing subtly with music energy
    # (audio-reactive: RMS proxy from beat phase)
    beat_phase = (t * 114.84 / 60.0) % 1.0
    rms = 0.55 + 0.20 * math.sin(2 * math.pi * beat_phase)
    gs = 64
    a_grid = int(7 + 4 * rms)
    for gx in range(0, W, gs):
        dr.line([(gx, 0), (gx, H)], fill=PRIM + (a_grid//2,), width=1)
    for gy in range(0, H, gs):
        dr.line([(0, gy), (W, gy)], fill=PRIM + (a_grid//2,), width=1)
    # vignette-ish radial: soft blue tint top-left, matching site wallpaper
    tint = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    tdr = ImageDraw.Draw(tint)
    for r in range(900, 0, -12):
        a = int(10 * (1 - r / 900))
        tdr.ellipse([90 - r, 60 - r, 90 + r, 60 + r], fill=(46, 60, 110, max(0, a)))
    im = Image.alpha_composite(im, tint)
    return im

# ---- shared scene chrome: nav bar ----
def draw_nav(dr, t, active=None):
    # top nav strip, styled like site nav-glass
    bar_h = 64
    ov = Layer((W, bar_h))
    odr = ov.dr
    odr.rectangle([0, 0, W, bar_h], fill=(18, 23, 42, 200))
    odr.line([(0, bar_h-1), (W, bar_h-1)], fill=PRIM + (28,), width=1)
    # logo text jalep//
    odr.text((40, bar_h//2), "jalep", font=mono500(22), fill=TXT, anchor="lm")
    wj = odr.textlength("jalep", font=mono500(22))
    odr.text((40+wj, bar_h//2), "//", font=mono500(22), fill=PRIM, anchor="lm")
    # right side: fake nav links
    links = ["Serviços", "Lab", "Preços", "Status"]
    x = W - 40
    for s in reversed(links):
        wl = odr.textlength(s, font=mono400(18))
        x -= wl
        odr.text((x, bar_h//2), s, font=mono400(18), fill=TXT2, anchor="lm")
        x -= 34
    return ov

# ---- SCENE 1: boot (0.0 - 3.0) ----
def scene1(t):
    im = base_bg(t)
    dr = ImageDraw.Draw(im, "RGBA")
    # typed jalep:// — chars appear over 0.25-1.35s, cursor blink
    s = "jalep://"
    n_chars = int(seg(t, 0.25, 1.35) * len(s) + 0.999)
    typed = s[:n_chars]
    fx, fy = W//2, H//2 - 40
    fw = dr.textlength(s, font=mono700 if False else mono(64))
    tx = fx - fw/2
    dr.text((tx, fy), typed, font=mono(64), fill=TXT, anchor="lm")
    # blinking cursor
    blink = (t % 0.8) < 0.45
    if blink and t < 2.6:
        cw = dr.textlength(s[:n_chars], font=mono(64))
        cx = tx + cw
        dr.rectangle([cx+4, fy-30, cx+16, fy+30], fill=PRIM)
    # blue dot pops at 1.60 (beat-locked)
    du = ease_out(seg(t, 1.60, 1.95))
    if du > 0:
        glow_dot(dr, W//2, H//2 + 60, 7*du, PRIM, 10*du)
    # tagline slides up + settles 1.9-2.6
    tu = ease_out(seg(t, 1.95, 2.55))
    if tu > 0:
        y = lerp(H//2 + 150, H//2 + 130, tu)
        a = int(255 * tu)
        # hero-tag style: dot + mono label
        label = "Assistência Técnica Profissional"
        f = mono500(30)
        lw = dr.textlength(label, font=f)
        dr.text((W//2 - lw/2, y), label, font=f, fill=TXT2 + (a,), anchor="lm")
    # music-reactive: subtle pulse on typed text glow after 1.6
    return im

# ---- SCENE 2: a empresa / stats (3.0 - 6.5) ----
STATS = [
    ("build",    "4",    "Serviços"),
    ("calendar", "2026", "Fundação"),
    ("verified", "100%", "Compromisso"),
    ("school",   "7",    "Turma"),
]
def scene2(t):
    im = base_bg(t)
    dr = ImageDraw.Draw(im, "RGBA")
    # kicker + title (site: section-kicker "serviços" style)
    ku = ease_out(seg(t, 3.0, 3.4))
    if ku > 0:
        a = int(255*ku)
        dr.text((W//2, 190), "números", font=mono500(24), fill=PRIM + (a,), anchor="mm")
        # section title
        f = sans(64)
        dr.text((W//2, 250), "A Empresa", font=f, fill=TXT + (a,), anchor="mm")
    # stat cards: beat-grid arrivals 3.18, 4.23, 5.28, 6.34
    times = [3.18, 4.23, 5.28, 6.34]
    cw, ch = 380, 220
    gap = 40
    total = 4*cw + 3*gap
    x0 = (W - total)/2
    y0 = 560
    for i, (ic, num, lab) in enumerate(STATS):
        u = ease_out(seg(t, times[i], times[i] + 0.45))
        if u <= 0: continue
        x = x0 + i*(cw+gap)
        # slide from left with fade
        xo = lerp(-60, 0, u)
        a = int(255 * u)
        box = [x+xo, y0, x+xo+cw, y0+ch]
        # card
        ov = Image.new("RGBA", (W, H), (0,0,0,0))
        odr = ImageDraw.Draw(ov)
        rr(odr, box, 20, fill=CARD + (a,), outline=PRIM + (int(a*0.28),), width=2)
        # icon
        draw_icon(odr, ic, x+xo+cw/2, y0+62, 40, PRIM + (a,))
        # number (counter: count-up over 0.6s after arrival)
        cu = ease_out(seg(t, times[i]+0.1, times[i]+0.7))
        if ic == "calendar":
            val = str(int(lerp(1990, 2026, cu))) if cu < 1 else "2026"
        elif ic == "verified":
            val = f"{int(lerp(0, 100, cu))}%"
        else:
            val = num
        f = sans(64)
        odr.text((x+xo+cw/2, y0+130), val, font=f, fill=TXT + (a,), anchor="mm")
        # label
        odr.text((x+xo+cw/2, y0+188), lab, font=mono400(22), fill=MUT + (a,), anchor="mm")
        im = Image.alpha_composite(im, ov)
    return im

# ---- SCENE 3: especificações (6.5 - 9.5) ----
def scene3(t):
    im = base_bg(t)
    dr = ImageDraw.Draw(im, "RGBA")
    # title
    ku = ease_out(seg(t, 6.5, 6.9))
    if ku <= 0: return im
    a0 = int(255*ku)
    dr.text((W//2, 190), "especificações", font=mono500(24), fill=PRIM + (a0,), anchor="mm")
    dr.text((W//2, 250), "Números", font=sans(64), fill=TXT + (a0,), anchor="mm")
    # left: spec bar "Taxa de Sucesso"
    bu = ease_out(seg(t, 6.9, 7.3))
    if bu > 0:
        a = int(255*bu)
        bx, by, bw, bh = 200, 450, 640, 18
        rr(dr, [bx, by, bx+bw, by+bh], 9, fill=CARD2 + (a,))
        # fill: 0->100% over 7.3-8.7, beat-lock landing at 8.96 strong cue
        fu = ease_io(seg(t, 7.3, 8.9))
        fw = int(bw * fu)
        if fw > 18:
            rr(dr, [bx, by, bx+fw, by+bh], 9, fill=PRIM + (a,))
        # labels
        dr.text((bx, by-40), "Taxa de Sucesso", font=mono500(28), fill=TXT2 + (a,), anchor="lm")
        dr.text((bx+bw, by-40), "100%", font=mono600(28), fill=PRIM + (a,), anchor="rm")
        # second bar: Precisão no Diagnóstico
        by2 = 620
        rr(dr, [bx, by2, bx+bw, by2+bh], 9, fill=CARD2 + (a,))
        fu2 = ease_io(seg(t, 7.6, 9.2))
        fw2 = int(bw * fu2)
        if fw2 > 18:
            rr(dr, [bx, by2, bx+fw2, by2+bh], 9, fill=PRIM + (a,))
        dr.text((bx, by2-40), "Precisão no Diagnóstico", font=mono500(28), fill=TXT2 + (a,), anchor="lm")
        dr.text((bx+bw, by2-40), "100%", font=mono600(28), fill=PRIM + (a,), anchor="rm")
    # right: glass card counting Improvisos 100->0, landing at 9.50 strong cue
    cu = seg(t, 8.9, 9.5)
    if cu > 0:
        v = int(round(lerp(100, 0, ease_io(cu))))
        # card
        cx0, cy0, cw2, ch2 = 1180, 420, 540, 300
        a = int(255 * ease_out(seg(t, 8.6, 9.0)))
        rr(dr, [cx0, cy0, cx0+cw2, cy0+ch2], 24, fill=CARD + (a,), outline=PRIM + (int(a*0.28),), width=2)
        draw_icon(dr, "block", cx0+cw2/2, cy0+70, 44, PRIM + (a,))
        f = sans(96)
        dr.text((cx0+cw2/2, cy0+160), str(v), font=f, fill=TXT + (a,), anchor="mm")
        dr.text((cx0+cw2/2, cy0+245), "Improvisos", font=mono400(26), fill=MUT + (a,), anchor="mm")
        # emphasis tick when 0 lands
        if v == 0:
            pu = seg(t, 9.5, 9.8)
            if pu < 1:
                r = int(120 + 40*pu)
                dr.ellipse([cx0+cw2/2-r, cy0+160-r, cx0+cw2/2+r, cy0+160+r], outline=PRIM + (int(120*(1-pu)),), width=3)
    return im

# ---- SCENE 4: orçamento IA (9.5 - 14.0) ----
SVC = [("up", "Upgrade"), ("build", "Reparo"), ("trouble", "Diagnóstico"), ("more", "Outro")]
DEV = [("laptop", "Notebook"), ("desktop", "Desktop"), ("phone", "Smartphone"), ("more", "Outro")]
def chip(dr, cx, cy, w, h, ic, label, state):
    """state: 0 hidden, 1 dim, 2 selected"""
    a = int(255 * state) if state < 1 else 255
    if state <= 0: return
    box = [cx-w/2, cy-h/2, cx+w/2, cy+h/2]
    if state >= 1.5:  # selected: blue dim bg + border + text
        rr(dr, box, 18, fill=PRIM + (36,), outline=PRIM + (72,), width=2)
        draw_icon(dr, ic, cx-40, cy, 20, PRIM)
        dr.text((cx-16, cy), label, font=mono500(20), fill=PRIM, anchor="lm")
        # dot indicator top-right
        dr.ellipse([cx+w/2-14, cy-h/2-6, cx+w/2+2, cy-h/2+10], fill=PRIM)
    else:  # unselected
        aa = int(255*state)
        rr(dr, box, 18, fill=CARD + (aa,), outline=(255,255,255, int(20*state)), width=1)
        draw_icon(dr, ic, cx-40, cy, 20, TXT2)
        dr.text((cx-16, cy), label, font=mono500(20), fill=TXT2, anchor="lm")

def cursor(dr, x, y, u=1.0):
    a = int(255 * u)
    # circle cursor with slight glow
    for r, aa in [(14, 40), (10, 90), (7, 255)]:
        dr.ellipse([x-r, y-r, x+r, y+r], fill=(255, 255, 255, int(aa * a / 255)))

def scene4(t):
    im = base_bg(t)
    dr = ImageDraw.Draw(im, "RGBA")
    ku = ease_out(seg(t, 9.5, 9.9))
    if ku <= 0: return im
    a0 = int(255*ku)
    dr.text((W//2, 170), "orçamento", font=mono500(24), fill=PRIM + (a0,), anchor="mm")
    dr.text((W//2, 230), "Simular Orçamento", font=sans(56), fill=TXT + (a0,), anchor="mm")
    # form panel (glass card)
    pu = ease_out(seg(t, 9.7, 10.2))
    if pu <= 0: return im
    a = int(255*pu)
    px, py, pw, ph = 320, 300, 1280, 640
    rr(dr, [px, py, px+pw, py+ph], 28, fill=CARD + (int(a*0.85),), outline=(255,255,255, int(14*a/255)), width=1)
    # label "Tipo de Serviço"
    dr.text((px+50, py+50), "Tipo de Serviço", font=mono500(24), fill=TXT2 + (a,), anchor="lm")
    # service chips row — appear staggered 10.0-10.3; cursor clicks Upgrade at 10.54 (beat)
    sw, sh = 250, 54
    row_y = py + 130
    for i, (ic, lab) in enumerate(SVC):
        cx = px + 60 + i*(sw+22)
        appear = ease_out(seg(t, 10.0 + i*0.1, 10.35 + i*0.1))
        selected = (i == 0) and t >= 10.54
        state = 2 if selected else (appear if appear > 0 else 0)
        # during 10.35-10.54 cursor hovers Upgrade chip
        chip(dr, cx, row_y, sw, sh, ic, lab, state)
    # label "Dispositivo"
    dr.text((px+50, py+230), "Dispositivo", font=mouse_font() if False else mono500(24), fill=TXT2 + (a,), anchor="lm")
    # device chips
    for i, (ic, lab) in enumerate(DEV):
        cx = px + 60 + i*(sw+22)
        appear = ease_out(seg(t, 10.7 + i*0.08, 11.0 + i*0.08))
        selected = (i == 0) and t >= 11.60
        state = 2 if selected else (appear if appear > 0 else 0)
        chip(dr, cx, py+310, sw, sh, ic, lab, state)
    # model input with typewriter "Acer Nitro V15"
    iu = seg(t, 11.9, 12.6)
    if iu > 0:
        ib = [px+50, py+390, px+pw-50, py+450]
        rr(dr, ib, 14, fill=CARD2 + (a,), outline=PRIM + (60,), width=1)
        model = "Acer Nitro V15 ANV15-51"
        n = int(seg(t, 11.95, 12.75) * len(model) + 0.999)
        if n > 0:
            dr.text((px+74, py+420), model[:n], font=mono400(22), fill=TXT + (a,), anchor="lm")
    # AI result card materializes 12.65 strong cue
    ru = ease_out(seg(t, 12.65, 13.15))
    if ru > 0:
        ra = int(255*ru)
        rx, ry, rw, rh = px+70, py+480, pw-140, 140
        # rise + fade
        yo = lerp(30, 0, ru)
        rr(dr, [rx, ry+yo, rx+rw, ry+yo+rh], 20, fill=PRIM + (26*ra//255,), outline=PRIM + (int(0.5*ra),), width=2)
        # content: RC case
        dr.text((rx+30, ry+yo+34), "RC-2025-0019", font=mono500(20), fill=PRIM + (ra,), anchor="lm")
        dr.text((rx+30, ry+yo+70), "Logitech MX Master 3S — RAM slot failure", font=mono500(24), fill=TXT + (ra,), anchor="lm")
        dr.text((rx+30, ry+yo+104), "R$ 441,39", font=sans600(34), fill=PRIM + (ra,), anchor="lm")
        # AI note
        dr.text((rx+rw-30, ry+yo+104), "gerado por IA", font=mono400(18), fill=MUT + (ra,), anchor="rm")
        # tiny check icon
        draw_icon(dr, "check", rx+rw-120, ry+yo+34, 22, GREEN + (ra,))
    # cursor path: hover Upgrade (10.35-10.54), click, hover Notebook (11.4-11.6), click, then exit
    cx, cy = None, None
    if 10.3 <= t < 11.9:
        if t < 10.54:   # move to Upgrade chip center then hold
            mu = ease_io(seg(t, 10.3, 10.5))
            cx = lerp(px+60+sw/2, px+60+sw/2, mu); cy = row_y
        elif t < 11.6:
            # click flash 10.54-10.66 then travel to Notebook
            tu = ease_io(seg(t, 10.7, 11.5))
            cx = lerp(px+60+sw/2, px+60+sw/2, tu); cy = lerp(row_y, py+310, tu)
        else:
            cx = px+60+sw/2; cy = py+310
    elif 11.9 <= t < 12.65:
        cx = lerp(px+60+sw/2, px+pw-260, ease_io(seg(t, 11.9, 12.2))); cy = lerp(py+310, py+300, 1)
    if cx is not None:
        cursor(dr, cx, cy)
    return im

def mouse_font():
    return mono500(24)

# ---- SCENE 5: JalepOS + Status (14.0 - 17.5) ----
OSAPPS = [("dash", "Dashboard"), ("inv", "Inventário"), ("chat", "Comunicação"), ("graph", "Analytics"), ("gear", "Config")]
STATUS = ["Diagnóstico Engine", "Lab API", "JalepOS Runtime"]
def scene5(t):
    im = base_bg(t)
    dr = ImageDraw.Draw(im, "RGBA")
    ku = ease_out(seg(t, 14.0, 14.4))
    if ku <= 0: return im
    a0 = int(255*ku)
    # LEFT: JalepOS window
    wx, wy, ww, wh = 140, 260, 760, 600
    wu = ease_out(seg(t, 14.1, 14.6))
    if wu > 0:
        a = int(255*wu)
        yo = lerp(40, 0, wu)
        rr(dr, [wx, wy+yo, wx+ww, wy+yo+wh], 22, fill=CARD + (a,), outline=(255,255,255, int(16*a/255)), width=1)
        # title bar
        rr(dr, [wx, wy+yo, wx+ww, wy+yo+64], 22, fill=CARD2 + (a,))
        dr.rectangle([wx, wy+yo+40, wx+ww, wy+yo+64], fill=CARD2 + (a,))
        # traffic lights
        for i, c in enumerate([RED, AMBER, GREEN]):
            dr.ellipse([wx+30+i*36, wy+yo+26-8, wx+30+i*36+16, wy+yo+26+8], fill=c + (a,))
        dr.text((wx+ww/2, wy+yo+32), "JalepOS v0.1", font=mono500(20), fill=TXT2 + (a,), anchor="mm")
        # desktop content: subtle grid + centered logo glyph
        draw_icon(dr, "term", wx+ww/2, wy+yo+300, 84, PRIM + (int(a*0.8),))
        dr.text((wx+ww/2, wy+yo+390), "JalepOS", font=sans600(34), fill=TXT + (a,), anchor="mm")
        dr.text((wx+ww/2, wy+yo+424), "scan: active", font=mono400(18), fill=MUT + (a,), anchor="mm")
        # dock icons pop one by one: beats 14.75, 15.28, 15.81, 16.34, 16.86
        times = [14.75, 15.28, 15.81, 16.34, 16.86]
        dw, dh = 64, 64
        dock_w = 5*dw + 4*18
        dx0 = wx + (ww - dock_w)/2
        dy = wy + yo + wh - 90
        for i, (ic, lab) in enumerate(OSAPPS):
            u = ease_out(seg(t, times[i], times[i]+0.35))
            if u <= 0: continue
            aa = int(255*u)
            cx = dx0 + i*(dw+18) + dw/2
            rr(dr, [cx-dw/2*u, dy-dh/2*u, cx+dw/2*u, dy+dh/2*u], 16, fill=CARD2 + (aa,), outline=PRIM + (int(0.4*aa),), width=1)
            draw_icon(dr, ic, cx, dy, 30*u, PRIM + (aa,))
    # RIGHT: status tiles flip to Operacional — beats 14.7, 15.8, 16.9 (every other beat)
    stimes = [14.7, 15.8, 16.9]
    tx0, ty0, tw, th, tgap = 1000, 300, 780, 150, 40
    for i, name in enumerate(STATUS):
        u = ease_out(seg(t, stimes[i], stimes[i]+0.45))
        if u <= 0: continue
        a = int(255*u)
        y = ty0 + i*(th+tgap)
        xo = lerp(50, 0, u)
        rr(dr, [tx0+xo, y, tx0+xo+tw, y+th], 20, fill=CARD + (a,), outline=(255,255,255, int(14*a/255)), width=1)
        # green dot + name
        glow_dot(dr, tx0+xo+50, y+th/2, 8, GREEN, 6)
        dr.text((tx0+xo+80, y+th/2), name, font=mono500(28), fill=TXT + (a,), anchor="lm")
        # status text right
        dr.text((tx0+xo+tw-40, y+th/2), "Operacional", font=mono500(24), fill=GREEN + (a,), anchor="rm")
        # progress bar blip
        bu = seg(t, stimes[i]+0.1, stimes[i]+0.5)
        rr(dr, [tx0+xo+80, y+th-24, tx0+xo+80+int(300*bu), y+th-16], 4, fill=GREEN + (int(120*bu),))
    # kicker
    dr.text((W//2, 170), "infraestrutura", font=mono500(24), fill=PRIM + (a0,), anchor="mm")
    return im

# ---- SCENE 6: punchline (17.5 - 21.0) ----
def scene6(t):
    im = base_bg(t)
    dr = ImageDraw.Draw(im, "RGBA")
    # logo slam at 17.91 (strong cue, beat-locked)
    lu = ease_out(seg(t, 17.75, 18.2))
    if lu > 0:
        a = int(255*lu)
        # big jalep// logo
        f = mono(110)
        s = "jalep//"
        w = dr.textlength(s, font=f)
        # slight scale-down settle (from 1.06 to 1.0)
        sc = lerp(1.06, 1.0, lu)
        f2 = F("JetBrainsMono-700.ttf", int(110*sc))
        w2 = dr.textlength(s, font=f2)
        dr.text((W//2 - w2/2, H//2 - 80), s, font=f2, fill=TXT + (a,), anchor="lm")
        # wordmark below
        f3 = sans600(44)
        s3 = "JALEP Corporação"
        w3 = dr.textlength(s3, font=f3)
        dr.text((W//2 - w3/2, H//2 + 40), s3, font=f3, fill=TXT2 + (a,), anchor="lm")
        # blue underline glow accent
        uw = 320 * lu
        dr.rounded_rectangle([W//2-uw/2, H//2+96, W//2+uw/2, H//2+102], 3, fill=PRIM + (int(200*lu),))
    # punchline fade 19.2-19.9, hold to end; music fades 19.5-21
    pu = ease_io(seg(t, 19.2, 19.9))
    if pu > 0:
        a = int(255*pu)
        f4 = mono500(28)
        s4 = "© 2026 — 7° Ano A"
        w4 = dr.textlength(s4, font=f4)
        dr.text((W//2 - w4/2, H//2 + 180), s4, font=f4, fill=MUT + (a,), anchor="lm")
    return im

SCENES = [(scene1, 0.0, 3.0), (scene2, 3.0, 6.5), (scene3, 6.5, 9.5), (scene4, 9.5, 14.0), (scene5, 14.0, 17.5), (scene6, 17.5, 21.0)]

def draw_frame(t):
    for fn, t0, t1 in SCENES:
        if t0 <= t < t1:
            im = fn(t)
            # global fade-in from black at start, fade-out at end
            if t < 0.4:
                u = t/0.4
                black = Image.new("RGBA", (W, H), (0,0,0,255))
                im = Image.blend(black, im, u)
            if t > DUR - 0.5:
                u = (DUR - t)/00.5 if False else (DUR - t)/0.5
                if u < 1:
                    black = Image.new("RGBA", (W, H), (0,0,0,255))
                    im = Image.blend(im, black, 1-u)
            return im.convert("RGB")
    return scene6(DUR - 1e-6).convert("RGB")

if __name__ == "__main__":
    import sys
    t = float(sys.argv[1]) if len(sys.argv) > 1 else 0.0
    out = sys.argv[2] if len(sys.argv) > 2 else "preview.png"
    draw_frame(t).save(out)
    print("wrote", out, "at t =", t)
