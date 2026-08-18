import json,glob,os,sys,collections
ROOT=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else os.path.dirname(__file__))
words={}; root_count=0
for p in glob.glob(os.path.join(ROOT,"surah","*.json")):
 d=json.load(open(p,encoding="utf-8"))
 for v in d["verses"]:
  for w in v["w"]:
   k=f"{v['k']}:{w['i']}"; words[k]=w
   if w.get("r"): root_count+=1
bad=[]
staff=["2:60:7","7:107:2","7:117:6","7:160:14","20:18:3","26:32:2","26:45:3","26:63:6","27:10:2","28:31:3"]
for k in staff:
 if words[k].get("r")!="3-s6-w": bad.append((k,"staff-root",words[k].get("r")))
for k,w in words.items():
 if w.get("lem")=="عَصا" and k not in staff and w.get("r")!="3-s6-y":
  bad.append((k,"disobey-root",w.get("r")))
for p in glob.glob(os.path.join(ROOT,"interlinear","*.json")):
 d=json.load(open(p,encoding="utf-8"))
 for v in d["verses"]:
  for w in v["w"]:
   k=f"{v['k']}:{w['i']}"
   if w.get("en")!=words[k].get("ig"): bad.append((k,"gloss-parity"))
print(f"words={len(words)} root_bearing={root_count} failures={len(bad)}")
for x in bad[:20]: print(x)
sys.exit(1 if bad else 0)
