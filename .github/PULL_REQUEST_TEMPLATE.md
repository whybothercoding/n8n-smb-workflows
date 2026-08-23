## Workflow name

<!-- e.g. "HubSpot Contact Sync" -->

## Category

<!-- crm / email / social / lead-gen / reporting / newsletter / utilities -->

## What it automates

<!-- One-paragraph description -->

## Checklist

- [ ] `workflow.json` exports as `active: false` with `executionOrder: "v1"`
- [ ] All credential IDs use the `REPLACE_WITH_YOUR_CREDENTIAL_ID` placeholder
- [ ] `settings.errorWorkflow` is set to `REPLACE_WITH_YOUR_ERROR_WORKFLOW_ID`
- [ ] `README.md` has all required sections (Use Case, Required Credentials, Node Overview, Configuration, Example)
- [ ] `python3 scripts/generate_docs.py` run — root README tables and Flow Diagram are up to date
- [ ] `bash validate.sh` passes locally

## Testing notes

<!-- How did you verify the workflow runs correctly? e.g. "Tested on n8n 1.40 with a live Baserow instance" -->
