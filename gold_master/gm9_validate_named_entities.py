import json,glob,os,sys,re,hashlib,collections
R=os.path.abspath(sys.argv[1]); bad=[]; tokenmap={}; versemap={}; proper=[]
for p in sorted(glob.glob(os.path.join(R,'surah','*.json'))):
 d=json.load(open(p,encoding='utf8'))
 for v in d['verses']:
  inds=[w['i'] for w in v['w']]
  if inds!=list(range(1,len(inds)+1)): bad.append((v['k'],'token-index-sequence'))
  versemap[v['k']]=v.get('ar')
  for w in v['w']:
   k=f"{v['k']}:{w['i']}"; tokenmap[k]=w
   if 'proper noun' in (w.get('g') or '').lower(): proper.append((k,w))
generic={'قُرْءان','جَنَّة','نَصْرانِيّ','مُسْلِم','صالِح','مَدِينَة','جاهِلِيَّة','سِلْم','بَعْل','مالِك'}
for k,w in proper:
 if w.get('lem') in generic: bad.append((k,'false-proper',w.get('lem')))
 if not w.get('lem') or not (w.get('ig') or '').strip(): bad.append((k,'missing-identity'))
 if not w.get('r') and not (w.get('lk') or w.get('lm')): bad.append((k,'missing-lookup-key'))
 if w.get('lk') and w.get('lm') and w['lk']!=w['lm']: bad.append((k,'lookup-key-mismatch'))
nr=collections.defaultdict(list)
for k,w in proper:
 if not w.get('r'): nr[w.get('lem')].append((k,w))
for lem,recs in nr.items():
 key=recs[0][1].get('lk') or recs[0][1].get('lm'); p=os.path.join(R,'lexicon',key+'.json')
 if not os.path.exists(p): bad.append((lem,'missing-lexicon-page',key)); continue
 d=json.load(open(p,encoding='utf8')); exp={x[0] for x in recs}; got={o['k'] for o in d.get('occ',[])}
 if d.get('lemma_ar')!=lem: bad.append((lem,'lemma-ar-mismatch'))
 if d.get('count')!=len(recs): bad.append((lem,'count-mismatch'))
 if exp!=got: bad.append((lem,'occurrence-set-mismatch'))
 for o in d.get('occ',[]):
  if o['k'] not in tokenmap or o.get('ar')!=tokenmap[o['k']].get('ar'): bad.append((lem,o['k'],'occ-reference'))
 for vk,ar in d.get('verses',{}).items():
  if versemap.get(vk)!=ar: bad.append((lem,vk,'verse-reference'))
# gloss consistency by lemma
for lem in set(w.get('lem') for _,w in proper):
 vals={w.get('ig') for _,w in proper if w.get('lem')==lem}
 if len(vals)>1: bad.append((lem,'proper-gloss-inconsistent',sorted(map(str,vals))))
# interlinear parity
inter={}
for p in glob.glob(os.path.join(R,'interlinear','*.json')):
 d=json.load(open(p,encoding='utf8'))
 for v in d['verses']:
  for w in v['w']: inter[f"{v['k']}:{w['i']}"]=w
for k,w in tokenmap.items():
 if inter.get(k,{}).get('en')!=w.get('ig'): bad.append((k,'gloss-parity'))
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
print(f"GM9 validation: tokens={len(tokenmap)} retained_proper_tokens={len(proper)} proper_lemmas={len(set(w.get('lem') for _,w in proper))} no_root_name_lemmas={len(nr)} failures={len(bad)}")
for x in bad[:50]: print(x)
sys.exit(1 if bad else 0)
