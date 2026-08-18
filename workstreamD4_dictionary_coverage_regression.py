import json,glob,os,sys,collections
ROOT=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else os.path.dirname(__file__))
actual=collections.Counter()
for p in glob.glob(os.path.join(ROOT,'surah','*.json')):
 d=json.load(open(p,encoding='utf-8'))
 for v in d['verses']:
  for w in v['w']:
   if w.get('r'): actual[w['r']]+=1
bad=[]
for rt,c in actual.items():
 rp=os.path.join(ROOT,'root',rt+'.json'); lp=os.path.join(ROOT,'lexicon',rt+'.json')
 if not os.path.exists(rp): bad.append((rt,'missing-root-page')); continue
 if not os.path.exists(lp): bad.append((rt,'missing-lexicon-page'))
 d=json.load(open(rp,encoding='utf-8'))
 if d.get('count')!=c: bad.append((rt,'count',d.get('count'),c))
# l-w-t must not claim Quran occurrences
lp=os.path.join(ROOT,'root','l-w-t.json')
if os.path.exists(lp):
 d=json.load(open(lp,encoding='utf-8'))
 if d.get('count')!=0: bad.append(('l-w-t','orphan-count',d.get('count')))
print(f"canonical_roots={len(actual)} token_occurrences={sum(actual.values())} failures={len(bad)}")
for x in bad[:30]: print(x)
sys.exit(1 if bad else 0)
