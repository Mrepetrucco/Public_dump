#!/usr/bin/env python3
"""PLAIN_INTERPRETER v0.1 (P-c1 default) - keyless teaching/data-science interpreter.
Governance floor: LEAN7POF2 External Edition v1.2 (fetched raw from public repo at start;
offline fallback = bundled copy). Reduced judgment set R1-R6 + embedded standalone
Reconciler (N1) running the J-screen on the engine side of the boundary.

*** STABILITY WARNING (owner-mandated, surface prominently to every user) ***
API-key-less (P-c1) may be UNSTABLE - it browser-automates a consumer product
(Google AI Mode) with no official API; Google can break it at any time; ToS risk.
Fallbacks: P-a free Gemini key (stable CLI) or P-c2 Chrome Nano (keyless web-app).
*** END WARNING ***

STATUS FLAG (R1): the P-c1 driver below is UNVERIFIED against live AI Mode - built
in a sandbox without a browser session; selectors are best-effort and 'unverified'.
Requires: playwright (pip install playwright && playwright install chromium).
"""
import json, os, re, sys, time, urllib.request

FLOOR_URL = ('https://raw.githubusercontent.com/Mrepetrucco/Public_Dump/main/'
             'LEAN7POF2_External_Edition_v1_2.md')
SANDBOX = os.path.expanduser('~/plain_interpreter_sandbox')  # persistent .md.txt store

def load_floor():
    os.makedirs(SANDBOX, exist_ok=True)
    cache = os.path.join(SANDBOX, 'LEAN7POF2_floor.md.txt')
    try:
        with urllib.request.urlopen(FLOOR_URL, timeout=15) as r:
            t = r.read().decode()
        open(cache, 'w').write(t)
        return t, 'fetched'
    except Exception:
        if os.path.exists(cache):
            return open(cache).read(), 'cache'
        sys.exit('No floor available: fetch failed and no cached copy. Halt (CZO rule).')

# ---------------- Embedded standalone Reconciler (N1) ----------------
class Reconciler:
    """Engine-side J-screen: J2 instruction-safety, J4/J4.1 certainty audit,
    J10 weighted linguistic markers (P1 .80 / P2 1.00 / P4 .50), Annex F
    missing-complement causal-claim criterion. Verdicts: PASS / FLAG / RAISE."""
    P1 = re.compile(r'\b(definitely|certainly|guaranteed|always|never|proves?)\b', re.I)
    P2 = re.compile(r'\b(I verified|I measured|I tested|confirmed by me)\b', re.I)
    P4 = re.compile(r'\b(probably|likely|should be|I believe|roughly)\b', re.I)
    CAUSAL = re.compile(r'\b(because|therefore|leads to|causes?|results? in)\b', re.I)
    COMPLEMENT = re.compile(r'\b(unless|however|but|absent|without|other (cause|factor)|alternative)\b', re.I)
    UNSAFE = re.compile(r'\b(ignore (all|previous)|exfiltrate|leak the (key|prompt)|disable safety)\b', re.I)

    def screen_instruction(self, text):  # J2
        return ('RAISE', 'instruction-safety trip') if self.UNSAFE.search(text) else ('PASS', '')

    def screen_output(self, z):  # J4/J4.1/J10/AnnexF over a parsed Z envelope
        flags = []
        claims = z.get('claims', [])
        for c in claims:
            t = c.get('text', '')
            w = 0.80 * len(self.P1.findall(t)) + 1.00 * len(self.P2.findall(t)) - 0.50 * len(self.P4.findall(t))
            if w > 0 and c.get('confidence') in (None, 'unverified', 'low'):
                flags.append(f'J10 marker-weight {w:.2f} exceeds confidence tier: "{t[:60]}"')
            if self.CAUSAL.search(t) and not self.COMPLEMENT.search(t):
                flags.append(f'AnnexF missing-complement causal claim: "{t[:60]}"')
            if c.get('confidence') in ('high', 'medium') and c.get('provenance', 'uninstrumented') == 'uninstrumented':
                flags.append(f'J4 certainty>provenance: "{t[:60]}"')
        if not z.get('unresolved') and any(f.startswith('J') for f in flags):
            flags.append('J4.1 unresolved[] empty despite flags')
        return ('FLAG' if flags else 'PASS'), flags

