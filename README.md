# claude-config

My live `~/.claude`, under version control. It holds the parts of my Claude Code setup that are safe to share and useful to copy: the operating manual (CLAUDE.md), custom skills, slash commands, and a portable settings template. Cloning it as `~/.claude` on a fresh machine restores the whole setup in one step.

## Layout

| Path | What it is |
|---|---|
| `CLAUDE.md` | Operating manual: thinking, communication, and building rules for every session |
| `RTK.md` | Usage notes for the rtk token-saving CLI proxy (imported by CLAUDE.md) |
| `HEARTBEAT.md` | Cycle prompt for autonomous cron sessions |
| `commands/` | Slash commands: browser-test, isolate, merge, tldr, to-gif |
| `skills/` | 16 skills as real files, no symlinks. Vendored skills keep their original licenses |
| `tools/` | Scripts that extract and clean my own prompt history (outputs stay untracked) |
| `settings.shared.json` | Portable settings template, with machine and work specific entries removed |

## New machine

```sh
git clone https://github.com/smk-labs/claude-config.git ~/.claude
cp ~/.claude/settings.shared.json ~/.claude/settings.json
```

If `~/.claude` already exists, graft the repo into it (repo versions overwrite tracked paths, everything else stays):

```sh
git clone --no-checkout https://github.com/smk-labs/claude-config.git /tmp/cc
mv /tmp/cc/.git ~/.claude/.git
git -C ~/.claude reset --hard origin/main
```

Plugins are not stored here; they reinstall from their marketplaces. The template's `extraKnownMarketplaces` block registers mine on first run: `anthropics/claude-plugins-official`, `smk-labs/claude-plugins`, `SMKeramati/gstack`, `SMKeramati/claude-backlog-md`, `rajool/yar`.

## Deliberately not here

- Anything with credentials or account state: `settings.json`, `history.jsonl`, `projects/`, `shell-snapshots/`
- Work specific commands and generated data files (ignored inside tracked folders too)
- Plugin caches (reinstallable) and machine state (`backups/`, `scripts/`, `file-history/`, and friends)

The `.gitignore` is an allowlist: every path is ignored unless listed.

## Related repos

- [claude-plugins](https://github.com/smk-labs/claude-plugins): my plugin marketplace (readable, getpix, cursor-delegate, and more)
- [fig](https://github.com/smk-labs/fig): home repo of the fig skill (a copy ships in `skills/fig`)
- [claude-rtl](https://github.com/smk-labs/claude-rtl): RTL patch for Claude Desktop
- [claude-sync](https://github.com/smk-labs/claude-sync): see sessions across Claude Desktop accounts
- [claude-deck](https://github.com/smk-labs/claude-deck): run several Claude accounts side by side

## License

MIT for my own content. Vendored skills in `skills/` keep the licenses inside their folders.
