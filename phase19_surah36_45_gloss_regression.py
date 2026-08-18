import json,glob,os,sys
ROOT=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else os.path.dirname(__file__))
words={}
for p in glob.glob(os.path.join(ROOT,"surah","*.json")):
 d=json.load(open(p,encoding="utf-8"))
 for v in d["verses"]:
  for w in v["w"]: words[f"{v['k']}:{w['i']}"]=w
protect={'39:20:10': 'built', '39:21:10': 'springs', '39:21:20': 'dries', '39:29:7': 'quarreling', '39:35:4': 'worst', '39:36:3': 'sufficient', '39:37:7': 'misleader', '39:45:5': 'shrink with aversion', '39:56:14': 'mockers', '39:60:9': 'blackened', '39:67:12': 'folded', '39:68:4': 'fall dead', '39:69:1': 'shine', '39:71:6': 'groups', '39:73:7': 'groups', '40:3:1': 'forgiver', '40:16:3': 'come forth', '40:18:3': 'Approaching Day', '40:19:2': 'deceiving glance', '40:21:30': 'protector', '40:37:23': 'ruin', '40:41:6': 'salvation', '40:47:2': 'argue', '40:71:5': 'chains', '40:81:6': 'deny', '41:10:10': 'sustenance', '41:16:4': 'screaming wind', '41:21:7': 'made us speak', '41:21:10': 'made speak', '41:22:3': 'covering yourselves', '41:24:11': 'allowed to appease', '41:25:1': 'appointed', '41:26:8': 'speak noisily', '41:30:15': 'receive good tidings', '41:31:16': 'request', '41:36:5': 'evil suggestion', '41:38:12': 'become weary', '41:40:3': 'inject deviation', '41:47:10': 'coverings', '41:49:2': 'weary', '41:49:10': 'hopeless', '41:51:6': 'distances himself', '41:51:13': 'extensive', '41:53:4': 'horizons', '42:16:11': 'invalid', '42:24:13': 'eliminates', '42:32:3': 'ships', '42:33:6': 'motionless', '42:45:10': 'covert', '42:47:16': 'refuge', '43:16:6': 'chosen you', '43:17:10': 'dark', '43:26:7': 'disassociated', '43:32:8': 'livelihood', '43:32:20': 'for service', '43:33:15': 'stairways', '43:34:5': 'recline', '43:36:6': 'appoint', '43:79:5': 'devising', '44:15:6': 'return', '44:23:5': 'pursued', '44:35:8': 'resurrected', '44:38:7': 'in play', '44:43:3': 'zaqqum', '44:46:1': 'boiling', '44:47:2': 'drag him', '44:59:3': 'watching', '45:29:8': 'transcribed'}
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
sys.exit(1 if bad else 0)
