import json,glob,os,sys,collections,hashlib
ROOT=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else os.path.join(os.path.dirname(__file__),'..'))
bad=[]; words={}
for p in glob.glob(os.path.join(ROOT,'surah','*.json')):
 d=json.load(open(p,encoding='utf-8'))
 for v in d['verses']:
  for w in v['w']: words[f"{v['k']}:{w['i']}"]=w
expect={
'5:105:4':{'pos':'P','ig':'on'},
'9:111:25':{'pos':'N','ig':'more faithful'},
'53:41:4':{'pos':'N','ig':'the fullest'},
}
for k,e in expect.items():
 for fld,val in e.items():
  if words.get(k,{}).get(fld)!=val: bad.append((k,fld,words.get(k,{}).get(fld),val))
for k,w in words.items():
 if w.get('r') and not w.get('lem'): bad.append((k,'root-without-lemma'))
# Arabic hash immutability
gm1=json.load(open(os.path.join(ROOT,'gold_master','GM1_ARABIC_TEXT_HASHES.json'),encoding='utf-8'))
va=hashlib.sha256(); ts=hashlib.sha256()
for p in sorted(glob.glob(os.path.join(ROOT,'surah','*.json'))):
 d=json.load(open(p,encoding='utf-8'))
 for v in d['verses']:
  va.update((v['k']+'\t'+v.get('ar','')+'\n').encode())
  for w in v['w']: ts.update(f"{v['k']}:{w['i']}\t{w['ar']}\n".encode())
if va.hexdigest()!=gm1['verse_arabic_sha256']: bad.append(('GM1','verse-arabic-hash'))
if ts.hexdigest()!=gm1['token_sequence_sha256']: bad.append(('GM1','token-sequence-hash'))
print(f"GM3 validation: words={len(words)} adjudicated_corrections={len(expect)} failures={len(bad)}")
for x in bad[:30]: print(x)
sys.exit(1 if bad else 0)
