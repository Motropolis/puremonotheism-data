import json,glob,os,sys
ROOT=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else os.path.dirname(__file__))
bad=[]; words=0; linked=0; prn=0
sur={}
for p in glob.glob(os.path.join(ROOT,"surah","*.json")):
 d=json.load(open(p,encoding="utf-8"))
 for v in d["verses"]:
  for w in v["w"]: sur[f"{v['k']}:{w['i']}"]=w
expect={'1s':'1st person singular','1p':'1st person plural','2ms':'2nd person masculine singular',
'2fs':'2nd person feminine singular','2mp':'2nd person masculine plural','2fp':'2nd person feminine plural',
'2d':'2nd person dual','3ms':'3rd person masculine singular','3fs':'3rd person feminine singular',
'3mp':'3rd person masculine plural','3fp':'3rd person feminine plural','3d':'3rd person dual'}
for p in glob.glob(os.path.join(ROOT,"interlinear","*.json")):
 d=json.load(open(p,encoding="utf-8"))
 for v in d["verses"]:
  for w in v["w"]:
   words+=1; k=f"{v['k']}:{w['i']}"
   kinds=[x for x in ['r','lm','fw','pr','mq'] if w.get(x)]
   if not kinds: bad.append((k,'unlinked'))
   else: linked+=1
   if w.get('pr'):
    prn+=1; code=w['pr'].replace('pron-',''); exp=expect.get(code)
    g=(sur[k].get('g') or '').lower()
    if exp and exp not in g: bad.append((k,'pronoun-feature-mismatch',w['pr'],g))
if sur.get('38:3:8',{}).get('fw')!='l-a-t': bad.append(('38:3:8','missing-lat-link'))
print(f"words={words} linked={linked} pronouns={prn} failures={len(bad)}")
for x in bad[:30]: print(x)
sys.exit(1 if bad else 0)
