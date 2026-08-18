import json,glob,os,sys
ROOT=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else os.path.dirname(__file__))
words={}
for p in glob.glob(os.path.join(ROOT,"surah","*.json")):
 d=json.load(open(p,encoding="utf-8"))
 for v in d["verses"]:
  for w in v["w"]: words[f"{v['k']}:{w['i']}"]=w
protect={'2:9:1': 'deceive', '2:76:13': 'tell them', '2:102:45': 'causing harm', '2:186:9': 'caller', '2:222:3': 'menstruation', '2:231:9': 'release them', '2:231:13': 'harm', '2:251:15': 'repelling', '2:270:4': 'expenditure', '2:282:79': 'grow weary', '3:9:3': 'Gatherer', '3:103:22': 'brink', '3:118:11': 'corruption', '4:27:11': 'incline', '5:6:33': 'place of relieving oneself', '5:6:43': 'wipe', '5:82:23': 'monks', '7:8:1': 'weighing', '7:22:10': 'patching together', '7:143:29': 'levelled', '8:6:12': 'looking', '9:8:11': 'please you', '11:37:6': 'address me', '11:56:13': 'forelock', '11:81:15': 'look back', '11:107:13': 'Doer', '12:43:10': 'lean', '16:58:7': 'darkened', '16:83:5': 'deny it', '17:81:4': 'vanished', '17:83:6': 'turns away', '18:41:4': 'sunken', '22:33:11': 'Ancient', '26:80:2': 'I am ill', '28:32:10': 'draw close', '28:58:6': 'livelihood', '36:51:7': 'graves', '36:57:6': 'request', '37:66:4': 'filling', '37:130:1': 'Peace', '37:145:2': 'open shore', '38:38:4': 'shackles', '48:6:11': 'evil turn', '48:15:25': 'envy us', '53:7:2': 'horizon', '66:4:9': 'support each other', '66:5:6': 'replace'}
kept={'9:1:1': 'Disavowal is contextually defensible for براءة; no semantic correction needed.', '17:12:5': 'Effaced is a correct English rendering of محونا, though less common than erased.', '68:32:10': 'Desiring is semantically correct for راغبون in context.'}
bad=[]
for k,g in protect.items():
 if words.get(k,{}).get("ig")!=g: bad.append((k,"protected",words.get(k,{}).get("ig"),g))
for k in kept:
 if k not in words: bad.append((k,"missing-kept-token"))
for p in glob.glob(os.path.join(ROOT,"interlinear","*.json")):
 d=json.load(open(p,encoding="utf-8"))
 for v in d["verses"]:
  for w in v["w"]:
   k=f"{v['k']}:{w['i']}"
   if w.get("en")!=words[k].get("ig"): bad.append((k,"parity"))
print(f"corrected={len(protect)} kept={len(kept)} words={len(words)} failures={len(bad)}")
for x in bad[:20]: print(x)
sys.exit(1 if bad else 0)
