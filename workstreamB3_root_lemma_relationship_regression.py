import json,glob,os,sys,collections
ROOT=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else os.path.dirname(__file__))
lemma_roots=collections.defaultdict(set); pairs=collections.Counter(); words=0
for p in glob.glob(os.path.join(ROOT,"surah","*.json")):
 d=json.load(open(p,encoding="utf-8"))
 for v in d["verses"]:
  for w in v["w"]:
   words+=1
   if w.get("r") and w.get("lem"):
    lemma_roots[w["lem"]].add(w["r"]); pairs[(w["r"],w["lem"])]+=1
bad=[]
for lem,roots in lemma_roots.items():
 if len(roots)>1: bad.append((lem,"multi-root",sorted(roots)))
for pair,c in pairs.items():
 if c<1: bad.append((pair,"empty-pair"))
print(f"words={words} root_lemma_pairs={len(pairs)} lemma_labels={len(lemma_roots)} failures={len(bad)}")
for x in bad[:20]: print(x)
sys.exit(1 if bad else 0)
