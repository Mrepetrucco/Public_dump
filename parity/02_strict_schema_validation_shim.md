# Capability Parity: Strict Schema Emission (LEAN7POF2 portable floor)

Claude-native: `strict:true` on a tool whose input_schema is the Z block guarantees conformance (GA, validated 27 Jul 2026). Every object must set `additionalProperties:false` and list all properties in `required`.

Claude-only. Non-Claude equivalent (same guarantee):
- Gemini: responseSchema / structured output (generationConfig).
- OpenAI: response_format {type:"json_schema", strict:true}.
- Any other: emit JSON then VALIDATE against the Z JSON-schema (validate-then-parse); on failure one bounded retry, then RAISE (Type-3 parse-gate).

Canonical schema: Framework_construction/Objects/Zblock_v2_1_strict.json. The validate-then-parse gate is mandatory on every emission regardless of engine.
