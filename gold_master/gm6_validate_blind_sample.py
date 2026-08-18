import json,glob,os,sys,re,hashlib
R=os.path.abspath(sys.argv[1])
rec=json.load(open(os.path.join(R,'gold_master','GM6_BLIND_SAMPLE_IDS.json'),encoding='utf8'))
ids=set(rec['ids']); words={}; inter={}; bad=[]
for p in glob.glob(os.path.join(R,'surah','*.json')):
 d=json.load(open(p,encoding='utf8'))
 for v in d['verses']:
  for w in v['w']: words[f"{v['k']}:{w['i']}"]=w
for p in glob.glob(os.path.join(R,'interlinear','*.json')):
 d=json.load(open(p,encoding='utf8'))
 for v in d['verses']:
  for w in v['w']: inter[f"{v['k']}:{w['i']}"]=w
if len(ids)!=1000: bad.append(('sample-size',len(ids)))
pat=re.compile(r'(species of|certain plant|subterranean|what is cut|red ants|thong with|hard land|smitten with|i\. q|he was, became|human dung|udder|vulva|trees of the kind)',re.I)
for k in ids:
 w=words[k]
 if w.get('r') and not w.get('lem'): bad.append((k,'root-without-lemma'))
 if pat.search(w.get('ig','')): bad.append((k,'fragment',w.get('ig')))
 if inter.get(k,{}).get('en')!=w.get('ig'): bad.append((k,'gloss-parity'))
# Entire nursing root must no longer contain obvious corrupted glosses.
for k,w in words.items():
 if w.get('r')=='r-d6-3' and (w.get('ig') in {'She','The','kind of trees upon whi','noun'}):
  bad.append((k,'r-d6-3-stale-gloss',w.get('ig')))
gm1=json.load(open(os.path.join(R,'gold_master','GM1_ARABIC_TEXT_HASHES.json'),encoding='utf8'))
va=hashlib.sha256(); ts=hashlib.sha256()
for p in sorted(glob.glob(os.path.join(R,'surah','*.json'))):
 d=json.load(open(p,encoding='utf8'))
 for v in d['verses']:
  va.update((v['k']+'\t'+v.get('ar','')+'\n').encode())
  for w in v['w']: ts.update(f"{v['k']}:{w['i']}\t{w['ar']}\n".encode())
if va.hexdigest()!=gm1['verse_arabic_sha256']: bad.append(('GM1','arabic-hash'))
if ts.hexdigest()!=gm1['token_sequence_sha256']: bad.append(('GM1','token-hash'))
print(f"GM6 validation: sample={len(ids)} population={len(words)} failures={len(bad)}")
for x in bad[:30]: print(x)
sys.exit(1 if bad else 0)
