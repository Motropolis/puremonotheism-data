import json,glob,os,sys,hashlib
R=os.path.abspath(sys.argv[1]); bad=[]; changed=0
checks={('d-y-n','دَيْن'):'debt',('k-f-r','كَفّارَة'):'expiation',('k-f-r','كافُور'):'camphor',
('a-m-n','أَمِين'):'trustworthy',('a-m-n','أَمْن'):'security',('a-m-n','أَمانَة'):'trust',
('s-l-m','سُلَّم'):'ladder',('3-b-d','عَبَدَ'):'worshipped',('r-q-b','رَقِيب'):'watcher',
('q-t-l','اقْتَتَلَ'):'fought one another'}
va=hashlib.sha256(); ts=hashlib.sha256()
for p in sorted(glob.glob(os.path.join(R,'surah','*.json'))):
 d=json.load(open(p,encoding='utf8'))
 for v in d['verses']:
  va.update((v['k']+'\t'+v.get('ar','')+'\n').encode())
  for w in v['w']:
   ts.update(f"{v['k']}:{w['i']}\t{w['ar']}\n".encode())
   if w.get('gm4_status'): changed+=1
   k=(w.get('r'),w.get('lem'))
   if k in checks and w.get('ig')!=checks[k]: bad.append((v['k'],w['i'],w.get('lem'),w.get('ig'),checks[k]))
gm1=json.load(open(os.path.join(R,'gold_master','GM1_ARABIC_TEXT_HASHES.json'),encoding='utf8'))
if va.hexdigest()!=gm1['verse_arabic_sha256']: bad.append(('GM1 Arabic hash changed',))
if ts.hexdigest()!=gm1['token_sequence_sha256']: bad.append(('GM1 token hash changed',))
print(f"GM4 validation: curated_tokens={changed} failures={len(bad)}")
for x in bad[:30]: print(x)
sys.exit(bool(bad))
