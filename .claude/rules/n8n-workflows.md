# n8n Workflows & Quirks

## Workflow IDs
- Lead URL Scorer — `jGDcEjOD8RIbXKpq`
- Gmail Draft from Outreach — `QxBuMHhSHuCpq3m6`
- Outreach Agent — `zVvZmfOWADGcN6kp`
- Gmail Status Sync — `PP2vkOQDsNcZcrig`
- Follow-up Checker — `Ox1mvhTkhVrJoaox`

## Known Quirks
- `create_workflow_from_code` fails with inline credential references and large inline data objects
- `appendOrUpdate` on Google Sheets requires `matchingColumns: ['url']`
- HTTP Request nodes for Anthropic API require manual credential assignment
- Always run `validate_workflow` before any production trigger
