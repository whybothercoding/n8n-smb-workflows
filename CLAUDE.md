# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

A library of ready-to-import n8n workflow templates for small business automation. No build step, no dependencies — every workflow ships as a raw JSON export plus a README. Users import the JSON directly into their n8n instance.

## Repository Structure

```
workflows/
  <category>/
    <workflow-slug>/
      workflow.json   ← n8n export JSON
      README.md       ← usage documentation
docs/
  how-to-import.md
  credentials-setup.md
```

**Categories:** `crm`, `email`, `social`, `lead-gen`, `reporting`, `newsletter`, `utilities`. Propose a new one in the PR description if none fits.

## Adding or Editing a Workflow

### workflow.json Requirements

- `active: false` — always ship as inactive
- `settings.executionOrder: "v1"`
- `settings.errorWorkflow: "REPLACE_WITH_YOUR_ERROR_WORKFLOW_ID"` — required on all non-utility workflows (the Error Handler utility uses `""` to avoid a circular loop)
- `id` — unique UUID
- Every credential `id` field must use: `"REPLACE_WITH_YOUR_CREDENTIAL_ID"`
- Every raw API token in HTTP Request header values must use a `REPLACE_WITH_YOUR_...` prefixed placeholder (e.g. `"Token REPLACE_WITH_YOUR_BASEROW_API_TOKEN"`)
- Node `id` values must be unique within the file
- Export via n8n: **Workflow menu → Download**, then clean up any instance-specific data (clear `meta.instanceId`)

### README.md Structure (required sections, in order)

1. **H1 title** — workflow name
2. One-line description
3. `## Use Case` — 2–3 sentences: business problem + who uses it
4. `## Required Credentials` — bulleted list of service + what it's used for
5. `## Node Overview` — table: Node name | Type (full `n8n-nodes-base.*` string) | Purpose
6. `## Flow Diagram` — a Mermaid chart between `<!-- FLOW_DIAGRAM:START -->`/`<!-- FLOW_DIAGRAM:END -->` markers, generated from `connections` by `scripts/generate_docs.py`. Never hand-edit the content between the markers — add the empty marker pair when creating a new workflow README, then run the generator.
7. `## Configuration` — numbered list of what to change post-import (IDs, addresses, field names)
8. `## Example` — sample input JSON and description of the output/result

### Root README Table

Generated — do not hand-edit. After adding a workflow, add a `<!-- picker: If you want to… -->` HTML comment to its README (right after the one-line description, before `## Use Case`) describing when to use it, then run `python3 scripts/generate_docs.py` from the repo root. This regenerates the root README's "What's Inside" and "Which Workflow Do I Need?" tables from every `workflow.json` + README pair on disk, and fills in each workflow's `## Flow Diagram`. Commit whatever it changes. CI runs this in `--check` mode and fails the build if the committed docs are stale.

### PR Convention

- Branch: `add/<workflow-slug>`
- Title: `Add: <workflow-slug>`
- One workflow per PR

## Validation

Run before committing any workflow change:

```bash
python3 scripts/generate_docs.py   # regenerate root README tables + Flow Diagrams
bash validate.sh                   # scripts/validate.py under the hood
```

`validate.sh` checks every rule on this page: valid JSON, full envelope (`meta.instanceId`, `pinData`, `staticData`, `tags`, valid UUIDs), `active: false`, `executionOrder: "v1"`, `errorWorkflow` wired, credential-ID placeholders, node-ID/assignment-ID/condition-ID naming convention, declared category, folder layout (no stray JSON outside `<category>/<slug>/workflow.json`), and that the README has all required sections and a root-table entry. Must exit 0 before a PR is opened — CI runs both commands on every push.

## Credential Placeholder Pattern

Any node that uses credentials must have the credential `id` set to `"REPLACE_WITH_YOUR_CREDENTIAL_ID"`. The `name` field can be descriptive (e.g. `"Baserow account"`). For HTTP Request nodes that pass tokens in headers, the header value must also use a `REPLACE_WITH_YOUR_...` prefixed string — not a bare placeholder like `YOUR_TOKEN`. Both patterns are checked by `validate.sh`.

## Workflow Design Conventions (for new workflows)

