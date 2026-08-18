import json,glob,os,sys,unicodedata
ROOT=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else os.path.dirname(__file__))
bad=[]; files=0; words=0
folders=['surah','interlinear','root','lexicon','lemma','pronoun','muqattaat','browse','suggest','search']
for f in folders:
 for p in glob.glob(os.path.join(ROOT,f,'*.json')):
  files+=1
  try: d=json.load(open(p,encoding='utf-8'))
  except Exception as e: bad.append((p,'json-parse',str(e))); continue
  if f in ('surah','interlinear'):
   if not isinstance(d,dict) or not isinstance(d.get('verses'),list): bad.append((p,'top-schema'))
   else:
    for v in d['verses']:
     if not isinstance(v.get('k'),str) or not isinstance(v.get('w'),list): bad.append((p,'verse-schema',v.get('k')))
     for w in v.get('w',[]):
      words+=1
      if not isinstance(w.get('i'),int) or not isinstance(w.get('ar'),str): bad.append((p,'word-schema',v.get('k'),w.get('i')))
  if f=='search' and isinstance(d,dict):
   for k in d:
    if any(unicodedata.category(c)=='Cf' for c in k): bad.append((p,'format-control-key',repr(k)))
print(f"files={files} canonical_word_records={words} failures={len(bad)}")
for x in bad[:30]: print(x)
sys.exit(1 if bad else 0)
