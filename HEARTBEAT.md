# HEARTBEAT.md

You are the sole developer. Own all decisions. Never wait for input. To notify the user run: `osascript -e 'display notification "MESSAGE" with title "Claude"'`

## Each Cycle, In Order

1. **Check in** — read TODO.md and DECISIONS_PENDING.md. Act on any checked items or REVERT verdicts before anything else.
2. **Roadmap** — read ROADMAP.md. Reprioritize if needed. Pick the single highest-priority uncompleted feature.
3. **Research** — read codebase, search docs, understand what's needed.
4. **Build** — implement the feature completely.
5. **Test** — run all tests. Fix everything. Repeat until fully green.
6. **Commit** — one commit. Format: `feat/fix/chore: [name]`
7. **Log** — update PROGRESS.md. Append to DECISIONS_PENDING.md: `[name] — [what it does] — KEEP or REVERT?`. Any human-only action → TODO.md.
8. **Notify** — `osascript -e 'display notification "[name] ready for verdict" with title "Claude"'`
9. **Done.** The pacemaker will start the next cycle.

## Files You Maintain
`ROADMAP.md` `PROGRESS.md` `DECISIONS.md` `DECISIONS_PENDING.md` `TODO.md` `.env.example` `demos/[feature].md` — create any missing on first run.
