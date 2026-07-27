# Capability Parity: Advisor / Escalation (LEAN7POF2 portable floor)

Claude-native: the Anthropic **Advisor tool** (executor + stronger advisor in one request). It is **Anthropic-API-only** (not on Bedrock/AWS/GCP/Foundry or any non-Claude engine), so non-Claude orchestrators use the pattern below.

## Owner scope ruling (27 Jul 2026)
- Advisor tool = WORK-TYPE tasks only (data science, teaching, subject-matter compiling). NOT framework/interpreter/plugin builds.
- Executor default Opus 5 for work tasks. For Fable-heavy tasks, prefer STAGED SEPARATE calls over the in-line advisor: Fable pre-constructs the staged operation by model-task suitability, then Opus checks certainty of the process-output.

## Portable pattern (non-Claude)
1. Route by model-task suitability (Artifact M).
2. Fable-class generative sub-task -> call Fable-equivalent first to draft the staged plan/output.
3. Certainty-check -> call an Opus-equivalent (cross-family where L14 independence is required) to verify the process-output; it returns a plan/course-correction, not a rewrite.
4. Executor continues, informed. Log both calls (author != sole-key).
5. Same-family checking = quality lift only, NOT author!=key independence.
