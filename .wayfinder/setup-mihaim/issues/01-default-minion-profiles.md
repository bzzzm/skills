# 01: The global default `herdr-minion-profiles` block

**What to build:** Not a build, a decision. Pick the actual profiles (names, harness, model, effort) that ship in `~/.agents/AGENTS.local.md`'s default `herdr-minion-profiles` block, plus a default `minion-settings` block (slots, headroom overrides if any). These are Mihai's own real defaults, not guessed placeholders, since every repo without its own override inherits them via the merge decided while charting.

Grill on: which profiles to ship (`coding`, `research`, `debugging`, `review` mirrors mono's, but mono's model choices were mono-specific), what `default_profile` should be, and what `slots` default is right globally versus what `babysit`'s own default (five) already assumes.

**Blocked by:** None (can start immediately)

**Status:** ready-for-agent

**Type:** grilling

- [ ] Profiles list, each with harness/model/effort, decided with Mihai
- [ ] `default_profile` decided
- [ ] `minion-settings` defaults (slots, any headroom override) decided
- [ ] The decision is recorded where ticket 02 will find it
