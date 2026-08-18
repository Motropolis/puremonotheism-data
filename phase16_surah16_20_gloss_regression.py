import json,glob,os,sys
ROOT=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else os.path.dirname(__file__))
words={}
for p in glob.glob(os.path.join(ROOT,"surah","*.json")):
 d=json.load(open(p,encoding="utf-8"))
 for v in d["verses"]:
  for w in v["w"]: words[f"{v['k']}:{w['i']}"]=w
protect={'18:41:8': 'seek it', '18:47:6': 'prominent', '18:47:9': 'leave behind', '18:49:14': 'leaves', '18:51:12': 'misguiders', '18:51:13': 'assistants', '18:63:6': 'rock', '18:70:9': 'make mention', '18:77:11': 'offer hospitality', '18:77:14': 'wall', '18:79:17': 'by force', '18:81:3': 'substitute', '18:82:2': 'wall', '18:90:15': 'shield', '18:96:17': 'pour', '18:98:11': 'level', '18:99:4': 'surging', '18:105:14': 'importance', '18:109:18': 'supplement', '19:3:5': 'private', '19:23:13': 'forgotten', '19:24:10': 'stream', '19:25:1': 'shake', '19:27:10': 'unprecedented', '19:29:1': 'pointed', '19:37:9': 'scene', '19:47:10': 'gracious', '19:55:9': 'pleasing', '19:58:29': 'weeping', '19:65:7': 'have patience', '19:68:5': 'bring them', '19:74:9': 'outward appearance', '19:81:8': 'honor', '19:83:8': 'inciting', '19:85:6': 'delegation', '19:86:5': 'in thirst', '19:89:4': 'atrocious', '19:97:10': 'hostile', '19:98:7': 'perceive', '20:12:5': 'sandals', '20:18:4': 'lean', '20:18:12': 'uses', '20:22:1': 'draw in', '20:40:24': 'severe trial', '20:42:6': 'slacken', '20:44:4': 'gentle', '20:45:6': 'hasten punishment', '20:61:10': 'exterminate', '20:64:10': 'overcomes', '20:66:7': 'seemed', '20:71:20': 'trunks', '20:77:16': 'being overtaken', '20:83:2': 'made you hasten', '20:85:9': 'Samiri', '20:87:15': 'Samiri', '20:94:5': 'beard', '20:95:4': 'Samiri', '20:97:10': 'contact', '20:97:23': 'burn', '20:97:28': 'blow it away', '20:105:7': 'blow them away', '20:107:6': 'unevenness', '20:112:11': 'deprivation', '20:113:12': 'cause', '20:121:7': 'fasten', '20:124:7': 'life', '20:129:7': 'obligation', '20:130:12': 'setting', '20:132:4': 'be steadfast', '20:134:19': 'be disgraced', '20:135:3': 'waiting'}
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
