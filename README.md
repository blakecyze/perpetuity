# perpetuity

Claude forgets everything between sessions. perpetuity keeps the part worth keeping: how you solved the hard stuff. It's one small skill on the [agentskills.io](https://agentskills.io) standard, sitting beside your other skills without fighting them for attention. Its job is memory, and it stays well out of how your code gets written.

Passive means something precise here: no clock, no background thread, nothing running while you sleep. A skill cannot do those things, so perpetuity works at the seams of a conversation instead. When a task begins, it searches its notes and loads only what matches. When the task ends, it writes one note back, and only if the task earned it. The third move, curate, you run by hand to stop the library turning to sludge. Recall, capture, curate: that is the whole of it.

## The loop

```
task starts → RECALL (search notes, load matches) → …work… → task ends → CAPTURE (write one note, if earned)
                                  (and, on command) CURATE → dedupe, age, consolidate
```

Three moves, and each one fails in its own way if you drop it.

**Recall** reads the small `INDEX.md`, greps `notes/` for anything tagged to the task in front of you, and pulls in only what matches. The index is always loaded. Full notes are not, so the whole thing stays cheap. Skip recall and you've built a diary nobody opens.

**Capture** saves a single note when a task ends, but only when the task earned one: a workflow that ran five or more steps and worked, a dead end you clawed your way back from, a correction you had to make, a config quirk you'd rather not trip over again. Nothing happened worth keeping? It writes nothing. Over-saving is exactly how a memory library turns to sludge.

**Curate** is the one move you trigger by hand, with `/perpetuity-curate`. It snapshots the library first, ages notes from active to stale to archived on a fixed clock, then folds overlapping ones together. It never deletes. Worst case, a note moves to `.archive/` and waits there.

## Install

```sh
git clone https://github.com/blakecyze/perpetuity ~/.claude/skills/perpetuity
```

The notes themselves live apart from the skill. Global memory goes in `~/.claude/perpetuity/`. Project memory goes in a `.perpetuity/` folder inside the repo it belongs to. Delete those two directories and the skill folder, and perpetuity is gone. No traces, no leftover config.

## What's in here

| File | Purpose |
|------|---------|
| `SKILL.md` | The whole protocol: recall, capture, curate, the capture bar, the schema. |
| `notes/_example.md` | One filled-in note that shows the schema. |
| `INDEX.md` | The bounded index that's always loaded. Built from note frontmatter. |
| `reindex.py` | A 30-odd-line script, stdlib only, that rebuilds `INDEX.md`. |
| `docs/` | The design dossier, and the reasoning behind every choice here. |

## Where it's at

This is v0.1, the pure-skill version. It runs anywhere Claude does, the chat UI included. Recall and capture fire on their own inside a session. Curate waits for you to ask. There are no lifecycle hooks and no daemon yet. Both are on the roadmap, and `docs/` walks through why the design stops where it does for now.

## Safety

perpetuity never deletes on its own. Every note carries how far to trust it, what it replaces, where it came from, its current state, and the date it last proved useful. Curate respects all of that. It leaves pinned notes where they are, never touches a note you wrote by hand, and never reaches outside its own directory.

## Licence

MIT. See [LICENSE](LICENSE).
