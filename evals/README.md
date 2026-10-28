# Evals

Suites for `claude plugin eval` (see the
[plugin eval docs](https://code.claude.com/docs/en/plugin-evals)). Each case
seeds a tiny under-distributed CLI repo with `fixture.sh` (the close-gaps cases
also seed a strategy report for it), runs a user-phrased prompt, and grades the
output.

| Case | What it proves |
|---|---|
| `gap-scan-tiny-cli` | `/gap-scan` triggers from plain phrasing, produces the gap table with an assumed primary channel, finds the real gaps (no LICENSE, no install command), and writes no files |
| `web-full-run` | With web tools the full run researches (3+ searches), records `"web": true`, sources every rival, labels the Size `ESTIMATE`, writes the path to the next band and pivot options, writes a private `FIRST-CUSTOMERS.md` with real openings (or says only N were found) and no email addresses, and gets `check_report.py` to print ok — the path the market-math, source and people-file checks guard |
| `offline-full-run` | Without web tools the full run still writes a complete `STRATEGY.md` + card with no unfilled slots and five actions, marks sections 2–3 `NOT RESEARCHED`, records `"web": false`, uses the PROVISIONAL headline, still writes the path and pivots, writes a `FIRST-CUSTOMERS.md` whose Openings say `NOT RESEARCHED` and that links no individual post, and gets `check_report.py` to print ok |
| `close-gaps-web` | With web tools, `/close-gaps` researches (3+ searches), cites at least one paper link, puts the report's known-fix P0 (the missing LICENSE) under *Just do it*, keeps its top ideas specific (LLM-judged), gets `check_ideas.py` to print ok, and creates or edits no other file |
| `close-gaps-offline` | Without web tools, `/close-gaps` still writes a `CLOSE-GAPS.md` that passes `check_ideas.py`, drawn from the plugin's playbooks: `NOT RESEARCHED` markers, `"web": false`, no links, and the known fix under *Just do it* |
| `close-gaps-no-report` | With no `STRATEGY.md`, `/close-gaps` stops, points to `/traction-doctor`, and writes nothing |

Run from the repo root (the fixture scripts are ours, so `--scaffold` is safe):

```bash
claude plugin eval . --trust-plugin --scaffold --allow-tools Bash Write Edit WebSearch WebFetch --runs 1
```

Add `--ablation none` to skip the no-plugin baseline arm while iterating, and
`--tag` to pick cases (`--tag web` is the expensive one).
CI runs the same command on demand (`.github/workflows/evals.yml`), adding
`--threshold 0.8 --no-publish` and an HTML report artifact. Granting Bash
needs a sandbox backend: on Linux, `bubblewrap` and `socat`.
