#!/bin/bash
# Global agent command guard.
# Blocks catastrophic shell commands before agents run them.
# Denylist: ~/.agents/hooks/dangerous-patterns.txt (one ERE regex per line).
#
# Used by:
#   Claude Code  ~/.claude/settings.json      PreToolUse (matcher Bash)
#   Codex        ~/.codex/hooks.json          PreToolUse (matcher Bash)
#   Cursor       ~/.cursor/hooks.json         beforeShellExecution (arg: cursor)
#   Antigravity  ~/.gemini/config/hooks.json  PreToolUse (matcher run_command, arg: antigravity)
#
# stdin:  hook JSON. Claude/Codex put the command at .tool_input.command,
#         Grok at .toolInput.command, Cursor at .command,
#         Antigravity at .toolCall.args.CommandLine.
# Block:  default mode      -> exit 2 + reason on stderr (Claude/Codex contract).
#         "cursor" mode     -> {"permission":"deny",...} JSON on stdout, exit 0.
#         "antigravity"     -> {"decision":"deny","reason":...} on stdout, exit 0.
# Allow:  default mode      -> exit 0, silent.
#         "cursor" mode     -> {"permission":"allow"}.
#         "antigravity"     -> {"decision":"allow"}.
#
# Antigravity fails CLOSED: a crash, a timeout, a non-zero exit or unparseable
# stdout denies the tool call. Every allow path here must print its verdict and
# exit 0, and nothing but the verdict may reach stdout.

export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH"
PATTERNS_FILE="$HOME/.agents/hooks/dangerous-patterns.txt"
MODE="${1:-exitcode}"

REASON_TAIL="Do not retry it or try to work around the guard; explain the block to the user instead."

allow() {
  case "$MODE" in
    cursor)      printf '{"permission":"allow"}\n' ;;
    antigravity) printf '{"decision":"allow"}\n' ;;
  esac
  exit 0
}

deny() { # $1 = matched pattern
  local msg="Blocked by the global dangerous-command guard (~/.agents/hooks/dangerous-patterns.txt). Matched pattern: $1. $REASON_TAIL"
  case "$MODE" in
    cursor)
      jq -cn --arg m "$msg" '{
        permission: "deny",
        user_message: "Command guard blocked a dangerous command.",
        agent_message: $m
      }'
      exit 0 ;;
    antigravity)
      jq -cn --arg m "$msg" '{decision: "deny", reason: $m}'
      exit 0 ;;
  esac
  echo "$msg" >&2
  exit 2
}

# Without jq we cannot inspect the command: fail open rather than break agents.
command -v jq >/dev/null 2>&1 || allow

INPUT=$(cat)
# .tool_input = Claude/Codex, .toolInput = Grok CLI (Claude-compat mode),
# .command = Cursor, .toolCall.args.CommandLine = Antigravity
CMD=$(printf '%s' "$INPUT" | jq -r '.tool_input.command // .toolInput.command // .command // .toolCall.args.CommandLine // empty' 2>/dev/null)

[ -z "$CMD" ] && allow
[ -f "$PATTERNS_FILE" ] || allow

while IFS= read -r pattern; do
  case "$pattern" in ''|\#*) continue ;; esac
  if printf '%s\n' "$CMD" | grep -qE -- "$pattern" 2>/dev/null; then
    deny "$pattern"
  fi
done < "$PATTERNS_FILE"

allow
