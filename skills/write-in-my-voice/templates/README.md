# The writing system

Claude drafts, Claude judges, the author edits, and every edit teaches the system something.

| File | What it's for |
| --- | --- |
| `voice.md` | One voice guide: how the author sounds, with real quotes. |
| `formats/*.md` | The shape of each kind of piece (how-to, essay, project write-up). |
| `voice-samples.md` | Which writing counts as the author's real voice, and which doesn't. |
| `edit-log.md` | Every round of the author's edits on a Claude draft, plus the predictions. |

## The loop

1. **Draft** from the author's notes, following `voice.md` and one format guide.
2. **Judge:** at most three fixes per round, at most three rounds.
3. **Predict** the author's edits in `edit-log.md` before they see the draft.
4. **Edit:** the author edits however they like and commits it.
5. **Learn:** diff their edit, log it, score the predictions, add candidate rules.
6. **Promote:** a candidate rule moves into `voice.md` only after it shows up in three pieces.

The number to watch is how much the author changes. The goal is that they only add the parts only
they can write.
