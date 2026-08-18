import json,glob,os,sys
ROOT=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else os.path.dirname(__file__))
case=["nominative","accusative","genitive"]
mood=["indicative","subjunctive","jussive","imperative"]
voice=["active","passive"]
bad=[]; words=0; verbs=0
for p in glob.glob(os.path.join(ROOT,"surah","*.json")):
 d=json.load(open(p,encoding="utf-8"))
 for v in d["verses"]:
  for w in v["w"]:
   words+=1
   g=(w.get("g") or "").lower()
   cm=[x for x in case if x in g]; mm=[x for x in mood if x in g]; vm=[x for x in voice if x in g]
   if len(cm)>1: bad.append((v["k"],w["i"],"case-conflict",cm))
   if len(mm)>1: bad.append((v["k"],w["i"],"mood-conflict",mm))
   if len(vm)>1: bad.append((v["k"],w["i"],"voice-conflict",vm))
   if w.get("pos")=="V":
    verbs+=1
    if cm: bad.append((v["k"],w["i"],"verb-with-case",cm))
    if "verb" not in g: bad.append((v["k"],w["i"],"verb-without-verb-marker",g))
   elif mm and "imperative" not in mm:
    bad.append((v["k"],w["i"],"nonverb-with-mood",mm))
print(f"words={words} verbs={verbs} failures={len(bad)}")
for x in bad[:30]: print(x)
sys.exit(1 if bad else 0)
