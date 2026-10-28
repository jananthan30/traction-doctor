# AI-Era Distribution (2026) — the channels most strategy content misses

Traditional channel thinking predates two shifts: buyers now ask AI assistants
instead of searching, and AI agents now install tools themselves. Both create
land-grab channels where early movers compound.

## 1. GEO — Generative Engine Optimization

Buyers increasingly get one synthesized answer with citations, not ten blue
links. Being the cited answer is the new ranking.

Figures in this file are background, not citations: before putting any
number from here into a report, re-verify it by search and cite what you
find (this file was last checked 2026-09).

- A significant share of pages cited by AI assistants have little or no
  Google visibility — Ahrefs' study of the 1,000 most-cited pages in ChatGPT
  found ~28% had zero organic Google visibility
  ([Ahrefs, Oct 2025](https://x.com/thinking_slow/status/1983184678954627538)).
  GEO is a **separate, still-open game**, not SEO's afterthought.
- What gets cited: structured, extractable content (direct answers high on the
  page, tables, steps), entity clarity (the product is a well-defined "thing"
  with consistent naming across sources), third-party corroboration
  (comparisons, reviews, forum mentions — assistants triangulate).

**Actions the report can prescribe:**
- Publish the comparison pages buyers ask assistants for ("X vs Y", "best tool
  for Z") — honest ones; assistants cross-check.
- `llms.txt` at the docs root; docs in clean markdown; quickstarts that an
  assistant can quote verbatim.
- Seed third-party surfaces assistants trust: GitHub README, package registry
  descriptions, Stack Overflow answers, Wikipedia-adjacent entity presence.
- Measure: ask the major assistants the category question monthly; track
  citation share like rankings ("share of answer").

## 2. Agent-installability — distribution TO the AI agents themselves

New in this era: the "user" acquiring the tool is often an AI agent acting for
a human. A repo is agent-distributable when an agent can discover, evaluate,
and install it without a human clicking anything.

**Surfaces to claim (each is a listing = a funnel):**
- **MCP server** — makes the product callable by Claude, ChatGPT, and IDE
  agents; listed in MCP registries.
- **Claude Code plugin / Codex skill** (Agent Skills standard) — installable
  into the developer's terminal loop. One repo can serve both: Codex installs
  plugins from a Claude-format `.claude-plugin/marketplace.json`. For Claude
  plugins, Anthropic's directory adds reach (claude.ai and Cowork) and is the
  only source of install and usage numbers — see `channel-playbooks.md`.
- **ChatGPT apps / GPT store, Claude connectors** where user-facing.
- Classic registries agents already search: npm, PyPI, Homebrew, VS Code
  marketplace.

**Checks for the gap analysis:** machine-readable metadata (clear README with
install one-liner near the top, typed APIs, versioned changelog), permissive
enough license for the surface, and a listing wherever the ecosystem's agents
look. A devtool with no MCP/plugin surface in 2026 is leaving a channel empty.

## 3. Community & build-in-public, updated

- Cold outbound is degrading under AI-generated spam saturation; warm surfaces
  (communities, mutuals, in-person) rise in relative value. Weight rubric
  scores accordingly for outbound-primary plans.
- Build-in-public works when artifacts are the content: benchmarks, changelogs
  with opinions, postmortems. It fails as diary. Prescribe artifact cadence,
  not "post more."
- Niche communities (specific Discords, subreddits, Slacks) are
  higher-conversion than general platforms; the report should name exact
  communities, not "engage on social media."

## 4. What did NOT change

Positioning still decides whether any channel works. Retention still beats
acquisition (leaky bucket law). One primary channel still beats four half-run
channels. Word-of-mouth from a product that wows is still the only channel
that's free. AI-era channels amplify a sharp wedge; they cannot rescue a
blurry one.
