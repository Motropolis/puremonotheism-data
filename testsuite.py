"""puremonotheism-data audit suite — repo-relative, runs from a fresh clone.

Usage:  python3 testsuite.py [path-to-repo]      (defaults to this file's directory)

Requires only the repo itself, except two accuracy tests (A1, and the Corpus parts)
which need the Quranic Arabic Corpus morphology file. It is downloaded automatically
to .cache/ on first run; if the network is unavailable those tests are skipped and
reported as SKIP rather than silently passing.
"""
import json, glob, os, re, sys, collections, statistics, urllib.request

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__)))
DATA = ROOT
LEX  = os.path.join(ROOT, 'lexicon_full')
BROWSE = os.path.join(ROOT, 'browse')
DSEARCH = os.path.join(ROOT, 'dictsearch')
IDXF = os.path.join(ROOT, 'roots-index-full.json')
LMAP = os.path.join(ROOT, 'letter_map.json')
CACHE = os.path.join(ROOT, '.cache'); os.makedirs(CACHE, exist_ok=True)
CORPUS_TXT = os.path.join(CACHE, 'quran-morphology.txt')
CORPUS_URL = 'https://raw.githubusercontent.com/mustafa0x/quran-morphology/master/quran-morphology.txt'
def _fetch_corpus():
    """Fetch the Corpus morphology. macOS python.org builds often lack CA certs,
    so fall back to an unverified context and then to curl before giving up."""
    import ssl, subprocess
    try:
        urllib.request.urlretrieve(CORPUS_URL, CORPUS_TXT); return True
    except Exception:
        pass
    try:
        ctx = ssl._create_unverified_context()
        with urllib.request.urlopen(CORPUS_URL, context=ctx, timeout=120) as r, open(CORPUS_TXT,'wb') as f:
            f.write(r.read())
        return True
    except Exception:
        pass
    try:
        subprocess.run(['curl','-sL','-o',CORPUS_TXT,CORPUS_URL], check=True, timeout=180)
        return os.path.getsize(CORPUS_TXT) > 1000
    except Exception as e:
        print('note: could not fetch Corpus morphology (%s)' % e)
        if os.path.exists(CORPUS_TXT) and os.path.getsize(CORPUS_TXT) < 1000:
            os.remove(CORPUS_TXT)
        return False

if not os.path.exists(CORPUS_TXT):
    _fetch_corpus()
HAVE_CORPUS = os.path.exists(CORPUS_TXT) and os.path.getsize(CORPUS_TXT) > 1000
if not HAVE_CORPUS:
    print('note: Corpus morphology unavailable — test A1 will report SKIP.')
    print('      to enable it, run:  curl -sL -o .cache/quran-morphology.txt %s' % CORPUS_URL)

# ---- normalisation helpers (inlined so the suite has no external imports) ----
_DIA = re.compile('[\u064b-\u0652\u0670\u0640\u0653-\u0655]')
def norm(s):
    s = _DIA.sub('', s or '').replace('\u0671', '\u0627')
    for a in '\u0623\u0625\u0622': s = s.replace(a, '\u0627')
    return s.replace('\u0649', '\u064a').replace('\u0629', '\u0647').strip()
_WEAK = '\u064a\u0648\u0627'
def variants(ar, lat):
    n = norm(ar); p = lat.split('-'); out = [n]
    if len(p) >= 3 and p[-1] == p[-2] and len(n) >= 3: out.append(n[:-1])
    if p[-1] in ('y','w','a') or (n and n[-1] in _WEAK):
        out += [n[:-1] + w for w in _WEAK] + [n[:-1]]
    if p[1:2] and p[1] in ('y','w','a') and len(n) == 3:
        out += [n[0] + w + n[2] for w in _WEAK] + [n[0] + n[2]]
    if n and n[0] in '\u0648\u064a': out += [w + n[1:] for w in '\u0648\u064a']
    seen = set(); return [x for x in out if x and not (x in seen or seen.add(x))]
def loose(ar, lat, wide=False):
    n = norm(ar); out = []
    if len(n) == 4 and n[:2] == n[2:]: out.append(n[:2])
    if wide and len(n) >= 4: out += [n[:3], n[-3:]]
    if len(n) == 3 and n[0] == n[2]: out += [n[1:], n[:2]]
    if n.startswith('\u0627') and len(n) > 2: out.append(n[1:])
    if len(n) == 3 and n[1] == n[2]: out.append(n[:2])
    seen = set(); return [x for x in out if len(x) >= 2 and not (x in seen or seen.add(x))]
