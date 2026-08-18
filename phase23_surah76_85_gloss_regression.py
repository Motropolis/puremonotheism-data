import json,glob,os,sys
ROOT=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else os.path.dirname(__file__))
words={}
for p in glob.glob(os.path.join(ROOT,"surah","*.json")):
 d=json.load(open(p,encoding="utf-8"))
 for v in d["verses"]:
  for w in v["w"]: words[f"{v['k']}:{w['i']}"]=w
protect={'76:1:11': 'mentioned', '76:4:4': 'chains', '76:5:7': 'mixture', '76:6:7': 'gush forth', '76:12:5': 'silk', '76:14:5': 'fruit to be picked', '76:15:8': 'glasses', '76:16:1': 'glasses', '76:17:5': 'mixture', '76:19:4': 'made eternal', '76:22:8': 'appreciated', '77:1:1': 'those sent forth', '77:9:3': 'opened', '77:27:4': 'lofty', '77:30:6': 'columns', '77:31:6': 'flame', '77:32:3': 'sparks', '77:33:3': 'yellowish', '78:7:2': 'stakes', '78:9:2': 'sleep', '78:16:2': 'entwined', '78:25:3': 'foul purulence', '78:26:2': 'appropriate', '78:32:1': 'gardens', '78:34:2': 'full', '79:1:1': 'those who extract', '79:1:2': 'with violence', '79:2:1': 'those who remove', '79:2:2': 'with ease', '79:3:1': 'those who glide', '79:4:1': 'those who race ahead', '79:10:3': 'returned', '79:10:5': 'former state', '79:11:4': 'decayed', '79:12:5': 'losing', '79:14:3': "earth's surface", '79:28:2': 'ceiling', '79:29:1': 'darkened', '79:30:4': 'spread', '79:42:5': 'arrival', '79:46:7': 'afternoon', '80:6:3': 'give attention', '80:15:2': 'messenger-angels', '80:28:2': 'herbage', '80:30:1': 'gardens', '80:38:3': 'bright', '80:39:1': 'laughing', '80:39:2': 'rejoicing', '80:40:4': 'dust', '80:41:2': 'blackness', '81:4:3': 'neglected', '81:5:2': 'wild beasts', '81:6:3': 'filled with flame', '81:12:3': 'set ablaze', '81:14:4': 'brought', '81:15:3': 'retreating', '81:16:1': 'those that run', '81:16:2': 'disappear', '81:21:1': 'obeyed', '81:23:3': 'horizon', '83:2:6': 'take in full', '83:3:2': 'give by measure', '83:3:4': 'give by weight', '83:12:6': 'transgressor', '83:15:6': 'partitioned', '83:16:3': 'burn in Hellfire', '83:26:1': 'last of it', '83:27:1': 'mixture', '83:30:4': 'exchange derisive glances', '84:6:7': 'laboring', '84:6:8': 'meet it', '84:17:3': 'envelops', '84:23:4': 'keep within', '85:4:3': 'trench', '85:16:1': 'Effecter'}
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
