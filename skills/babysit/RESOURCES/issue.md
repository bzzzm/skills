# Issue context

**Cadence:** 15 minutes.

Learn how issues work in this repo from `AGENTS.md` and `AGENTS.local.md` and the skills they name: where they live, what state they carry, and what marks one ready for an agent to pick up. No tracker is hardcoded here.

**Given one issue**, watch its state.

**Settled** is whatever that repo's issue tracking calls resolved or closed.

**Given a query or a map** instead of one issue, dispatch: find every issue it currently marks ready, and spawn a minion per ready issue by calling the Skill tool with `minion`, subject to the loop's slot cap on how many run at once.

Anything an issue's state raises that these rules do not cover escalates through the loop's escalation step.
