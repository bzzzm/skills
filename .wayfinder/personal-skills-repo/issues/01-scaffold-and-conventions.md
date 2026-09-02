# 01: Scaffold and conventions

**What to build:** An empty but opinionated repo that a skill can land in. Someone cloning `~/work/skills` can read what a skill here looks like, and the `skills` CLI can already see the tree.

Write `AGENTS.md` as the conventions doc: the flat `skills/<name>/` layout and what would justify buckets later, the frontmatter rules (`name`, `description`, and when `disable-model-invocation: true` applies), the user-invoked versus model-invoked split and how the `description` differs between the two, that only Mihai's own skills live here, and that a dependency on another skill is written as an instruction to call the Skill tool rather than a path into another repo. `CLAUDE.md` is a symlink to it. `README.md` says what the repo is, how to install from it, and lists the skills.

`.scratch/mattpocock-skills/.agents/invocation.md` is the reference for the invocation axis. Take the rule, leave the publisher scaffolding.

**Blocked by:** None (can start immediately)

**Status:** ready-for-agent

**Type:** task

- [x] `skills/` exists as a flat tree, one directory per skill
- [x] `AGENTS.md` covers layout, frontmatter, invocation modes, the own-skills-only rule, and cross-skill dependencies
- [x] `CLAUDE.md` is a symlink to `AGENTS.md`
- [x] `README.md` states the purpose, the install command, and the skill list
- [x] `npx skills add ~/work/skills --list` runs against the tree without error
- [x] Every prose file has been through `writing-for-agents` and `unslop`
