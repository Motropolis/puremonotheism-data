import json,glob,os,sys,collections
ROOT=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else os.path.dirname(__file__))
words={}
for p in glob.glob(os.path.join(ROOT,"surah","*.json")):
 d=json.load(open(p,encoding="utf-8"))
 for v in d["verses"]:
  for w in v["w"]: words[f"{v['k']}:{w['i']}"]=w
protect={'2:181:1': 'N', '2:181:2': 'V', '2:181:3': 'N', '2:181:4': 'N', '2:181:5': 'V', '2:181:6': 'P', '2:181:7': 'N', '2:181:8': 'P', '2:181:9': 'N', '2:181:10': 'V', '2:181:11': 'P', '2:181:12': 'N', '2:181:13': 'N', '2:181:14': 'N', '8:6:1': 'V', '8:6:2': 'P', '8:6:3': 'N', '8:6:4': 'N', '8:6:5': 'N', '8:6:6': 'V', '8:6:7': 'P', '8:6:9': 'P', '8:6:10': 'N', '8:6:11': 'N', '8:6:12': 'V', '13:37:1': 'N', '13:37:2': 'V', '13:37:3': 'N', '13:37:4': 'N', '13:37:5': 'P', '13:37:6': 'V', '13:37:7': 'N', '13:37:8': 'N', '13:37:9': 'N', '13:37:10': 'V', '13:37:11': 'P', '13:37:12': 'N', '13:37:13': 'P', '13:37:14': 'N', '13:37:15': 'P', '13:37:16': 'N', '13:37:17': 'P', '13:37:18': 'N', '13:37:19': 'P', '13:37:20': 'N', '15:7:1': 'P', '15:7:2': 'V', '15:7:3': 'N', '15:7:4': 'P', '15:7:5': 'V', '15:7:6': 'P', '15:7:7': 'N', '27:20:2': 'N', '27:20:3': 'V', '27:20:4': 'N', '27:20:5': 'P', '27:20:6': 'V', '27:20:8': 'P', '27:20:9': 'V', '27:20:10': 'P', '27:20:11': 'N', '36:22:1': 'N', '36:22:2': 'P', '36:22:3': 'V', '36:22:4': 'N', '36:22:5': 'V', '36:22:6': 'P', '36:22:7': 'V', '37:130:1': 'N', '37:130:2': 'P', '37:130:3': 'N', '37:130:4': 'N', '4:78:1': 'P', '15:2:1': 'P', '17:97:24': 'P', '28:28:5': 'P', '28:82:7': 'P', '28:82:23': 'P'}
bad=[]
for k,pos in protect.items():
 if words.get(k,{}).get("pos")!=pos: bad.append((k,"POS",words.get(k,{}).get("pos"),pos))
blanks=[k for k,w in words.items() if not w.get("pos")]
invalid=[(k,w.get("pos")) for k,w in words.items() if w.get("pos") not in {"N","V","P","NEG"}]
if blanks: bad.append(("blank-pos",len(blanks),blanks[:10]))
if invalid: bad.append(("invalid-pos",len(invalid),invalid[:10]))
print(f"protected={len(protect)} words={len(words)} blank_pos={len(blanks)} invalid_pos={len(invalid)} failures={len(bad)}")
for x in bad[:20]: print(x)
sys.exit(1 if bad else 0)
