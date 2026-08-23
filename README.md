# n8n SMB Workflows

> Ready-to-import n8n workflow templates for small business automation.

[![CI](https://github.com/whybothercoding/n8n-smb-workflows/actions/workflows/ci.yml/badge.svg)](https://github.com/whybothercoding/n8n-smb-workflows/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![n8n](https://img.shields.io/badge/n8n-compatible-orange)](https://n8n.io)
<!-- WORKFLOW_COUNT_BADGE:START -->[![Workflows: 14](https://img.shields.io/badge/workflows-14-blue)](#whats-inside)<!-- WORKFLOW_COUNT_BADGE:END -->

A curated library of production-ready n8n workflows covering the most common automation needs for small businesses: lead capture, email handling, social media, reporting, and more. Every workflow ships as a clean JSON export — import directly into any n8n instance, connect your credentials, and activate.

---

## How Each Workflow Works

Every workflow follows the same import-and-activate pattern:

```
Trigger (Webhook · Schedule · Gmail poll)
  └─▶  Normalize / Filter
          └─▶  Action (CRM · Email · Social · AI)
                  └─▶  Log / Confirm / Alert
```

All workflows ship as `active: false`. Import → connect credentials → activate. Each workflow's own README also includes a Mermaid flow diagram generated straight from its `workflow.json` — see [How This Repo Is Tested](#how-this-repo-is-tested).

---

## What's Inside

<!-- WORKFLOWS_TABLE:START -->
| # | Workflow | Category | Description |
|---|----------|----------|-------------|
| 1 | [Lead Capture to Baserow](workflows/crm/lead-capture-to-baserow/) | CRM | Receives a contact form submission via webhook, normalises the fields, saves the lead to a Baserow table, and sends the submitter a confirmation email. |
| 2 | [Contact Form to Notion](workflows/crm/contact-form-to-notion/) | CRM | Receives a contact form submission via webhook, creates a Notion database page, and posts a summary to a Slack channel. |
| 3 | [AI Email Auto-Reply](workflows/email/ai-email-auto-reply/) | Email | Monitors Gmail for new unread emails, generates a draft reply with GPT-4o, and logs the interaction to Notion. |
| 4 | [Invoice Reminder](workflows/email/invoice-reminder/) | Email | Runs every weekday morning, fetches unpaid overdue invoices from Baserow, sends a reminder email to each client, and marks the reminder as sent. |
| 5 | [RSS to Social Post](workflows/social/rss-to-social-post/) | Social | Reads new items from an RSS feed hourly, rewrites each item as a LinkedIn post using GPT-4o, and publishes directly to LinkedIn. |
| 6 | [Content Repurpose Pipeline](workflows/social/content-repurpose-pipeline/) | Social | Takes an article URL via webhook, scrapes the text, and uses GPT-4o to generate a 5-tweet thread, a LinkedIn post, and a newsletter snippet — all saved to a Notion page. |
| 7 | [Newsletter Subscriber to CRM](workflows/lead-gen/newsletter-subscriber-to-crm/) | Lead Gen | Syncs every new Beehiiv subscriber to a Baserow CRM table, creating a new row or updating an existing one if the email already exists. |
| 8 | [Abandoned Lead Follow-up](workflows/lead-gen/abandoned-lead-followup/) | Lead Gen | Runs every weekday morning, finds leads that haven't been contacted in 3+ days, sends a follow-up email to each one, and records the contact timestamp in Baserow. |
| 9 | [Weekly Business Digest](workflows/reporting/weekly-business-digest/) | Reporting | Every Monday at 8am, pulls new leads and invoice data from Baserow, computes a weekly summary, and emails an HTML digest to the business owner. |
| 10 | [Support Ticket to Slack](workflows/reporting/support-ticket-to-slack/) | Reporting | Receives a contact/support form submission, creates a Baserow ticket row, posts an alert to Slack, generates an AI-suggested reply with GPT-4o, and saves the suggestion back to the ticket. |
| 11 | [Error Handler](workflows/utilities/error-handler/) | Utilities | Centralized error handler for all other workflows in this library. When any workflow fails, n8n routes the error here and sends an alert email to the business owner. |
| 12 | [StackSignal Weekly Draft Generator](workflows/newsletter/stacksignal-weekly-draft-generator/) | Newsletter | Every Sunday evening, pulls the week's top posts from five RSS feeds, has an AI agent curate and write editorial takes on the 3–5 most relevant items, and queues a pre-populated newsletter draft for a human to finish. |
| 13 | [StackSignal RSS Feed Server](workflows/newsletter/stacksignal-rss-feed-server/) | Newsletter | Serves a live RSS feed of queued newsletter drafts over a webhook, so Beehiiv (or any RSS-polling tool) can pull drafts straight out of your Baserow content queue. |
| 14 | [StackSignal Manual RSS Push](workflows/newsletter/stacksignal-manual-rss-push/) | Newsletter | A token-authenticated webhook for manually queuing a one-off newsletter draft — for when you want to publish something outside the automated weekly cycle. |
<!-- WORKFLOWS_TABLE:END -->

*(This table is generated — see [How This Repo Is Tested](#how-this-repo-is-tested). Don't hand-edit it.)*

---

## Which Workflow Do I Need?

<!-- WORKFLOW_PICKER:START -->
| If you want to… | Use |
|---|---|
| Capture form leads into a CRM (via Baserow) | [Lead Capture to Baserow](workflows/crm/lead-capture-to-baserow/) |
| Capture form leads into a CRM (via Notion) | [Contact Form to Notion](workflows/crm/contact-form-to-notion/) |
| Auto-draft replies to inbound emails | [AI Email Auto-Reply](workflows/email/ai-email-auto-reply/) |
| Chase unpaid invoices automatically | [Invoice Reminder](workflows/email/invoice-reminder/) |
| Turn blog posts into LinkedIn content | [RSS to Social Post](workflows/social/rss-to-social-post/) |
| Repurpose any article into 3 content formats | [Content Repurpose Pipeline](workflows/social/content-repurpose-pipeline/) |
| Sync newsletter subscribers to your CRM | [Newsletter Subscriber to CRM](workflows/lead-gen/newsletter-subscriber-to-crm/) |
| Follow up with leads that went cold | [Abandoned Lead Follow-up](workflows/lead-gen/abandoned-lead-followup/) |
| Get a weekly business numbers email | [Weekly Business Digest](workflows/reporting/weekly-business-digest/) |
| Route support tickets to Slack + AI draft replies | [Support Ticket to Slack](workflows/reporting/support-ticket-to-slack/) |
| Get alerted when any workflow fails | [Error Handler](workflows/utilities/error-handler/) |
| Auto-generate a curated weekly newsletter draft | [StackSignal Weekly Draft Generator](workflows/newsletter/stacksignal-weekly-draft-generator/) |
| Turn a Baserow content queue into a pollable RSS feed | [StackSignal RSS Feed Server](workflows/newsletter/stacksignal-rss-feed-server/) |
| Manually queue a one-off newsletter draft via API | [StackSignal Manual RSS Push](workflows/newsletter/stacksignal-manual-rss-push/) |
<!-- WORKFLOW_PICKER:END -->

---

## Installation

Clone the repository to have all workflows available locally:

```bash
git clone https://github.com/whybothercoding/n8n-smb-workflows.git
cd n8n-smb-workflows
```

Or download a single workflow — navigate to any `workflow.json` on GitHub and click **Raw**, then save the file.

No dependencies to install. No build step. The files are ready to use as-is.

---

## Usage

### How to Import a Workflow

**Step 1 — Copy the workflow JSON**
Open the workflow folder, then copy the raw contents of `workflow.json`.

**Step 2 — Import into n8n**
In your n8n instance: go to **Workflows** → click the **+** button → **⋮** menu → **Import from JSON** → paste the JSON → click **Import**.

**Step 3 — Configure and activate**
Follow the workflow's `README.md` to connect credentials, update any IDs (table IDs, database IDs, channel names), then toggle the workflow **Active**.

See [docs/how-to-import.md](docs/how-to-import.md) for a detailed walkthrough, including CLI import via `n8n import:workflow`.

---

## Prerequisites

- A running n8n instance (self-hosted or cloud). See [n8n docs](https://docs.n8n.io/hosting/) for setup.
- Credentials for the services each workflow uses. See [docs/credentials-setup.md](docs/credentials-setup.md).

---

## How This Repo Is Tested

Every push and PR runs through CI ([`.github/workflows/ci.yml`](.github/workflows/ci.yml)), three layers deep:

1. **Structural + convention lint** — `bash validate.sh` (backed by `scripts/validate.py`) checks every `workflow.json` against every rule documented in [CLAUDE.md](CLAUDE.md): valid JSON, `active: false`, `executionOrder: "v1"`, `errorWorkflow` wired, credential placeholders, tag/category consistency, node-ID uniqueness and naming convention, valid UUIDs, and that every workflow folder has a matching README with all required sections and a root-table entry.
2. **Real n8n-engine import check** — CI spins up the official `n8nio/n8n` Docker image and runs `n8n import:workflow --input=...` against every single `workflow.json`, using n8n's own CLI. This is the strongest guarantee in the repo: it's not schema-checked JSON, it's JSON n8n itself has actually accepted.
3. **Secret scanning** — [gitleaks](https://github.com/gitleaks/gitleaks) scans the full git history for credentials, on top of the repo's own placeholder-pattern check.

Docs don't drift either: `python3 scripts/generate_docs.py --check` fails the build if the tables above or any workflow's Flow Diagram are out of sync with the actual `workflow.json` files — the tables and diagrams you see in this repo are generated, not hand-typed.

Run the fast checks locally before opening a PR:

```bash
bash validate.sh
python3 scripts/generate_docs.py --check
```

The n8n import check and gitleaks run in CI; reproduce them locally with Docker / a local gitleaks install if you want to check before pushing.

---

## Contributing

Contributions welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for the workflow template and PR process.

---

## License

MIT — see [LICENSE](LICENSE).
