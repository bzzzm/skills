# Minion context

**Cadence:** 15s.

**State.** One call covers every watched minion at once:

```bash
herdr tab list --workspace "$HERDR_WORKSPACE_ID"
```

Filter to tabs labelled `minion-*`. Each tab's `agent_status` is the minion's state.

**Settled** is `idle` or `done`.

**On `blocked`**, read the buffer:

```bash
herdr agent read <name> --source recent-unwrapped --lines 120
```

Answer it yourself only when the whole command Herdr is asking to run is a single invocation of one of these read-only binaries, with no shell metacharacter (pipe, redirect, `&&`, `;`, backtick, `$(...)`) anywhere in it:

`echo`, `pwd`, `ls`, `cat`, `head`, `tail`, `wc`, `stat`, `file`, `find` (without `-exec` or `-delete`), `grep`, `rg`, `ps`, `date`, `env`, `which`, `git status`, `git log`, `git diff`, `git show`, `go doc`.

Also answer a harness UI prompt that carries no shell command at all: an edit-mode toggle, a "continue?" confirmation, a dismissal.

Anything else escalates: leave it blocked and use the loop's escalation step, naming the minion and what it is asking.

**Context headroom** is never a directed extra read on this cadence. Note it only when a read already done for another reason on this minion (answering a blocked prompt, or a read the user asked for) happens to carry it, using the per-harness method from the `minion` skill, call the Skill tool with `minion` for that.
