import json,glob,os,sys
ROOT=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else os.path.dirname(__file__))
words={}
for p in glob.glob(os.path.join(ROOT,"surah","*.json")):
 d=json.load(open(p,encoding="utf-8"))
 for v in d["verses"]:
  for w in v["w"]: words[f"{v['k']}:{w['i']}"]=w
protect={'3:154:62': 'beds', '2:88:3': 'covered', '11:10:13': 'boastful', '16:26:10': 'foundations', '28:35:3': 'arm', '2:127:4': 'foundations', '31:18:16': 'boastful', '4:36:32': 'boastful', '57:23:15': 'boastful', '6:63:9': 'humbly', '7:205:5': 'humbly', '7:55:3': 'humbly', '21:68:2': 'burn him', '22:23:22': 'silk', '27:60:12': 'gardens', '37:62:6': 'Zaqqum', '38:12:8': 'stakes', '56:13:1': 'company', '16:37:2': 'strive', '24:33:29': 'compel', '26:214:2': 'kindred', '27:44:17': 'glass', '28:15:37': 'misleader', '34:16:11': 'bitter fruit', '5:89:13': 'feeding', '2:19:10': 'fingers', '2:222:10': 'menstruation', '17:16:14': 'destruction', '17:37:5': 'exultantly', '26:52:8': 'pursued', '56:17:4': 'made eternal', '69:21:4': 'pleasing', '6:85:2': 'Yahya'}
bad=[]
for k,g in protect.items():
 if words.get(k,{}).get("ig")!=g: bad.append((k,"protected",words.get(k,{}).get("ig"),g))
for p in glob.glob(os.path.join(ROOT,"interlinear","*.json")):
 d=json.load(open(p,encoding="utf-8"))
 for v in d["verses"]:
  for w in v["w"]:
   k=f"{v['k']}:{w['i']}"
   if w.get("en")!=words[k].get("ig"): bad.append((k,"parity"))
print(f"protected={len(protect)} words={len(words)} failures={len(bad)}")
for x in bad[:20]: print(x)
sys.exit(1 if bad else 0)
