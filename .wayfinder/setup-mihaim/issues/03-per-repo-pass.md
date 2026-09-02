# 03: `setup-mihaim`'s per-repo pass

**What to build:** The second half. Run in a repo: install `minion` and `babysit` at project scope if either is missing (`npx skills add ~/work/skills`); check whether that repo's `docs/agents/issue-tracker.md` already redirects to `~/.agents/scratch/<namespace>/`, and skip with a report if it does. Otherwise call the Skill tool with `setup-matt-pocock-skills`, answering its issue-tracker question with **Other** pointing at `~/.agents/scratch/<namespace>/` and its domain-docs question the same way for `~/.agents/docs/<namespace>/`, where `<namespace>` follows `babysit`'s own naming rule (herdr workspace `label`, falling back to the repo name).

Re-running in an already-bootstrapped repo only picks up anything new (a missing `minion`/`babysit` install); it never re-runs the interactive matt-pocock flow unless the user explicitly asks to reconfigure.

**Blocked by:** 02

**Status:** ready-for-agent

**Type:** task

- [ ] `minion`/`babysit` installed at project scope if missing
- [ ] Already-redirected repos are detected and skipped, with a report of what was found
- [ ] A not-yet-redirected repo gets `setup-matt-pocock-skills` driven with `Other` for both the issue tracker and domain docs, pointing at its namespaced `~/.agents/(scratch|docs)/` path
- [ ] The namespace follows `babysit`'s naming rule exactly, collisions surfaced rather than silently overwritten
- [ ] Explicit reconfigure request re-runs the interactive flow; a plain re-run does not
- [ ] Put through `writing-for-agents`
