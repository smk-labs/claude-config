---
name: review-packages
description: Audit a project's dependencies and give a per-package call: keep, replace, vendor-slice, or drop. Use when the user asks to "review packages", "audit dependencies", "which deps can we drop", "trim the dependency tree", "reduce supply-chain risk", or wants a keep-or-replace verdict on the stack. Also use mid-planning, or right after an architecture names its libraries, to vet proposed dependencies BEFORE they are installed. Weighs real usage depth, supply-chain risk, weight, and rewrite effort, with development cost treated as near-zero.
---

This skill decides which dependencies earn their place and which should become a lean equivalent you own.

The premise: supply-chain is today's top attack, and AI drove code-writing cost to near-zero. So the old reflex ("reuse before writing custom") flips. Every dependency is untrusted attack surface plus permanent maintenance load. The bar to keep one is high, and "rewriting is work" is no longer a reason to keep it.

## Two moments to run it

- **Audit an existing stack.** Point at a repo, or one workspace, and review what is already installed.
- **Vet a proposed stack.** During planning, or the moment the architecture names its libraries, review the candidates before anyone runs install. The cheapest dependency to remove is the one you never add.

## Score every dependency on four axes

1. **Usage depth.** How much of the package's real API surface do you actually exercise? "Used or not" is too coarse. Two icons out of 1,500 is near-zero, even though the import counts.
2. **Supply-chain risk.** Fame, audit history, maintainer count, transitive tree. An obscure single-maintainer SDK is the exact profile that gets poisoned.
3. **Weight.** Install size, bundle cost, transitive bloat. One chart that drags in the whole d3 tree is heavy for what it does.
4. **Rewrite effort.** How many lines, at what risk, to hand-roll just the slice you use? Estimate in LoC and risk, never in hours.

## Read the code, do not just run tools

Lean on existing tools for the cheap, mechanical signals: depcheck or knip for unused, Socket or OSV for known-bad, a size lookup for weight. They are inputs, not the verdict.

The judgment no tool gives is yours: open the real import and call sites and read enough to understand how deeply each package is used and how hard a lean replacement truly is. Read the right amount, not the whole tree. Aim for an intelligent recommendation, not a scanner's checklist.

## The verdict

Give each dependency one call:
- **Keep (standard).** Genuinely needed AND famous/standard/audited AND either deeply used or genuinely dangerous to hand-roll (auth, crypto, DB drivers, parsers, frameworks). These earn their keep. Do not waste effort replacing them.
- **Replace.** Shallow, heavy, or obscure, and cheap to rewrite. Write a lean equivalent you own.
- **Vendor-slice.** You need one small part of a big package. Copy that slice in (read, pinned) and drop the rest.
- **Drop.** Declared but unused, or duplicated by another dependency. Remove on sight.

## Deliver

One compact table, most valuable action first: Dep | what it does (plain words) | usage depth | supply-chain risk | weight | rewrite effort (LoC + risk) | verdict + a one-line "how". Follow it with a short 80/20 shortlist: the handful of removals with the best payoff, each with a one-line plan. Write every recommendation in plain language a non-expert reads once and gets.

## At scale

For a large or monorepo project, fan out: one agent per batch of dependencies, each reading its own call sites. Tell each agent to do the reading itself and return findings directly. Do not let agents recursively spawn more agents; that burns budget and returns nothing.
