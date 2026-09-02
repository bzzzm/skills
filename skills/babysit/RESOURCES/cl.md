# Changelist context

**Cadence:** 15 minutes.

A **changelist** is a proposed change under review: a merge request, a pull request, or whatever the repo's `AGENTS.md` names as its equivalent. Learn how to read one, its state, its pipeline, and its review comments, from `AGENTS.md` and the tooling or skills it names. Do not assume a specific forge.

**Settled** is merged or closed.

**On a failing pipeline or a new review comment**, spawn a minion for it by calling the Skill tool with `minion`, carrying the changelist's identifier, what failed or what the comment asked, and a link back to the changelist. Babysit never fixes a changelist itself.

Anything else about a changelist's state that these rules do not cover escalates through the loop's escalation step.