- Webhook-triggered flows: set `responseMode: "onReceived"` so the form gets an immediate 200
- Use a `Set` node immediately after the trigger to normalise field names before any logic
- Schedule-triggered flows: default to a sensible cron (e.g. Monday 08:00) — importers will adjust
- Keep flows linear where possible; branch only when the use case genuinely requires it
- **OpenAI nodes (`n8n-nodes-base.openAi`):** always set `"simplify": false` at the parameter level. The node defaults to `simplify: true`, which strips the `choices[]` wrapper — any downstream expression referencing `$json.choices[0].message.content` will silently return `undefined` without this flag. This does not apply to `@n8n/n8n-nodes-langchain.*` nodes (e.g. the Agent node) — they have no `simplify` parameter and return their result under `output` instead.

## Standard Service Per Category

Locked so the library stays learnable — one workflow's config transfers to the next instead of every template teaching a different tool for the same job:

- **Team/ops alerts → Discord**, `n8n-nodes-base.discord`, `authentication: "webhook"`, `operation: "sendLegacy"`, message text in the `content` parameter. Never Slack — dropped repo-wide (2026-08-23) because its bot/OAuth setup is real friction for a template a reader is trying to get running in 5 minutes, where Discord's webhook mode is a single copy-pasted URL. Credential type `discordWebhookApi`, name it `"Discord Webhook"`. Message formatting is Discord markdown (`**bold**`), not Slack's (`*bold*`).
- **Structured data storage → Baserow**, `n8n-nodes-base.baserow`. Never Notion — dropped repo-wide (2026-08-23) to avoid two competing "where does this data live" answers across the library; Baserow's row+field model covers both flat CRM rows and the richer per-workflow content Notion pages used to hold (multi-paragraph fields instead of blocks).
- **AI text generation → `n8n-nodes-base.openAi`** (gpt-4o) for a single prompt/response. The `@n8n/n8n-nodes-langchain.agent` + Chat Model pattern (currently only the StackSignal newsletter workflows) is the deliberate exception for genuinely multi-step/agentic work — don't convert plain completion workflows to it just for consistency; that adds a node per workflow for no functional gain, which cuts against "keep flows linear" above.
- **Customer-facing or digest email → SMTP** (`n8n-nodes-base.emailSend`) stays on its own track, not Discord — the recipient there is an end customer or a plain inbox digest, not a team channel, so a chat-platform dependency would be the wrong direction.

If a new workflow's use case doesn't fit an existing category, propose the service choice in the PR description rather than silently introducing a new one-off dependency.

## Node ID and Field Naming Conventions

Follow the established patterns so the repo stays consistent:

- **Node IDs:** `node-{workflow-number}-{purpose}` — e.g. `node-003-openai`, `node-007-if`
- **Assignment IDs** (inside Set nodes): `assign-{workflow-number}-{sequence}` — e.g. `assign-003-001`
- **Condition IDs** (inside IF nodes): `cond-{workflow-number}-{sequence}` — e.g. `cond-004-001`
- **Workflow number** is the three-digit sequence from the `id` field (e.g. `0003` → `003`)

## Required JSON Envelope Fields

Every `workflow.json` must include these top-level fields (beyond nodes/connections):

```json
{
  "id": "<uuid>",
  "meta": { "instanceId": "", "templateCredsSetupCompleted": true },
  "name": "...",
  "pinData": {},
  "staticData": null,
  "tags": [{ "name": "<category>" }],
  "active": false,
  "settings": { "executionOrder": "v1", "errorWorkflow": "..." },
  "versionId": "<uuid>"
}
```

`instanceId` must be an empty string (never a real instance ID). `tags` must include an entry for the workflow's category slug.

**Tag shape matters for real imports, not just validation.** `tags` must be `{"name": "..."}` objects — never bare strings, never a real export's full tag record (`{"id": ..., "createdAt": ..., ...}`). n8n's `import:workflow` CLI resolves each tag by calling `TagRepository.setTags`, which finds-or-creates a `tag_entity` row by `name` and only then knows the tag's real `id` for the `workflows_tags` join-table insert. A bare string has no `.name`, so `setTags` silently skips it and the later insert writes `tagId: undefined` — `SQLITE_CONSTRAINT: NOT NULL constraint failed: workflows_tags.tagId`, and the import fails outright. This is exactly the kind of defect `validate.sh`'s field checks can't catch (the JSON is well-formed) but the CI's Docker-based n8n import check does — see [How This Repo Is Tested](README.md#how-this-repo-is-tested).
