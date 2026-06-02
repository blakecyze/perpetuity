## 2026-06-01 — Build perpetuity skill v0.1 (Tier 1)

### Decisions made outside the spec
- Seed store (`notes/_example.md` + `INDEX.md`) ships inside the skill folder; `SKILL.md` points the runtime store at `~/.claude/perpetuity/` (or repo-local `.perpetuity/`) — reconciles the deliverables tree with the anti-bloat "notes live in their own removable dir" rule.
- `reindex.py` indexes all `notes/*.md` including the `_`-prefixed example, so the shipped `INDEX.md` is actually reproducible rather than wiped on first run.
- Generated `desc`/`tags` come straight from frontmatter, so the regenerated index differs slightly from a hand-tuned line — expected for a generated file, not a drift bug.

### Tradeoffs taken
- `reindex.py` uses a ~15-line stdlib frontmatter parser (no PyYAML) — handles the folded `>-` description and inline `#` comments, but is not a general YAML parser. Single-purpose by design.

### Anything else you should know
- `SKILL.md` is 137 lines, under the ~180 budget.
- Curate is command-only (`/perpetuity-curate`); no command file ships in v0.1 — the protocol lives in `SKILL.md`. Nothing from the out-of-scope list (hooks, daemon, HTML dashboard, USER profile, embeddings) was built.
