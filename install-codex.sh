#!/usr/bin/env bash
# Install distribution-god skills into OpenAI Codex (Agent Skills standard).
#
# Codex discovers skills in ~/.agents/skills (user-level) or .agents/skills
# (repo-level). This script symlinks both skills user-level so every Codex
# session can invoke them with $distribution-god / $gap-scan.
#
# Usage:  ./install-codex.sh          # symlink (updates with this repo)
#         ./install-codex.sh --copy   # copy instead (frozen snapshot)
#         ./install-codex.sh --uninstall
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="${HOME}/.agents/skills"
SKILLS=(distribution-god gap-scan)

if [[ "${1:-}" == "--uninstall" ]]; then
  for skill in "${SKILLS[@]}"; do
    rm -rf "${TARGET_DIR:?}/${skill}"
    echo "removed ${TARGET_DIR}/${skill}"
  done
  exit 0
fi

mkdir -p "${TARGET_DIR}"

for skill in "${SKILLS[@]}"; do
  src="${REPO_DIR}/skills/${skill}"
  dst="${TARGET_DIR}/${skill}"
  [[ -d "${src}" ]] || { echo "error: ${src} not found" >&2; exit 1; }
  rm -rf "${dst}"
  if [[ "${1:-}" == "--copy" ]]; then
    cp -R "${src}" "${dst}"
    echo "copied  ${skill} -> ${dst}"
  else
    ln -s "${src}" "${dst}"
    echo "linked  ${skill} -> ${dst}"
  fi
done

cat <<'EOF'

Done. In Codex, invoke with:
  $distribution-god   full strategist run (sequential mode, needs web access)
  $gap-scan           fast local-only gap audit

Note: Codex runs these single-agent. The skill detects this and runs its
phases sequentially — same rigor, longer wall-clock than Claude Code's
parallel mode.
EOF
