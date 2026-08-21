# RECONCILER (single-source producer) — Lean7POF_V3 corrected. Owns the schema; converts prose -> j_trace -> output-schema.
# Schema is Reconciler-owned + owner-ratified versioned + hash-anchored (NOT moved to a registry). Produces RAW emit only; validation is the Runner's (deterministic) job.
import json,hashlib
SCHEMA_VERSION="v3.0-prospective"; SCHEMA_KEYS=["verdict","retry_count","TMU","certainty_audit","OCSUL","evidence"]
def reconcile(prose_fields:dict)->dict:
    # single-source conversion; every value must arrive value<-source (j_trace). Raw emit; no self-validation.
    emit={k:v for k,v in prose_fields.items() if k in SCHEMA_KEYS}
    emit["schema_version"]=SCHEMA_VERSION
    emit["schema_hash"]=hashlib.sha256((SCHEMA_VERSION+"|"+",".join(SCHEMA_KEYS)).encode()).hexdigest()[:12]
    return emit  # -> handed to Runner (independent deterministic checker)
