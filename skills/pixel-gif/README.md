# Pixel GIFs

8-bit crab animations for X posts and blog posts about working with AI agents. Opus is the big crab
with the crown, the Sonnet agents are the small crabs, and the human is the little guy in the white
cap and tan hoodie (that's me; redraw `PERSON` in `crabkit.py` to make it you).

![Opus runs a team of Sonnet agents](gallery/opus-runs-sonnet-agents.gif)

## Style rules

The look is NES era: outlined sprites and an energy-bar HUD, and a double-bordered text box. These are the
decisions that keep every GIF looking like the same game.

1. **One pixel grid.** Everything is drawn on a 400x225 canvas with no anti-aliasing and scaled
   up 2x with nearest neighbor. Never draw at the output size, and never use smooth shapes or
   regular fonts; they break the grid.
2. **Two pixel fonts, both at 8px.** `BIG` (Press Start 2P) for dialogue, titles and card
   titles; `BIG2` (16px) only for title cards. `SMALL` (Silkscreen, caps only) for the HUD,
   labels and board rows. Both are SIL OFL and live in `fonts/`.
3. **Fixed palette.** Every color is in `PALETTE` (29 colors). Need a new one? Add it there,
   don't inline an RGB tuple.
4. **Sprites have black outlines.** `sprite()` adds them automatically, one sprite
   pixel thick. Body colors come in threes: highlight, base, shadow.
5. **Cast.** Opus: big orange crab with a gold crown, sprite pixel size 3. Sonnet workers:
   lighter crabs, size 2, standing on floating platforms when they're at work. The human (`person()`): white
   cap worn backwards, brown beard, tan hoodie by default, size 2. Everyone blinks now and then and can `walk=True`.
6. **The post's words go in the dialogue box**, typed out with a blinking arrow when
   done. Name tab (`name="ME"`, or your name) when you're speaking in first person.
7. **In-scene talk is short.** `bubble()` for a few words, `emote()` for `!` `?` `...` above a
   head. Anything longer belongs in the dialogue box.
8. **HUD shows progress like an energy bar.** One cell per step, `STAGE n NAME` beside it,
   `hud="ALL CLEAR"` on the last scene.
9. **Things the agents make are cards.** Stripe colors: orange issue, blue PR, red problem.
   Status uses spinner (working), red `?` (stuck), green check (done).
10. **Its own background and a 1px black frame**, so it reads the same on X's light and dark
    themes and on the blog's light and dark themes.

## Make one

```sh
pip install pillow
python3 scenes/opus-runs-sonnet-agents.py --preview
```

The GIF lands in `gallery/`. `--preview` also writes `gallery/preview.png`, a 4x4 contact sheet of
frames across the whole movie, so you can check the layout without scrubbing through the GIF
(it's gitignored).

For a new one, copy a script in `scenes/` and change the scenes. Each scene is a function
`draw(t, frame, d)` on the 400x225 canvas, where `t` runs from 0 to 1 across the scene and
`seg(t, a, b)` stages things inside it (0 before `a`, eases to 1 by `b`). The floor is drawn for
you; characters stand on `GROUND`, and the dialogue box starts at `BOX_Y`.

```python
m = Movie("Header on every frame", steps=3)
def s1(t, fr, d):
    opus(d, 80, GROUND, fr)
    sonnet(d, lerp(420, 250, seg(t, 0, 0.5)), GROUND, fr, walk=t < 0.5)
    if t > 0.5: bubble(d, 250, GROUND - 30, "on it!")
m.scene(3.0, s1, step=1, stage="HANDOFF", text="1. Opus hands off the work. One issue per agent.")
m.save("gallery/my-gif.gif")
```

## What's in `crabkit.py`

| Helper | What it draws |
| --- | --- |
| `opus`, `sonnet`, `person` | The cast. `walk=True` animates; `label=` puts a name under them. |
| `sprite` | Any sprite grid, outlined. Use it for new characters and props. |
| `dialogue` | Double-bordered text box (the `Movie` draws it for you from `text=`). |
| `bubble`, `emote` | Short speech, and `!` `?` `...` balloons. |
| `card`, `board`, `pill` | Issue/PR cards, the "who has what" board, labels. |
| `check`, `spinner`, `platform` | Done, working, and a floating platform. |
| `title_card`, `ready` | Big title text and a blinking READY. |
| `Movie` | HUD, floor, dialogue, frame edge, and saving with the fixed palette. `still()` saves one frame. |

## Other rules of thumb

- About 3 to 5 seconds per scene; leave time after the text finishes typing (it types over the
  first 45% by default). The 40 second Opus GIF is about 900 KB, far under X's 15 MB limit.
- The dialogue box fits 3 lines of about 46 characters.
- The crabs are original pixel art, not official Anthropic artwork, and the look is a nod to NES
  games, not their sprites.
