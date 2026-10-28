# Changelog

All notable changes to distribution-god. The version in
`.claude-plugin/plugin.json` pins installs: Claude Code and Codex keep users on
the cached copy until it changes, so every release that touches `skills/` or
`agents/` bumps it (CI enforces this).

## [0.4.0] — 2026-10-28

### Added
- **Path to the next band**, right under the Verdict scores: how many points
  stand between the report and the next Bigness and Moat band, 2–5 moves
  that would earn the next rubric points (each quoting the anchor it aims
  at), and the caps locking points today. Every move is labeled `outcome`
  (it changes users, retention, revenue or defensibility) or `rubric-only`
  (it only meets the anchor's wording); a path with no `outcome` move is
  rejected as score gaming, and no move may project a total. The checker
  verifies the arithmetic against the `dg` line, and the red team re-judges
  every move's kind (a new seventh attack surface).
- **Pivot options**: section 9 becomes *Kill criteria and pivot options*.
  Each report offers 1–3 pivots from Eric Ries's ten types (at least 2 when
  the moat is *Nothing defensible yet* or Bigness is 13 or less). Every
  pivot keeps a named asset from the repo, names the moat power it unlocks,
  carries an ESTIMATE re-score, a precedent, and a test of at most five days
  with a pass line, and is started by a kill criterion that names it; a
  *Persevere if* line says when to stay the course. New reference:
  `references/pivot-playbook.md`. The red team attacks pivot realism.
- **First customers**: the tool now does the prospecting. A new research
  sensor, `customer-scout` (web and read-only tools only — no shell, no
  writes), runs in a new Phase 6, after the red team settles the wedge. It
  finds real, recent public posts — GitHub issues, Hacker News, Stack
  Exchange, forums — where the wedge customer asked for what the product
  does, each with its URL, post and fetch dates, and the person's own words,
  plus every venue's self-promotion rule (karma minimums, megathreads) and a
  search link. The strategist writes **`FIRST-CUSTOMERS.md`**, a private
  working file: who to look for, the offer, the openings, message drafts
  that always disclose authorship, a 14-day plan, a tracker, and the rules
  (one message per person, no follow-ups). The report's section 5 gains a
  *First customers* sub-section that names venues, never people. Re-runs
  keep the user's own file, carry over tracker rows, and never re-suggest
  someone already contacted. Local-only runs give search links and drafts,
  marked NOT RESEARCHED, with no people.
- `scripts/check_customers.py` enforces the people file: structure, no email
  addresses or phone numbers, each opening's link, dates and short quote,
  drafts' disclosure, a tracker that covers every opening. `check_report.py`
  rejects individual post links in the report and checks the linked people
  file when present (a missing one is a warning — it's meant to stay
  private).
- The reply in chat leads with who to contact today and which pivot each
  kill criterion starts, then the verdict.

### Changed
- `check_report.py` reads the report's version from its `dg` line: reports
  from v0.4.0 on get the v0.4.0 contract, older reports keep the one they
  were written under (the examples and the archive still pass). The line
  budget for v0.4.0 reports is 500.
- The full-run evals grade the new parts: the path block, pivot options, the
  First customers sub-section and the people file (web: real openings or
  "only N found", no email addresses; offline: `NOT RESEARCHED` and no post
  links). `tests/run.sh` checks people files. README, `llms.txt`, the design
  doc and both manifests describe v0.4.0.
- The self-analysis is regenerated with v0.4.0 (2026-10-28, generic-subagents
  mode): Bigness 12 → 11 on fresher market inputs, Moat 1, a path to the
  next band, two pivots, and a first-customers search that found only two
  public asks — kept in a gitignored `FIRST-CUSTOMERS.md`. The 2026-09-26
  report and its card are archived in `docs/strategy-history/`.

## [0.3.0] — 2026-09-27

