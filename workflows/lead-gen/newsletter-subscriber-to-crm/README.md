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
