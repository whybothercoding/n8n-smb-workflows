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
