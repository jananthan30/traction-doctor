# Channel Playbooks — channel–product fit

The core law: **products don't pick channels; product properties do.** Price,
buyer, time-to-value, and virality coefficient determine which channels can
physically work. Rank channels with the rubric, then commit to ONE primary.

## Channel–product fit rubric

Score each candidate channel 0–5 on four axes; sum /20:

1. **Reach** — are there enough ICPs actually present in this channel?
2. **Economics** — CAC this channel implies vs. plausible revenue per user
   (rule of thumb: self-serve <$100/yr products cannot afford outbound or paid;
   $10k+/yr products cannot rely on virality alone).
3. **Repo evidence** — does the codebase already support it? (A CLI with great
   docs supports SEO/GEO; a product with no landing page supports nothing yet.)
4. **Founder fit** — can the actual team execute it? (No audience → cold-start
   content is slow; strong engineering → build-the-tool-that-markets-the-tool.)

Recommend: 1 primary (where 80% of effort goes), 1 secondary (compounding,
low-maintenance), and name 2–3 channels explicitly deferred with the reason.
Spreading across four channels pre-traction is the most common distribution
failure — the report must forbid it.

## Playbooks by product type

### Developer tools / CLIs / libraries / plugins
- **Default primary:** marketplace + registry presence (npm, PyPI, VS Code,
  JetBrains, Claude Code / ChatGPT plugin stores, Homebrew) — the install
  command IS the funnel. Optimize the listing like a landing page: first
  screenshot, first 10 words, keywords.
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
