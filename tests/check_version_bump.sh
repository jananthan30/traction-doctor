#!/usr/bin/env bash
# Fail when skills/ or agents/ changed since BASE but plugin.json's version
# didn't. Installs are pinned to the version string, so an unbumped change
# never reaches existing users.
#
# Usage: tests/check_version_bump.sh <base-ref>
set -euo pipefail

base="${1:?usage: tests/check_version_bump.sh <base-ref>}"
if ! git cat-file -e "${base}^{commit}" 2>/dev/null; then
  echo "base ${base} not available; skipping version-bump check"
  exit 0
fi

changed="$(git diff --name-only "${base}" HEAD -- skills agents)"
if [[ -z "${changed}" ]]; then
  echo "no changes under skills/ or agents/"
  exit 0
fi

version_at() {
  git show "$1:.claude-plugin/plugin.json" 2>/dev/null \
    | python3 -c 'import json,sys; print(json.load(sys.stdin)["version"])'
}
old="$(version_at "${base}" || echo none)"
new="$(version_at HEAD)"
if [[ "${old}" == "${new}" ]]; then
  echo "error: skills/ or agents/ changed but plugin.json version is still ${new}:" >&2
  while IFS= read -r path; do echo "  ${path}" >&2; done <<< "${changed}"
  echo "bump the version in .claude-plugin/plugin.json, then everywhere it is pinned:" >&2
  echo "  skills/distribution-god/SKILL.md, CHANGELOG.md, llms.txt," >&2
  echo "  skills/distribution-god/references/scoring-rubrics.md, scripts/strategy_card.py EXAMPLE" >&2
  echo "  (python3 -m unittest discover -s tests fails until they all agree)" >&2
  exit 1
fi
echo "version bumped ${old} -> ${new}"
