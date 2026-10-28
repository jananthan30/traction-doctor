# Distribution God

**Point it at any repo. Get an investor-grade strategy report.**

[![validate](https://github.com/jananthan30/distribution-god/actions/workflows/validate.yml/badge.svg)](https://github.com/jananthan30/distribution-god/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-plugin-blueviolet)](https://code.claude.com/docs/en/plugins)
[![Codex](https://img.shields.io/badge/Codex-plugin-black)](https://developers.openai.com/codex)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-standard-blue)](https://agentskills.io)

**Claude Code**

```
/plugin marketplace add jananthan30/distribution-god
/plugin install distribution-god@distribution-god
```

**OpenAI Codex**

```
codex plugin marketplace add jananthan30/distribution-god
codex plugin add distribution-god@distribution-god
```

Then, in the repo you want analyzed, run `/distribution-god` (Codex:
`$distribution-god:distribution-god`, or just ask for a strategy report).

A repo-native AI strategist for Claude Code and OpenAI Codex. It reads your
codebase like a data room — license, dependencies, telemetry, onboarding,
release cadence are all strategy evidence — then researches your live market
and competitors on the web, and writes `STRATEGY.md`: positioning, a ranked
distribution plan, a prioritized gap table, a moat roadmap, and a calibrated
"how big can this get" verdict with explicit kill criteria.

Then it tells you what to do about it:

- **Path to the next band** — how many points you need for the next band,
  and the moves that would earn them, each marked as a real outcome or a
  rubric-only box-tick.
- **Pivot options** — if the moat won't come: 1–3 pivots that keep what you
  built, each with a five-day test and the kill criterion that triggers it.
- **First customers** — real people who recently asked, in public, for what
  you built, with drafted replies you send yourself, in a private
  `FIRST-CUSTOMERS.md`.

`/close-gaps` goes deeper on the weakest points: it researches current
trends, papers, and products that fixed the same weakness, and keeps only
ideas you can test within a week.

Not another GTM prompt pack. Existing packs help revenue teams write emails.
This one starts from your code and tells you what business it can become —
then red-teams its own answer before showing you.

## It analyzed itself

The verdict on its own repo, unedited — from [STRATEGY.md](STRATEGY.md)
(v0.1.0 scored itself 17/25; the anchored v0.2.0 rubric and red team say 12):

<img src="assets/strategy-card.svg" alt="Strategy card: distribution-god's own verdict" width="600">

<!-- verdict-table:start -->
| | |
|---|---|
| **Bigness** | **12/25 — Niche tool / lifestyle business** (confidence: Medium) |
| **Moat today** | **1/25 — Nothing defensible yet:** the rubric is MIT and forkable in a day; one point for anti-hype counter-positioning |
| **The crux** | Recurring use: do plugin authors re-run it on each release, or run it once and forget it? |
| **Falsifier** | List it in Anthropic's directory and read the **Usage** tab: share of installing accounts still active 30+ days after install (free, 60–90 days). Until the listing is live: weekly unique cloners from `gh api repos/jananthan30/distribution-god/traffic/clones`, logged to `metrics/traffic.csv` |
<!-- verdict-table:end -->

A strategy tool that flatters you is worthless. This one is built to say
"this is a feature, not a company" — even about itself.

**On other repos:** see [`examples/`](examples/) — full reports on public
projects, each stamped with the commit, date, model, and run mode.

## It prescribed for itself

`/close-gaps` run on that report, unedited — from [CLOSE-GAPS.md](CLOSE-GAPS.md)
(23 minutes, 83 web calls, parallel mode):

<!-- close-gaps:start -->
**Do this first**

**I6. List on skills.sh through `npx skills add`, so installs raise the rank that agents' `find-skills` uses to recommend it in other clients** — closes `bigness.expansion` — 13/20

1. Do *Just do it* rows 1–2 first: decide close-gaps' license, then merge to `main`. Then run `DISABLE_TELEMETRY=1 npx skills add jananthan30/distribution-god --list` and confirm it finds every skill you pushed.
2. Add `npx skills add jananthan30/distribution-god` to README.md and llms.txt as a third install path, "any Agent Skills client (Cursor, Copilot, Gemini CLI…)".
3. Record the day-1 baseline: the repo's skills.sh page, and whether `npx skills find "distribution"` returns it.
4. Put the one-liner in the First-10 issues and the directory listing copy.
5. Re-read the page every Monday until 2026-10-25; keep telemetry off for your own installs.

**Success:** ≥10 skills.sh installs by 2026-10-25, ≥5 of them after First-10 outreach ends on 2026-10-04 (baseline 0: not listed on skills.sh at the run date). **Stop if:** <3 installs by 2026-10-25.

**Top ideas**

| # | Idea | Closes | Kind | First test | Build | Score |
|---|---|---|---|---|---|---|
| I6 | List on skills.sh via `npx skills add` | `bigness.expansion` | fresh | third install line, day-1 baseline, weekly install count | S | 13/20 |
| I1 | Release-time hook: "STRATEGY.md predates this tag" | `crux+bigness.wedge` | proven | build the hook, see it fire on this repo's own tag | S | 12/20 |
| I2 | A 5-minute per-release "release pass" note | `crux+bigness.wedge` | fresh | 5 notes for 5 indie plugins that just shipped a release | M | 12/20 |
| I7 | Offer the skill committed inside each author's repo | `bigness.expansion` | fresh | one optional line in the First-10 issues | S | 11/20 |
| I4 | Sell `/close-gaps` for $19 one-time via Polar | `bigness.delivery` | fresh | private repo, checkout, one r/SideProject post | S | 11/20 |
<!-- close-gaps:end -->

```
sensors (parallel)    strategist     check        prospecting
┌─ repo-intel    ─┐
├─ market-scout  ─┼──► synthesis ──► red-team ──► customer-scout ──► STRATEGY.md + card
└─ rival-scout   ─┘    (verdict,     (attacks     (real people,      FIRST-CUSTOMERS.md
                        path,         the draft)   final wedge)      (private)
                        pivots)

then, on request — /close-gaps
STRATEGY.md ──► triage ──► gap-researcher × ≤3 ──► ranking ──► pragmatist ──► CLOSE-GAPS.md
                           (trends · papers · look-alikes)
```

## Use

| Command | What you get | Time |
|---|---|---|
| `/distribution-god` (Codex: `$distribution-god:distribution-god`) | Full run: market + rivals research, distribution plan, gaps, moat, verdict, path to the next band, pivot options → `STRATEGY.md` + `assets/strategy-card.svg`; real first-customer openings with drafted replies → `FIRST-CUSTOMERS.md` (private) | ~15–20 min through the red team (v0.2.0, sequential, four repos), plus the prospecting |
| `/close-gaps` (Codex: `$distribution-god:close-gaps`) | After a full run: researches trends, papers, and look-alike products for the report's weakest points → `CLOSE-GAPS.md`, at most five ideas, each with a linked precedent, a one-week test, and a stop signal | ~25 min (measured twice in parallel mode on this repo: 25 and 23 min) |
| `/gap-scan` (Codex: `$distribution-god:gap-scan`) | Local-only audit of your distribution surface — prioritized gap table in chat | about a minute on a small repo, a few on a large one |

Also usable piecemeal in Claude Code: `@agent-distribution-god:rival-scout`
("who competes with X and how do they grow"), `@agent-distribution-god:red-team`
("attack this plan"), `@agent-distribution-god:repo-intel`,
`@agent-distribution-god:market-scout`, `@agent-distribution-god:customer-scout`
("find people who need X"), `@agent-distribution-god:gap-researcher`
("find proven ways to fix X"), `@agent-distribution-god:pragmatist` ("attack
these ideas") — or type `@` and pick the agent from the list.

### Before you run

- **Web permissions.** The full run makes roughly 20–30 web searches plus a
  similar number of page fetches before prospecting, and the customer scout
  adds about 10 searches plus API fetches; `/close-gaps` made 80–83 web calls
  on this repo (two measured runs). For an unattended run, choose "don't ask
  again" on the first WebSearch/WebFetch prompt, or allow both in
  `~/.claude/settings.json`:
  `"permissions": {"allow": ["WebSearch", "WebFetch"]}`. Without web access
  it still runs and writes a local-only report, marked `NOT RESEARCHED`.
- **Codex:** start with live search — `codex --search`, or
  `web_search = "live"` in `~/.codex/config.toml`. The default cached search
  returns stale results.
- **Cost.** A full run uses up to five high-effort agents on your current
  model; expect it to cost more than a normal coding task. `/close-gaps`
  used about $10 of model usage per run on this repo (four high-effort
  agents, 80–83 web calls; two runs measured 2026-09-27). `/gap-scan` is cheap.
- **What it writes.** `STRATEGY.md` and `assets/strategy-card.svg` — plus
  `assets/strategy-card.png` only if you ask for it — and it never commits.
  Files it didn't create are never overwritten: next to your own
  `STRATEGY.md` it writes `STRATEGY.distribution-god.md`, and next to your
  own card `assets/strategy-card.distribution-god.svg`. Its own previous
  report and card are archived to `docs/strategy-history/`. `/close-gaps`
  writes only `CLOSE-GAPS.md` (or `CLOSE-GAPS.distribution-god.md` beside your
  own file) and archives its previous run the same way. The full run also
  writes `FIRST-CUSTOMERS.md` (beside your own file of that name it writes
  `FIRST-CUSTOMERS.distribution-god.md`); on a re-run it keeps a
  `FIRST-CUSTOMERS.previous.md` copy and carries over your tracker.
- **Privacy.** Search queries include a one-line description of your
  product (and, for `/close-gaps`, the weakness being researched). For a stealth project, use `/gap-scan`: it does no web research
  (at most it reads your repo's own GitHub metadata with `gh`).
  `FIRST-CUSTOMERS.md` lists strangers' public posts, so keep it out of git:
  add `FIRST-CUSTOMERS*.md` to your `.gitignore`. The tool never contacts
  anyone, never records an email or phone number, and writes every draft to
  say that you built the product.

### Update

Installs are pinned to the plugin version, so pull new releases explicitly:

```
claude plugin marketplace update distribution-god && claude plugin update distribution-god@distribution-god
codex plugin marketplace upgrade && codex plugin add distribution-god@distribution-god
```

### Install from a clone (Codex fallback)

```
git clone https://github.com/jananthan30/distribution-god ~/.distribution-god
~/.distribution-god/install-codex.sh
```

This links the skills into `~/.agents/skills`; Codex names linked skills
after the plugin, so invoke `$distribution-god:distribution-god` and
`$distribution-god:gap-scan`. `--copy` installs a frozen snapshot named
`$distribution-god` and `$gap-scan`; `--uninstall` removes them. It never
deletes a skill folder it didn't create — anything in the way is moved to
`~/.agents/skills-backup/`.

## What makes the output trustworthy

- **Calibrated verdicts.** Bigness /25 and Moat /25 scored against anchored
  rubrics — every sub-score cites its evidence in the report. Every market
  number is labeled `ESTIMATE` with the arithmetic shown; every verdict names
  its crux, its cheapest falsifier, and dated kill criteria. "This is a
  feature, not a company" is a permitted answer.
- **Distribution-first.** Every gap names the channel it blocks. Every channel
  names this week's concrete action. One primary channel — spreading across
  four is the failure mode the report is built to prevent.
- **2026-aware.** Scores AI-era channels most strategy content ignores:
  GEO (being the answer AI assistants cite), agent-installability
  (MCP servers, plugin/skill marketplaces, llms.txt), and post-outbound
  community dynamics.
- **Adversarial by design.** A red team re-derives every score from the
  rubric and recomputes the market math; each serious objection is applied
  or rebutted on the record in the Dissent section.
- **Action, not just scores.** The path to the next band labels every move
  `outcome` or `rubric-only` and never projects a total, so it can't steer
  you into gaming the score. Every pivot keeps a named asset and has a test
  that can fail.
- **Honest outreach.** First-customer openings are real posts fetched during
  the run — linked, dated, quoted — never invented. One message per person,
  no follow-ups, authorship always disclosed.
- **Checked before you see it.** `scripts/check_report.py` rejects a report
  with missing sections, unfilled blanks, scores that don't add up, unsourced
  rivals, a broken card, path arithmetic that's off, or an incomplete pivot;
  `scripts/check_customers.py` rejects a people file with contact details,
  an undated or unlinked opening, or an undisclosed draft.

## Layout

```
skills/distribution-god/   orchestrator skill
  references/              moats · channel playbooks · AI-era channels ·
                           scoring rubrics · pivot playbook · first customers ·
                           report template · strategy card
  references/sensors/      repo-intel · market-scout · rival-scout · red-team ·
                           customer-scout methods
  scripts/                 strategy_card.py (renders the card) · check_report.py ·
                           check_customers.py (the FIRST-CUSTOMERS.md contract)
  assets/                  strategy-card template
skills/gap-scan/           fast local audit
skills/close-gaps/         research stage: triage → gap-researchers → pragmatist
  references/              idea rubric · CLOSE-GAPS.md template · sensor methods
  scripts/                 check_ideas.py (the CLOSE-GAPS.md contract)
agents/                    Claude Code subagents (thin wrappers over the sensor methods)
.claude-plugin/            plugin + marketplace manifests (Codex reads these too)
examples/                  reports on other public repos
evals/ · tests/            claude plugin eval suites · unit tests and fixtures
install-codex.sh           Codex fallback installer (~/.agents/skills)
docs/DESIGN.md             architecture & decisions
```

The skills follow the open [Agent Skills](https://agentskills.io) standard —
one methodology, both tools. With the plugin's agents available the sensors
run in parallel; otherwise the same sensor methods run as generic sub-agents
or in sequence.

## Contributing

`tests/run.sh` runs every check CI runs. Any change under `skills/` or
`agents/` needs a version bump — installs are pinned to the version string.
Change it in `.claude-plugin/plugin.json`; the unit tests then list every
other place it's pinned (`SKILL.md`, [CHANGELOG.md](CHANGELOG.md),
`llms.txt`, the scoring rubric, the card example) until they all agree. Ran it
on your repo and the verdict aged well (or badly)? Open a
[verdict check](https://github.com/jananthan30/distribution-god/issues/new?template=verdict-check.yml).

## License

MIT
