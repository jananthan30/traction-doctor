#!/usr/bin/env bash
# Install traction-doctor skills into OpenAI Codex (Agent Skills standard).
#
# Preferred: Codex's native plugin install (see README), which needs no clone.
# This script is the fallback for a local clone: it links (or copies) the
# skills into ~/.agents/skills, where every Codex session discovers them.
# Codex follows a link back into this clone, sees .claude-plugin/ above it, and
# names the skills $traction-doctor:traction-doctor / $traction-doctor:gap-scan /
# $traction-doctor:close-gaps; a --copy has no manifest above it, so its names
# are $traction-doctor / $gap-scan / $close-gaps. close-gaps reads files from
# the traction-doctor skill next to it, so the skills install together.
#
# It only ever replaces or removes entries it created itself: a symlink into
# this clone, or a copy carrying the marker file below. Anything else already
# at a target path is moved to ~/.agents/skills-backup/ (outside the folder
# Codex scans, so it can't show up as a duplicate skill), never deleted.
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="${HOME}/.agents/skills"
BACKUP_DIR="${HOME}/.agents/skills-backup"
SKILLS=(traction-doctor gap-scan close-gaps)
MARKER=".installed-by-traction-doctor"
# Before 0.5.0 the plugin was distribution-god: an earlier install left its
# orchestrator under that name, and its copies carry the old marker.
FORMER_SKILL="distribution-god"
FORMER_MARKER=".installed-by-distribution-god"

usage() {
  cat <<'EOF'
Usage: ./install-codex.sh [--copy | --uninstall | --help]

  (no flag)     symlink the skills into ~/.agents/skills (updates with this clone)
  --copy        copy instead (a frozen snapshot; re-run to update)
  --uninstall   remove the skills this script installed
  -h, --help    show this help
EOF
}

mode="link"
case "${1:-}" in
  "") ;;
  --copy) mode="copy" ;;
  --uninstall) mode="uninstall" ;;
  -h|--help) usage; exit 0 ;;
  *) echo "error: unknown option '${1}'" >&2; usage >&2; exit 2 ;;
esac
if [[ $# -gt 1 ]]; then
  echo "error: expected at most one option" >&2; usage >&2; exit 2
fi

# True when $1 is something this script installed: a symlink into this
# clone's skills/ directory, or a directory holding our marker file.
owned() {
  local dst="$1"
  if [[ -L "${dst}" ]]; then
    [[ "$(readlink "${dst}")" == "${REPO_DIR}/skills/"* ]]
  else
    [[ -f "${dst}/${MARKER}" || -f "${dst}/${FORMER_MARKER}" ]]
  fi
}

# Remove $1 if we own it; otherwise move it aside (install) or leave it (uninstall).
clear_target() {
  local dst="$1" action="$2"
  [[ -e "${dst}" || -L "${dst}" ]] || return 0
  if owned "${dst}"; then
    rm -rf "${dst}"
  elif [[ "${action}" == "install" ]]; then
    local backup
    mkdir -p "${BACKUP_DIR}"
    backup="${BACKUP_DIR}/$(basename "${dst}").$(date +%Y%m%d%H%M%S)"
    mv "${dst}" "${backup}"
    echo "moved   existing ${dst} -> ${backup} (not installed by this script)"
  else
    echo "skipped ${dst} (not installed by this script)"
    return 1
  fi
}

# Remove the orchestrator an install before 0.5.0 left under the old name, if
# this script made it; anything else under that name is left alone.
clear_former() {
  local dst="${TARGET_DIR}/${FORMER_SKILL}"
  if [[ -e "${dst}" || -L "${dst}" ]] && owned "${dst}"; then
    rm -rf "${dst}"
    echo "removed ${dst} (the plugin's name before 0.5.0)"
  fi
}

if [[ "${mode}" == "uninstall" ]]; then
  for skill in "${SKILLS[@]}"; do
    dst="${TARGET_DIR}/${skill}"
    if [[ -e "${dst}" || -L "${dst}" ]]; then
      clear_target "${dst}" uninstall && echo "removed ${dst}"
    fi
  done
  clear_former
  exit 0
fi

mkdir -p "${TARGET_DIR}"
clear_former

for skill in "${SKILLS[@]}"; do
  src="${REPO_DIR}/skills/${skill}"
  dst="${TARGET_DIR}/${skill}"
  [[ -d "${src}" ]] || { echo "error: ${src} not found" >&2; exit 1; }
  clear_target "${dst}" install
  if [[ "${mode}" == "copy" ]]; then
    cp -R "${src}" "${dst}"
    touch "${dst}/${MARKER}"
    echo "copied  ${skill} -> ${dst}"
  else
    ln -s "${src}" "${dst}"
    echo "linked  ${skill} -> ${dst}"
  fi
done

# The dollar signs are literal Codex invocation syntax, not shell expansions.
# shellcheck disable=SC2016
if [[ "${mode}" == "copy" ]]; then
  full='$traction-doctor' scan='$gap-scan' gaps='$close-gaps'
else
  full='$traction-doctor:traction-doctor' scan='$traction-doctor:gap-scan'
  gaps='$traction-doctor:close-gaps'
fi
printf '\nDone. In Codex, invoke with:\n  %-36s full strategist run (needs web access)\n  %-36s fast local-only gap audit\n  %-36s research fixes for the weakest points in STRATEGY.md (needs web access)\n' \
  "${full}" "${scan}" "${gaps}"

cat <<'EOF'

For the full run, start Codex with live web search — `codex --search`, or set
web_search = "live" in ~/.codex/config.toml. The default cached search
returns pre-indexed results, so figures come out stale or `unverified`.

The skills use Codex sub-agents when they are available and otherwise run
their phases one after another, with the same method either way.
EOF
