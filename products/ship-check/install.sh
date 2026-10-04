#!/usr/bin/env bash
# Install the Ship Check skill for Claude Code and/or OpenAI Codex.
#
#   ./install.sh                 # auto-detect installed tools, install for current user
#   ./install.sh --claude        # Claude Code only
#   ./install.sh --codex         # Codex only
#   ./install.sh --all           # both, even if not detected
#   ./install.sh --project DIR   # install into a repo instead (shared with your team)
#   ./install.sh --uninstall     # remove it again (combine with the flags above)
set -euo pipefail

SKILL_NAME="ship-check"
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/skills/${SKILL_NAME}"

want_claude=0 want_codex=0 project="" uninstall=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --claude) want_claude=1 ;;
    --codex) want_codex=1 ;;
    --all) want_claude=1; want_codex=1 ;;
    --project) project="${2:?--project needs a directory}"; shift ;;
    --uninstall) uninstall=1 ;;
    -h|--help) sed -n '2,10p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "Unknown option: $1" >&2; exit 2 ;;
  esac
  shift
done

if [[ ! -f "${SRC}/SKILL.md" ]]; then
  echo "Cannot find ${SRC}/SKILL.md - run this script from the unzipped package." >&2
  exit 1
fi

if [[ $want_claude -eq 0 && $want_codex -eq 0 ]]; then
  command -v claude >/dev/null 2>&1 || [[ -d "${HOME}/.claude" ]] && want_claude=1
  command -v codex  >/dev/null 2>&1 || [[ -d "${HOME}/.codex" ]] && want_codex=1
  if [[ $want_claude -eq 0 && $want_codex -eq 0 ]]; then
    echo "Neither Claude Code nor Codex was detected; installing for both."
    want_claude=1; want_codex=1
  fi
fi

if [[ -n "$project" ]]; then
  base="$(cd "$project" && pwd)"
  claude_dir="${base}/.claude/skills"
  codex_dir="${base}/.agents/skills"
else
  claude_dir="${CLAUDE_SKILLS_DIR:-${HOME}/.claude/skills}"
  codex_dir="${CODEX_SKILLS_DIR:-${HOME}/.agents/skills}"
fi

install_to() {
  local label="$1" dir="$2" dest="$2/${SKILL_NAME}"
  if [[ $uninstall -eq 1 ]]; then
    rm -rf "$dest" && echo "Removed ${label} skill: ${dest}"
    return
  fi
  mkdir -p "$dir"
  rm -rf "$dest"
  cp -R "$SRC" "$dest"
  chmod +x "${dest}/scripts/scan.py" 2>/dev/null || true
  echo "Installed for ${label}: ${dest}"
}

[[ $want_claude -eq 1 ]] && install_to "Claude Code" "$claude_dir"
[[ $want_codex  -eq 1 ]] && install_to "Codex" "$codex_dir"

if [[ $uninstall -eq 0 ]]; then
  echo
  echo "Done. Restart your agent, then ask:  \"Is this repo ready to ship?\""
  echo "  Claude Code: or type /ship-check"
  echo "  Codex:       or mention \$ship-check"
fi
