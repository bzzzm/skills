# Workspace Env

Exports `HERDR_WORKSPACE` into every Herdr shell: the absolute path of the workspace the pane
belongs to, whether that workspace is a linked worktree or a plain directory.

Herdr already injects `HERDR_WORKSPACE_ID`, `HERDR_TAB_ID` and `HERDR_PANE_ID` into panes, but
an id is not a path, and no read-only Herdr command turns one into a path for a workspace that
is not a git worktree.

## Install

Link the plugin, then source the shell hook.

```sh
herdr plugin link ~/work/skills/herdr-plugins/herdr-workspace-env
```

Add to `~/.zshrc` (or `~/.bashrc`):

```sh
[ -f ~/work/skills/herdr-plugins/herdr-workspace-env/shell/herdr-workspace-env.sh ] \
  && . ~/work/skills/herdr-plugins/herdr-workspace-env/shell/herdr-workspace-env.sh
```

Open a new pane and check:

```sh
printf '%s\n' "$HERDR_WORKSPACE"
```

Panes that were already open keep the old environment until their shell restarts.

## Why both halves

A Herdr plugin manifest accepts `build`, `startup`, `actions`, `events`, `panes` and
`link_handlers`. None of them add a variable to a pane's environment, so the export has to
happen in the pane's own shell. That is the hook's half.

The plugin's half is the part a shell hook cannot do. A workspace created moments ago is
absent from `~/.config/herdr/session.json`, and `herdr worktree list` answers only for git
workspaces, so a shell starting in a brand-new non-git workspace has nowhere to look. The
creation events carry the path in their context, and the hook records it as the workspace is
born.

## Resolution chain

The shell hook takes the first answer that names a directory that exists, and leaves
`HERDR_WORKSPACE` unset when none do.

1. `identity_cwd` from `~/.config/herdr/session.json`. Authoritative and fast (3ms via `jq`),
   but blind to workspaces created seconds ago.
2. The plugin's cache under `~/.local/state/herdr/plugins/mihai.workspace-env/workspaces/`,
   written by the creation events. Covers exactly that blind spot.
3. `herdr worktree list --workspace <id>`, reading `source.source_checkout_path`. An IPC
   roundtrip, and it answers only inside a git work tree.

`workspace_cwd` from the plugin context is deliberately not a link in this chain outside of
creation. On a focus event it tracks the focused pane's cwd, not the workspace: in a live
session, workspace `w1H` reported `workspace_cwd` as `/home/mihai/Documents/acoperis` while the
workspace itself is `/home/mihai`.

## Debugging

```sh
herdr plugin action invoke show --plugin mihai.workspace-env
herdr plugin log list --plugin mihai.workspace-env --limit 1
```

The action reports on the *focused* workspace, not the one you invoked it from:
`herdr plugin action invoke` targets whatever workspace has focus.
