import json,glob,os,sys
ROOT=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else os.path.dirname(__file__))
words={}
for p in glob.glob(os.path.join(ROOT,"surah","*.json")):
 d=json.load(open(p,encoding="utf-8"))
 for v in d["verses"]:
  for w in v["w"]: words[f"{v['k']}:{w['i']}"]=w
protect={'22:5:28': 'barren', '22:72:13': 'assault', '22:73:24': 'recover', '22:9:2': 'neck', '23:104:6': 'grimacing', '23:113:8': 'those who enumerate', '23:20:7': 'oil', '23:20:8': 'food', '23:44:4': 'in succession', '23:67:3': 'conversing by night', '24:23:5': 'unaware', '24:26:10': 'declared innocent', '24:29:8': 'inhabited', '24:33:32': 'prostitution', '25:19:7': 'avert', '25:29:11': 'deserter', '25:30:9': 'abandoned', '25:45:11': 'stationary', '25:62:6': 'in succession', '25:64:2': 'spend the night', '25:67:7': 'be sparing', '25:77:3': 'care for', '26:128:3': 'elevation', '26:129:2': 'fortresses', '26:168:5': 'detest', '27:88:4': 'rigid', '27:88:7': 'passing', '27:90:4': 'overturned', '28:23:15': 'driving back', '29:38:16': 'endowed with perception', '2:164:37': 'controlled', '2:171:6': 'shouts', '2:185:2': 'Ramadan', '2:196:12': 'shave', '2:282:110': 'transact', '2:96:17': 'remove', '30:17:4': 'reach the evening', '30:44:9': 'preparing', '31:18:2': 'turn your cheek in contempt', '31:33:15': 'avail', '32:27:8': 'barren', '33:19:19': 'lash', '33:26:15': 'take captive', '33:35:9': 'truthful', '33:40:11': 'seal', '33:50:38': 'marry', '33:53:25': 'remain for conversation', '33:59:8': 'bring down', '33:60:16': 'remain your neighbors', '33:68:7': 'curse', '34:10:7': 'repeat'}
bad=[]
for k,g in protect.items():
 if words.get(k,{}).get("ig")!=g: bad.append((k,words.get(k,{}).get("ig"),g))
# Interlinear parity for selected glosses.
for p in glob.glob(os.path.join(ROOT,"interlinear","*.json")):
 d=json.load(open(p,encoding="utf-8"))
 for v in d["verses"]:
  for w in v["w"]:
   k=f"{v['k']}:{w['i']}"
   if w.get("en")!=words[k].get("ig"): bad.append((k,"interlinear",w.get("en"),words[k].get("ig")))
print(f"protected={len(protect)} words={len(words)} failures={len(bad)}")
for x in bad[:50]: print(x)
sys.exit(1 if bad else 0)
