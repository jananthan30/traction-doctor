#!/usr/bin/env bash
# Every check CI runs. Usage: tests/run.sh
# Optional tools (shellcheck, xmllint, claude) are used when installed; CI
# installs all of them, so a skip here is a failure there.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}"
SCRIPTS="skills/distribution-god/scripts"
status=0
step() { printf '\n== %s\n' "$1"; }
fail() { echo "FAIL: $1" >&2; status=1; }

step "unit tests"
python3 -m unittest discover -s tests || fail "unit tests"

step "reports pass the report checker"
reports=(STRATEGY.md tests/fixtures/sample-report/STRATEGY.md)
while IFS= read -r f; do reports+=("$f"); done < <(find examples -name STRATEGY.md 2>/dev/null | sort)
python3 "${SCRIPTS}/check_report.py" "${reports[@]}" || fail "report checker"

step "strategy cards parse"
while IFS= read -r svg; do
  python3 "${SCRIPTS}/strategy_card.py" check "${svg}" || fail "${svg}"
  if command -v xmllint >/dev/null; then xmllint --noout "${svg}" || fail "xmllint ${svg}"; fi
done < <(find assets examples tests/fixtures -name 'strategy-card*.svg' 2>/dev/null | sort)

step "version bump (skills/ or agents/ changed since origin/main)"
if base="$(git merge-base HEAD origin/main 2>/dev/null)"; then
  tests/check_version_bump.sh "${base}" || fail "version bump"
  if [[ -n "$(git status --porcelain -- skills agents)" ]]; then
    echo "note: uncommitted changes under skills/ or agents/ are checked once committed"
  fi
else
  echo "skipped: no origin/main to compare against"
fi

step "shellcheck"
if command -v shellcheck >/dev/null; then
  shellcheck install-codex.sh tests/run.sh tests/check_version_bump.sh || fail "shellcheck"
else
  echo "skipped: shellcheck not installed"
fi

step "claude plugin validate --strict"
if command -v claude >/dev/null; then
  for target in . .claude-plugin/plugin.json agents skills; do
    claude plugin validate --strict "${target}" || fail "validate ${target}"
  done
else
  echo "skipped: claude CLI not installed"
fi

if [[ ${status} -eq 0 ]]; then echo; echo "all checks passed"; fi
exit ${status}
