import json,glob,os,sys
ROOT=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else os.path.dirname(__file__))
words={}
for p in glob.glob(os.path.join(ROOT,"surah","*.json")):
 d=json.load(open(p,encoding="utf-8"))
 for v in d["verses"]:
  for w in v["w"]: words[f"{v['k']}:{w['i']}"]=w
protect={'22:38:3': 'defends', '22:38:12': 'treacherous', '22:40:13': 'checks', '22:40:19': 'monasteries', '22:40:20': 'churches', '22:45:12': 'abandoned', '22:45:14': 'lofty', '22:51:5': 'seeking to cause failure', '22:52:16': 'abolishes', '22:52:22': 'makes precise', '22:54:11': 'humbly submit', '22:67:8': 'contend', '23:18:11': 'take it away', '23:27:27': 'address', '23:30:7': 'testing', '23:50:8': 'high ground', '23:66:9': 'turning back', '23:76:5': 'yield', '23:101:6': 'relationships', '24:2:1': 'female fornicator', '24:2:3': 'lash', '24:3:5': 'female fornicator', '24:3:8': 'female fornicator', '24:4:9': 'lash', '24:4:10': 'eighty', '24:22:2': 'swear', '24:31:18': 'chests', '24:31:49': 'attendants', '24:32:1': 'marry', '24:33:35': 'chastity', '24:35:12': 'glass', '24:35:13': 'glass', '24:35:25': 'western', '24:41:17': 'exalting', '24:43:25': 'hail', '24:53:12': 'known', '24:58:27': 'night prayer', '24:60:1': 'women past childbearing age', '24:62:12': 'common', '24:63:18': 'dissent', '25:12:8': 'fury', '25:12:9': 'roaring', '25:27:2': 'bite', '25:32:15': 'spaced distinctly', '25:33:8': 'explanation', '25:36:9': 'destruction', '25:39:7': 'total destruction', '25:47:7': 'sleep', '25:53:9': 'salty', '25:53:15': 'prohibiting', '25:54:9': 'relationship by marriage', '25:63:9': 'address', '25:68:17': 'commit unlawful sexual intercourse', '25:77:12': 'adherent'}
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
