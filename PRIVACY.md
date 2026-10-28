# Privacy policy — distribution-god

Effective 2026-10-28. distribution-god is an open-source plugin (skills and
agents) for Claude Code and OpenAI Codex. It runs inside your own AI coding
client, with that client's tools and permission settings.

## What the author collects

Nothing. The plugin has no server, no telemetry and no analytics, and it
sends nothing to its author.

## What leaves your machine

Only these requests, made by your client's own tools:

- **Web searches and page fetches**, made by your client's WebSearch and
  WebFetch tools. Queries are built from a one-line description of your
  product, its category, its rivals' names, the pain it solves and, for
  `/close-gaps`, the weakness being researched.
- **Keyless public APIs**, queried with the same kind of phrases. The
  customer scout uses GitHub issue search (`api.github.com`), Hacker News
  search (`hn.algolia.com`) and Stack Exchange (`api.stackexchange.com`).
  `/close-gaps` uses arXiv (`export.arxiv.org`), OpenAlex
  (`api.openalex.org`) and Hugging Face Papers (`huggingface.co`).
- **Your repository's GitHub details**, such as its description, topics and
  latest release, read with your own `gh` CLI (`gh repo view`) when it is
  installed.

The searches and API queries happen during a full run, during `/close-gaps`,
or when you call one of its research agents directly (for example
`@agent-distribution-god:rival-scout`). `/gap-scan` does no web research: at
most it reads your repository's GitHub details with `gh`.

Your code is read by your AI client, and your model provider processes it
under your agreement with them, as with any other prompt.

## What it stores

Only files in your repository, plus one temporary file:

- `STRATEGY.md`, the strategy card (an SVG in `assets/`, and a PNG if you ask
  for one), `CLOSE-GAPS.md` and `FIRST-CUSTOMERS.md`, with earlier runs
  archived under `docs/strategy-history/` and `FIRST-CUSTOMERS.previous.md`
- the card's data, written to your system's temp folder (`/tmp/dg-card.json`)
  while the card is drawn

These stay until you delete them. The plugin never commits or uploads them.

## Other people's data

`FIRST-CUSTOMERS.md` lists recent public posts by people who asked for what
you built: a link to each post, the date it was posted and fetched, a quote
of at most 15 words and why it fits. The plugin never records email
addresses, phone numbers or other contact details, never looks anyone up
across sites and never contacts anyone. The message drafts are yours to
send or not, one per person, and each says that you built the product.
Keep the file out of git (`FIRST-CUSTOMERS*.md` in `.gitignore`), and delete
it when you're done.

## This repository's CI

The workflows under `.github/` run only on GitHub, for this repository. They
test the plugin and log this repository's own traffic counts with a token
the maintainer stores as a repository secret. Installing or running the
plugin never runs them.

## Children

The plugin is not intended for people under 18.

## Contact and changes

Questions: open an issue at
<https://github.com/jananthan30/distribution-god/issues>. Changes to this
policy are recorded in this file's git history.