STOP = set('''أبوعبيد أخبرنا أخبرني أراد أما أنشد أي أيضا الأصمعي الجمع الفراء الليث اي تفسيره تقول ثعلب ثم جمعه حدثنا حدثني رواه روى فأما فقال فيه قال قالوا قلت قوله قيل كقوله مثل معناه منه منها نحو وأخبرني وأراد وأما وأنشد واحدته والجمع وتفسيره وتقول وحدثني وروى وفيه وقال وقالوا وقوله وقيل ومعناه ومنه ومنها وهو وهي ويروى ويروي ويريد ويقال يروى يروي يريد يعني يقال ينشد'''.split())
RESULTS=[]
def t(name, ok, detail=''): RESULTS.append((name, ok, detail)); return ok

# ---------- load once ----------
lex={}
for f in glob.glob(LEX+'/*.json'):
    d=json.load(open(f)); lex[d['root']]=d
idx={x['r']:x for x in json.load(open(IDXF))['roots']}
qidx={x['r']:x for x in json.load(open(DATA+'/meta/roots-index.json'))['roots']}
fw=json.load(open(DATA+'/meta/function-words.json'))['map']
lemmas={os.path.basename(f)[:-5] for f in glob.glob(DATA+'/lemma/*.json')}
prons={os.path.basename(f)[:-5] for f in glob.glob(DATA+'/pronoun/*.json')}
muqs={os.path.basename(f)[:-5] for f in glob.glob(DATA+'/muqattaat/*.json')}
roots_q={os.path.basename(f)[:-5] for f in glob.glob(DATA+'/root/*.json')}

# ===== T1 schema integrity =====
bad=[]
REQ=('root','root_ar','quranic','classical')
for r,d in lex.items():
    for k in REQ:
        if k not in d: bad.append((r,'missing '+k))
    if not isinstance(d.get('classical'),list): bad.append((r,'classical not list'))
t('T1  schema: required fields present', not bad, f'{len(bad)} violations {bad[:3]}')

# ===== T2 no empty content =====
empty=[r for r,d in lex.items() if not d['classical'] and not d.get('lane')]
blank=[(r,c['id']) for r,d in lex.items() for c in d['classical'] for e in c.get('entries',[]) if not (e.get('text') or '').strip()]
t('T2  no empty roots / blank entries', not empty and not blank, f'{len(empty)} empty roots, {len(blank)} blank entries')

# ===== T3 index <-> disk parity =====
onlyidx=set(idx)-set(lex); onlydisk=set(lex)-set(idx)
t('T3  index/disk parity', not onlyidx and not onlydisk, f'idx-only {len(onlyidx)}, disk-only {len(onlydisk)} {sorted(onlydisk)[:3]}')

# ===== T4 index dictionary lists match file contents =====
mism=[]
for r,d in lex.items():
    want=[c['id'] for c in d['classical']]+(['lane'] if d.get('lane') else [])
    if r in idx and sorted(idx[r]['d'])!=sorted(want): mism.append(r)
t('T4  index d[] matches file contents', not mism, f'{len(mism)} mismatched {mism[:3]}')

# ===== T5 chronological ordering =====
unsorted_=[r for r,d in lex.items() if [c['died'] for c in d['classical']]!=sorted(c['died'] for c in d['classical'])]
t('T5  classical blocks chronologically sorted', not unsorted_, f'{len(unsorted_)} unsorted {unsorted_[:3]}')

# ===== T6 provenance completeness =====
noprov=[(r,c['id']) for r,d in lex.items() for c in d['classical'] if not c.get('source')]
nomt=[(r,c['id']) for r,d in lex.items() for c in d['classical'] if not c.get('match_type')]
t('T6  every block has source + match_type', not noprov and not nomt, f'{len(noprov)} no source, {len(nomt)} no match_type')

# ===== T7 compiler/date consistency across all files =====
seen=collections.defaultdict(set)
for d in lex.values():
    for c in d['classical']: seen[c['id']].add((c['compiler'],c['died'],c['tier']))
incons={k:v for k,v in seen.items() if len(v)>1}
t('T7  dictionary metadata consistent everywhere', not incons, str({k:len(v) for k,v in incons.items()}))

