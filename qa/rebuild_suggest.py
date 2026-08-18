#!/usr/bin/env python3
import json,glob,os,sys,re,unicodedata,collections
R=os.path.abspath(sys.argv[1] if len(sys.argv)>1 and not sys.argv[1].startswith('--') else '.'); CHECK='--check' in sys.argv
EN=re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?"); ARLET=re.compile(r'[\u0621-\u063a\u0641-\u064a]')
def load(p): return json.load(open(p,encoding='utf8'))
def dump(d): return json.dumps(d,ensure_ascii=False,separators=(',',':'))
def anorm(s):
 s=unicodedata.normalize('NFKD',s or ''); out=[]
 for c in s:
  if unicodedata.category(c) in ('Mn','Me','Cf') or c=='ـ': continue
  if c in 'أإآٱ': c='ا'
  elif c=='ى': c='ي'
  elif c=='ة': c='ه'
  elif c=='ؤ': c='و'
  elif c=='ئ': c='ي'
  elif c=='ء': continue
  if ARLET.fullmatch(c): out.append(c)
 return ''.join(out)
def posname(p): return {'N':'noun','V':'verb','P':'particle','NEG':'particle'}.get(p,(p or '').lower())
groups=collections.defaultdict(list); rootcounts=collections.Counter()
for p in sorted(glob.glob(os.path.join(R,'surah','*.json'))):
 d=load(p)
 for v in d['verses']:
  for w in v['w']:
   if w.get('r'): rootcounts[w['r']]+=1
   if w.get('lem'): groups[(w.get('r') or '',w['lem'])].append(w)
items=[]
for rt,n in rootcounts.items():
 p=os.path.join(R,'root',rt+'.json')
 if not os.path.exists(p): continue
 d=load(p); en=(d.get('meaning') or '').strip(); items.append({'t':'r','ar':d.get('root_ar',''),'k':anorm(d.get('root_ar','')),'en':en[:160],'pos':'root','n':n,'r':rt})
for (rt,lem),ws in groups.items():
 gloss=collections.Counter((w.get('sg') or w.get('ig') or '').strip() for w in ws if (w.get('sg') or w.get('ig'))); en=gloss.most_common(1)[0][0] if gloss else ''
 pos=collections.Counter(w.get('pos') for w in ws).most_common(1)[0][0]; items.append({'t':'w','ar':lem,'k':anorm(lem),'en':en[:160],'pos':posname(pos),'n':len(ws),'r':rt})
uniq={(x['t'],x['r'],x['ar']):x for x in items}; items=list(uniq.values()); items.sort(key=lambda x:(-x['n'],x['t'],x['k'],x['r']))
outputs=collections.defaultdict(list)
for x in items:
 if x['k']: outputs[f"ar-{ord(x['k'][0]):04x}.json"].append(x)
 for m in sorted(set(z.group(0).lower() for z in EN.finditer(x['en']))):
  y=dict(x); y['m']=m; outputs[f'en-{m[0]}.json'].append(y)
for fn in outputs: outputs[fn].sort(key=lambda x:(-x['n'],x.get('m',''),x['t'],x['k'],x['r']))
changed=0; existing={os.path.basename(p) for p in glob.glob(os.path.join(R,'suggest','*.json'))}
for fn,out in outputs.items():
 p=os.path.join(R,'suggest',fn); cur=load(p) if os.path.exists(p) else None
 if cur!=out:
  changed+=1
  if not CHECK: open(p,'w',encoding='utf8').write(dump(out))
for fn in existing-set(outputs):
 changed+=1
 if not CHECK: os.unlink(os.path.join(R,'suggest',fn))
print(f"suggest rebuild {'check' if CHECK else 'write'}: items={len(items)} files={len(outputs)} changed={changed}")
sys.exit(1 if CHECK and changed else 0)
