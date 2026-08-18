import json,glob,os,sys
ROOT=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else os.path.dirname(__file__))
words={}
for p in glob.glob(os.path.join(ROOT,"surah","*.json")):
 d=json.load(open(p,encoding="utf-8"))
 for v in d["verses"]:
  for w in v["w"]: words[f"{v['k']}:{w['i']}"]=w
protect={'86:1:2': 'night comer', '86:2:4': 'night comer', '86:3:2': 'piercing', '86:7:4': 'backbone', '86:7:5': 'ribs', '86:9:3': 'secrets', '86:17:4': 'awhile', '87:5:2': 'stubble', '87:5:3': 'black', '87:6:1': 'make you recite', '88:1:4': 'Overwhelming', '88:3:2': 'exhausted', '88:6:6': 'thorny plant', '88:8:3': 'show pleasure', '88:10:3': 'elevated', '88:11:4': 'unsuitable speech', '88:16:1': 'carpets', '88:21:4': 'reminder', '89:9:3': 'carved out', '89:10:3': 'stakes', '89:13:4': 'scourge', '89:16:10': 'humiliated', '89:18:2': 'encourage one another', '89:21:5': 'pounded', '89:21:6': 'crushed', '89:26:2': 'bind', '90:4:5': 'hardship', '90:9:2': 'two lips', '90:14:2': 'feeding', '90:14:6': 'severe hunger', '90:15:3': 'near relationship', '90:17:9': 'compassion', '90:19:6': 'left', '91:3:3': 'displays', '91:8:2': 'wickedness', '91:14:3': 'brought destruction', '92:17:1': 'avoid it', '93:3:2': 'taken leave', '93:3:5': 'detested', '93:9:4': 'oppress', '93:10:4': 'repel', '93:11:4': 'report it', '95:1:1': 'fig', '95:8:3': 'most just'}
bad=[]
for k,g in protect.items():
 if words.get(k,{}).get("ig")!=g: bad.append((k,words.get(k,{}).get("ig"),g))
for p in glob.glob(os.path.join(ROOT,"interlinear","*.json")):
 d=json.load(open(p,encoding="utf-8"))
 for v in d["verses"]:
  for w in v["w"]:
   k=f"{v['k']}:{w['i']}"
   if w.get("en")!=words[k].get("ig"): bad.append((k,"parity"))
print(f"protected={len(protect)} words={len(words)} failures={len(bad)}")
sys.exit(1 if bad else 0)
