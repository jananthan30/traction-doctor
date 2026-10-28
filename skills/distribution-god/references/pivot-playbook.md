# Pivot Playbook — what to do when the verdict or the moat says no

Read in Phase 4, after the moat audit and the Bigness verdict. A pivot is a
change of strategy that keeps what has already been built and learned and
tests one new core hypothesis — Eric Ries's framing in *The Lean Startup*
(2011, the "Pivot (or Persevere)" chapter;
[book](https://en.wikipedia.org/wiki/The_Lean_Startup)). Pivots belong next
to the kill criteria: each kill criterion says when to stop the current
path, and a pivot says what to run instead.

## Pivot, persevere, or stop

- The kill criteria decide, dated in advance — never mood. Every pivot
  answers one kill criterion: "if X fails by D, run Pivot A's test".
- **Persevere** while the crux is unresolved and the primary channel hasn't
  had its 90 days.
- **Pivot** when a kill criterion fires and the asset inventory still holds
  something worth keeping.
- **Stop** when nothing in the inventory is worth more than the time it
  costs — say so plainly; open-sourcing for reputation is an honest ending.
- A low Moat today is not by itself a reason to pivot: early products almost
  never have one (`moat-frameworks.md`). It is a reason to prefer, among
  paths that could work, one whose loop compounds.

## Asset inventory — what a pivot keeps

Before proposing pivots, list what the repo already holds, each with a path
or link:

- **Code that works**, especially the hard part (the parser, the engine,
  the integration nobody else has).
- **Formats or data** others read or depend on.
- **Distribution already claimed:** a registry or marketplace listing,
  stars, an audience, a community.
- **Expertise the code proves** (a domain, a platform, a performance trick).
- **Anything users already rely on** — the feature they'd miss.

A pivot keeps at least one named asset. One that keeps nothing is a
restart: say so instead of calling it a pivot.

## The ten pivot types

Use these names exactly in the card header (`*<type> pivot:*`).

| Type | The move | Moat power it can unlock |
|---|---|---|
| zoom-in | One feature becomes the whole product | Brand / category ownership — own a narrow category outright |
| zoom-out | The product becomes one feature of a larger product, often by attaching to a platform | Switching costs — embedded in a bigger workflow |
| customer-segment | Same product, a different buyer who has the problem worse | Counter-positioning or switching costs — a segment incumbents serve badly |
| customer-need | Same buyer, a different and more painful problem the assets already solve | Depends on the new need — name it |
| platform | An application becomes a platform others build on, or the reverse | Network economies |
| business-architecture | High margin and low volume (sales-led) ↔ low margin and high volume (self-serve) | Scale economies |
| value-capture | A different way to make money: sponsorship → hosted tier → services → marketplace fee | Scale economies / data — a hosted tier sees usage |
| engine-of-growth | Switch the growth engine: viral, sticky (retention), or paid | Network economies (viral) or switching costs (sticky) |
| channel | Same product, a different distribution channel | Counter-positioning — a channel the incumbent's model can't use |
| technology | Same solution, a different technology that is cheaper or better | Scale economies |

**Illustrations** — background that the moves are real, not evidence for any
report (checked 2026-10-28):

- *zoom-in:* Instagram began as Burbn, a check-in app; its founders
  refocused it on photo sharing, already popular with its users
  ([Wikipedia](https://en.wikipedia.org/wiki/Instagram)).
- *customer-need:* Slack began as an internal communication tool at Tiny
  Speck, a studio building the game Glitch
  ([Wikipedia](https://en.wikipedia.org/wiki/Slack_(software))).
- *platform:* Shopify's founders built the Snowdevil snowboard store, then
  launched its software as a platform
  ([Wikipedia](https://en.wikipedia.org/wiki/Shopify)).

A report's **Precedent** should come from the product's own category — the
rival field's cautionary tales and pivots are the best source. A famous
consumer pivot shows the move exists; it doesn't show it transfers.

## Pivots for a moat-poor product

When Moat today is *Nothing defensible yet*, "build a moat" usually means
"move to where one can form". Prefer pivots whose loop you can draw:

- **Own a narrow category** (zoom-in): the one job you do best, named so the
  category's comparisons and AI answers list you.
- **Embed in a workflow** (zoom-out, platform): become the step inside a
  tool people already live in, where leaving means rebuilding the step.
- **Serve the segment incumbents can't** (customer-segment, channel): a
  model the incumbent would hurt itself copying.
- **See usage** (value-capture): a hosted tier whose usage data improves the
  product — only if the data really does (`moat-frameworks.md`, data moats).

## Card format (what the report must produce)

In section 9, after the kill criteria, under a `**Pivot options**` line:

```markdown
**A. <short name>** — *<type> pivot:* <the move in one line>
- **Keeps:** <assets from the inventory, with paths or links>
- **Changes:** <what's different: the buyer, the job, the channel, or how it makes money>
- **Unlocks:** <the Moat row it builds toward> — <the loop that builds it>
- **Projected (ESTIMATE):** <which sub-scores would move, from → to, per which anchor, if the test passes>
- **Precedent:** <a product that made the same move, linked, and what happened — or `unverified`>
- **Test (≤5 days, ~$0):** <what to do>. Pass: <the result that counts as a pass>
- **Trigger:** <the kill criterion or checkpoint result that starts it>
```

Then one line: `**Persevere if:** <the signal that says stay the course>`.

Rules (`check_report.py` enforces them):

- 1–3 cards, lettered A, B, C. At least 2 when Moat today is *Nothing
  defensible yet* or Bigness is 13 or less. More than 3 is a menu, not a
  plan.
- One type per card, from the table above, by its exact name.
- **Keeps** names at least one inventory asset.
- **Unlocks** names the Moat row and the mechanism.
- **Projected** is labeled ESTIMATE and names the sub-scores and anchors. A
  projected band may appear here, since it compares ceilings, but never in
  the `dg` line, on the card, or in the Path to the next band block.
- **Precedent** carries a link or `unverified`.
- **Test** fits five working days at about $0 and states `Pass:`.
- At least one kill criterion names each pivot ("run Pivot A's test").
