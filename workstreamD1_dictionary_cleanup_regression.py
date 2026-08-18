import json,glob,os,sys
ROOT=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else os.path.dirname(__file__))
protect={'gh-l-f': ['covered'], 'f-kh-r': ['boastful', 'proud'], 'kh-m-t6': ['bitter fruit'], 'z-q-m': ['Zaqqum'], 'w-t-d': ['stakes'], 'th-l-l': ['company', 'multitude']}
bad=[]; roots=0
for p in glob.glob(os.path.join(ROOT,"root","*.json")):
 d=json.load(open(p,encoding="utf-8")); roots+=1
 if d.get("root") in protect and d.get("en")!=protect[d["root"]]:
  bad.append((d.get("root"),"en",d.get("en"),protect[d["root"]]))
 if not d.get("root") or not d.get("root_ar") or "meaning" not in d:
  bad.append((p,"missing-core-field"))
print(f"root_pages={roots} protected={len(protect)} failures={len(bad)}")
for x in bad[:20]: print(x)
sys.exit(1 if bad else 0)
