import json,glob,os,sys,re,hashlib
R=os.path.abspath(sys.argv[1]); rec=json.load(open(os.path.join(R,'gold_master','GM7_STRATIFIED_SAMPLE_IDS.json'),encoding='utf8'))
ids=set(rec['ids']); words={}; inter={}; bad=[]
for p in glob.glob(os.path.join(R,'surah','*.json')):
 d=json.load(open(p,encoding='utf8'))
 for v in d['verses']:
  for w in v['w']: words[f"{v['k']}:{w['i']}"]=w
for p in glob.glob(os.path.join(R,'interlinear','*.json')):
 d=json.load(open(p,encoding='utf8'))
 for v in d['verses']:
  for w in v['w']: inter[f"{v['k']}:{w['i']}"]=w
pat=re.compile(r'(species of|certain plant|subterranean|what is cut|red ants|thong|hard land|smitten with|i\. q|he was, became|human dung|udder|vulva|trees upon|called,|west wind|having milk|^the$|^she$|^noun$|^verb$)',re.I)
for k in ids:
 w=words[k]
 if w.get('r') and not w.get('lem'): bad.append((k,'root-without-lemma'))
 if pat.search(w.get('ig','')): bad.append((k,'raw-or-truncated-gloss',w.get('ig')))
 if inter.get(k,{}).get('en')!=w.get('ig'): bad.append((k,'gloss-parity'))
gm1=json.load(open(os.path.join(R,'gold_master','GM1_ARABIC_TEXT_HASHES.json'),encoding='utf8'))
va=hashlib.sha256(); ts=hashlib.sha256()
for p in sorted(glob.glob(os.path.join(R,'surah','*.json'))):
 d=json.load(open(p,encoding='utf8'))
 for v in d['verses']:
  va.update((v['k']+'\t'+v.get('ar','')+'\n').encode())
  for w in v['w']: ts.update(f"{v['k']}:{w['i']}\t{w['ar']}\n".encode())
if va.hexdigest()!=gm1['verse_arabic_sha256']: bad.append(('GM1','arabic-hash'))
if ts.hexdigest()!=gm1['token_sequence_sha256']: bad.append(('GM1','token-hash'))
print(f"GM7 validation: stratified_unique_sample={len(ids)} corpus={len(words)} failures={len(bad)}")
for x in bad[:40]: print(x)
sys.exit(1 if bad else 0)
