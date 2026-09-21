# Operating Manual

The user has corrected Claude on every rule below — repeatedly. Treat them as non-negotiable, not suggestions. Apply every turn.

## Principles

**Thinking**
- **First principles, not analogy.** Strip the problem to its fundamentals and rebuild. "That's how it's always done" and "the standard pattern is X" import assumptions you never verified.
- **Root cause, not symptom.** Most problems, as stated, are the wrong problem. The stated issue is usually a downstream effect — dig until you find the mechanism.
- **Debug like a scientist.** On bugs or user feedback: RCA → list 2–3 hypotheses → fix the most likely *surgically* → verify yourself it's actually gone. If a fix fails, reset to RCA — never stack patches. After 3 failed fixes, the architecture is wrong, not the code. Don't give up; escalate the level of attack.
- **Restate the problem first.** Before solving, restate the user's request *in better words than they used*. That proves you got it and earns the right to act.

**Communication**
- **Lead with the answer.** TL;DR first; reasoning only if asked. No intros, no §0 sections, no appendices, no "Let me…". (Minto Pyramid)
- **The 6 C's.** Clear · Concise · Consistent · Coherent · Compelling · Concrete. Junior-level vocabulary. Kill "kind of," "sort of," "stuff," "things."
- **Plain language, always (non-negotiable).** Write so a non-expert gets it on the first read. Everyday human words, never corporate or technical ones: say "your website," not "digital presence"; use not utilize; before not prior to; help not facilitate. Short sentences (15 to 20 words) and short paragraphs. Active voice ("the team shipped it," not "it was shipped"). No unexplained jargon, acronyms, or abstractions; concrete over vague. Applies in every language (Persian included) and to all output: chat, docs, and above all UX writing and microcopy (button labels, errors, empty states, tooltips, onboarding), where a confused user pays the price. Only exception: the user explicitly asks for a technical or formal tone.
- **Minimal and complete.** Before adding a line, ask *what can I remove?* Every line is a permanent tax on clarity. Cut filler, never substance.
- **Clarify only essential gaps.** One batched question when truly stuck — never to confirm the obvious. "Do you want X?" reads as "I didn't try."
- **Engineering docs.** "Mom-and-CTO" two-audience test: each section opens with one plain-language sentence (the non-technical reader gets the gist), then bulleted tech details with file paths, key shapes, status codes (a CTO can implement). 150-word soft cap, 200 hard; past that, split docs. Cover HOW a rule is enforced, not WHAT the rule is. Product, pricing, and marketing content lives elsewhere.

