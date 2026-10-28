# v0.4.0 — Action sections: path to the next band, pivot options, first customers

**Date:** 2026-10-28 · **Status:** approved ("do it") · **Branch:** `v0.4.0`
(stacked on the unmerged `v0.3.0`)

## Problem Statement

A distribution-god report diagnoses well and prescribes thinly. The owner's
words: "currently it's just scores — it needs to give more: how to pivot if
the moat is not there, how to improve it and make it better, how to reach the
first customers — do it."

Measured against the report this repo wrote about itself (2026-09-26):

- **Pivots** appear only as a clause inside kill criteria ("stop or pivot"),
  with no pivot named, no asset it keeps, no test.
- **Improvement** lives in the Evidence column ("3 needs evidence that…"),
  scattered across five rows, and in a separate command (`/close-gaps`) the
  user has to know to run.
- **First customers** get one bullet ("First 10: hand-to-hand…"). The tool
  never finds a single real person who asked for what the product does, and
  never drafts the message. The owner then hit two Reddit karma gates the
  report didn't mention.

## Solution

Three action parts, added inside the existing report sections so nothing is
renumbered, plus a private companion file:

1. **Path to the next band** — under the Verdict scores: the arithmetic to
   the next Bigness and Moat band, 2–5 moves that would earn the next rubric
   point, each labeled `outcome` (changes users, retention, revenue or
   defensibility) or `rubric-only`, and the cap rules locking points today.
2. **Pivot options** — in section 9, renamed *Kill criteria and pivot
   options*: 1–3 pivots from Eric Ries's catalog, each keeping a named repo
   asset, unlocking a named moat power, with a ≤5-day test, a precedent, an
   ESTIMATE re-score, and the kill criterion that triggers it; plus a
   *Persevere if* line.
3. **First customers** — a new research sensor, `customer-scout`, runs after
   the red team settles the wedge. It finds real, recent public posts where
   the wedge ICP asked for what the product does. The report's section 5
   gains a *First customers* sub-section (the offer, the venues with their
   self-promotion rules, counts, search links — no individual posts). The
   people, the drafted messages, a 14-day plan and a tracker go in
   `FIRST-CUSTOMERS.md`, a private working file the user keeps out of git.

The chat reply leads with who to contact today and which pivot each kill
criterion triggers, then the verdict.

## User Stories

1. As a builder with a low Moat score, I want named pivots that reuse what I
   already built, so that a weak verdict comes with a way out instead of a
   dead end.
2. As a builder, I want each pivot to say which asset it keeps, so that I can
   see it isn't "start over".
3. As a builder, I want each pivot to name the moat power it unlocks and how,
   so that I can tell why it would be more defensible than today.
4. As a builder, I want each pivot to carry a test of at most five working
   days with a pass line, so that I can check it before committing to it.
5. As a builder, I want each pivot tied to the kill criterion that triggers
   it, so that I know when to switch, decided in advance.
6. As a builder, I want a *Persevere if* line, so that I know what result
   means "don't pivot".
7. As a builder, I want a precedent for each pivot (a product that made the
   same move, linked), so that the pivot isn't speculation.
8. As a builder, I want each pivot's re-score labeled ESTIMATE, naming the
   sub-scores that would move and why, so that I can compare ceilings
   honestly.
9. As a builder, I want the report to tell me how many points I need for the
   next band, so that "12/25" becomes a target, not a grade.
10. As a builder, I want 2–5 moves that would earn the next rubric point,
    each quoting the anchor it aims at, so that I know exactly what evidence
    or change counts.
11. As a builder, I want each move labeled `outcome` or `rubric-only`, so
    that I'm never steered into gaming the score instead of growing.
12. As a builder, I want the cap rules locking my scores spelled out (Wedge
    ≤ 3 without evidence from the wedge ICP; Delivery ≤ 3 without existing
    value capture), so that I know which points no amount of polish unlocks.
13. As a builder, I want the tool to find real people who recently asked,
    in public, for what my product does, so that my first outreach goes to
    people who want it.
14. As a builder, I want each person's post linked, dated, and quoted in
    their own words, so that I can check the fit myself in seconds.
15. As a builder, I want message drafts written for those posts, so that
    reaching out takes minutes, not an evening.
16. As a builder, I want every draft to disclose that I built the product,
    so that my outreach is honest and doesn't get me banned.
17. As a builder, I want each venue's self-promotion rule (karma gates,
    megathreads, flair) with a link, so that I don't get auto-removed like
    last time.
18. As a builder, I want a concrete offer for the first ten (what they get,
    what I ask back), so that my message has a reason to be answered.
19. As a builder, I want a 14-day plan and a tracker table, so that I can run
    outreach as a routine and see what's working.
20. As a builder, I want prebuilt search links for venues the tool couldn't
    fetch, so that I can find more openings myself.
