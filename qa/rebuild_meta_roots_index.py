#!/usr/bin/env python3
import json,glob,os,sys
R=os.path.abspath(sys.argv[1] if len(sys.argv)>1 and not sys.argv[1].startswith('--') else '.')
CHECK='--check' in sys.argv
def load(p): return json.load(open(p,encoding='utf8'))
def dump(d): return json.dumps(d,ensure_ascii=False,separators=(',',':'))
p=os.path.join(R,'meta','roots-index.json')
cur=load(p)
old_order={x['r']:i for i,x in enumerate(cur.get('roots',[]))}
roots=[]
for rp in sorted(glob.glob(os.path.join(R,'root','*.json'))):
 d=load(rp); rt=os.path.splitext(os.path.basename(rp))[0]
 roots.append({'r':rt,'ar':d.get('root_ar',''),'n':d.get('count',0)})
roots.sort(key=lambda x:(old_order.get(x['r'],10**9),x['r']))
out={'version':cur.get('version','1.2.0'),'count':len(roots),'roots':roots}
changed=(cur!=out)
if changed and not CHECK:
 with open(p,'w',encoding='utf8') as f:f.write(dump(out))
print(f"meta root index {'check' if CHECK else 'write'}: active_roots={len(roots)} changed={int(changed)}")
sys.exit(1 if CHECK and changed else 0)
