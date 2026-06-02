---
name: flutter-hot-reload-state-loss
description: >-
  Fix for Riverpod state vanishing on hot reload. Use when avatar cosmetic
  state resets mid-edit in the Avatone shop UI.
tags: [flutter, riverpod, avatone, hot-reload]
created: 2026-06-01
source_task: "debugging cosmetic preview resetting on save"
confidence: high          # high | medium | tentative
state: active             # active | stale | archived
use_count: 0
last_used: 2026-06-01
supersedes: null          # name of a note this replaces, if any
pinned: false
origin: agent-created     # never let curate touch hand-authored
---

## When to use
Riverpod providers holding ephemeral UI state reset on hot reload,
losing the in-progress cosmetic selection.

## Procedure
1. Move the selection into an `autoDispose` provider keyed by item id.
2. Persist the draft to the `cosmetic_draft` box before rebuild.
3. Rehydrate in `build()` from the box, not from a field.

## Pitfalls
- A plain StateProvider survives reload but leaks across items.
- Don't key by index. A reorderable grid breaks it.

## Verification
Edit a cosmetic, save, trigger hot reload. The selection persists.
