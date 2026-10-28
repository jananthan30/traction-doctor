# Example reports

Full v0.2.0 runs (the plugin was called distribution-god then) on public
repositories, each unedited and stamped with the commit analyzed, the run
date, the model, and the mode.
They are automated analyses from public information only — not affiliated
with or endorsed by the projects. Every report passes
`skills/traction-doctor/scripts/check_report.py` (CI re-checks them).

| Report | Repository | Bigness | Moat today |
|---|---|---|---|
| [context7](context7/STRATEGY.md) | [upstash/context7](https://github.com/upstash/context7) @ `e275a84` — MCP server serving library docs to coding agents | 15/25 — Strong business possible (confidence: Medium) | 12/25 — Real moat forming |
| [hyperfine](hyperfine/STRATEGY.md) | [sharkdp/hyperfine](https://github.com/sharkdp/hyperfine) @ `f12f3d9` — Rust CLI benchmarking tool | 11/25 — Niche tool / lifestyle business (confidence: Medium) | 5/25 — Early edge |
| [umami](umami/STRATEGY.md) | [umami-software/umami](https://github.com/umami-software/umami) @ `ec0ff50` — open-source web analytics with a hosted cloud (SaaS) | 14/25 — Strong business possible (confidence: Medium) | 8/25 — Early edge |

Three contrasting shapes: a free, single-maintainer CLI with nothing to sell
yet; an open-source product with a paid cloud; and an agent-facing service
that already has distribution. Compare how the rubric's value-capture and
wedge-evidence caps play out across them.