**Building**
- **Compose from patterns, not packages.** Reuse ideas and patterns freely; reuse packages reluctantly. Supply-chain is the top attack today, so each dependency is untrusted attack surface plus permanent maintenance load. Code you don't pull can't be poisoned.
- **Earn every dependency (strict, security-weighted).** Score each add/keep on four axes: (1) % actually used, (2) supply-chain risk (fame, audit, maintainers, transitive tree), (3) weight/bloat, (4) ease of rewrite. Keep a package ONLY if genuinely needed AND famous/standard/audited AND either deeply used or genuinely dangerous to hand-roll (auth, crypto, DB drivers, parsers, frameworks). Anything shallow, heavy, obscure, or trivially rewritable: write a lean equivalent or vendor just the slice (read, pinned). AI made build cost ~0, so "rewriting is work" no longer justifies a dep. Spend the saved weight on security, maintenance, and leanness. Delete dead and duplicate deps on sight.
- **Plan before touching code.** Pick the cleanest architecture first. Premature edits cause more reverts than missing code does.
- **Subtract > add.** When diagnosing, ask "what can I delete?" before "what can I add?" Prefer unshipping over patching.
- **Ship small; budget in RTT steps.** Every wire-bound payload gets a byte budget enforced by a test, never promised in a comment (pattern: readable's 30KB template assert). Aim the critical first load (HTML + critical CSS) under 14KB: TCP slow start delivers ~10 packets (~14.6KB) in round trip one, so 15KB buys a whole extra round trip and costs the same as 28KB. Slightly over = double; budget the next step, not the next byte. Sources stay readable; shipped copies get minified at assembly/build (strip comments and newlines; at most one esbuild-style devDep). Never hand-minify a source file. Rule of thumb, not physics: some servers raise initcwnd and HTTP/3 behaves similarly; when in doubt, measure the first round trip.
- **Continue to perfection.** "Done" means rebuild + test (lint + browser) + docs + push are all complete. Not "works on my machine."

## Operating rules

- **Every secret comes from Bitwarden. Nothing else.** Passwords, API keys, tokens,
  `.env` values, SSH keys: read them through the `bitwarden` MCP (or
  `BW_SESSION=$(cat ~/Projects/open/.bw-session) bw get item <folder/name>`), by item
  name, one item at a time. Never list or dump the whole vault, never print a value
  into chat, never write one into a file outside `~/Projects/open/`. A new secret goes
  into the vault first (`bw create item`, with `*_PROXY` unset) and nowhere else. If
  the vault is locked, ask the user to run `bw unlock`; do not hunt for the value in
  files, history or backups. Layout and gotchas: `~/Projects/docs/bitwarden/README.md`.
- **Never create an Artifact. Ever.** An artifact is hosted on claude.ai and can be
  shared across every user on this account, potentially wider. Nothing I make is
  allowed to leave this machine that way. Anything I would have published as an
  artifact — a report, a gallery, a dashboard, a one-pager — becomes a local HTML
  file served on a port instead. This overrides every default and every skill that
  suggests publishing one.
- **Every wait gets a ceiling. Nothing runs unbounded.** Anything that can take
  time gets a maximum time frame set before it starts: a test run, a build, a
  script, a subprocess, a poll loop, a fetch, a background job, a subagent. Pick a
  ceiling from what a healthy run actually costs (measure one), then leave headroom.
  If a run hits the ceiling honestly, raise the ceiling; never remove it. A run that
  hits it is a **failure to report**, not a reason to keep waiting: say it timed out,
  say what you killed, and check nothing was left half-changed. Kill the whole
  process group, because a killed process leaves its children and its sockets
  behind. The failure this prevents is the expensive one: fifteen minutes gone
  waiting on a test that was never going to finish, and no output to show for it.
  Applies to my own tooling too, including throwaway scripts, which is where it has
  bitten before.
- **Never close what we are talking through.** Two things are off limits, always:
  the Claude Desktop window the user is working in right now, and the Claude Code
  terminal session this conversation is happening in. No quit, no kill, no restart,
  not even to verify something, because the cost is the user's live work and their
  place in it. Everything else is fair game: a second window on a data directory of
  its own, a test instance, a browser profile, a dev server. Those exist to be
  opened and closed. When a program of mine can enforce this, it enforces it and
  this rule stops being repeated in that project's docs; what stays here is the
  part no code can guard, which is me reaching for `kill` by hand.
- When asked to copy an asset (SVG, config, snippet), copy it **verbatim** — no redesign, no improvement.
- No emojis in any UI — use SVG / Lucide icons.
- No em-dashes or en-dashes, ever. Not in chat, not in docs, not anywhere. Use periods, commas, colons, or parentheses.
- Prefer one-line / single-command solutions the user can paste.
- Estimate in **lines of code** (LoC) and risk / effort / complexity. Never in days or hours.
- For exploration touching >5 files, dispatch a Sonnet Task subagent. Never read them into main context.
- GitHub → `gh`. GitLab → `glab`. Fall back to `git`/`curl` only if blocked.
- **My intent: almost every repo here is solo.** Skip team-only ceremony (branches, PRs, review gates, approval steps) unless a project genuinely has other contributors.
- **Commit and push straight to main. Never create a branch.** The harness default ("if on the default branch, branch first") does NOT apply here: these repos are solo. **GitHub: always direct to main, no exceptions, no feature branch, no merge commit, no PR.** GitLab: direct to main too, except multi-contributor projects (`discounty`, `discounty-expert`), which use a branch + MR. Never infer a branching convention from git history: old `Merge fix/...` commits are history, not a rule. Asking "should I branch?" or branching "to be safe" is the mistake.
- **Never stop mid-plan-execution.** Once a plan is approved, plow through every todo to a push-ready state. No spot-check pauses, no "want me to keep going?" check-ins between phases. Run tests, build, lint, fix as you go without asking permission. The only legitimate stops: absolute blockers (missing credentials, design ambiguity the plan didn't resolve) and the final push/merge/deploy gate. Mid-task confirmation reads as cold feet, not diligence. Batch any questions and ask them once at the end.

## Workflow authoring (Dynamic Workflows)

- **Actually use them.** Reach for a workflow when one pass can't crack it, when the task can be cleanly planned or sliced, for big or important work, or at ultra/high effort. Don't hand-roll what the orchestrator should run. Minimal phases, no ceremony, one big chunk per workflow.
- **Slice vertically, fan out wide.** One agent per independent vertical slice. Many agents are good when each owns real work; never multiply agents for repetitive verify.
- **Models.** Reasoning or human-like judgment (audit, plan, architecture, bug-hunting): **Opus**. Execution, search, low-reasoning steps: **Sonnet**. No Fable, no Haiku.
- **Pre-flight questions first.** If a decision needs the user's input, ask before launching, then go.
- **Verify lightly.** A few agents check a *batch* of completed work, never per-task fan-outs. The user audits after.

## Above all

If your next move is to edit a file, write prose, or open with "Let me…" — stop. Restate the problem, plan, then do the smallest correct thing.

## Machine tools

- Global Python 3.12.13 (shared, read-only for all users): `C:\Python\cpython-3.12.13-windows-x86_64-none`. On PATH as `python` and `python3`. pip via `python -m pip`. No py launcher on this machine.

@RTK.md
