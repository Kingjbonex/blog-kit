"""X post, Oct 2026: "How I let Opus run a team of Sonnet agents" (Option A, 7 steps)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from crabkit import *

m = Movie("How I let Opus run a team of Sonnet agents", steps=7)
ISSUES = ["#12 DARK MODE", "#13 RSS FEED", "#14 TAG PAGES", "#15 OG IMAGES", "#16 404 PAGE"]
OP = (60, GROUND)                 # Opus's spot in the team scenes
SX, PLAT = 196, [50, 90, 130]     # Sonnet x, and the tops of their platforms

def intro(t, fr, d):
    title_card(d, ["How I let Opus", "run a team of", "Sonnet agents"], y=24)
    opus(d, lerp(-30, 110, seg(t, 0, 0.55)), GROUND, fr, walk=t < 0.55)
    for k in range(3):
        a = 0.1 + k * 0.08
        sonnet(d, lerp(W + 20 + k * 30, 230 + k * 50, seg(t, a, a + 0.5)), GROUND, fr, seed=k,
               walk=t < a + 0.5)
    if t > 0.6: ready(d, fr, y=96)
m.scene(3.4, intro, text="(and stay out of the way)", name="JAMES", type_until=0.5)

def s1(t, fr, d):
    person(d, 70, GROUND, fr)
    opus(d, 330, GROUND, fr)
    pbox(d, 150, 26, 250, 128, corner=2)
    text(d, 200, 32, "PLAN", BIG, center=True)
    for k in range(int(seg(t, 0.1, 0.9) * 6)):
        d.rectangle([160, 48 + k * 13, 160 + [70, 52, 80, 40, 64, 56][k], 50 + k * 13], fill=GREY_D)
    if 0.05 < t < 0.35: bubble(d, 70, GROUND - 42, "what if we...")
    if 0.35 < t < 0.65: bubble(d, 330, GROUND - 52, "ok, but then...")
    if 0.65 < t < 0.95: bubble(d, 70, GROUND - 42, "no code yet!")
m.scene(4.0, s1, 1, "PLAN", "1. Plan first. Opus and I talk it through. No code yet.")

def s2(t, fr, d):
    opus(d, 40, GROUND, fr)
    if t < 0.3:
        sc = 1 - 0.4 * seg(t, 0, 0.25)
        pbox(d, 230 - 50 * sc, 77 - 50 * sc, 230 + 50 * sc, 77 + 50 * sc, corner=2)
        text(d, 230, 77 - 50 * sc + 6, "PLAN", BIG, center=True)
    for k, name in enumerate(ISSUES):
        q = seg(t, 0.25 + k * 0.1, 0.45 + k * 0.1)
        if q > 0:
            tx, ty = 100 + (k % 3) * 100, 32 + (k // 3) * 46
            card(d, lerp(200, tx, q), lerp(70, ty, q), name, ["ONE CHANGE"], font=SMALL, w=88)
m.scene(4.0, s2, 2, "ISSUES", "2. Opus splits the plan into small issues. One change each, ideally one PR.")

def s3(t, fr, d):
    g = seg(t, 0, 0.2)
    x0, y0, x1, y1 = lerp(150, 20, g), lerp(60, 22, g), lerp(250, 350, g), lerp(90, 140, g)
    pbox(d, x0, y0, x1, y1, corner=2)
    d.rectangle([x0 + 1, y0 + 2, x0 + 3, y1 - 2], fill=ORANGE)
    if g >= 1:
        text(d, x0 + 10, y0 + 8, "#12 Add a dark mode toggle")
        rows = [("WHAT", "a toggle in the header that flips the theme"),
                ("WHERE", "layouts/partials/header.html"),
                ("DONE WHEN", "the choice sticks after a reload")]
        for k, (a, b) in enumerate(rows):
            q = seg(t, 0.25 + k * 0.18, 0.37 + k * 0.18)
            if q > 0:
                yy = y0 + 28 + k * 26
                text(d, x0 + 10, yy, a, SMALL, ORANGE_D)
                text(d, x0 + 10, yy + 10, b[: int(len(b) * q)], SMALL)
        if t > 0.85: pill(d, x1 - 68, y0 + 6, "AGENT-READY")
    opus(d, 376, GROUND, fr, label=None, s=2)
m.scene(4.4, s3, 3, "WRITE IT UP", "3. Each issue is written like the agent knows nothing: what, where, and how we'll know it's done.")

def team(d, fr, cards=None, accent=ORANGE):
    opus(d, *OP, fr)
    for k, py in enumerate(PLAT):
        platform(d, SX, py)
        sonnet(d, SX, py, fr, seed=k + 1)
        text(d, SX - 26, py - 12, str(k + 1), SMALL, GREY_D)
        if cards and cards[k]: card(d, SX + 24, py - 20, cards[k], accent=accent, font=SMALL)

def s4(t, fr, d):
    held, rows = [None] * 3, []
    for k, py in enumerate(PLAT):
        q = seg(t, 0.1 + k * 0.25, 0.3 + k * 0.25)
        if q >= 1:
            held[k] = ISSUES[k]; rows.append((ISSUES[k][:3], f"SONNET {k + 1}", "work"))
    team(d, fr, held)
    for k, py in enumerate(PLAT):
        q = seg(t, 0.1 + k * 0.25, 0.3 + k * 0.25)
        if 0 < q < 1: card(d, lerp(OP[0], SX + 24, q), lerp(GROUND - 60, py - 20, q), ISSUES[k], font=SMALL)
    board(d, 6, 22, "WHO HAS WHAT", rows, fr, w=104)
m.scene(4.4, s4, 4, "HANDOFF", "4. Opus starts a Sonnet session per agent-ready issue and keeps a checklist of who has what.")

def s5(t, fr, d):
    team(d, fr, ISSUES[:3])
    person(d, 370, GROUND, fr)
    st = ["work", "work", "work"]
    if 0.05 < t < 0.45:
        st[1] = "q"; emote(d, SX + 16, PLAT[1] - 16, "?")
    if 0.12 < t < 0.24: bubble(d, SX, PLAT[1] - 24, "which CSS var?", SMALL)
    if 0.24 < t < 0.45: bubble(d, OP[0], GROUND - 46, "it's in the plan", SMALL)
    if t > 0.5:
        st[2] = "q"; emote(d, SX + 16, PLAT[2] - 16, "?")
    if 0.5 < t < 0.62: bubble(d, SX, PLAT[2] - 24, "rename the feed URL?", SMALL)
    if 0.62 < t < 0.76: bubble(d, OP[0], GROUND - 46, "that's James's call", SMALL)
    if t > 0.72:
        q = seg(t, 0.72, 0.86)
        pill(d, lerp(OP[0], 352, q), lerp(GROUND - 60, GROUND - 64, q), "PING!", fill=RED)
    if t > 0.86:
        emote(d, 370, GROUND - 38, "!")
        pill(d, 300, GROUND - 76, "NEEDS-DECISIONS", fill=YELLOW, fg=INK)
    board(d, 6, 22, "WHO HAS WHAT",
          [(ISSUES[k][:3], f"SONNET {k + 1}", st[k]) for k in range(3)], fr, w=104)
m.scene(5.4, s5, 5, "UNBLOCK", "5. When a worker gets stuck, it asks Opus, not me. Opus answers from the plan, or pings me if it's a real call.")

def s6(t, fr, d):
    prs = [f"PR #{40 + k} " + ISSUES[k].split(" ", 1)[1] for k in range(3)]
    team(d, fr, prs, accent=BLUE)
    rows = []
    for k, py in enumerate(PLAT):
        w = tw(d, prs[k], SMALL) + 12
        if t < 0.5 + k * 0.12:
            spinner(d, SX + 24 + w + 8, py - 14, fr + k); rows.append((f"#{40 + k}", "CI RUNNING", "work"))
        else:
            check(d, SX + 24 + w + 9, py - 14); rows.append((f"#{40 + k}", "CI GREEN", "done"))
    board(d, 6, 22, "WHO HAS WHAT", rows, fr, w=104)
m.scene(4.0, s6, 6, "CI", "6. Every worker opens a PR. CI runs on all of them.")

def s7(t, fr, d):
    opus(d, 40, GROUND, fr)
    d.rectangle([110, 30, 392, 33], fill=GREY_D); d.line([(110, 30), (392, 30)], fill=INK)
    text(d, 110, 21, "MAIN", SMALL)
    names = ["PR #40", "PR #41", "PR #42"]
    what = ["DARK MODE", "RSS FEED", "TAG PAGES"]
    files = ["header.html", "config.toml", "header.html"]
    start = [(120, 100), (250, 62), (250, 104)]
    for k in range(3):
        ex = 120 + k * 90
        q = seg(t, 0.45 + k * 0.12, 0.6 + k * 0.12)
        acc = RED if 0.12 < t < 0.45 and k in (0, 2) else BLUE
        w, _ = card(d, lerp(start[k][0], ex, q), lerp(start[k][1], 42, q), names[k], [what[k], files[k]],
                    accent=acc, font=SMALL, w=70)
        if q >= 1:
            done = t > 0.75 + k * 0.08
            pbox(d, ex + 31, 27, ex + 39, 36, fill=GREEN if done else WHITE)
            text(d, ex + 33, 30, str(k + 1), SMALL, WHITE if done else INK)
    if 0.12 < t < 0.45:
        d.line([(190, 116), (250, 120)], fill=RED)
        bubble(d, 220, 112, "same file!", SMALL, fg=RED)
    if 0.25 < t < 0.5: bubble(d, 40, GROUND - 46, "#40 first, then #42", SMALL)
m.scene(5.0, s7, 7, "MERGE", "7. Opus watches for PRs that touch the same files and picks the merge order.")

def outro(t, fr, d):
    title_card(d, ["I mostly read logic", "and make calls."], y=30)
    person(d, 200, GROUND, fr)
    opus(d, 110, GROUND, fr, label=None, walk=True)
    for k in range(3): sonnet(d, 260 + k * 40, GROUND, fr + k * 2, seed=k, walk=True)
    if t > 0.75: emote(d, 200, GROUND - 40, "?", BLUE)
m.scene(5.0, outro, step=7, hud="ALL CLEAR", text="(Turns out I'm the bottleneck, not the agents.) What would you add?",
        name="JAMES", type_until=0.6)

here = os.path.dirname(__file__)
m.save(os.path.join(here, "..", "gallery", "opus-runs-sonnet-agents.gif"),
       preview=os.path.join(here, "..", "gallery", "preview.png") if "--preview" in sys.argv else None)
