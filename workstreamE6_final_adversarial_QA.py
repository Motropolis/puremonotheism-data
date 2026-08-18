import json,glob,os,sys,unicodedata,collections
ROOT=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else os.path.dirname(__file__))
bad=[]; sur={}; inter={}
for folder,target in [('surah',sur),('interlinear',inter)]:
 for p in glob.glob(os.path.join(ROOT,folder,'*.json')):
  d=json.load(open(p,encoding='utf-8'))
  for v in d['verses']:
   for w in v['w']:
    k=f"{v['k']}:{w['i']}"
    if k in target: bad.append((folder,'duplicate-token',k))
    target[k]=w
    if not isinstance(w.get('ar'),str) or not w['ar'].strip(): bad.append((folder,'empty-ar',k))
    if '\ufffd' in w.get('ar',''): bad.append((folder,'replacement-char',k))
    g=w.get('ig') if folder=='surah' else w.get('en')
    if isinstance(g,str) and g.count('"')%2: bad.append((folder,'unmatched-gloss-quote',k))
if set(sur)!=set(inter): bad.append(('cross-layer-token-parity',len(set(sur)^set(inter))))
for p in glob.glob(os.path.join(ROOT,'lexicon','*.json')):
 d=json.load(open(p,encoding='utf-8'))
 if 'summary' in d and isinstance(d['summary'],str) and not d['summary'].strip(): bad.append((p,'empty-summary'))
for p in glob.glob(os.path.join(ROOT,'search','*.json')):
 d=json.load(open(p,encoding='utf-8'))
 for k in d:
  if any(unicodedata.category(c)=='Cf' for c in k): bad.append((p,'format-control-key',repr(k)))
zero={os.path.splitext(os.path.basename(p))[0] for p in glob.glob(os.path.join(ROOT,'root','*.json')) if json.load(open(p,encoding='utf-8')).get('count')==0}
for p in glob.glob(os.path.join(ROOT,'suggest','*.json')):
 for x in json.load(open(p,encoding='utf-8')):
  if x.get('t')=='r' and x.get('r') in zero: bad.append((p,'zero-count-root-suggestion',x['r']))
print(f"surah_words={len(sur)} interlinear_words={len(inter)} zero_count_roots={len(zero)} failures={len(bad)}")
for x in bad[:30]: print(x)
sys.exit(1 if bad else 0)
