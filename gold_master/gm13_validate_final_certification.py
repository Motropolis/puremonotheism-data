import json,glob,os,sys,hashlib,subprocess
R=os.path.abspath(sys.argv[1]); bad=[]; verses={}; tokens={}; roots={}
for p in glob.glob(os.path.join(R,'surah','*.json')):
 d=json.load(open(p,encoding='utf8'))
 for v in d['verses']:
  verses[v['k']]=v
  for w in v['w']:
   k=f"{v['k']}:{w['i']}"; tokens[k]=w
   if w.get('r'): roots[w['r']]=roots.get(w['r'],0)+1
# deterministic primary layers
r=subprocess.run([sys.executable,os.path.join(R,'qa','rebuild_generated.py'),R,'--check'],capture_output=True,text=True)
if r.returncode: bad.append(('generated-drift',(r.stdout+r.stderr)[-1000:]))
# parallels
for p in glob.glob(os.path.join(R,'parallels','*.json')):
 d=json.load(open(p,encoding='utf8'))
 for src,arr in d.items():
  if src not in verses: bad.append((p,'parallel-source',src))
  for x in arr:
   if x.get('v') not in verses: bad.append((p,'parallel-target',x.get('v')))
# dictsearch roots must resolve to lexicon_full
rootkeys={os.path.splitext(os.path.basename(p))[0] for p in glob.glob(os.path.join(R,'lexicon_full','*.json'))}
for p in glob.glob(os.path.join(R,'dictsearch','*.json')):
 d=json.load(open(p,encoding='utf8'))
 if isinstance(d,dict):
  for term,arr in d.items():
   if isinstance(arr,list):
    for rt in arr:
     if rt not in rootkeys: bad.append((p,term,'dictsearch-dangling',rt))
# Quranic lexicon frequency
for p in glob.glob(os.path.join(R,'lexicon','*.json')):
 d=json.load(open(p,encoding='utf8')); rt=d.get('root')
 if rt in roots and d.get('quran_frequency')!=roots[rt]: bad.append((rt,'lexicon-frequency',d.get('quran_frequency'),roots[rt]))
# lemma occurrence refs (counts may be grammatical subsets; do not infer identity from lemma_ar)
for p in glob.glob(os.path.join(R,'lemma','*.json')):
 d=json.load(open(p,encoding='utf8'))
 for o in d.get('occ',[]):
  k=o.get('k')
  if k not in tokens or o.get('ar')!=tokens.get(k,{}).get('ar'): bad.append((p,'lemma-occ',k))
# GM1 hashes
gm1=json.load(open(os.path.join(R,'gold_master','GM1_ARABIC_TEXT_HASHES.json'),encoding='utf8'))
va=hashlib.sha256(); ts=hashlib.sha256()
for p in sorted(glob.glob(os.path.join(R,'surah','*.json'))):
 d=json.load(open(p,encoding='utf8'))
 for v in d['verses']:
  va.update((v['k']+'\t'+v.get('ar','')+'\n').encode())
  for w in v['w']: ts.update(f"{v['k']}:{w['i']}\t{w['ar']}\n".encode())
if va.hexdigest()!=gm1['verse_arabic_sha256']: bad.append(('GM1','arabic-hash'))
if ts.hexdigest()!=gm1['token_sequence_sha256']: bad.append(('GM1','token-hash'))
print(f"GM13 FINAL validation: verses={len(verses)} tokens={len(tokens)} quran_roots={len(roots)} lexicon_full_roots={len(rootkeys)} failures={len(bad)}")
for x in bad[:50]: print(x)
sys.exit(1 if bad else 0)
