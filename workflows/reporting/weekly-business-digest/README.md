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
