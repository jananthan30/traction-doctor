# Scoring Rubrics & Calibration Rules

These rubrics exist to prevent the two failure modes of AI strategy output:
hype ("this could be huge!") and hedge ("it depends"). Score honestly, show the
arithmetic, name the falsifier.

This is **rubric version 2** (distribution-god v0.2.0). Reports record it as
`"rubric": 2` in their `dg` line; scores from a different rubric version are
not one-for-one comparable, and the Delta section must say so.

**Anchoring rule (makes re-runs agree):** every sub-score cites one line of
evidence (`path:line` or a link). A score is the highest anchor the evidence
fully meets — when torn between two anchors, take the lower one and say what
evidence would earn the higher.

## Bigness Score (/25) — "how big can this get?"

Score each dimension 0–5 against the anchors below. Sum. Every sub-score goes
in the report's **Bigness breakdown** table with its evidence.

**Market headroom** — the midpoint of the reconciled SAM from the Market
section's `ESTIMATE` range. Use the **geometric midpoint**, √(low × high)
(e.g. $10M–$160M → $40M), because the bands are logarithmic.

SAM here means: the number of ICPs who would need the product's strongest
plausible paid offering (hosted tier, team or enterprise features, support)
× what they would pay for it per year. Count buyers who need the paid layer
— e.g. teams that require hosting or SSO — not every free user; don't apply
a market-share or conversion forecast on top (that's the obtainable market,
which this rubric doesn't score). If the repo has no paid path at all, size
the paid layer the strategy would have to build, and say so in the Size
bullet. For tiered pricing, the low end uses the entry paid tier's annual
price and the high end the tier the wedge ICP would most plausibly buy — not
an enterprise list-price ceiling; name the tiers you used. When an input
can't be sourced, state it as an assumption with its range; the confidence
label carries that uncertainty.

| 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| < $50M | $50–200M | $200–500M | $0.5–2B | $2–10B | > $10B |

**Why-now force**

| Score | Anchor |
|---|---|
| 0 | None; could have existed in 2015 |
| 1 | A generic tailwind ("AI is growing") with no mechanism tied to this product |
| 2 | One plausible tailwind with a named mechanism, but unsourced or not specific to this ICP |
| 3 | One real, sourced tailwind (platform shift, cost collapse, behavior change) that directly enables this product |
| 4 | Two independent sourced tailwinds (neither causes the other — two facets of one platform shift, including its demand-side and supply-side effects, count as one), or one strong tailwind whose opening closes within ~2 years (an opportunity this product can still seize — a threat to it, like an incumbent bundling the feature, is a timing risk, not a tailwind) |
| 5 | Multiple compounding tailwinds; window measured in quarters |

**Wedge sharpness**

| Score | Anchor |
|---|---|
| 0 | "For everyone" — no specific user |
| 1 | A broad persona ("developers", "small businesses") with a vague job |
| 2 | A named ICP, but the job is occasional or low-pain |
| 3 | Identifiable ICP with a painful, frequent job ("frequent" = how often the ICP needs the job this product does, not how often they face the broader goal behind it) |
| 4 | As 3, plus external evidence people seek this: requests or threads from at least 3 different people or orgs, or one with 25+ reactions/upvotes (linked) |
| 5 | A segment on fire: evidence users would be angry if it vanished (retention, paying users, unprompted testimonials) |

Score the wedge the report names — the 6-month beachhead — not a segment
the product has already won. Cap: without evidence from that wedge ICP itself
(people other than the authors, in the segment the wedge targets), Wedge
sharpness is at most **3**. Usage by a different segment doesn't lift the
cap.

**Expansion path**

| Score | Anchor |
|---|---|
| 0 | Wedge is a dead end |
| 1 | Expansion requires building a different product |
| 2 | One adjacent segment or use case, not yet reachable from the wedge |
| 3 | Adjacent segments or use cases visible and reachable from the wedge |
| 4 | A clear sequence where each segment's win makes the next cheaper (mechanism named) |
| 5 | Natural land-and-expand (seat → team → platform), or a credible path to creating a new category |

**Delivery leverage** — the seller's economics: the owner's marginal cost to
serve one more user (not the user's own costs, such as tokens a user pays
for with their own model account). For open-core products, score the users
the wedge monetizes (e.g. the hosted tier's), not free self-hosters.

| Score | Anchor |
|---|---|
| 0 | Services economics: every customer needs human work |
| 1 | Heavy per-customer setup or support; margins capped by headcount |
| 2 | Mostly self-serve, but meaningful marginal cost per use (compute, LLM calls) or manual onboarding |
| 3 | Standard SaaS/library economics |
| 4 | Near-zero marginal cost AND one working self-distribution surface (shareable artifact, marketplace listing, registry) |
| 5 | Near-zero marginal cost AND the product demonstrably distributes itself (viral loop, marketplace pull, agent-installable) |

Each anchor's conditions must all hold: a product strong on one (it
distributes itself) and weak on the other (real per-use serving cost) scores
at the anchor its weaker condition meets.

Cap: scores 4–5 also need a way to capture value that **exists today** —
billing or pricing code, a pricing page, or a live paid tier (cite it).
Donations and sponsorships count only when the repo itself links them
(`FUNDING.yml` or the README). A paid layer the report only proposes
doesn't count: without existing capture,
Delivery leverage is at most **3**, because free distribution with nothing
to sell is reach, not leverage.

**Verdict bands** (state the band, not just the number — the strategy card
and report must use these exact labels):
- **20–25 — Venture-scale possible.** Say what must go right.
- **14–19 — Strong business possible.** Great outcome for a small team; venture scale needs a factor to change (name it).
- **8–13 — Niche tool / lifestyle business.** Honest and respectable; say it plainly.
- **0–7 — Feature, not a company.** Recommend: attach to a platform, open-source for reputation, or pivot the asset.

## Moat Score (/25) — what exists TODAY

Score the five rows 0–5 **as they exist today**, not as they could be. Early
repos usually score 0–4 total. Writing "Moat today: 2/25 — nothing
defensible yet" is a correct and useful output. The roadmap section is where
future moats live. Every row goes in the report's **Moat today** table.

| Row (Helmer's 7 Powers, software-adapted) | 0 | 1 | 3 | 5 |
|---|---|---|---|---|
| **Network economies** | None | Users interact, but value doesn't grow with count | Measurable value from other users within a segment | Each new user measurably improves the product for others |
| **Switching costs** | Leave in minutes | Some config or habit lost | Accumulated data or integrations take days to migrate | Leaving is genuinely painful (data, workflows, integrations) |
| **Scale economies / data** | None | Usage data collected but unused | Usage data demonstrably improves quality | Unit costs fall or quality rises with volume in a way rivals can't copy at small scale |
| **Brand / category ownership** | Unknown | Recognized in one niche community | Named in the category's comparisons and AI-assistant answers (cite a published comparison, roundup, or AI-answer page), or the reference rivals cite as prior art | The project name is the category's default answer |
| **Cornered resource / counter-positioning** (score the stronger of the two) | None | A soft exclusive, or a model incumbents could copy with some pain | An exclusive asset with usage rights, or a model whose copying would cost a named incumbent real revenue or channel conflict | Exclusive asset (dataset, distribution deal, community) or a model incumbents can't copy without self-harm |

Award 2 or 4 when the evidence clearly exceeds the anchor below but misses a
named condition of the anchor above (say which). Process power rarely
applies pre-scale; fold it into scale economies only with evidence (e.g. a
release cadence rivals demonstrably can't match).

**Moat bands** (the card and report use these exact labels):
- **0–4 — Nothing defensible yet**
- **5–9 — Early edge**
- **10–16 — Real moat forming**
- **17–25 — Durable moat**

## Gap severity

- **P0** — blocks the PRIMARY channel. The distribution plan cannot start.
  (No landing page when the channel is content/SEO; no telemetry when the plan
  requires measuring activation; no install path when the channel is a
  marketplace.)
- **P1** — blocks scale, not start. (Manual onboarding, no billing, no docs
  versioning, single-tenant architecture.)
- **P2** — polish. List max five; strategists who list twenty P2s are hiding
  from the P0s.

Every gap row: `gap | severity | channel it blocks | concrete fix | effort (S/M/L)`.

## Calibration rules (bind all output)

1. The market Size is `ESTIMATE $X–$Y` with the method (bottom-up
   arithmetic written as `a × b ÷ c = d`, or source linked). The headline
   range must be the result of a written calculation — when it adds
   sub-totals, write the sum too (`$14M–$407M + $10M–$72M = $24M–$479M`).
   Ranges run low × low to high × high; a divisor flips (smallest
   multipliers ÷ largest divisors gives the low end). `check_report.py`
   recomputes every calculation written with ×, x, ÷ or +, checks the
   headline matches one, checks the stated geometric midpoint, and checks
   Market headroom's score against the midpoint's band. Analyst
   figures are someone else's estimate: label them ESTIMATE too. When
   bottom-up and analyst numbers disagree by >3×, show both and say which you
   trust and why. Any other money figure in the report (a rival's revenue, a
   funding round) carries a source link or `unverified`.
2. Every verdict states its **crux**: the single assumption that, if wrong,
   flips the verdict. And its **falsifier**: the cheapest real-world test of
   that assumption (with rough cost/time), written so someone else could run
   it (exact query, exact metric). Check the measurement actually works
   before relying on it: GitHub code search doesn't index most small repos,
   so a fingerprint or mention count there reads zero regardless of use.
   Prefer signals the owner can read directly — GitHub traffic
   (`/repos/{owner}/{repo}/traffic/clones`, kept 14 days), registry download
   counts, a marketplace or directory usage dashboard, or product telemetry.
3. **Kill criteria** are dated and measurable: "If <metric> hasn't hit <level>
   by <date/effort>, stop or pivot." Never "if it doesn't work out."
4. **"What would have to be true"** (Roger Martin): for the top-band outcome,
   list 3–5 conditions as testable statements. Do not argue they're true —
   list what the bet requires.
5. Confidence labels: **High** = multiple independent sources or direct code
   evidence; **Medium** = one source or strong analogy; **Low** = reasoned
   guess. When the Bigness verdict's overall confidence is Low, the headline
   must read `<n>/25 — <band> (PROVISIONAL — Low confidence: <what's
   missing>)`. Individual Low-confidence claims never appear in the verdict
   box otherwise.
6. Every rival, number, and trend claim carries a source link or the word
   `unverified`. Memory is not a source.
7. If the user pushes back on a score, re-check evidence and restate with a
   probability — do not capitulate, do not flatter.
