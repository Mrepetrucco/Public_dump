# Capability Parity: API-Update Tracking (LEAN7POF2 portable floor)

Claude-native: Anthropic's open-source **claude-api-skill** keeps API reference + best practices current, bundled with Claude Code.

Portable equivalent: mirror the API-surface facts the framework depends on here, refreshed on the monthly reconcile (1st) alongside Artifact M.

## Tracked surface facts (verify monthly; IDs volatile)
- Advisor tool: beta header advisor-tool-2026-03-01; Anthropic-API-only; advisor >= executor (Sonnet-4.6+); advisor tokens billed separately (read usage.iterations).
- Strict tool use: GA; additionalProperties:false + all-required per object.
- Message Batches: -50%; caching-compatible (retained).
- Models: opus-5, sonnet-5, opus-4-8, fable-5. HAIKU EXCLUDED by owner ruling — never route under any circumstance.
Source of truth: platform.claude.com docs; this file is a convenience mirror, not authoritative.
