"""Shared pieces for 8-bit crab GIFs (Opus orchestrator, Sonnet workers, and "me", the human).

Everything is drawn on a small native canvas (400x225) with hard pixels, no anti-aliasing, then
scaled up 2x with nearest neighbor, so bubbles, text and sprites all sit on the same pixel grid.
The look is NES era: black-outlined sprites, an energy bar for progress, READY, and a
double-bordered dialogue box with a typewriter and a blinking arrow.

    from crabkit import *
    m = Movie("Header text shown on every frame", steps=7)
    def s1(t, fr, d):              # t goes 0 -> 1 across the scene, fr is the global frame count
        opus(d, 200, GROUND, fr)
    m.scene(3.0, s1, step=1, stage="PLAN", text="1. Plan first. No code yet.")
    m.save("gallery/my-gif.gif")

See README.md for the design rules and the full list of helpers.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 400, 225          # native canvas; saved at SCALE x (800x450, 16:9)
SCALE = 2
FPS = 15
GROUND = 148             # top of the floor tiles; characters stand here
BOX_Y = 168              # top of the dialogue box

# Palette: every pixel in every frame is one of these, so the GIF never bands or flickers.
INK = (24, 16, 16)
WHITE = (248, 248, 248)
BG = (240, 232, 216)
TILE = (216, 200, 176); TILE_D = (176, 156, 128)
GREY = (168, 160, 160); GREY_D = (104, 96, 96)
ORANGE = (216, 112, 80); ORANGE_L = (240, 160, 128); ORANGE_D = (160, 72, 48)
SON = (232, 144, 112); SON_L = (248, 192, 168); SON_D = (184, 104, 72)
GOLD = (248, 200, 56); GOLD_D = (184, 128, 16)
BLUE = (32, 112, 224); BLUE_L = (96, 176, 248); BLUE_D = (16, 72, 144)
GREEN = (56, 160, 72); RED = (216, 56, 48); YELLOW = (248, 224, 96)
SKIN = (248, 192, 144); SKIN_D = (200, 136, 96); HAIR = (80, 48, 32); HAIR_L = (128, 80, 48)
PANTS = (56, 56, 80)
HOOD = (196, 170, 132); HOOD_L = (226, 206, 168); HOOD_D = (156, 128, 100)  # the avatar's tan hoodie
PALETTE = [INK, WHITE, BG, TILE, TILE_D, GREY, GREY_D, ORANGE, ORANGE_L, ORANGE_D, SON, SON_L,
           SON_D, GOLD, GOLD_D, BLUE, BLUE_L, BLUE_D, GREEN, RED, YELLOW, SKIN, SKIN_D, HAIR,
           HAIR_L, PANTS, HOOD, HOOD_L, HOOD_D]

# Fonts (both SIL OFL, in fonts/). BIG is Press Start 2P: dialogue, titles, card titles.
# SMALL is Silkscreen: HUD, labels, board rows. Both are drawn at their native 8px.
_HERE = os.path.dirname(os.path.abspath(__file__))
BIG = ImageFont.truetype(os.path.join(_HERE, "fonts", "PressStart2P-Regular.ttf"), 8)
BIG2 = ImageFont.truetype(os.path.join(_HERE, "fonts", "PressStart2P-Regular.ttf"), 16)
SMALL = ImageFont.truetype(os.path.join(_HERE, "fonts", "Silkscreen-Regular.ttf"), 8)
_DY = {id(SMALL): -4}    # Silkscreen draws its caps 4px low; pull it up so y is the cap top

def text(d, x, y, s, font=BIG, fill=INK, center=False):
    x = int(x - d.textlength(s, font=font) / 2) if center else int(x)
    d.text((x, int(y) + _DY.get(id(font), 0)), s, font=font, fill=fill)

def tw(d, s, font=BIG): return int(d.textlength(s, font=font))

# Easing and timing
def ease(t): t = max(0, min(1, t)); return t * t * (3 - 2 * t)
def lerp(a, b, t): return int(round(a + (b - a) * t))
def seg(t, a, b):
    """0 before a, eased 0->1 between a and b, 1 after b. Use it to stage things inside a scene."""
    return ease((t - a) / (b - a)) if b > a else float(t >= a)

# ---------------------------------------------------------------- sprites

def sprite(d, rows, x, y, s, colors, outline=INK):
    """Draw a sprite grid with its top-left at (x, y), s native px per sprite pixel. Each char maps
    through `colors`, '.' is transparent. Every transparent cell touching a filled one (4 ways) is
    drawn as outline, so the outline sits one sprite pixel outside the grid."""
    filled = {(r, c) for r, row in enumerate(rows) for c, ch in enumerate(row) if ch != "."}
    if outline:
        edge = {(r + dr, c + dc) for r, c in filled for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1))}
        for r, c in edge - filled:
            d.rectangle([x + c * s, y + r * s, x + c * s + s - 1, y + r * s + s - 1], fill=outline)
    for r, c in filled:
        d.rectangle([x + c * s, y + r * s, x + c * s + s - 1, y + r * s + s - 1], fill=colors[rows[r][c]])

CROWN = [
    "...G..GG..G...",
    "...GG.GG.GG...",
    "...GGGRRGGG...",
    "...gggggggg...",
]
CRAB = [
    "..hhhhhhhhhh..",
    "..OOOOOOOOOO..",
    "..OOEOOOOEOO..",
    "..OOEOOOOEOO..",
    "hhOOOOOOOOOOhh",
    "OOOOOOOOOOOOOO",
    "..OOOOOOOOOO..",
    "..dddddddddd..",
]
CRAB_BLINK = CRAB[:2] + ["..OOOOOOOOOO..", "..OOEOOOOEOO.."] + CRAB[4:]
LEGS = ["..d.d....d.d..", "..d.d....d.d.."]
LEGS_B = [".d..d....d..d.", ".d..d....d..d."]
OPUS_COLORS = {"O": ORANGE, "h": ORANGE_L, "d": ORANGE_D, "E": INK, "G": GOLD, "g": GOLD_D, "R": RED}
SON_COLORS = {"O": SON, "h": SON_L, "d": SON_D, "E": INK}

def _blink(frame, seed): return (frame + seed * 17) % 45 < 2

def crab(d, cx, by, s, frame, colors=OPUS_COLORS, crown=False, walk=False, label=None, seed=0):
    """Crab standing on y=by, centered on cx. Returns (cx, top y) for placing bubbles."""
    step = walk and (frame // 3) % 2
    body = CRAB_BLINK if _blink(frame, seed) else CRAB
    rows = (CROWN if crown else []) + body + (LEGS_B if step else LEGS)
    x = cx - 7 * s; y = by - len(rows) * s - (s if step else 0)
    sprite(d, rows, x, y, s, colors)
    if label: text(d, cx, by + 4, label, SMALL, center=True)
    return (cx, y - s)

def opus(d, cx, by, frame, s=3, label="OPUS", **kw):
    return crab(d, cx, by, s, frame, OPUS_COLORS, crown=True, label=label, **kw)

def sonnet(d, cx, by, frame, s=2, label=None, seed=1, **kw):
    return crab(d, cx, by, s, frame, SON_COLORS, label=label, seed=seed, **kw)

PERSON = [
    "...CCCCCC...",
    "..CCCCCCCC..",
    ".cCCCooCCCc.",
    ".cccccccccc.",
    ".HSSSSSSSSH.",
    ".HSESSSSESH.",
    "..SSSSSSSS..",
    "..HSHHHHSH..",
    "...HHHHHH...",
    "..LTTTTTTD..",
    ".LLTTTTTTDD.",
    "SLLTTTTTTDDS",
    "SLTTTTTTTTDS",
    "..TTTTTTTT..",
    "..DDDDDDDD..",
    "..PPPPPPPP..",
    "..PPP..PPP..",
    ".WWWW..WWWW.",
]
PERSON_BLINK = PERSON[:5] + [".HSSSSSSSSH."] + PERSON[6:]
PERSON_STEP = PERSON[:16] + ["..PPP...PPP.", ".WWWW...WWWW"]
PERSON_COLORS = {"C": WHITE, "c": GREY, "o": HAIR, "H": HAIR, "S": SKIN, "E": INK, "T": HOOD,
                 "L": HOOD_L, "D": HOOD_D, "P": PANTS, "W": WHITE}

def person(d, cx, by, frame, s=2, label="ME", walk=False, seed=2):
    """The human ("me"): white cap worn backwards, brown beard, tan hoodie. Redraw PERSON to look like you."""
    rows = PERSON_STEP if walk and (frame // 3) % 2 else (PERSON_BLINK if _blink(frame, seed) else PERSON)
    y = by - len(rows) * s
    sprite(d, rows, cx - 6 * s, y, s, PERSON_COLORS)
    if label: text(d, cx, by + 4, label, SMALL, center=True)
    return (cx, y - s)

CHECK = ["......G", ".....GG", "G...GG.", "GG.GG..", ".GGG...", "..G...."]
def check(d, cx, cy, s=1):
    sprite(d, CHECK, cx - 3 * s, cy - 3 * s, s, {"G": GREEN})

def spinner(d, cx, cy, frame):
    """Four dots chasing each other, like a loading cursor."""
    pts = [(0, -3), (3, 0), (0, 3), (-3, 0)]
    for i, (dx, dy) in enumerate(pts):
        c = INK if i == (frame // 2) % 4 else GREY
        d.rectangle([cx + dx - 1, cy + dy - 1, cx + dx, cy + dy], fill=c)

# ---------------------------------------------------------------- boxes and bubbles

def pbox(d, x0, y0, x1, y1, fill=WHITE, outline=INK, corner=1):
    """Pixel box: 1px outline with the corners notched, so it reads as rounded on the grid."""
    x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
    d.rectangle([x0 + 1, y0 + 1, x1 - 1, y1 - 1], fill=fill)
    c = corner
    d.line([(x0 + c, y0), (x1 - c, y0)], fill=outline); d.line([(x0 + c, y1), (x1 - c, y1)], fill=outline)
    d.line([(x0, y0 + c), (x0, y1 - c)], fill=outline); d.line([(x1, y0 + c), (x1, y1 - c)], fill=outline)
    if c > 1:
        for k in range(1, c):
            d.point([(x0 + k, y0 + c - k), (x1 - k, y0 + c - k), (x0 + k, y1 - c + k), (x1 - k, y1 - c + k)], fill=outline)

def bubble(d, x, y, s, font=BIG, fill=WHITE, fg=INK, tail=True):
    """Speech balloon whose tail tip is at (x, y). Keep lines short: a few words."""
    w = tw(d, s, font) + 8; h = 14 if font is BIG else 11
    bx = max(2, min(W - w - 2, x - w // 2)); top = y - 4 - h
    pbox(d, bx, top, bx + w, top + h, fill=fill, corner=2)
    if tail:
        for k in range(4):
            d.line([(x - 3 + k, top + h + k), (x + 3 - k, top + h + k)], fill=fill)
            d.point([(x - 4 + k, top + h + k), (x + 4 - k, top + h + k)], fill=INK)
        d.point((x, top + h + 4), fill=INK)
        d.line([(x - 3, top + h), (x + 3, top + h)], fill=fill)
    text(d, bx + 5, top + (4 if font is BIG else 4), s, font, fg)

def emote(d, x, y, mark="!", color=RED):
    """Emote balloon above a character: '!', '?', '...'."""
    pbox(d, x - 6, y - 16, x + 6, y - 4, corner=2)
    d.line([(x - 1, y - 4), (x + 1, y - 4)], fill=WHITE); d.point([(x - 2, y - 3), (x + 2, y - 3)], fill=INK)
    d.point((x - 1, y - 3), fill=WHITE); d.point((x + 1, y - 3), fill=WHITE); d.point((x, y - 2), fill=INK)
    text(d, x - 3 if mark != "..." else x - 5, y - 14, mark, BIG if mark != "..." else SMALL, color)

def card(d, x, y, title, lines=(), accent=ORANGE, font=BIG, w=None):
    """Issue or PR card. accent: ORANGE issue, BLUE PR, RED problem. Width fits the text unless
    w is given; height follows the lines. Returns (w, h)."""
    if w is None: w = max([tw(d, title, font)] + [tw(d, l, SMALL) for l in lines]) + 12
    h = 13 + 9 * len(lines) if font is BIG else 11 + 9 * len(lines)
    pbox(d, x, y, x + w, y + h, corner=2)
    d.rectangle([x + 1, y + 2, x + 3, y + h - 2], fill=accent)
    text(d, x + 7, y + 3, title, font)
    for k, ln in enumerate(lines):
        text(d, x + 7, y + (13 if font is BIG else 11) + 9 * k, ln, SMALL, GREY_D)
    return w, h

def pill(d, x, y, s, fill=GREEN, fg=WHITE):
    w = tw(d, s, SMALL) + 8
    pbox(d, x, y, x + w, y + 10, fill=fill, outline=INK, corner=2)
    text(d, x + 4, y + 3, s, SMALL, fg)

def board(d, x, y, title, rows, frame=0, w=112):
    """'Who has what' board. rows = [(id, text, state)], state in work / q / done / ''."""
    pbox(d, x, y, x + w, y + 15 + 11 * len(rows), corner=2)
    text(d, x + 5, y + 4, title, SMALL)
    d.line([(x + 4, y + 11), (x + w - 4, y + 11)], fill=GREY)
    for k, (a, b, st) in enumerate(rows):
        yy = y + 15 + 11 * k
        text(d, x + 5, yy, a, SMALL); text(d, x + 28, yy, b, SMALL, GREY_D)
        if st == "work": spinner(d, x + w - 8, yy + 2, frame + k)
        elif st == "q": text(d, x + w - 11, yy - 1, "?", BIG, RED)
        elif st == "done": check(d, x + w - 9, yy + 2)

def platform(d, cx, y, tiles=3):
    """Floating platform for a character to stand on (top at y)."""
    w = tiles * 12; x0 = cx - w // 2
    d.rectangle([x0, y, x0 + w - 1, y + 5], fill=GREY_D); d.rectangle([x0, y, x0 + w - 1, y + 1], fill=GREY)
    for k in range(1, tiles): d.line([(x0 + k * 12, y + 2), (x0 + k * 12, y + 5)], fill=INK)
    d.rectangle([x0 - 1, y - 1, x0 + w, y + 6], outline=INK)

def floor(d):
    d.rectangle([0, GROUND, W, BOX_Y - 1], fill=TILE)
    d.line([(0, GROUND), (W, GROUND)], fill=INK)
    d.line([(0, GROUND + 1), (W, GROUND + 1)], fill=WHITE)
    for row, yy in enumerate(range(GROUND + 2, BOX_Y, 8)):
        d.line([(0, yy + 7), (W, yy + 7)], fill=TILE_D)
        for xx in range((row % 2) * 8, W, 16): d.line([(xx, yy), (xx, yy + 6)], fill=TILE_D)

def dialogue(d, s, p=1.0, frame=0, name=None):
    """Double-bordered dialogue box along the bottom. p (0..1) reveals the text like a typewriter; once it's
    all out, the arrow blinks. Wraps to 3 lines of BIG (about 46 characters each)."""
    x0, y0, x1, y1 = 2, BOX_Y, W - 3, H - 3
    pbox(d, x0, y0, x1, y1, fill=WHITE, corner=3)
    pbox(d, x0 + 2, y0 + 2, x1 - 2, y1 - 2, fill=WHITE, outline=INK, corner=2)
    if name:
        nw = tw(d, name, SMALL) + 10
        pbox(d, x0 + 8, y0 - 9, x0 + 8 + nw, y0 + 2, fill=YELLOW, corner=2)
        text(d, x0 + 13, y0 - 5, name, SMALL)
    lines = wrap(d, s, x1 - x0 - 22)
    shown = int(round(len(s) * max(0, min(1, p))))
    for k, ln in enumerate(lines[:3]):
        take = max(0, min(len(ln), shown)); shown -= len(ln) + 1
        text(d, x0 + 10, y0 + 10 + 13 * k, ln[:take])
    if p >= 1 and (frame // 5) % 2 == 0:
        ax, ay = x1 - 12, y1 - 10
        for k in range(4): d.line([(ax - 3 + k, ay + k), (ax + 3 - k, ay + k)], fill=INK)

def wrap(d, s, width, font=BIG):
    out, cur = [], ""
    for word in s.split():
        nxt = (cur + " " + word).strip()
        if tw(d, nxt, font) <= width: cur = nxt
        else: out.append(cur); cur = word
    return out + ([cur] if cur else [])

def title_card(d, lines, y=40, font=BIG2, gap=6):
    h = font.size + gap
    for i, ln in enumerate(lines): text(d, W // 2, y + i * h, ln, font, center=True)

def ready(d, frame, y=100):
    """READY, blinking."""
    if (frame // 4) % 2 == 0: text(d, W // 2, y, "READY", BIG, BLUE, center=True)


class Movie:
    def __init__(self, header, steps=None, fps=FPS):
        self.header, self.steps, self.fps = header.upper(), steps, fps
        self.frames = []

    def base(self, step, stage, show_floor, hud=None):
        im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im); d.fontmode = "1"
        text(d, 6, 5, self.header, SMALL, GREY_D)
        if self.steps:
            # Energy bar: one cell per step, filled up to the current one.
            cw = 5; x1 = W - 6; x0 = x1 - self.steps * (cw + 1) - 1
            d.rectangle([x0, 3, x1, 12], fill=INK)
            for k in range(self.steps):
                cx = x0 + 1 + k * (cw + 1)
                if step and k < step:
                    d.rectangle([cx, 4, cx + cw - 1, 11], fill=YELLOW)
                    d.rectangle([cx + 1, 4, cx + cw - 2, 11], fill=WHITE)
            label = f"STAGE {step}" + (f" {stage}" if stage else "") if step else (stage or "")
            label = hud or label
            if label: text(d, x0 - 4 - tw(d, label, SMALL), 5, label, SMALL)
        d.line([(0, 15), (W, 15)], fill=TILE_D)
        if show_floor: floor(d)
        return im, d

    def scene(self, seconds, draw, step=None, stage=None, text=None, name=None, type_until=0.45,
              floor=True, hud=None):
        """draw(t, frame, d) paints over the base. `text` goes in the dialogue box and types out
        over the first `type_until` of the scene. `hud` replaces the "STAGE n NAME" label."""
        n = max(2, int(seconds * self.fps))
        for i in range(n):
            t = i / (n - 1); fr = len(self.frames)
            im, d = self.base(step, stage, floor, hud)
            draw(t, fr, d)
            if text: dialogue(d, text, t / type_until if type_until else 1, fr, name)
            d.rectangle([0, 0, W - 1, H - 1], outline=INK)   # frame edge, reads on light and dark
            self.frames.append(im)

    def save(self, path, hold_last_ms=2500, preview=None):
        """Write the GIF at SCALE x. preview="x.png" also writes a 4x4 contact sheet."""
        pal = Image.new("P", (1, 1))
        flat = [v for c in PALETTE for v in c]; pal.putpalette(flat + flat[:3] * (256 - len(PALETTE)))
        big = [f.resize((W * SCALE, H * SCALE), Image.NEAREST) for f in self.frames]
        if preview:
            sheet = Image.new("RGB", (W * 4, H * 4))
            for i in range(16):
                sheet.paste(self.frames[i * (len(big) - 1) // 15], ((i % 4) * W, (i // 4) * H))
            sheet.resize((W * 4, H * 4), Image.NEAREST).save(preview)
        q = [f.quantize(palette=pal, dither=Image.Dither.NONE) for f in big]
        durs = [int(1000 / self.fps)] * len(q); durs[-1] = hold_last_ms
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        q[0].save(path, save_all=True, append_images=q[1:], duration=durs, loop=0, optimize=True)
        print(f"{path}: {len(q)} frames, {len(q) / self.fps:.1f}s, {os.path.getsize(path) // 1024} KB")

    def still(self, i, path):
        """Save one frame at full size, for checking details."""
        self.frames[i].resize((W * SCALE, H * SCALE), Image.NEAREST).save(path)
