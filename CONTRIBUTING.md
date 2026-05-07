# Contributing

Thanks for wanting to add a workflow. Follow the steps below to get your contribution merged cleanly.

---

## How to Add a Workflow

**Step 1 — Fork and clone**

```bash
git clone https://github.com/YOUR_USERNAME/n8n-smb-workflows.git
cd n8n-smb-workflows
```

**Step 2 — Create your workflow folder**

Pick the right category (`crm`, `email`, `social`, `lead-gen`, `reporting`, `utilities`) or propose a new one in the PR description.

```bash
mkdir -p workflows/<category>/<your-workflow-name>
```

**Step 3 — Add the required files**

Each workflow directory must contain exactly two files:

- `workflow.json` — valid n8n workflow export JSON (see format below)
- `README.md` — usage documentation (see template below)

**Step 4 — Update the main README table**

Add a row to the "What's Inside" table in the root `README.md`.

**Step 5 — Open a PR**

Branch name: `add/<your-workflow-name>`
PR title: `Add: <your-workflow-name>`

---

## workflow.json Requirements

Export your workflow from n8n (**Workflow menu → Download**). The file must include:

- `id` — unique UUID
- `name` — human-readable name
- `nodes` — array of node objects, each with `id`, `name`, `type`, `typeVersion`, `position`, `parameters`, and `credentials` (with placeholder IDs)
- `connections` — object mapping node outputs to inputs
- `active: false` — always ship as inactive
- `settings.executionOrder: "v1"`
- `settings.errorWorkflow: "REPLACE_WITH_YOUR_ERROR_WORKFLOW_ID"` — required on all non-utility workflows
- `versionId` — UUID

Credential IDs in `credentials` blocks must use the placeholder string `"REPLACE_WITH_YOUR_CREDENTIAL_ID"` so importers know they need to reconnect.

---

## README.md Template

Every workflow README must contain these sections:

```markdown
# Workflow Name

One-line description of what this workflow does.

## Use Case

2–3 sentences describing the business problem this solves and who would use it.

## Required Credentials

- **Service Name** — what it's used for (e.g. Baserow API Key — read/write rows)

## Node Overview

| Node | Type | Purpose |
|------|------|---------|
| Trigger | n8n-nodes-base.webhook | Receives incoming data |
| ... | ... | ... |

## Configuration

After importing, update the following:

1. **Node name** — what to change and where to find the value
2. ...

## Example

**Input:**
```json
{ "field": "value" }
```

**Output / Result:**
Description of what happens after the workflow runs.
```

---

## Code of Conduct

Be constructive. Keep PRs focused — one workflow per PR. If you're fixing a bug in an existing workflow, reference the issue.
