import json,glob,os,sys
ROOT=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else os.path.dirname(__file__))
words={}
for p in glob.glob(os.path.join(ROOT,"surah","*.json")):
 d=json.load(open(p,encoding="utf-8"))
 for v in d["verses"]:
  for w in v["w"]: words[f"{v['k']}:{w['i']}"]=w
protect={'96:2:4': 'clinging substance', '96:8:4': 'return', '96:15:6': 'forelock', '96:16:1': 'forelock', '99:4:2': 'report', '100:10:1': 'obtained', '101:4:5': 'dispersed', '101:5:4': 'fluffed up', '104:1:4': 'mocker', '104:3:4': 'make him immortal', '104:4:4': 'Crusher', '104:5:4': 'Crusher', '104:9:2': 'columns', '104:9:3': 'extended', '105:2:5': 'misguidance', '105:5:3': 'eaten', '106:2:4': 'summer', '107:2:3': 'drives away', '107:3:2': 'encourage', '107:5:5': 'heedless', '107:6:3': 'make show', '108:3:2': 'enemy', '111:1:4': 'Lahab', '111:3:4': 'flame', '111:4:2': 'carrier', '113:4:3': 'blowers', '113:5:3': 'envier', '113:5:5': 'envies', '114:4:3': 'whisperer', '114:4:4': 'retreating'}
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
