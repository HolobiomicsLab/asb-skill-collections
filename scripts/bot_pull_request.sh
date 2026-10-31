#!/usr/bin/env bash
# Propose regenerated files to main as a pull request from a bot branch.
#
# Usage: scripts/bot_pull_request.sh <bot/branch> <title> <path>...
#
# Workflows that regenerate tracked files call this instead of pushing to main,
# so main changes only through a pull request. The script commits the
# working-tree state of the given paths on top of HEAD without moving HEAD, so
# later steps see the same checkout. It then points the bot branch, which the
# workflow owns, at that commit, and opens a pull request into main unless one
# from that branch is already open. A fixed branch name keeps one pull request
# carrying the latest regeneration; a name that changes per run gives each run
# its own pull request.
#
# The branch is rewritten with an explicit lease: the push succeeds only if the
# branch is still where `git ls-remote` saw it (or still absent), so two runs at
# once cannot silently overwrite each other.
#
# A pull request opened with the workflow's GITHUB_TOKEN does not start other
# workflows: close and reopen it so the checks run before merging. Opening it
# needs the repository setting that lets GitHub Actions create pull requests,
# and the job needs `contents: write` and `pull-requests: write`.
#
# Environment: GH_TOKEN for gh; GITHUB_WORKFLOW names the caller in the body.
set -euo pipefail

if [ "$#" -lt 3 ]; then
  echo "usage: $0 <bot/branch> <title> <path>..." >&2
  exit 2
fi
branch="$1"
title="$2"
shift 2
case "${branch}" in
  bot/?*) ;;
  *)
    echo "::error::the branch must start with bot/: ${branch}" >&2
    exit 2
    ;;
esac

paths=()
for path in "$@"; do
  if [ -e "${path}" ] || git ls-files --error-unmatch -- "${path}" >/dev/null 2>&1; then
    paths+=("${path}")
  fi
done
if [ "${#paths[@]}" -eq 0 ]; then
  echo "None of the paths exist: $*"
  exit 0
fi

# Build the tree in a separate index seeded from HEAD, so only the given paths
# enter the commit, whatever an earlier step staged in the real index.
index_dir="$(mktemp -d)"
trap 'rm -rf "${index_dir}"' EXIT
export GIT_INDEX_FILE="${index_dir}/index"
git read-tree HEAD
git add -- "${paths[@]}"
if git diff --cached --quiet; then
  echo "No changes to propose in: ${paths[*]}"
  exit 0
fi
commit="$(git commit-tree "$(git write-tree)" -p HEAD -m "${title}")"
unset GIT_INDEX_FILE
seen="$(git ls-remote origin "refs/heads/${branch}" | cut -f1)"
git push --force-with-lease="refs/heads/${branch}:${seen}" origin "${commit}:refs/heads/${branch}"

open="$(gh pr list --head "${branch}" --base main --state open --json number --jq 'length')"
if [ "${open}" != "0" ]; then
  echo "A pull request from ${branch} is already open; the branch now carries ${commit}"
  exit 0
fi
body="Opened by the ${GITHUB_WORKFLOW:-release} workflow, which does not push to main.
A pull request opened with the workflow token does not start other workflows:
close and reopen it so the checks run before merging."
gh pr create --base main --head "${branch}" --title "${title}" --body "${body}"
