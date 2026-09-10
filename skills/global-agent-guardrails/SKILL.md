---
name: global-agent-guardrails
description: 'One shared denylist of catastrophic shell commands (rm -rf on / or ~, dd/mkfs, sudo rm, fork bombs, curl|sh, git push --force, gh repo delete) enforced as a PreToolUse/pre-exec guard across every AI coding agent on the machine: Cursor, Claude Code, Codex, Antigravity, OpenCode, Pi, Hermes, Grok, Droid, Devin. Use when adding or tuning blocked-command patterns, wiring the guard into a new agent or a new machine, debugging why a command was (or was not) blocked, or when the user mentions command guard, guardrails, dangerous command hook, or PreToolUse safety.'
---

# Global Agent Guardrails

A "bouncer" that blocks catastrophic shell commands before any AI agent runs them. One patterns file is the single source of truth; every agent reads it via a shared hook script or a tiny native adapter. It is a seatbelt against accidents, NOT a sandbox against a malicious agent (obfuscation like `python -c "shutil.rmtree(...)"` can slip past regex).

## File map

```
hooks/                                   # THIS SKILL: the shipped copies, the source of truth
~/.agents/hooks/dangerous-patterns.txt   # THE denylist: one POSIX-ERE regex per line, # comments
~/.agents/hooks/deny-dangerous.sh        # shared guard: hook JSON on stdin -> blocks per mode arg
~/.agents/hooks/test-guard.sh            # test suite: run after ANY pattern change
~/.config/opencode/plugins/command-guard.ts   # OpenCode adapter (throws to block)
~/.pi/agent/extensions/command-guard.ts       # Pi adapter (returns {block:true})
~/.hermes/plugins/command-guard/              # Hermes plugin (returns {"action":"block"})
```

The three files under [`hooks/`](hooks/) in this skill are what `~/.agents/hooks/` gets installed from. Tune the pattern list there and copy it out, so the deployed copy and the shipped one stay one file.

## State check (is it installed?)

```bash
ls ~/.agents/hooks/deny-dangerous.sh ~/.agents/hooks/dangerous-patterns.txt
~/.agents/hooks/test-guard.sh   # must end "failed: 0"
```

Install or restore the scripts from this skill, then wire the agents up from the table below:

```bash
mkdir -p ~/.agents/hooks && cp hooks/* ~/.agents/hooks/ && chmod +x ~/.agents/hooks/*.sh
~/.agents/hooks/test-guard.sh
```

## Add or tune a pattern

1. Edit `hooks/dangerous-patterns.txt` in this skill, the copy every machine installs from. Write POSIX ERE (`grep -E`). Use `[[:space:]]`, never `\s`: adapters auto-convert `[:space:]` to `\s` for JS/Python and compile in multiline mode.
2. Add block + allow cases to `hooks/test-guard.sh`, install both with the command above, then run `~/.agents/hooks/test-guard.sh`. Must pass 100%.
3. Verify the new pattern compiles in the adapter engines:

```bash
python3 -c 'import re,pathlib; [re.compile(l.strip().replace("[:space:]",r"\s"),re.M) for l in pathlib.Path.home().joinpath(".agents/hooks/dangerous-patterns.txt").read_text().splitlines() if l.strip() and not l.startswith("#")]; print("ok")'
```

4. Changes apply instantly everywhere (all consumers re-read the file per command). Exception: Droid uses its own `commandBlocklist` in `~/.factory/settings.json`, so mirror the change there manually.

Design rule: block only irreversible/catastrophic commands (data loss, disk wipe, repo deletion, token exfil). Local-destructive-but-recoverable commands (`git status`, `git clean -fdx`, `rm -rf node_modules`) stay ALLOWED, because over-blocking kills agent usefulness.

Password managers are also a hard NO (pattern group 10): agents must never use their CLIs (`bw`, `bws`, `lpass`, `keepassxc-cli`, `rbw`, `nordpass` outright; `pass` with any argument at command position; `op` with its real subcommands; bare `op`/`pass` stay unblocked because they are common words), dump the macOS keychain (`security find-*-password`, `dump-keychain`), export gpg secret keys, touch vault data (`~/.password-store`, the `.app` bundles), or open/uninstall the apps.

## Per-agent wiring (user-global)

| Agent | Config | Event | Blocks via |
|---|---|---|---|
| Claude Code | `~/.claude/settings.json` | `PreToolUse` matcher `Bash` | shared script, exit 2 |
| Codex CLI/app/IDE | `~/.codex/hooks.json` | `PreToolUse` matcher `Bash` | shared script, exit 2 |
| Cursor IDE + CLI | `~/.cursor/hooks.json` | `beforeShellExecution` | shared script with `cursor` arg, deny JSON |
| Antigravity CLI + IDE + app | `~/.gemini/config/hooks.json` | `PreToolUse` matcher `run_command` | shared script with `antigravity` arg, deny JSON |
| Grok (xAI) | auto-loads Claude + Cursor hook files (compat on by default); native option `~/.grok/hooks/*.json` | `PreToolUse` | shared script (reads `.toolInput.command`) |
| OpenCode | `~/.config/opencode/plugins/command-guard.ts` | `tool.execute.before` | adapter throws Error |
| Pi | `~/.pi/agent/extensions/command-guard.ts` | `pi.on("tool_call")` | adapter returns `{block:true}` |
| Hermes | `~/.hermes/plugins/command-guard/` (`plugin.yaml` + `__init__.py`) | `pre_tool_call` hook | plugin returns `{"action":"block"}` |
| Droid (Factory) | `~/.factory/settings.json` | native `commandBlocklist` | hard-block, no approval possible |
| Devin CLI | `~/.config/devin/config.json` | `PreToolUse` matcher `^exec$` | shared script, exit 2 |