### Added
- **`/close-gaps`** (Codex: `$distribution-god:close-gaps`): the prescription
  after the diagnosis. It reads a distribution-god `STRATEGY.md`, sorts the
  report's weak points into known fixes (*Just do it*), structural limits
  (*Can't move now*), and open questions, and researches up to three open
  ones through current trends, papers (arXiv, OpenAlex, Hugging Face Papers,
  all keyless), and products that closed the same weakness. It writes
  `CLOSE-GAPS.md`: at most five ideas, each scored /20 on Impact, Proof, Fit
  and Cheap (any 0 cuts it), with a linked precedent, a first test of at
  most five working days, a dated success metric, and a stop signal.
- `gap-researcher` and `pragmatist` agents. The pragmatist runs six checks
  (proof, transfer, a test that can't fail, hidden costs, score gaming,
  missed idea); its serious objections are applied or rebutted in Dissent.
- `skills/close-gaps/scripts/check_ideas.py` enforces the `CLOSE-GAPS.md`
  contract: sections, the machine-readable `cg` line, complete idea cards,
  score arithmetic, Kind/Proof rules, date windows, and the top-five rules.
- Evals `close-gaps-web`, `close-gaps-offline` and `close-gaps-no-report`.

### Changed
- The full run's closing message offers `/close-gaps`.
- `install-codex.sh` installs the new skill.
- `check_report.py` exposes its template-slot check as `unfilled_slots()`,
  shared with `check_ideas.py`.

## [0.2.0] — 2026-09-25

### Added
- **Strategy card**: every run renders `assets/strategy-card.svg`, a shareable
  verdict infographic with the `Generated by distribution-god` fingerprint.
  Rendered by `scripts/strategy_card.py` from plain JSON — it escapes text,
  derives band labels from the rubric, checks each line fits its box, and
  refuses to overwrite an SVG it didn't generate. `png` subcommand for a
  social-post twin.
- **Report checker** `scripts/check_report.py`: the skill runs it before
  finishing; it fails on missing sections, unfilled slots, scores that
  disagree between the `dg` line and the tables, wrong band labels,
  unlabeled market figures, unsourced rivals, and a linked card that is
  missing, broken, or shows different scores.
- The checker recomputes every market calculation written with ×, x, ÷ or +
  (ranges, k/M/B and million/billion included), requires the Size headline
  to be the result of one of them, checks the stated geometric midpoint, and
  checks the Market headroom score against the midpoint's dollar band.
  `NOT RESEARCHED` is accepted only on a local-only run, whose score caps and
  Low confidence are enforced; the card's confidence label, version and date
  must match the report.
- Machine-readable `<!-- dg: {...} -->` line in every report (plugin version,
  rubric version, UTC date, mode, scores), used to compute the Delta section
  on re-runs.
- Bigness breakdown and Moat today tables in the report, each sub-score with
  evidence.
- Local-only mode when web access is missing (sections 2–3 marked
  `NOT RESEARCHED`, confidence capped at Low).
- Sensor methods in `skills/distribution-god/references/sensors/`, shared by
  the Claude Code agents and every Codex mode.
- `tests/` (unit tests + fixtures), `evals/` for `claude plugin eval`
  (gap-scan, offline full run, web full run), CI
  workflow, `llms.txt`, traffic logging, verdict-check issue template,
  example reports on other repositories.

### Changed
- Scoring rubric (version 2) anchors every Bigness score 0–5. Market
  headroom maps the geometric midpoint of the capturable SAM to fixed dollar
  bands; Wedge sharpness is capped at 3 without evidence from the wedge ICP;
  Delivery leverage 4–5 needs a way to capture value. Moat is five rows with
  0/1/3/5 anchors and named bands. Falsifiers must be measurable (GitHub code
  search doesn't index small repos). Scores are not comparable to v0.1.0
  scores one-for-one.
- Channel playbook: incremental reach for already-won channels, `claimed`
  and `ignition` calls, a crux-based tie-break, and Anthropic's plugin
  directory as both channel and usage meter.
- Research rules: confirm load-bearing claims on the primary page, not a
  search summary; fallbacks for client-rendered vendor pages; a defined
  "web research degraded" path when search runs out mid-run.
- Observer mode for analyzing someone else's repo; monorepos of thin clients
  are analyzed as one hosted service; dates are UTC.
- Strategy card: full-width install line (fits real plugin, Docker, and MCP
  install commands), documented length guides measured against the renderer.
- Execution modes: `parallel` only when the plugin's agents exist;
  `generic-subagents` (e.g. Codex) hands each sub-agent its sensor method;
  `sequential` reads the same methods inline.
- The red team receives the rubric and sub-scores, re-derives scores,
  recomputes market math, and its fatal/serious objections must be applied
  or rebutted in Dissent.
- Rival research no longer pads to a minimum count, requires a source per
  rival, and never cites model memory as mindshare.
- An existing `STRATEGY.md` not written by this tool is never overwritten; a
  prior report is archived to `docs/strategy-history/`.
- `repo-intel` runs with an explicit tool allowlist (Read, Grep, Glob,
  Bash) instead of inheriting every tool; it is read-only by instruction.
- `install-codex.sh` validates options, never deletes paths it didn't
  create (it moves them to `~/.agents/skills-backup/`, outside Codex's scan
  path), prints the skill names each mode actually produces, and documents
  `codex --search`; README leads with Codex's native plugin install.
- Strategy card width budgets hold in DejaVu Sans (the widest common Linux
  fallback), and the font stack prefers Helvetica-metric fonts.

## [0.1.0] — 2026-08-09

### Added
- Initial release: `/distribution-god` orchestrator skill with repo-intel,
  market-scout, rival-scout, and red-team agents; `/gap-scan`; reference
  library (moats, channel playbooks, AI-era distribution, scoring rubrics,
  report template); Codex installer.
