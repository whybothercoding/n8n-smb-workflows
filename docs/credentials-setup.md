# Credentials Setup

Instructions for creating the credentials used across workflows in this repository.

In n8n, credentials are created via **Settings → Credentials → + Add Credential**.

---

## Baserow API Key

Used by: Lead Capture to Baserow, Invoice Reminder, Newsletter Subscriber to CRM, Abandoned Lead Follow-up, Weekly Business Digest, Support Ticket to Slack, StackSignal Weekly Draft Generator

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

Used by: Contact Form to Notion, Support Ticket to Slack, StackSignal Weekly Draft Generator (OAuth)

**Option A — Incoming Webhook (simpler, for posting only)**
1. Go to [https://api.slack.com/apps](https://api.slack.com/apps) → **Create New App** → **From scratch**
2. Enable **Incoming Webhooks** → **Add New Webhook to Workspace** → select a channel
3. Copy the webhook URL
4. In n8n: **+ Add Credential** → search "Slack" → choose **Webhook** type → paste the URL

**Option B — OAuth (for reading and posting)**
1. Create a Slack app at [https://api.slack.com/apps](https://api.slack.com/apps)
2. Under **OAuth & Permissions**, add Bot Token Scopes: `chat:write`, `channels:read`
3. Install the app to your workspace and copy the **Bot User OAuth Token**
4. In n8n: **+ Add Credential** → search "Slack" → choose **Access Token** → paste the token (StackSignal Weekly Draft Generator specifically uses the **OAuth2** credential type — same app, choose OAuth2 instead of Access Token when creating the credential)

---

## Google Gemini API

Used by: StackSignal Weekly Draft Generator

1. Go to [Google AI Studio](https://aistudio.google.com/apikey) and create an API key
2. In n8n: **+ Add Credential** → search "Google Gemini" → paste the API key

---

## LinkedIn Access Token

Used by: RSS to Social Post

Set directly as a header value in the HTTP Request node — not an n8n credential type.

1. Create an app at the [LinkedIn Developer Portal](https://developer.linkedin.com/) with `w_member_social` permission
2. Generate an access token for your app
3. Get your LinkedIn person URN by calling `https://api.linkedin.com/v2/me` with the token
4. In the workflow's **Post to LinkedIn** node, replace `REPLACE_WITH_YOUR_LINKEDIN_ACCESS_TOKEN` in the Authorization header and `YOUR_LINKEDIN_PERSON_ID` in the body

---

## Beehiiv Webhook

Used by: Newsletter Subscriber to CRM

Configured on Beehiiv's side, not an n8n credential — the workflow's Webhook node just needs to be the receiving end.

1. Copy the workflow's webhook URL after importing
2. In Beehiiv: **Settings → Integrations → Webhooks** → add the URL for the `subscriber.created` and `subscriber.updated` events

---

## SMTP (Email Send)

Used by: Lead Capture to Baserow, Invoice Reminder, Abandoned Lead Follow-up, Weekly Business Digest, Error Handler

You need an SMTP host, port, username, and password. Common options:

| Provider | Host | Port | Notes |
|----------|------|------|-------|
| Gmail | `smtp.gmail.com` | 587 | Requires an App Password (not your main password) |
| Infomaniak | `mail.infomaniak.com` | 587 | Use your Infomaniak email credentials |
| Mailgun | `smtp.mailgun.org` | 587 | Get credentials from Mailgun dashboard |
| AWS SES | `email-smtp.<region>.amazonaws.com` | 587 | Create SMTP credentials in AWS IAM |

In n8n: **+ Add Credential** → search "SMTP" → fill in host, port, username, password → toggle **SSL/TLS** if required by your provider.

For Gmail App Passwords: [https://support.google.com/accounts/answer/185833](https://support.google.com/accounts/answer/185833)
