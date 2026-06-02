---
name: perpetuity
description: >-
  Cross-session memory of how hard problems got solved. Use when recalling past
  work: "have we solved this before", "what did we decide about X", "did we hit
  this error already", "remember how we fixed Y". Recalls relevant notes when a
  non-trivial task starts and captures a note when one ends. It governs what
  gets remembered across sessions. It stays out of how code is written, so it
  never competes with the kanso skills for code-writing triggers.
---

# perpetuity

A note library that gives you memory of how hard problems got solved, with zero
effort from the user. It is passive in one sense only: it acts automatically at
the **edges of a turn**: recall when a task starts, capture when it ends. It
has no daemon and no clock; it wakes only while you are already working.

Three behaviours: **recall**, **capture**, **curate**. Miss recall and the
library is a diary nobody reads; miss capture and it stays empty; miss curate
and it rots into near-duplicate sludge that poisons recall.

## Where the notes live

Global by default: `~/.claude/perpetuity/` with `notes/` and `INDEX.md` inside.
Prefer a repo-local `.perpetuity/` when the memory is clearly project-specific
and worth committing. Pick one per task; don't write the same note to both.
Deleting that directory and this skill folder fully uninstalls perpetuity.

The example note and index shipped in this skill folder are a seed, not the
runtime store. On first capture, create the runtime directory if absent.

## Recall, at the start of a non-trivial task

Skip for trivial or one-step tasks. Otherwise, before doing the work:

1. Read `INDEX.md` only. It is the bounded, always-loaded layer. Never load all
   notes up front.
2. Pull terms from the task: tools, errors, frameworks, domain nouns. Grep
   `notes/` for matching `tags:` and body terms.
3. Load **only** the matching full notes. This is progressive disclosure. The
   index is cheap, full notes cost tokens, so load them on match alone.
4. On a note you actually use, bump its `use_count` by 1 and set `last_used` to
   today. These counters drive decay; stale-but-useful notes shouldn't age out.
5. Weigh `confidence`. Treat `tentative` as a lead, not gospel; if a note is
   `supersedes`-pointed-at by a newer one, prefer the newer.

If nothing matches, say so in one line and proceed cold. Absence of a note is a
normal outcome, not a failure.

## Capture, at the end of a qualifying task

Capture writes or patches **exactly one** Markdown note. Patch an existing note
when the lesson refines one (token-cheap); write a new note only for genuinely
new ground.

Capture when one of these is true:

- A non-trivial workflow took 5+ meaningful steps and worked.
- You recovered from a non-obvious error or dead end. The working path is the
  gold.
- The user corrected your approach. Corrections are the highest-signal events.
- You hit a tool, config, or environment quirk worth not rediscovering.

Skip these. Over-capture is the failure mode that turns the library to sludge:

- Trivial or one-step tasks handled cold.
- Facts cheaper to re-derive or web-search than to store.
- Session ephemera: temp paths, one-off debugging state, run-specific IDs.
- Anything with secrets, keys, or tokens. Scan the note before writing; if it
  would leak a credential, don't write it.

**When in doubt, do not capture.** A smaller, trusted library beats a large one
you stop reading.

### Writing the note

One file per note under `notes/`, named by a kebab-case slug. Frontmatter is the
engine; the body follows the When / Procedure / Pitfalls / Verification shape.
Use this schema exactly (see `notes/_example.md` for a filled example):

```yaml
---
name: <kebab-case-slug>
description: <one line: what it fixes and when to reach for it; drives recall>
tags: [<searchable>, <terms>]
created: <YYYY-MM-DD>
source_task: "<short phrase naming the task it came from>"
confidence: high          # high | medium | tentative
state: active             # active | stale | archived
use_count: 0
last_used: <YYYY-MM-DD>
supersedes: null          # name of a note this replaces, if any
pinned: false
origin: agent-created     # agent-created | hand-authored
---
```

Set `origin: agent-created` on every note you write. `hand-authored` is reserved
for notes the user wrote by hand, and curate must never touch those.

After writing or patching, add or update the note's line in `INDEX.md` (run
`reindex.py` if present, else edit the one line by hand to match the format in
`INDEX.md`). If `INDEX.md` has grown past its budget, don't widen the budget.
That's the signal for a curate pass.

## Curate, only on `/perpetuity-curate`

Never automatic in v0.1. Curate only when the user runs the command. It operates
solely inside the perpetuity directory and never on a note where
`pinned: true` or `origin: hand-authored`.

1. **Snapshot first.** Copy the notes directory to a timestamped `.archive/`
   snapshot before any mutation, so every pass is reversible.
2. **Age deterministically, no model judgement.** From `last_used`: unused 30+
   days → `state: stale`; unused 90+ days → move the file to `.archive/` and set
   `state: archived`. Ageing runs before any consolidation.
3. **Consolidate overlaps.** Where two notes cover the same ground, merge into
   the stronger one, point the weaker's `supersedes` at it (or fold and archive
   the weaker). Consolidation is mandatory, not optional. It is what stops
   near-duplicate sprawl.
4. **Never delete.** The worst outcome is a move to `.archive/`. Nothing is ever
   removed from disk.
5. Regenerate `INDEX.md` from the surviving notes' frontmatter and write a short
   plain-language summary of what changed.

## Boundaries

- Markdown only, for notes and index. No HTML store, no JSON, no database, no
  embeddings, no vector search, no server.
- Only `INDEX.md` is loaded by default; full notes load on match.
- perpetuity governs memory; kanso governs code. They compose, they don't
  overlap. Never let curate touch a kanso skill or anything outside the
  perpetuity directory.

Out of scope for v0.1, by design: Claude Code hooks, any daemon or cron
behaviour, the HTML review dashboard, and a USER profile. Don't build them here.