21. As a builder, I want the people list kept out of my public report and
    flagged as private, so that strangers' posts with pitches drafted at
    them never land in a public repo.
22. As a builder re-running the tool, I want people I already contacted
    carried over with my notes and never suggested as new, so that I never
    message someone twice.
23. As a builder running without web access, I want the search links and
    drafts anyway, clearly marked NOT RESEARCHED and with no invented people,
    so that the offline run is still useful and still honest.
24. As a builder, I want the chat reply to lead with who to contact today and
    which pivot each kill criterion triggers, so that I don't have to open a
    file to know what to do.
25. As a builder with my own `FIRST-CUSTOMERS.md`, I want the tool to leave it
    untouched and write beside it, so that it never overwrites my notes.
26. As a maintainer of this plugin, I want old v0.2/v0.3 reports to keep
    passing the checker, so that the examples and history stay valid.
27. As a maintainer, I want the checker to enforce the new parts (arithmetic
    against the scores, pivot fields, privacy of the people file), so that a
    run can't hand back a thin or unsafe version.
28. As a maintainer, I want the red team to attack the new parts, so that
    pivots and moves face the same adversarial pass as the verdict.
29. As a maintainer, I want the research sensor that reads the most untrusted
    pages to have no shell and no write access, so that a hostile page can't
    turn into a command.
30. As a close-gaps user, I want the scoring rubric unchanged, so that
    `/close-gaps` keeps accepting new reports.

## Implementation Decisions

**Owner's decisions:** the three action parts; the tool does the prospecting
("do it").

**Design decisions taken under "do it"** (owner may revisit):

- **No renumbering.** close-gaps addresses gap rows as `gap.<n>` in §6, and
  the checker and evals key on §7 and §10. The new parts sit inside existing
  sections: the path block inside `## Verdict`, *First customers* as a `###`
  sub-section of §5, pivot options inside §9 (heading text becomes *Kill
  criteria and pivot options*; the checker matches the `## 9. Kill criteria`
  prefix, so old reports still pass).
- **Version-gated contract.** The report checker applies the new checks only
  when `dg.v ≥ 0.4.0`. v0.2/v0.3 reports, the examples and the archive keep
  passing unchanged. The scoring rubric stays version 2; projections never
  enter the `dg` line or the card. The card is unchanged.
- **Path block collides with nothing.** The Verdict section's existing checks
  read every table row whose first cell is `Bigness`, `Moat today`, a
  dimension name or `Total`. The path table's first column is a move number,
  and the dimension it raises sits in a later column, so those checks can't
  be fooled.
