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
