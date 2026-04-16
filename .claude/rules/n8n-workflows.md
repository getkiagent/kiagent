# n8n Known Quirks
- `create_workflow_from_code` fails with inline credential references and large inline data objects
- `appendOrUpdate` on Google Sheets requires `matchingColumns: ['url']`
- HTTP Request nodes for Anthropic API require manual credential assignment
- Always run `validate_workflow` before any production trigger
