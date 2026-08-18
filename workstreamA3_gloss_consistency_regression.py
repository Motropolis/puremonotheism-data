import json,glob,os,sys
ROOT=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else os.path.dirname(__file__))
words={}
for p in glob.glob(os.path.join(ROOT,"surah","*.json")):
 d=json.load(open(p,encoding="utf-8"))
 for v in d["verses"]:
  for w in v["w"]: words[f"{v['k']}:{w['i']}"]=w
protect={'2:181:9': 'who', '13:37:13': 'what', '27:20:5': 'not', '36:22:2': 'not', '8:6:10': 'death', '4:33:19': 'witness', '7:35:3': 'if', '20:123:8': 'if', '8:57:1': 'if', '20:132:2': 'your family', '41:40:3': 'deviate', '20:74:13': 'live', '87:13:6': 'live'}
bad=[]
for k,g in protect.items():
 if words.get(k,{}).get("ig")!=g: bad.append((k,"protected",words.get(k,{}).get("ig"),g))
for p in glob.glob(os.path.join(ROOT,"interlinear","*.json")):
 d=json.load(open(p,encoding="utf-8"))
 for v in d["verses"]:
  for w in v["w"]:
   k=f"{v['k']}:{w['i']}"
   if w.get("en")!=words[k].get("ig"): bad.append((k,"parity"))
print(f"corrected={len(protect)} words={len(words)} failures={len(bad)}")
sys.exit(1 if bad else 0)
