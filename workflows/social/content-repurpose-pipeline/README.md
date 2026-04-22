# Content Repurpose Pipeline

Takes an article URL via webhook, scrapes the text, and uses GPT-4o to generate a 5-tweet thread, a LinkedIn post, and a newsletter snippet — all saved to a Notion page.

## Use Case

Turn one article into three pieces of ready-to-publish content in under 30 seconds. Send any URL to this webhook from your browser (using a bookmarklet or tool like Raycast) and get a full content set waiting for you in Notion.

## Required Credentials

- **OpenAI API Key** — GPT-4o content generation
- **Notion Integration Token** — write to your content database

## Node Overview

| Node | Type | Purpose |
|------|------|---------|
| Webhook | `n8n-nodes-base.webhook` | Receives `{ "url": "https://..." }` POST |
| Fetch Article | `n8n-nodes-base.httpRequest` | Fetches the raw HTML of the article |
| Extract Text | `n8n-nodes-base.code` | Strips HTML tags, collapses whitespace, truncates to 4000 chars |
| Generate Content Variations | `n8n-nodes-base.openAi` | Returns structured JSON with tweet_thread, linkedin_post, newsletter_snippet |
| Save to Notion | `n8n-nodes-base.notion` | Creates a Notion page with all three outputs as blocks |

## Configuration

After importing:

1. **Webhook node** — copy the webhook URL; trigger it by sending: `curl -X POST https://your-n8n.com/webhook/repurpose-content -H "Content-Type: application/json" -d '{"url":"https://example.com/article"}'`
2. **Save to Notion** — replace `YOUR_NOTION_CONTENT_DATABASE_ID`; ensure the database has properties: `Source URL` (url), `Status` (select with option `draft`), `Created` (date)
3. **Generate Content Variations** — edit the system prompt to adjust tone, format, or add brand-specific instructions
4. Connect OpenAI and Notion credentials

## Example

**Input webhook body:**
```json
{ "url": "https://hbr.org/2026/04/why-small-businesses-automate-first" }
```

**Notion page created with:**
- **Tweet Thread:** 5 tweets, tweet 1 = hook, tweet 5 = CTA
- **LinkedIn Post:** 180-word professional post with hashtags
- **Newsletter Snippet:** 90-word teaser paragraph
