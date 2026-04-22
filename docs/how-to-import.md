# How to Import a Workflow into n8n

This guide covers importing any workflow from this repository into your n8n instance.

---

## Method A: Import from JSON (Recommended)

**1. Get the JSON**

Navigate to the workflow folder in this repo (e.g. `workflows/crm/lead-capture-to-baserow/`) and open `workflow.json`. Click **Raw** on GitHub, then select all and copy.

**2. Open n8n and import**

- Go to your n8n instance (e.g. `http://localhost:5678`)
- Click **Workflows** in the left sidebar
- Click the **+** (New Workflow) button in the top-right
- In the workflow editor, click the **three-dot menu (⋮)** in the top-right
- Select **Import from JSON**
- Paste the copied JSON into the text box
- Click **Import**

**3. Reconnect credentials**

After import, nodes that require credentials will show a red warning badge. Click each flagged node, open the **Credentials** dropdown, and either select an existing credential or click **Create New** to add one.

See [credentials-setup.md](credentials-setup.md) for setup instructions per service.

**4. Update configuration values**

Each workflow's `README.md` lists what you need to change (table IDs, database IDs, email addresses, channel names). Update these in the node parameters before activating.

**5. Activate**

Toggle the workflow switch to **Active** in the top-right of the editor. For webhook-triggered workflows, n8n will display the webhook URL — copy it and add it to your form or service.

---

## Method B: Upload JSON File

- Download `workflow.json` from this repo to your computer
- In n8n: **Workflows** → **+** → **⋮ menu** → **Import from file**
- Select the downloaded file

---

## Testing Before Activating

For webhook workflows: use the **Test Workflow** button and send a test request using a tool like [hoppscotch.io](https://hoppscotch.io) or `curl`:

```bash
curl -X POST https://your-n8n.com/webhook/YOUR_PATH \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com"}'
```

For schedule-triggered workflows: click **Execute Workflow** manually to test a single run before setting the schedule live.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Red badge on node | Credential not connected — click the node and assign or create a credential |
| "Webhook already registered" error | Another workflow is using the same webhook path — change the path in the Webhook node parameters |
| Workflow imports but does nothing | Check it is set to **Active** and the trigger condition is met |
| Expression errors (`{{ }}`) | A referenced field name doesn't match — check the upstream node output using the **Output** panel |
