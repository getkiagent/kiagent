# Builder-Validator Pattern

When building any n8n workflow or script with >20 lines:

1. **Builder phase**: Build the solution. Save output.
2. **Validator phase**: Spawn a subagent (`--agent validator`) that:
   - Re-reads the original requirement
   - Checks the output against it
   - Runs tests or dry-runs
   - Lists: PASS / WARN (with reason) / FAIL (with fix)
3. Only mark done after Validator returns all PASS.

## Trigger
Use this pattern when:
- Building new n8n workflows
- Writing scripts >20 lines
- Modifying production workflows

Skip when:
- Quick fixes (<10 lines)
- Pure analysis/research tasks
