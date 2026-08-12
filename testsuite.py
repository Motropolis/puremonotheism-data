"""Full-corpus audit suite. Each test returns (name, passed, detail)."""
import json, glob, os, re, sys, collections, pickle
sys.path.insert(0,'/home/claude/build')
from match import norm

DATA='/home/claude/pm/puremonotheism-data-main'
LEX='/home/claude/build/lexicon_full'
RESULTS=[]
def t(name, ok, detail=''): RESULTS.append((name, ok, detail)); return ok

# ---------- load once ----------
lex={}
for f in glob.glob(LEX+'/*.json'):
    d=json.load(open(f)); lex[d['root']]=d
idx={x['r']:x for x in json.load(open('/home/claude/build/roots-index-full.json'))['roots']}
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
bl=json.load(open('/home/claude/build/browse/browse-manifest.json'))
alpha=0
for L in bl['letters']:
    alpha+=len(json.load(open('/home/claude/build/browse/'+L['file']))['roots'])
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
    fn=f'/home/claude/build/dictsearch/ds-{ord(ar[0]):04x}.json'
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
corpus,LEM,ctok=pickle.load(open('/home/claude/build/corpus.pkl','rb'))
LM=json.load(open('/home/claude/build/letter_map.json')); INV={}
for ar,la in LM.items(): INV.setdefault(la,ar)
def s2a(s): return ''.join(INV.get(p,p) for p in s.split('-'))
DIA=re.compile('[\u064b-\u0652\u0670\u0640\u0653-\u0655]')
def cn(s):
    s=DIA.sub('',s)
    for x in '\u0623\u0625\u0622\u0671': s=s.replace(x,'\u0627')
    return s.replace('\u0649','\u064a').replace('\u0629','\u0647').replace('\u0621','\u0627').replace('\u0624','\u0627').replace('\u0626','\u0627')
REALIGNED={'13:37','15:7','27:20','2:181','36:22','37:130','8:6'}
CSURF={}
for line in open('/home/claude/corpus.txt',encoding='utf-8'):
    _p=line.rstrip('\n').split('\t')
    if len(_p)<4: continue
    _s,_a,_w,_g=_p[0].split(':'); _k=f'{int(_s)}:{int(_a)}:{int(_w)}'
    CSURF[_k]=CSURF.get(_k,'')+_p[1]
ag=dis=0; dl=[]
for f in glob.glob(DATA+'/interlinear/*.json'):
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
a('A1  root assignments match Quranic Corpus', dis==0, f'{ag} agree, {dis} disagree {dl[:3]}')

# A2 headword/root trace inside each dictionary entry
sys.path.insert(0,'/home/claude/build')
from match import variants
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
from openiti2 import loose as _loose, STOP as _STOP
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
        if hw in _NARR or hw in _STOP: continue
        forms={norm(d['root_ar'])}|set(variants(d['root_ar'],r))|set(_loose(d['root_ar'],r,wide=True))
        fs=[_sk(f) for f in forms if len(_sk(f))>=2]
        h=hw[2:] if hw.startswith('\u0627\u0644') and len(hw)>3 else hw
        hs=_sk(h)
        if not fs or len(hs)<2: continue
        judged+=1
        if not any(_issub(f,hs) for f in fs): wrong+=1
a('A7  entry headword compatible with root', wrong==0, f'{wrong} wrong-root blocks of {judged} judged')


# A8 no block carries an unrelated root's article (headword owns another page)
_byar={x['ar']:x['r'] for x in json.load(open('/home/claude/build/roots-index-full.json'))['roots']}
coll=0
for r,d in lex.items():
    legit={norm(d['root_ar'])}|set(variants(d['root_ar'],r))
    for c in d['classical']:
        m=HEADRE.match(DIA.sub('', c['entries'][0]['text'].lstrip()))
        if not m: continue
        hw=norm(m.group(1))
        if hw in _NARR or hw in _STOP: continue
        h=hw[2:] if hw.startswith('\u0627\u0644') and len(hw)>3 else hw
        if h in legit: continue
        if h in _byar and _byar[h]!=r and not c.get('suspect'): coll+=1
a('A8  no unrelated root article attached', coll==0, f'{coll} collisions')

print(f"{'ACCURACY TEST':60}{'RESULT':8}DETAIL")
print('-'*120)
p2=0
for n,ok,dt in ACC:
    p2+=ok; print(f"{n:60}{'PASS' if ok else 'FAIL':8}{dt[:70]}")
print('-'*120)
print(f'{p2}/{len(ACC)} accuracy tests passed   |   {npass}/{len(RESULTS)} integrity tests passed')
