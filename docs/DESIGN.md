# Distribution God — Design Document

**Date:** 2026-08-09
**Status:** v1 shipped

## What it is

A cross-tool AI strategist plugin that points at any repository and produces an
investor-grade strategy report: what the product is, how big it can get, who it
competes with, which distribution channels fit, what gaps block growth, and what
moat can realistically be built. It thinks distribution-first: product gaps only
matter if they block a channel.

Works in **Claude Code** (as a full plugin with parallel subagents) and in
**OpenAI Codex** (via the shared open Agent Skills standard, sequential mode).

## Why this design

### Research findings (2026-08-09)

1. **Positioning gap confirmed.** Existing Claude Code GTM packs
   (e.g. gtmagents/gtm-agents, 67 plugins) target *revenue teams executing GTM
   tasks* — sales emails, CRM ops, campaign copy. Nothing found that is
   *repo-native*: reads code + git history + license + docs to infer the
   product and then strategizes. Code-awareness is the wedge.
2. **Cross-tool standard exists.** Codex deprecated custom prompts in favor of
   skills following the open Agent Skills standard (agentskills.io) — the same
   SKILL.md format Claude Code uses. Codex loads from `.agents/skills/`
   (repo) and `~/.agents/skills/` (user), invoked with `$skill-name`.
   One skill body can serve both tools.
3. **AI-era channels are the fresh content.** GEO (generative engine
   optimization) is growing ~50% CAGR; 28% of ChatGPT's most-cited pages have
   zero Google visibility. "Being recommendable/installable by AI agents"
   (MCP servers, plugin marketplaces, llms.txt) is a new distribution channel
   most strategy content ignores. Encoding this is a differentiator.

### Approaches considered

| Approach | Verdict |
|---|---|
| **A. Single flat skill** (one SKILL.md does everything inline) | Rejected: shallow analysis, context bloat, no parallelism, weak evidence gathering. |
| **B. Plugin: parallel sensor agents + main-loop synthesis + red-team pass** | **Chosen.** Evidence gathering is independent → fan out. Synthesis needs full context → main loop. Adversarial pass kills sycophantic verdicts. Degrades gracefully to sequential in Codex. |
| **C. Standalone MCP server / CLI** | Rejected for v1: heavier build + maintenance, and the value is in prompting methodology, not compute. Can be added later as productization. |

### Architecture (chosen)

```
                    /distribution-god  (skill = orchestrator)
                            |
        +-------------------+-------------------+
        v                   v                   v
   repo-intel          market-scout        rival-scout      <- parallel "sensors"
  (reads the repo)    (web: market,       (web: rivals,        (subagents in
                       trends, timing)     channels, gaps)      Claude Code;
        |                   |                   |               sequential in Codex)
        +-------------------+-------------------+
                            v
                 MAIN LOOP SYNTHESIS
        positioning, wedge, channel ranking,
        gap analysis, moat roadmap, verdict
                            v
                        red-team          <- adversarial subagent attacks the draft
                            v
                       STRATEGY.md        <- written into the analyzed repo
```

Design principle: **subagents are sensors, the main loop is the strategist,
the red team is the check.** Synthesis stays where full context lives.

## Components

- `skills/distribution-god/SKILL.md` — orchestrator: phases, agent dispatch
  (or sequential fallback), output contract.
- `skills/distribution-god/references/` — the actual IP:
  - `moat-frameworks.md` — 7 Powers mapped to software reality, moat sequencing
  - `channel-playbooks.md` — channel–product-fit matrix by product type
  - `ai-era-distribution.md` — GEO, agent-installability, 2026 channels
  - `scoring-rubrics.md` — Bigness /25, Moat /25, gap severity, calibration rules
  - `report-template.md` — STRATEGY.md structure
- `skills/gap-scan/SKILL.md` — fast local-only gap check (no web), for iteration.
- `agents/` (Claude Code only) — `repo-intel`, `market-scout`, `rival-scout`,
  `red-team`.
- `.claude-plugin/plugin.json` + `marketplace.json` — repo doubles as its own
  marketplace.
- `install-codex.sh` — symlinks skills into `~/.agents/skills/`.

## Non-negotiable product values

1. **Calibrated, not hype.** Every verdict carries a score, a confidence label,
   explicit kill criteria, and "what would have to be true." Market sizes are
   labeled ESTIMATE. No "this could be huge!" without the falsifier.
2. **Distribution-first.** Every gap must name the channel it blocks.
   Every channel must name the first concrete action.
3. **Code is evidence.** License, deps, telemetry, onboarding, API surface,
   release cadence are strategy signals, not implementation details.

## Out of scope (v1)

Hosted/SaaS version, continuous market monitoring, outcome database,
CRM/analytics integrations, financial projections. These are the
productization path if the wedge lands.
