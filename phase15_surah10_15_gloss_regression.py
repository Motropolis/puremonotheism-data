import json,glob,os,sys
ROOT=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else os.path.dirname(__file__))
words={}
for p in glob.glob(os.path.join(ROOT,"surah","*.json")):
 d=json.load(open(p,encoding="utf-8"))
 for v in d["verses"]:
  for w in v["w"]: words[f"{v['k']}:{w['i']}"]=w
protect={'12:43:24': 'interpret', '12:45:5': 'remembered', '12:46:11': 'lean', '12:47:2': 'plant', '12:47:10': 'spikes', '12:49:11': 'press', '12:54:5': 'appoint him exclusively', '12:59:2': 'furnished them', '12:59:3': 'supplies', '12:70:2': 'furnished them', '12:70:3': 'supplies', '12:70:5': 'measuring bowl', '12:70:11': 'announcer', '12:70:13': 'caravan', '12:70:15': 'thieves', '12:71:5': 'missing', '12:72:2': 'missing', '12:73:12': 'thieves', '12:82:6': 'caravan', '12:86:3': 'complain', '12:92:3': 'blame', '12:94:3': 'caravan', '12:94:12': 'think me weakened in mind', '12:103:5': 'strive', '12:107:4': 'overwhelming punishment', '13:2:6': 'pillars', '13:4:10': 'several from a root', '13:4:12': 'otherwise', '13:11:2': 'successive', '13:13:19': 'assault', '13:17:11': 'rising', '13:17:31': 'cast off', '13:29:5': 'good state', '13:34:8': 'more severe', '13:34:14': 'protector', '13:36:11': 'deny', '13:37:20': 'protector', '13:39:1': 'eliminates', '13:41:12': 'adjuster', '14:6:17': 'slaughtering', '14:15:1': 'requested victory', '14:16:7': 'purulent', '14:17:1': 'gulp', '14:17:4': 'swallow', '14:24:13': 'branches', '14:35:9': 'keep me away', '14:43:2': 'heads raised', '14:44:26': 'cessation', '14:49:6': 'shackles', '14:50:1': 'garments', '15:18:3': 'steals', '15:22:3': 'fertilizing', '15:22:12': 'retainers', '15:24:3': 'preceding generations', '15:24:7': 'later ones', '15:26:7': 'black mud', '15:26:8': 'altered', '15:28:11': 'black mud', '15:28:12': 'altered', '15:33:10': 'black mud', '15:33:11': 'altered', '15:52:9': 'fearful', '15:59:5': 'save them', '15:65:9': 'look back', '15:66:8': 'eliminated', '15:68:6': 'shame me', '15:75:5': 'those who discern', '15:88:13': 'lower', '15:91:4': 'portions', '15:95:3': 'mockers'}
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
