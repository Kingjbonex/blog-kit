---
name: pixel-gif
description: Make an 8-bit crab GIF (an Opus orchestrator crab, Sonnet worker crabs and you) that animates a post about working with AI agents, using crabkit.py in this skill's folder.
---

# Make a pixel crab GIF

These GIFs explain how you work with agents in a few seconds, for an X post or the top of a blog
post. The look is NES era: outlined sprites and an energy-bar HUD for progress, and a double-bordered
dialogue box for the words. Read `README.md` in this folder, especially **Style rules**, and the
scripts in `scenes/` first. Don't break the style rules (pixel grid, two fonts, fixed palette) to
make one scene easier.

Needs Python 3 and Pillow (`pip install pillow`).

1. **Storyboard from the post.** One scene per step or idea, plus a short intro (the post's hook)
   and an outro (its ending, usually a question to readers). The post's own words go in the
   dialogue box (`text=`, 3 lines of about 46 characters); in-scene bubbles are a few words. If the
   project has a voice guide (`writing/voice.md`), follow it for any new text.
2. **Cast.** Opus = `opus()` (crown, big). Sonnet workers = `sonnet()` (small), labeled "Sonnet
   1..n" when they need telling apart. The human = `person()` labeled "me"; redraw `PERSON` in
   `crabkit.py` once so it looks like the user. Issues are `card(..., accent=ORANGE)`, PRs
   `accent=BLUE`, problems `RED`. A new character or prop is a new `sprite()` grid with highlight,
   base and shadow colors from `PALETTE`.
3. **Write the script** at `scenes/<slug>.py`, saving to `gallery/<slug>.gif`. Make up example
   issue names only when the post doesn't give any, and say they're made up.
4. **Render with `--preview` and look at `gallery/preview.png`**, a contact sheet of frames. Use
   `m.still(i, path)` for a full-size look at a busy frame. Fix overlapping cards, bubbles running
   off the frame and text overflowing its box. Re-render until the sheet is clean.
5. **Deliver** the GIF with its length and size. Don't post it anywhere; the user posts it.

Keep it influenced, not borrowed: never use characters, items, logos, title fonts, music or sprites
from real games, and don't put game names in the GIF. Nothing should look official or imply that a
game studio or Anthropic made or endorsed it.
