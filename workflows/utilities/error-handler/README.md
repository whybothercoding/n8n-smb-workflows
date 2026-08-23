# Error Handler

Centralized error handler for all other workflows in this library. When any workflow fails, n8n routes the error here and posts an alert to Discord.

<!-- picker: Get alerted when any workflow fails -->

## Use Case

Set this as the `errorWorkflow` in every other workflow's settings. Instead of silent failures, every error posts a Discord message with the workflow name, execution ID, failing node, and error message — giving you immediate visibility when something breaks.

## Required Credentials

- **Discord Webhook** — post access to your ops/alerts channel

## Node Overview

| Node | Type | Purpose |
|------|------|---------|
| Workflow Error Trigger | `n8n-nodes-base.errorTrigger` | Fires when any linked workflow encounters an error |
| Format Error Message | `n8n-nodes-base.set` | Builds the subject and body from error context fields |
| Send Error Alert | `n8n-nodes-base.discord` | Posts the formatted error alert to Discord via webhook |

## Flow Diagram

<!-- FLOW_DIAGRAM:START -->
```mermaid
flowchart LR
    n0(["Workflow Error Trigger"])
    n1["Format Error Message"]
    n2["Send Error Alert"]
    n0 --> n1
    n1 --> n2
```
<!-- FLOW_DIAGRAM:END -->

## Configuration

1. **Import and activate this workflow first**, before activating any others.
2. **Copy this workflow's ID.** After importing, open the workflow in n8n, check the URL — the ID is the string after `/workflow/`. Copy it.
3. **Update all other workflows.** In each workflow's **Settings** panel (⚙ icon, top-right of the editor), set **Error Workflow** to the ID you copied.
4. **Send Error Alert** — create a webhook in your Discord server (**Server Settings → Integrations → Webhooks → New Webhook**) and use its URL for the credential.
5. Connect the Discord Webhook credential.

## Example

**When Invoice Reminder fails on the Baserow node:**

> **Subject:** ⚠️ n8n workflow failed: Invoice Reminder
> **Body:**
> Workflow: Invoice Reminder
> Execution ID: 8472
> Error: Could not connect to Baserow — ECONNREFUSED
> Node: Get Unpaid Invoices
> Started: 2026-05-05T09:00:03.000Z
