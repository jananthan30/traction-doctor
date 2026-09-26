# Evals

Suites for `claude plugin eval` (see the
[plugin eval docs](https://code.claude.com/docs/en/plugin-evals)). Each case
seeds a tiny under-distributed CLI repo with `fixture.sh`, runs a user-phrased
prompt, and grades the output.

| Case | What it proves |
|---|---|
| `gap-scan-tiny-cli` | `/gap-scan` triggers from plain phrasing, produces the gap table with an assumed primary channel, finds the real gaps (no LICENSE, no install command), and writes no files |
| `web-full-run` | With web tools the full run researches (3+ searches), records `"web": true`, sources every rival, labels the Size `ESTIMATE`, and gets `check_report.py` to print ok — the path the market-math and source checks guard |
| `offline-full-run` | Without web tools the full run still writes a complete `STRATEGY.md` + card with no unfilled slots and five actions, marks sections 2–3 `NOT RESEARCHED`, records `"web": false`, uses the PROVISIONAL headline, and gets `check_report.py` to print ok |

Run from the repo root (the fixture scripts are ours, so `--scaffold` is safe):

```bash
claude plugin eval . --trust-plugin --scaffold --allow-tools Bash Write Edit WebSearch WebFetch --runs 1
```

Add `--ablation none` to skip the no-plugin baseline arm while iterating, and
`--tag` to pick cases (`--tag web` is the expensive one).
CI runs the same command on demand (`.github/workflows/evals.yml`), adding
`--threshold 0.8 --no-publish` and an HTML report artifact. Granting Bash
needs a sandbox backend: on Linux, `bubblewrap` and `socat`.
