#!/usr/bin/env bash
# PreToolUse hook: enforces the <type>/<slug> branch naming convention
# (see plugins/foundations/skills/branch-naming/SKILL.md) on `git checkout -b`
# and `git switch -c` commands, before the branch is created.
set -euo pipefail

input="$(cat)"
command="$(echo "$input" | jq -r '.tool_input.command // empty')"

if [[ -z "$command" ]]; then
  exit 0
fi

branch_name="$(echo "$command" | sed -nE 's/.*(git checkout -b|git switch -c)[[:space:]]+([^[:space:]]+).*/\2/p')"

if [[ -z "$branch_name" ]]; then
  exit 0
fi

pattern='^(feat|fix|docs|chore|refactor|test|perf|ci|build)/[a-z0-9]+(-[a-z0-9]+)*$'

if [[ "$branch_name" =~ $pattern ]]; then
  exit 0
fi

reason="Branch name '$branch_name' doesn't match the <type>/<slug> convention (types: feat, fix, docs, chore, refactor, test, perf, ci, build; slug: lowercase, hyphen-separated, no underscores/spaces/ticket numbers). See the branch-naming skill for details and examples."

jq -n --arg reason "$reason" '{
  hookSpecificOutput: {
    hookEventName: "PreToolUse",
    permissionDecision: "deny",
    permissionDecisionReason: $reason
  }
}'
exit 0
