# 04: `babysit`, written alongside it

**What to build:** The second skill in the repo, installing by the path 03 proved. The watch loop and nothing else: read the watchlist, check each resource, classify, act within that context's rules, wait the cadence, repeat, in the foreground until everything settles.

`skills/babysit/SKILL.md` plus one reference file per context: `RESOURCES/minion.md` at 15s with the approval allowlist, `RESOURCES/cl.md` at 15 minutes, `RESOURCES/issue.md` at 15 minutes with the dispatcher branch. Babysit writes no code and runs no reviews: when the work needs technical action it calls the Skill tool with `minion`. Five slots, the watchlist at `~/.agents/babysit/<workspace>.md`, and `herdr notification show --sound request` to wake the human.

Leave it for Mihai to review with `writing-for-agents`.

**Blocked by:** 03

**Status:** ready-for-agent

**Type:** task

- [ ] `skills/babysit/SKILL.md` exists with one generic loop, no minion mechanics inlined
- [ ] The three context files carry their own state source, settled states, cadence and permitted actions
- [ ] The approval allowlist and the wake-the-human rule are written as 02 decided
- [ ] The watchlist is read on start, added to on a new resource, and never used for run state
- [ ] Installs into the same throwaway repo for all three harnesses
- [ ] Flagged to Mihai for review with `writing-for-agents`
