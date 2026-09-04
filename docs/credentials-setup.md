# Credentials Setup

Instructions for creating the credentials used across workflows in this repository.

In n8n, credentials are created via **Settings → Credentials → + Add Credential**.

---

## Baserow API Key

Used by: Lead Capture to Baserow, Contact Form Team Alert, AI Email Auto-Reply, Invoice Reminder, Content Repurpose Pipeline, Newsletter Subscriber to CRM, Abandoned Lead Follow-up, Weekly Business Digest, Support Ticket Alert, StackSignal Weekly Draft Generator, StackSignal RSS Feed Server, StackSignal Manual RSS Push

Baserow is this repo's standard for structured data storage — CRM rows, logs, content queues, tickets. If a workflow needs to store or read rows, it uses this.

1. Log in to your Baserow instance
2. Go to **Profile → API tokens** → click **Create token**
3. Name it (e.g. "n8n"), set permissions to **Read & Write** for the relevant databases
4. Copy the token
5. In n8n: **+ Add Credential** → search "Baserow" → paste the token and your Baserow host URL (e.g. `https://baserow.yourdomain.com`)

---

## OpenAI API Key

Used by: AI Email Auto-Reply, RSS to Social Post, Content Repurpose Pipeline, Support Ticket Alert

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

## Discord Webhook

Used by: Contact Form Team Alert, Support Ticket Alert, Error Handler, StackSignal Weekly Draft Generator, StackSignal Manual RSS Push

Discord is this repo's standard for team/ops alerts — every workflow that used to post to Slack, plus the error handler, uses this. Webhook mode needs no app registration or bot install, unlike Slack's OAuth flow — this is the whole setup:

1. In your Discord server: **Server Settings → Integrations → Webhooks → New Webhook**
2. Name it, pick the target channel, copy the **Webhook URL** (`https://discord.com/api/webhooks/...`)
3. In n8n: **+ Add Credential** → search "Discord" → paste the URL into **Webhook URL**

Each workflow's Discord node already has `authentication: webhook` set — you only need to attach the credential, no per-node config.

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

## Beehiiv RSS Integration

Used by: StackSignal RSS Feed Server

The opposite direction from the webhook above — Beehiiv *polls* an RSS feed this workflow serves, rather than pushing to it. Not an n8n credential; configured on Beehiiv's side.

1. Copy the RSS Feed Server workflow's webhook URL after importing and activating (keep the path stable — see the workflow's own sticky note)
2. In Beehiiv: **Settings → Integrations → RSS** → paste the URL

---

## RSS Push Token (Header Auth)

Used by: StackSignal Manual RSS Push

An n8n **Header Auth** credential attached directly to the webhook node — it rejects an unauthorized request before the workflow even runs, so no token comparison lives in workflow code.

1. Generate any random string you'll treat as a secret (e.g. `openssl rand -hex 32`)
2. In n8n: **+ Add Credential** → search "Header Auth" → set **Name** to `X-RSS-Token` and **Value** to the string you generated
3. Attach the credential to the **Manual Push Webhook** node's Authentication field
4. Callers must send it as an `X-RSS-Token` header on every request

---

## SMTP (Email Send)

Used by: Lead Capture to Baserow, Invoice Reminder, Abandoned Lead Follow-up, Weekly Business Digest

These are customer-facing/owner-digest emails, not team alerts — deliberately kept on plain SMTP rather than Discord, since the recipient here is the end customer or a plain inbox digest, not a team channel.

You need an SMTP host, port, username, and password. Common options:

| Provider | Host | Port | Notes |
|----------|------|------|-------|
| Gmail | `smtp.gmail.com` | 587 | Requires an App Password (not your main password) |
| Infomaniak | `mail.infomaniak.com` | 587 | Use your Infomaniak email credentials |
| Mailgun | `smtp.mailgun.org` | 587 | Get credentials from Mailgun dashboard |
| AWS SES | `email-smtp.<region>.amazonaws.com` | 587 | Create SMTP credentials in AWS IAM |

In n8n: **+ Add Credential** → search "SMTP" → fill in host, port, username, password → toggle **SSL/TLS** if required by your provider.

For Gmail App Passwords: [https://support.google.com/accounts/answer/185833](https://support.google.com/accounts/answer/185833)
