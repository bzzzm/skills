#!/usr/bin/env bash
# Call the Paperclip REST API as the board operator.
#
#   api.sh base                                  print the instance URL
#   api.sh GET /companies
#   api.sh POST /issues/PC-12/comments '{"body":"..."}'
#   jq -n ... | api.sh POST /companies/<id>/issues @-
#
# Reads PAPERCLIP_API_URL and PAPERCLIP_API_KEY from board.env. The key goes to
# curl through a file descriptor, so it never shows up in argv or in output.
set -euo pipefail

env_file="${PAPERCLIP_BOARD_ENV:-$HOME/.config/paperclip/board.env}"
if [[ ! -r "$env_file" ]]; then
  echo "paperclip: $env_file not found" >&2
  exit 78
fi
# shellcheck disable=SC1090
. "$env_file"
: "${PAPERCLIP_API_URL:?not set in $env_file}"
: "${PAPERCLIP_API_KEY:?not set in $env_file}"
base="${PAPERCLIP_API_URL%/}"

if [[ "${1:-}" == base ]]; then
  echo "$base"
  exit 0
fi
if [[ $# -lt 2 || $# -gt 3 ]]; then
  echo "usage: api.sh base | api.sh METHOD /path [json | @file | @-]" >&2
  exit 64
fi

args=(-sS --fail-with-body -X "$1")
if [[ $# -eq 3 ]]; then
  args+=(-H "Content-Type: application/json" --data-binary "$3")
fi
exec curl "${args[@]}" \
  -H @<(printf 'Authorization: Bearer %s\n' "$PAPERCLIP_API_KEY") \
  "$base/api$2"
