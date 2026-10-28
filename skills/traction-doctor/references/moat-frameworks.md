# Moat Frameworks — building defensibility in software

Read after the distribution plan exists. Moats are downstream of distribution:
you earn the right to a moat by winning a wedge first.

## The honest starting point

Pre-traction software has almost no moat. Code is copyable in weeks (in the AI
era, days). Say this plainly in the report, then answer the only question that
matters: **what compounding loop can this specific product start that rivals
starting later cannot catch?**

## The 7 Powers, translated to software reality

(Hamilton Helmer, "7 Powers" — each power = a benefit to you + a barrier to them.
Understand all seven; score them on the five rows of the Moat rubric.)

1. **Network economies.** Product improves as users join.
   - Real versions: marketplaces (liquidity), collaboration tools (coworkers),
     protocols/formats (compatibility), community knowledge bases (answers).
   - Fake version: "we have a Discord." A community is a channel, not a moat,
     until member-created value retains other members.
   - Test: does user #1,001 get a measurably better product because of the
     first 1,000? What's the metric?

2. **Switching costs.** Leaving hurts.
   - Levers a repo can build deliberately: accumulated user data that grows in
     value (history, embeddings, configs), workflow integrations (CI, Slack,
     IDE), team habits (shared conventions), API surface others build on.
   - Ethical note & strategic note in one: easy import for rivals' data + easy
     export of yours signals confidence and is itself positioning; lock-in
     resentment is churn deferred, not prevented.

3. **Scale economies & data moats.** Costs fall or quality rises with volume.
   - The only data moat that counts: data that (a) accrues from usage
     automatically, (b) improves the product visibly, and (c) is not
     purchasable elsewhere. Telemetry nobody looks at is not a moat.
   - In AI products: proprietary evaluation sets and usage-derived preference
     data are the durable part; prompts and model choice are not.

4. **Brand / category ownership.** Being the default answer.
   - For devtools and OSS this is the most reachable early moat: the README
     everyone links, the benchmark everyone cites, the name that IS the
     category ("the X for Y").
   - In 2026 this includes being the answer AI assistants give — see
     `ai-era-distribution.md`. Citation share is measurable brand.

5. **Counter-positioning.** A business model the incumbent can't copy without
   self-harm.
   - Classic software forms: open-source vs proprietary incumbent; usage-based
     vs seat-based pricing; local-first vs cloud; free tier funded by a
     different revenue line. Name the incumbent and the exact reason copying
     hurts them (revenue cannibalization, channel conflict, cost structure).

6. **Cornered resource.** Exclusive access to something scarce.
   - Realistic early forms: a distribution deal, a dataset with usage rights,
     a maintainer seat in a critical ecosystem, a community you actually
     control.

7. **Process power.** Embedded organizational capability. Rarely relevant
   before scale; skip unless evidence exists (e.g. a shipping cadence rivals
   demonstrably can't match — cite the release history).

## Open-source-specific moat patterns

If the repo is OSS, evaluate explicitly:
- **License as strategy:** MIT/Apache maximizes adoption (distribution) but
  invites cloud-provider capture; AGPL/BSL/FSL trades adoption for
  monetization defense. State what the current license enables competitors to
  do, and whether that matches the business intent.
- **Open core:** the line between open and paid must follow a natural boundary
  (single-player open, team/compliance paid). Flag if the current feature set
  has no such line.
- **The real OSS moat is the community + velocity + brand bundle:** fork risk
  is theoretical when maintainers, roadmap trust, and the contributor pipeline
  all live in one place. Measure: external contributors per month, time-to-
  first-response on issues.

## Moat roadmap format (what the report must produce)

1. **Today:** the Moat today table — the five rubric rows in
   `scoring-rubrics.md`, each 0–5 with one line of evidence (most will be
   0 — fine). The seven powers above map onto those five rows:
   counter-positioning and cornered resource share one row (score the
   stronger), and process power folds into scale economies only with
   evidence. The total is out of 25, with its band label.
2. **Buildable:** the 1–2 powers this product can realistically develop, with
   the mechanism named.
3. **The compounding loop:** one diagram-in-text:
   `more X → better Y → more users → more X`. If you cannot draw this loop,
   there is no moat plan — say so.
4. **First signal:** the earliest measurable evidence the loop spins (e.g.
   "% of new users arriving via shared artifacts," "retention delta for users
   with >3 integrations"), and when to check it.
5. **Incumbent response:** what the most dangerous rival does when this works,
   and why the loop survives it (or doesn't — say which).