# ===== T8 anachronism scan (modern contamination) =====
MOD=['التيفوئيد','الكهرباء','الهاتف','التلفاز','الكمبيوتر','البنزين','الميكروب','الإنترنت','الراديو']
hits=collections.Counter()
for r,d in lex.items():
    for c in d['classical']:
        txt=' '.join(e['text'] for e in c['entries'])
        for m in MOD:
            if m in txt: hits[(c['id'],m)]+=1
t('T8  no modern-term contamination in classical text', not hits, str(dict(hits)))

# ===== T9 truncation =====
tr=[(r,c['id']) for r,d in lex.items() for c in d['classical'] for e in c['entries']
    if e['text'].rstrip().endswith(('…','...')) and not e.get('source_ellipsis')]
allell=sum(1 for d in lex.values() for c in d['classical'] for e in c['entries'] if e['text'].rstrip().endswith(('…','...')))
t('T9  no cap-truncated entries', not tr, f'{len(tr)} cap artifacts ({allell} source-native ellipses, verified)')

# ===== T10 duplicate detection =====
dupar=collections.Counter(d['root_ar'] for d in lex.values())
dups={k:v for k,v in dupar.items() if v>1}
t('T10 no duplicate root spellings', not dups, str(dict(list(dups.items())[:5])))

# ===== T11 encoding sanity =====
CTRL=re.compile('[\u0000-\u0008\u000b\u000c\u000e-\u001f\ufffd]')
enc=[(r,c['id']) for r,d in lex.items() for c in d['classical'] for e in c['entries'] if CTRL.search(e['text'])]
t('T11 no control chars / replacement chars', not enc, f'{len(enc)} affected blocks {enc[:3]}')

# ===== T12 arabic content present in arabic dictionaries =====
AR=re.compile('[\u0621-\u064a]')
noar=[(r,c['id']) for r,d in lex.items() for c in d['classical'] if not AR.search(' '.join(e['text'] for e in c['entries']))]
t('T12 arabic dictionaries contain arabic text', not noar, f'{len(noar)} blocks lack arabic {noar[:3]}')

# ===== T13 quranic flag agrees with quran root list =====
mismq=[r for r,d in lex.items() if d['quranic'] != (r in qidx)]
t('T13 quranic flag matches meta/roots-index', not mismq, f'{len(mismq)} disagreements {mismq[:5]}')

# ===== T14 word-link referential integrity (reader) =====
missing=collections.Counter(); tot=0; kinds=collections.Counter()
for f in glob.glob(DATA+'/interlinear/*.json'):
    d=json.load(open(f))
    vs=d if isinstance(d,list) else d.get('verses') or list(d.values())[0]
    for v in (vs if isinstance(vs,list) else vs.values()):
        for w in (v.get('w') or []):
            tot+=1
            if w.get('r'):
                kinds['r']+=1
                if w['r'] not in roots_q: missing['r:'+w['r']]+=1
                if w['r'] not in lex: missing['r-dict:'+w['r']]+=1
            elif w.get('lm'):
                kinds['lm']+=1
                if w['lm'] not in lemmas: missing['lm:'+w['lm']]+=1
            elif w.get('fw'):
                kinds['fw']+=1
                if w['fw'] not in lex: missing['fw:'+w['fw']]+=1
            elif w.get('pr'):
                kinds['pr']+=1
                if w['pr'] not in prons: missing['pr:'+w['pr']]+=1
            elif w.get('mq'):
                kinds['mq']+=1
                if w['mq'] not in muqs: missing['mq:'+w['mq']]+=1
            else: missing['UNLINKED']+=1
t('T14 every word link resolves to an existing file', not missing,
  f'{tot} tokens, {dict(kinds)}, broken: {dict(list(missing.items())[:5])}')

# ===== T15 root occurrence counts =====
badc=[]
for f in glob.glob(DATA+'/root/*.json'):
    d=json.load(open(f))
    if d['count']!=len(d['occ']) or d['count']!=qidx.get(d['root'],{}).get('n'): badc.append(d['root'])
t('T15 root counts == occ length == index n', not badc, f'{len(badc)} inconsistent {badc[:3]}')

# ===== T16 occurrence keys point at real verses =====
sur={}
for f in glob.glob(DATA+'/surah/*.json'):
    s=json.load(open(f))
    for v in (s['verses'] if isinstance(s,dict) else s): sur[v['k']]=len(v.get('w') or [])
