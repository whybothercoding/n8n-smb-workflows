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
