# 02: Settle the agent-workflow / minion-manager boundary

**What to build:** A written decision, agreed with Mihai, that says how the two Herdr skills divide once their `home/mono` halves are cut away. Nothing gets migrated until this is settled, because the answer changes what each migration is allowed to keep.

`agent-workflow` is minion lifecycle standards plus mono monorepo navigation. `minion-manager` is the orchestration loop wrapped in mandatory mono preambles. Cutting mono out of both leaves an overlap that has to be resolved once rather than twice. Both live at `~/work/home/mono/.agents/skills/`.

This is a conversation with Mihai, not a decision to make alone.

**Blocked by:** None (can start immediately)

**Status:** done

**Type:** grilling

- [x] Decided: the portable remainders stay two skills, or collapse into one
- [x] Decided: which skill owns the minion lifecycle vocabulary, so it is defined in exactly one place
- [x] Decided: where a consuming repo's specifics live (a config file the skill reads, a documented convention, or left behind entirely)
- [x] Decided: how a skill here declares its dependency on `herdr`, which stays upstream at `herdrdev/herdr` and is never vendored
- [x] The decision is recorded where the migrations will find it

---

## Decision

Settled with Mihai on 2026-09-03, by grilling. The portable remainders are **not** migrations of `agent-workflow` and `minion-manager`. Those two stay in mono until 05 deletes them. Two new skills get written instead, cut along a different seam: `minion` knows minions, `babysit` knows loops.

Herdr is reached through the `herdr` CLI only. The MCP tools are out of scope for these skills. For CLI syntax, call the Skill tool with `herdr`. Both skills require `HERDR_ENV=1` and say so.

### `minion` (model-invoked)

One minion, end to end: what a minion is, how to start one, how to work with it, how to close it.

**One tab per minion**, appended to the end of the current workspace's tab list, replacing the shared `minions` tab that `herdr_minion_spawn` builds. `herdr tab create --workspace "$HERDR_WORKSPACE_ID" --label <name> --cwd <path> --no-focus` returns `result.root_pane.pane_id` already at a shell prompt, then `herdr agent start <name> --kind <harness> --pane <pane-id> -- <native flags>` and `herdr agent prompt <name> "<prompt>"`.

**Name.** The herdr agent name and the tab label are the same string: `minion-<ticket>-<harness>`, with the ticket segment dropped when there is no ticket (`minion-agy`), `-2` and `-3` suffixes on collision, truncated to fit `[a-z][a-z0-9_-]{0,31}`.

**Profiles.** Read the `herdr-minion-profiles` block in `AGENTS.local.md`, resolved upward from the working directory, and translate `harness`, `model`, `effort`, `agent` and `args` into native flags. Off the MCP tool, this skill owns that adapter table.

**Every minion starts in auto-edit mode.**

**Prompt composition** carries the task, the ticket reference, the acceptance criteria, the demand for evidence, and the instruction to write a handoff before finishing. Handoffs go to `~/.agents/handoff/<ticket>-handoff.md`, `<map>-handoff.md`, or `<workspace>-handoff.md`, picked by what the minion was spawned for. Where the repo has a `handoff` skill installed, the prompt tells the minion to use it.

**Context headroom.** The limit is 15% of context used, or 150k tokens where a count exists, overridable in a `<!-- minion-settings:start -->` block in `AGENTS.md` or `AGENTS.local.md`. It cannot live in the herdr profiles block, whose parser rejects unknown fields. Claude minions report `tokens.context` through `herdr agent list`; agy prints `Context N%` in its statusline, read with `herdr pane read <pane> --source visible`; opencode exposes nothing, and the skill reports that rather than implying it checked. On crossing the limit: tell the minion to commit and write its handoff, wait for it to settle, close the tab, and spawn a successor seeded with the handoff when work remains.

**Teardown** verifies the artifact the minion was asked to produce before `herdr tab close`.

### `babysit` (model-invoked)

The watch loop, and nothing else. It writes no code and runs no reviews. When the work it is watching needs technical action, it spawns a minion for it by calling the Skill tool with `minion`.

The loop is one shape for every resource: read the watchlist, check each resource, classify, act within that context's rules, wait the cadence, repeat. It runs in the foreground and returns when everything settles or the user stops it.

**Contexts** are one reference file each, because they differ in more than a number:

- `RESOURCES/minion.md`, 15s. One `herdr tab list --workspace <id>` call covers every minion at once, filtered to `minion-*` labels. Settled is `idle` or `done`. On `blocked`, read the buffer and answer within the approval rules below. Context headroom is checked from output babysit is already reading, never by a directed extra read, unless the user asks for a fresh number.
- `RESOURCES/cl.md`, 15 minutes. A changelist: a merge request, a pull request, or whatever the repo's `AGENTS.md` says a changelist is there. Watch its state, its pipeline, and its review comments. Settled is merged or closed. A failing pipeline or a new review comment spawns a minion; babysit never fixes it.
- `RESOURCES/issue.md`, 15 minutes. The agent learns how issues work in this repo from `AGENTS.md` and `AGENTS.local.md` and the skills they name, so no tracker is hardcoded. Given one issue, watch its state. Given a query or a map, dispatch: keep up to the slot cap busy by spawning a minion per ready issue.

**Approval rules**, in `RESOURCES/minion.md`. Babysit may answer a blocked minion, in conversation or persistently, only when the whole command is a single invocation of an allowlisted read-only binary with no shell metacharacter in it: `echo`, `pwd`, `ls`, `cat`, `head`, `tail`, `wc`, `stat`, `file`, `find` without `-exec` or `-delete`, `grep`, `rg`, `ps`, `date`, `env`, `which`, `git status`, `git log`, `git diff`, `git show`, `go doc`. Harness UI prompts (edit-mode toggle, "continue?", dismissals) are answered too. Everything else wakes the human with `herdr notification show --sound request` while the remaining resources stay watched.

**Slots.** Five minions at once, configurable in the same `minion-settings` block. Babysit refuses to exceed the cap and reports how much work it is holding back.

**Watchlist.** `~/.agents/babysit/<workspace>.md`, named for the herdr workspace (`skills`, `home/mono` written as `home-mono.md`, `pcc-cla`), falling back to the repository name, or the map name for a map-scoped run. One entry per resource: type, identifier, why it is watched, and any cadence override. Babysit reads it on start, adds an entry when it starts watching something new, and removes one when a resource settles for good. It holds no run state and is not a log, so it is not rewritten every cycle.

### What stays in mono

Ticket intake and classification, the repository preamble, the `arch` router, the Gitea specifics, the monorepo table, and anything naming `kornel-cluster`. None of it travels.
