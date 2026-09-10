# Minion context

**Cadence:** 15s.

**State.** One call covers every watched minion at once:

```bash
herdr tab list --workspace "$HERDR_WORKSPACE_ID"
```

Filter to tabs labelled `minion-*`. Each tab's `agent_status` is the minion's state.

Read the minion's conversation ID from `.result.agent.agent_session.value` with `herdr agent get <name>` (or `.result.agents[]` in `herdr agent list`).

**Settled** is a claim to check, never a verdict to act on. `idle` or `done` makes a minion a candidate; some harnesses report `done` for an agent parked at a permission prompt, having produced nothing. Confirm with one buffer read before dropping it from the watchlist: the buffer shows the turn ended and no prompt pending. That is one read per settle event, not per cycle.

**On `blocked`**, or on a candidate whose buffer shows a pending prompt, read the buffer:

```bash
herdr agent read <name> --source recent-unwrapped --lines 120
```

Babysit answers prompts through keystrokes to the minion tab (`herdr agent send-keys <name> ...`). Never run the minion's command in your own shell.

Approve routine development commands inside the workspace:
- File and symlink creation (`touch`, `mkdir`, `ln`, `cp`).
- Package and dependency management (`pip`, `npm`, `pnpm`, `yarn`, `cargo`, `go get`).
- Reading, searching, and inspecting (`cat`, `ls`, `grep`, `find`, `git status`, `git log`, `git diff`).
- Test runners, linters, and formatters (`pytest`, `ruff`, `eslint`, `go test`).
- Read-only network fetches of a URL the minion has chosen to read.
- Harness UI prompts: confirmations, mode toggles, continuations, and rating or survey screens (send `0` or dismiss).

When an interactive prompt offers an option to always allow the command for this conversation (such as option 2 in `agy`), select that option to avoid blocking repeatedly on the same binary. Fetch approvals arrive one per domain, so a research minion parks over and over on the same permission; this is the option that ends that.

Escalate to the human only when the command:
- Contains destructive operations: file deletions (`rm`, `unlink`), database drops or truncations, or destructive git actions (`git reset --hard`, `git push --force`, `git checkout .`, `git branch -D`).
- Targets production infrastructure, remote production databases, or cloud deployments.

Anything requiring escalation leaves the minion blocked and wakes the human through the loop's escalation step, naming the minion and what it is asking.

**Stalled** is `working` that is not moving: a pane hung on processes that already died still reports `working` every cycle. A minion whose buffer is unchanged across several minutes is a stall candidate; confirm and interrupt it through the `minion` skill's stall rules, call the Skill tool with `minion` for that. A confirmed stall that an interrupt does not clear escalates.

**Context headroom** is never a directed extra read on this cadence. Note it only when a read already done for another reason on this minion (answering a blocked prompt, or a read the user asked for) happens to carry it, using the per-harness method from the `minion` skill, call the Skill tool with `minion` for that.
