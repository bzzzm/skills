---
name: babysit
description: Watch resources until they settle, acting only within each one's own rules. Use when the user wants a minion, changelist, or issue watched, asks to babysit or keep an eye on something until it's done, or wants to dispatch minions across an issue query or map. Requires HERDR_ENV=1.
---

# Babysit

```bash
test "${HERDR_ENV:-}" = 1
```

If that fails, say you are not running inside Herdr and stop. Reach Herdr through `herdr`. If `herdr` is not on `$PATH`, use `~/.local/bin/herdr`.

Babysit writes no code and runs no reviews. Where the work it is watching needs technical action, call the Skill tool with `minion` to spawn one for it.

## The loop

When started, or right after spawning a minion, enter the loop immediately. Do not return to the user after starting or recording a resource: keep running until every watched resource has settled, an escalation triggers, or the user stops the loop.

Read the watchlist, then for each resource: check its state through its context, classify what that state calls for, act within that context's rules, wait the context's cadence, repeat.

## Status format

Every progress update printed during the loop follows this fixed structure so updates remain scannable across cycles:

```markdown
🔄 **Babysit loop**
- **Orchestrator:** [<orchestrator-conv-id>](conversation://<orchestrator-conv-id>)
- **<Resource-Type>:** <identifier> [<conv-id-if-minion>](conversation://<conv-id>) | <status> [| context: <percent>% (<tokens>)]
  <Indented concrete action, file modified, or condition waiting on>
⏳ Next check in <cadence>.
```

Rules for the status block:
- **Header:** Starts with `🔄 **Babysit loop**`.
- **Orchestrator:** First bullet links the driving session's conversation ID.
- **Resources:** One bullet per active watched resource (`Minion:`, `Issue:`, `Changelist:`). For minions, include the minion's conversation ID link (from `agent_session.value`) and context usage. Indent the latest action or state change directly below.
- **Footer:** Ends with `⏳ Next check in <cadence>.` stating the wait until the next cycle.

A **resource** is one thing being watched: a minion, a changelist, an issue. A **context** is the rules for one kind of resource, one reference file each because they differ in more than a cadence:

| Resource | Context | Cadence |
| :--- | :--- | :--- |
| A minion this session spawned | [`RESOURCES/minion.md`](RESOURCES/minion.md) | 15s |
| A changelist: a merge request, a pull request, or whatever the repo calls one | [`RESOURCES/cl.md`](RESOURCES/cl.md) | 15 minutes |
| One issue, or an issue query or map to dispatch across | [`RESOURCES/issue.md`](RESOURCES/issue.md) | 15 minutes |

A resource is **settled** once its context says it has reached the state that ends the watch. A settled resource is dropped from the loop and removed from the watchlist; the loop keeps running for whatever is left.

## Escalation

Whatever a context's rules do not cover wakes the human, in conversation if this is an interactive session, otherwise with:

```bash
herdr notification show "<what needs a decision>" --sound request
```

The rest of the watchlist stays watched while the human decides.

## Slots

Five minions running at once by default, overridable with a `slots` field in the same `<!-- minion-settings:start -->` block the `minion` skill reads its headroom override from. Babysit never exceeds the cap; when a context wants to spawn a minion and every slot is full, it holds that resource back and reports how much work is waiting.

Quota is the other cap, and the one that bites mid-batch: a full slate of high-effort minions can spend an hourly allowance in a single run, and the work already done is what gets stranded. Read the harness account's remaining quota from its statusline before dispatching a batch, and dispatch fewer than the slots allow when what is left will not cover them.

## Watchlist

The standing record of what a workspace is being babysat for, at `~/.agents/babysit/<workspace>.md`. Name the file for the herdr workspace's `label` (from `herdr workspace list`, matched to `$HERDR_WORKSPACE_ID`), with any `/` in the label written as `-` (`home/mono` becomes `home-mono.md`). Fall back to the repository name outside Herdr, or to the map name for a run scoped to one map.

One line per resource:

```
- <type>: <identifier>: <why it is watched>[, cadence: <override>]
```

Read the watchlist on start. Add a line the moment babysit starts watching something new. Remove a line the moment its resource settles for good. The watchlist holds no run state and is not a log: never rewrite it just because a cycle passed.
