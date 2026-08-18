import json,glob,os,sys
ROOT=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else os.path.dirname(__file__))
words={}
for p in glob.glob(os.path.join(ROOT,"surah","*.json")):
 d=json.load(open(p,encoding="utf-8"))
 for v in d["verses"]:
  for w in v["w"]: words[f"{v['k']}:{w['i']}"]=w
protect={'56:39:1': 'company', '56:40:1': 'company', '56:52:5': 'zaqqum', '56:53:1': 'filling', '56:55:3': 'thirsty camels', '56:60:7': 'outdone', '56:63:3': 'sow', '56:64:2': 'makes it grow', '56:65:6': 'remain in wonder', '56:70:4': 'bitter', '56:72:6': 'producer', '56:83:4': 'throat', '56:94:1': 'burning', '57:7:7': 'made you successors', '57:13:8': 'acquire some', '57:13:21': 'interior', '57:16:24': 'hardened', '57:20:20': 'dries', '57:27:29': 'observe it', '58:4:6': 'consecutively', '58:4:14': 'feeding', '58:10:9': 'harm', '58:11:7': 'make space', '58:19:1': 'overcome', '58:22:21': 'kindred', '59:2:20': 'fortresses', '59:2:33': 'destroyed', '59:2:38': 'take warning', '59:7:2': 'restored', '59:7:20': 'perpetual distribution', '59:9:24': 'privation', '59:11:5': 'practice hypocrisy', '59:13:3': 'fearful', '59:14:7': 'fortified', '59:24:4': 'Inventor', '59:24:5': 'Fashioner', '60:4:4': 'excellent pattern', '60:6:5': 'excellent pattern', '60:7:8': 'were enemies', '60:10:40': 'marriage bonds', '60:12:16': 'commit unlawful sexual intercourse', '61:4:11': 'joined firmly', '61:8:2': 'extinguish', '61:8:7': 'perfect', '62:3:4': 'joined', '62:8:8': 'meet you', '62:9:9': "Jumu'ah", '63:4:10': 'pieces of wood', '65:1:38': 'bring about', '65:4:4': 'menstruation', '65:4:16': 'pregnant', '65:5:12': 'make great', '65:6:8': 'harm', '65:6:9': 'oppress', '65:8:9': 'took it to account'}
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
