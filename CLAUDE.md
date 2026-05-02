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

**Categories:** `crm`, `email`, `social`, `lead-gen`, `reporting`, `utilities`. Propose a new one in the PR description if none fits.

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
6. `## Configuration` — numbered list of what to change post-import (IDs, addresses, field names)
7. `## Example` — sample input JSON and description of the output/result

### Root README Table

When adding a workflow, append a row to the "What's Inside" table in `README.md`:
```
| N | [Workflow Name](workflows/<category>/<slug>/) | Category | One-line description |
```

### PR Convention

- Branch: `add/<workflow-slug>`
- Title: `Add: <workflow-slug>`
- One workflow per PR

## Validation

Run before committing any workflow change:

```bash
bash validate.sh
```

Checks all `workflow.json` files for: valid JSON, required fields, `active: false`, `executionOrder: v1`, `errorWorkflow` present, no raw API tokens in headers. Must exit 0 before a PR is opened.

## Credential Placeholder Pattern

Any node that uses credentials must have the credential `id` set to `"REPLACE_WITH_YOUR_CREDENTIAL_ID"`. The `name` field can be descriptive (e.g. `"Baserow account"`). For HTTP Request nodes that pass tokens in headers, the header value must also use a `REPLACE_WITH_YOUR_...` prefixed string — not a bare placeholder like `YOUR_TOKEN`. Both patterns are checked by `validate.sh`.

## Workflow Design Conventions (for new workflows)

- Webhook-triggered flows: set `responseMode: "onReceived"` so the form gets an immediate 200
- Use a `Set` node immediately after the trigger to normalise field names before any logic
- Schedule-triggered flows: default to a sensible cron (e.g. Monday 08:00) — importers will adjust
- Keep flows linear where possible; branch only when the use case genuinely requires it
