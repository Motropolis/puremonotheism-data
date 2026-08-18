#!/usr/bin/env python3
import json,os,sys,glob
R=os.path.abspath(sys.argv[1] if len(sys.argv)>1 and not sys.argv[1].startswith('--') else '.')
CHECK='--check' in sys.argv
ov=json.load(open(os.path.join(R,'gold_master','GM12_INTERLINEAR_OVERRIDES.json'),encoding='utf8'))['records']
def dump(d): return json.dumps(d,ensure_ascii=False,separators=(',',':'))
changed=0; words=0
for sp in sorted(glob.glob(os.path.join(R,'surah','*.json'))):
 sd=json.load(open(sp,encoding='utf8')); out={'id':sd['id'],'verses':[]}
 for v in sd['verses']:
  iv={'k':v['k'],'ar':v['ar'],'w':[]}
  for sw in v['w']:
   words+=1; tid=f"{v['k']}:{sw['i']}"; iw={'i':sw['i'],'ar':sw['ar'],'en':sw.get('ig','')}
   for fld in ['r','pos','g','lm','fw','pk','pr']:
    if sw.get(fld) is not None: iw[fld]=sw[fld]
   if sw.get('mq') is not None: iw['mq']=sw['mq']
   elif sw.get('mk') is not None: iw['mq']=sw['mk']
   for fld,val in ov.get(tid,{}).items():
    if fld=='s': iw['s']=val
    elif val is None: iw.pop(fld,None)
    else: iw[fld]=val
   iv['w'].append(iw)
  out['verses'].append(iv)
 ip=os.path.join(R,'interlinear',os.path.basename(sp)); cur=json.load(open(ip,encoding='utf8'))
 if cur!=out:
  changed+=1
  if not CHECK: open(ip,'w',encoding='utf8').write(dump(out))
print(f"interlinear rebuild {'check' if CHECK else 'write'}: words={words} changed_files={changed}")
sys.exit(1 if CHECK and changed else 0)
