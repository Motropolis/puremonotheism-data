#!/usr/bin/env python3
import json,glob,os,sys,collections
R=os.path.abspath(sys.argv[1] if len(sys.argv)>1 and not sys.argv[1].startswith('--') else '.'); CHECK='--check' in sys.argv
def load(p): return json.load(open(p,encoding='utf8'))
def dump(d): return json.dumps(d,ensure_ascii=False,separators=(',',':'))
q=collections.Counter()
for p in sorted(glob.glob(os.path.join(R,'surah','*.json'))):
 d=load(p)
 for v in d['verses']:
  for w in v['w']:
   if w.get('r'): q[w['r']]+=1
idxp=os.path.join(R,'roots-index-full.json'); idx=load(idxp); roots=idx['roots']; idx_changed=False
for x in roots:
 should=x['r'] in q
 if bool(x.get('q'))!=should: x['q']=should; idx_changed=True
 if should:
  if x.get('n')!=q[x['r']]: x['n']=q[x['r']]; idx_changed=True
 elif 'n' in x: x.pop('n'); idx_changed=True
alpha=collections.OrderedDict()
for x in roots:
 ar=x.get('ar','')
 if ar: alpha.setdefault(ar[0],[]).append(x)
outputs={}; manifest={'letters':[],'dicts':{}}
for L,arr in alpha.items():
 fn=f'alpha-{ord(L):04x}.json'; outputs[fn]={'letter':L,'count':len(arr),'roots':arr}; manifest['letters'].append({'letter':L,'file':fn,'count':len(arr)})
for did in ['ayn','tahdhib','sihah','maqayis','mufradat','lisan','qamus','lane']:
 arr=[x for x in roots if did in (x.get('d') or [])]; outputs[f'dict-{did}.json']={'dict':did,'count':len(arr),'roots':arr}; manifest['dicts'][did]=len(arr)
outputs['browse-manifest.json']=manifest; changed=0
if idx_changed:
 changed+=1
 if not CHECK: open(idxp,'w',encoding='utf8').write(dump(idx))
for fn,out in outputs.items():
 p=os.path.join(R,'browse',fn); cur=load(p) if os.path.exists(p) else None
 if cur!=out:
  changed+=1
  if not CHECK: open(p,'w',encoding='utf8').write(dump(out))
print(f"browse rebuild {'check' if CHECK else 'write'}: roots={len(roots)} quran_roots={len(q)} outputs={len(outputs)} changed={changed}")
sys.exit(1 if CHECK and changed else 0)
