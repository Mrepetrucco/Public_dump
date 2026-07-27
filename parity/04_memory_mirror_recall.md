# Capability Parity: Cross-session Memory / Recall (LEAN7POF2 portable floor)

Claude-native: the **Memory tool** + this platform's memory filesystem give cross-session recall.

Portable equivalent: mirror the memory SET to markdown; the orchestrator resends it as context to any stateless engine (measured: plain relays give 0/4 recall when history is NOT resent — recall requires resend, not a gateway).

## Protocol
1. Export the canonical memory set as markdown (one file per subject), aligned to this platform's memory.
2. Orchestrator FETCHES the memory md and includes it in each engine call.
3. XAPI recall validation: fetch memory md from GitHub -> include -> ask the engine to return a known stored fact -> score. Repeat per engine (OpenAI, Gemini, Memories/MemoryLake).

## PRIVACY (hard — blocks the content mirror)
The memory set contains personal /profile.md and /people/* data. It MUST NOT be mirrored to a PUBLIC repo. All three current repos are PUBLIC (27 Jul 2026). A PRIVATE destination or a full scrub of personal fields is required before the content mirror runs. This spec is safe to be public; the memory CONTENT is not.
