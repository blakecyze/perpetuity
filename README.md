# perpetuity

Cross-session memory for Claude — a single, lightweight
[agentskills.io](https://agentskills.io) skill that remembers *how hard problems
got solved* so they don't get re-solved next month. It sits beside your other
skills as an additive, removable layer; it governs **what is remembered across
sessions**, not how code is written.

It is passive in one sense only: **zero effort from you**, not *runs while you
sleep*. A skill has no daemon and no clock — perpetuity acts at the **edges of a
turn**: recall when a task starts, capture when it ends.

## The two-beat loop

```
task starts → RECALL (search notes, load matches) → …work… → task ends → CAPTURE (write one note, if earned)
                                  — and, on command — CURATE (dedupe, age, consolidate) —
```

- **Recall** — reads the bounded `INDEX.md`, greps `notes/` for relevant tags,
  loads only matching notes. Progressive disclosure keeps it cheap.
- **Capture** — at task end, writes/patches exactly one Markdown note *if* it
  met the bar: a 5+ step workflow that worked, a recovered dead end, a
  correction, or a tooling quirk worth not rediscovering. When in doubt, it
  doesn't. Over-capture is the failure mode.
- **Curate** — manual only, via `/perpetuity-curate`: snapshot, age
  `active → stale → archived`, consolidate overlaps. Never deletes; worst case
  is a move to `.archive/`.

## Install

```sh
git clone https://github.com/blaketime/perpetuity ~/.claude/skills/perpetuity
```

The notes themselves live in their own directory — `~/.claude/perpetuity/`
(global) or a repo-local `.perpetuity/` (project-scoped) — so the store is
separate from the skill. Deleting both directories fully uninstalls it.

## What's here

| File | Purpose |
|------|---------|
| `SKILL.md` | The whole protocol — recall, capture, curate, criteria, schema. |
| `notes/_example.md` | One filled note demonstrating the schema. |
| `INDEX.md` | The bounded, always-loaded index. Generated from frontmatter. |
| `reindex.py` | Stdlib-only, regenerates `INDEX.md` from note frontmatter. |
| `docs/` | The design dossier (HTML) — why perpetuity is built the way it is. |

## Status

**v0.1 — Tier 1 (pure skill).** Works everywhere, including the chat UI. Recall
and capture run automatically within a session; curate is manual. No Claude Code
hooks, no daemon — those are the Tier 2 / Tier 3 roadmap (see `docs/`).

## Safety rails

Never auto-deletes. Every note carries `confidence`, `supersedes`, `origin`,
`state`, and `last_used`. Curate never touches a `pinned: true` or
`origin: hand-authored` note, nor anything outside the perpetuity directory.

## Licence

MIT — see [LICENSE](LICENSE).
