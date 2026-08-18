import json,glob,os,sys
ROOT=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else os.path.dirname(__file__))
words={}
for p in glob.glob(os.path.join(ROOT,"surah","*.json")):
 d=json.load(open(p,encoding="utf-8"))
 for v in d["verses"]:
  for w in v["w"]: words[f"{v['k']}:{w['i']}"]=w
protect={'4:33:19': 'bound', '4:34:17': 'guarding', '4:34:28': 'beds', '4:35:15': 'cause reconciliation', '4:43:16': 'passing through', '4:43:31': 'place of relieving oneself', '4:43:41': 'wipe', '4:46:13': 'heard', '4:46:14': 'attend to us', '4:46:15': 'twisting', '4:46:17': 'defaming', '4:54:2': 'envy', '4:56:9': 'roasted through', '4:62:16': 'reconciliation', '4:69:18': 'companions', '4:72:4': 'lingers behind', '4:83:20': 'draw conclusions', '4:84:9': 'encourage', '4:84:22': 'exemplary punishment', '4:85:22': 'Keeper', '4:92:53': 'consecutively', '4:95:8': 'disabled', '4:100:9': 'alternative locations', '4:102:36': 'incline', '4:102:38': 'single attack', '4:105:14': 'deceitful', '4:107:13': 'habitually deceitful', '4:117:11': 'rebellious', '4:128:8': 'evasion', '4:128:18': 'made present', '4:129:8': 'strive', '4:129:10': 'incline', '4:129:12': 'inclination', '4:129:14': 'hanging', '4:135:29': 'distort', '4:140:28': 'will gather', '4:141:20': 'gain the advantage', '4:142:3': 'deceive', '4:142:13': 'showing off', '4:145:4': 'depth', '4:146:7': 'be sincere', '4:154:13': 'transgress', '4:155:13': 'wrapped', '4:157:30': 'following', '4:172:2': 'disdain', '4:172:12': 'disdain'}
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
