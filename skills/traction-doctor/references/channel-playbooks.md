# Channel Playbooks — channel–product fit

The core law: **products don't pick channels; product properties do.** Price,
buyer, time-to-value, and virality coefficient determine which channels can
physically work. Rank channels with the rubric, then commit to ONE primary.

## Channel–product fit rubric

Score each candidate channel 0–5 on four axes; sum /20:

1. **Reach** — are there enough of the wedge's ICPs actually present in
   this channel, and not yet reached? Score every channel for the wedge
   buyer. For a channel the product has already won (it's in every package
   manager, it tops the marketplace), score all four axes on what more
   effort there would return — a `claimed` row is kept for the record, not
   ranked against the primary.
2. **Economics** — CAC this channel implies vs. plausible revenue per user
   (rule of thumb: self-serve <$100/yr products cannot afford outbound or paid;
   $10k+/yr products cannot rely on virality alone).
3. **Repo evidence** — does the codebase already support it? (A CLI with great
   docs supports SEO/GEO; a product with no landing page supports nothing yet.)
4. **Founder fit** — can the actual team execute it? (No audience → cold-start
   content is slow; strong engineering → build-the-tool-that-markets-the-tool.)
   Base it on what the user has said about the team plus repo evidence
   (contributors, linked profiles). When analyzing someone else's repo,
   infer it from public evidence (maintainer count, their audience, launch
   history) and say so. If nothing is known, score 3 for every channel and
   say so — never invent a founder profile.

Recommend: 1 primary (where 80% of effort goes), 1 secondary (compounding,
low-maintenance), and name 2–3 channels explicitly deferred with the reason.
The Call column uses exactly: `PRIMARY`, `secondary`, `defer`, `claimed`
(already won — keep it maintained, no new effort), or `ignition` (a one-off
launch event, not an ongoing channel). **Ties:** pick the channel whose
results most directly test the crux, and say that's why.
Spreading across four channels pre-traction is the most common distribution
failure — the report must forbid it.

## Playbooks by product type

### Developer tools / CLIs / libraries / plugins
- **Default primary:** marketplace + registry presence (npm, PyPI, VS Code,
  JetBrains, Homebrew, MCP registries, agent plugin marketplaces) — the
  install command IS the funnel. Optimize the listing like a landing page:
  first screenshot, first 10 words, keywords.
- **Claude Code plugins specifically:** a self-hosted marketplace gives the
  author no usage data at all — Claude Code reports nothing back
  ([docs](https://code.claude.com/docs/en/plugins/measure)). Anthropic's
  directory (submitted from claude.ai/directory/manage; needs a paid
  claude.ai plan and passes a review) reaches claude.ai, Cowork, and Claude
  Code with one listing ([docs](https://code.claude.com/docs/en/plugins/publish))
  and comes with install and usage tracking
  ([Track published plugin usage](https://claude.com/docs/connectors/building/after-publishing#track-published-plugin-usage)). Treat it as
  both a channel and the measurement surface.
- **Secondary:** technical content with proof (benchmarks, postmortems,
  "how X works internally") targeted at high-intent comparison and
  how-to queries; GitHub SEO (topics, description, social preview, README
  above-the-fold demo GIF).
- **Ignition:** launches are events not strategies — Hacker News (Show HN),
  Product Hunt, relevant subreddits (r/programming, r/LocalLLaMA, niche subs),
  lobste.rs. One launch per meaningful release; a launch without a
  wow-in-90-seconds demo is wasted.
- **Community:** answer questions where the pain is voiced (Stack Overflow,
  Discord servers of the ecosystem you ride, GitHub issues of adjacent
  projects — helpfully, never spammy).
- **The riding-an-ecosystem rule:** a tool that extends platform X gets
  distribution from X's growth, X's marketplace, X's community. State which
  ecosystem this repo rides and whether it has claimed its surface there.

### B2B SaaS (team buyer, $1k–50k/yr)
- **Primary candidates:** founder-led outbound to a named list of 100 ICP
  accounts (works from day 0, teaches positioning); or content/SEO+GEO if the
  category has search volume; or community-led if buyers congregate.
- **Product-led motion requires:** self-serve signup, time-to-value under
  15 minutes, a free tier or trial that demos the core loop — check the repo
  for all three; each missing one is a P0/P1 gap.
- **The land-and-expand check:** does one team's usage naturally expose
  adjacent teams? (Shared links, invites, cross-team artifacts.) If not, and
  ACV is low, the math rarely works — flag it.

### Consumer / prosumer apps
- **Primary candidates:** virality built into the artifact (outputs users
  share with the product's fingerprint on them), short-form video
  (TikTok/Reels/Shorts demos), app-store ASO.
- **The k-factor question:** what does a user's output look like to a
  non-user, and does it carry an install path? If outputs are private,
  consumer virality is unavailable — plan for paid or content instead and
  check the margin supports it.

### APIs / infrastructure
- **Primary:** docs-as-product (the docs ARE the marketing: interactive
  playground, copy-paste quickstarts per language), GEO (developers ask AI
  assistants "how do I do X" — be the cited answer), integration marketplaces
  of the platforms above you.
- **Secondary:** champion motion — the IC who discovers you must be armed to
  sell internally (security page, pricing clarity, comparison pages).

### Marketplaces / network products
- Solve cold-start explicitly (Chen's "atomic network"): name the smallest
  self-sustaining network (one city, one game, one framework), subsidize the
  hard side manually, do things that don't scale. A marketplace strategy
  without a named atomic network is a P0 gap.

## Sequencing: 10 → 100 → 1,000

For a product that already has distribution, count the wedge's units
instead — the first 10 / 100 / 1,000 paying teams, or owners of the new
segment — not total users.

- **First 10 users:** hand-to-hand. DMs to people you can name, communities
  you're already in, personal network. Goal is not revenue — it's watching
  10 real users hit the core loop and saying "I'd be upset if this vanished."
- **First 100:** one ignition event (launch) + the primary channel's unscalable
  version (manual onboarding calls, concierge setup). Instrument activation
  and retention NOW — flag missing telemetry as a gap before this stage.
- **First 1,000:** the primary channel, systematized. Weekly cadence of the
  channel's atomic unit (post, listing update, outbound batch). Kill or double
  down per the kill criteria — not per mood.

## 90-day plan format (what the report must produce)

- Weeks 1–4 in weekly grain: concrete actions with owners ("you") and outputs.
- Months 2–3 in monthly grain: the channel cadence + the measurement loop.
- Each line: action → channel it serves → metric it moves.
- End with the week-12 checkpoint: the numbers that decide double-down vs
  pivot (tie to kill criteria from the rubric).
