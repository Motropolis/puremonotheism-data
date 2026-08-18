import json,os,sys
ROOT=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else os.path.dirname(__file__))
roots=['3-z6-m', 'a-dh-n', 'a-w-l', 'b-sh-r', 'd-y-n', 'j-n-n', 'n-3-m', 'n-f-q', 'n-h-r', 'n-w-r']
bad=[]
for rt in roots:
 for folder in ['root','lexicon']:
  p=os.path.join(ROOT,folder,rt+'.json')
  if not os.path.exists(p): bad.append((rt,folder,'missing')); continue
  d=json.load(open(p,encoding='utf-8'))
  senses=d.get('quran_senses',[])
  if len(senses)<2: bad.append((rt,folder,'insufficient-senses'))
  if d.get('quran_senses_status')!='curated-D3': bad.append((rt,folder,'status'))
  for s in senses:
   if not s.get('sense') or not s.get('lemmas') or not s.get('note'):
    bad.append((rt,folder,'malformed-sense',s))
print(f"polysemy_roots={len(roots)} layers={len(roots)*2} failures={len(bad)}")
for x in bad[:20]: print(x)
sys.exit(1 if bad else 0)
