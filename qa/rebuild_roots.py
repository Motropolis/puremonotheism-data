#!/usr/bin/env python3
import json,collections,glob,os,sys
R=os.path.abspath(sys.argv[1] if len(sys.argv)>1 and not sys.argv[1].startswith('--') else '.')
CHECK='--check' in sys.argv
def load(p): return json.load(open(p,encoding='utf8'))
def dump(d): return json.dumps(d,ensure_ascii=False,separators=(',',':'))
byroot=collections.defaultdict(list)
for p in sorted(glob.glob(os.path.join(R,'surah','*.json'))):
 d=load(p)
 for v in d['verses']:
  for w in v['w']:
   if w.get('r'): byroot[w['r']].append((v,w))
changed=0
for rt,exp in byroot.items():
 p=os.path.join(R,'root',rt+'.json'); d=load(p)
 occ=[{'k':f"{v['k']}:{w['i']}",'v':v['k'],'ar':w['ar']} for v,w in exp]
 fg=collections.OrderedDict()
 for idx,(v,w) in enumerate(exp): fg.setdefault((w.get('lem'),w.get('pos')),[]).append(idx)
 forms=[{'lem':k[0],'pos':k[1],'count':len(ix),'occ':ix} for k,ix in fg.items()]
 verses={}
 for v,w in exp: verses[v['k']]=v.get('ar')
 new={'count':len(exp),'occ':occ,'forms':forms,'verses':verses}
 if any(d.get(k)!=v for k,v in new.items()):
  changed+=1
  if not CHECK:
   d.update(new); d['gm10_status']='generated-references-rebuilt'; open(p,'w',encoding='utf8').write(dump(d))
print(f"root rebuild {'check' if CHECK else 'write'}: canonical_roots={len(byroot)} changed={changed}")
sys.exit(1 if CHECK and changed else 0)