badocc=[]
for f in glob.glob(DATA+'/root/*.json'):
    d=json.load(open(f))
    for o in d['occ']:
        v=o['v']; i=int(o['k'].split(':')[2])
        if v not in sur or i>sur[v]: badocc.append(o['k'])
t('T16 occurrence keys reference real word positions', not badocc, f'{len(badocc)} dangling {badocc[:5]}')

# ===== T17 function-word map targets exist =====
badfw=[L for L,e in fw.items() if e.get('type')=='dict' and e['slug'] not in lex]
t('T17 function-word map targets exist', not badfw, f'{len(badfw)} {badfw[:5]}')

# ===== T18 browse index parity =====
bl=json.load(open(os.path.join(BROWSE,'browse-manifest.json')))
alpha=0
for L in bl['letters']:
    alpha+=len(json.load(open(os.path.join(BROWSE,L['file'])))['roots'])
t('T18 browse alpha shards cover every root', alpha==len(idx), f'{alpha} in shards vs {len(idx)} in index')

# ===== T19 per-dictionary browse counts match reality =====
real=collections.Counter()
for r,d in lex.items():
    for c in d['classical']: real[c['id']]+=1
    if d.get('lane'): real['lane']+=1
bad19={k:(v,real[k]) for k,v in bl['dicts'].items() if v!=real[k]}
t('T19 per-dictionary browse counts accurate', not bad19, str(bad19))

# ===== T20 search shard round-trip =====
import random
random.seed(11)
sample=random.sample(list(lex),40); missed=[]
for r in sample:
    ar=norm(lex[r]['root_ar'])
    if not ar: continue
    fn=os.path.join(DSEARCH, f'ds-{ord(ar[0]):04x}.json')
    if not os.path.exists(fn): missed.append((r,'no shard')); continue
    sh=json.load(open(fn))
    if ar not in sh or r not in sh[ar]: missed.append((r,ar))
t('T20 search index round-trip (sample 40)', len(missed)<=4, f'{len(missed)} not self-findable {missed[:4]}')

print(f"{'TEST':60}{'RESULT':8}DETAIL")
print('-'*120)
npass=0
for name,ok,det in RESULTS:
    npass+=ok
    print(f"{name:60}{'PASS' if ok else 'FAIL':8}{det[:70]}")
print('-'*120)
print(f'{npass}/{len(RESULTS)} passed')

# ================= ACCURACY TESTS (content, not structure) =================
print()
ACC=[]
def a(name, ok, detail=''): ACC.append((name,ok,detail))

# A1 root assignments vs Quranic Arabic Corpus (ground truth)
def _load_corpus():
    corpus=collections.defaultdict(set); lem=collections.defaultdict(set); toks=set()
    if not HAVE_CORPUS: return corpus, lem, toks
    for line in open(CORPUS_TXT, encoding='utf-8'):
        p=line.rstrip('\n').split('\t')
        if len(p)<4: continue
        s_,a_,w_,seg=p[0].split(':')
        k=f'{int(s_)}:{int(a_)}:{int(w_)}'; toks.add(k)
        m=re.search(r'ROOT:([^|]+)',p[3])
        if m: corpus[k].add(m.group(1))
        m=re.search(r'LEM:([^|]+)',p[3])
        if m: lem[k].add(m.group(1))
    return corpus, lem, toks
corpus,LEM,ctok=_load_corpus()
LM=json.load(open(LMAP)); INV={}
for ar,la in LM.items(): INV.setdefault(la,ar)
def s2a(s): return ''.join(INV.get(p,p) for p in s.split('-'))
DIA=re.compile('[\u064b-\u0652\u0670\u0640\u0653-\u0655]')
def cn(s):
    s=DIA.sub('',s)
    for x in '\u0623\u0625\u0622\u0671': s=s.replace(x,'\u0627')
    return s.replace('\u0649','\u064a').replace('\u0629','\u0647').replace('\u0621','\u0627').replace('\u0624','\u0627').replace('\u0626','\u0627')
REALIGNED={'13:37','15:7','27:20','2:181','36:22','37:130','8:6'}
CSURF={}
if HAVE_CORPUS:
    for line in open(CORPUS_TXT,encoding='utf-8'):
        _p=line.rstrip('\n').split('\t')
        if len(_p)<4: continue
        _s,_a,_w,_g=_p[0].split(':'); _k=f'{int(_s)}:{int(_a)}:{int(_w)}'
        CSURF[_k]=CSURF.get(_k,'')+_p[1]
