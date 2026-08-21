# Lean7POF_V3 — Reconciler/Runner components (PROSPECTIVE, corrected single-source)
Pull to disk and run: `python3 runner.py` (validates runner against dataset.json).
- reconciler.py = SINGLE-SOURCE producer: owns schema (owner-ratified versioned + hash-anchored), converts prose->j_trace->output-schema, raw emit only. No self-validation.
- runner.py = INDEPENDENT DETERMINISTIC checker: executes BX1 X0-X9 as code; owns nothing; one-word retry; X8 fact-gate (existence+entailment) is a MODEL hook.
- dataset.json = real schema-bind FAIL cases from the build chat (X0-X9 coverage) + start_values FAR=0.05 FRR=0.15 k=2 (ESTIMATED start, not yet measured).
DETERMINISTIC RESULT (this build): 11/11 structural cases correct; 2 fact-gate cases (FC9 forced-slot fabrication, FC10 real-cite fabricated-value) HELD for X8 model scoring (GPT_XAPI + Fable per the measurement plan).
STATUS: prospective, NOT accepted. X8 threshold/band are estimated start values pending the measurement plan.
