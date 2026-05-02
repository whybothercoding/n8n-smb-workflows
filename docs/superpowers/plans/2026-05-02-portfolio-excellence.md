# n8n SMB Workflows — Portfolio Excellence Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Bring all 10 workflow templates to portfolio-grade quality — fix logic bugs that would break workflows in production, enforce consistent patterns across all files, add validation tooling, and polish the repository for public display.

**Architecture:** Pure static-file repository (JSON + Markdown). No build step. All "tests" are structural validation via `validate.sh`. TDD here means: write the validator first, confirm it reports the known issues, fix them, confirm it passes.

**Tech Stack:** n8n workflow JSON (v1 export format), Bash (`validate.sh`), Markdown, GitHub CLI (`gh`)

---

## Audit Summary — Issues Found

| # | Issue | Severity | Affects |
|---|-------|----------|---------|
| A | OpenAI `simplify: true` set but expressions reference `$json.choices[0].message.content` — would return `undefined` at runtime | **Bug** | Workflows 3, 5, 6, 10 |
| B | RSS to Social Post runs every hour with no recency filter — posts ALL RSS items every run | **Bug** | Workflow 5 |
| C | Newsletter Subscriber uses raw `YOUR_BASEROW_API_TOKEN` placeholder in HTTP header instead of the `REPLACE_WITH_...` convention | **Inconsistency** | Workflow 7 |
| D | Contact Form to Notion jumps directly from Webhook → Notion with no normalize Set node (all other webhook workflows have one) | **Pattern gap** | Workflow 2 |
| E | Weekly Business Digest distinguishes leads from invoices using `invoice_number === undefined` — brittle if column names differ | **Fragile code** | Workflow 9 |
| F | All 10 workflows missing `errorWorkflow` in `settings` — n8n has no error routing on any workflow | **Best practice** | All |
| G | No `.gitignore` at repo root | **Quality** | Repo |
| H | No validation script — no way to verify workflow files meet requirements before PR merge | **Quality** | Repo |
| I | No GitHub PR/issue templates — OSS scaffolding missing | **Quality** | Repo |
| J | No Error Handler utility workflow — referenced by fix F but nothing ships it | **Gap** | Repo |

---

## File Map

**Create:**
- `.gitignore`
- `validate.sh`
- `.github/PULL_REQUEST_TEMPLATE.md`
- `.github/ISSUE_TEMPLATE/bug-report.md`
- `.github/ISSUE_TEMPLATE/workflow-submission.md`
- `workflows/utilities/error-handler/workflow.json`
- `workflows/utilities/error-handler/README.md`

**Modify:**
- `workflows/email/ai-email-auto-reply/workflow.json` — remove `simplify: true` (issue A)
- `workflows/social/rss-to-social-post/workflow.json` — remove `simplify: true` + add recency IF node (issues A, B)
- `workflows/social/rss-to-social-post/README.md` — document new IF node
- `workflows/social/content-repurpose-pipeline/workflow.json` — remove `simplify: true` (issue A)
- `workflows/reporting/support-ticket-to-slack/workflow.json` — remove `simplify: true` (issue A)
- `workflows/lead-gen/newsletter-subscriber-to-crm/workflow.json` — fix placeholder (issue C)
- `workflows/lead-gen/newsletter-subscriber-to-crm/README.md` — update config step
- `workflows/crm/contact-form-to-notion/workflow.json` — add Normalize Fields node (issue D)
- `workflows/crm/contact-form-to-notion/README.md` — document new node
- `workflows/reporting/weekly-business-digest/workflow.json` — add Tag Set nodes + fix Code node (issue E)
- `workflows/reporting/weekly-business-digest/README.md` — update config note
- All 10 workflow.json — add `errorWorkflow` to settings (issue F)
- `README.md` — portfolio polish

---

## Task 1: Validation Tooling and .gitignore

**Files:**
- Create: `validate.sh`
- Create: `.gitignore`

- [ ] **Step 1: Write `.gitignore`**

```
.DS_Store
*.swp
*.swo
```

- [ ] **Step 2: Write `validate.sh`**

