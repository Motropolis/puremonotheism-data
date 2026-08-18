import json,glob,os,sys,collections,hashlib
ROOT=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else os.path.dirname(__file__))
bad=[]
# Canonical references
refs={'root':set(),'lemma':set(),'pronoun':set(),'muqattaat':set()}
for p in glob.glob(os.path.join(ROOT,'interlinear','*.json')):
 d=json.load(open(p,encoding='utf-8'))
 for v in d['verses']:
  for w in v['w']:
   if w.get('r'): refs['root'].add(w['r'])
   if w.get('lm'): refs['lemma'].add(w['lm'])
   if w.get('pr'): refs['pronoun'].add(w['pr'])
   if w.get('mq'): refs['muqattaat'].add(w['mq'])
for folder in ['lemma','pronoun','muqattaat']:
 stems={os.path.splitext(os.path.basename(p))[0] for p in glob.glob(os.path.join(ROOT,folder,'*.json'))}
 if stems!=refs[folder]: bad.append((folder,'reference-set-mismatch',len(stems),len(refs[folder])))
# l-w-t must remain non-Quranic and absent from Quran root suggestions.
rp=os.path.join(ROOT,'root','l-w-t.json')
if os.path.exists(rp):
 d=json.load(open(rp,encoding='utf-8'))
 if d.get('count')!=0: bad.append(('l-w-t','root-count',d.get('count')))
for p in glob.glob(os.path.join(ROOT,'suggest','*.json')):
 for x in json.load(open(p,encoding='utf-8')):
  if x.get('t')=='r' and x.get('r')=='l-w-t': bad.append((p,'dead-quran-suggestion','l-w-t'))
print(f"canonical_roots={len(refs['root'])} lemma_targets={len(refs['lemma'])} failures={len(bad)}")
for x in bad[:20]: print(x)
sys.exit(1 if bad else 0)
