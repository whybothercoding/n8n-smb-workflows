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
