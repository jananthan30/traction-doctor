# Scoring Rubrics & Calibration Rules

These rubrics exist to prevent the two failure modes of AI strategy output:
hype ("this could be huge!") and hedge ("it depends"). Score honestly, show the
arithmetic, name the falsifier.

## Bigness Score (/25) — "how big can this get?"

Score each dimension 0–5. Sum. Show each sub-score with one line of evidence.

| Dimension | 0 | 3 | 5 |
|---|---|---|---|
| **Market headroom** | Hobby niche; <$100M plausible spend | $1B± category or credible path to one | Multi-billion category, or creates its own |
| **Why-now force** | None; could have existed in 2015 | One real tailwind (platform shift, cost collapse, behavior change) | Multiple compounding tailwinds; window measured in quarters |
| **Wedge sharpness** | "For everyone" — no specific desperate user | Identifiable ICP with a painful, frequent job | A user segment on fire; they'd be angry if the product vanished |
| **Expansion path** | Wedge is a dead end | Adjacent segments or use cases visible | Natural land-and-expand: each win creates the next (seat → team → platform) |
| **Delivery leverage** | High-touch services economics | Standard SaaS/library economics | Near-zero marginal cost AND the product distributes itself (viral loop, marketplace, agent-installable) |

**Verdict bands** (state the band, not just the number):
- **20–25 — Venture-scale possible.** Say what must go right.
- **14–19 — Strong business possible.** Great outcome for a small team; venture scale needs a factor to change (name it).
- **8–13 — Niche tool / lifestyle business.** Honest and respectable; say it plainly.
- **0–7 — Feature, not a company.** Recommend: attach to a platform, open-source for reputation, or pivot the asset.

## Moat Score (/25) — what exists TODAY

Score each 0–5 **as it exists today**, not as it could be. Early repos usually
score 0–4 total. Writing "Moat today: 2/25 — nothing defensible yet" is a
correct and useful output. The roadmap section is where future moats live.

| Power (Helmer's 7, software-adapted) | What 5 looks like |
|---|---|
| **Network economies** | Each new user measurably improves the product for others |
| **Switching costs** | Data, workflows, or integrations make leaving genuinely painful |
| **Scale economies / data** | Unit costs fall or quality rises with volume in a way rivals can't copy at small scale |
| **Brand / category ownership** | The project name is the category's default answer |
| **Cornered resource / counter-positioning** | Exclusive asset (dataset, distribution deal, community) or a model incumbents can't copy without self-harm |

(Process power and interconnected scale rarely apply pre-scale; fold them into
scale economies if relevant.)

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

1. Every market number is `ESTIMATE: $X–$Y` with the method (bottom-up
   arithmetic shown, or source linked). When bottom-up and analyst numbers
   disagree by >3×, show both and say which you trust and why.
2. Every verdict states its **crux**: the single assumption that, if wrong,
   flips the verdict. And its **falsifier**: the cheapest real-world test of
   that assumption (with rough cost/time).
3. **Kill criteria** are dated and measurable: "If <metric> hasn't hit <level>
   by <date/effort>, stop or pivot." Never "if it doesn't work out."
4. **"What would have to be true"** (Roger Martin): for the top-band outcome,
   list 3–5 conditions as testable statements. Do not argue they're true —
   list what the bet requires.
5. Confidence labels: **High** = multiple independent sources or direct code
   evidence; **Medium** = one source or strong analogy; **Low** = reasoned
   guess. Never present Low-confidence claims in verdict headlines.
6. If the user pushes back on a score, re-check evidence and restate with a
   probability — do not capitulate, do not flatter.