```bash
#!/usr/bin/env bash
# Validates all workflow.json files meet repository requirements.
# Usage: bash validate.sh
# Exit 0 = all pass. Exit 1 = failures found.

set -euo pipefail

PASS=0
FAIL=0
ERRORS=()

check_workflow() {
  local file="$1"
  local errs=0

  # 1. Valid JSON
  if ! python3 -m json.tool "$file" > /dev/null 2>&1; then
    ERRORS+=("$file: invalid JSON")
    ((errs++))
  fi

  # 2. Required top-level fields
  for field in id name nodes connections active settings versionId; do
    if ! python3 -c "
import json, sys
d = json.load(open('$file'))
assert '$field' in d, '$field missing'
" 2>/dev/null; then
      ERRORS+=("$file: missing required field '$field'")
      ((errs++))
    fi
  done

  # 3. active must be false
  if ! python3 -c "
import json, sys
d = json.load(open('$file'))
assert d.get('active') is False
" 2>/dev/null; then
    ERRORS+=("$file: 'active' must be false")
    ((errs++))
  fi

  # 4. executionOrder must be "v1"
  if ! python3 -c "
import json, sys
d = json.load(open('$file'))
assert d.get('settings', {}).get('executionOrder') == 'v1'
" 2>/dev/null; then
    ERRORS+=("$file: settings.executionOrder must be 'v1'")
    ((errs++))
  fi

  # 5. errorWorkflow must be present in settings
  if ! python3 -c "
import json, sys
d = json.load(open('$file'))
assert 'errorWorkflow' in d.get('settings', {})
" 2>/dev/null; then
    ERRORS+=("$file: settings.errorWorkflow is missing")
    ((errs++))
  fi

  # 6. No raw API tokens in HTTP header values (must use REPLACE_WITH_ prefix)
  local bad_tokens
  bad_tokens=$(python3 -c "
import json, re
d = json.load(open('$file'))
text = json.dumps(d)
matches = re.findall(r'(?:Token|Bearer)\s+([A-Za-z0-9_]+)', text)
bad = [m for m in matches if not m.upper().startswith('REPLACE_WITH')]
print('\n'.join(bad))
" 2>/dev/null)
  if [ -n "$bad_tokens" ]; then
    ERRORS+=("$file: hardcoded token found in header — use REPLACE_WITH_... placeholder")
    ((errs++))
  fi

  if [ "$errs" -eq 0 ]; then
    ((PASS++))
    echo "  ✓ $file"
  else
    ((FAIL++))
    echo "  ✗ $file  ($errs issue(s))"
  fi
}

echo "=== n8n workflow validation ==="
echo ""

while IFS= read -r -d '' file; do
  check_workflow "$file"
done < <(find workflows -name "workflow.json" -print0 | sort -z)

echo ""
echo "Results: $PASS passed, $FAIL failed"
echo ""

if [ "$FAIL" -gt 0 ]; then
  echo "Issues:"
  for err in "${ERRORS[@]}"; do
    echo "  - $err"
  done
  exit 1
fi

echo "All workflows valid."
```

- [ ] **Step 3: Make validate.sh executable and run it — confirm it reports failures**

```bash
chmod +x validate.sh
bash validate.sh
```

Expected output (before any fixes): all 10 workflows listed as `✗` with at least one issue each (missing `errorWorkflow`, hardcoded token in workflow 7). The script exits 1. This is the "red" state.

- [ ] **Step 4: Commit**

```bash
git add validate.sh .gitignore
git commit -m "chore: add validate.sh and .gitignore"
```

---

## Task 2: Fix OpenAI `simplify: true` Bug (4 Workflows)

**Background:** The n8n OpenAI node with `simplify: true` and `operation: "message"` strips the `choices` wrapper from the API response, returning `$json.message.content` (not `$json.choices[0].message.content`). All 4 affected workflows set `simplify: true` but then reference `$json.choices[0].message.content` — this evaluates to `undefined` at runtime. Fix: remove `simplify: true` so the raw API response is returned and the existing expression paths are correct.

**Files:**
- Modify: `workflows/email/ai-email-auto-reply/workflow.json`
- Modify: `workflows/social/rss-to-social-post/workflow.json`
- Modify: `workflows/social/content-repurpose-pipeline/workflow.json`
- Modify: `workflows/reporting/support-ticket-to-slack/workflow.json`

- [ ] **Step 1: Fix `ai-email-auto-reply/workflow.json`**

In node `node-003-openai`, remove the `"simplify": true` line from `parameters`. The `parameters` block becomes:

```json
"parameters": {
  "resource": "text",
  "operation": "message",
  "modelId": {
    "__rl": true,
    "value": "gpt-4o",
    "mode": "list",
    "cachedResultName": "gpt-4o"
  },
  "messages": {
    "values": [
      {
        "role": "system",
        "content": "You are a professional business email assistant. Write a concise, polite, and helpful reply to the incoming email. Address the sender by their first name if you can infer it. Sign off as 'The Team'. Keep the reply under 150 words. Do not include a subject line."
      },
      {
        "role": "user",
        "content": "=From: {{ $json.from.value[0].address }}\nSubject: {{ $json.subject }}\n\n{{ $json.text ?? $json.snippet }}"
      }
    ]
  },
  "options": {}
}
```

- [ ] **Step 2: Fix `rss-to-social-post/workflow.json`**

In node `node-005-openai`, remove `"simplify": true`. Parameters become:

```json
"parameters": {
  "resource": "text",
  "operation": "message",
  "modelId": {
    "__rl": true,
    "value": "gpt-4o",
    "mode": "list",
    "cachedResultName": "gpt-4o"
  },
  "messages": {
    "values": [
      {
        "role": "system",
        "content": "You are a professional LinkedIn content writer. Rewrite the article summary below as a LinkedIn post. Use a professional yet conversational tone. Include 3–5 relevant hashtags at the end. Maximum 150 words. Do not use marketing clichés. Start with a strong hook — a question, statistic, or provocative statement."
      },
      {
        "role": "user",
        "content": "=Article title: {{ $json.title }}\n\nSummary: {{ $json.contentSnippet ?? $json.summary ?? $json.content }}\n\nSource URL: {{ $json.link }}"
      }
    ]
  },
  "options": { "maxTokens": 300 }
}
```

- [ ] **Step 3: Fix `content-repurpose-pipeline/workflow.json`**

In node `node-006-openai`, remove `"simplify": true`. Parameters become:

