---
name: gap-scan
description: Fast, local-only distribution gap scan of the current repository — no web research. Checks the repo's conversion and distribution surface (README, install path, docs, license, telemetry, marketplace/agent-installability presence) and returns a prioritized gap table. Use for quick iteration between full distribution-god runs, or when the user asks "what's missing / what blocks growth" and wants an answer in minutes.
---

# Gap Scan

A 3–5 minute local audit of the repo's distribution surface. No web access, no
market research, no subagents — just the repo as evidence. For the full
strategist run (market, rivals, moat, 90-day plan), use `distribution-god`.

## Checklist — inspect each surface, cite file paths

**Conversion surface (can a stranger become a user in 15 minutes?)**
1. README above-the-fold: what-it-is in one line, demo (GIF/screenshot), and a
   copy-paste install command — all visible without scrolling?
2. Time-to-value: from install to the core "wow" moment — how many steps? What
   breaks on a clean machine (missing env vars, credentials, undocumented
   deps)?
3. Docs: quickstart exists? Copy-paste blocks actually runnable?
4. Landing page / homepage link, social preview image, GitHub description +
   topics set?

**Distribution surface (can the product be found and installed where its
users look?)**
5. Published to the ecosystem's registries (npm/PyPI/crates/Homebrew/Docker
   Hub) with a listing written like a landing page?
6. Agent-installability: MCP server, Claude Code plugin, or Codex skill
   surface where applicable; `llms.txt`; machine-readable install metadata?
7. Shareable artifacts: does anything a user produces carry the product's
   fingerprint and a path back (links, badges, "made with")?

**Business readiness (strategy signals in code)**
8. License present and consistent with apparent business intent? (Flag: no
   license, or a license that contradicts monetization signals like billing
   code.)
9. Telemetry/analytics: could activation or retention be measured today at
   all? (Privacy-respecting is fine; absent is a gap.)
10. Self-serve loop where applicable: signup → value without human contact?
    Pricing visible anywhere?

**Trust surface**
11. CHANGELOG / releases / versioning discipline; CI badge that's green;
    security policy; responsive issue history (spot-check timestamps).

## Output — in chat, no file

A single table sorted by severity:

| # | Gap | Severity | Blocks | Fix | Effort |
|---|---|---|---|---|---|

- Severity: **P0** = blocks the most plausible primary channel entirely;
  **P1** = blocks scale; **P2** = polish (max five P2s).
- "Blocks": name the specific channel (e.g. "npm discovery", "GEO citations",
  "Show HN launch", "self-serve conversion") — never "growth" generically.
- Fix: concrete and small ("add 30-sec GIF of the core loop to README top",
  not "improve documentation").
- End with **Top 3 this week** — the highest severity-to-effort ratio items.

Guardrail: this scan judges the surface, not the strategy. If the product's
wedge itself looks unclear from the repo, say so in one line and recommend the
full `distribution-god` run rather than guessing.
