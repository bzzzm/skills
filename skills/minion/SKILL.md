---
name: minion
description: Start, work with, and close a Herdr minion. Use when delegating a task to a background coding agent, following up on or interrupting a running one, checking its context headroom, or closing one out. Requires HERDR_ENV=1.
---

# Minion

A **minion** is an agent started by this session, running in its own tab, whose work this session stays responsible for until it is closed out.

```bash
test "${HERDR_ENV:-}" = 1
```

If that fails, say you are not running inside Herdr and stop.

Reach Herdr through the `herdr` CLI only. If `herdr` is not on `$PATH`, use `~/.local/bin/herdr`. Any MCP minion tools available in context are out of scope here. For CLI syntax not spelled out below, call the Skill tool with `herdr`.

## Lifecycle

| Doing this | Read |
| :--- | :--- |
| Spawning one: naming, profile, start, prompt | [`SPAWN.md`](SPAWN.md) |
| Working with a running one: follow-up, interrupt, stall, headroom | [`STEER.md`](STEER.md) |
| Closing one out | below |

## Teardown

Before `herdr tab close <tab_id>`, verify the artifacts the minion was asked to produce, every one of them, against what the prompt actually asked for: the commit, the written file, the passing check, the ticket update. Closing without that check is not teardown, it is losing track of the minion.