ag=dis=0; dl=[]
for f in (glob.glob(DATA+'/interlinear/*.json') if HAVE_CORPUS else []):
    d=json.load(open(f)); vs=d if isinstance(d,list) else d.get('verses') or list(d.values())[0]
    for v in (vs if isinstance(vs,list) else vs.values()):
        k=v.get('k') or v.get('key')
        for w in (v.get('w') or []):
            if not w.get('r'): continue
            cr=corpus.get(f"{k}:{w['i']}")
            if k in REALIGNED:
                # index positions differ from the corpus here by construction;
                # match on surface form instead
                surf=cn(re.sub('[^\u0621-\u064a]','',w.get('ar','')))
                cr=set()
                for ck,cs in CSURF.items():
                    if ck.startswith(k+':') and (cn(cs)==surf or surf in cn(cs) or cn(cs) in surf):
                        cr |= corpus.get(ck,set())
            if not cr: continue
            if cn(s2a(w['r'])) in {cn(x) for x in cr}: ag+=1
            else:
                dis+=1
                if len(dl)<5: dl.append((k,w['i'],w['r'],sorted(cr)))
a('A1  root assignments match Quranic Corpus', (dis==0) if HAVE_CORPUS else None, (f'{ag} agree, {dis} disagree {dl[:3]}' if HAVE_CORPUS else 'corpus file unavailable — see note above'))

# A2 headword/root trace inside each dictionary entry
WEAK=set('اويءة')
def sk(x): return [c for c in x if c not in WEAK]
def sub(s,w):
    it=iter(w); return all(c in it for c in s)
flag=0; tot2=0
for r,d in lex.items():
    for c in d['classical']:
        tot2+=1
        toks=[norm(x) for x in re.findall('[\u0621-\u064a]{2,}', DIA.sub('',' '.join(e['text'] for e in c['entries'])[:400]))]
        forms=[d['root_ar']]+variants(d['root_ar'],r)
        ok=None
        for fm in forms:
            s=sk(norm(fm))
            if len(s)<2: continue
            ok=False if ok is None else ok
            if any(sub(s,t) for t in toks): ok=True; break
        if ok is False: flag+=1
a('A2  entry text traces back to its root', flag/max(tot2,1) < 0.005, f'{flag}/{tot2} untraceable ({100*flag/max(tot2,1):.2f}%)')

# A3 proper-noun glosses are curated, not homographs
bad3=[]
for f in glob.glob(DATA+'/lemma/*.json'):
    d=json.load(open(f))
    if 'proper noun' not in (d.get('g') or ''): continue
    if d.get('gloss') and d.get('gloss_source')!='curated (proper noun)' and d.get('gloss_homograph_note') is None:
        pass
    if d.get('gloss_source')=='curated (proper noun)': continue
    if d.get('gloss'): bad3.append((d['lemma_ar'],str(d['gloss'])[:30]))
a('A3  proper-noun glosses curated', len(bad3)<=8, f'{len(bad3)} uncurated {bad3[:4]}')

# A4 chronological tiers plausible (no dictionary dated after its successor)
ORDERD=['ayn','tahdhib','sihah','maqayis','mufradat','lisan','qamus']
years={'ayn':786,'tahdhib':980,'sihah':1002,'maqayis':1004,'mufradat':1108,'lisan':1311,'qamus':1414}
bad4=[(r,c['id'],c['died']) for r,d in lex.items() for c in d['classical'] if c['id'] in years and c['died']!=years[c['id']]]
a('A4  dictionary death-dates correct everywhere', not bad4, f'{len(bad4)} wrong {bad4[:3]}')

# A5 lemma pages uncapped
lt=sum(1 for f in glob.glob(DATA+'/lemma/*.json') for c in (json.load(open(f)).get('classical') or [])
       for e in (c.get('entries') or []) if e['text'].rstrip().endswith(('…','...')))
a('A5  lemma pages uncapped', lt==0, f'{lt} truncated lemma entries')

# A6 every Quranic root reachable from the dictionary layer
unreach=[r for r in qidx if r not in lex]
a('A6  every Quranic root has a dictionary page', not unreach, f'{len(unreach)} unreachable {unreach[:5]}')


