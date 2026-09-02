# 06: The skill-authoring skill

**What to build:** The skill that writes skills. Asked for a new skill, it scaffolds `skills/<name>/SKILL.md` to whatever `AGENTS.md` says by then, settles the invocation mode with the human rather than guessing, and puts the draft through `writing-for-agents` and `unslop` before calling it done.

Last on the map on purpose. Two real migrations will have bent the conventions, and this skill should encode what they bent them into, not what 01 guessed.

**Blocked by:** 05

**Status:** ready-for-agent

**Type:** task

- [ ] `skills/<authoring-skill-name>/SKILL.md` exists and matches the conventions it enforces
- [ ] It scaffolds a new skill directory with valid frontmatter
- [ ] It settles user-invoked versus model-invoked with the human instead of defaulting silently
- [ ] It runs the draft past `writing-for-agents` and `unslop`
- [ ] Used once to create a real skill, end to end
