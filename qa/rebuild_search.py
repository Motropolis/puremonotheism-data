#!/usr/bin/env python3
import json,glob,os,sys,re,unicodedata,collections
R=os.path.abspath(sys.argv[1] if len(sys.argv)>1 and not sys.argv[1].startswith('--') else '.'); CHECK='--check' in sys.argv
ARLET=re.compile(r'[\u0621-\u063a\u0641-\u064a]'); ENWORD=re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?")
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
def surface_terms(s):
 n=anorm(s); out={n} if n else set(); cur=n
 for _ in range(2):
  if len(cur)>3 and cur[0] in 'وفبكلس': cur=cur[1:]; out.add(cur)
  else: break
 if len(cur)>4 and cur.startswith('ال'): out.add(cur[2:])
 return {x for x in out if x}
ar=collections.defaultdict(set)
for p in sorted(glob.glob(os.path.join(R,'surah','*.json'))):
 d=load(p)
 for v in d['verses']:
  for w in v['w']:
   terms=set(surface_terms(w.get('ar')))
   for val in [w.get('lem'),w.get('ra')]:
    n=anorm(val)
    if n: terms.add(n)
   for t in terms: ar[t].add(v['k'])
en=collections.defaultdict(lambda:collections.defaultdict(set))
for ap in sorted(glob.glob(os.path.join(R,'translation','*','all.json'))):
 d=load(ap); slug=d['slug']
 for vk,segs in d['verses'].items():
  text=' '.join(x.get('t','') for x in segs)
  for word in set(m.group(0).lower() for m in ENWORD.finditer(text)): en[word][slug].add(vk)
outputs={}
for k,vals in ar.items(): outputs.setdefault(f'ar-{ord(k[0]):04x}.json',{})[k]=sorted(vals)
for k,bytr in en.items(): outputs.setdefault(f'en-{k[0]}.json',{})[k]={slug:sorted(vs) for slug,vs in sorted(bytr.items())}
outputs={fn:{k:v for k,v in sorted(d.items())} for fn,d in outputs.items()}; changed=0
existing={os.path.basename(p) for p in glob.glob(os.path.join(R,'search','*.json'))}
for fn,out in outputs.items():
 p=os.path.join(R,'search',fn); cur=load(p) if os.path.exists(p) else None
 if cur!=out:
  changed+=1
  if not CHECK: open(p,'w',encoding='utf8').write(dump(out))
for fn in existing-set(outputs):
 changed+=1
 if not CHECK: os.unlink(os.path.join(R,'search',fn))
print(f"search rebuild {'check' if CHECK else 'write'}: arabic_terms={len(ar)} english_terms={len(en)} files={len(outputs)} changed={changed}")
sys.exit(1 if CHECK and changed else 0)
