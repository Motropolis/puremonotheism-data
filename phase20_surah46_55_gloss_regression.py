import json,glob,os,sys
ROOT=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else os.path.dirname(__file__))
words={}
for p in glob.glob(os.path.join(ROOT,"surah","*.json")):
 d=json.load(open(p,encoding="utf-8"))
 for v in d["verses"]:
  for w in v["w"]: words[f"{v['k']}:{w['i']}"]=w
protect={'48:25:21': 'trample', '48:26:17': 'imposed', '48:27:14': 'heads shaved', '48:27:16': 'hair shortened', '48:29:36': 'grew firm', '48:29:41': 'sowers', '49:4:6': 'chambers', '49:7:28': 'rightly guided', '49:11:24': 'insult', '49:12:13': 'spy', '49:12:15': 'backbite', '49:14:20': 'deprive', '50:10:2': 'lofty', '50:15:1': 'fail', '50:16:14': 'jugular vein', '50:18:2': 'utter', '50:19:9': 'avoid', '50:21:5': 'driver', '50:25:3': 'aggressor', '50:38:13': 'weariness', '50:39:12': 'setting', '50:44:2': 'breaks away', '50:44:5': 'rapidly', '51:10:2': 'falsifiers', '51:11:5': 'heedless', '51:29:4': 'cry', '51:34:1': 'marked', '51:47:5': 'expander', '51:59:4': 'portion', '51:59:6': 'portion', '52:3:3': 'spread open', '52:12:4': 'empty discourse', '52:13:2': 'thrust', '52:30:7': 'misfortune of time', '52:31:6': 'waiters', '52:33:3': 'made it up', '52:44:6': 'falling', '52:45:7': 'struck insensible', '52:49:4': 'setting', '53:9:2': 'bow length', '53:14:2': 'Lote Tree', '53:16:3': 'Lote Tree', '53:19:3': 'al-Uzza', '53:20:1': 'Manat', '53:32:21': 'fetuses', '53:34:3': 'refrained', '53:43:4': 'makes weep', '53:53:1': 'overturned towns', '53:57:2': 'Approaching Day', '54:4:7': 'deterrence', '54:6:5': 'Caller', '54:7:5': 'graves', '54:8:3': 'Caller', '54:9:9': 'repelled', '54:11:5': 'pouring down', '54:13:5': 'nails', '54:19:5': 'screaming wind', '54:20:4': 'trunks', '54:24:10': 'madness', '54:25:9': 'insolent', '54:26:5': 'insolent', '54:27:7': 'be patient', '54:28:8': 'attended', '54:43:7': 'immunity', '54:47:5': 'madness', '54:50:5': 'glance', '55:9:2': 'weight', '55:15:4': 'smokeless flame', '55:24:2': 'ships', '55:24:3': 'with sails elevated', '55:27:5': 'Majesty', '55:37:5': 'rose-colored', '55:48:2': 'branches', '55:54:4': 'linings', '55:54:7': 'fruit', '55:56:5': 'untouched', '55:64:1': 'dark green', '55:72:4': 'pavilions', '55:74:2': 'untouched', '55:76:3': 'cushions', '55:76:5': 'fine carpets', '55:78:5': 'Majesty'}
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
