# 03: `minion`, written and installed end to end

**What to build:** The first complete path through every layer. `skills/minion/SKILL.md` is written to the decision in 02, and an agent in a fresh repo can actually reach it.

One minion, end to end: what a minion is, one tab per minion at the end of the current workspace's tab list, profile resolution from `AGENTS.local.md` with the harness adapter table, prompt composition including the handoff instruction, follow-up and interrupt, the context headroom check, and teardown that verifies the artifact first. Herdr is reached through the CLI only, with `herdr` called as a skill for its syntax. No `home/mono`, no `kornel-cluster`, no monorepo navigation, no ticket intake.

Then install it at project scope into a throwaway repo for `claude-code`, `opencode` and `antigravity-cli`, and confirm each harness resolves it.

While installing, establish what the `skills` CLI does with a local-path source: whether `skills-lock.json` gains an entry, what `sourceType` it records, and whether `npx skills update` can follow a local path. Those answers go in the README, because every later install depends on them.

Leave the skill for Mihai to review with `writing-for-agents`; a skill that installs is not a finished skill.

**Blocked by:** 01, 02

**Status:** ready-for-review

**Type:** task

- [x] `skills/minion/SKILL.md` exists, honouring the decision in 02, with no `home/mono` or `kornel-cluster` references
- [x] Tab-per-minion, profile translation, handoff instruction, headroom check and verified teardown are all in it
- [x] Installed at project scope into a throwaway repo for all three harnesses, each resolving the skill
- [x] The local-path install behaviour (lockfile entry, `sourceType`, `update` support) is documented in `README.md`
- [x] Flagged to Mihai for review with `writing-for-agents`
