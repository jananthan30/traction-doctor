# 02: Path to the next band

**What to build:** under the Verdict scores, every v0.4 report shows how many
points stand between it and the next Bigness and Moat band, the 2–5 moves
that would earn the next rubric points (each quoting the anchor, labeled
`outcome` or `rubric-only`), and the cap rules locking points today. The
skill tells the strategist how to build it, the red team attacks it, and the
checker verifies its arithmetic against the `dg` line.

**Blocked by:** 01.

**Status:** done

- [x] Rubric file explains the method (gap arithmetic, anchors, kinds, caps,
      no projected totals) without changing rubric version 2
- [x] Template and skill produce the block inside `## Verdict`
- [x] Checker: header arithmetic, top-band form, `Now → next` starts at the
      `dg` value and ends higher ≤ 5, kinds, ≥1 `outcome`, *Locked by caps*
- [x] The block can't spoof the Verdict, breakdown or Total checks (test)
- [x] Red team's seventh attack covers rubric-only moves dressed as outcomes
