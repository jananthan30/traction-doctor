# Traction Doctor — Design Document

**Date:** 2026-08-09 (updated 2026-09-25 for v0.2.0, 2026-09-27 for v0.3.0, 2026-10-28 for v0.4.0 and v0.5.0)
**Status:** v0.5.0

## What it is

A cross-tool AI strategist plugin that points at any repository and produces an
investor-grade strategy report: what the product is, how big it can get, who it
competes with, which distribution channels fit, what gaps block growth, and what
moat can realistically be built. It thinks distribution-first: product gaps only
matter if they block a channel.

Works in **Claude Code** (as a full plugin with parallel subagents) and in
**OpenAI Codex** (native plugin install from the same marketplace file; the
sensor methods run as generic sub-agents or in sequence).

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
   optimization) is a separate game from SEO: ~28% of ChatGPT's 1,000
   most-cited pages had zero Google organic visibility
   ([Ahrefs, Oct 2025](https://x.com/thinking_slow/status/1983184678954627538)).
   "Being recommendable/installable by AI agents"
   (MCP servers, plugin marketplaces, llms.txt) is a new distribution channel
   most strategy content ignores. Encoding this is a differentiator.

### Approaches considered

| Approach | Verdict |
|---|---|
| **A. Single flat skill** (one SKILL.md does everything inline) | Rejected: shallow analysis, context bloat, no parallelism, weak evidence gathering. |
| **B. Plugin: parallel sensor agents + main-loop synthesis + red-team pass** | **Chosen.** Evidence gathering is independent → fan out. Synthesis needs full context → main loop. Adversarial pass kills sycophantic verdicts. Degrades to generic sub-agents or sequential phases in Codex. |
| **C. Standalone MCP server / CLI** | Rejected for v1: heavier build + maintenance, and the value is in prompting methodology, not compute. Can be added later as productization. |

### Architecture (chosen)

```
                    /traction-doctor   (skill = orchestrator)
                            |
        +-------------------+-------------------+
        v                   v                   v
   repo-intel          market-scout        rival-scout      <- parallel "sensors"
  (reads the repo)    (web: market,       (web: rivals,        (plugin agents,
                       trends, timing)     channels, gaps)      generic sub-agents,
        |                   |                   |               or sequential)
        +-------------------+-------------------+
                            v
                 MAIN LOOP SYNTHESIS
        positioning, wedge, channel ranking,
        gap analysis, moat roadmap, verdict
                            v
                        red-team          <- adversarial subagent attacks the draft,
                            v                including the path and the pivots
                     customer-scout       <- v0.4.0: real openings for the FINAL wedge
                            v
          STRATEGY.md + FIRST-CUSTOMERS.md   <- report (public) + people file (private)
                            v
   check_report.py + check_customers.py + strategy_card.py   <- deterministic checks
```

Design principle: **subagents are sensors, the main loop is the strategist,
the red team is the check.** Synthesis stays where full context lives.

## Components

- `skills/traction-doctor/SKILL.md` — orchestrator: phases, execution modes
  (`parallel` / `generic-subagents` / `sequential`), red-team disposition,
  output contract.
- `skills/traction-doctor/references/` — the actual IP:
  - `moat-frameworks.md` — 7 Powers mapped to software reality, moat sequencing
  - `channel-playbooks.md` — channel–product-fit matrix by product type
  - `ai-era-distribution.md` — GEO, agent-installability, 2026 channels
  - `scoring-rubrics.md` — anchored Bigness /25 and Moat /25, bands, gap
    severity, calibration rules
  - `report-template.md` — STRATEGY.md structure, including the `dg` line
  - `strategy-card.md` — the shareable card's data schema and steps
  - `pivot-playbook.md` — when to pivot, the asset inventory, Ries's ten
    pivot types mapped to the moat powers they unlock, the pivot card
  - `first-customers.md` — the offer, picking openings, drafting rules,
    re-runs, and the FIRST-CUSTOMERS.md template
  - `sensors/` — the method for each sensor, the red team and the customer
    scout; the single source of truth for every mode
- `skills/traction-doctor/scripts/` — `strategy_card.py` renders the card
  from JSON (escaping, width budgets, rubric bands); `check_report.py` lints
  STRATEGY.md against the contract (version-gated: each report is held to
  the contract of the version that wrote it); `check_customers.py` lints
  FIRST-CUSTOMERS.md, including privacy.
- `skills/traction-doctor/assets/strategy-card.template.svg` — card template.
- `skills/gap-scan/SKILL.md` — fast local-only gap check (no web), for iteration.
- `skills/close-gaps/` (v0.3.0) — the research stage. `SKILL.md` orchestrates
  triage → one `gap-researcher` per weakness → ranking → `pragmatist`;
  `references/idea-rubric.md` holds the target ids, triage, the /20 idea
  score and the top-five rules; `references/ideas-template.md` the output;
  `scripts/check_ideas.py` enforces the `CLOSE-GAPS.md` contract. Full
  design: `docs/superpowers/specs/2026-09-27-close-gaps-design.md`.
- `agents/` (Claude Code) — `repo-intel`, `market-scout`, `rival-scout`,
  `red-team`, `customer-scout`, `gap-researcher`, `pragmatist`: thin wrappers that load their
  method from their skill's `references/sensors/` via `${CLAUDE_PLUGIN_ROOT}`.
- `.claude-plugin/plugin.json` + `marketplace.json` — repo doubles as its own
  marketplace; Codex reads the same marketplace file.
- `install-codex.sh` — fallback: symlinks skills into `~/.agents/skills/`.
- `tests/`, `evals/`, `.github/workflows/` — unit tests and fixtures,
  `claude plugin eval` suites, CI (validate, on-demand evals, weekly traffic
  log to `metrics/traffic.csv`).

### Decisions added in v0.2.0

- **Deterministic where it can be.** SVG escaping, meter math, band labels,
  and report consistency are code, not prompt instructions — the model
  writes values, scripts enforce the contract.
- **One method, many runtimes.** Sensor methods live under the skill (which
  every install path ships) instead of in `agents/` (which only Claude Code
  loads), so Codex runs get the same rigor.
- **Version is a release gate.** Installs pin to `plugin.json`'s version; CI
  fails any change to `skills/` or `agents/` that doesn't bump it.

### Decisions added in v0.3.0

```
/close-gaps   STRATEGY.md ──► triage ──► gap-researcher × ≤3 ──► rank ──► pragmatist ──► CLOSE-GAPS.md
                             │           (trends · papers ·                            + check_ideas.py
                             │            look-alikes)
                             ├──► Just do it       (known fixes: no research)
                             └──► Can't move now   (scores the market sets)
```

- **Diagnosis and prescription are separate commands.** `/close-gaps` reads
  a finished report instead of extending the full run: the full run stays
  at 15–20 minutes, users can correct the diagnosis before paying for
  research, re-run one weakness at a time, and have a reason to come back —
  the self-report's crux is recurring use.
- **Research only unknown fixes.** Triage sends known fixes to *Just do it*
  and market-set scores to *Can't move now*; the research budget goes to
  open questions, ranked by whether closing them moves the verdict band.
- **One researcher per weakness, three lenses each** (trends, papers,
  look-alikes), rather than one researcher per source: every idea is born
  attached to a weakness and its rubric anchor, and a researcher can follow
  a lead from a paper to the product that shipped it.
- **Pragmatism is a contract.** Ideas are scored /20 on Impact, Proof, Fit
  and Cheap; any 0 cuts. `check_ideas.py` rejects a card without a linked
  precedent, a first test of one to five steps, or dates within 28 days. A
  separate pragmatist checks what code can't: whether a source says what
  the card claims, whether it transfers to this stage, and whether an idea
  moves a real outcome or only a score.
- **Keyless paper search.** arXiv, OpenAlex and Hugging Face Papers answer
  without API keys (checked 2026-09-27); Semantic Scholar refuses keyless
  calls and is left out.

### Decisions added in v0.4.0

The owner's critique of v0.3.0: "it's just scores." The report diagnosed in
depth and prescribed in one bullet. v0.4.0 adds three action parts.
Full design: `docs/superpowers/specs/2026-10-28-action-sections-design.md`.

- **Inside the existing sections, never renumbered.** close-gaps addresses
  gap rows as `gap.<n>` in §6 and the checker and evals key on §7 and §10,
  so the path block lives in the Verdict, *First customers* is a `###`
  sub-section of §5, and pivots join §9 (whose heading keeps its prefix).
- **Version-gated contract.** The checker applies the v0.4.0 checks only to
  reports stamped 0.4.0 or later; the rubric stays version 2, so close-gaps
  and every older report keep working.
- **Prescriptions can't game the score.** Path moves are labeled `outcome`
  or `rubric-only`, at least one must be an outcome, and no projected total
  may appear anywhere; the red team re-judges every label.
- **Pivots answer kill criteria.** Each pivot is started by a named kill
  criterion, keeps a named asset, and has a test that can fail — so a weak
  verdict ends in a decision rule, not a shrug.
- **Prospecting runs last.** The customer scout needs the final wedge,
  which the red-team disposition can change, and the market scout's
  watering holes — so it runs after the red team, not alongside the first
  sensors. It has no shell and no write access: it reads the most hostile
  pages of any agent.
- **People are private.** STRATEGY.md is often committed, so it names
  venues, never posts; the people live in FIRST-CUSTOMERS.md, which the
  user is told to gitignore. The checker rejects contact details, unlinked
  or undated openings, and drafts that don't disclose authorship.

### Decisions added in v0.5.0

- **Renamed to traction-doctor** (the owner's call, 2026-10-28), before
  the directory submission: nothing depended on the old name yet, and a
  submission can't change its repository later.
- **Old files stay valid.** A fingerprint names the plugin as it was at
  the stamped version. `tool_for()` in `strategy_card.py` is that one rule,
  and the report, card, people-file and idea checkers all use it. Dated
  records (the self-reports, examples and archives) keep the old name,
  and the `dg` and `cg` data lines keep their keys.

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
