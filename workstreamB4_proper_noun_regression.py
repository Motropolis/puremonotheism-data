import json,glob,os,sys
ROOT=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else os.path.dirname(__file__))
words={}
for p in glob.glob(os.path.join(ROOT,"surah","*.json")):
 d=json.load(open(p,encoding="utf-8"))
 for v in d["verses"]:
  for w in v["w"]: words[f"{v['k']}:{w['i']}"]=w
protect={'5:114:5': 'O God', '8:32:3': 'O God', '10:10:4': 'O God', '3:39:11': 'Yahya', '19:7:6': 'Yahya', '21:90:5': 'Yahya', '3:144:2': 'Muhammad', '33:40:3': 'Muhammad', '47:2:9': 'Muhammad', '61:6:24': 'Ahmad', '4:163:25': 'Zabur', '17:55:15': 'Zabur', '21:105:4': 'Zabur', '5:95:26': 'Kaaba', '5:97:3': 'Kaaba', '27:22:12': 'Saba', '2:158:3': 'al-Marwah', '2:198:12': 'Arafat', '11:44:13': 'al-Judi', '46:21:7': 'al-Ahqaf', '71:23:7': 'Wadd', '71:23:11': 'Yaghuth'}
bad=[]
for k,g in protect.items():
 if words.get(k,{}).get("ig")!=g: bad.append((k,"proper-name",words.get(k,{}).get("ig"),g))
for p in glob.glob(os.path.join(ROOT,"interlinear","*.json")):
 d=json.load(open(p,encoding="utf-8"))
 for v in d["verses"]:
  for w in v["w"]:
   k=f"{v['k']}:{w['i']}"
   if w.get("en")!=words[k].get("ig"): bad.append((k,"parity"))
print(f"protected={len(protect)} words={len(words)} failures={len(bad)}")
sys.exit(1 if bad else 0)
