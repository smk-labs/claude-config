---
name: map
description: The index of every project Seyed owns, read live from GitHub with no clone needed. Use when (a) a project is named and you need its path, its remote or what it is ("where is nasir", "clone dana", "کجاست", "چیه"), (b) you are about to start work and must find the right folder, (c) a new repo appears or one is renamed, archived or re-described, so the map needs a row, or (d) the user asks what projects exist or asks to search the map.
---

# map

`~/Projects/MAP.md` is the one index of every project: path, remote, one sentence. It lives in the private `SMKeramati/daftar` repo. This skill reads and writes it straight through the GitHub API, so it is always the current version and no clone is needed.

The script is `map`, next to this file. Call it by its full path, or add `~/.claude/skills/map` to `PATH`.

```bash
~/.claude/skills/map/map find nasir
~/.claude/skills/map/map sections
~/.claude/skills/map/map add "Personal" "smk-labs/thing" "https://github.com/smk-labs/thing.git" "One sentence saying what it is."
~/.claude/skills/map/map set "smk-labs/thing" "https://github.com/smk-labs/thing.git" "A better sentence."
~/.claude/skills/map/map rm "smk-labs/thing"
```

## Rules

- **One sentence per project, never two.** The sentence says what the thing is, not how it deploys or what happened to it. That belongs in the project's own repo.
- **A new project gets its row the same session it appears.** Renamed, archived or gone legacy: fix the row the same day.
- **Preview first when unsure.** Every write takes `--dry-run` and prints the diff instead of committing.
- **Never hand-edit `~/Projects/MAP.md`.** Writes go through this script, which commits to GitHub and then fast-forwards the local clone. A hand edit sitting uncommitted is what turns the next write into a conflict.
- **Reads are cached for 120 seconds.** Pass `--fresh` to bypass it. Writes always fetch fresh.

## When it cannot reach GitHub

Reads fall back to `~/Projects/MAP.md` and say so on stderr. Writes refuse rather than guess. Authentication is whatever `gh auth token` returns, or `GH_TOKEN` in the environment.

## Working on a project once you have its row

`cd` into the path. If the folder is not there, `git clone <remote> <path>`, and clone parents before children: `git clone` refuses a non-empty directory, so `dana` must be cloned before `dana/dana-api`.
