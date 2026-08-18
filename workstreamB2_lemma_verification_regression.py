import json,glob,os,sys,collections
ROOT=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else os.path.dirname(__file__))
words={}
for p in glob.glob(os.path.join(ROOT,"surah","*.json")):
 d=json.load(open(p,encoding="utf-8"))
 for v in d["verses"]:
  for w in v["w"]: words[f"{v['k']}:{w['i']}"]=w
protect={'2:61:57': 'عَصَى', '2:71:18': 'الآن', '2:93:14': 'عَصَى', '2:173:18': 'عَدا', '2:187:24': 'الآن', '3:112:33': 'عَصَى', '3:152:14': 'عَصَى', '4:14:2': 'عَصَى', '4:18:14': 'الآن', '4:42:5': 'عَصَى', '4:46:10': 'عَصَى', '5:78:15': 'عَصَى', '6:15:5': 'عَصَى', '6:145:35': 'عَدا', '7:4:10': 'قال', '8:66:1': 'الآن', '10:15:35': 'عَصَى', '10:51:7': 'الآن', '10:91:1': 'الآن', '10:91:3': 'عَصَى', '11:59:6': 'عَصَى', '11:63:18': 'عَصَى', '12:51:20': 'الآن', '14:36:12': 'عَصَى', '16:115:18': 'عَدا', '18:69:8': 'عَصَى', '20:93:3': 'عَصَى', '20:121:12': 'عَصَى', '23:7:7': 'عَدا', '26:166:11': 'عَدا', '26:216:2': 'عَصَى', '33:36:18': 'عَصَى', '39:13:5': 'عَصَى', '55:44:5': 'آنٍ', '60:12:28': 'عَصَى', '66:6:16': 'عَصَى', '69:10:1': 'عَصَى', '70:31:7': 'عَدا', '71:21:5': 'عَصَى', '72:9:9': 'الآن', '72:23:7': 'عَصَى', '73:16:1': 'عَصَى', '79:21:2': 'عَصَى'}
bad=[]
for k,lem in protect.items():
 w=words.get(k,{})
 if w.get("lem")!=lem: bad.append((k,"lemma",w.get("lem"),lem))
 if "lem_source" not in w: bad.append((k,"missing-provenance"))
# No lemma label should span multiple nonempty roots after B2.
groups=collections.defaultdict(set)
for w in words.values():
 if w.get("lem") and w.get("r"): groups[w["lem"]].add(w["r"])
for lem,roots in groups.items():
 if len(roots)>1: bad.append((lem,"multi-root",sorted(roots)))
print(f"protected={len(protect)} words={len(words)} failures={len(bad)}")
for x in bad[:20]: print(x)
sys.exit(1 if bad else 0)
