# 05: mono cuts over

**What to build:** The point where "source of truth" stops being a claim. `home/mono` drops `agent-workflow` and `minion-manager` and consumes `minion` and `babysit` from `~/work/skills` instead, at project scope so a local tweak there never forces an immediate port back.

Install into `~/work/home/mono` for `claude-code`, `opencode` and `antigravity-cli`, delete the superseded `agent-workflow` and `minion-manager` directories, and confirm `.claude/skills/` symlinks still resolve. Whatever mono still needs from those two (the monorepo table, the operational references, ticket intake, the repository preamble) moves into mono's own `AGENTS.md` or a mono-only skill before they go.

The trap to avoid: mono's five repo-coupled skills (`arch`, `helm-manager`, `homeassistant`, `kubernetes`, `setup-home`) and its 22 vendored `mattpocock/skills` entries plus `herdr` must come through untouched.

**Blocked by:** 04

**Status:** ready-for-agent

**Type:** task

- [ ] `minion` and `babysit` installed into mono at project scope for all three harnesses
- [ ] mono's `agent-workflow` and `minion-manager` directories are gone, with anything mono-specific they held rehoused in mono first
- [ ] `.claude/skills/` symlinks resolve
- [ ] The other 27 skills in mono are unchanged, and `skills-lock.json` still tracks them
- [ ] The install commands are recorded in this repo's `README.md`
