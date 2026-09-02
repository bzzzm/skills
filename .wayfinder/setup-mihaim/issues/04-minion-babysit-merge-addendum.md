# 04: Document the two-layer profile merge in `minion` and `babysit`

**What to build:** `minion`'s Profile section and `babysit`'s Slots section currently assume one `AGENTS.local.md`, resolved upward from cwd, full stop. With the global file from ticket 02 in place, that walk can now cross two layers: a repo-local `herdr-minion-profiles`/`minion-settings` block and the global one. State the merge rule decided while charting, repo-local fields override matching global fields, unnamed fields fall through, in both `SKILL.md` files, without duplicating the rule's explanation between them (one owns the definition, the other points at it, or both state it in one shared sentence if that reads better than a cross-reference).

**Blocked by:** 02

**Status:** ready-for-agent

**Type:** task

- [ ] `skills/minion/SKILL.md`'s Profile section states the merge rule
- [ ] `skills/babysit/SKILL.md`'s Slots section states or points at the same rule, not a re-explanation
- [ ] Put through `writing-for-agents`
