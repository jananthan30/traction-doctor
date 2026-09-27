# Idea Rubric — targets, triage, score, top five

These rules turn a strategy report's weak points into at most five ideas
worth a week each. They exist to prevent the two failure modes of AI idea
lists: the generic ("build a community") and the impractical (a paper's
result that needs a million users). `scripts/check_ideas.py` enforces every
mechanical rule below; the pragmatist enforces the judgment calls.

## Target ids

Every weakness is named by a target id. The research brief, the idea cards,
the `cg` line, and the checker all use the same ids.

| Weakness | Target ids |
|---|---|
| Bigness sub-score | `bigness.market`, `bigness.why_now`, `bigness.wedge`, `bigness.expansion`, `bigness.delivery` |
| Moat row | `moat.network`, `moat.switching`, `moat.scale_data`, `moat.brand`, `moat.cornered_counter` |
| The report's crux | `crux` |
| A gap-table row | `gap.<n>`, the 1-based row in the report's §6 table |

When two candidates describe the same underlying weakness, merge them into
one target and join the ids with `+` — e.g. `crux+bigness.wedge` when the
crux is recurring use and the wedge's next anchor needs evidence of
re-runs. Research at most three targets.

## Triage

**Candidates:** the crux; every Bigness sub-score of 3 or less; the Moat
rows the report names under *Buildable powers*; every P0 and P1 gap.

**Buckets** — record every candidate's bucket in the file:

| Bucket | Test | Goes to |
|---|---|---|
| Known fix | The report already names a concrete fix, and doing it is the only blocker: push a branch, submit a form, add a file | *Just do it* — no research |
| Structural | The outside world sets the score, so only a strategy change moves it. By default: `bigness.market` (the market's size) and `bigness.why_now` (external tailwinds) | *Can't move now* — with what would move it, and "re-run /distribution-god after that change" |
| Unknown fix | Nobody in the report knows the best way to close it | Research candidate |

**Ranking** — research candidates, highest first:

1. **The crux**, when it is an unknown fix. An idea that makes it come true
   has the highest possible impact by definition.
2. **Band-crossers:** candidates whose next anchor, alone or together with
   one other candidate's next anchor, moves the Bigness or Moat total
   across a band boundary. Bigness bands: 0–7, 8–13, 14–19, 20–25. Moat
   bands: 0–4, 5–9, 10–16, 17–25.
3. **P0 gaps**, then P1 gaps.
4. **The rest**, lowest current score first.

Keep the top three. A target the user names replaces the ranking and is
the only target.

**The target itself.** For a sub-score or Moat row: the next anchor up in
`../distribution-god/references/scoring-rubrics.md`, quoted. When the
report's evidence column says what would earn the higher score, carry that
sentence into the brief. For the crux: the crux coming true. For a gap: the
gap closed.

**Worked example.** distribution-god's own report (2026-09-26) scored
Bigness 12, two points below the 14–19 band. The rubric says Wedge
sharpness 2→3 needs evidence that authors re-run the tool on each release,
and Delivery leverage 3→4 needs a way to capture value that exists today.
Two ideas that earn those anchors change the headline from "Niche tool /
lifestyle business" to "Strong business possible". Two points on a report
at 9/25 would change nothing a reader sees — so band-crossers rank above
them.

## The idea card

Every surviving idea is a card; a cut idea is one row in *Shiny but not
now*.

```markdown
### I<n>. <one line: the specific mechanism>
- **Closes:** `<target id>` <current> → <target> — <plain-words weakness>
- **Kind:** <proven | fresh | reasoned>
- **Fits:** <prerequisites present, with path:line; the missing piece, if any>
- **Proof:** <precedent, dated outcome, "quote", link — or `unverified`>
- **1-week test:** cost: <free | $n>
  1. <step>
- **Success:** <metric ≥ level> by <YYYY-MM-DD>
- **Stop if:** <metric < level> by <YYYY-MM-DD>
- **If it works:** <next step> · **Full build:** <S | M | L>
- **Score:** Impact <a> · Proof <b> · Fit <c> · Cheap <d> = <n>/20
```

- **Kind.**
  - `proven` — the proof is a look-alike's result. Needs Proof 3 or more.
  - `fresh` — the proof is a trend dated within 12 months of the run, or a
    paper published within 24 months of it. The Proof line carries the date.
  - `reasoned` — the proof is reasoning from a cited mechanism. Proof is 1.
- **Proof.** A precedent, its dated outcome, a quote of at most 25 words
  from the primary page, and the link. A claim you couldn't confirm is
  `unverified`, and Proof is then at most 1.
- **1-week test.** At most five numbered steps and at most five working
  days of work, with the cost stated (`cost: free` or `cost: $<n>`).
- **Dates.** The Success and Stop-if dates fall after the run date and no
  more than 28 days after it: a week of work, then time to read the result.
- **Full build.** S is at most a week, M at most a month, L more. L marks a
  *big bet*.

## Score (/20)

Score each part against its anchors. Award 2 or 4 when the evidence
clearly exceeds the anchor below but misses a named condition of the anchor
above (say which), as the Moat rubric does. **Any part at 0 cuts the idea.**

| Part | 5 | 3 | 1 | 0 → cut |
|---|---|---|---|---|
| **Impact** — what success does to the verdict | Crosses a Bigness or Moat band boundary (alone, or with another top idea it names), closes a P0 gap, or makes the crux come true | Earns the next anchor on one sub-score or Moat row, or closes a P1 gap | P2 polish, or strengthens evidence without moving a score | Touches no named weakness |
| **Proof** — why we believe it works | Worked for a comparable product at a comparable stage (team size, delivery form, traction), with a dated before/after number and a link | Worked at a different stage; or a trend with dated adoption numbers; or a paper with code or a reported deployment | A paper without code or deployment, a single anecdote, or reasoning from a cited mechanism; also the cap for `unverified` | No source |
| **Fit** — can this repo and team do it | Every prerequisite exists (path:line) and the team has done this kind of work | Exactly one prerequisite is missing, and the 1-week test builds it | Needs something the team lacks: an audience, money, a skill, a partner | Contradicts a repo fact or a report finding |
| **Cheap** — the first test | Under a day of work, free | At most five working days, free | At most five working days, but costs up to $100 or needs outside help | No test fits in a week, or it costs more than $100 |

**Outcomes, not scores.** Impact measures a real outcome — users,
retention, revenue, defensibility — expressed through the rubric. An idea
that satisfies a rubric condition without moving a real outcome scores
Impact 1 at most. Example: a `FUNDING.yml` sponsor link satisfies Delivery
leverage's value-capture cap without capturing value.

## Top five

1. Each researched target contributes its best surviving idea, if it has one.
2. At least one `fresh` idea, if any survived (waived on a local-only run).
3. At most one big bet (Full build L).
4. Remaining slots go by score; ties go to higher Proof, then higher Cheap.
5. Fewer than five survivors: list fewer. Never pad.
6. Sort the table by score, highest first. *Do this first* is its first row.

A survivor stays out of the table only when the table is full, or when it
would be a second big bet.
