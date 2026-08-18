import json,glob,os,sys
ROOT=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else os.path.dirname(__file__))
words={}
for p in glob.glob(os.path.join(ROOT,"surah","*.json")):
 d=json.load(open(p,encoding="utf-8"))
 for v in d["verses"]:
  for w in v["w"]: words[f"{v['k']}:{w['i']}"]=w
protect={'2:181:2': 'form II perfect verb (3rd person masculine singular)', '2:181:5': 'form I perfect verb (3rd person masculine singular)', '2:181:10': 'form II imperfect verb (3rd person masculine plural)', '8:6:1': 'form III imperfect verb (3rd person masculine plural) + object pronoun (2nd person masculine singular)', '8:6:6': 'form V perfect verb (3rd person masculine singular)', '8:6:12': 'form I imperfect verb (3rd person masculine plural)', '13:37:2': 'form IV perfect verb (1st person plural) + object pronoun (3rd person masculine singular)', '13:37:6': 'form VIII perfect verb (2nd person masculine singular)', '13:37:10': 'form I perfect verb (3rd person masculine singular) + object pronoun (2nd person masculine singular)', '15:7:2': 'form I imperfect verb (2nd person masculine singular) + object pronoun (1st person plural)', '15:7:5': 'form I perfect verb (2nd person masculine singular)', '27:20:3': 'form I perfect verb (3rd person masculine singular)', '27:20:6': 'form IV imperfect verb (1st person singular)', '27:20:9': 'form I perfect verb (3rd person masculine singular)', '36:22:3': 'form I imperfect verb (1st person singular)', '36:22:5': 'form I perfect verb (3rd person masculine singular) + object pronoun (1st person singular)', '36:22:7': 'form I imperfect passive verb (2nd person masculine plural)', '27:20:1': 'form V perfect verb (3rd person masculine singular)', '2:90:1': 'form I perfect verb (3rd person masculine singular) + ما', '2:93:21': 'form I perfect verb (3rd person masculine singular) + ما', '4:58:18': 'form I perfect verb (3rd person masculine singular) + ما', '7:150:9': 'form I perfect verb (3rd person masculine singular) + ما'}
bad=[]
for k,g in protect.items():
 if words.get(k,{}).get("g")!=g: bad.append((k,"grammar",words.get(k,{}).get("g"),g))
for k,w in words.items():
 if "lem/pos/g" in w: bad.append((k,"malformed-key"))
 if w.get("pos")=="V" and not ("verb" in (w.get("g","").lower())):
  bad.append((k,"verb-without-verb-grammar",w.get("g")))
print(f"protected={len(protect)} words={len(words)} failures={len(bad)}")
for x in bad[:30]: print(x)
sys.exit(1 if bad else 0)
