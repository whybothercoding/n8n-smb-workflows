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