# A7 entry headword compatible with the root (catches wrong-root articles)
HEADRE=re.compile(r'^[^\u0621-\u064a]{0,6}\(?([\u0621-\u064a]{2,8})\)?\s*[:\u061b]')
_WEAK=set('\u0627\u0648\u064a\u0621')
_NARR=set("""يقال ويقال قال وقال قلت الاصمعي الليث الفراء ثعلب الكسائي قرئ قولهم سيبويه الخليل الازهري""".split())
_sk=lambda x: ''.join(c for c in x if c not in _WEAK)
def _issub(a,b):
    it=iter(b); return all(c in it for c in a)
wrong=0; judged=0
for r,d in lex.items():
    for c in d['classical']:
        m=HEADRE.match(DIA.sub('', c['entries'][0]['text'].lstrip()))
        if not m: continue
        hw=norm(m.group(1))
        if hw in _NARR or hw in STOP: continue
        forms={norm(d['root_ar'])}|set(variants(d['root_ar'],r))|set(loose(d['root_ar'],r,wide=True))
        fs=[_sk(f) for f in forms if len(_sk(f))>=2]
        h=hw[2:] if hw.startswith('\u0627\u0644') and len(hw)>3 else hw
        hs=_sk(h)
        if not fs or len(hs)<2: continue
        judged+=1
        if not any(_issub(f,hs) for f in fs): wrong+=1
a('A7  entry headword compatible with root', wrong==0, f'{wrong} wrong-root blocks of {judged} judged')


# A8 no block carries an unrelated root's article (headword owns another page)
_byar={x['ar']:x['r'] for x in json.load(open(IDXF))['roots']}
coll=0
for r,d in lex.items():
    legit={norm(d['root_ar'])}|set(variants(d['root_ar'],r))
    for c in d['classical']:
        m=HEADRE.match(DIA.sub('', c['entries'][0]['text'].lstrip()))
        if not m: continue
        hw=norm(m.group(1))
        if hw in _NARR or hw in STOP: continue
        h=hw[2:] if hw.startswith('\u0627\u0644') and len(hw)>3 else hw
        if h in legit: continue
        if c.get('filed_under') and norm(c['filed_under'])==h: continue
        if h in _byar and _byar[h]!=r and not c.get('suspect'): coll+=1
a('A8  no unrelated root article attached', coll==0, f'{coll} collisions')




# A9 Lane field must not carry another root's article
_AR=re.compile('[\u0621-\u064a]{2,}')
def _redup_ok(root,hw):
    n=norm(root)
    if len(n)==4 and n[:2]==n[2:] and hw==n[:2]: return True
    if len(n)>=3 and n[-1]==n[-2] and hw in (n[:-1],n[:2]): return True
    return False
lw=0
for r,d in lex.items():
    if not d.get('lane'): continue
    tk=_AR.findall(DIA.sub('', d['lane'][:200]))
    if not tk: continue
    hw=norm(tk[0])
    ok={norm(d['root_ar'])}|set(variants(d['root_ar'],r))
    if hw in ok: continue
    if hw in _byar and _byar[hw]!=r and not _redup_ok(d['root_ar'],hw): lw+=1
a('A9  Lane field carries the correct root', lw==0, f'{lw} wrong Lane blocks')


# A10 lemma blocks: article must name the lemma; provenance complete
_L=os.path.join(DATA,'lemma')
_AR2=re.compile('[\u0621-\u064a]{2,}')
lm_bad=0; lm_noprov=0; lm_blocks=0
for _f in glob.glob(_L+'/*.json'):
    _d=json.load(open(_f)); _nm=norm(_d['lemma_ar'])
    _core=_nm[2:] if _nm.startswith('\u0627\u0644') and len(_nm)>4 else _nm
    for _c in (_d.get('classical') or []):
        lm_blocks+=1
        if 'source' not in _c or 'match_type' not in _c: lm_noprov+=1
        _t=norm(DIA.sub('',' '.join(e['text'] for e in _c.get('entries') or [])))
        if _core and _core not in _t and _nm not in _t and _c.get('match_type')!='headword-verified': lm_bad+=1
a('A10 lemma blocks name their lemma + have provenance', lm_bad<=1 and lm_noprov==0,
  f'{lm_bad} unnamed, {lm_noprov} missing provenance, of {lm_blocks} blocks')