Hook entry shape for Claude/Codex/Devin (merge into existing `hooks` object, never overwrite):

```json
{"hooks": {"PreToolUse": [{"matcher": "Bash", "hooks": [{"type": "command", "command": "/ABSOLUTE/HOME/.agents/hooks/deny-dangerous.sh"}]}]}}
```

Cursor entry (payload has `.command`, so pass the `cursor` arg):

```json
{"beforeShellExecution": [{"command": "/ABSOLUTE/HOME/.agents/hooks/deny-dangerous.sh cursor", "failClosed": false}]}
```

Antigravity entry, where the top level is a hook NAME of your choosing, not an event, and the whole file is one object of them:

```json
{"command-guard": {"PreToolUse": [{"matcher": "run_command", "hooks": [{"type": "command", "command": "/ABSOLUTE/HOME/.agents/hooks/deny-dangerous.sh antigravity", "timeout": 10}]}]}}
```

Use absolute paths in configs (`~` expansion is inconsistent across agents).

## Gotchas (hard-won, do not rediscover)

- **Codex trust is hash-pinned.** Any edit to the hook ENTRY in `hooks.json` (not the patterns file) invalidates trust; run `/hooks` in Codex and re-trust, else Codex silently skips the guard. Trust hashes live in `[hooks.state]` in `~/.codex/config.toml` and are shared by CLI, desktop app, and IDE extension. CI/scripts: `--dangerously-bypass-hook-trust`.
- **Cursor `failClosed` must stay `false`.** Cursor background/worker hosts cannot execute hook scripts; fail-closed blocks EVERY command there. Trade-off: Cursor background agents run unguarded.
- **Hermes plugin manifest key is `provides_hooks`** (not `hooks`). Plugin must be enabled: `plugins.enabled` list in `~/.hermes/config.yaml` (the `hermes plugins enable` CLI prompts interactively and hangs non-interactive shells). Hermes hooks are fail-open on exceptions, so keep the plugin trivial. Shell tool name is `terminal`.
- **Antigravity fails CLOSED, alone among the hook harnesses.** A crash, a timeout, a non-zero exit or stdout it cannot parse all read as `deny`, so a broken guard bricks every command. Every path in `antigravity` mode therefore prints a verdict and exits 0, stdout carries the verdict and nothing else, and debug output goes to stderr. Test with `test-guard.sh` (it asserts exit 0 and parseable stdout on all three shapes) before trusting an edit.
- **Antigravity `~/.gemini/config/hooks.json` covers CLI, IDE and app** from one file. The workspace-level `.agents/hooks.json` is separate and gated on folder trust, so leave the guard global. Denial vocabulary is richer than allow/deny (`ask`, `force_ask`, `deny_unless_prior_grant`); the guard uses plain `deny` because catastrophic commands should not be approvable.
- **Pi `tool_call` handler errors block the tool** (fail-safe), so the adapter must catch its own errors and fail open, or a broken patterns file bricks every bash call.
- **Droid semantics:** `commandDenylist` = ask for confirmation; `commandBlocklist` = never runs, even at full autonomy with `--skip-permissions-unsafe`. Use blocklist for catastrophic entries.
- **Guard script payload detection:** command lives at `.tool_input.command` (Claude/Codex/Devin), `.toolInput.command` (Grok), `.command` (Cursor), `.toolCall.args.CommandLine` (Antigravity). Keep all four in the jq fallback chain.
- **Adapter regexes require multiline mode.** Keep JavaScript's `m` flag and Python's `re.M` so `^` matches each shell line like `grep`.
- **False-positive class:** a harmless command whose ARGUMENT text contains a dangerous-looking string (e.g. passing a prompt mentioning `git push --force` on a CLI) gets blocked. Workaround: put the text in a file and reference it.
- **Not coverable natively (no hook system as of 2026-07):** Gemini CLI, Qwen Code, Amp, kimi-cli. Codex cloud tasks and Cursor background agents also bypass the local guard.

## E2E verification recipe

Safe probe: ask the agent to run `git push --force` from a NON-git directory: blocked = guard works; "not a git repository" = guard failed but no harm done.

```bash
cd "$(mktemp -d)"
claude -p 'Run exactly: git push --force. Report the result in one line.' --permission-mode bypassPermissions
codex exec --skip-git-repo-check 'Run exactly: git push --force. Report the result in one line.' < /dev/null
droid exec --auto high -f prompt.txt        # prompt text in a file (see false-positive gotcha)
agy -p "$(cat prompt.txt)" --dangerously-skip-permissions   # headless agy auto-denies every tool without this
pi -p --no-session 'Run exactly: git push --force. Report the result in one line.'
hermes chat --query 'Run exactly this terminal command: git push --force. Report in one line.'
```

Direct script test without any agent:

```bash
echo '{"tool_input":{"command":"rm -rf /"}}' | ~/.agents/hooks/deny-dangerous.sh; echo "exit=$?"   # expect exit=2
echo '{"toolCall":{"args":{"CommandLine":"rm -rf /"}}}' | ~/.agents/hooks/deny-dangerous.sh antigravity   # expect {"decision":"deny",...}
```
