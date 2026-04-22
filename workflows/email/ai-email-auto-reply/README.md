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
