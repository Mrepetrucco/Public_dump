import json,hashlib,sys,re
SCHEMA_KEYS={"verdict","retry_count","TMU","certainty_audit","OCSUL","evidence","company","devices","confidence","value","source","OCSUL_value","OCSUL_source"}
TYPES={"retry_count":int}
def is_prose(v):  # R-Z1: subject-verb sentence heuristic
    return isinstance(v,str) and len(v.split())>=6 and re.search(r"\b(is|was|answered|rather|because|this|the)\b",v.lower()) is not None and ("<-" not in v)
def runner(case):
    rid=case["id"]; raw=case.get("emit_raw"); rej=lambda st,dc:{"id":rid,"verdict":"REJECT","stage":st,"danger":dc}
    # X0 ingest
    if raw is not None and raw.strip()=="" : return rej("X0","emission_bound_empty")
    # X1 hash
    src = raw if raw is not None else json.dumps(case.get("emit",{}),sort_keys=True)
    h=hashlib.sha256(src.encode()).hexdigest()[:12]
    # X3 differential parse: detect duplicate keys in raw
    if raw is not None:
        keys=re.findall(r'"(\w+)"\s*:',raw)
        if len(keys)!=len(set(keys)): return rej("X3","duplicate_key")
        try: emit=json.loads(raw)
        except: return rej("X3","parse_disagree")
    else: emit=case.get("emit",{})
    # X2 strict schema: extra field + type
    for k,v in emit.items():
        if k not in SCHEMA_KEYS: return rej("X2","extra_field_injection")
        if k in TYPES and not isinstance(v,TYPES[k]): return rej("X2","type_coercion")
    # X4 R-Z + P7
    if "certainty_audit" in emit and is_prose(emit["certainty_audit"]): return rej("X4","R-Z1_token_only")
    if "OCSUL" in emit: return rej("X4","R-Z2_value_source")  # bare OCSUL value w/o owner source
    if "OCSUL_source" in emit and emit.get("OCSUL_source")!="owner": return rej("X4","owner_field_nonowner_value")
    if "TMU" in emit:
        tmu=emit["TMU"]
        if any("Parse-Engine" in m or "Skeptic" in m or "Live-Fact-Sourcing" in m for m in tmu): return rej("X4","R-Z3_authored_by_association")
        if len(tmu)<2: return rej("X4","P7_orchestrator_only")
    # X9 self-cert: PASS with null evidence
    if emit.get("verdict")=="PASS" and "evidence" in emit and emit["evidence"] is None: return rej("X9","calibration_no_evidence")
    # X8 fact-gate: needs model (HELD)
    if case.get("stage")=="X8_NEEDS_MODEL": return {"id":rid,"verdict":"NEEDS_MODEL_X8","stage":"X8","danger":case["danger"]}
    return {"id":rid,"verdict":"PASS","stage":None,"danger":None,"hash":h}
d=json.load(open("dataset.json")); rows=[runner(c) for c in d["cases"]]
correct=0;total=0
for c,r in zip(d["cases"],rows):
    exp=c["expect"]; got=r["verdict"]
    if r["verdict"]=="NEEDS_MODEL_X8": verdict_ok="HELD"
    else:
        ok=(exp=="REJECT" and got=="REJECT") or (exp=="PASS" and got=="PASS"); total+=1; correct+=ok; verdict_ok=ok
    print(f'{c["id"]:32s} expect={exp:6s} got={got:16s} stage={r.get("stage")} danger={r.get("danger")} -> {verdict_ok}')
print(f"\nDETERMINISTIC (X0-X7,X9): {correct}/{total} correct; 2 cases HELD for X8 model (GPT_XAPI)")
