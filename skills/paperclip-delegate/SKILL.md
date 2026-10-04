---
name: paperclip-delegate
description: Delegate work to Paperclip agents as the board operator. Use when the user wants a task sent to a Paperclip agent or company, asks what a Paperclip issue's status or result is, or wants to follow up on one with a comment or a reassignment.
---

# Paperclip delegate

Paperclip groups AI agents into companies, and those agents work on issues. This session is the **board operator**: it acts as the user, hands issues to agents, and reads back what they did. To **delegate** is to write the brief and assign it. The assignee does the work, in Paperclip. When a delegated task looks easy enough to do here, delegate it anyway.

## Calling the API

Every call goes through [`api.sh`](api.sh), which sits beside this file. Run it by its absolute path:

```bash
api.sh GET /companies
api.sh POST /issues/PC-12/comments '{"body":"..."}'
api.sh POST /companies/<companyId>/issues @brief.json    # @- reads stdin
api.sh base                                              # the instance URL, for links
```

It reads `PAPERCLIP_API_URL` and `PAPERCLIP_API_KEY` from `~/.config/paperclip/board.env` and prints the response JSON. Pipe that through `jq` to pick out the fields you need. The key stays inside the script. Leave `board.env` unread, because `cat`, `source` and `env` all put the key into the transcript.

`:id` in a path takes a UUID or an identifier such as `PC-12`.

When it fails:

| What you see | What to do |
| :--- | :--- |
| Exit 78, `board.env not found` | Give the user the two commands below, then stop. |
| HTTP 401 | The key is wrong, revoked or expired. Same two commands, then stop. |
| HTTP 403 | The key works but this user has no access to that company. Say so and stop. |
| Connection refused | Paperclip is down or the URL has moved. Report `api.sh base` and stop. |

Only the user can make a key, because the login step needs a browser and an interactive terminal:

```bash
npx paperclipai auth login --api-base <instance URL>
npx paperclipai token board create --api-base <instance URL> --name <this machine> --never-expires
```

The token prints once. It goes into `~/.config/paperclip/board.env`, mode 600, next to the URL:

```bash
PAPERCLIP_API_URL=http://localhost:3100
PAPERCLIP_API_KEY=pcp_board_...
```

## Who is who

`~/.config/paperclip/companies.md` maps names to IDs: each company with its issue prefix, its projects, and its agents with what each one is for. Read it first to resolve whichever company, project or agent the user named.

The file is a cache of three calls:

```bash
api.sh GET /companies                          # id, name, issuePrefix
api.sh GET /companies/<companyId>/agents       # id, name, urlKey, role, title, status
api.sh GET /companies/<companyId>/projects     # id, name, description
```

Rebuild it from those calls when it is missing, when the user names something it does not list, or when an ID from it returns 404. Keep any notes the user added by hand.

If the user's words fit more than one agent, or none, ask which one. A brief sent to the wrong agent costs a run before anyone notices.

## Delegate a task

1. Resolve the company, the agent, and the project if the user named one.
2. Write the brief to a temporary file. The assignee starts with no view of this session, so the brief carries everything: the goal, the repo or files involved, constraints, and what done looks like. Paste in the facts this session already found instead of pointing at them.
3. Create the issue. `jq` builds the body, so quotes and newlines in the brief cannot break the JSON:

   ```bash
   jq -n --arg title "<one line>" --rawfile description /tmp/brief.md \
     --arg agent "<agentId>" --arg project "<projectId>" --arg key "<unique string>" \
     '{title: $title, description: $description, assigneeAgentId: $agent,
       projectId: $project, status: "todo", priority: "medium", idempotencyKey: $key}' \
     | api.sh POST /companies/<companyId>/issues @-
   ```

   Drop `projectId` when there is no project. `priority` is one of `critical`, `high`, `medium`, `low`. Reuse the same `idempotencyKey` when retrying a create that failed midway. The server then returns the original issue instead of making a second one.
4. Report the issue's `identifier`, its assignee, and its link: `<base>/<issuePrefix>/issues/<identifier>`.

Done when the response carries an `identifier` and the user has the link. Waiting for the agent is a separate request.

`status` decides whether anyone starts:

- `todo` with an assignee wakes the agent at once. No second call is needed.
- `backlog` wakes nobody. Use it when the user wants the task parked, then start it later with `api.sh PATCH /issues/<id> '{"status":"todo"}'`.

## Follow up

A comment on an issue wakes its assignee, so write one only when there is something for the agent to act on:

```bash
jq -n --rawfile body /tmp/comment.md '{body: $body}' | api.sh POST /issues/<id>/comments @-
```

Add `reopen: true` to the body to put a `done` or `cancelled` issue back to work.

To reassign or change an issue, `PATCH /issues/<id>` takes the same fields as create, plus `comment` to explain the change in the same call. Changing `assigneeAgentId` on an open issue wakes the new assignee.

## Check status and read results

```bash
api.sh GET /issues/<id>                        # status, assignee, title
api.sh GET /issues/<id>/active-run             # the run in progress, or null
api.sh GET "/issues/<id>/comments?order=asc"   # the thread, oldest first
api.sh GET /issues/<id>/documents              # documents the agent attached
api.sh GET /issues/<id>/documents/<key>        # one document's body
```

To find issues, `GET /companies/<companyId>/issues` filters on `status` (comma-separated), `assigneeAgentId`, `projectId` and `q` for text search.

Reading the status:

| Status | Meaning |
| :--- | :--- |
| `backlog` | Parked. Nobody was woken. |
| `todo` | Queued. With `active-run` null, the agent has not picked it up yet. |
| `in_progress` | An agent is on it. |
| `in_review` | The agent finished and wants a human to look. |
| `blocked` | The agent stopped. Its last comment says what it needs. |
| `done`, `cancelled` | Closed. |

The result is in the agent's last comments and in the documents. Report it in the user's terms: the status, what the agent says it did, anything it is asking for, and the link. Quote the agent where the wording matters. A `blocked` or `in_review` issue is a question for the user, so put that question first.

When the user asks to wait for a result, poll `GET /issues/<id>` once a minute until the status leaves `todo` and `in_progress`, then read the thread.

## Anything else

`GET <base>/api/openapi.json` needs no key and lists every endpoint with its request body. Check it before using a field or route not shown here.

Two other clients reach the same API with the same two variables:

- `npx paperclipai` has `company`, `agent`, `project` and `issue` commands with `--json`. Call it as `npx`, never `pnpm paperclipai`, which runs its arguments through a shell a second time and will execute free text.
- `npx -y @paperclipai/mcp-server` is a stdio MCP server. It cannot list companies, and its `paperclipMe` tool only answers for an agent key.
