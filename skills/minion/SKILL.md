---
name: minion
description: Start, work with, and close a Herdr minion, one agent running in its own tab whose work stays this session's responsibility. Use when delegating a task to a background coding agent, following up on or interrupting one that is already running, checking how much context headroom it has left, or closing one out. Requires HERDR_ENV=1.
---

# Minion

A **minion** is an agent started by this session, running in its own tab, whose work this session stays responsible for until it is closed out.

```bash
test "${HERDR_ENV:-}" = 1
```

If that fails, say you are not running inside Herdr and stop.

For any CLI syntax not spelled out below, call the Skill tool with `herdr`.

## Name

The herdr agent name and the tab label are the same string: `minion-<ticket>-<harness>`, with the ticket segment dropped when there is no ticket (`minion-agy`). On a collision with a live agent name, append `-2`, then `-3`. Truncate to fit `[a-z][a-z0-9_-]{0,31}`, trimming the ticket segment first.

## Profile

Read the `herdr-minion-profiles` block in `AGENTS.local.md`, resolved upward from the working directory. It names `default_profile` and a `profiles` map; each profile requires `harness` and may carry `model`, `effort`, `agent`, and `args`. If the workflow does not name a profile, use `default_profile`. If the block is absent, ask the human which harness and settings to use rather than guessing.

Translate the profile's portable fields to native flags for the chosen harness:

| Harness | `model` | `effort` | `agent` | auto-edit flag |
| :--- | :--- | :--- | :--- | :--- |
| `claude` | `--model` | not supported; put it in `args` if the model name should encode it | `--agent` | `--permission-mode acceptEdits` |
| `agy` | `--model` | `--effort` (`low`, `medium`, `high`) | `--agent` | `--mode accept-edits` |
| `opencode` | `--model` | `--variant` | `--agent` | `--auto` (approves every permission, not only edits; there is no edits-only flag) |

For a harness not in this table, or a portable field this table marks unsupported, put the native flags in the profile's `args` instead of guessing a mapping. Every minion starts in auto-edit mode: always include that harness's flag.

## Start

```bash
herdr tab create --workspace "$HERDR_WORKSPACE_ID" --label <name> --cwd <path> --no-focus
```

Read the pane ID from `.result.root_pane.pane_id`; the tab opens at an interactive shell prompt.

```bash
herdr agent start <name> --kind <harness> --pane <pane-id> -- <native flags>
```

Then compose and send the prompt (below):

```bash
herdr agent prompt <name> "<prompt>" --wait
```

## Prompt composition

The prompt carries, in order:

1. The task.
2. The ticket reference, if there is one.
3. The acceptance criteria the minion is working against.
4. A demand for evidence: the minion reports what it verified, not just what it did.
5. An instruction to write a handoff before finishing, to whichever of these fits what the minion was spawned for: `~/.agents/handoff/<ticket>-handoff.md`, `<map>-handoff.md`, or `<workspace>-handoff.md`. Where the repo has a `handoff` skill installed, tell the minion to use it instead of writing the file freehand.

## Follow-up

Once the minion settles (`idle` or `done`) and more work remains on the same task, send it directly rather than closing the tab and starting over:

```bash
herdr agent prompt <name> "<next instruction>" --wait
```

## Interrupt

To redirect a working minion, send Escape and wait for it to settle before prompting new work; prompting into an agent still mid-turn queues behind whatever it is already doing, which is rarely what a redirect wants.

```bash
herdr agent send-keys <name> esc
herdr agent wait <name>
herdr agent prompt <name> "<redirected instruction>" --wait
```

## Context headroom

Headroom is how much of the minion's context window is still unused. The limit is 15% of context used, or 150k tokens where a count exists, overridable in a `<!-- minion-settings:start -->` block in `AGENTS.md` or `AGENTS.local.md`. That setting cannot live in the `herdr-minion-profiles` block; its parser rejects unknown fields.

How to read it depends on the harness:

- `claude`: `herdr agent list` reports `tokens.context` for it.
- `agy`: its statusline prints `Context N%`, read with `herdr pane read <pane-id> --source visible`.
- `opencode`: exposes no context figure. Report that headroom cannot be checked rather than implying it was.

On crossing the limit: tell the minion to commit and write its handoff, wait for it to settle, close the tab, and spawn a successor seeded with that handoff if work remains.

## Teardown

Before `herdr tab close <tab_id>`, verify the artifact the minion was asked to produce, a commit, a written file, a passing check, against what the prompt actually asked for. Closing without that check is not teardown, it is losing track of the minion.
