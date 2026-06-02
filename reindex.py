#!/usr/bin/env python3
"""Regenerate INDEX.md from the frontmatter of every note in notes/.

Stdlib only, no PyYAML. Run from the perpetuity directory: python3 reindex.py
Only notes/*.md are indexed; archived notes live in .archive/ and are skipped
by the glob, keeping the index the always-loaded hot layer.
"""
import pathlib

HERE = pathlib.Path(__file__).parent
NOTES = HERE / "notes"


def frontmatter(text):
    """Return the YAML frontmatter as a flat dict. Folded scalars are joined."""
    if not text.startswith("---"):
        return {}
    body = text.split("---", 2)[1].splitlines()
    fields, key = {}, None
    for line in body:
        if line[:1] in " \t" and key:  # continuation of a folded value
            fields[key] += " " + line.strip()
        elif ":" in line:
            key, val = line.split(":", 1)
            key = key.strip()
            raw = val.split("#", 1)[0].strip()
            if raw in (">", ">-", "|", "|-"):  # block-scalar marker; value is on the following lines
                raw = ""
            elif len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in "\"'":
                raw = raw[1:-1]
            fields[key] = raw
    return {k: v.strip() for k, v in fields.items()}


def main():
    lines = ["# perpetuity INDEX  (generated; do not hand-edit, run reindex.py)", ""]
    notes = sorted(NOTES.glob("*.md"))
    for path in notes:
        f = frontmatter(path.read_text())
        lines += [
            f"- name: {f.get('name', path.stem)}",
            f"  desc: {f.get('description', '')}",
            f"  tags: {f.get('tags', '[]')}  state: {f.get('state', 'active')}  conf: {f.get('confidence', '')}",
        ]
    (HERE / "INDEX.md").write_text("\n".join(lines) + "\n")
    print(f"reindexed {len(notes)} note(s)")


if __name__ == "__main__":
    main()
