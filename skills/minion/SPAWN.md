# Spawning a minion

## Name

The herdr agent name and the tab label are the same string: `minion-<ticket>-<harness>`, with the ticket segment dropped when there is no ticket (`minion-agy`). On a collision with a live agent name, append `-2`, then `-3`. Truncate to fit `[a-z][a-z0-9_-]{0,31}`, trimming the ticket segment first.

## Profile

Check for `herdr-minion-profiles` in `AGENTS.local.md`, resolved upward from the working directory. It names `default_profile` and a `profiles` map; each profile requires `harness` and may carry `model`, `effort`, `agent`, and `args`. If the workflow names a profile, use that; otherwise use `default_profile`.

If `AGENTS.local.md` is absent or lacks the block, and the human did not specify harness and settings in the prompt, ask the human immediately. Do not explore the filesystem, read unrelated config files, or probe running agents to infer a profile.

Translate the profile's portable fields to native flags for the chosen harness:

| Harness | `model` | `effort` | `agent` | auto-edit flag |
| :--- | :--- | :--- | :--- | :--- |
| `claude` | `--model` | not supported; put it in `args` if the model name should encode it | `--agent` | `--permission-mode acceptEdits` |
| `agy` | `--model` | `--effort` (`low`, `medium`, `high`) | `--agent` | `--mode accept-edits` |
| `opencode` | `--model` | `--variant` | `--agent` | `--auto` (approves every permission, not only edits; there is no edits-only flag) |

For a harness not in this table, or a portable field this table marks unsupported, put the native flags in the profile's `args` instead of guessing a mapping. Every minion starts in auto-edit mode: always include that harness's flag.

Auto-edit covers edits, not every prompt. A minion still parks on approvals its work depends on, network fetches above all, and it parks silently. One whose whole job is reading primary sources stops on the first domain it reaches, then on every further one. Decide before spawning who clears them: a babysit loop watching the minion answers read-only fetch prompts on its own, and that is the default answer. The alternative is a blanket auto-approve in the profile's `args` (`agy --dangerously-skip-permissions`), which covers writes and shell too, so it belongs only to a profile the human has chosen for it.

## Start

```bash
herdr tab create --workspace "$HERDR_WORKSPACE_ID" --label <name> --cwd <path> --no-focus
```

Read the pane ID from `.result.root_pane.pane_id`; the tab opens at an interactive shell prompt.

```bash
herdr agent start <name> --kind <harness> --pane <pane-id> -- <native flags>
```

Then compose and send the prompt:

```bash
herdr agent prompt <name> "<prompt>" --wait
```

## Prompt composition

Everything below goes into the prompt. A minion does what the prompt asks and nothing beside it; whatever you leave to its initiative comes back inconsistent across a batch.

1. **The task**, and the ticket reference if there is one.
2. **Environment context:** any active virtualenv (`.venv`), interpreter path, runtime version, or service endpoints the minion must use.
3. **The acceptance criteria** the minion is working against.
4. **Fence the search space.** Name the files, directories, or sources that are in scope, and say where the answer does not live. Point at source directories and keep compiled bundles and build output out of scope: recursive search through build artifacts is the classic sink that eats a whole turn. When the question is how a deployed thing behaves, point at the running instance (`docker exec <container> sed -n ...`) so the answer describes the installed version rather than upstream `main`.
5. **Checkpoint to disk.** The minion creates its output file first, with the questions or sections as headings, then fills each one in as that answer lands. Work held only in the minion's context dies with the turn: one interrupt and every unwritten finding is gone.
6. **Ground every claim.** A primary source per claim, cited as a URL or `file:line`, and an explicit statement of what it could not verify. This is what keeps a report free of extrapolation, and it is worth the words every time.
7. **What is already decided.** The map, the ADRs, the options ruled out. A minion that does not know a path is excluded will spend its turn proposing it.
8. **Every artifact, listed.** The report path, the ticket's `## Answer` and `Status:`, the pointer in the map's decisions, and a handoff path unique to this minion (`~/.agents/handoff/<ticket>-handoff.md`, `<map>-handoff.md`, or `<workspace>-handoff.md`; minions launched in parallel on one shared path overwrite each other). Name each one: a minion left to infer the repo's conventions finds some of them and misses the rest. Where the repo has a `handoff` skill installed, tell the minion to use it instead of writing the file freehand.
