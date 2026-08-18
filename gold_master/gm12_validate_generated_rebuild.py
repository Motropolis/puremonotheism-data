import json,glob,os,sys,re,subprocess,hashlib,collections
R=os.path.abspath(sys.argv[1]); bad=[]
r=subprocess.run([sys.executable,os.path.join(R,'qa','rebuild_generated.py'),R,'--check'],capture_output=True,text=True)
if r.returncode: bad.append(('generated-rebuild-drift',(r.stdout+r.stderr)[-2000:]))
verses=set(); tokens={}; rootcounts=collections.Counter()
for p in glob.glob(os.path.join(R,'surah','*.json')):
 d=json.load(open(p,encoding='utf8'))
 for v in d['verses']:
  verses.add(v['k'])
  for w in v['w']:
   k=f"{v['k']}:{w['i']}"; tokens[k]=w
   if w.get('r'): rootcounts[w['r']]+=1
inter={}
for p in glob.glob(os.path.join(R,'interlinear','*.json')):
 d=json.load(open(p,encoding='utf8'))
 for v in d['verses']:
  for w in v['w']: inter[f"{v['k']}:{w['i']}"]=w
if set(tokens)!=set(inter): bad.append(('interlinear-token-set',len(tokens),len(inter)))
for k,w in tokens.items():
 iw=inter.get(k,{})
 for a,b in [('ar','ar'),('ig','en'),('r','r'),('pos','pos'),('g','g'),('lm','lm')]:
  if w.get(a)!=iw.get(b): bad.append((k,'interlinear-field',a,b))
idx=json.load(open(os.path.join(R,'roots-index-full.json'),encoding='utf8'))['roots']
for x in idx:
 should=x['r'] in rootcounts
 if bool(x.get('q'))!=should: bad.append((x['r'],'index-q'))
 if should and x.get('n')!=rootcounts[x['r']]: bad.append((x['r'],'index-n'))
arsearch={}
for p in glob.glob(os.path.join(R,'search','ar-*.json')): arsearch.update(json.load(open(p,encoding='utf8')))
for vals in arsearch.values():
 for vk in vals:
  if vk not in verses: bad.append(('search-dangling',vk))
for p in glob.glob(os.path.join(R,'search','en-*.json')):
 for term,bytr in json.load(open(p,encoding='utf8')).items():
  for slug,vals in bytr.items():
   for vk in vals:
    if vk not in verses: bad.append((term,slug,'english-search-dangling',vk))
for p in glob.glob(os.path.join(R,'suggest','ar-*.json')):
 for x in json.load(open(p,encoding='utf8')):
  if x.get('t')=='r' and x.get('r') in rootcounts and x.get('n')!=rootcounts[x['r']]: bad.append((x['r'],'suggest-root-count'))
gm1=json.load(open(os.path.join(R,'gold_master','GM1_ARABIC_TEXT_HASHES.json'),encoding='utf8')); va=hashlib.sha256(); ts=hashlib.sha256()
for p in sorted(glob.glob(os.path.join(R,'surah','*.json'))):
 d=json.load(open(p,encoding='utf8'))
 for v in d['verses']:
  va.update((v['k']+'\t'+v.get('ar','')+'\n').encode())
  for w in v['w']: ts.update(f"{v['k']}:{w['i']}\t{w['ar']}\n".encode())
if va.hexdigest()!=gm1['verse_arabic_sha256']: bad.append(('GM1','arabic-hash'))
if ts.hexdigest()!=gm1['token_sequence_sha256']: bad.append(('GM1','token-hash'))
print(f"GM12 validation: tokens={len(tokens)} roots={len(rootcounts)} search_ar_terms={len(arsearch)} failures={len(bad)}")
for x in bad[:50]: print(x)
sys.exit(1 if bad else 0)
