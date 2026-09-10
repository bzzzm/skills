# Spec: herdr-workspace-env scripts

Three shell scripts plus a test harness. `herdr-plugin.toml` is already written and is the
contract: it names `bin/cache-workspace-path.sh` and `bin/show.sh`. The third script,
`shell/herdr-workspace-env.sh`, is sourced by the user's shell rc and is named by `README.md`.

Target shells: `zsh` and `bash`. Write POSIX `sh` throughout so both source it and `sh` runs it.

## What HERDR_WORKSPACE holds

The absolute path of the workspace the current pane belongs to: `identity_cwd` in Herdr's
session state. It is the worktree checkout path for a worktree-backed workspace and the
plain directory for every other one. Verified against a live session:

| workspace | kind | value |
| --- | --- | --- |
| `w1H` | plain, not a git repo | `/home/mihai` |
| `w1A` | git repo, subdirectory of the repo root | `/home/mihai/work/skills/skills` |
| `w4` | git repo, workspace at the repo root | `/home/mihai/work/home/mono` |
| `wG` | linked worktree | `/home/mihai/.herdr/worktrees/cosmos/mma-toolbox-sso` |

## `shell/herdr-workspace-env.sh`

Sourced on every interactive shell start, so it runs in the pane's own shell. Exit without
touching the environment unless `$HERDR_ENV` is `1` and `$HERDR_WORKSPACE_ID` is non-empty.

Resolve through this chain and export `HERDR_WORKSPACE` from the first link that answers with
a path that exists as a directory. Leave the variable unset when every link comes up empty:
an unset variable is honest, a wrong path is not.

1. **`~/.config/herdr/session.json`**, honouring `$XDG_CONFIG_HOME` and `$HERDR_CONFIG_PATH`
   (the latter names the config *file*; the session file is its sibling `session.json`).
   The shape is `{"workspaces": [{"id": "w1A", "identity_cwd": "/path", ...}, ...]}`.
   Read it with `jq -r --arg id "$HERDR_WORKSPACE_ID" '.workspaces[]|select(.id==$id)|.identity_cwd // empty'`.
   Measured at 3ms on a 50KB session file, which is the whole reason this link is first.
   Skip the link when `jq` is absent rather than failing the hook.
2. **The plugin cache**, `${XDG_STATE_HOME:-$HOME/.local/state}/herdr/plugins/mihai.workspace-env/workspaces/$HERDR_WORKSPACE_ID`,
   a file holding one path. Covers the window where a brand-new workspace has not reached
   `session.json` yet. A plain `cat`, no dependency.
3. **`herdr worktree list --workspace "$HERDR_WORKSPACE_ID"`**, reading
   `.result.source.source_checkout_path`. An IPC roundtrip and git-only, hence last.
   Use `${HERDR_BIN_PATH:-herdr}`. It answers `{"error":{"code":"not_git_worktree",...}}`
   for a non-git workspace; treat any `.error` as no answer.

The script is sourced into the user's live shell, so it may not `set -e`, may not `exit`, may
not leak helper functions or scratch variables, and may not write to stdout or stderr on the
happy path. Wrap the body in a function and `unset -f` it at the end.

## `bin/cache-workspace-path.sh`

Runs as the `workspace.created`, `worktree.created` and `worktree.opened` event hook. Herdr
passes the context in `$HERDR_PLUGIN_CONTEXT_JSON` and also sets `$HERDR_PLUGIN_STATE_DIR`.
A real captured context:

```json
{"workspace_id":"w1H","workspace_label":"home","workspace_cwd":"/home/mihai/Documents/acoperis","tab_id":"w1H:t3","tab_label":"agy","focused_pane_id":"w1H:p3","focused_pane_cwd":"/home/mihai/Documents/acoperis","focused_pane_agent":"agy","focused_pane_status":"idle","invocation_source":"cli","correlation_id":"cli:plugin"}
```

Write `workspace_cwd` to `$HERDR_PLUGIN_STATE_DIR/workspaces/<workspace_id>`, creating the
directory. Write nothing when either field is missing or the path is not a directory. Writing
must be atomic (temp file in the same directory, then `mv`), since a shell in a new pane may
be reading the file at the same moment.

The cache is append-and-overwrite only, never pruned. A stale entry for a closed workspace
costs one file; a workspace id is never reused, so a stale entry is never read back.

## `bin/show.sh`

The `show` action. Print, for the focused workspace, which link answered and with what, then
each link's raw answer. Herdr captures stdout into the plugin log, so plain lines are the
right output. The action runs against the *focused* workspace, not the caller's, because
`herdr plugin action invoke` targets the focused one; say so in the output so a reader is not
misled.

## `tests/run.sh`

Run the resolver against fixture trees rather than the live session. Drive it by overriding
`XDG_CONFIG_HOME`, `XDG_STATE_HOME` and `HERDR_BIN_PATH` (pointing the last at a stub script
that prints a canned JSON response), so no case touches the real Herdr.

Cover, at minimum: each link answering in turn; a link answering with a path that does not
exist, falling through to the next; every link empty leaving `HERDR_WORKSPACE` unset;
`HERDR_ENV` unset leaving it unset; `jq` absent falling through to the cache. Assert also that
sourcing the script leaves no helper function or scratch variable behind.

Run the suite under both `sh` and `zsh`.
