import json,glob,os,sys,re,hashlib
R=os.path.abspath(sys.argv[1]); bad=[]; marked=0; sur={}; inter={}
pat=re.compile(r"(species of|trees of the kind|subterranean|what is cut|red ants|thong with|hard land|smitten with|i\. q|he was, became|certain plant|human dung|udder|penis|vagina|testicle|glasswort|camels acquired|returning supply|his impress|\[gave ear|what\?)",re.I)
for p in glob.glob(os.path.join(R,'surah','*.json')):
 d=json.load(open(p,encoding='utf8'))
 for v in d['verses']:
  for w in v['w']:
   k=f"{v['k']}:{w['i']}"; sur[k]=w
   if w.get('gm5_status'): marked+=1
   if pat.search(w.get('ig','')): bad.append((k,'dictionary-fragment-gloss',w.get('ig')))
   if w.get('r') and not w.get('lem'): bad.append((k,'root-without-lemma'))
   if w.get('proper_noun_status')=='verified-B4' and 'proper noun' not in (w.get('g') or '').lower():
    bad.append((k,'misindexed-B4-proper-name-edit'))
for p in glob.glob(os.path.join(R,'interlinear','*.json')):
 d=json.load(open(p,encoding='utf8'))
 for v in d['verses']:
  for w in v['w']: inter[f"{v['k']}:{w['i']}"]=w
if set(sur)!=set(inter): bad.append(('token-key-parity',len(set(sur)^set(inter))))
for k in sur:
 if sur[k].get('ig')!=inter[k].get('en'): bad.append((k,'selected-gloss-parity'))
gm1=json.load(open(os.path.join(R,'gold_master','GM1_ARABIC_TEXT_HASHES.json'),encoding='utf8'))
va=hashlib.sha256(); ts=hashlib.sha256()
for p in sorted(glob.glob(os.path.join(R,'surah','*.json'))):
 d=json.load(open(p,encoding='utf8'))
 for v in d['verses']:
  va.update((v['k']+'\t'+v.get('ar','')+'\n').encode())
  for w in v['w']: ts.update(f"{v['k']}:{w['i']}\t{w['ar']}\n".encode())
if va.hexdigest()!=gm1['verse_arabic_sha256']: bad.append(('GM1','verse-arabic-hash-changed'))
if ts.hexdigest()!=gm1['token_sequence_sha256']: bad.append(('GM1','token-sequence-hash-changed'))
print(f"GM5 validation: words={len(sur)} gm5_marked={marked} failures={len(bad)}")
for x in bad[:40]: print(x)
sys.exit(1 if bad else 0)
