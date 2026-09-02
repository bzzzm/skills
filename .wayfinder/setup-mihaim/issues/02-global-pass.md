# 02: `setup-mihaim`'s global pass

**What to build:** `skills/setup-mihaim/SKILL.md`, the global half. Run once per machine: probe the tool-path list and the herdr `--kind` list for what's installed, read `~/.agents/.skill-lock.json` for matt-pocock presence and count, write `~/.agents/AGENTS.local.md` to the schema settled while charting (Local Tools & Binary Paths, Harnesses, Matt Pocock skills, the default `herdr-minion-profiles`/`minion-settings` block from ticket 01, a free-form Overrides section), and symlink `~/AGENTS.local.md` to it. Re-running it refreshes the detected sections in place without touching anything a human added under Overrides.

The per-repo pass (ticket 03) is a separate section of the same `SKILL.md` or a separate skill; decide which while writing, but the global pass must be usable and correct on its own first.

**Blocked by:** 01

**Status:** ready-for-agent

**Type:** task

- [ ] `skills/setup-mihaim/SKILL.md` exists, user-invoked, writes `~/.agents/AGENTS.local.md` to the settled schema
- [ ] Tool paths probed from the settled list, harnesses probed from herdr's own `--kind` list, matt-pocock presence and count read from `~/.agents/.skill-lock.json`
- [ ] The default profiles/settings block from ticket 01 is written in
- [ ] `~/AGENTS.local.md` is symlinked to it
- [ ] Re-running it updates detected sections without clobbering a hand-edited Overrides section
- [ ] Put through `writing-for-agents`
