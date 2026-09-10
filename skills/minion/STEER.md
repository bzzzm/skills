# Working with a running minion

## Follow-up

Once the minion settles and more work remains on the same task, send it directly rather than closing the tab and starting over:

```bash
herdr agent prompt <name> "<next instruction>" --wait
```

## Interrupt

Escape is not a pause. On `agy` it discards the turn in progress along with everything the minion accumulated in it, a context drop steep enough to send an hour-old investigation back to zero; the minion starts that work again from nothing.

So choose by which loss is cheaper. A prompt sent mid-turn queues behind the current turn and lands when it ends: you pay the rest of that turn, and the context survives. Escape pays the whole turn. Redirect a merely slow minion with a queued prompt, and reserve Escape for one that is genuinely stalled or working on the wrong thing entirely.

```bash
herdr agent send-keys <name> esc
herdr agent wait <name>
herdr agent prompt <name> "<redirected instruction>" --wait
```

## Stall

`working` is a status, not evidence of progress. A harness pane keeps reporting `working` while its tool calls hang on processes that already died, and Herdr reports the same thing back.

Progress is the context figure moving between two reads minutes apart. A figure frozen across reads, with the same tool call still on screen, is a **stall**: confirm it by checking on the host or in the container whether the process the pane claims to be running still exists, then interrupt with a fenced instruction that keeps it out of whatever sank it.

## Context headroom

Headroom is how much of the minion's context window is still unused. The limit is 15% of context used, or 150k tokens where a count exists, overridable in a `<!-- minion-settings:start -->` block in `AGENTS.md` or `AGENTS.local.md`. That setting cannot live in the `herdr-minion-profiles` block; its parser rejects unknown fields.

How to read it depends on the harness:

- `claude`: `herdr agent list` reports `tokens.context` for it.
- `agy`: its statusline prints `Context N%`, read with `herdr pane read <pane-id> --source visible`. This read is also the stall check.
- `opencode`: exposes no context figure. Report that headroom cannot be checked rather than implying it was, and watch for a stall by the pane's tool calls instead.

On crossing the limit: tell the minion to commit and write its handoff, wait for it to settle, close the tab, and spawn a successor seeded with that handoff if work remains.
