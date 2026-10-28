# Traction Doctor

**Point it at any repo. Get an investor-grade strategy report.**

[![validate](https://github.com/jananthan30/traction-doctor/actions/workflows/validate.yml/badge.svg)](https://github.com/jananthan30/traction-doctor/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-plugin-blueviolet)](https://code.claude.com/docs/en/plugins)
[![Codex](https://img.shields.io/badge/Codex-plugin-black)](https://developers.openai.com/codex)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-standard-blue)](https://agentskills.io)

**Claude Code**

```
/plugin marketplace add jananthan30/traction-doctor
/plugin install traction-doctor@traction-doctor
```

**OpenAI Codex**

```
codex plugin marketplace add jananthan30/traction-doctor
codex plugin add traction-doctor@traction-doctor
```

Then, in the repo you want analyzed, run `/traction-doctor` (Codex:
`$traction-doctor:traction-doctor`, or just ask for a strategy report).

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
(v0.1.0 scored itself 17/25; the anchored v0.2.0 rubric said 12; v0.4.0, on
fresher market inputs, says 11). These runs predate the rename in v0.5.0,
so they say distribution-god:

<img src="assets/strategy-card.svg" alt="Strategy card: its own verdict, run as distribution-god" width="600">

<!-- verdict-table:start -->
| | |
|---|---|
| **Bigness** | **11/25 — Niche tool / lifestyle business** (confidence: Medium) |
| **Moat today** | **1/25 — Nothing defensible yet:** the method is MIT and forkable in a day; one point for free, anti-hype counter-positioning |
| **The crux** | Recurring use: do builders come back — a re-run on each release, or fresh openings — or run it once and leave? |
| **Falsifier** | Now, with no listing needed: give 10 indie plugin authors who have a release coming `/gap-scan` as a per-release check (the full report on request) and count who runs either again on their next release — 3 of 10 by 2027-01-15 means true (free, about 11 weeks). Once listed: the Usage tab's retention and each skill's runs per active account ([docs](https://claude.com/docs/connectors/building/after-publishing#track-published-plugin-usage); up to 90 days, CSV export) |
<!-- verdict-table:end -->

A strategy tool that flatters you is worthless. This one is built to say
"this is a feature, not a company" — even about itself. When v0.4.0 went
looking for its own first customers, it found only two people asking in
public, both stuck at the directory's listing step, and the report says
so.

**On other repos:** see [`examples/`](examples/) — full reports on public
projects, each stamped with the commit, date, model, and run mode.

## It prescribed for itself

`/close-gaps` run on the 2026-09-26 report
([archived](docs/strategy-history/STRATEGY-2026-09-26.md)), unedited — from
[CLOSE-GAPS.md](CLOSE-GAPS.md) (23 minutes, 83 web calls, parallel mode; also
run as distribution-god):

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
| `/traction-doctor` (Codex: `$traction-doctor:traction-doctor`) | Full run: market + rivals research, distribution plan, gaps, moat, verdict, path to the next band, pivot options → `STRATEGY.md` + `assets/strategy-card.svg`; real first-customer openings with drafted replies → `FIRST-CUSTOMERS.md` (private) | ~15–20 min through the red team (v0.2.0, sequential, four repos), plus about 4 min of prospecting (measured once) |
| `/close-gaps` (Codex: `$traction-doctor:close-gaps`) | After a full run: researches trends, papers, and look-alike products for the report's weakest points → `CLOSE-GAPS.md`, at most five ideas, each with a linked precedent, a one-week test, and a stop signal | ~25 min (measured twice in parallel mode on this repo: 25 and 23 min) |
| `/gap-scan` (Codex: `$traction-doctor:gap-scan`) | Local-only audit of your distribution surface — prioritized gap table in chat | about a minute on a small repo, a few on a large one |

Also usable piecemeal in Claude Code: `@agent-traction-doctor:rival-scout`
("who competes with X and how do they grow"), `@agent-traction-doctor:red-team`
("attack this plan"), `@agent-traction-doctor:repo-intel`,
`@agent-traction-doctor:market-scout`, `@agent-traction-doctor:customer-scout`
("find people who need X"), `@agent-traction-doctor:gap-researcher`
("find proven ways to fix X"), `@agent-traction-doctor:pragmatist` ("attack
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
  `STRATEGY.md` it writes `STRATEGY.traction-doctor.md`, and next to your
  own card `assets/strategy-card.traction-doctor.svg`. Its own previous
  report and card are archived to `docs/strategy-history/`. `/close-gaps`
  writes only `CLOSE-GAPS.md` (or `CLOSE-GAPS.traction-doctor.md` beside your
  own file) and archives its previous run the same way. The full run also
  writes `FIRST-CUSTOMERS.md` (beside your own file of that name it writes
  `FIRST-CUSTOMERS.traction-doctor.md`); on a re-run it keeps a
  `FIRST-CUSTOMERS.previous.md` copy and carries over your tracker.
- **What it runs.** Only your client's own tools: it reads files and git
  history, runs `gh repo view` for your repo's GitHub details when `gh` is
  installed, and runs its bundled Python checkers and card renderer (plus
  `xmllint`, if installed, to check the card). The optional PNG card is drawn
  on your machine with headless Chrome or `rsvg-convert`. It never installs
  packages or runs code it fetched, and it writes the card's data to a temp
  file outside your repo.
- **Privacy.** Nothing goes to the plugin's author: there is no server and
  no telemetry. What leaves your machine is web research, sent by your
  client's WebSearch and WebFetch tools, with queries built from a one-line
  description of your product, its category, its rivals and the pain it
  solves (and, for `/close-gaps`, the weakness being researched). The
  customer scout also queries three keyless public APIs (GitHub issue
  search, Hacker News search through Algolia, and Stack Exchange), and
  `/close-gaps` queries arXiv, OpenAlex and Hugging Face Papers. For a
  stealth project, use `/gap-scan`: it does no web research (at most it
  reads your repo's own GitHub metadata with `gh`). `FIRST-CUSTOMERS.md`
  lists strangers' public posts, so keep it out of git: add
  `FIRST-CUSTOMERS*.md` to your `.gitignore`. The tool never contacts
  anyone, never records an email or phone number, and writes every draft to
  say that you built the product. This repo's `.github/` workflows are its
  own CI; installing the plugin never runs them. Details:
  [PRIVACY.md](PRIVACY.md).

### Update

Installs are pinned to the plugin version, so pull new releases explicitly:

```
claude plugin marketplace update traction-doctor && claude plugin update traction-doctor@traction-doctor
codex plugin marketplace upgrade && codex plugin add traction-doctor@traction-doctor
```

Coming from **distribution-god**, this plugin's name before v0.5.0? The
marketplace was renamed too, so swap it in Claude Code:

```
claude plugin uninstall distribution-god@distribution-god
claude plugin marketplace remove distribution-god
claude plugin marketplace add jananthan30/traction-doctor
claude plugin install traction-doctor@traction-doctor
```

In Codex, add it again with the install commands at the top.

### Install from a clone (Codex fallback)

```
git clone https://github.com/jananthan30/traction-doctor ~/.traction-doctor
~/.traction-doctor/install-codex.sh
```

This links the skills into `~/.agents/skills`; Codex names linked skills
after the plugin, so invoke `$traction-doctor:traction-doctor` and
`$traction-doctor:gap-scan`. `--copy` installs a frozen snapshot named
`$traction-doctor` and `$gap-scan`; `--uninstall` removes them. Both also
clear out what an install before v0.5.0 left under the old name. It never
deletes a skill folder it didn't create — anything in the way is moved to
`~/.agents/skills-backup/`.

### Troubleshooting

- **The report says `NOT RESEARCHED`.** Web access was off or denied. Allow
  WebSearch and WebFetch (see *Before you run*) and run it again.
- **A command or agent is missing.** Plugins load when a session starts, so
  start a new session after you install or update. `claude plugin list`
  should show traction-doctor as enabled.
- **"Only N openings found".** That's a finding, not a failure: the people
  you want rarely ask in public, so the report leads with an offer to make
  instead of people to reply to.
- **A file appeared with `.traction-doctor` in its name.** It never
  overwrites a file it didn't create, so it writes beside yours (for
  example `STRATEGY.traction-doctor.md`).
- **Anything else:** open an
  [issue](https://github.com/jananthan30/traction-doctor/issues) with the
  command you ran and the last lines of its output.

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
skills/traction-doctor/    orchestrator skill
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
[verdict check](https://github.com/jananthan30/traction-doctor/issues/new?template=verdict-check.yml).

## License

MIT
