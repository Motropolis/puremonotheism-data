import json,glob,os,sys,collections,re
ROOT=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else os.path.dirname(__file__))
actual=collections.Counter(); verses=set(); bad=[]
for p in glob.glob(os.path.join(ROOT,'surah','*.json')):
 d=json.load(open(p,encoding='utf-8'))
 for v in d['verses']:
  verses.add(v['k'])
  for w in v['w']:
   if w.get('r'): actual[w['r']]+=1
for p in glob.glob(os.path.join(ROOT,'browse','*.json')):
 d=json.load(open(p,encoding='utf-8'))
 for x in d.get('roots',[]):
  rt=x.get('r'); should=rt in actual
  if bool(x.get('q'))!=should: bad.append((p,'browse-q',rt,x.get('q'),should))
  if should and x.get('n')!=actual[rt]: bad.append((p,'browse-n',rt,x.get('n'),actual[rt]))
for p in glob.glob(os.path.join(ROOT,'suggest','*.json')):
 d=json.load(open(p,encoding='utf-8'))
 for x in d:
  if x.get('t')=='r' and x.get('r') in actual and x.get('n')!=actual[x['r']]:
   bad.append((p,'suggest-n',x['r'],x.get('n'),actual[x['r']]))
refs=0
def walk(x,p):
 global refs
 if isinstance(x,dict):
  for z in x.values(): walk(z,p)
 elif isinstance(x,list):
  if not x: bad.append((p,'empty-search-list'))
  for z in x: walk(z,p)
 elif isinstance(x,str) and re.fullmatch(r'\d+:\d+',x):
  refs+=1
  if x not in verses: bad.append((p,'invalid-search-ref',x))
for p in glob.glob(os.path.join(ROOT,'search','*.json')): walk(json.load(open(p,encoding='utf-8')),p)
print(f"canonical_roots={len(actual)} search_refs={refs} failures={len(bad)}")
for x in bad[:30]: print(x)
sys.exit(1 if bad else 0)
