import json,glob,os,sys,re,hashlib,collections
R=os.path.abspath(sys.argv[1]); bad=[]; tokens={}; verses={}; byroot=collections.defaultdict(list); inter={}
for p in sorted(glob.glob(os.path.join(R,'surah','*.json'))):
 d=json.load(open(p,encoding='utf8'))
 for v in d['verses']:
  verses[v['k']]=v
  for w in v['w']:
   k=f"{v['k']}:{w['i']}"; tokens[k]=w
   if w.get('r'): byroot[w['r']].append((v,w))
for p in glob.glob(os.path.join(R,'interlinear','*.json')):
 d=json.load(open(p,encoding='utf8'))
 for v in d['verses']:
  for w in v['w']: inter[f"{v['k']}:{w['i']}"]=w
for k,w in tokens.items():
 if k not in inter or inter[k].get('en')!=w.get('ig'): bad.append((k,'interlinear-parity'))
rootfiles={os.path.splitext(os.path.basename(p))[0]:p for p in glob.glob(os.path.join(R,'root','*.json'))}
if set(rootfiles)!=set(byroot): bad.append(('roots','page-set',len(rootfiles),len(byroot)))
for rt,exp in byroot.items():
 d=json.load(open(rootfiles[rt],encoding='utf8')); expset={f"{v['k']}:{w['i']}" for v,w in exp}; got={o['k'] for o in d.get('occ',[])}
 if d.get('count')!=len(exp): bad.append((rt,'count'))
 if got!=expset: bad.append((rt,'occ-set'))
 fg=collections.Counter((w.get('lem'),w.get('pos')) for _,w in exp)
 dg=collections.Counter({(f.get('lem'),f.get('pos')):f.get('count') for f in d.get('forms',[])})
 if fg!=dg: bad.append((rt,'forms'))
 for o in d.get('occ',[]):
  if o['k'] not in tokens or o.get('ar')!=tokens[o['k']].get('ar') or o.get('v') not in verses: bad.append((rt,'occ-ref',o.get('k')))
for folder in ['lexicon','lemma']:
 for p in glob.glob(os.path.join(R,folder,'*.json')):
  d=json.load(open(p,encoding='utf8')); occ=d.get('occ')
  if not isinstance(occ,list): continue
  for o in occ:
   if o.get('k') not in tokens or o.get('ar')!=tokens.get(o.get('k'),{}).get('ar') or o.get('v') not in verses: bad.append((p,'lex-ref',o.get('k')))
for p in glob.glob(os.path.join(R,'search','*.json')):
 d=json.load(open(p,encoding='utf8'))
 for key,vals in d.items():
  if isinstance(vals,list):
   for vk in vals:
    if isinstance(vk,str) and re.fullmatch(r'\d+:\d+',vk) and vk not in verses: bad.append((p,'search-ref',vk))
for p in glob.glob(os.path.join(R,'parallels','*.json')):
 d=json.load(open(p,encoding='utf8'))
 for vk,arr in d.items():
  if vk not in verses: bad.append((p,'parallel-source',vk))
  for x in arr:
   if x.get('v') not in verses: bad.append((p,'parallel-target',x.get('v')))
gm1=json.load(open(os.path.join(R,'gold_master','GM1_ARABIC_TEXT_HASHES.json'),encoding='utf8')); va=hashlib.sha256(); ts=hashlib.sha256()
for p in sorted(glob.glob(os.path.join(R,'surah','*.json'))):
 d=json.load(open(p,encoding='utf8'))
 for v in d['verses']:
  va.update((v['k']+'\t'+v.get('ar','')+'\n').encode())
  for w in v['w']: ts.update(f"{v['k']}:{w['i']}\t{w['ar']}\n".encode())
if va.hexdigest()!=gm1['verse_arabic_sha256']: bad.append(('GM1','arabic-hash'))
if ts.hexdigest()!=gm1['token_sequence_sha256']: bad.append(('GM1','token-hash'))
print(f"GM10 validation: verses={len(verses)} tokens={len(tokens)} roots={len(byroot)} root_pages={len(rootfiles)} failures={len(bad)}")
for x in bad[:50]: print(x)
sys.exit(1 if bad else 0)
