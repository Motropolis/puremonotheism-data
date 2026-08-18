import json,glob,os,sys
ROOT=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else os.path.dirname(__file__))
words={}
for p in glob.glob(os.path.join(ROOT,"surah","*.json")):
 d=json.load(open(p,encoding="utf-8"))
 for v in d["verses"]:
  for w in v["w"]: words[f"{v['k']}:{w['i']}"]=w
protect={'9:16:20': 'intimates', '9:19:4': 'maintenance', '9:24:8': 'relatives', '9:24:13': 'decline', '9:25:11': 'great number', '9:31:3': 'monks', '9:32:3': 'extinguish', '9:34:8': 'monks', '9:35:2': 'heated', '9:35:7': 'seared', '9:35:9': 'foreheads', '9:37:3': 'increase', '9:37:14': 'correspond', '9:42:6': 'moderate', '9:42:11': 'journey', '9:46:11': 'kept them back', '9:47:7': 'confusion', '9:52:22': 'waiting', '9:54:6': 'expenditures', '9:55:14': 'depart', '9:57:11': 'run heedlessly', '9:58:3': 'criticize', '9:59:19': 'desirous', '9:60:7': 'those whose hearts are brought together', '9:60:11': 'those in debt', '9:62:4': 'satisfy', '9:62:9': 'satisfy', '9:70:15': 'overturned towns', '9:79:2': 'criticize', '9:85:13': 'depart', '9:87:5': 'those who stay behind', '9:90:2': 'those with excuses', '9:93:12': 'those who stay behind', '9:98:10': 'turns of misfortune', '9:98:12': 'misfortune', '9:107:4': 'harm', '9:107:11': 'warred', '9:109:15': 'edge', '9:109:16': 'bank', '9:109:17': 'about to collapse', '9:109:18': 'collapsed', '9:110:6': 'skepticism', '9:112:1': 'repentant', '9:114:21': 'compassionate', '9:118:18': 'refuge', '9:120:10': 'remain behind', '9:120:27': 'hunger', '9:120:33': 'ground', '9:120:40': 'infliction', '9:121:3': 'expenditure', '9:128:10': 'concerned'}
bad=[]
for k,g in protect.items():
 if words.get(k,{}).get("ig")!=g: bad.append((k,words.get(k,{}).get("ig"),g))
for p in glob.glob(os.path.join(ROOT,"interlinear","*.json")):
 d=json.load(open(p,encoding="utf-8"))
 for v in d["verses"]:
  for w in v["w"]:
   k=f"{v['k']}:{w['i']}"
   if w.get("en")!=words[k].get("ig"): bad.append((k,"interlinear-parity"))
print(f"protected={len(protect)} words={len(words)} failures={len(bad)}")
for x in bad[:50]: print(x)
sys.exit(1 if bad else 0)
