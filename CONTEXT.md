# Skills

Mihai's own agent skills. The language below is what these skills mean by their own terms, so a skill written here and a skill read in another repo say the same thing.

## Language

**Skill**:
A directory holding a `SKILL.md` that an agent loads to do one kind of work.
_Avoid_: Command, prompt, plugin

**Model-invoked**:
A skill an agent can reach on its own, and that other skills can call.
_Avoid_: Auto, automatic, implicit

**User-invoked**:
A skill only the human can start, by typing its name.
_Avoid_: Manual, explicit, slash command

## Minions

**Minion**:
An agent started by another agent, running in its own tab, whose work its parent stays responsible for.
_Avoid_: Sub-agent, worker, background agent, delegate

**Harness**:
The CLI program a minion runs as: `agy`, `opencode`, `claude`.
_Avoid_: Kind, tool, client, CLI

**Profile**:
A named harness, model, effort and argument set that a repo declares for its minions to be started with.
_Avoid_: Config, preset, template

**Headroom**:
How much of a minion's context window is still unused.
_Avoid_: Capacity, budget, remaining tokens

**Handoff**:
What a minion writes before it finishes, so its successor or its human can pick the work up.
_Avoid_: Summary, report, notes

## Babysitting

**Babysit**:
Watching resources until they settle, acting only within what each resource's rules allow.
_Avoid_: Monitor, supervise, poll, orchestrate

**Resource**:
Something worth watching: a minion, a changelist, an issue.
_Avoid_: Target, entity, object, job

**Context** (of a babysit run):
The rules for one kind of resource: where its state comes from, what settles it, how often to look, and what may be done about it.
_Avoid_: Type, mode, strategy, handler

**Changelist**:
A proposed change under review, whatever a given repo calls it.
_Avoid_: PR, MR, patch, diff

**Settled**:
A resource has reached a state that ends the watch.
_Avoid_: Finished, complete, resolved, terminal

**Cadence**:
How long to wait before looking at a resource again.
_Avoid_: Interval, frequency, refresh rate, poll rate

**Slot**:
One of the limited places a running minion can occupy.
_Avoid_: Worker, seat, concurrency unit

**Watchlist**:
The standing record of which resources a workspace is being babysat for. It carries no run state.
_Avoid_: Queue, backlog, log, state file
