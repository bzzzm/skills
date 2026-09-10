# skills

My agent skills. One flat tree of `SKILL.md` files that any repo or harness can install from, so a skill I write once is not stuck in the repo I happened to write it in.

Only my own skills live here. Third-party ones I use get installed from their own sources.

## Install

From inside the repo you want them in:

```bash
npx skills add ~/work/skills
```

That installs at project scope. Commit what it writes: a consuming repo owns its copy, so tweaking a skill for one project does not mean porting the change back the same day.

Add `-g` instead to install into the global skill directories (`~/.claude/skills`, `~/.config/opencode/skills`, `~/.gemini/antigravity-cli/skills`).

Pick individual skills with `--skill <name>`, or see what is on offer without installing:

```bash
npx skills add ~/work/skills --list
```

### Installing from a local path

`npx skills add ~/work/skills` records the skill in the consuming repo's `skills-lock.json` with `sourceType: "local"` and a relative `source` path back to this repo. It writes the skill once to a universal location (`.agents/skills/<name>`), and symlinks it into any harness-specific directory that needs one, `.claude/skills/<name>` for Claude Code.

`npx skills update` does not follow a local path: it reports "No project skills to update" even after the source file has changed underneath it. Pulling in a change made here means reinstalling (`npx skills add ~/work/skills --skill <name>`) in the consuming repo.

## Skills

- `minion`: start, work with, and close a Herdr minion.
- `babysit`: watch a minion, a changelist, or an issue until it settles, spawning a minion for anything that needs technical action.
- `diagrams`: draw architecture diagrams and flowcharts as PNG and SVG with the Python `diagrams` library.

## Working in this repo

[AGENTS.md](./AGENTS.md) has the conventions: layout, frontmatter, when a skill is user-invoked, and how one skill depends on another. `CLAUDE.md` is a symlink to it.