# A11-A13 provenance and manifest additions (v3.0.0)
_ls=[r for r,d in lex.items() if d.get('lane') and not d.get('lane_source')]
a('A11 every Lane block carries lane_source', not _ls, f'{len(_ls)} missing')
_dm=os.path.join(DATA,'dictionaries.json')
_ok=os.path.exists(_dm)
if _ok:
    _md=json.load(open(_dm))['dictionaries']
    _cnt=json.load(open(os.path.join(DATA,'browse','browse-manifest.json')))['dicts']
    _ok = ({x['id'] for x in _md}==set(_cnt)
           and all(x.get('roots')==_cnt[x['id']] for x in _md)
           and [x['died'] for x in _md]==sorted(x['died'] for x in _md))
a('A12 dictionaries.json matches manifest and is date-ordered', _ok,
  'ids, counts and death-year order all verified' if _ok else 'missing or inconsistent')
_bad=[os.path.basename(_f) for _f in glob.glob(os.path.join(DATA,'browse','dict-*.json'))
      if any('d' not in _r for _r in json.load(open(_f))['roots'][:200])]
a('A13 per-dictionary browse rows carry d[]', not _bad, f'{len(_bad)} files without d[]')


# A14 Lane text carries no raw HTML markup
_html=[r for r,d in lex.items() if d.get('lane') and re.search(r'</?[a-zA-Z][^>]*>', d['lane'])]
a('A14 Lane text free of raw HTML markup', not _html, f'{len(_html)} roots with visible tags')
# A15 lemma truncated flag agrees with reality
_mis=[]
for _f in glob.glob(os.path.join(DATA,'lemma','*.json')):
    _d=json.load(open(_f))
    if (_d['count']>len(_d['occ'])) != bool(_d.get('truncated')): _mis.append(os.path.basename(_f))
    if _d['count']>len(_d['occ']) and not _d.get('occ_note'): _mis.append(os.path.basename(_f)+':no-note')
a('A15 lemma truncated flag matches occ list and is explained', not _mis, f'{len(_mis)} wrong {_mis[:3]}')


# A16 meaning paragraphs name the root, not a form derived from it
_DIAX=re.compile('[\u064b-\u0652\u0670\u0640\u0653-\u0655]')
def _nz(x):
    x=_DIAX.sub('',x or '')
    for _a in '\u0623\u0625\u0622': x=x.replace(_a,'\u0627')
    return x.replace('\u0649','\u064a').replace('\u0629','')
_mm=[]
for _f in glob.glob(os.path.join(DATA,'root','*.json')):
    _d=json.load(open(_f)); _t=_d.get('meaning') or ''
    _m=re.match(r'\s*The root\s+([\u0621-\u064a\u064b-\u0652\s\-]+?)\s*[\(,]', _t)
    if not _m: continue
    _named=_nz(_m.group(1).replace(' ','').replace('-','')); _act=_nz(_d['root_ar'])
    if _named and _named!=_act and len(_named)>len(_act) and all(c in _named for c in _act):
        _mm.append((_d['root_ar'],_m.group(1).strip()))
a('A16 meanings name the root, not a derived form', not _mm, f'{len(_mm)} mislabelled {_mm[:3]}')

print(f"{'ACCURACY TEST':60}{'RESULT':8}DETAIL")
print('-'*120)
p2=0
for n,ok,dt in ACC:
    lab='SKIP' if ok is None else ('PASS' if ok else 'FAIL')
    p2+= 1 if ok else 0
    print(f"{n:60}{lab:8}{dt[:70]}")
print('-'*120)
print(f'{p2}/{len(ACC)} accuracy tests passed   |   {npass}/{len(RESULTS)} integrity tests passed')

# ================= LAYER TESTS (quran text, grammar, translations, indexes) =====
D=[]
def dd(n,ok,det=''): D.append((n,ok,det))
_verses=set(); _wc={}
for _f in glob.glob(DATA+'/surah/*.json'):
    for _v in json.load(open(_f))['verses']:
        _verses.add(_v['k']); _wc[_v['k']]=len(_v.get('w') or [])
