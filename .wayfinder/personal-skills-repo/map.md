# Personal skills repo

## Destination

`~/work/skills` is the single source of truth for Mihai's own agent skills: a flat `skills/<name>/SKILL.md` tree with its conventions written down, installable into any repo or harness with `npx skills add ~/work/skills`. Reaching the end means `minion` and `babysit` live here, mono consumes them from here at project scope and drops `agent-workflow` and `minion-manager`, and a skill-authoring skill exists that writes new skills to these conventions.

## Notes

**Domain**: a personal agent-skills repo, modelled on `mattpocock/skills` (cloned to `.scratch/mattpocock-skills`) but stripped of the machinery that only a publisher needs.

**This map carries execution.** The destination is a built repo, not a decision, so tickets that say "write" do the work rather than plan it. Only the boundary ticket was a pure decision.

**Skills every session should consult**:
- `writing-for-agents` for every `SKILL.md` written or edited (Mihai reviews the new skills with it).
- `unslop` for all prose, including `README.md` and `AGENTS.md`.
- `grilling` and `domain-modeling` when in doubt.

All four are installed globally in `~/.agents/skills/`, along with 36 others.

**Standing preferences, decided while charting**:
- Flat layout: `skills/<name>/`. No buckets until the count justifies them; promoting later is a `git mv`.
- Harnesses: `claude-code`, `opencode`, `antigravity-cli` (`agy`). All three read a plain `SKILL.md`, so no `agents/openai.yaml`.
- Only Mihai's own skills live here. Third-party skills (`herdr`, `unslop`, the 22 from `mattpocock/skills`) are installed, never vendored.
- Consuming repos install at **project** scope and commit the result, so a local tweak in one repo does not force an immediate port back.
- Conventions doc is `AGENTS.md` with a `CLAUDE.md` symlink.
- No `docs/` pages, no changesets, no plugin manifests.

**Facts already established**:
- `npx skills` v1.5.23 accepts local paths, any git URL, and private repos over existing git credentials. `-g` installs to `~/<agent>/skills/`; symlinking is the default method.
- `~/.agents/skills/` holds 40 globally installed skills and a `.skill-lock.json`. The harness-specific global dirs (`~/.claude/skills/`, `~/.config/opencode/skills/`, `~/.gemini/antigravity-cli/skills/`) do not exist.
- Herdr exposes minion control twice: an MCP server (`herdr-mcp`, Go, built from `source.lan/home/mono/src/mcp/herdr`) and the `herdr` CLI. The new skills use the CLI only. `herdr_minion_spawn` puts every minion in one shared `minions` tab, which is what tab-per-minion replaces.
- `herdr agent list` reports `tokens.context` for claude agents only. agy prints `Context N%` in its own statusline, readable with `herdr pane read --source visible`. opencode reports neither.
- Herdr workspaces carry real names (`skills`, `home/mono`, `pcc-cla`), not just ids.
- mono keeps real directories in `.agents/skills/` and symlinks them from `.claude/skills/`. Its `skills-lock.json` tracks 22 skills from `mattpocock/skills` and `herdr` from `herdrdev/herdr`.
- No `gh` CLI on this machine, and anonymous GitHub HTTPS clones fail. `tea` 0.15.1 is installed for Gitea.

## Decisions so far

<!-- one line per closed ticket -->

- **01**: `skills/` is flat, `AGENTS.md` holds the conventions with `CLAUDE.md` symlinked to it, `README.md` covers purpose and install.
- **02**: the two mono skills are not migrated. `minion` (one minion, tab per minion, CLI only) and `babysit` (one watch loop, one reference file per resource context) get written instead, and the decision in full lives at the foot of the ticket.

## Not yet specified

- **Which further personal skills to write.** The inventory conversation Mihai flagged for after the scaffold exists. Likely to graduate into several tickets once the conventions are proven by `minion` and `babysit`.
- **Publishing.** Local-path install is the route for now; Gitea (mono already uses one) or a private GitHub repo is the backup. Graduates if a second machine or another person needs these skills. A Claude Code plugin manifest only becomes possible once there is a remote.
- **Whether mono's five repo-coupled skills ever come back.** `arch`, `helm-manager`, `homeassistant`, `kubernetes` and `setup-home` stay in mono for now. If a second cluster or a second home repo appears, the portability question reopens.

## Out of scope

- Vendoring third-party skills into this repo. Ruled out by "host only my skills"; they are installed from their sources.
- Codex support and the per-skill `agents/openai.yaml`. Not one of the three target harnesses.
- Publisher machinery: `docs/` pages, changesets, `CHANGELOG.md`, `.claude-plugin/` manifests. These exist in `mattpocock/skills` because it ships to an audience.
