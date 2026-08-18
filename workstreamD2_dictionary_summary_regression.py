import json,glob,os,sys
ROOT=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else os.path.dirname(__file__))
bad=[]; roots=0; lex=0
for p in glob.glob(os.path.join(ROOT,"root","*.json")):
 d=json.load(open(p,encoding="utf-8")); roots+=1
 s=(d.get("meaning") or "").strip()
 if s.count('"')%2: bad.append((d.get("root"),"unmatched-quote-root",s))
for p in glob.glob(os.path.join(ROOT,"lexicon","*.json")):
 d=json.load(open(p,encoding="utf-8")); lex+=1
 if "summary" in d:
  s=(d.get("summary") or "").strip()
  if s.count('"')%2: bad.append((d.get("root") or d.get("lemma"),"unmatched-quote-lexicon",s))
print(f"root_pages={roots} lexicon_files={lex} failures={len(bad)}")
for x in bad[:30]: print(x)
sys.exit(1 if bad else 0)
