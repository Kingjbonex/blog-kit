---
name: learn-from-edits
description: Learn from the author's edits to a Claude-drafted piece. Diff their commits, log what changed in writing/edit-log.md, score the predictions, and promote repeated patterns into writing/voice.md. Use after the author edits or publishes a draft.
---

# Learn from the author's edits

Pairs with `write-in-my-voice`. Expects the `writing/` folder that skill sets up.

1. **Find the edits.** `scripts/my_edits.sh <file> "<author name>"` (in this skill's folder) shows
   a word diff of every commit the author made to the file. If they edited outside git (pasted text,
   a comment), diff their version against the last Claude version instead.
2. **Log them.** Fill in the piece's entry in `writing/edit-log.md` (create one if there's none).
   List each change in a few words with a short quote, then a one-line takeaway. Note roughly how
   much they changed (lines or words added and removed), so the trend is visible.
3. **Score the predictions.** Mark each one hit, miss or partial, and list the edits nobody
   predicted. Unpredicted edits are the most useful thing to learn from.
4. **Update candidate rules.** Add a row for each new pattern, or bump the tally on an existing
   one. Count pieces, not edits: three similar edits in one piece count once.
5. **Promote carefully.** When a candidate reaches 3 pieces, move it into `voice.md` with its quotes
   and mark it *(promoted)*, then list it under "Promoted rules". If the author's edits contradict a
   rule in `voice.md`, flag it to them rather than quietly deleting it.
6. **Don't over-learn.** Fixing a fact or adding a personal story is content, not voice. Log it,
   but don't make a style rule out of it.

Commit the changes to `writing/` on their own, with a message like "Learn from edits to `<file>`".
