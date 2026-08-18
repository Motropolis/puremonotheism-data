import json,glob,os,sys,re,collections
ROOT=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else os.path.dirname(__file__))
sur={}; inter={}; bad=[]
for p in glob.glob(os.path.join(ROOT,'surah','*.json')):
 d=json.load(open(p,encoding='utf-8'))
 for v in d['verses']:
  for w in v['w']: sur[f"{v['k']}:{w['i']}"]=w
for p in glob.glob(os.path.join(ROOT,'interlinear','*.json')):
 d=json.load(open(p,encoding='utf-8'))
 for v in d['verses']:
  for w in v['w']: inter[f"{v['k']}:{w['i']}"]=w
if set(sur)!=set(inter): bad.append(('token-key-set',len(set(sur)-set(inter)),len(set(inter)-set(sur))))
# strict safe parity fields; compound segmentation links are intentionally layer-specific.
for k in set(sur)&set(inter):
 for a,b in [('ar','ar'),('ig','en'),('r','r'),('lm','lm'),('mq','mq')]:
  if sur[k].get(a)!=inter[k].get(b): bad.append((k,a,b,sur[k].get(a),inter[k].get(b)))
# target file existence
roots={os.path.splitext(os.path.basename(p))[0] for p in glob.glob(os.path.join(ROOT,'root','*.json'))}
lex={os.path.splitext(os.path.basename(p))[0] for p in glob.glob(os.path.join(ROOT,'lexicon','*.json'))}
lems={os.path.splitext(os.path.basename(p))[0] for p in glob.glob(os.path.join(ROOT,'lemma','*.json'))}
prs={os.path.splitext(os.path.basename(p))[0] for p in glob.glob(os.path.join(ROOT,'pronoun','*.json'))}
mqs={os.path.splitext(os.path.basename(p))[0] for p in glob.glob(os.path.join(ROOT,'muqattaat','*.json'))}
for k,w in inter.items():
 if w.get('r') and (w['r'] not in roots or w['r'] not in lex): bad.append((k,'broken-root-link',w['r']))
 if w.get('lm') and w['lm'] not in lems: bad.append((k,'broken-lemma-link',w['lm']))
 if w.get('pr') and w['pr'] not in prs: bad.append((k,'broken-pronoun-link',w['pr']))
 if w.get('mq') and w['mq'] not in mqs: bad.append((k,'broken-muq-link',w['mq']))
# browse Quran flags
canonical={w['r'] for w in inter.values() if w.get('r')}; bq={}
for p in glob.glob(os.path.join(ROOT,'browse','*.json')):
 d=json.load(open(p,encoding='utf-8'))
 for x in d.get('roots',[]): bq[x.get('r')]=x.get('q')
for rt in canonical:
 if bq.get(rt) is not True: bad.append((rt,'browse-q-flag',bq.get(rt)))
if bq.get('l-w-t') is not False: bad.append(('l-w-t','stale-browse-q',bq.get('l-w-t')))
print(f"surah_words={len(sur)} interlinear_words={len(inter)} canonical_roots={len(canonical)} failures={len(bad)}")
for x in bad[:30]: print(x)
sys.exit(1 if bad else 0)
