import json,glob,os,sys
ROOT=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else os.path.dirname(__file__))
words={}
for p in glob.glob(os.path.join(ROOT,"surah","*.json")):
 d=json.load(open(p,encoding="utf-8"))
 for v in d["verses"]:
  for w in v["w"]: words[f"{v['k']}:{w['i']}"]=w
protect={'66:5:15': 'traveling', '66:12:2': 'daughter', '67:3:12': 'inconsistency', '67:3:18': 'breaks', '67:4:8': 'humbled', '67:5:7': 'projectiles', '67:7:8': 'boils up', '67:11:1': 'admit', '67:11:3': 'away with', '67:22:3': 'fallen on his face', '67:27:13': 'call for', '67:30:6': 'sunken', '68:6:2': 'afflicted', '68:10:4': 'habitual swearer', '68:11:1': 'scorner', '68:11:3': 'malicious gossip', '68:12:3': 'transgressor', '68:13:1': 'cruel', '68:13:4': 'ignoble pretender', '68:16:1': 'brand him', '68:22:7': 'cut the fruit', '68:30:5': 'blaming each other', '68:32:4': 'substitute', '68:43:11': 'sound', '68:49:8': 'naked shore', '68:49:10': 'censured', '69:6:5': 'screaming', '69:7:7': 'in succession', '69:7:11': 'fallen', '69:7:13': 'trunks', '69:9:5': 'overturned cities', '69:10:6': 'exceeding', '69:12:4': 'be conscious of it', '69:13:5': 'blast', '69:16:5': 'infirm', '69:18:6': 'concealed', '69:22:3': 'elevated', '69:23:1': 'fruit to be picked', '69:24:5': 'put forth', '69:24:8': 'past', '69:34:2': 'encourage', '69:36:5': 'discharge of wounds', '69:47:6': 'prevent', '70:3:4': 'ways of ascent', '70:11:1': 'shown each other', '70:16:1': 'remover', '70:18:2': 'hoarded', '70:19:4': 'anxious', '70:20:4': 'impatient', '70:21:4': 'withholding', '70:23:5': 'constant', '70:37:5': 'separate groups', '70:41:8': 'outdone', '70:43:4': 'graves', '70:43:5': 'rapidly', '71:7:7': 'fingers', '71:9:7': 'secretly', '71:13:6': 'grandeur', '71:19:5': 'expanse', '71:23:9': "Suwa'", '71:23:13': 'Nasr', '71:27:9': 'wicked', '72:3:3': 'nobleness', '72:4:7': 'excessive transgression', '72:6:11': 'burden', '72:8:6': 'guards', '72:8:8': 'burning flames', '72:13:12': 'deprivation', '72:13:14': 'burden', '72:14:5': 'unjust', '72:14:9': 'sought out', '72:15:2': 'unjust', '72:17:10': 'arduous', '73:4:6': 'measured recitation', '73:6:2': 'hours of the night', '73:6:6': 'concurrence', '73:8:6': 'complete devotion', '73:14:7': 'heap of sand', '74:1:2': 'one who covers himself', '74:8:2': 'blown', '74:29:1': 'blackening', '74:30:2': 'nine', '74:31:14': 'be convinced', '74:34:3': 'brightens', '74:37:7': 'stay behind', '74:45:4': 'those engaged in it', '74:48:4': 'intercessors', '75:16:2': 'move', '75:23:3': 'looking', '75:25:5': 'backbreaking calamity', '75:26:4': 'collarbones', '75:27:3': 'cure him', '75:29:1': 'wound', '75:33:5': 'swaggering', '75:36:5': 'neglected', '75:37:5': 'semen'}
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