CANON=[7,286,200,176,120,165,206,75,129,109,123,111,43,52,99,128,111,110,98,135,112,78,118,64,77,227,93,88,69,60,34,30,73,54,45,83,182,88,75,85,54,53,89,59,37,35,38,29,18,45,60,49,62,55,78,96,29,22,24,13,14,11,11,18,12,12,30,52,52,44,28,28,20,56,40,31,50,40,46,42,29,19,36,25,22,17,19,26,30,20,15,21,11,8,8,19,5,8,8,11,11,8,3,9,5,4,7,3,6,3,5,4,5,6]
dd('D1  6236 verses across 114 surahs', len(_verses)==6236 and len(glob.glob(DATA+'/surah/*.json'))==114, f'{len(_verses)} verses')
_bad=[i for i,n in enumerate(CANON,1) if sum(1 for k in _verses if k.startswith(f'{i}:'))!=n]
dd('D2  verse counts match the canonical index', not _bad, f'{len(_bad)} surahs wrong')
_il={}
for _f in glob.glob(DATA+'/interlinear/*.json'):
    _d=json.load(open(_f)); _vs=_d if isinstance(_d,list) else _d.get('verses') or list(_d.values())[0]
    for _v in (_vs if isinstance(_vs,list) else _vs.values()): _il[_v.get('k') or _v.get('key')]=_v
dd('D3  interlinear matches surah verse-for-verse', set(_il)==_verses and not [k for k in _il if len(_il[k].get('w') or [])!=_wc.get(k)], 'sets and word counts agree')
_ut=sum(1 for v in _il.values() for w in (v.get('w') or []) if not w.get('g'))
dd('D4  every word token carries a grammar tag', _ut==0, f'{_ut} untagged')
_td=[x for x in glob.glob(DATA+'/translation/*') if os.path.isdir(x)]
_meta={x.get('id') or x.get('key') or x.get('slug') for x in json.load(open(DATA+'/meta/translations.json'))['translations']}
_gap={}
for _x in _td:
    _j=json.load(open(_x+'/all.json')); _b=_j.get('verses')
    if len(set(_b)&_verses)!=6236: _gap[os.path.basename(_x)]=len(set(_b)&_verses)
dd('D5  all translations cover all 6236 verses', not _gap and _meta=={os.path.basename(x) for x in _td}, f'{len(_td)} translations, gaps {_gap}')
_ok=True; _det=[]
for _lay,_f,_k,_idk in (('pronoun','pronoun-index.json','pronouns','k'),('muqattaat','muqattaat-index.json','sets','k'),('lemma','lemma-index.json','lemmas','l')):
    _files={os.path.basename(x)[:-5] for x in glob.glob(f'{DATA}/{_lay}/*.json')}
    _lst=json.load(open(f'{DATA}/meta/{_f}'))[_k]
    _ids={x.get(_idk) for x in _lst}
    if _ids!=_files: _ok=False; _det.append(_lay)
    for _e in _lst:
        _p=f"{DATA}/{_lay}/{_e[_idk]}.json"
        if os.path.exists(_p):
            _o=json.load(open(_p)); _n=_o.get('count') if _o.get('count') is not None else len(_o.get('occ') or [])
            if _e.get('n') is not None and _e['n']!=_n: _ok=False; _det.append(_lay+':count')
dd('D6  pronoun/muqattaat/lemma indexes match files and counts', _ok, str(set(_det)))
_nm=[]; _ne=[]
for _f in glob.glob(DATA+'/root/*.json'):
    _d=json.load(open(_f))
    if not (_d.get('meaning') or '').strip(): _nm.append(_d['root'])
    if not _d.get('en') and _d['count']>=15: _ne.append(_d['root'])
dd('D7  every root has a meaning paragraph', not _nm, f'{len(_nm)} missing')
_lowfreq=sum(1 for _f in glob.glob(DATA+'/root/*.json') for _d in [json.load(open(_f))] if not _d.get('en') and _d['count']<15)
dd('D8  roots with >=15 occurrences have an en gloss', not _ne,
   f'{len(_ne)} missing; {_lowfreq} low-frequency roots lack one by method design')
_pb=0;_pt=0
for _f in glob.glob(DATA+'/parallels/*.json')+glob.glob(DATA+'/phrases/*.json')+glob.glob(DATA+'/search/*.json'):
    for _m in re.finditer(r'"(\d{1,3}:\d{1,3})"', open(_f).read()):
        _pt+=1
        if _m.group(1) not in _verses: _pb+=1
dd('D9  parallels/phrases/search verse refs valid', _pb==0, f'{_pb} dangling of {_pt}')
print()
print(f"{'LAYER TEST':60}{'RESULT':8}DETAIL")
print('-'*120)
_p=0
for n,ok,det in D:
    _p+=ok; print(f"{n:60}{'PASS' if ok else 'FAIL':8}{det[:60]}")
print('-'*120)
print(f'{_p}/{len(D)} layer tests passed')
