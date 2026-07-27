# Capability Parity: Tool Discovery (LEAN7POF2 portable floor)

Claude-native: the **Tool Search tool** loads tools on demand (progressive disclosure), keeping the tool-schema token floor low (OTES).

Portable equivalent for non-Claude engines: this GitHub-hosted index. The orchestrator fetches it, selects only the tools a sub-task needs, and injects just those schemas — instead of broadcasting all tool schemas every call.

| tool | purpose | schema location | engines |
|------|---------|-----------------|---------|
| web_search | live fact sourcing (Perplexity-class limits) | provider-native | all |
| emit_zblock | Z v2.1 structured emission | Objects/Zblock_v2_1_strict.json | all (validate-then-parse off-Claude) |
| read_file / write_file | md.txt sandbox persistence | Interpreter_Agent | all |
| github_contents | read/write mirror files | GitHub Contents API | all |

Rule: inject the minimum tool set per sub-task; discovery is a fetch of this index, not a full-schema broadcast.
