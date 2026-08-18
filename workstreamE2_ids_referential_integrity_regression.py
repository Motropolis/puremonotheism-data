import json,glob,os,sys,re,collections
ROOT=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else os.path.dirname(__file__))
bad=[]; sur={}; inter={}; verses=[]
for s in range(1,115):
 p=os.path.join(ROOT,'surah',f'{s:03d}.json')
 d=json.load(open(p,encoding='utf-8'))
 for v in d['verses']:
  verses.append(v['k'])
  if int(v['k'].split(':')[0])!=s: bad.append(('wrong-surah',v['k'],s))
  for exp,w in enumerate(v['w'],1):
   if w.get('i')!=exp: bad.append(('surah-word-order',v['k'],w.get('i'),exp))
   k=f"{v['k']}:{w.get('i')}"
   if k in sur: bad.append(('duplicate-surah-token',k))
   sur[k]=w
for s in range(1,115):
 p=os.path.join(ROOT,'interlinear',f'{s:03d}.json')
 d=json.load(open(p,encoding='utf-8'))
 for v in d['verses']:
  for exp,w in enumerate(v['w'],1):
   if w.get('i')!=exp: bad.append(('interlinear-word-order',v['k'],w.get('i'),exp))
   k=f"{v['k']}:{w.get('i')}"
   if k in inter: bad.append(('duplicate-interlinear-token',k))
   inter[k]=w
if len(verses)!=len(set(verses)): bad.append(('duplicate-verse-keys',len(verses),len(set(verses))))
if set(sur)!=set(inter): bad.append(('token-key-parity',len(set(sur)^set(inter))))
actual=collections.Counter(w['r'] for w in sur.values() if w.get('r'))
for p in glob.glob(os.path.join(ROOT,'root','*.json')):
 d=json.load(open(p,encoding='utf-8')); rt=d.get('root')
 if rt in actual and d.get('count')!=actual[rt]: bad.append((rt,'root-count',d.get('count'),actual[rt]))
targets={f:{os.path.splitext(os.path.basename(p))[0] for p in glob.glob(os.path.join(ROOT,f,'*.json'))} for f in ['root','lemma','pronoun','muqattaat']}
for k,w in inter.items():
 for fld,folder in [('r','root'),('lm','lemma'),('pr','pronoun'),('mq','muqattaat')]:
  if w.get(fld) and w[fld] not in targets[folder]: bad.append((k,'broken-'+fld,w[fld]))
print(f"verses={len(verses)} unique_verses={len(set(verses))} words={len(sur)} interlinear_words={len(inter)} failures={len(bad)}")
for x in bad[:30]: print(x)
sys.exit(1 if bad else 0)