```json
"parameters": {
  "resource": "text",
  "operation": "message",
  "modelId": {
    "__rl": true,
    "value": "gpt-4o",
    "mode": "list",
    "cachedResultName": "gpt-4o"
  },
  "messages": {
    "values": [
      {
        "role": "system",
        "content": "You are a content repurposing specialist. Given article text, produce three outputs in this exact JSON format:\n{\n  \"tweet_thread\": [\"tweet1\", \"tweet2\", \"tweet3\", \"tweet4\", \"tweet5\"],\n  \"linkedin_post\": \"...\",\n  \"newsletter_snippet\": \"...\"\n}\n\nRules:\n- tweet_thread: 5 tweets, each under 280 characters, the first grabs attention, the last includes a call to action. No hashtags.\n- linkedin_post: professional tone, 150–200 words, 3–5 relevant hashtags at end.\n- newsletter_snippet: 80–100 words, written for an email newsletter subscriber, conversational tone, ends with a teaser linking back to the original.\n\nReturn only valid JSON. No markdown code fences."
      },
      {
        "role": "user",
        "content": "={{ $json.text }}"
      }
    ]
  },
  "options": { "maxTokens": 1500 }
}
```

- [ ] **Step 4: Fix `support-ticket-to-slack/workflow.json`**

In node `node-010-openai`, remove `"simplify": true`. Parameters become:

```json
"parameters": {
  "resource": "text",
  "operation": "message",
  "modelId": {
    "__rl": true,
    "value": "gpt-4o",
    "mode": "list",
    "cachedResultName": "gpt-4o"
  },
  "messages": {
    "values": [
      {
        "role": "system",
        "content": "You are a friendly and helpful customer support agent. Write a concise, professional reply to the customer's support message. Address them by name. Acknowledge their issue, provide a brief helpful response or next step, and sign off as 'The Support Team'. Keep it under 100 words."
      },
      {
        "role": "user",
        "content": "=Customer name: {{ $('Webhook').item.json.name }}\nSubject: {{ $('Webhook').item.json.subject ?? 'Support request' }}\nMessage: {{ $('Webhook').item.json.message }}"
      }
    ]
  },
  "options": { "maxTokens": 200 }
}
```

- [ ] **Step 5: Verify all 4 files are valid JSON**

```bash
for f in \
  workflows/email/ai-email-auto-reply/workflow.json \
  workflows/social/rss-to-social-post/workflow.json \
  workflows/social/content-repurpose-pipeline/workflow.json \
  workflows/reporting/support-ticket-to-slack/workflow.json; do
  python3 -m json.tool "$f" > /dev/null && echo "✓ $f" || echo "✗ $f"
done
```

Expected: all 4 print `✓`.

- [ ] **Step 6: Commit**

```bash
git add workflows/email/ai-email-auto-reply/workflow.json \
        workflows/social/rss-to-social-post/workflow.json \
        workflows/social/content-repurpose-pipeline/workflow.json \
        workflows/reporting/support-ticket-to-slack/workflow.json
git commit -m "fix: remove simplify: true from OpenAI nodes — expressions reference raw response shape"
```

---

## Task 3: Fix RSS to Social Post — Add Recency Filter

**Background:** The workflow runs hourly but has no date check — it processes every item in the RSS feed every time, which would post duplicate LinkedIn content on every run. An IF node must filter to items published in the last 60 minutes. The README already mentions this in a "Note on volume" but it's not in the JSON.

**Files:**
- Modify: `workflows/social/rss-to-social-post/workflow.json`
- Modify: `workflows/social/rss-to-social-post/README.md`

- [ ] **Step 1: Add the IF node and update positions + connections in `workflow.json`**

Insert a new node after `node-005-rss`. Shift `node-005-openai` and `node-005-linkedin` 220px right each. The complete updated `nodes` array and `connections` object:

New node to add:
```json
{
  "id": "node-005-if",
  "name": "Published in Last Hour?",
  "type": "n8n-nodes-base.if",
  "typeVersion": 2,
  "position": [680, 300],
  "parameters": {
    "conditions": {
      "options": {
        "caseSensitive": false,
        "leftValue": "",
        "typeValidation": "loose"
      },
      "conditions": [
        {
          "id": "cond-005-001",
          "leftValue": "={{ $json.isoDate ? new Date($json.isoDate) > new Date(Date.now() - 3600000) : true }}",
          "rightValue": true,
          "operator": {
            "type": "boolean",
            "operation": "true"
          }
        }
      ],
      "combinator": "and"
    },
    "looseTypeValidation": true
  }
}
```

Updated positions (in existing nodes):
- `node-005-openai` (Write LinkedIn Post): change `"position"` from `[680, 300]` to `[900, 300]`
- `node-005-linkedin` (Post to LinkedIn): change `"position"` from `[900, 300]` to `[1120, 300]`

Updated `connections` object (replace entirely):
```json
"connections": {
  "Every Hour": {
    "main": [[{ "node": "Read RSS Feed", "type": "main", "index": 0 }]]
  },
  "Read RSS Feed": {
    "main": [[{ "node": "Published in Last Hour?", "type": "main", "index": 0 }]]
  },
  "Published in Last Hour?": {
    "main": [
      [{ "node": "Write LinkedIn Post", "type": "main", "index": 0 }],
      []
    ]
  },
  "Write LinkedIn Post": {
    "main": [[{ "node": "Post to LinkedIn", "type": "main", "index": 0 }]]
  }
}
```

- [ ] **Step 2: Verify JSON is valid**

```bash
python3 -m json.tool workflows/social/rss-to-social-post/workflow.json > /dev/null && echo "✓ valid"
```

Expected: `✓ valid`

- [ ] **Step 3: Update `rss-to-social-post/README.md`**

In the Node Overview table, add the new row between `Read RSS Feed` and `Write LinkedIn Post`:

```markdown
| Published in Last Hour? | `n8n-nodes-base.if` | Filters items to those with `isoDate` in the past 60 minutes, preventing duplicate posts on each run |
```

