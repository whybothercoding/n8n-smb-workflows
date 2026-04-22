# n8n SMB Workflows — Open Source Repository Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a complete, importable open-source GitHub repository of 10 n8n workflow templates covering CRM, email, social media, lead gen, and reporting for small businesses.

**Architecture:** Pure static-file repository — no build tooling, no dependencies, no application code. Each workflow is a self-contained directory with a valid n8n-export JSON and a usage README. Top-level docs cover import instructions and credential setup guides.

**Tech Stack:** n8n workflow JSON (v1 export format), Markdown, Git, GitHub CLI (`gh`)

---

## File Map

```
README.md                                      — Repo hero, workflow table, import quickstart
LICENSE                                        — MIT
CONTRIBUTING.md                                — Contribution guide with required template
docs/how-to-import.md                          — Step-by-step n8n import walkthrough
docs/credentials-setup.md                      — Credential setup for all services used
workflows/crm/lead-capture-to-baserow/workflow.json
workflows/crm/lead-capture-to-baserow/README.md
workflows/crm/contact-form-to-notion/workflow.json
workflows/crm/contact-form-to-notion/README.md
workflows/email/ai-email-auto-reply/workflow.json
workflows/email/ai-email-auto-reply/README.md
workflows/email/invoice-reminder/workflow.json
workflows/email/invoice-reminder/README.md
workflows/social/rss-to-social-post/workflow.json
workflows/social/rss-to-social-post/README.md
workflows/social/content-repurpose-pipeline/workflow.json
workflows/social/content-repurpose-pipeline/README.md
workflows/lead-gen/newsletter-subscriber-to-crm/workflow.json
workflows/lead-gen/newsletter-subscriber-to-crm/README.md
workflows/lead-gen/abandoned-lead-followup/workflow.json
workflows/lead-gen/abandoned-lead-followup/README.md
workflows/reporting/weekly-business-digest/workflow.json
workflows/reporting/weekly-business-digest/README.md
workflows/reporting/support-ticket-to-slack/workflow.json
workflows/reporting/support-ticket-to-slack/README.md
```

---

## Task 1: Directory Structure and LICENSE

**Files:**
- Create: `LICENSE`
- Create all workflow/docs directories (via empty `.gitkeep` or direct file creation in subsequent tasks)

- [ ] **Step 1: Create full directory tree**

```bash
mkdir -p workflows/crm/lead-capture-to-baserow
mkdir -p workflows/crm/contact-form-to-notion
mkdir -p workflows/email/ai-email-auto-reply
mkdir -p workflows/email/invoice-reminder
mkdir -p workflows/social/rss-to-social-post
mkdir -p workflows/social/content-repurpose-pipeline
mkdir -p workflows/lead-gen/newsletter-subscriber-to-crm
mkdir -p workflows/lead-gen/abandoned-lead-followup
mkdir -p workflows/reporting/weekly-business-digest
mkdir -p workflows/reporting/support-ticket-to-slack
mkdir -p docs
```

- [ ] **Step 2: Write LICENSE**

Create `LICENSE` with this exact content:

```
MIT License

Copyright (c) 2026 IndieGoWeb Ltd

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

- [ ] **Step 3: Verify structure**

```bash
find . -type d | grep -v '.git' | sort
```

Expected output includes all 10 workflow dirs plus `docs/`.

---

## Task 2: Main README.md

**Files:**
- Create: `README.md`

- [ ] **Step 1: Write README.md**

```markdown
# n8n SMB Workflows

