import json,os,sys,hashlib
ROOT=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else os.path.join(os.path.dirname(__file__),'..'))
bad=[]; verse_ar=hashlib.sha256(); token_seq=hashlib.sha256(); words=0; verses=0
for s in range(1,115):
 p=os.path.join(ROOT,'surah',f'{s:03d}.json')
 d=json.load(open(p,encoding='utf-8'))
 for v in d['verses']:
  verses+=1
  verse_ar.update((v['k']+'\t'+v.get('ar','')+'\n').encode())
  for exp,w in enumerate(v['w'],1):
   words+=1
   if w.get('i')!=exp: bad.append((v['k'],'word-order',w.get('i'),exp))
   token_seq.update(f"{v['k']}:{w['i']}\t{w['ar']}\n".encode())
record=json.load(open(os.path.join(ROOT,'gold_master','GM1_ARABIC_TEXT_HASHES.json'),encoding='utf-8'))
if record['verse_arabic_sha256']!=verse_ar.hexdigest(): bad.append(('verse-arabic-hash','changed'))
if record['token_sequence_sha256']!=token_seq.hexdigest(): bad.append(('token-sequence-hash','changed'))
if words!=77430: bad.append(('word-count',words,77430))
if verses!=6236: bad.append(('verse-count',verses,6236))
print(f"GM1 validation: verses={verses} words={words} failures={len(bad)}")
for x in bad: print(x)
sys.exit(1 if bad else 0)