Remove the "Note on volume" paragraph at the bottom of the Configuration section (it's now fixed in the workflow, not just a note).

Add step 2a to the Configuration section:

```markdown
2a. **Published in Last Hour?** — the condition uses `$json.isoDate` from the RSS item. If your feed uses a different date field, update the expression accordingly. Items without an `isoDate` field pass through (defaults to `true`) so no content is silently dropped.
```

- [ ] **Step 4: Commit**

```bash
git add workflows/social/rss-to-social-post/workflow.json workflows/social/rss-to-social-post/README.md
git commit -m "fix: add hourly recency filter to RSS to Social Post — prevents duplicate LinkedIn posts"
```

---

## Task 4: Fix Newsletter Subscriber — Credential Placeholder Convention

**Background:** The `Check If Email Exists` HTTP Request node has `"value": "Token YOUR_BASEROW_API_TOKEN"` in its Authorization header. Every other credential placeholder in this repo uses the `REPLACE_WITH_...` prefix. This inconsistency makes the file fail validate.sh check 6 and confuses importers expecting a consistent pattern.

**Files:**
- Modify: `workflows/lead-gen/newsletter-subscriber-to-crm/workflow.json`
- Modify: `workflows/lead-gen/newsletter-subscriber-to-crm/README.md`

- [ ] **Step 1: Update the Authorization header value in `workflow.json`**

In node `node-007-check`, find the `headerParameters` block:

```json
"headerParameters": {
  "parameters": [
    { "name": "Authorization", "value": "Token YOUR_BASEROW_API_TOKEN" }
  ]
}
```

Change to:

```json
"headerParameters": {
  "parameters": [
    { "name": "Authorization", "value": "Token REPLACE_WITH_YOUR_BASEROW_API_TOKEN" }
  ]
}
```

- [ ] **Step 2: Update `README.md` configuration step 2**

Find:
```
2. **Check If Email Exists** — replace `YOUR_BASEROW_INSTANCE` (e.g. `baserow.yourdomain.com`), `YOUR_SUBSCRIBERS_TABLE_ID`, and `YOUR_BASEROW_API_TOKEN`
```

Replace with:
```
2. **Check If Email Exists** — in the node parameters, replace:
   - `YOUR_BASEROW_INSTANCE` with your Baserow host (e.g. `baserow.yourdomain.com`)
   - `YOUR_SUBSCRIBERS_TABLE_ID` with your subscribers table ID
   - `REPLACE_WITH_YOUR_BASEROW_API_TOKEN` in the Authorization header value with your Baserow API token (the same token you add as a Baserow credential). This node uses a direct HTTP call for the existence check, so the token must also be set here.
```

- [ ] **Step 3: Verify JSON is valid**

```bash
python3 -m json.tool workflows/lead-gen/newsletter-subscriber-to-crm/workflow.json > /dev/null && echo "✓ valid"
```

- [ ] **Step 4: Commit**

```bash
git add workflows/lead-gen/newsletter-subscriber-to-crm/workflow.json workflows/lead-gen/newsletter-subscriber-to-crm/README.md
git commit -m "fix: standardise credential placeholder in Newsletter Subscriber HTTP Request node"
```

---

## Task 5: Add Normalize Fields Node to Contact Form to Notion

**Background:** Every other webhook-triggered workflow in this repo uses a Set node to normalise field names immediately after the trigger (handling aliased fields like `full_name` vs `name`, defaulting missing optional fields). Contact Form to Notion jumps directly from the Webhook to a Notion API call, which will fail silently if the form sends different field names.

**Files:**
- Modify: `workflows/crm/contact-form-to-notion/workflow.json`
- Modify: `workflows/crm/contact-form-to-notion/README.md`

- [ ] **Step 1: Add the Normalize Fields Set node and update positions + connections**

New node to insert between Webhook and Create Notion Page:
```json
{
  "id": "node-002-set",
  "name": "Normalize Fields",
  "type": "n8n-nodes-base.set",
  "typeVersion": 3,
  "position": [460, 300],
  "parameters": {
    "assignments": {
      "assignments": [
        {
          "id": "assign-002-001",
          "name": "name",
          "value": "={{ $json.name ?? $json.full_name ?? '' }}",
          "type": "string"
        },
        {
          "id": "assign-002-002",
          "name": "email",
          "value": "={{ $json.email ?? '' }}",
          "type": "string"
        },
        {
          "id": "assign-002-003",
          "name": "phone",
          "value": "={{ $json.phone ?? $json.telephone ?? '' }}",
          "type": "string"
        },
        {
          "id": "assign-002-004",
          "name": "source",
          "value": "={{ $json.source ?? 'website' }}",
          "type": "string"
        },
        {
          "id": "assign-002-005",
          "name": "message",
          "value": "={{ $json.message ?? '' }}",
          "type": "string"
        }
      ]
    },
    "options": {}
  }
}
```

Updated positions for existing nodes:
- `node-002-notion` (Create Notion Page): `"position"` → `[680, 300]`
- `node-002-slack` (Slack Notification): `"position"` → `[900, 300]`

Updated `connections` object (replace entirely):
```json
"connections": {
  "Webhook": {
    "main": [[{ "node": "Normalize Fields", "type": "main", "index": 0 }]]
  },
  "Normalize Fields": {
    "main": [[{ "node": "Create Notion Page", "type": "main", "index": 0 }]]
  },
  "Create Notion Page": {
    "main": [[{ "node": "Slack Notification", "type": "main", "index": 0 }]]
  }
}
```

Also update the Notion node's property values to use the normalized field names. In `node-002-notion`, change the `propertiesUi` to reference the normalized output:

```json
"propertiesUi": {
  "propertyValues": [
    {
      "key": "Email|email",
      "emailValue": "={{ $json.email }}"
    },
    {
      "key": "Phone|phone_number",
      "phoneValue": "={{ $json.phone }}"
    },
    {
      "key": "Source|select",
      "selectValue": "={{ $json.source }}"
    },
    {
      "key": "Message|rich_text",
      "textContent": "={{ $json.message }}"
    }
  ]
}
```

The `title` in the Notion node should reference the normalized name:
```json
"title": "={{ $json.name }} — {{ new Date().toLocaleDateString('en-GB') }}"
```

And the Slack message should reference normalized fields:
```json
"text": ":mailbox_with_mail: *New contact form submission*\n*Name:* {{ $('Normalize Fields').item.json.name }}\n*Email:* {{ $('Normalize Fields').item.json.email }}\n*Message:* {{ $('Normalize Fields').item.json.message || '(no message)' }}\n<{{ $json.url }}|View in Notion>"
```

- [ ] **Step 2: Verify JSON is valid**

```bash
python3 -m json.tool workflows/crm/contact-form-to-notion/workflow.json > /dev/null && echo "✓ valid"
```

- [ ] **Step 3: Update `contact-form-to-notion/README.md`**

Add `Normalize Fields` row to the Node Overview table:
```markdown
| Normalize Fields | `n8n-nodes-base.set` | Maps `name`/`full_name`, `phone`/`telephone` aliases; defaults `source` to `website` |
```

Insert it between the Webhook row and the Create Notion Page row.

In Configuration, add a step:
```markdown
0. **Normalize Fields** — if your form sends field names other than `name`, `email`, `phone`, `message`, or `source`, update the fallback aliases in this Set node.
```

- [ ] **Step 4: Commit**

```bash
git add workflows/crm/contact-form-to-notion/workflow.json workflows/crm/contact-form-to-notion/README.md
git commit -m "fix: add Normalize Fields node to Contact Form to Notion — consistent with all other webhook workflows"
```

---

## Task 6: Fix Weekly Business Digest — Source Tagging

**Background:** The Code node (`Aggregate Stats`) receives items from both `Get New Leads` and `Get Invoices` via two connections to the same node. It currently distinguishes leads from invoices using `i.json.invoice_number === undefined`, which silently misclassifies rows if a leads table happens to have a column named `invoice_number`. Adding a Set node after each Baserow node to stamp a `data_type` field makes the distinction explicit and rename-proof.

**Files:**
- Modify: `workflows/reporting/weekly-business-digest/workflow.json`
- Modify: `workflows/reporting/weekly-business-digest/README.md`

- [ ] **Step 1: Add two Tag Set nodes, update positions and connections in `workflow.json`**

New node after `Get New Leads`:
```json
{
  "id": "node-009-tag-lead",
  "name": "Tag as Lead",
  "type": "n8n-nodes-base.set",
  "typeVersion": 3,
  "position": [680, 200],
  "parameters": {
    "assignments": {
      "assignments": [
        {
          "id": "assign-009-tag-001",
          "name": "data_type",
          "value": "lead",
          "type": "string"
        }
      ]
    },
    "options": { "includeOtherFields": true }
  }
}
```

New node after `Get Invoices`:
```json
{
  "id": "node-009-tag-invoice",
  "name": "Tag as Invoice",
  "type": "n8n-nodes-base.set",
  "typeVersion": 3,
  "position": [680, 400],
  "parameters": {
    "assignments": {
      "assignments": [
        {
          "id": "assign-009-tag-002",
          "name": "data_type",
          "value": "invoice",
          "type": "string"
        }
      ]
    },
    "options": { "includeOtherFields": true }
  }
}
```

Updated positions for existing nodes:
- `node-009-code` (Aggregate Stats): `"position"` → `[900, 300]`
- `node-009-set` (Build HTML Email): `"position"` → `[1120, 300]`
- `node-009-email` (Email Digest to Owner): `"position"` → `[1340, 300]`

Updated `connections` object (replace entirely):
```json
"connections": {
  "Monday 8am": {
    "main": [[
      { "node": "Get New Leads", "type": "main", "index": 0 },
      { "node": "Get Invoices", "type": "main", "index": 0 }
    ]]
  },
  "Get New Leads": {
    "main": [[{ "node": "Tag as Lead", "type": "main", "index": 0 }]]
  },
  "Get Invoices": {
    "main": [[{ "node": "Tag as Invoice", "type": "main", "index": 0 }]]
  },
  "Tag as Lead": {
    "main": [[{ "node": "Aggregate Stats", "type": "main", "index": 0 }]]
  },
  "Tag as Invoice": {
    "main": [[{ "node": "Aggregate Stats", "type": "main", "index": 0 }]]
  },
  "Aggregate Stats": {
    "main": [[{ "node": "Build HTML Email", "type": "main", "index": 0 }]]
  },
  "Build HTML Email": {
    "main": [[{ "node": "Email Digest to Owner", "type": "main", "index": 0 }]]
  }
}
```

- [ ] **Step 2: Update the Code node JS in `node-009-code`**

Replace the `jsCode` value with:

```javascript
const allItems = $input.all();

const leads = allItems.filter(i => i.json.data_type === 'lead');
const invoices = allItems.filter(i => i.json.data_type === 'invoice');

const newLeadsCount = leads.length;
const newLeadsList = leads.slice(0, 5)
  .map(l => `<li>${l.json.name ?? 'Unknown'} (${l.json.email ?? ''})</li>`)
  .join('');

const paidInvoices = invoices.filter(i => i.json.Status === 'paid');
const unpaidInvoices = invoices.filter(i => i.json.Status === 'unpaid');
const totalRevenue = paidInvoices.reduce((sum, i) => sum + (parseFloat(i.json.amount) || 0), 0);
const totalOutstanding = unpaidInvoices.reduce((sum, i) => sum + (parseFloat(i.json.amount) || 0), 0);

const weekStart = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toLocaleDateString('en-GB');
const weekEnd = new Date().toLocaleDateString('en-GB');

return [{
  json: {
    weekStart,
    weekEnd,
    newLeadsCount,
    newLeadsList: newLeadsList || '<li>No new leads this week</li>',
    paidCount: paidInvoices.length,
    unpaidCount: unpaidInvoices.length,
    totalRevenue: totalRevenue.toFixed(2),
    totalOutstanding: totalOutstanding.toFixed(2)
  }
}];
```

The only change from the original is the first two lines: `data_type === 'lead'` and `data_type === 'invoice'` instead of the fragile `invoice_number === undefined` heuristic.

- [ ] **Step 3: Verify JSON is valid**

```bash
python3 -m json.tool workflows/reporting/weekly-business-digest/workflow.json > /dev/null && echo "✓ valid"
```

- [ ] **Step 4: Update `weekly-business-digest/README.md`**

Add two rows to the Node Overview table:
```markdown
| Tag as Lead | `n8n-nodes-base.set` | Stamps `data_type: "lead"` on every lead row before merging with invoices |
| Tag as Invoice | `n8n-nodes-base.set` | Stamps `data_type: "invoice"` on every invoice row before merging with leads |
```

Remove the note in Configuration step 3:
> "the Code node distinguishes leads from invoices by the presence of `invoice_number`. If your column name differs, update the `i.json.invoice_number === undefined` check"

Replace with:
> "3. **Aggregate Stats** — the Code node separates leads from invoices using the `data_type` field stamped by the Tag nodes. No column name dependency."

- [ ] **Step 5: Commit**

```bash
git add workflows/reporting/weekly-business-digest/workflow.json workflows/reporting/weekly-business-digest/README.md
git commit -m "fix: replace fragile invoice_number heuristic with explicit data_type tagging in Weekly Digest"
```

---

## Task 7: Add Error Handler Workflow + Wire All Workflows

**Background:** n8n routes errors to an `errorWorkflow` specified in each workflow's settings. None of the 10 existing workflows have this field. This task adds the field to all workflows and ships a matching Error Handler utility workflow.

**Files:**
- Create: `workflows/utilities/error-handler/workflow.json`
- Create: `workflows/utilities/error-handler/README.md`
- Modify: all 10 existing `workflow.json` files (settings block only)
- Modify: `README.md` (add Error Handler to table)

- [ ] **Step 1: Create `workflows/utilities/error-handler/workflow.json`**

```json
{
  "id": "a1b2c3d4-0011-4abc-8def-000000000011",
  "meta": {
    "instanceId": "",
    "templateCredsSetupCompleted": true
  },
  "name": "Error Handler",
  "nodes": [
    {
      "id": "node-011-trigger",
      "name": "Workflow Error Trigger",
      "type": "n8n-nodes-base.errorTrigger",
      "typeVersion": 1,
      "position": [240, 300],
      "parameters": {}
    },
    {
      "id": "node-011-set",
      "name": "Format Error Message",
      "type": "n8n-nodes-base.set",
      "typeVersion": 3,
      "position": [460, 300],
      "parameters": {
        "assignments": {
          "assignments": [
            {
              "id": "assign-011-001",
              "name": "subject",
              "value": "=⚠️ n8n workflow failed: {{ $json.workflow.name }}",
              "type": "string"
            },
            {
              "id": "assign-011-002",
              "name": "body",
              "value": "=Workflow: {{ $json.workflow.name }}\nExecution ID: {{ $json.execution.id }}\nError: {{ $json.execution.error.message }}\nNode: {{ $json.execution.error.node?.name ?? 'unknown' }}\nStarted: {{ new Date($json.execution.startedAt).toISOString() }}",
              "type": "string"
            }
          ]
        },
        "options": {}
      }
    },
    {
      "id": "node-011-email",
      "name": "Send Error Alert",
      "type": "n8n-nodes-base.emailSend",
      "typeVersion": 2,
      "position": [680, 300],
      "parameters": {
        "fromEmail": "n8n-alerts@yourcompany.com",
        "toEmail": "owner@yourcompany.com",
        "subject": "={{ $json.subject }}",
        "message": "={{ $json.body }}",
        "options": {}
      },
      "credentials": {
        "smtp": {
          "id": "REPLACE_WITH_YOUR_CREDENTIAL_ID",
          "name": "SMTP account"
        }
      }
    }
  ],
  "connections": {
    "Workflow Error Trigger": {
      "main": [[{ "node": "Format Error Message", "type": "main", "index": 0 }]]
    },
    "Format Error Message": {
      "main": [[{ "node": "Send Error Alert", "type": "main", "index": 0 }]]
    }
  },
  "pinData": {},
  "active": false,
  "settings": { "executionOrder": "v1" },
  "staticData": null,
  "tags": ["utilities"],
  "versionId": "v1b2c3d4-0011-4abc-8def-000000000011"
}
```

Note: the Error Handler itself does NOT have an `errorWorkflow` in its settings (to avoid a circular error loop).

- [ ] **Step 2: Create `workflows/utilities/error-handler/README.md`**

```markdown
# Error Handler

Centralized error handler for all other workflows in this library. When any workflow fails, n8n routes the error here and sends an alert email to the business owner.

## Use Case

Set this as the `errorWorkflow` in every other workflow's settings. Instead of silent failures, every error generates an email with the workflow name, execution ID, failing node, and error message — giving you immediate visibility when something breaks.

## Required Credentials

- **SMTP** — outbound email for error alerts

## Node Overview

| Node | Type | Purpose |
|------|------|---------|
| Workflow Error Trigger | `n8n-nodes-base.errorTrigger` | Fires when any linked workflow encounters an error |
| Format Error Message | `n8n-nodes-base.set` | Builds the subject and body from error context fields |
| Send Error Alert | `n8n-nodes-base.emailSend` | Sends the formatted error alert to the owner email |

## Configuration

**Step 1 — Import and activate this workflow first**, before activating any others.

**Step 2 — Copy this workflow's ID.** After importing, open the workflow in n8n, check the URL — the ID is the string after `/workflow/`. Copy it.

**Step 3 — Update all other workflows.** In each workflow's **Settings** panel (⚙ icon, top-right of the editor), set **Error Workflow** to the ID you copied.

**Step 4 — Update the Email node:** replace `n8n-alerts@yourcompany.com` with your sending address and `owner@yourcompany.com` with your receiving address.

**Step 5 — Connect SMTP credential.**

## Example

**When Invoice Reminder fails on the Baserow node:**

> **Subject:** ⚠️ n8n workflow failed: Invoice Reminder
> **Body:**
> Workflow: Invoice Reminder
> Execution ID: 8472
> Error: Could not connect to Baserow — ECONNREFUSED
> Node: Get Unpaid Invoices
> Started: 2026-05-05T09:00:03.000Z
```

- [ ] **Step 3: Add `errorWorkflow` to all 10 existing workflow settings**

For each of the 10 workflow.json files, find the `"settings"` object and add the `errorWorkflow` key:

**Before** (identical in all 10):
```json
"settings": { "executionOrder": "v1" }
```

**After** (identical in all 10):
```json
"settings": {
  "executionOrder": "v1",
  "errorWorkflow": "REPLACE_WITH_YOUR_ERROR_WORKFLOW_ID"
}
```

Files to update:
- `workflows/crm/lead-capture-to-baserow/workflow.json`
- `workflows/crm/contact-form-to-notion/workflow.json`
- `workflows/email/ai-email-auto-reply/workflow.json`
- `workflows/email/invoice-reminder/workflow.json`
- `workflows/social/rss-to-social-post/workflow.json`
- `workflows/social/content-repurpose-pipeline/workflow.json`
- `workflows/lead-gen/newsletter-subscriber-to-crm/workflow.json`
- `workflows/lead-gen/abandoned-lead-followup/workflow.json`
- `workflows/reporting/weekly-business-digest/workflow.json`
- `workflows/reporting/support-ticket-to-slack/workflow.json`

- [ ] **Step 4: Run validate.sh — all workflows should now pass every check**

```bash
bash validate.sh
```

Expected output: all 11 workflows (10 existing + error-handler) print `✓`. `Results: 11 passed, 0 failed`. Script exits 0.

If any still fail, fix the specific issue reported before proceeding.

- [ ] **Step 5: Add Error Handler row to root `README.md` table**

In the "What's Inside" table, add a row at the end:

```markdown
| 11 | [Error Handler](workflows/utilities/error-handler/) | Utilities | Centralized error alert — routes n8n workflow failures to an email |
```

Also add `workflows/utilities/error-handler/` to the file map in the table header area if it's listed.

- [ ] **Step 6: Commit**

```bash
git add workflows/utilities/ \
        workflows/crm/lead-capture-to-baserow/workflow.json \
        workflows/crm/contact-form-to-notion/workflow.json \
        workflows/email/ai-email-auto-reply/workflow.json \
        workflows/email/invoice-reminder/workflow.json \
        workflows/social/rss-to-social-post/workflow.json \
        workflows/social/content-repurpose-pipeline/workflow.json \
        workflows/lead-gen/newsletter-subscriber-to-crm/workflow.json \
        workflows/lead-gen/abandoned-lead-followup/workflow.json \
        workflows/reporting/weekly-business-digest/workflow.json \
        workflows/reporting/support-ticket-to-slack/workflow.json \
        README.md
git commit -m "feat: add Error Handler utility workflow and wire errorWorkflow in all 10 workflows"
```

---

## Task 8: GitHub OSS Scaffolding

**Files:**
- Create: `.github/PULL_REQUEST_TEMPLATE.md`
- Create: `.github/ISSUE_TEMPLATE/bug-report.md`
- Create: `.github/ISSUE_TEMPLATE/workflow-submission.md`

- [ ] **Step 1: Create `.github/PULL_REQUEST_TEMPLATE.md`**

```markdown
## Workflow name

<!-- e.g. "HubSpot Contact Sync" -->

## Category

<!-- crm / email / social / lead-gen / reporting / utilities -->

## What it automates

<!-- One-paragraph description -->

## Checklist

- [ ] `workflow.json` exports as `active: false` with `executionOrder: "v1"`
- [ ] All credential IDs use the `REPLACE_WITH_YOUR_CREDENTIAL_ID` placeholder
- [ ] `settings.errorWorkflow` is set to `REPLACE_WITH_YOUR_ERROR_WORKFLOW_ID`
- [ ] `README.md` has all required sections (Use Case, Required Credentials, Node Overview, Configuration, Example)
- [ ] Root `README.md` table updated with a new row
- [ ] `bash validate.sh` passes locally

## Testing notes

<!-- How did you verify the workflow runs correctly? e.g. "Tested on n8n 1.40 with a live Baserow instance" -->
```

- [ ] **Step 2: Create `.github/ISSUE_TEMPLATE/bug-report.md`**

```markdown
---
name: Bug report
about: An existing workflow is broken or incorrect
labels: bug
---

**Workflow**
<!-- e.g. "Invoice Reminder" (link to the folder) -->

**n8n version**
<!-- e.g. 1.40.0, self-hosted -->

**What went wrong**

**What you expected**

**Steps to reproduce**
1.
2.
3.

**Relevant node / expression**
<!-- Paste the node name and the expression or parameter that's failing -->
```

- [ ] **Step 3: Create `.github/ISSUE_TEMPLATE/workflow-submission.md`**

```markdown
---
name: Workflow idea
about: Suggest a new workflow for this library
labels: new-workflow
---

**Proposed workflow name**

**Category**
<!-- crm / email / social / lead-gen / reporting / utilities -->

**What it automates**
<!-- One paragraph: what the workflow does, what triggers it, what it outputs -->

**Services / credentials required**

**Will you submit a PR?**
- [ ] Yes
- [ ] No — I'm requesting it
```

- [ ] **Step 4: Verify directory structure**

```bash
ls .github/
ls .github/ISSUE_TEMPLATE/
```

Expected:
```
.github/
  PULL_REQUEST_TEMPLATE.md
  ISSUE_TEMPLATE/
    bug-report.md
    workflow-submission.md
```

- [ ] **Step 5: Commit**

```bash
git add .github/
git commit -m "chore: add GitHub PR template and issue templates"
```

---

## Task 9: Polish Root README

**File:**
- Modify: `README.md`

- [ ] **Step 1: Add an ASCII flow diagram after the intro paragraph and before the table**

Insert after the first paragraph:
````markdown
## How Each Workflow Works

Every workflow follows the same pattern:

```
Trigger (Webhook · Schedule · Gmail poll)
  └─▶  Normalize / Filter
          └─▶  Action (CRM · Email · Social · AI)
                  └─▶  Log / Confirm / Alert
```

All workflows ship as `active: false`. Import → connect credentials → activate.
````

- [ ] **Step 2: Add a "Pick Your Workflow" quick-decision guide after the table**

Insert after the table:
```markdown
## Which Workflow Do I Need?

| If you want to… | Use |
|---|---|
| Capture form leads into a CRM | Lead Capture to Baserow or Contact Form to Notion |
| Auto-draft replies to inbound emails | AI Email Auto-Reply |
| Chase unpaid invoices automatically | Invoice Reminder |
| Turn blog posts into LinkedIn content | RSS to Social Post |
| Repurpose any article into 3 content formats | Content Repurpose Pipeline |
| Sync newsletter subscribers to your CRM | Newsletter Subscriber to CRM |
| Follow up with leads that went cold | Abandoned Lead Follow-up |
| Get a weekly business numbers email | Weekly Business Digest |
| Route support tickets to Slack + get AI draft replies | Support Ticket to Slack |
| Get alerted when any workflow fails | Error Handler |
```

- [ ] **Step 3: Add validate badge and usage note to the Prerequisites section**

Add to the Prerequisites section:
```markdown
### Validating workflows before contributing

Run `bash validate.sh` from the repo root to check all workflow files meet the repository requirements (valid JSON, required fields, correct placeholders, error routing).
```

- [ ] **Step 4: Verify README renders cleanly**

```bash
# Quick check — no syntax that would break markdown rendering
python3 -c "
text = open('README.md').read()
assert '# n8n SMB Workflows' in text
assert 'validate.sh' in text
print('README looks good')
"
```

Expected: `README looks good`

- [ ] **Step 5: Commit**

```bash
git add README.md
git commit -m "docs: add flow diagram, quick-pick guide, and validate badge to README"
```

---

## Self-Review

**Spec coverage check:**

| Issue from Audit | Task | Addressed? |
|---|---|---|
| A — OpenAI simplify bug (4 workflows) | Task 2 | ✓ |
| B — RSS no recency filter | Task 3 | ✓ |
| C — Newsletter hardcoded token | Task 4 | ✓ |
| D — Contact Form no normalize step | Task 5 | ✓ |
| E — Weekly Digest fragile heuristic | Task 6 | ✓ |
| F — Missing errorWorkflow (all) | Task 7 | ✓ |
| G — No .gitignore | Task 1 | ✓ |
| H — No validation tooling | Task 1 | ✓ |
| I — No GitHub templates | Task 8 | ✓ |
| J — No Error Handler workflow | Task 7 | ✓ |

**Placeholder scan:** No "TBD", "TODO", or "implement later" in any task. Every step has exact content.

**Type/name consistency:** Node IDs, names, and connection keys are consistent within each task. `data_type` field name is used in both Tag Set nodes (Tasks 6) and the Code node fix. `errorWorkflow` spelling is consistent across all workflow settings updates.
