# 05: Run `setup-mihaim` for real, end to end

**What to build:** Use the finished skill on this machine. Global pass against this machine's real state; per-repo pass against `~/work/skills` itself and `~/work/home/mono` (already has its own `AGENTS.local.md`, a real test of the merge from ticket 04, not a fresh-repo case). Confirm the written files are correct, the redirect actually lands where `setup-matt-pocock-skills` writes its docs, and a second run behaves idempotently per ticket 03.

**Blocked by:** 02, 03

**Status:** ready-for-agent

**Type:** task

- [ ] Global pass run on this machine, `~/.agents/AGENTS.local.md` and the `~/AGENTS.local.md` symlink verified
- [ ] Per-repo pass run against `~/work/skills`
- [ ] Per-repo pass run against `~/work/home/mono`, confirming the merge with its existing `AGENTS.local.md` behaves as ticket 04 documents
- [ ] A second run of each pass confirmed idempotent
