# RSS to Social Post

Reads new items from an RSS feed hourly, rewrites each item as a LinkedIn post using GPT-4o, and publishes directly to LinkedIn.

## Use Case

Turn your industry news feed or blog into a steady stream of LinkedIn content — automatically. Each RSS item is rewritten in a professional, scroll-stopping LinkedIn format with hashtags. Runs every hour so you're always sharing fresh, relevant content.

## Required Credentials

- **OpenAI API Key** — GPT-4o rewriting
- **LinkedIn Access Token** — post to your LinkedIn profile or company page (set directly in the HTTP Request node header)

## Node Overview

| Node | Type | Purpose |
|------|------|---------|
| Every Hour | `n8n-nodes-base.scheduleTrigger` | Triggers the workflow every 60 minutes |
| Read RSS Feed | `n8n-nodes-base.rssFeedRead` | Fetches items from your RSS feed URL |
| Published in Last Hour? | `n8n-nodes-base.if` | Filters to items with isoDate in the past 60 minutes; items without isoDate pass through |
| Write LinkedIn Post | `n8n-nodes-base.openAi` | Rewrites each item as a 150-word LinkedIn post |
| Post to LinkedIn | `n8n-nodes-base.httpRequest` | Posts to LinkedIn UGC Posts API |

## Configuration

After importing:

1. **Read RSS Feed** — replace `YOUR_RSS_FEED_URL` with your feed URL (e.g. `https://techcrunch.com/feed/`). The **Published in Last Hour?** IF node automatically filters out older items on each run — no duplicate posts.
2. **Post to LinkedIn** — replace `REPLACE_WITH_YOUR_LINKEDIN_ACCESS_TOKEN` in the Authorization header. Get a token via the [LinkedIn Developer Portal](https://developer.linkedin.com/) — you need an app with `w_member_social` permission.
3. **Post to LinkedIn** — replace `YOUR_LINKEDIN_PERSON_ID` with your LinkedIn person URN (find it by calling `https://api.linkedin.com/v2/me` with your token)
4. **Write LinkedIn Post** — edit the system prompt to match your brand voice
5. Connect OpenAI credentials


## Example

**RSS item title:** "How AI is transforming small business invoicing"

**Generated LinkedIn post:**
> Are you still sending invoices manually in 2026? Small businesses that adopt AI invoicing report 40% fewer late payments.
>
> Here's what's changing: AI tools now auto-generate payment reminders, match bank statements, and flag disputes — without any human input.
>
> The businesses winning aren't the ones working harder. They're the ones automating faster.
>
> #SmallBusiness #Automation #AI #Invoicing #Productivity
