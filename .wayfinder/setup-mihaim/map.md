# Setup Mihaim

## Destination

`/setup-mihaim` exists: a user-invoked skill in `~/work/skills` with two passes. The **global pass**, run once per machine, writes `~/.agents/AGENTS.local.md` (detected tool paths, detected harnesses, matt-pocock skill status, a default `herdr-minion-profiles`/`minion-settings` block) and symlinks it from `~/AGENTS.local.md`. The **per-repo pass**, run once per repo and safe to re-run, installs `minion`/`babysit` at project scope if missing, and redirects that repo's matt-pocock issue-tracker and domain-doc output to its namespaced slice of `~/.agents/(scratch|docs)/` instead of the repo itself, idempotently.

## Notes

**Domain**: a personal setup/onboarding skill, loosely modelled on `srv/cosmos`'s `setup-cosmos` (audit host tooling, write a local config file) but without its version-pinning and drift-remediation machinery, which doesn't apply here.

**This map carries execution**, same as `personal-skills-repo`: the destination is a built skill, not a decision, so tickets that say "write" do the work.

**Skills every session should consult**: `writing-for-agents` for the `SKILL.md`, `unslop` for prose, `grilling` and `domain-modeling` when in doubt. All installed globally in `~/.agents/skills/`.

**Where this lives**: `skills/setup-mihaim/SKILL.md` in `~/work/skills`, same repo and conventions as `minion`/`babysit`. User-invoked (`disable-model-invocation: true`), matching every other `setup-*` skill found on this machine.

**Standing preferences, decided while charting**:
- Global file: `~/.agents/AGENTS.local.md` is the source of truth; `~/AGENTS.local.md` is a symlink to it, so the upward-directory-walk resolution `minion` and mono's `AGENTS.local.md` already use finds it without any change to those skills.
- Per-repo profile resolution is a **merge**, not a shadow: a repo-local `herdr-minion-profiles`/`minion-settings` block overrides only the fields it names; anything it doesn't name falls through to the global block. `minion` and `babysit` don't say this yet (see ticket 04).
- Per-repo namespace under `~/.agents/(scratch|docs)/`: reuse `babysit`'s existing rule verbatim (herdr workspace `label`, falling back to the repo name). Two differently-pathed repos sharing a bare name can collide outside Herdr; surface that rather than silently overwriting.
- Redirect mechanism: the per-repo pass drives `setup-matt-pocock-skills` and answers its issue-tracker question with **Other**, supplying the namespaced path; the same redirect covers its domain-docs question (`CONTEXT.md`/`docs/adr/`). No change needed to that skill itself.
- Matt-pocock detection: read `~/.agents/.skill-lock.json` for entries with `source: "mattpocock/skills"` (37 present as of charting); presence of `setup-matt-pocock-skills` itself is the fast yes/no, the count rides along free.
- Harness detection is dynamic, probed from herdr's own `--kind` list (`pi`, `claude`, `codex`, `gemini`, `cursor`, `devin`, `agy`, `cline`, `omp`, `mastracode`, `opencode`, `copilot`, `kimi`, `kiro`, `droid`, `amp`, `grok`, `hermes`, `kilo`, `qodercli`, `qwen`, `maki`), never a hand-picked subset that can go stale against it.
- Tool-path probe list: `herdr`, `herdr-mcp`, `nvim`, `git`, `node`, `npm`, `python3`, `uv`, `tea`.
- `AGENTS.local.md` schema: `Local Tools & Binary Paths`, `Harnesses`, `Matt Pocock skills`, the default `herdr-minion-profiles`/`minion-settings` block, and a free-form `Overrides` section for anything else, rather than a closed schema.
- The per-repo pass is idempotent: a repo whose `docs/agents/issue-tracker.md` already points at `~/.agents/...` is skipped and reported, not re-run interactively, unless the user explicitly asks to reconfigure it.
- No version pinning or drift remediation, unlike `setup-cosmos`: nothing in this suite pins tool versions.

## Decisions so far

<!-- one line per closed ticket -->

## Not yet specified

- **Doctor / health-check mode.** A read-only report of what's missing, no writes. Real, not needed for a first working version.
- **`.herdr/workspace.yml` scaffolding per repo**, mirroring mono's layout. Graduates once the two passes above exist and prove out.

## Out of scope

- Version pinning and drift remediation against a canonical tool-version table, `setup-cosmos`'s model. Ruled out while charting: nothing here pins versions.
- MCP secrets / `.env` scaffolding. This suite carries no MCP secrets today.
