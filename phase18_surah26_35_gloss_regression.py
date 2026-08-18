import json,glob,os,sys
ROOT=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else os.path.dirname(__file__))
words={}
for p in glob.glob(os.path.join(ROOT,"surah","*.json")):
 d=json.load(open(p,encoding="utf-8"))
 for v in d["verses"]:
  for w in v["w"]: words[f"{v['k']}:{w['i']}"]=w
protect={'28:71:8': 'continuous', '28:72:8': 'continuous', '28:85:6': 'take you back', '29:14:14': 'flood', '29:24:10': 'burn', '29:33:17': 'save you', '30:4:2': 'three to nine', '30:46:6': 'bringers of good tidings', '31:10:4': 'pillars', '31:16:11': 'rock', '31:18:9': 'exultantly', '31:19:1': 'be moderate', '31:20:16': 'apparent', '31:20:17': 'unapparent', '31:32:21': 'treacherous', '32:11:6': 'entrusted', '32:16:4': 'beds', '33:5:19': 'erred', '33:21:7': 'excellent pattern', '33:26:8': 'fortresses', '33:28:13': 'give you a gracious release', '33:35:11': 'patient women', '33:35:14': 'charitable men', '33:49:20': 'give them a gracious release', '33:50:18': 'paternal uncle', '33:52:9': 'exchange', '33:60:12': 'incite you', '33:61:6': 'massacred completely', '33:67:5': 'masters', '33:70:8': 'appropriate', '34:5:5': 'seeking to cause failure', '34:7:12': 'disintegrated', '34:11:3': 'full', '34:13:8': 'bowls', '34:14:13': 'staff', '34:15:3': 'Saba', '34:16:5': 'dam', '34:18:9': 'visible', '34:19:12': 'dispersion', '34:23:11': 'terror is removed', '34:38:5': 'to cause failure', '34:45:7': 'a tenth', '34:51:6': 'escape', '34:54:1': 'prevention will be placed', '35:1:13': 'four', '35:2:8': 'withhold', '35:10:24': 'perish', '35:11:22': 'aged person', '35:12:7': 'palatable', '35:12:10': 'salty', '35:18:8': 'heavily laden', '35:22:13': 'make hear', '35:27:16': 'tracts', '35:27:18': 'red', '35:27:21': 'extremely black', '35:27:22': 'black', '35:29:16': 'perish', '35:33:13': 'silk', '35:35:14': 'weariness', '35:37:2': 'cry out'}
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
