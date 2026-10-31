---
name: write-in-my-voice
description: Draft or revise writing (blog posts, docs, threads) in the author's own voice, using a voice guide, a format guide, a self-judging revision loop and predicted edits. Use when asked to write, draft, flesh out or rewrite something that should sound like the author.
---

# Write in my voice

A drafting loop that gets closer to the author's voice every time they edit a draft. It pairs with
the `learn-from-edits` skill, which turns their edits into rules.

The voice lives in a `writing/` folder in the project. If it doesn't exist yet, set it up first
(step 0).

## 0. Set up (first run only)

Copy `templates/` from this skill into the project as `writing/`. Then fill in `writing/voice.md`
from real samples of the author's writing: ask for 3 to 5 pieces they wrote themselves (not
AI-assisted), and list them in `writing/voice-samples.md`. Every rule in `voice.md` must quote the
sample it came from. Rules you can't back with a quote don't go in.

## 1. Load the voice

Read `writing/voice.md`, the matching guide in `writing/formats/`, and `writing/edit-log.md`
(promoted rules, candidate rules and the latest two entries). Then read one or two samples from
`writing/voice-samples.md` that are closest to this piece.

If the author has edited a Claude draft since the last edit-log entry, run `learn-from-edits` first.

## 2. Draft

- Start from the author's input: notes, a voice memo transcript, an issue or an outline. Keep their
  own phrasing wherever they gave it. Their words beat yours.
- Never invent a personal story, number, opinion or memory. Anything only the author can know
  becomes a gap written as `**[AUTHOR: specific question]**`. Mark gaps they can skip "(optional)".

## 3. Judge, at most 3 rounds

Reread the draft as a strict editor who knows `voice.md`. Each round, list the **three** biggest
ways it doesn't sound like the author and fix only those. Stop after three rounds or when nothing
big is left. More rounds smooth the draft into mush. Look hardest at the usual AI tells: stock
phrases, em dashes, dramatic one-liners, "in the next post" teasers, filler sections, and structure
tidier than the author would write.

In the last round, read it once as the reader: someone on a phone who has never heard of the
author. Is the point clear by the end of the first section? Is any paragraph doing two jobs, any
sentence that needs a second read? Count these toward the same three fixes. Then check spelling.

## 4. Predict the edits

Before the author sees the draft, add an entry at the top of `writing/edit-log.md` (below the
rules tables) with 3 to 6 concrete edits you expect them to make:

```markdown
## YYYY-MM-DD: <title> (`<file>`, awaiting edits)

**Predicted:**

- cuts the closing paragraph
- adds an aside about ...
```

They get scored later, so vague ones are useless.

## 5. Hand off

Tell the author which gaps are theirs to fill. Don't ask "any thoughts?". Ask one or two directed
questions about the spots you're least sure of, such as "Which part felt redundant?" or "Is the
takeaway clear?".