> Ready-to-import n8n workflow templates for small business automation.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![n8n](https://img.shields.io/badge/n8n-compatible-orange)](https://n8n.io)

A curated library of production-ready n8n workflows covering the most common automation needs for small businesses: lead capture, email handling, social media, reporting, and more. Every workflow ships as a clean JSON export — import directly into any n8n instance, connect your credentials, and activate.

---

## What's Inside

| # | Workflow | Category | Description |
|---|----------|----------|-------------|
| 1 | [Lead Capture to Baserow](workflows/crm/lead-capture-to-baserow/) | CRM | Webhook form submission → Baserow row + confirmation email |
| 2 | [Contact Form to Notion](workflows/crm/contact-form-to-notion/) | CRM | Webhook form → Notion database page + Slack notification |
| 3 | [AI Email Auto-Reply](workflows/email/ai-email-auto-reply/) | Email | Gmail trigger → GPT-4o draft reply + Notion log |
| 4 | [Invoice Reminder](workflows/email/invoice-reminder/) | Email | Daily check of unpaid Baserow invoices → reminder emails |
| 5 | [RSS to Social Post](workflows/social/rss-to-social-post/) | Social | RSS feed → GPT-4o LinkedIn post → LinkedIn API |
| 6 | [Content Repurpose Pipeline](workflows/social/content-repurpose-pipeline/) | Social | Article URL → tweet thread + LinkedIn post + newsletter snippet → Notion |
| 7 | [Newsletter Subscriber to CRM](workflows/lead-gen/newsletter-subscriber-to-crm/) | Lead Gen | Beehiiv webhook → Baserow upsert |
| 8 | [Abandoned Lead Follow-up](workflows/lead-gen/abandoned-lead-followup/) | Lead Gen | Daily stale-lead check → follow-up email + Baserow update |
| 9 | [Weekly Business Digest](workflows/reporting/weekly-business-digest/) | Reporting | Monday summary of Baserow stats → HTML digest email |
| 10 | [Support Ticket to Slack](workflows/reporting/support-ticket-to-slack/) | Reporting | Contact form → Baserow ticket + Slack alert + AI suggested reply |

---

## How to Import

**Step 1 — Copy the workflow JSON**
Open the workflow folder, then copy the raw contents of `workflow.json`.

**Step 2 — Import into n8n**
In your n8n instance: go to **Workflows** → click the **+** button → select **Import from JSON** → paste the JSON → click **Import**.

**Step 3 — Configure and activate**
Follow the workflow's `README.md` to connect credentials, update any IDs (table IDs, database IDs, channel names), then toggle the workflow **Active**.

See [docs/how-to-import.md](docs/how-to-import.md) for a detailed walkthrough.

---

## Prerequisites

- A running n8n instance (self-hosted or cloud). See [n8n docs](https://docs.n8n.io/hosting/) for setup.
- Credentials for the services each workflow uses. See [docs/credentials-setup.md](docs/credentials-setup.md).

---

## Contributing

Contributions welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for the workflow template and PR process.

---

## License

MIT — see [LICENSE](LICENSE).
```

- [ ] **Step 2: Verify**

```bash
wc -l README.md
```

Expected: 60+ lines.

---

## Task 3: CONTRIBUTING.md

**Files:**
- Create: `CONTRIBUTING.md`

- [ ] **Step 1: Write CONTRIBUTING.md**

```markdown
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

Pick the right category (`crm`, `email`, `social`, `lead-gen`, `reporting`) or propose a new one in the PR description.

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
```

- [ ] **Step 2: Verify**

```bash
wc -l CONTRIBUTING.md
```

Expected: 80+ lines.

---

## Task 4: docs/how-to-import.md

**Files:**
- Create: `docs/how-to-import.md`

- [ ] **Step 1: Write docs/how-to-import.md**

```markdown
# How to Import a Workflow into n8n

This guide covers importing any workflow from this repository into your n8n instance.

---

## Method A: Import from JSON (Recommended)

**1. Get the JSON**

Navigate to the workflow folder in this repo (e.g. `workflows/crm/lead-capture-to-baserow/`) and open `workflow.json`. Click **Raw** on GitHub, then select all and copy.

**2. Open n8n and import**

- Go to your n8n instance (e.g. `http://localhost:5678`)
- Click **Workflows** in the left sidebar
- Click the **+** (New Workflow) button in the top-right
- In the workflow editor, click the **three-dot menu (⋮)** in the top-right
- Select **Import from JSON**
- Paste the copied JSON into the text box
- Click **Import**

**3. Reconnect credentials**

After import, nodes that require credentials will show a red warning badge. Click each flagged node, open the **Credentials** dropdown, and either select an existing credential or click **Create New** to add one.

See [credentials-setup.md](credentials-setup.md) for setup instructions per service.

**4. Update configuration values**

Each workflow's `README.md` lists what you need to change (table IDs, database IDs, email addresses, channel names). Update these in the node parameters before activating.

**5. Activate**

Toggle the workflow switch to **Active** in the top-right of the editor. For webhook-triggered workflows, n8n will display the webhook URL — copy it and add it to your form or service.

---

## Method B: Upload JSON File

- Download `workflow.json` from this repo to your computer
- In n8n: **Workflows** → **+** → **⋮ menu** → **Import from file**
- Select the downloaded file

---

## Testing Before Activating

For webhook workflows: use the **Test Workflow** button and send a test request using a tool like [hoppscotch.io](https://hoppscotch.io) or `curl`:

```bash
curl -X POST https://your-n8n.com/webhook/YOUR_PATH \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com"}'
```

For schedule-triggered workflows: click **Execute Workflow** manually to test a single run before setting the schedule live.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Red badge on node | Credential not connected — click the node and assign or create a credential |
| "Webhook already registered" error | Another workflow is using the same webhook path — change the path in the Webhook node parameters |
| Workflow imports but does nothing | Check it is set to **Active** and the trigger condition is met |
| Expression errors (`{{ }}`) | A referenced field name doesn't match — check the upstream node output using the **Output** panel |
```

- [ ] **Step 2: Verify**

```bash
wc -l docs/how-to-import.md
```

Expected: 65+ lines.

---

## Task 5: docs/credentials-setup.md

**Files:**
- Create: `docs/credentials-setup.md`

- [ ] **Step 1: Write docs/credentials-setup.md**

```markdown
# Credentials Setup

Instructions for creating the credentials used across workflows in this repository.

In n8n, credentials are created via **Settings → Credentials → + Add Credential**.

---

## Baserow API Key

Used by: Lead Capture to Baserow, Invoice Reminder, Newsletter Subscriber to CRM, Abandoned Lead Follow-up, Weekly Business Digest, Support Ticket to Slack

1. Log in to your Baserow instance
2. Go to **Profile → API tokens** → click **Create token**
3. Name it (e.g. "n8n"), set permissions to **Read & Write** for the relevant databases
4. Copy the token
5. In n8n: **+ Add Credential** → search "Baserow" → paste the token and your Baserow host URL (e.g. `https://baserow.yourdomain.com`)

---

## Notion Integration (Internal)

Used by: Contact Form to Notion, AI Email Auto-Reply, Content Repurpose Pipeline

1. Go to [https://www.notion.so/my-integrations](https://www.notion.so/my-integrations)
2. Click **+ New integration** → give it a name → select your workspace → click **Submit**
3. Copy the **Internal Integration Token** (starts with `secret_`)
4. In each Notion database you want to connect: open the database → click **...** (top-right) → **Connections** → add your integration
5. In n8n: **+ Add Credential** → search "Notion" → paste the token

---

## OpenAI API Key

Used by: AI Email Auto-Reply, RSS to Social Post, Content Repurpose Pipeline, Support Ticket to Slack

1. Go to [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Click **+ Create new secret key** → copy it (shown only once)
3. In n8n: **+ Add Credential** → search "OpenAI" → paste the API key

---

## Gmail OAuth2

Used by: AI Email Auto-Reply

1. Go to [Google Cloud Console](https://console.cloud.google.com/) → create or select a project
2. Enable the **Gmail API** under **APIs & Services → Library**
3. Go to **APIs & Services → Credentials** → **+ Create Credentials** → **OAuth 2.0 Client ID**
4. Set Application type to **Web application**
5. Add `https://your-n8n.com/rest/oauth2-credential/callback` as an Authorized redirect URI
6. Copy the **Client ID** and **Client Secret**
7. In n8n: **+ Add Credential** → search "Gmail OAuth2" → paste the Client ID and Client Secret → click **Connect** and follow the Google auth flow

---

## Slack

Used by: Contact Form to Notion, Support Ticket to Slack

**Option A — Incoming Webhook (simpler, for posting only)**
1. Go to [https://api.slack.com/apps](https://api.slack.com/apps) → **Create New App** → **From scratch**
2. Enable **Incoming Webhooks** → **Add New Webhook to Workspace** → select a channel
3. Copy the webhook URL
4. In n8n: **+ Add Credential** → search "Slack" → choose **Webhook** type → paste the URL

**Option B — OAuth (for reading and posting)**
1. Create a Slack app at [https://api.slack.com/apps](https://api.slack.com/apps)
2. Under **OAuth & Permissions**, add Bot Token Scopes: `chat:write`, `channels:read`
3. Install the app to your workspace and copy the **Bot User OAuth Token**
4. In n8n: **+ Add Credential** → search "Slack" → choose **Access Token** → paste the token

---

## SMTP (Email Send)

Used by: Lead Capture to Baserow, Invoice Reminder, Abandoned Lead Follow-up, Weekly Business Digest

You need an SMTP host, port, username, and password. Common options:

| Provider | Host | Port | Notes |
|----------|------|------|-------|
| Gmail | `smtp.gmail.com` | 587 | Requires an App Password (not your main password) |
| Infomaniak | `mail.infomaniak.com` | 587 | Use your Infomaniak email credentials |
| Mailgun | `smtp.mailgun.org` | 587 | Get credentials from Mailgun dashboard |
| AWS SES | `email-smtp.<region>.amazonaws.com` | 587 | Create SMTP credentials in AWS IAM |

In n8n: **+ Add Credential** → search "SMTP" → fill in host, port, username, password → toggle **SSL/TLS** if required by your provider.

For Gmail App Passwords: [https://support.google.com/accounts/answer/185833](https://support.google.com/accounts/answer/185833)
```

- [ ] **Step 2: Verify**

```bash
wc -l docs/credentials-setup.md
```

Expected: 75+ lines.

- [ ] **Step 3: Commit docs foundation**

```bash
git add LICENSE README.md CONTRIBUTING.md docs/how-to-import.md docs/credentials-setup.md
git commit -m "docs: add LICENSE, README, CONTRIBUTING, and setup guides"
```

---

## Task 6: Workflow 1 — lead-capture-to-baserow

**Files:**
- Create: `workflows/crm/lead-capture-to-baserow/workflow.json`
- Create: `workflows/crm/lead-capture-to-baserow/README.md`

- [ ] **Step 1: Write workflow.json**

```json
{
  "id": "a1b2c3d4-0001-4abc-8def-000000000001",
  "meta": {
    "instanceId": "",
    "templateCredsSetupCompleted": true
  },
  "name": "Lead Capture to Baserow",
  "nodes": [
    {
      "id": "node-001-webhook",
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [240, 300],
      "parameters": {
        "path": "lead-capture",
        "httpMethod": "POST",
        "responseMode": "onReceived",
        "options": {}
      }
    },
    {
      "id": "node-001-set",
      "name": "Normalize Fields",
      "type": "n8n-nodes-base.set",
      "typeVersion": 3,
      "position": [460, 300],
      "parameters": {
        "assignments": {
          "assignments": [
            {
              "id": "assign-001",
              "name": "name",
              "value": "={{ $json.name ?? $json.full_name ?? '' }}",
              "type": "string"
            },
            {
              "id": "assign-002",
              "name": "email",
              "value": "={{ $json.email ?? '' }}",
              "type": "string"
            },
            {
              "id": "assign-003",
              "name": "phone",
              "value": "={{ $json.phone ?? $json.telephone ?? '' }}",
              "type": "string"
            },
            {
              "id": "assign-004",
              "name": "source",
              "value": "={{ $json.source ?? 'website' }}",
              "type": "string"
            },
            {
              "id": "assign-005",
              "name": "message",
              "value": "={{ $json.message ?? '' }}",
              "type": "string"
            },
            {
              "id": "assign-006",
              "name": "created_at",
              "value": "={{ new Date().toISOString() }}",
              "type": "string"
            }
          ]
        },
        "options": {}
      }
    },
    {
      "id": "node-001-baserow",
      "name": "Create Lead Row",
      "type": "n8n-nodes-base.baserow",
      "typeVersion": 1,
      "position": [680, 300],
      "parameters": {
        "operation": "create",
        "tableId": "YOUR_BASEROW_TABLE_ID",
        "fieldsUi": {
          "fieldValues": [
            { "fieldId": "Name", "fieldValue": "={{ $json.name }}" },
            { "fieldId": "Email", "fieldValue": "={{ $json.email }}" },
            { "fieldId": "Phone", "fieldValue": "={{ $json.phone }}" },
            { "fieldId": "Source", "fieldValue": "={{ $json.source }}" },
            { "fieldId": "Message", "fieldValue": "={{ $json.message }}" },
            { "fieldId": "Status", "fieldValue": "new" },
            { "fieldId": "Created At", "fieldValue": "={{ $json.created_at }}" }
          ]
        }
      },
      "credentials": {
        "baserowApi": {
          "id": "REPLACE_WITH_YOUR_CREDENTIAL_ID",
          "name": "Baserow account"
        }
      }
    },
    {
      "id": "node-001-email",
      "name": "Send Confirmation Email",
      "type": "n8n-nodes-base.emailSend",
      "typeVersion": 2,
      "position": [900, 300],
      "parameters": {
        "fromEmail": "your@company.com",
        "toEmail": "={{ $('Normalize Fields').item.json.email }}",
        "subject": "Thanks for reaching out!",
        "message": "Hi {{ $('Normalize Fields').item.json.name }},\n\nThank you for contacting us. We have received your message and will get back to you within 24 hours.\n\nBest regards,\nYour Company",
        "options": {}
      },
      "credentials": {
        "smtp": {
          "id": "REPLACE_WITH_YOUR_CREDENTIAL_ID",
          "name": "SMTP account"
        }
      }
    }
  ],
  "connections": {
    "Webhook": {
      "main": [[{ "node": "Normalize Fields", "type": "main", "index": 0 }]]
    },
    "Normalize Fields": {
      "main": [[{ "node": "Create Lead Row", "type": "main", "index": 0 }]]
    },
    "Create Lead Row": {
      "main": [[{ "node": "Send Confirmation Email", "type": "main", "index": 0 }]]
    }
  },
  "pinData": {},
  "active": false,
  "settings": { "executionOrder": "v1" },
  "staticData": null,
  "tags": [],
  "versionId": "v1b2c3d4-0001-4abc-8def-000000000001"
}
```

- [ ] **Step 2: Validate JSON**

```bash
python3 -m json.tool workflows/crm/lead-capture-to-baserow/workflow.json > /dev/null && echo "Valid JSON"
```

Expected: `Valid JSON`

- [ ] **Step 3: Write README.md**

```markdown
# Lead Capture to Baserow

Receives a contact form submission via webhook, normalises the fields, saves the lead to a Baserow table, and sends the submitter a confirmation email.

## Use Case

When a visitor fills in a contact or lead-capture form on your website, this workflow automatically stores the lead in your Baserow CRM table and sends an instant acknowledgement email. No manual copy-paste, no missed leads.

## Required Credentials

- **Baserow API Key** — write access to your leads table
- **SMTP** — outbound email for confirmation messages

## Node Overview

| Node | Type | Purpose |
|------|------|---------|
| Webhook | `n8n-nodes-base.webhook` | Receives POST from your contact form |
| Normalize Fields | `n8n-nodes-base.set` | Maps form fields to consistent names, adds `created_at` |
| Create Lead Row | `n8n-nodes-base.baserow` | Creates a new row in your Baserow leads table |
| Send Confirmation Email | `n8n-nodes-base.emailSend` | Sends a thank-you email to the submitter |

## Configuration

After importing:

1. **Webhook node** — copy the webhook URL and add it as the form `action` on your website
2. **Create Lead Row** — replace `YOUR_BASEROW_TABLE_ID` with your actual table ID (visible in the Baserow URL when viewing the table)
3. **Create Lead Row** — update `fieldId` values to match your Baserow column names exactly
4. **Send Confirmation Email** — update `fromEmail` to your sending address
5. Connect credentials: Baserow API → "Baserow account", SMTP → "SMTP account"

## Example

**Input (webhook POST body):**
```json
{
  "name": "Maria Papadopoulos",
  "email": "maria@example.com",
  "phone": "+30 210 1234567",
  "message": "I'm interested in your automation services."
}
```

**Result:**
- New row appears in Baserow with Status = `new`
- `maria@example.com` receives: _"Thanks for reaching out! We'll get back to you within 24 hours."_
```

- [ ] **Step 4: Commit**

```bash
git add workflows/crm/lead-capture-to-baserow/
git commit -m "feat: add lead-capture-to-baserow workflow"
```

---

## Task 7: Workflow 2 — contact-form-to-notion

**Files:**
- Create: `workflows/crm/contact-form-to-notion/workflow.json`
- Create: `workflows/crm/contact-form-to-notion/README.md`

- [ ] **Step 1: Write workflow.json**

```json
{
  "id": "a1b2c3d4-0002-4abc-8def-000000000002",
  "meta": {
    "instanceId": "",
    "templateCredsSetupCompleted": true
  },
  "name": "Contact Form to Notion",
  "nodes": [
    {
      "id": "node-002-webhook",
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [240, 300],
      "parameters": {
        "path": "contact-form",
        "httpMethod": "POST",
        "responseMode": "onReceived",
        "options": {}
      }
    },
    {
      "id": "node-002-notion",
      "name": "Create Notion Page",
      "type": "n8n-nodes-base.notion",
      "typeVersion": 2,
      "position": [460, 300],
      "parameters": {
        "resource": "databasePage",
        "operation": "create",
        "databaseId": {
          "__rl": true,
          "value": "YOUR_NOTION_DATABASE_ID",
          "mode": "id"
        },
        "title": "={{ $json.name }} — {{ new Date().toLocaleDateString('en-GB') }}",
        "blockUi": {
          "blockValues": []
        },
        "propertiesUi": {
          "propertyValues": [
            {
              "key": "Email|email",
              "emailValue": "={{ $json.email }}"
            },
            {
              "key": "Phone|phone_number",
              "phoneValue": "={{ $json.phone ?? '' }}"
            },
            {
              "key": "Source|select",
              "selectValue": "={{ $json.source ?? 'website' }}"
            },
            {
              "key": "Message|rich_text",
              "textContent": "={{ $json.message ?? '' }}"
            }
          ]
        }
      },
      "credentials": {
        "notionApi": {
          "id": "REPLACE_WITH_YOUR_CREDENTIAL_ID",
          "name": "Notion account"
        }
      }
    },
    {
      "id": "node-002-slack",
      "name": "Slack Notification",
      "type": "n8n-nodes-base.slack",
      "typeVersion": 2,
      "position": [680, 300],
      "parameters": {
        "resource": "message",
        "operation": "post",
        "channel": "#contacts",
        "text": ":mailbox_with_mail: *New contact form submission*\n*Name:* {{ $('Webhook').item.json.name }}\n*Email:* {{ $('Webhook').item.json.email }}\n*Message:* {{ $('Webhook').item.json.message ?? '(no message)' }}\n<{{ $json.url }}|View in Notion>",
        "otherOptions": {}
      },
      "credentials": {
        "slackApi": {
          "id": "REPLACE_WITH_YOUR_CREDENTIAL_ID",
          "name": "Slack account"
        }
      }
    }
  ],
  "connections": {
    "Webhook": {
      "main": [[{ "node": "Create Notion Page", "type": "main", "index": 0 }]]
    },
    "Create Notion Page": {
      "main": [[{ "node": "Slack Notification", "type": "main", "index": 0 }]]
    }
  },
  "pinData": {},
  "active": false,
  "settings": { "executionOrder": "v1" },
  "staticData": null,
  "tags": [],
  "versionId": "v1b2c3d4-0002-4abc-8def-000000000002"
}
```

- [ ] **Step 2: Validate JSON**

```bash
python3 -m json.tool workflows/crm/contact-form-to-notion/workflow.json > /dev/null && echo "Valid JSON"
```

- [ ] **Step 3: Write README.md**

```markdown
# Contact Form to Notion

Receives a contact form submission via webhook, creates a Notion database page, and posts a summary to a Slack channel.

## Use Case

Keep your entire contact history inside Notion while getting instant Slack alerts for every new inquiry. Ideal if your team already uses Notion as a lightweight CRM and Slack for internal comms.

## Required Credentials

- **Notion Integration Token** — write access to your contacts database
- **Slack API** — post access to your notification channel

## Node Overview

| Node | Type | Purpose |
|------|------|---------|
| Webhook | `n8n-nodes-base.webhook` | Receives POST from the contact form |
| Create Notion Page | `n8n-nodes-base.notion` | Creates a page in your Notion contacts database |
| Slack Notification | `n8n-nodes-base.slack` | Posts a summary card to a Slack channel |

## Configuration

After importing:

1. **Webhook node** — copy the webhook URL and point your form to it
2. **Create Notion Page** — replace `YOUR_NOTION_DATABASE_ID` with your database ID (from the Notion URL: `notion.so/<database_id>?v=...`)
3. **Create Notion Page** — ensure your Notion database has properties named `Email`, `Phone`, `Source`, `Message` (types: email, phone_number, select, rich_text respectively). Add the Notion integration to the database via the database's **Connections** settings.
4. **Slack Notification** — change `#contacts` to your preferred channel name
5. Connect credentials: Notion account, Slack account

## Example

**Input:**
```json
{
  "name": "Nikos Georgiou",
  "email": "nikos@example.com",
  "phone": "+30 694 0000000",
  "message": "Can you help automate our invoicing?"
}
```

**Result:**
- New Notion page created: _"Nikos Georgiou — 22/04/2026"_ with all fields populated
- Slack message posted to `#contacts` with name, email, and a link to the Notion page
```

- [ ] **Step 4: Commit**

```bash
git add workflows/crm/contact-form-to-notion/
git commit -m "feat: add contact-form-to-notion workflow"
```

---

## Task 8: Workflow 3 — ai-email-auto-reply

**Files:**
- Create: `workflows/email/ai-email-auto-reply/workflow.json`
- Create: `workflows/email/ai-email-auto-reply/README.md`

- [ ] **Step 1: Write workflow.json**

```json
{
  "id": "a1b2c3d4-0003-4abc-8def-000000000003",
  "meta": {
    "instanceId": "",
    "templateCredsSetupCompleted": true
  },
  "name": "AI Email Auto-Reply",
  "nodes": [
    {
      "id": "node-003-gmail-trigger",
      "name": "Gmail Trigger",
      "type": "n8n-nodes-base.gmailTrigger",
      "typeVersion": 1,
      "position": [240, 300],
      "parameters": {
        "filters": {
          "readStatus": "unread",
          "includeSpamTrash": false
        },
        "pollTimes": {
          "item": [{ "mode": "everyMinute" }]
        },
        "options": {}
      },
      "credentials": {
        "gmailOAuth2": {
          "id": "REPLACE_WITH_YOUR_CREDENTIAL_ID",
          "name": "Gmail account"
        }
      }
    },
    {
      "id": "node-003-openai",
      "name": "Generate Reply",
      "type": "n8n-nodes-base.openAi",
      "typeVersion": 1,
      "position": [460, 300],
      "parameters": {
        "resource": "text",
        "operation": "message",
        "modelId": {
          "__rl": true,
          "value": "gpt-4o",
          "mode": "list",
          "cachedResultName": "gpt-4o"
        },
        "messages": {
          "values": [
            {
              "role": "system",
              "content": "You are a professional business email assistant. Write a concise, polite, and helpful reply to the incoming email. Address the sender by their first name if you can infer it. Sign off as 'The Team'. Keep the reply under 150 words. Do not include a subject line."
            },
            {
              "role": "user",
              "content": "=From: {{ $json.from.value[0].address }}\nSubject: {{ $json.subject }}\n\n{{ $json.text ?? $json.snippet }}"
            }
          ]
        },
        "simplify": true,
        "options": {}
      },
      "credentials": {
        "openAiApi": {
          "id": "REPLACE_WITH_YOUR_CREDENTIAL_ID",
          "name": "OpenAI account"
        }
      }
    },
    {
      "id": "node-003-gmail-draft",
      "name": "Create Draft Reply",
      "type": "n8n-nodes-base.gmail",
      "typeVersion": 2,
      "position": [680, 300],
      "parameters": {
        "resource": "draft",
        "operation": "create",
        "subject": "=Re: {{ $('Gmail Trigger').item.json.subject }}",
        "message": "={{ $json.choices[0].message.content }}",
        "additionalFields": {
          "threadId": "={{ $('Gmail Trigger').item.json.threadId }}",
          "toList": "={{ $('Gmail Trigger').item.json.from.value[0].address }}"
        }
      },
      "credentials": {
        "gmailOAuth2": {
          "id": "REPLACE_WITH_YOUR_CREDENTIAL_ID",
          "name": "Gmail account"
        }
      }
    },
    {
      "id": "node-003-notion",
      "name": "Log to Notion",
      "type": "n8n-nodes-base.notion",
      "typeVersion": 2,
      "position": [900, 300],
      "parameters": {
        "resource": "databasePage",
        "operation": "create",
        "databaseId": {
          "__rl": true,
          "value": "YOUR_NOTION_EMAIL_LOG_DATABASE_ID",
          "mode": "id"
        },
        "title": "={{ $('Gmail Trigger').item.json.subject }}",
        "propertiesUi": {
          "propertyValues": [
            {
              "key": "From|email",
              "emailValue": "={{ $('Gmail Trigger').item.json.from.value[0].address }}"
            },
            {
              "key": "Date|date",
              "date": "={{ new Date().toISOString() }}"
            },
            {
              "key": "Draft Created|checkbox",
              "checkboxValue": true
            }
          ]
        }
      },
      "credentials": {
        "notionApi": {
          "id": "REPLACE_WITH_YOUR_CREDENTIAL_ID",
          "name": "Notion account"
        }
      }
    }
  ],
  "connections": {
    "Gmail Trigger": {
      "main": [[{ "node": "Generate Reply", "type": "main", "index": 0 }]]
    },
    "Generate Reply": {
      "main": [[{ "node": "Create Draft Reply", "type": "main", "index": 0 }]]
    },
    "Create Draft Reply": {
      "main": [[{ "node": "Log to Notion", "type": "main", "index": 0 }]]
    }
  },
  "pinData": {},
  "active": false,
  "settings": { "executionOrder": "v1" },
  "staticData": null,
  "tags": [],
  "versionId": "v1b2c3d4-0003-4abc-8def-000000000003"
}
```

- [ ] **Step 2: Validate JSON**

```bash
python3 -m json.tool workflows/email/ai-email-auto-reply/workflow.json > /dev/null && echo "Valid JSON"
```

- [ ] **Step 3: Write README.md**

```markdown
# AI Email Auto-Reply

Monitors Gmail for new unread emails, generates a draft reply with GPT-4o, and logs the interaction to Notion.

## Use Case

Never face an empty inbox again. This workflow checks for new unread emails every minute, uses GPT-4o to write a contextual reply, and saves it as a Gmail draft — ready for your review before sending. Every handled email is logged to a Notion database so you have a complete record.

## Required Credentials

- **Gmail OAuth2** — read inbox + create drafts
- **OpenAI API Key** — GPT-4o chat completions
- **Notion Integration Token** — write to your email log database

## Node Overview

| Node | Type | Purpose |
|------|------|---------|
| Gmail Trigger | `n8n-nodes-base.gmailTrigger` | Polls Gmail every minute for new unread emails |
| Generate Reply | `n8n-nodes-base.openAi` | Sends email content to GPT-4o, returns a draft reply |
| Create Draft Reply | `n8n-nodes-base.gmail` | Saves the generated text as a Gmail draft in the same thread |
| Log to Notion | `n8n-nodes-base.notion` | Creates a log entry in your Notion email database |

## Configuration

After importing:

1. **Gmail Trigger** — connect Gmail OAuth2 credentials; optionally add a sender filter in the `filters` parameters to scope which emails trigger the workflow
2. **Generate Reply** — edit the `system` message to match your business tone, sign-off name, and any specific instructions (e.g. "if the email is asking for a quote, say we'll follow up within 1 business day")
3. **Log to Notion** — replace `YOUR_NOTION_EMAIL_LOG_DATABASE_ID`; ensure the database has properties: `From` (email), `Date` (date), `Draft Created` (checkbox)
4. Connect all three credentials

## Example

**Incoming email:**
> From: client@example.com  
> Subject: Question about pricing  
> Body: Hi, I'd like to know more about your automation packages. What's included?

**Generated draft reply:**
> Hi,  
> Thank you for reaching out! We'd be happy to walk you through our automation packages. Could you share a bit more about what you're looking to automate? That'll help us suggest the best fit.  
> The Team

**Notion log entry:** Row with subject "Question about pricing", From = client@example.com, Draft Created = ✓
```

- [ ] **Step 4: Commit**

```bash
git add workflows/email/ai-email-auto-reply/
git commit -m "feat: add ai-email-auto-reply workflow"
```

---

## Task 9: Workflow 4 — invoice-reminder

**Files:**
- Create: `workflows/email/invoice-reminder/workflow.json`
- Create: `workflows/email/invoice-reminder/README.md`

- [ ] **Step 1: Write workflow.json**

```json
{
  "id": "a1b2c3d4-0004-4abc-8def-000000000004",
  "meta": {
    "instanceId": "",
    "templateCredsSetupCompleted": true
  },
  "name": "Invoice Reminder",
  "nodes": [
    {
      "id": "node-004-schedule",
      "name": "Daily 9am",
      "type": "n8n-nodes-base.scheduleTrigger",
      "typeVersion": 1,
      "position": [240, 300],
      "parameters": {
        "rule": {
          "interval": [
            {
              "field": "cronExpression",
              "expression": "0 9 * * 1-5"
            }
          ]
        }
      }
    },
    {
      "id": "node-004-baserow",
      "name": "Get Unpaid Invoices",
      "type": "n8n-nodes-base.baserow",
      "typeVersion": 1,
      "position": [460, 300],
      "parameters": {
        "operation": "getAll",
        "tableId": "YOUR_INVOICES_TABLE_ID",
        "returnAll": true,
        "filters": {
          "filters": [
            {
              "field": "Status",
              "condition": "equal",
              "value": "unpaid"
            }
          ]
        },
        "options": {}
      },
      "credentials": {
        "baserowApi": {
          "id": "REPLACE_WITH_YOUR_CREDENTIAL_ID",
          "name": "Baserow account"
        }
      }
    },
    {
      "id": "node-004-if",
      "name": "Is Overdue?",
      "type": "n8n-nodes-base.if",
      "typeVersion": 2,
      "position": [680, 300],
      "parameters": {
        "conditions": {
          "options": {
            "caseSensitive": false,
            "leftValue": "",
            "typeValidation": "loose"
          },
          "conditions": [
            {
              "id": "cond-004-001",
              "leftValue": "={{ new Date($json.due_date) < new Date() }}",
              "rightValue": true,
              "operator": {
                "type": "boolean",
                "operation": "true"
              }
            }
          ],
          "combinator": "and"
        },
        "looseTypeValidation": true
      }
    },
    {
      "id": "node-004-email",
      "name": "Send Reminder Email",
      "type": "n8n-nodes-base.emailSend",
      "typeVersion": 2,
      "position": [900, 200],
      "parameters": {
        "fromEmail": "billing@yourcompany.com",
        "toEmail": "={{ $json.client_email }}",
        "subject": "=Payment reminder: Invoice #{{ $json.invoice_number }}",
        "message": "=Hi {{ $json.client_name }},\n\nThis is a friendly reminder that Invoice #{{ $json.invoice_number }} for {{ $json.currency ?? '€' }}{{ $json.amount }} was due on {{ new Date($json.due_date).toLocaleDateString('en-GB') }}.\n\nPlease arrange payment at your earliest convenience. If you have any questions, reply to this email.\n\nThank you,\nYour Company",
        "options": {}
      },
      "credentials": {
        "smtp": {
          "id": "REPLACE_WITH_YOUR_CREDENTIAL_ID",
          "name": "SMTP account"
        }
      }
    },
    {
      "id": "node-004-baserow-update",
      "name": "Mark Reminder Sent",
      "type": "n8n-nodes-base.baserow",
      "typeVersion": 1,
      "position": [1120, 200],
      "parameters": {
        "operation": "update",
        "tableId": "YOUR_INVOICES_TABLE_ID",
        "id": "={{ $json.id }}",
        "fieldsUi": {
          "fieldValues": [
            { "fieldId": "Reminder Sent", "fieldValue": "={{ new Date().toISOString() }}" }
          ]
        }
      },
      "credentials": {
        "baserowApi": {
          "id": "REPLACE_WITH_YOUR_CREDENTIAL_ID",
          "name": "Baserow account"
        }
      }
    }
  ],
  "connections": {
    "Daily 9am": {
      "main": [[{ "node": "Get Unpaid Invoices", "type": "main", "index": 0 }]]
    },
    "Get Unpaid Invoices": {
      "main": [[{ "node": "Is Overdue?", "type": "main", "index": 0 }]]
    },
    "Is Overdue?": {
      "main": [
        [{ "node": "Send Reminder Email", "type": "main", "index": 0 }],
        []
      ]
    },
    "Send Reminder Email": {
      "main": [[{ "node": "Mark Reminder Sent", "type": "main", "index": 0 }]]
    }
  },
  "pinData": {},
  "active": false,
  "settings": { "executionOrder": "v1" },
  "staticData": null,
  "tags": [],
  "versionId": "v1b2c3d4-0004-4abc-8def-000000000004"
}
```

- [ ] **Step 2: Validate JSON**

```bash
python3 -m json.tool workflows/email/invoice-reminder/workflow.json > /dev/null && echo "Valid JSON"
```

- [ ] **Step 3: Write README.md**

```markdown
# Invoice Reminder

Runs every weekday morning, fetches unpaid overdue invoices from Baserow, sends a reminder email to each client, and marks the reminder as sent.

## Use Case

Stop chasing payments manually. This workflow runs at 9am Monday–Friday, checks your Baserow invoices table for overdue unpaid invoices, and automatically sends a professional reminder email to each client. Each reminder is timestamped in the `Reminder Sent` field.

## Required Credentials

- **Baserow API Key** — read and write access to your invoices table
- **SMTP** — outbound email for reminder messages

## Node Overview

| Node | Type | Purpose |
|------|------|---------|
| Daily 9am | `n8n-nodes-base.scheduleTrigger` | Triggers Monday–Friday at 09:00 |
| Get Unpaid Invoices | `n8n-nodes-base.baserow` | Fetches all rows where Status = `unpaid` |
| Is Overdue? | `n8n-nodes-base.if` | Passes only invoices where `due_date` is in the past |
| Send Reminder Email | `n8n-nodes-base.emailSend` | Sends a personalized reminder per invoice |
| Mark Reminder Sent | `n8n-nodes-base.baserow` | Updates `Reminder Sent` timestamp on the row |

## Configuration

After importing:

1. **Get Unpaid Invoices + Mark Reminder Sent** — replace `YOUR_INVOICES_TABLE_ID` in both Baserow nodes
2. **Baserow column names** — your invoices table must have columns: `Status` (text, value `unpaid`), `due_date` (date, ISO format), `client_email` (text), `client_name` (text), `invoice_number` (text), `amount` (number), `Reminder Sent` (date). Adjust `fieldId` values to match your actual column names.
3. **Send Reminder Email** — update `fromEmail` to your billing address
4. **Daily 9am** — change the cron expression if you want a different schedule (e.g. `0 9 * * *` for every day including weekends)
5. Connect credentials: Baserow account, SMTP account

## Example

**Baserow row:**
```json
{
  "id": 42,
  "Status": "unpaid",
  "due_date": "2026-04-10",
  "client_name": "Stavros Ltd",
  "client_email": "stavros@example.com",
  "invoice_number": "INV-0098",
  "amount": 1200
}
```

**Email sent to stavros@example.com:**
> Subject: Payment reminder: Invoice #INV-0098  
> Hi Stavros Ltd, this is a friendly reminder that Invoice #INV-0098 for €1200 was due on 10/04/2026...
```

- [ ] **Step 4: Commit**

```bash
git add workflows/email/invoice-reminder/
git commit -m "feat: add invoice-reminder workflow"
```

---

## Task 10: Workflow 5 — rss-to-social-post

**Files:**
- Create: `workflows/social/rss-to-social-post/workflow.json`
- Create: `workflows/social/rss-to-social-post/README.md`

- [ ] **Step 1: Write workflow.json**

```json
{
  "id": "a1b2c3d4-0005-4abc-8def-000000000005",
  "meta": {
    "instanceId": "",
    "templateCredsSetupCompleted": true
  },
  "name": "RSS to Social Post",
  "nodes": [
    {
      "id": "node-005-schedule",
      "name": "Every Hour",
      "type": "n8n-nodes-base.scheduleTrigger",
      "typeVersion": 1,
      "position": [240, 300],
      "parameters": {
        "rule": {
          "interval": [
            {
              "field": "hours",
              "hoursInterval": 1
            }
          ]
        }
      }
    },
    {
      "id": "node-005-rss",
      "name": "Read RSS Feed",
      "type": "n8n-nodes-base.rssFeedRead",
      "typeVersion": 1,
      "position": [460, 300],
      "parameters": {
        "url": "https://YOUR_RSS_FEED_URL/feed.xml",
        "options": {}
      }
    },
    {
      "id": "node-005-openai",
      "name": "Write LinkedIn Post",
      "type": "n8n-nodes-base.openAi",
      "typeVersion": 1,
      "position": [680, 300],
      "parameters": {
        "resource": "text",
        "operation": "message",
        "modelId": {
          "__rl": true,
          "value": "gpt-4o",
          "mode": "list",
          "cachedResultName": "gpt-4o"
        },
        "messages": {
          "values": [
            {
              "role": "system",
              "content": "You are a professional LinkedIn content writer. Rewrite the article summary below as a LinkedIn post. Use a professional yet conversational tone. Include 3–5 relevant hashtags at the end. Maximum 150 words. Do not use marketing clichés. Start with a strong hook — a question, statistic, or provocative statement."
            },
            {
              "role": "user",
              "content": "=Article title: {{ $json.title }}\n\nSummary: {{ $json.contentSnippet ?? $json.summary ?? $json.content }}\n\nSource URL: {{ $json.link }}"
            }
          ]
        },
        "simplify": true,
        "options": { "maxTokens": 300 }
      },
      "credentials": {
        "openAiApi": {
          "id": "REPLACE_WITH_YOUR_CREDENTIAL_ID",
          "name": "OpenAI account"
        }
      }
    },
    {
      "id": "node-005-linkedin",
      "name": "Post to LinkedIn",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4,
      "position": [900, 300],
      "parameters": {
        "method": "POST",
        "url": "https://api.linkedin.com/v2/ugcPosts",
        "sendHeaders": true,
        "headerParameters": {
          "parameters": [
            { "name": "Authorization", "value": "Bearer YOUR_LINKEDIN_ACCESS_TOKEN" },
            { "name": "Content-Type", "value": "application/json" },
            { "name": "X-Restli-Protocol-Version", "value": "2.0.0" }
          ]
        },
        "sendBody": true,
        "contentType": "raw",
        "rawContentType": "application/json",
        "body": "={{ JSON.stringify({ \"author\": \"urn:li:person:YOUR_LINKEDIN_PERSON_ID\", \"lifecycleState\": \"PUBLISHED\", \"specificContent\": { \"com.linkedin.ugc.ShareContent\": { \"shareCommentary\": { \"text\": $json.choices[0].message.content }, \"shareMediaCategory\": \"NONE\" } }, \"visibility\": { \"com.linkedin.ugc.MemberNetworkVisibility\": \"PUBLIC\" } }) }}",
        "options": {}
      }
    }
  ],
  "connections": {
    "Every Hour": {
      "main": [[{ "node": "Read RSS Feed", "type": "main", "index": 0 }]]
    },
    "Read RSS Feed": {
      "main": [[{ "node": "Write LinkedIn Post", "type": "main", "index": 0 }]]
    },
    "Write LinkedIn Post": {
      "main": [[{ "node": "Post to LinkedIn", "type": "main", "index": 0 }]]
    }
  },
  "pinData": {},
  "active": false,
  "settings": { "executionOrder": "v1" },
  "staticData": null,
  "tags": [],
  "versionId": "v1b2c3d4-0005-4abc-8def-000000000005"
}
```

- [ ] **Step 2: Validate JSON**

```bash
python3 -m json.tool workflows/social/rss-to-social-post/workflow.json > /dev/null && echo "Valid JSON"
```

- [ ] **Step 3: Write README.md**

```markdown
# RSS to Social Post

Reads new items from an RSS feed hourly, rewrites each item as a LinkedIn post using GPT-4o, and publishes directly to LinkedIn.

## Use Case

Turn your industry news feed or blog into a steady stream of LinkedIn content — automatically. Each RSS item is rewritten in a professional, scroll-stopping LinkedIn format with hashtags. Runs every hour so you're always sharing fresh, relevant content.

## Required Credentials

- **OpenAI API Key** — GPT-4o rewriting
- **LinkedIn Access Token** — post to your LinkedIn profile or company page (set directly in the HTTP Request node header)

## Node Overview

| Node | Type | Purpose |
|------|------|---------|
| Every Hour | `n8n-nodes-base.scheduleTrigger` | Triggers the workflow every 60 minutes |
| Read RSS Feed | `n8n-nodes-base.rssFeedRead` | Fetches items from your RSS feed URL |
| Write LinkedIn Post | `n8n-nodes-base.openAi` | Rewrites each item as a 150-word LinkedIn post |
| Post to LinkedIn | `n8n-nodes-base.httpRequest` | Posts to LinkedIn UGC Posts API |

## Configuration

After importing:

1. **Read RSS Feed** — replace `YOUR_RSS_FEED_URL` with your feed URL (e.g. `https://techcrunch.com/feed/`)
2. **Post to LinkedIn** — replace `YOUR_LINKEDIN_ACCESS_TOKEN` in the Authorization header. Get a token via the [LinkedIn Developer Portal](https://developer.linkedin.com/) — you need an app with `w_member_social` permission.
3. **Post to LinkedIn** — replace `YOUR_LINKEDIN_PERSON_ID` with your LinkedIn person URN (find it by calling `https://api.linkedin.com/v2/me` with your token)
4. **Write LinkedIn Post** — edit the system prompt to match your brand voice
5. Connect OpenAI credentials

**Note on volume:** A busy RSS feed may generate many posts per hour. Add an IF node after the RSS step to filter only items published in the last hour using `{{ new Date($json.isoDate) > new Date(Date.now() - 3600000) }}`.

## Example

**RSS item title:** "How AI is transforming small business invoicing"

**Generated LinkedIn post:**
> Are you still sending invoices manually in 2026? Small businesses that adopt AI invoicing report 40% fewer late payments.
>
> Here's what's changing: AI tools now auto-generate payment reminders, match bank statements, and flag disputes — without any human input.
>
> The businesses winning aren't the ones working harder. They're the ones automating faster.
>
> #SmallBusiness #Automation #AI #Invoicing #Productivity
```

- [ ] **Step 4: Commit**

```bash
git add workflows/social/rss-to-social-post/
git commit -m "feat: add rss-to-social-post workflow"
```

---

## Task 11: Workflow 6 — content-repurpose-pipeline

**Files:**
- Create: `workflows/social/content-repurpose-pipeline/workflow.json`
- Create: `workflows/social/content-repurpose-pipeline/README.md`

- [ ] **Step 1: Write workflow.json**

```json
{
  "id": "a1b2c3d4-0006-4abc-8def-000000000006",
  "meta": {
    "instanceId": "",
    "templateCredsSetupCompleted": true
  },
  "name": "Content Repurpose Pipeline",
  "nodes": [
    {
      "id": "node-006-webhook",
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [240, 300],
      "parameters": {
        "path": "repurpose-content",
        "httpMethod": "POST",
        "responseMode": "onReceived",
        "options": {}
      }
    },
    {
      "id": "node-006-fetch",
      "name": "Fetch Article",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4,
      "position": [460, 300],
      "parameters": {
        "method": "GET",
        "url": "={{ $json.url }}",
        "sendHeaders": true,
        "headerParameters": {
          "parameters": [
            { "name": "User-Agent", "value": "Mozilla/5.0 (compatible; n8n-bot/1.0)" }
          ]
        },
        "options": {}
      }
    },
    {
      "id": "node-006-code",
      "name": "Extract Text",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [680, 300],
      "parameters": {
        "jsCode": "const html = $input.first().json.data;\n// Strip HTML tags and collapse whitespace\nconst text = html\n  .replace(/<script[\\s\\S]*?<\\/script>/gi, '')\n  .replace(/<style[\\s\\S]*?<\\/style>/gi, '')\n  .replace(/<[^>]+>/g, ' ')\n  .replace(/&nbsp;/g, ' ')\n  .replace(/&amp;/g, '&')\n  .replace(/&lt;/g, '<')\n  .replace(/&gt;/g, '>')\n  .replace(/\\s+/g, ' ')\n  .trim()\n  .substring(0, 4000); // Limit to 4000 chars to stay within token limits\n\nreturn [{ json: { text, url: $('Webhook').item.json.url } }];"
      }
    },
    {
      "id": "node-006-openai",
      "name": "Generate Content Variations",
      "type": "n8n-nodes-base.openAi",
      "typeVersion": 1,
      "position": [900, 300],
      "parameters": {
        "resource": "text",
        "operation": "message",
        "modelId": {
          "__rl": true,
          "value": "gpt-4o",
          "mode": "list",
          "cachedResultName": "gpt-4o"
        },
        "messages": {
          "values": [
            {
              "role": "system",
              "content": "You are a content repurposing specialist. Given article text, produce three outputs in this exact JSON format:\n{\n  \"tweet_thread\": [\"tweet1\", \"tweet2\", \"tweet3\", \"tweet4\", \"tweet5\"],\n  \"linkedin_post\": \"...\",\n  \"newsletter_snippet\": \"...\"\n}\n\nRules:\n- tweet_thread: 5 tweets, each under 280 characters, the first grabs attention, the last includes a call to action. No hashtags.\n- linkedin_post: professional tone, 150–200 words, 3–5 relevant hashtags at end.\n- newsletter_snippet: 80–100 words, written for an email newsletter subscriber, conversational tone, ends with a teaser linking back to the original.\n\nReturn only valid JSON. No markdown code fences."
            },
            {
              "role": "user",
              "content": "={{ $json.text }}"
            }
          ]
        },
        "simplify": true,
        "options": { "maxTokens": 1500 }
      },
      "credentials": {
        "openAiApi": {
          "id": "REPLACE_WITH_YOUR_CREDENTIAL_ID",
          "name": "OpenAI account"
        }
      }
    },
    {
      "id": "node-006-notion",
      "name": "Save to Notion",
      "type": "n8n-nodes-base.notion",
      "typeVersion": 2,
      "position": [1120, 300],
      "parameters": {
        "resource": "databasePage",
        "operation": "create",
        "databaseId": {
          "__rl": true,
          "value": "YOUR_NOTION_CONTENT_DATABASE_ID",
          "mode": "id"
        },
        "title": "=Repurposed: {{ $('Webhook').item.json.url }}",
        "propertiesUi": {
          "propertyValues": [
            {
              "key": "Source URL|url",
              "urlValue": "={{ $('Webhook').item.json.url }}"
            },
            {
              "key": "Status|select",
              "selectValue": "draft"
            },
            {
              "key": "Created|date",
              "date": "={{ new Date().toISOString() }}"
            }
          ]
        },
        "blockUi": {
          "blockValues": [
            {
              "type": "heading_2",
              "textContent": "Tweet Thread"
            },
            {
              "type": "paragraph",
              "textContent": "={{ (() => { try { const c = JSON.parse($json.choices[0].message.content); return c.tweet_thread.map((t, i) => (i+1) + '. ' + t).join('\\n\\n'); } catch(e) { return $json.choices[0].message.content; } })() }}"
            },
            {
              "type": "heading_2",
              "textContent": "LinkedIn Post"
            },
            {
              "type": "paragraph",
              "textContent": "={{ (() => { try { return JSON.parse($json.choices[0].message.content).linkedin_post; } catch(e) { return ''; } })() }}"
            },
            {
              "type": "heading_2",
              "textContent": "Newsletter Snippet"
            },
            {
              "type": "paragraph",
              "textContent": "={{ (() => { try { return JSON.parse($json.choices[0].message.content).newsletter_snippet; } catch(e) { return ''; } })() }}"
            }
          ]
        }
      },
      "credentials": {
        "notionApi": {
          "id": "REPLACE_WITH_YOUR_CREDENTIAL_ID",
          "name": "Notion account"
        }
      }
    }
  ],
  "connections": {
    "Webhook": {
      "main": [[{ "node": "Fetch Article", "type": "main", "index": 0 }]]
    },
    "Fetch Article": {
      "main": [[{ "node": "Extract Text", "type": "main", "index": 0 }]]
    },
    "Extract Text": {
      "main": [[{ "node": "Generate Content Variations", "type": "main", "index": 0 }]]
    },
    "Generate Content Variations": {
      "main": [[{ "node": "Save to Notion", "type": "main", "index": 0 }]]
    }
  },
  "pinData": {},
  "active": false,
  "settings": { "executionOrder": "v1" },
  "staticData": null,
  "tags": [],
  "versionId": "v1b2c3d4-0006-4abc-8def-000000000006"
}
```

- [ ] **Step 2: Validate JSON**

```bash
python3 -m json.tool workflows/social/content-repurpose-pipeline/workflow.json > /dev/null && echo "Valid JSON"
```

- [ ] **Step 3: Write README.md**

```markdown
# Content Repurpose Pipeline

Takes an article URL via webhook, scrapes the text, and uses GPT-4o to generate a 5-tweet thread, a LinkedIn post, and a newsletter snippet — all saved to a Notion page.

## Use Case

Turn one article into three pieces of ready-to-publish content in under 30 seconds. Send any URL to this webhook from your browser (using a bookmarklet or tool like Raycast) and get a full content set waiting for you in Notion.

## Required Credentials

- **OpenAI API Key** — GPT-4o content generation
- **Notion Integration Token** — write to your content database

## Node Overview

| Node | Type | Purpose |
|------|------|---------|
| Webhook | `n8n-nodes-base.webhook` | Receives `{ "url": "https://..." }` POST |
| Fetch Article | `n8n-nodes-base.httpRequest` | Fetches the raw HTML of the article |
| Extract Text | `n8n-nodes-base.code` | Strips HTML tags, collapses whitespace, truncates to 4000 chars |
| Generate Content Variations | `n8n-nodes-base.openAi` | Returns structured JSON with tweet_thread, linkedin_post, newsletter_snippet |
| Save to Notion | `n8n-nodes-base.notion` | Creates a Notion page with all three outputs as blocks |

## Configuration

After importing:

1. **Webhook node** — copy the webhook URL; trigger it by sending: `curl -X POST https://your-n8n.com/webhook/repurpose-content -H "Content-Type: application/json" -d '{"url":"https://example.com/article"}'`
2. **Save to Notion** — replace `YOUR_NOTION_CONTENT_DATABASE_ID`; ensure the database has properties: `Source URL` (url), `Status` (select with option `draft`), `Created` (date)
3. **Generate Content Variations** — edit the system prompt to adjust tone, format, or add brand-specific instructions
4. Connect OpenAI and Notion credentials

## Example

**Input webhook body:**
```json
{ "url": "https://hbr.org/2026/04/why-small-businesses-automate-first" }
```

**Notion page created with:**
- **Tweet Thread:** 5 tweets, tweet 1 = hook, tweet 5 = CTA
- **LinkedIn Post:** 180-word professional post with hashtags
- **Newsletter Snippet:** 90-word teaser paragraph
```

- [ ] **Step 4: Commit**

```bash
git add workflows/social/content-repurpose-pipeline/
git commit -m "feat: add content-repurpose-pipeline workflow"
```

---

## Task 12: Workflow 7 — newsletter-subscriber-to-crm

**Files:**
- Create: `workflows/lead-gen/newsletter-subscriber-to-crm/workflow.json`
- Create: `workflows/lead-gen/newsletter-subscriber-to-crm/README.md`

- [ ] **Step 1: Write workflow.json**

```json
{
  "id": "a1b2c3d4-0007-4abc-8def-000000000007",
  "meta": {
    "instanceId": "",
    "templateCredsSetupCompleted": true
  },
  "name": "Newsletter Subscriber to CRM",
  "nodes": [
    {
      "id": "node-007-webhook",
      "name": "Beehiiv Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [240, 300],
      "parameters": {
        "path": "beehiiv-subscriber",
        "httpMethod": "POST",
        "responseMode": "onReceived",
        "options": {}
      }
    },
    {
      "id": "node-007-set",
      "name": "Map Subscriber Fields",
      "type": "n8n-nodes-base.set",
      "typeVersion": 3,
      "position": [460, 300],
      "parameters": {
        "assignments": {
          "assignments": [
            {
              "id": "assign-007-001",
              "name": "email",
              "value": "={{ $json.data?.email ?? $json.email ?? '' }}",
              "type": "string"
            },
            {
              "id": "assign-007-002",
              "name": "name",
              "value": "={{ $json.data?.name ?? $json.name ?? '' }}",
              "type": "string"
            },
            {
              "id": "assign-007-003",
              "name": "status",
              "value": "={{ $json.data?.status ?? $json.status ?? 'active' }}",
              "type": "string"
            },
            {
              "id": "assign-007-004",
              "name": "source",
              "value": "beehiiv",
              "type": "string"
            },
            {
              "id": "assign-007-005",
              "name": "subscribed_at",
              "value": "={{ new Date().toISOString() }}",
              "type": "string"
            }
          ]
        },
        "options": {}
      }
    },
    {
      "id": "node-007-check",
      "name": "Check If Email Exists",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4,
      "position": [680, 300],
      "parameters": {
        "method": "GET",
        "url": "=https://YOUR_BASEROW_INSTANCE/api/database/rows/table/YOUR_SUBSCRIBERS_TABLE_ID/?user_field_names=true&search={{ encodeURIComponent($json.email) }}&filter__field_Email__equal={{ encodeURIComponent($json.email) }}",
        "sendHeaders": true,
        "headerParameters": {
          "parameters": [
            { "name": "Authorization", "value": "Token YOUR_BASEROW_API_TOKEN" }
          ]
        },
        "options": {}
      }
    },
    {
      "id": "node-007-if",
      "name": "Exists?",
      "type": "n8n-nodes-base.if",
      "typeVersion": 2,
      "position": [900, 300],
      "parameters": {
        "conditions": {
          "options": {
            "caseSensitive": false,
            "leftValue": "",
            "typeValidation": "loose"
          },
          "conditions": [
            {
              "id": "cond-007-001",
              "leftValue": "={{ $json.count }}",
              "rightValue": 0,
              "operator": {
                "type": "number",
                "operation": "gt"
              }
            }
          ],
          "combinator": "and"
        },
        "looseTypeValidation": true
      }
    },
    {
      "id": "node-007-update",
      "name": "Update Subscriber",
      "type": "n8n-nodes-base.baserow",
      "typeVersion": 1,
      "position": [1120, 200],
      "parameters": {
        "operation": "update",
        "tableId": "YOUR_SUBSCRIBERS_TABLE_ID",
        "id": "={{ $json.results[0].id }}",
        "fieldsUi": {
          "fieldValues": [
            { "fieldId": "Status", "fieldValue": "={{ $('Map Subscriber Fields').item.json.status }}" },
            { "fieldId": "Last Seen", "fieldValue": "={{ new Date().toISOString() }}" }
          ]
        }
      },
      "credentials": {
        "baserowApi": {
          "id": "REPLACE_WITH_YOUR_CREDENTIAL_ID",
          "name": "Baserow account"
        }
      }
    },
    {
      "id": "node-007-create",
      "name": "Create Subscriber",
      "type": "n8n-nodes-base.baserow",
      "typeVersion": 1,
      "position": [1120, 400],
      "parameters": {
        "operation": "create",
        "tableId": "YOUR_SUBSCRIBERS_TABLE_ID",
        "fieldsUi": {
          "fieldValues": [
            { "fieldId": "Email", "fieldValue": "={{ $('Map Subscriber Fields').item.json.email }}" },
            { "fieldId": "Name", "fieldValue": "={{ $('Map Subscriber Fields').item.json.name }}" },
            { "fieldId": "Status", "fieldValue": "={{ $('Map Subscriber Fields').item.json.status }}" },
            { "fieldId": "Source", "fieldValue": "beehiiv" },
            { "fieldId": "Subscribed At", "fieldValue": "={{ $('Map Subscriber Fields').item.json.subscribed_at }}" }
          ]
        }
      },
      "credentials": {
        "baserowApi": {
          "id": "REPLACE_WITH_YOUR_CREDENTIAL_ID",
          "name": "Baserow account"
        }
      }
    }
  ],
  "connections": {
    "Beehiiv Webhook": {
      "main": [[{ "node": "Map Subscriber Fields", "type": "main", "index": 0 }]]
    },
    "Map Subscriber Fields": {
      "main": [[{ "node": "Check If Email Exists", "type": "main", "index": 0 }]]
    },
    "Check If Email Exists": {
      "main": [[{ "node": "Exists?", "type": "main", "index": 0 }]]
    },
    "Exists?": {
      "main": [
        [{ "node": "Update Subscriber", "type": "main", "index": 0 }],
        [{ "node": "Create Subscriber", "type": "main", "index": 0 }]
      ]
    }
  },
  "pinData": {},
  "active": false,
  "settings": { "executionOrder": "v1" },
  "staticData": null,
  "tags": [],
  "versionId": "v1b2c3d4-0007-4abc-8def-000000000007"
}
```

- [ ] **Step 2: Validate JSON**

```bash
python3 -m json.tool workflows/lead-gen/newsletter-subscriber-to-crm/workflow.json > /dev/null && echo "Valid JSON"
```

- [ ] **Step 3: Write README.md**

```markdown
# Newsletter Subscriber to CRM

Syncs every new Beehiiv subscriber to a Baserow CRM table, creating a new row or updating an existing one if the email already exists.

## Use Case

Keep your newsletter subscriber list and CRM in sync automatically. Every time someone subscribes (or re-subscribes) to your Beehiiv newsletter, this workflow checks if their email already exists in Baserow. If yes, it updates their status. If no, it creates a new CRM row.

## Required Credentials

- **Baserow API Key** — read and write access to your subscribers table (also used directly in the HTTP Request node for the existence check)

## Node Overview

| Node | Type | Purpose |
|------|------|---------|
| Beehiiv Webhook | `n8n-nodes-base.webhook` | Receives Beehiiv `subscriber.created` events |
| Map Subscriber Fields | `n8n-nodes-base.set` | Normalises Beehiiv payload to standard fields |
| Check If Email Exists | `n8n-nodes-base.httpRequest` | Queries Baserow REST API for an existing row with this email |
| Exists? | `n8n-nodes-base.if` | Routes to update (true) or create (false) |
| Update Subscriber | `n8n-nodes-base.baserow` | Updates Status and Last Seen on existing row |
| Create Subscriber | `n8n-nodes-base.baserow` | Creates a new CRM row with all fields |

## Configuration

After importing:

1. **Beehiiv Webhook** — copy the webhook URL; add it in Beehiiv under **Settings → Integrations → Webhooks** for the `subscriber.created` and `subscriber.updated` events
2. **Check If Email Exists** — replace `YOUR_BASEROW_INSTANCE` (e.g. `baserow.yourdomain.com`), `YOUR_SUBSCRIBERS_TABLE_ID`, and `YOUR_BASEROW_API_TOKEN`
3. **Update Subscriber + Create Subscriber** — replace `YOUR_SUBSCRIBERS_TABLE_ID`; ensure your Baserow table has columns: `Email`, `Name`, `Status`, `Source`, `Subscribed At`, `Last Seen`
4. Connect Baserow credentials on both Baserow nodes

## Example

**Beehiiv webhook payload:**
```json
{
  "event": "subscriber.created",
  "data": {
    "email": "alex@example.com",
    "name": "Alex Stavros",
    "status": "active"
  }
}
```

**Result (new subscriber):** New Baserow row created with Source = `beehiiv`, Status = `active`  
**Result (existing subscriber):** Existing row updated with new Status and current timestamp in Last Seen
```

- [ ] **Step 4: Commit**

```bash
git add workflows/lead-gen/newsletter-subscriber-to-crm/
git commit -m "feat: add newsletter-subscriber-to-crm workflow"
```

---

## Task 13: Workflow 8 — abandoned-lead-followup

**Files:**
- Create: `workflows/lead-gen/abandoned-lead-followup/workflow.json`
- Create: `workflows/lead-gen/abandoned-lead-followup/README.md`

- [ ] **Step 1: Write workflow.json**

```json
{
  "id": "a1b2c3d4-0008-4abc-8def-000000000008",
  "meta": {
    "instanceId": "",
    "templateCredsSetupCompleted": true
  },
  "name": "Abandoned Lead Follow-up",
  "nodes": [
    {
      "id": "node-008-schedule",
      "name": "Daily 8am",
      "type": "n8n-nodes-base.scheduleTrigger",
      "typeVersion": 1,
      "position": [240, 300],
      "parameters": {
        "rule": {
          "interval": [
            {
              "field": "cronExpression",
              "expression": "0 8 * * 1-5"
            }
          ]
        }
      }
    },
    {
      "id": "node-008-baserow",
      "name": "Get Stale Leads",
      "type": "n8n-nodes-base.baserow",
      "typeVersion": 1,
      "position": [460, 300],
      "parameters": {
        "operation": "getAll",
        "tableId": "YOUR_LEADS_TABLE_ID",
        "returnAll": true,
        "filters": {
          "filters": [
            {
              "field": "Status",
              "condition": "equal",
              "value": "lead"
            }
          ]
        },
        "options": {}
      },
      "credentials": {
        "baserowApi": {
          "id": "REPLACE_WITH_YOUR_CREDENTIAL_ID",
          "name": "Baserow account"
        }
      }
    },
    {
      "id": "node-008-if",
      "name": "Not Contacted in 3 Days?",
      "type": "n8n-nodes-base.if",
      "typeVersion": 2,
      "position": [680, 300],
      "parameters": {
        "conditions": {
          "options": {
            "caseSensitive": false,
            "leftValue": "",
            "typeValidation": "loose"
          },
          "conditions": [
            {
              "id": "cond-008-001",
              "leftValue": "={{ $json.last_contacted ? new Date($json.last_contacted) < new Date(Date.now() - 3 * 24 * 60 * 60 * 1000) : true }}",
              "rightValue": true,
              "operator": {
                "type": "boolean",
                "operation": "true"
              }
            }
          ],
          "combinator": "and"
        },
        "looseTypeValidation": true
      }
    },
    {
      "id": "node-008-email",
      "name": "Send Follow-up Email",
      "type": "n8n-nodes-base.emailSend",
      "typeVersion": 2,
      "position": [900, 200],
      "parameters": {
        "fromEmail": "hello@yourcompany.com",
        "toEmail": "={{ $json.email }}",
        "subject": "Quick follow-up from Your Company",
        "message": "=Hi {{ $json.name }},\n\nI wanted to follow up — did you have a chance to think about what you reached out about?\n\nI'd love to find a time to chat and see if we can help. Even a 15-minute call could be useful.\n\nIf you're not interested, no worries at all — just let me know and I won't follow up again.\n\nBest,\nYour Name\nYour Company",
        "options": {}
      },
      "credentials": {
        "smtp": {
          "id": "REPLACE_WITH_YOUR_CREDENTIAL_ID",
          "name": "SMTP account"
        }
      }
    },
    {
      "id": "node-008-update",
      "name": "Update Last Contacted",
      "type": "n8n-nodes-base.baserow",
      "typeVersion": 1,
      "position": [1120, 200],
      "parameters": {
        "operation": "update",
        "tableId": "YOUR_LEADS_TABLE_ID",
        "id": "={{ $json.id }}",
        "fieldsUi": {
          "fieldValues": [
            { "fieldId": "last_contacted", "fieldValue": "={{ new Date().toISOString() }}" },
            { "fieldId": "follow_up_count", "fieldValue": "={{ ($json.follow_up_count ?? 0) + 1 }}" }
          ]
        }
      },
      "credentials": {
        "baserowApi": {
          "id": "REPLACE_WITH_YOUR_CREDENTIAL_ID",
          "name": "Baserow account"
        }
      }
    }
  ],
  "connections": {
    "Daily 8am": {
      "main": [[{ "node": "Get Stale Leads", "type": "main", "index": 0 }]]
    },
    "Get Stale Leads": {
      "main": [[{ "node": "Not Contacted in 3 Days?", "type": "main", "index": 0 }]]
    },
    "Not Contacted in 3 Days?": {
      "main": [
        [{ "node": "Send Follow-up Email", "type": "main", "index": 0 }],
        []
      ]
    },
    "Send Follow-up Email": {
      "main": [[{ "node": "Update Last Contacted", "type": "main", "index": 0 }]]
    }
  },
  "pinData": {},
  "active": false,
  "settings": { "executionOrder": "v1" },
  "staticData": null,
  "tags": [],
  "versionId": "v1b2c3d4-0008-4abc-8def-000000000008"
}
```

- [ ] **Step 2: Validate JSON**

```bash
python3 -m json.tool workflows/lead-gen/abandoned-lead-followup/workflow.json > /dev/null && echo "Valid JSON"
```

- [ ] **Step 3: Write README.md**

```markdown
# Abandoned Lead Follow-up

Runs every weekday morning, finds leads that haven't been contacted in 3+ days, sends a follow-up email to each one, and records the contact timestamp in Baserow.

## Use Case

Stop losing warm leads to silence. This workflow automatically identifies leads in your Baserow table that have gone quiet for 3 or more days and sends a short, human-feeling follow-up email. The `last_contacted` field is updated after each send, so the same lead won't be emailed again until another 3 days have passed.

## Required Credentials

- **Baserow API Key** — read and write access to your leads table
- **SMTP** — outbound email for follow-up messages

## Node Overview

| Node | Type | Purpose |
|------|------|---------|
| Daily 8am | `n8n-nodes-base.scheduleTrigger` | Triggers Monday–Friday at 08:00 |
| Get Stale Leads | `n8n-nodes-base.baserow` | Fetches all rows where Status = `lead` |
| Not Contacted in 3 Days? | `n8n-nodes-base.if` | Filters to leads where `last_contacted` is >3 days ago or empty |
| Send Follow-up Email | `n8n-nodes-base.emailSend` | Sends a short, personal follow-up to the lead |
| Update Last Contacted | `n8n-nodes-base.baserow` | Sets `last_contacted` to now and increments `follow_up_count` |

## Configuration

After importing:

1. **Get Stale Leads + Update Last Contacted** — replace `YOUR_LEADS_TABLE_ID` in both Baserow nodes
2. **Baserow columns required:** `Status` (text, value `lead`), `last_contacted` (date), `email` (text), `name` (text), `follow_up_count` (number). Adjust `fieldId` values to match your actual column names.
3. **Send Follow-up Email** — update `fromEmail` and personalise the message body. Add your name and company name.
4. To stop following up after a certain count, add an IF node between "Get Stale Leads" and "Not Contacted in 3 Days?" filtering for `follow_up_count < 3`.
5. Connect credentials: Baserow account, SMTP account

## Example

**Baserow lead row:**
```json
{
  "id": 15,
  "name": "Elena Vassilou",
  "email": "elena@example.com",
  "Status": "lead",
  "last_contacted": "2026-04-18T09:00:00Z",
  "follow_up_count": 0
}
```

**Email sent on 2026-04-22:**
> Subject: Quick follow-up from Your Company  
> Hi Elena, I wanted to follow up — did you have a chance to think about what you reached out about?...

**Baserow after:** `last_contacted = 2026-04-22T08:01:00Z`, `follow_up_count = 1`
```

- [ ] **Step 4: Commit**

```bash
git add workflows/lead-gen/abandoned-lead-followup/
git commit -m "feat: add abandoned-lead-followup workflow"
```

---

## Task 14: Workflow 9 — weekly-business-digest

**Files:**
- Create: `workflows/reporting/weekly-business-digest/workflow.json`
- Create: `workflows/reporting/weekly-business-digest/README.md`

- [ ] **Step 1: Write workflow.json**

```json
{
  "id": "a1b2c3d4-0009-4abc-8def-000000000009",
  "meta": {
    "instanceId": "",
    "templateCredsSetupCompleted": true
  },
  "name": "Weekly Business Digest",
  "nodes": [
    {
      "id": "node-009-schedule",
      "name": "Monday 8am",
      "type": "n8n-nodes-base.scheduleTrigger",
      "typeVersion": 1,
      "position": [240, 300],
      "parameters": {
        "rule": {
          "interval": [
            {
              "field": "cronExpression",
              "expression": "0 8 * * 1"
            }
          ]
        }
      }
    },
    {
      "id": "node-009-leads",
      "name": "Get New Leads",
      "type": "n8n-nodes-base.baserow",
      "typeVersion": 1,
      "position": [460, 200],
      "parameters": {
        "operation": "getAll",
        "tableId": "YOUR_LEADS_TABLE_ID",
        "returnAll": true,
        "filters": {
          "filters": [
            {
              "field": "Created At",
              "condition": "date_after",
              "value": "={{ new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0] }}"
            }
          ]
        },
        "options": {}
      },
      "credentials": {
        "baserowApi": {
          "id": "REPLACE_WITH_YOUR_CREDENTIAL_ID",
          "name": "Baserow account"
        }
      }
    },
    {
      "id": "node-009-invoices",
      "name": "Get Invoices",
      "type": "n8n-nodes-base.baserow",
      "typeVersion": 1,
      "position": [460, 400],
      "parameters": {
        "operation": "getAll",
        "tableId": "YOUR_INVOICES_TABLE_ID",
        "returnAll": true,
        "options": {}
      },
      "credentials": {
        "baserowApi": {
          "id": "REPLACE_WITH_YOUR_CREDENTIAL_ID",
          "name": "Baserow account"
        }
      }
    },
    {
      "id": "node-009-code",
      "name": "Aggregate Stats",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [680, 300],
      "parameters": {
        "jsCode": "const allItems = $input.all();\n\n// Separate leads and invoices by checking for discriminating fields\nconst leads = allItems.filter(i => i.json.Status !== undefined && i.json.invoice_number === undefined);\nconst invoices = allItems.filter(i => i.json.invoice_number !== undefined);\n\nconst newLeadsCount = leads.length;\nconst newLeadsList = leads.slice(0, 5).map(l => `<li>${l.json.name ?? 'Unknown'} (${l.json.email ?? ''})</li>`).join('');\n\nconst paidInvoices = invoices.filter(i => i.json.Status === 'paid');\nconst unpaidInvoices = invoices.filter(i => i.json.Status === 'unpaid');\nconst totalRevenue = paidInvoices.reduce((sum, i) => sum + (parseFloat(i.json.amount) || 0), 0);\nconst totalOutstanding = unpaidInvoices.reduce((sum, i) => sum + (parseFloat(i.json.amount) || 0), 0);\n\nconst weekStart = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toLocaleDateString('en-GB');\nconst weekEnd = new Date().toLocaleDateString('en-GB');\n\nreturn [{\n  json: {\n    weekStart,\n    weekEnd,\n    newLeadsCount,\n    newLeadsList: newLeadsList || '<li>No new leads this week</li>',\n    paidCount: paidInvoices.length,\n    unpaidCount: unpaidInvoices.length,\n    totalRevenue: totalRevenue.toFixed(2),\n    totalOutstanding: totalOutstanding.toFixed(2)\n  }\n}];"
      }
    },
    {
      "id": "node-009-set",
      "name": "Build HTML Email",
      "type": "n8n-nodes-base.set",
      "typeVersion": 3,
      "position": [900, 300],
      "parameters": {
        "assignments": {
          "assignments": [
            {
              "id": "assign-009-001",
              "name": "html",
              "value": "=<!DOCTYPE html><html><body style=\"font-family:Arial,sans-serif;max-width:600px;margin:0 auto;padding:20px;color:#333\">\n<h1 style=\"color:#1a1a1a\">Weekly Business Digest</h1>\n<p style=\"color:#666\">{{ $json.weekStart }} — {{ $json.weekEnd }}</p>\n\n<h2>Leads</h2>\n<table style=\"width:100%;border-collapse:collapse\">\n  <tr style=\"background:#f5f5f5\">\n    <td style=\"padding:8px\"><strong>New leads this week</strong></td>\n    <td style=\"padding:8px;text-align:right\">{{ $json.newLeadsCount }}</td>\n  </tr>\n</table>\n<ul style=\"margin-top:8px\">{{ $json.newLeadsList }}</ul>\n\n<h2>Revenue</h2>\n<table style=\"width:100%;border-collapse:collapse\">\n  <tr style=\"background:#f5f5f5\">\n    <td style=\"padding:8px\"><strong>Paid invoices</strong></td>\n    <td style=\"padding:8px;text-align:right\">{{ $json.paidCount }}</td>\n  </tr>\n  <tr>\n    <td style=\"padding:8px\"><strong>Total collected</strong></td>\n    <td style=\"padding:8px;text-align:right\">€{{ $json.totalRevenue }}</td>\n  </tr>\n  <tr style=\"background:#fff3cd\">\n    <td style=\"padding:8px\"><strong>Outstanding (unpaid)</strong></td>\n    <td style=\"padding:8px;text-align:right\">€{{ $json.totalOutstanding }} ({{ $json.unpaidCount }} invoices)</td>\n  </tr>\n</table>\n\n<p style=\"color:#999;font-size:12px;margin-top:30px\">Sent automatically by n8n every Monday at 8am.</p>\n</body></html>",
              "type": "string"
            },
            {
              "id": "assign-009-002",
              "name": "subject",
              "value": "=Weekly Digest: {{ $json.newLeadsCount }} new leads | €{{ $json.totalRevenue }} collected",
              "type": "string"
            }
          ]
        },
        "options": {}
      }
    },
    {
      "id": "node-009-email",
      "name": "Email Digest to Owner",
      "type": "n8n-nodes-base.emailSend",
      "typeVersion": 2,
      "position": [1120, 300],
      "parameters": {
        "fromEmail": "digest@yourcompany.com",
        "toEmail": "owner@yourcompany.com",
        "subject": "={{ $json.subject }}",
        "message": "={{ $json.html }}",
        "options": {
          "allowUnauthorizedCerts": false
        }
      },
      "credentials": {
        "smtp": {
          "id": "REPLACE_WITH_YOUR_CREDENTIAL_ID",
          "name": "SMTP account"
        }
      }
    }
  ],
  "connections": {
    "Monday 8am": {
      "main": [
        [
          { "node": "Get New Leads", "type": "main", "index": 0 },
          { "node": "Get Invoices", "type": "main", "index": 0 }
        ]
      ]
    },
    "Get New Leads": {
      "main": [[{ "node": "Aggregate Stats", "type": "main", "index": 0 }]]
    },
    "Get Invoices": {
      "main": [[{ "node": "Aggregate Stats", "type": "main", "index": 0 }]]
    },
    "Aggregate Stats": {
      "main": [[{ "node": "Build HTML Email", "type": "main", "index": 0 }]]
    },
    "Build HTML Email": {
      "main": [[{ "node": "Email Digest to Owner", "type": "main", "index": 0 }]]
    }
  },
  "pinData": {},
  "active": false,
  "settings": { "executionOrder": "v1" },
  "staticData": null,
  "tags": [],
  "versionId": "v1b2c3d4-0009-4abc-8def-000000000009"
}
```

- [ ] **Step 2: Validate JSON**

```bash
python3 -m json.tool workflows/reporting/weekly-business-digest/workflow.json > /dev/null && echo "Valid JSON"
```

- [ ] **Step 3: Write README.md**

```markdown
# Weekly Business Digest

Every Monday at 8am, pulls new leads and invoice data from Baserow, computes a weekly summary, and emails an HTML digest to the business owner.

## Use Case

Start every Monday with a clear picture of last week. This workflow automatically compiles your key numbers — new leads, revenue collected, outstanding invoices — into a clean HTML email delivered to your inbox before your day starts. No dashboards to open, no reports to run.

## Required Credentials

- **Baserow API Key** — read access to your leads and invoices tables
- **SMTP** — outbound email for the digest

## Node Overview

| Node | Type | Purpose |
|------|------|---------|
| Monday 8am | `n8n-nodes-base.scheduleTrigger` | Triggers every Monday at 08:00 |
| Get New Leads | `n8n-nodes-base.baserow` | Fetches leads created in the last 7 days |
| Get Invoices | `n8n-nodes-base.baserow` | Fetches all invoice rows |
| Aggregate Stats | `n8n-nodes-base.code` | Computes counts, total revenue, and outstanding amount |
| Build HTML Email | `n8n-nodes-base.set` | Assembles the HTML email body and subject line |
| Email Digest to Owner | `n8n-nodes-base.emailSend` | Sends the digest to the owner's email address |

## Configuration

After importing:

1. **Get New Leads** — replace `YOUR_LEADS_TABLE_ID`; ensure your leads table has a `Created At` date field
2. **Get Invoices** — replace `YOUR_INVOICES_TABLE_ID`; ensure your invoices table has `Status` (values `paid`/`unpaid`) and `amount` (number) fields
3. **Aggregate Stats** — the Code node distinguishes leads from invoices by the presence of `invoice_number`. If your column name differs, update the `i.json.invoice_number === undefined` check
4. **Email Digest to Owner** — update `fromEmail` and `toEmail` in the Email node parameters
5. Connect credentials: Baserow account (both Baserow nodes), SMTP account

## Example

**Digest email:**
> **Subject:** Weekly Digest: 4 new leads | €3,200 collected  
> **Body:** Clean HTML table showing 4 new leads (first 5 listed by name/email), 2 paid invoices totalling €3,200, €800 outstanding (1 invoice).
```

- [ ] **Step 4: Commit**

```bash
git add workflows/reporting/weekly-business-digest/
git commit -m "feat: add weekly-business-digest workflow"
```

---

## Task 15: Workflow 10 — support-ticket-to-slack

**Files:**
- Create: `workflows/reporting/support-ticket-to-slack/workflow.json`
- Create: `workflows/reporting/support-ticket-to-slack/README.md`

- [ ] **Step 1: Write workflow.json**

```json
{
  "id": "a1b2c3d4-0010-4abc-8def-000000000010",
  "meta": {
    "instanceId": "",
    "templateCredsSetupCompleted": true
  },
  "name": "Support Ticket to Slack",
  "nodes": [
    {
      "id": "node-010-webhook",
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [240, 300],
      "parameters": {
        "path": "support-ticket",
        "httpMethod": "POST",
        "responseMode": "onReceived",
        "options": {}
      }
    },
    {
      "id": "node-010-baserow",
      "name": "Create Ticket",
      "type": "n8n-nodes-base.baserow",
      "typeVersion": 1,
      "position": [460, 300],
      "parameters": {
        "operation": "create",
        "tableId": "YOUR_TICKETS_TABLE_ID",
        "fieldsUi": {
          "fieldValues": [
            { "fieldId": "Name", "fieldValue": "={{ $json.name }}" },
            { "fieldId": "Email", "fieldValue": "={{ $json.email }}" },
            { "fieldId": "Subject", "fieldValue": "={{ $json.subject ?? 'Support request' }}" },
            { "fieldId": "Message", "fieldValue": "={{ $json.message }}" },
            { "fieldId": "Status", "fieldValue": "open" },
            { "fieldId": "Created At", "fieldValue": "={{ new Date().toISOString() }}" }
          ]
        }
      },
      "credentials": {
        "baserowApi": {
          "id": "REPLACE_WITH_YOUR_CREDENTIAL_ID",
          "name": "Baserow account"
        }
      }
    },
    {
      "id": "node-010-slack",
      "name": "Post to Slack",
      "type": "n8n-nodes-base.slack",
      "typeVersion": 2,
      "position": [680, 300],
      "parameters": {
        "resource": "message",
        "operation": "post",
        "channel": "#support",
        "text": ":tickets: *New support ticket #{{ $json.id }}*\n*From:* {{ $('Webhook').item.json.name }} ({{ $('Webhook').item.json.email }})\n*Subject:* {{ $('Webhook').item.json.subject ?? 'Support request' }}\n*Message:* {{ $('Webhook').item.json.message }}",
        "otherOptions": {}
      },
      "credentials": {
        "slackApi": {
          "id": "REPLACE_WITH_YOUR_CREDENTIAL_ID",
          "name": "Slack account"
        }
      }
    },
    {
      "id": "node-010-openai",
      "name": "Generate Suggested Reply",
      "type": "n8n-nodes-base.openAi",
      "typeVersion": 1,
      "position": [900, 300],
      "parameters": {
        "resource": "text",
        "operation": "message",
        "modelId": {
          "__rl": true,
          "value": "gpt-4o",
          "mode": "list",
          "cachedResultName": "gpt-4o"
        },
        "messages": {
          "values": [
            {
              "role": "system",
              "content": "You are a friendly and helpful customer support agent. Write a concise, professional reply to the customer's support message. Address them by name. Acknowledge their issue, provide a brief helpful response or next step, and sign off as 'The Support Team'. Keep it under 100 words."
            },
            {
              "role": "user",
              "content": "=Customer name: {{ $('Webhook').item.json.name }}\nSubject: {{ $('Webhook').item.json.subject ?? 'Support request' }}\nMessage: {{ $('Webhook').item.json.message }}"
            }
          ]
        },
        "simplify": true,
        "options": { "maxTokens": 200 }
      },
      "credentials": {
        "openAiApi": {
          "id": "REPLACE_WITH_YOUR_CREDENTIAL_ID",
          "name": "OpenAI account"
        }
      }
    },
    {
      "id": "node-010-update",
      "name": "Update Ticket with Suggestion",
      "type": "n8n-nodes-base.baserow",
      "typeVersion": 1,
      "position": [1120, 300],
      "parameters": {
        "operation": "update",
        "tableId": "YOUR_TICKETS_TABLE_ID",
        "id": "={{ $('Create Ticket').item.json.id }}",
        "fieldsUi": {
          "fieldValues": [
            { "fieldId": "AI Suggested Reply", "fieldValue": "={{ $json.choices[0].message.content }}" }
          ]
        }
      },
      "credentials": {
        "baserowApi": {
          "id": "REPLACE_WITH_YOUR_CREDENTIAL_ID",
          "name": "Baserow account"
        }
      }
    }
  ],
  "connections": {
    "Webhook": {
      "main": [[{ "node": "Create Ticket", "type": "main", "index": 0 }]]
    },
    "Create Ticket": {
      "main": [[{ "node": "Post to Slack", "type": "main", "index": 0 }]]
    },
    "Post to Slack": {
      "main": [[{ "node": "Generate Suggested Reply", "type": "main", "index": 0 }]]
    },
    "Generate Suggested Reply": {
      "main": [[{ "node": "Update Ticket with Suggestion", "type": "main", "index": 0 }]]
    }
  },
  "pinData": {},
  "active": false,
  "settings": { "executionOrder": "v1" },
  "staticData": null,
  "tags": [],
  "versionId": "v1b2c3d4-0010-4abc-8def-000000000010"
}
```

- [ ] **Step 2: Validate JSON**

```bash
python3 -m json.tool workflows/reporting/support-ticket-to-slack/workflow.json > /dev/null && echo "Valid JSON"
```

- [ ] **Step 3: Write README.md**

```markdown
# Support Ticket to Slack

Receives a contact/support form submission, creates a Baserow ticket row, posts an alert to Slack, generates an AI-suggested reply with GPT-4o, and saves the suggestion back to the ticket.

## Use Case

Give your support inbox instant visibility and a head start on every reply. The moment a customer submits a support form, your team sees it in Slack, a ticket is created in Baserow, and an AI-drafted reply is already waiting in the ticket record — ready to review, edit, and send.

## Required Credentials

- **Baserow API Key** — write access to your tickets table
- **Slack API** — post messages to your support channel
- **OpenAI API Key** — GPT-4o reply generation

## Node Overview

| Node | Type | Purpose |
|------|------|---------|
| Webhook | `n8n-nodes-base.webhook` | Receives POST from contact/support form |
| Create Ticket | `n8n-nodes-base.baserow` | Creates a new ticket row with Status = `open` |
| Post to Slack | `n8n-nodes-base.slack` | Posts a formatted alert to `#support` with ticket details |
| Generate Suggested Reply | `n8n-nodes-base.openAi` | Writes a draft reply using ticket context |
| Update Ticket with Suggestion | `n8n-nodes-base.baserow` | Saves the AI reply to the `AI Suggested Reply` field |

## Configuration

After importing:

1. **Webhook** — copy the webhook URL and add it as your support form action
2. **Create Ticket + Update Ticket** — replace `YOUR_TICKETS_TABLE_ID` in both Baserow nodes; ensure your table has columns: `Name`, `Email`, `Subject`, `Message`, `Status`, `Created At`, `AI Suggested Reply`
3. **Post to Slack** — change `#support` to your actual Slack channel name
4. **Generate Suggested Reply** — edit the system prompt with your product/service context for more relevant suggestions
5. Connect credentials: Baserow account (both nodes), Slack account, OpenAI account

## Example

**Form submission:**
```json
{
  "name": "Dimitris K.",
  "email": "dimitris@example.com",
  "subject": "Can't log in to my account",
  "message": "I keep getting an error when I try to log in. It says 'invalid credentials' but I'm sure my password is correct."
}
```

**Slack alert posted to #support:**
> 🎫 **New support ticket #23**  
> **From:** Dimitris K. (dimitris@example.com)  
> **Subject:** Can't log in to my account  
> **Message:** I keep getting an error...

**AI Suggested Reply saved to Baserow:**
> Hi Dimitris, sorry to hear you're having trouble logging in! This is usually caused by a browser-cached session. Please try clearing your cookies or using an incognito window. If that doesn't help, use the "Forgot password" link to reset. Let us know how it goes! — The Support Team
```

- [ ] **Step 4: Commit**

```bash
git add workflows/reporting/support-ticket-to-slack/
git commit -m "feat: add support-ticket-to-slack workflow"
```

---

## Task 16: Git Init, Initial Commit, and GitHub Push

**Files:** No new files — git and GitHub setup only.

- [ ] **Step 1: Initialise git**

```bash
git init
```

Expected: `Initialized empty Git repository in .../n8n-smb-workflows/.git/`

(Skip this step if git is already initialised from previous commits — check with `git status`)

- [ ] **Step 2: Stage all files**

```bash
git add -A
git status
```

Expected: All files listed as "Changes to be committed". Verify no `.env` or credential files are staged.

- [ ] **Step 3: Create initial commit**

```bash
git commit -m "Initial commit: 10 n8n workflow templates for SMB automation"
```

Expected: Commit created showing number of files changed.

- [ ] **Step 4: Create GitHub repo and push**

```bash
gh repo create n8n-smb-workflows \
  --public \
  --description "Ready-to-import n8n workflow templates for small business automation. Covers CRM, email, social media, lead gen, and reporting." \
  --source=. \
  --push
```

Expected: Repo created at `https://github.com/YOUR_USERNAME/n8n-smb-workflows` and pushed.

- [ ] **Step 5: Add GitHub topics**

```bash
gh repo edit n8n-smb-workflows \
  --add-topic n8n \
  --add-topic automation \
  --add-topic workflows \
  --add-topic small-business \
  --add-topic no-code \
  --add-topic self-hosted
```

Expected: No error output. Verify at `https://github.com/YOUR_USERNAME/n8n-smb-workflows`.

- [ ] **Step 6: Verify**

```bash
gh repo view n8n-smb-workflows
```

Expected: Repo info shown with description, topics, and public visibility.

---

## Self-Review Checklist

**Spec coverage:**
- [x] All 10 workflows present with workflow.json + README.md each
- [x] Directory structure matches spec exactly
- [x] All 10 per-workflow READMEs contain: description, use case, credentials, node overview, configuration, example input/output
- [x] Main README contains: hero section, workflow table with all 10, import steps, prerequisites, contributing link, license
- [x] CONTRIBUTING.md contains contribution steps, required README fields, workflow.json requirements
- [x] docs/how-to-import.md covers method A (JSON paste), method B (file upload), testing, troubleshooting
- [x] docs/credentials-setup.md covers all 6 services: Baserow, Notion, OpenAI, Gmail OAuth2, Slack, SMTP
- [x] git init + initial commit with exact specified message
- [x] `gh repo create` with exact specified flags
- [x] `gh repo edit` with all 6 specified topics

**Placeholder scan:**
- All `YOUR_*` strings in workflow JSONs are config values requiring user replacement — not missing implementation. Each workflow's README documents exactly what to replace.
- Credential IDs use `"REPLACE_WITH_YOUR_CREDENTIAL_ID"` consistently across all 10 workflows.

**JSON consistency:**
- All workflow JSONs use the same top-level structure: `id`, `meta`, `name`, `nodes`, `connections`, `pinData`, `active`, `settings`, `staticData`, `tags`, `versionId`
- Node IDs follow `node-00N-purpose` convention throughout
- Connection keys match node `name` fields exactly in all 10 workflows
