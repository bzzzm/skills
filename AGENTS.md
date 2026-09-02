# Conventions

Mihai's own agent skills, in one flat tree, installed into a repo or a harness with `npx skills add ~/work/skills`.

## What lives here

Only skills Mihai wrote. Third-party skills (`herdr`, `unslop`, the `mattpocock/skills` set) are installed into the repos that use them, straight from their sources. A copy pasted in here would go stale with nowhere to send a fix.

## Layout

```
skills/<name>/SKILL.md
```

One directory per skill, flat, no buckets. A skill's own reference files sit beside its `SKILL.md` and are reached by a relative link from it.

Buckets become worth it when the list stops being scannable in one screen, or when one group needs to install differently from the rest. Until then the flat tree costs nothing, and promoting later is a `git mv`.

## Frontmatter

```yaml
---
name: <matches the directory name>
description: <see below>
disable-model-invocation: true   # user-invoked skills only
---
```

Nothing else. The three target harnesses (`claude-code`, `opencode`, `antigravity-cli`) all read a plain `SKILL.md`, so there is no per-harness metadata file to keep in sync.

## Invocation

Every skill is one of two kinds, and the `description` is written for whoever can reach it.

**Model-invoked** is the default: omit `disable-model-invocation`. Model and human can both reach it, and other skills can call it. The `description` is model-facing and carries the trigger branches ("Use when the user wants..., mentions..., asks for...") that fire auto-invocation, so it is worth the tokens it spends in context on every turn.

**User-invoked** costs no context, because you are the index that has to remember the skill exists. Set `disable-model-invocation: true`. Only the human typing its name reaches it. The `description` becomes a one-line human-facing summary for someone browsing slash-commands, with trigger phrasing stripped.

The test for model-invocation is whether the agent could usefully reach for the skill on its own, or another skill needs to. Reuse alone is the reason to extract a skill, not the reason to give it a description.

Nothing but the human fires a user-invoked skill. No skill can, including another user-invoked one. A user-invoked skill may call model-invoked skills freely.

## Depending on another skill

A dependency is an instruction to call the Skill tool by name:

> Call the Skill tool with "grilling".

Never a path into another repo or another skill's folder. Skills here are installed as a set into places whose layout this repo does not control, so a relative path across skills breaks on arrival; the name resolves wherever the skill was installed. Naming the tool is also what gets it fired: dropping a bare `/grilling` into prose leaves the model to read it as a command, and it often reads it as a label instead.

The Skill tool takes one skill per call. A step needing two is two calls: "Call the Skill tool twice, for `grilling` and `domain-modeling`", not "call it with X and Y".

This only works when the target is model-invoked. When a step's precondition is a user-invoked skill, write it as an instruction for the human: "tell the user to run `/setup-home`".

Shared reference lives inside the skill that owns it. Another skill reaches that material by calling the Skill tool with it.

## Writing

Both of these are installed globally in `~/.agents/skills/`, so read them from there when the harness does not expose them as skills:

- Every `SKILL.md` written or edited: `writing-for-agents`, plus its `SKILL-MECHANICS.md`.
- All prose, `README.md` and this file included: `unslop`.

No em dashes anywhere in this repo. Where a sentence reaches for one, use a comma, a colon, or a full stop, whichever the sentence actually wants.
