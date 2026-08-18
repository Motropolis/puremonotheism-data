import json,glob,os,sys,re,hashlib
R=os.path.abspath(sys.argv[1]); bad=[]; words={}; inter={}; roots=0; lex=0; gm8=0
hard=re.compile(r'^(noun|verb|the|she|he|it)$',re.I)
debris=re.compile(r'(thong with|subterranean structure|what is cut|red ants|certain plant|trees of the kind|human dung|vulva|testicle|glasswort|grape, bunch of grapes|west wind)',re.I)
for p in glob.glob(os.path.join(R,'surah','*.json')):
 d=json.load(open(p,encoding='utf8'))
 for v in d['verses']:
  for w in v['w']:
   k=f"{v['k']}:{w['i']}"; words[k]=w
   if w.get('gm8_status'): gm8+=1
   if w.get('r') and hard.fullmatch((w.get('ig') or '').strip()):
    bad.append((k,'hard-placeholder',w.get('ig')))
for p in glob.glob(os.path.join(R,'interlinear','*.json')):
 d=json.load(open(p,encoding='utf8'))
 for v in d['verses']:
  for w in v['w']: inter[f"{v['k']}:{w['i']}"]=w
for k,w in words.items():
 if inter.get(k,{}).get('en')!=w.get('ig'): bad.append((k,'gloss-parity'))
for folder,fld in [('root','meaning'),('lexicon','summary')]:
 for p in glob.glob(os.path.join(R,folder,'*.json')):
  d=json.load(open(p,encoding='utf8'))
  if folder=='root': roots+=1
  else: lex+=1
  s=d.get(fld,'')
  if isinstance(s,str) and debris.search(s): bad.append((p,'editorial-debris',s[:120]))
for p in glob.glob(os.path.join(R,'root','*.json')):
 d=json.load(open(p,encoding='utf8')); stem=os.path.splitext(os.path.basename(p))[0]
 if d.get('root')!=stem: bad.append((stem,'root-self-id',d.get('root')))
 if not isinstance(d.get('root_ar'),str) or not d.get('root_ar','').strip(): bad.append((stem,'root-ar'))
gm1=json.load(open(os.path.join(R,'gold_master','GM1_ARABIC_TEXT_HASHES.json'),encoding='utf8'))
va=hashlib.sha256(); ts=hashlib.sha256()
for p in sorted(glob.glob(os.path.join(R,'surah','*.json'))):
 d=json.load(open(p,encoding='utf8'))
 for v in d['verses']:
  va.update((v['k']+'\t'+v.get('ar','')+'\n').encode())
  for w in v['w']: ts.update(f"{v['k']}:{w['i']}\t{w['ar']}\n".encode())
if va.hexdigest()!=gm1['verse_arabic_sha256']: bad.append(('GM1','arabic-hash'))
if ts.hexdigest()!=gm1['token_sequence_sha256']: bad.append(('GM1','token-hash'))
print(f"GM8 validation: words={len(words)} gm8_token_records={gm8} root_pages={roots} lexicon_files={lex} failures={len(bad)}")
for x in bad[:40]: print(x)
sys.exit(1 if bad else 0)