- **Path arithmetic is checked.** The block's header line states `Bigness
  <n> → <floor> (<band>) needs +<gap>` and the same for Moat, where `<n>`
  matches the `dg` line, `<floor>` is the next band's lower bound and its
  label, and `<gap>` is the difference. Top bands state *top band* instead.
  Each move row's `Now → next` must start at the `dg` value for the
  dimension it raises and end higher, at most 5. Kinds are exactly `outcome`
  or `rubric-only`; at least one move is `outcome`. A *Locked by caps* line
  is required. The report never sums projected lifts into a projected total.
- **Pivot catalog.** Eric Ries's ten pivot types (*The Lean Startup*, 2011):
  zoom-in, zoom-out, customer-segment, customer-need, platform,
  business-architecture, value-capture, engine-of-growth, channel,
  technology. At most 3 cards; at least 2 when the Moat band is *Nothing
  defensible yet* or Bigness is 13 or less. Each card names a type from the
  catalog and has *Keeps*, *Changes*, *Unlocks* (naming a moat power),
  *Projected (ESTIMATE)*, *Precedent* (link or `unverified`), *Test (≤5
  days, ~$0)* with a pass line, and *Trigger*; at least one kill criterion
  names each pivot ("run Pivot A's test").
- **Prospecting runs late.** `customer-scout` needs the final wedge (set in
  Phase 3, possibly changed by the red-team disposition) and market-scout's
  watering holes, so it runs in a new Phase 6, after the disposition and
  before writing. In parallel mode it is a named agent; otherwise a generic
  sub-agent or the orchestrator itself, per the existing mode rules.
- **customer-scout's tools:** web search, web fetch and read-only file tools.
  No shell, no writes — it reads the most hostile content of any sensor.
- **customer-scout's rules:** an opening is a post where someone asked for
  what the product does; recent (prefer ≤ 90 days; never over a year);
  thread still open to replies; real person or org, not a vendor or bot.
  Every opening carries the exact URL, the post date, the date fetched this
  run, and a verbatim quote of at most 15 words, or it is dropped (a fetch
  that failed becomes a "search it yourself" link, never a prospect). Cap
  about 10. Never record emails, phone numbers or real names beyond the
  public handle in the URL; never link one person's accounts across sites.
  Reddit fetches usually fail: use the HN Algolia API, GitHub search and the
  Stack Exchange API directly, and give Reddit as prebuilt search links.
  Record each venue's self-promotion rule with a link, or `unverified`.
- **Privacy split.** `STRATEGY.md` (often committed) holds only the offer,
  venues, rules, counts and search links — the checker rejects individual
  post links (Reddit comments, HN items, GitHub issues, Stack Overflow
  questions) in that sub-section. `FIRST-CUSTOMERS.md` holds the people,
  opens with a private-file notice, and the skill tells the user to add
  `FIRST-CUSTOMERS*.md` to `.gitignore` (it never edits `.gitignore`
  itself). This repo gitignores its own.
- **Outreach rules baked into the file:** one message per person, no
  follow-ups unless they reply; every draft discloses authorship; follow each
  venue's rule; contact only through the venue where they posted.
- **File collisions and re-runs.** A `FIRST-CUSTOMERS.md` without the
  fingerprint is the user's: leave it, write
  `FIRST-CUSTOMERS.distribution-god.md`. A prior run's file is copied to
  `FIRST-CUSTOMERS.previous.md` (beside it, equally private), its tracker
  rows the user touched are carried over, and new openings are deduplicated
  by URL against every prior row. No archive into `docs/strategy-history/`
  (that folder is often committed).
- **People-file checker.** A new standard-library module validates
  `FIRST-CUSTOMERS.md`: title, fingerprint, private notice, sections in
  order, no unfilled slots, no email addresses or phone numbers (narrow
  pattern: ISO dates, star counts, versions and SHAs must not trip it), each
  opening's link, dates and short quote, every draft's disclosure, a tracker
  covering every opening, the one-message rule. Offline files say NOT
  RESEARCHED and contain no individual post links. The report checker calls
  it when the linked file exists; a missing file is a warning (expected when
  kept private).
- **Red team.** A seventh attack surface: are the pivots real (asset kept,
  power unlocked, test can fail, tied to a kill criterion)? Is any
  `outcome` move really `rubric-only`? Has a projected total crept in? The
  payload gains the path block and the pivot cards.
- **Chat reply order:** who to contact today (top 3 openings, linked — the
  chat is private), which pivot each kill criterion triggers, the verdict
  box, the five actions, the paths written with the gitignore advice, then
  the `/close-gaps` offer.
- **Line budget** rises from 450 to 500 (a warning, not an error); the bulk
  of the new content lives in `FIRST-CUSTOMERS.md`.

## Testing Decisions

- **Seams:** the two checkers' `check(path)` functions — the highest seam
  (they are the report contract) and the one existing tests already use.
  Good tests copy a valid fixture to a temp dir, break one thing, and assert
  the checker names it; they never assert on internal helpers.
- **Fixture:** the synthetic sample report moves to v0.4.0 and gains the
  three parts plus a synthetic `FIRST-CUSTOMERS.md`. Old-layout coverage:
  a test that downgrades the fixture's version and strips the new parts
  still passes, and the v0.2.0 examples keep passing in `tests/run.sh`.
- **New negative tests:** path arithmetic off by one; a move starting below
  the `dg` value; a move with an unknown kind; all moves `rubric-only`; the
  path table's rows can't spoof the Verdict checks; a pivot with an unknown
  type, a missing field, no pass line, or no kill criterion naming it; too
  few pivots for a weak moat; an individual post link in the report's First
  customers sub-section; an email or phone number in the people file; ISO
  dates, star counts, versions and SHAs don't count as phone numbers; an
  opening without a link, date or short quote; a draft without disclosure;
  an offline file with a post link.
- **Prior art:** `tests/test_scripts.py` (report checker cases) and
  `tests/test_check_ideas.py` (a second checker with its own fixture).
- **Evals** (written, not run — they cost API money): the web full run
  checks the people file exists with its notice and contains no emails; the
  offline full run checks NOT RESEARCHED and zero post links.
- **Dogfood:** run v0.4.0 on this repo by following the working-tree
  `SKILL.md` (the session's loaded plugin is an older cached copy), verify
  the outputs with both checkers and `strategy_card.py check` — no visual
  checks.

## Out of Scope

- Sending, posting, or scheduling any message; any CRM or email tool.
- Collecting contact details or enriching profiles.
- Changes to the scoring rubric, the strategy card, `/gap-scan` or
  `/close-gaps`.
- Re-running `/close-gaps` on the new self-report (offered, not done).
- Pushing the branch, merging, tagging, or directory submission.

## Further Notes

- The self-report's kill criteria date 2026-11-15 and 2026-12-26 for the
  directory listing; a v0.4.0 self-run will re-derive them.
- `customer-scout` mirrors `market-scout`/`rival-scout` in format: an agent
  file pointing at a method file under `references/sensors/`, so Codex's
  generic-subagents mode reads the same method.