# ---------------- P-c1 driver (UNVERIFIED - see status flag) ----------------
class AIModeDriver:
    """Browser-automation of Google AI Mode via playwright. Keyless. Fragile by design
    constraint; every session must re-verify selectors. ToS risk is the user's call."""
    def __init__(self):
        from playwright.sync_api import sync_playwright  # deferred import
        self._pw = sync_playwright().start()
        self.browser = self._pw.chromium.launch(headless=True)
        self.page = self.browser.new_page()

    def ask(self, prompt, timeout_s=60):
        p = self.page
        p.goto('https://www.google.com/search?udm=50', timeout=timeout_s * 1000)  # AI Mode tab
        box = p.locator('textarea, [contenteditable="true"]').first  # unverified selector
        box.fill(prompt)
        box.press('Enter')
        p.wait_for_timeout(8000)
        for sel in ('[data-attrid*="ai"]', 'div[role="main"]'):  # unverified selectors
            loc = p.locator(sel)
            if loc.count():
                return loc.first.inner_text()
        return ''

    def close(self):
        self.browser.close(); self._pw.stop()


# ---------------- P-a stable engine (Gemini API key) with emission-bound guard ----------------
MIN_CAP = 2500  # floor's own rule: reasoning models need cap >= reasoning + 2x visible
class GeminiAPIEngine:
    """Stable keyed alternative to the browser P-c1 path. Enforces MIN_CAP and does a
    one-shot truncation retry (doubling the cap) so the verbose Z envelope never truncates —
    the defect the live test surfaced (900-tok cap ate the envelope)."""
    def __init__(self):
        self.key = os.environ.get('GEMINI_API_KEY')
        if not self.key: sys.exit('P-a mode needs GEMINI_API_KEY in env. Or use P-c1 (browser) / P-c2 (Nano).')
    def _once(self, prompt, cap):
        import urllib.request
        url=('https://generativelanguage.googleapis.com/v1beta/models/'
             'gemini-2.5-flash:generateContent?key='+self.key)
        body={'contents':[{'parts':[{'text':prompt}]}],'generationConfig':{'maxOutputTokens':cap}}
        req=urllib.request.Request(url,data=json.dumps(body).encode(),headers={'content-type':'application/json'})
        with urllib.request.urlopen(req,timeout=60) as r: d=json.load(r)
        c=d['candidates'][0]
        txt='\n'.join(p.get('text','') for p in c.get('content',{}).get('parts',[]))
        return txt, c.get('finishReason')
    def ask(self, prompt, timeout_s=60):
        cap=MIN_CAP
        txt,fin=self._once(prompt,cap)
        if fin in ('MAX_TOKENS','LENGTH') or (txt and '{' in txt and txt.rstrip()[-1:] != '}'):
            txt,fin=self._once(prompt,cap*2)   # truncation retry
        return txt
    def close(self): pass

def build_prompt(floor, user_task, memory_txt):
    return (floor + '\n\n## PERSISTED CONTEXT (md.txt sandbox)\n' + memory_txt[:4000]
            + '\n\n## TASK\n' + user_task + '\n\nEmit ONLY the Z JSON object.')

def parse_z(raw):
    m = re.search(r'\{.*\}', raw, re.S)
    if not m: return None
    try: return json.loads(m.group(0))
    except Exception: return None

def main():
    print(__doc__.split('***')[1].join(['***', '***']))  # surface the warning first
    floor, src = load_floor()
    print(f'[floor: LEAN7POF2 v1.2 ({src})] [sandbox: {SANDBOX}]')
    rec = Reconciler()
    mem_path = os.path.join(SANDBOX, 'session_memory.md.txt')
    memory = open(mem_path).read() if os.path.exists(mem_path) else ''
    task = ' '.join(sys.argv[1:]) or input('task> ')
    verdict, why = rec.screen_instruction(task)
    if verdict == 'RAISE':
        print(f'RAISED instead of executed (R5/J2): {why}'); return
    mode = os.environ.get('PLAIN_MODE', 'browser')
    try:
        drv = GeminiAPIEngine() if mode == 'api' else AIModeDriver()
    except Exception as e:
        sys.exit(f'engine unavailable ({e}). Modes: PLAIN_MODE=api (P-a, stable, needs GEMINI_API_KEY) or default browser P-c1 (keyless, unstable).')
    raw = drv.ask(build_prompt(floor, task, memory)); drv.close()
    z = parse_z(raw)
    if z is None:
        print('Engine did not bind Z (raw below, unverified):\n', raw[:1500]); return
    v, flags = rec.screen_output(z)
    z.setdefault('unresolved', []).extend(flags)
    print(json.dumps(z, indent=1))
    with open(mem_path, 'a') as f:
        f.write(f"\n- [{time.strftime('%Y%m%d')}] task: {task[:80]} | reconciler: {v} ({len(flags)} flags)")

if __name__ == '__main__':
    main()
