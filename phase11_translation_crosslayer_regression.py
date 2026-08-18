import json,glob,os,sys,re
ROOT=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else os.path.dirname(__file__))
bad=[]; words={}; verses=set()
for p in glob.glob(os.path.join(ROOT,"surah","*.json")):
 d=json.load(open(p,encoding="utf-8"))
 for v in d["verses"]:
  verses.add(v["k"])
  for w in v["w"]: words[f"{v['k']}:{w['i']}"]=w

# Translation structural coverage.
tdirs=[x for x in glob.glob(os.path.join(ROOT,"translation","*")) if os.path.isdir(x)]
if len(tdirs)!=15: bad.append(("translation-count",len(tdirs)))
for d in tdirs:
 p=os.path.join(d,"all.json")
 if not os.path.exists(p): bad.append((os.path.basename(d),"missing-all")); continue
 x=json.load(open(p,encoding="utf-8")); vs=x.get("verses",{})
 if set(vs)!=verses: bad.append((x.get("slug"),"verse-coverage",len(vs),len(verses)))
 for vk,segs in vs.items():
  text=" ".join(z.get("t","") for z in segs)
  if not text.strip() or "\ufffd" in text: bad.append((x.get("slug"),vk,"bad-text"))

# Interlinear selected gloss parity.
for p in glob.glob(os.path.join(ROOT,"interlinear","*.json")):
 ii=json.load(open(p,encoding="utf-8"))
 for v in ii["verses"]:
  for w in v["w"]:
   k=f"{v['k']}:{w['i']}"; sw=words.get(k,{})
   if w.get("en")!=sw.get("ig") or w.get("r")!=sw.get("r") or w.get("pos")!=sw.get("pos"):
    bad.append((k,"interlinear-parity"))

# Protect representative high-confidence selected gloss repairs.
protect={
"100:1:1":"racers","100:1:2":"panting","100:2:1":"striking sparks","100:4:3":"dust",
"101:1:1":"Striking Calamity","106:1:1":"accustomed security","106:3:1":"worship",
"108:2:3":"sacrifice","112:4:4":"equivalent","18:8:6":"barren","19:84:2":"be impatient",
"20:106:3":"level","20:119:6":"be hot from the sun","20:54:9":"understanding",
"22:29:6":"circumambulate","2:235:8":"proposal","2:233:40":"consultation",
"26:37:3":"skilled magician","27:39:2":"powerful one","28:34:9":"support",
"31:19:3":"pace","32:12:5":"hanging their heads"
}
for k,g in protect.items():
 if words.get(k,{}).get("ig")!=g: bad.append((k,"protected-gloss",words.get(k,{}).get("ig"),g))

# Protect Quran-centric root summaries.
rp={
"m-a-y":"one hundred","r-j-z":"punishment","j-b-r":"tyranny","sh-y-3":"sects",
"s-f-r":"travel","h-w-y":"desire","dh-r-r":"offspring","b-3-th":"resurrect",
"s-kh-r":"mocking","h7-l-l":"lawful","w-k-l":"relying","d-r-j":"degrees"
}
for r,needle in rp.items():
 p=os.path.join(ROOT,"root",r+".json")
 if not os.path.exists(p): bad.append((r,"missing-root")); continue
 m=json.load(open(p,encoding="utf-8")).get("meaning","").lower()
 if needle.lower() not in m: bad.append((r,"root-prose",needle))

print(f"words={len(words)} translations={len(tdirs)} failures={len(bad)}")
for x in bad[:80]: print(x)
sys.exit(1 if bad else 0)
