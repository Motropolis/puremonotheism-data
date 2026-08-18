import json,glob,os,math,re,sys
from collections import Counter
ROOT=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else os.path.dirname(__file__))
bad=[]

# Canonical verse lemma sequences.
seqs={}
for p in glob.glob(os.path.join(ROOT,"surah","*.json")):
    d=json.load(open(p,encoding="utf-8"))
    for v in d["verses"]:
        seqs[v["k"]]=[w.get("lem") for w in v["w"] if w.get("lem")]

# Phrase support and reverse parity.
idx=json.load(open(os.path.join(ROOT,"phrases","index.json"),encoding="utf-8"))
byv=json.load(open(os.path.join(ROOT,"phrases","by-verse.json"),encoding="utf-8"))
pid={}
for ph in idx["phrases"]:
    pid[ph["id"]]=set(ph["verses"])
    ng=ph["lemmas"]
    if ph.get("count")!=len(ph["verses"]):
        bad.append((ph["id"],"phrase-count"))
    for vk in ph["verses"]:
        s=seqs.get(vk,[])
        if not any(s[i:i+len(ng)]==ng for i in range(max(0,len(s)-len(ng)+1))):
            bad.append((ph["id"],vk,"noncontiguous"))
for vk,pids in byv.items():
    for x in pids:
        if x not in pid or vk not in pid[x]: bad.append((vk,x,"bad-reverse"))
for x,vks in pid.items():
    for vk in vks:
        if x not in byv.get(vk,[]): bad.append((x,vk,"missing-reverse"))

# Parallel canonical informative shared count and score.
sets={vk:set(s) for vk,s in seqs.items()}
df=Counter()
for st in sets.values():
    for l in st: df[l]+=1
N=len(sets)
informative={l for l,c in df.items() if c<=1000}
idf={l:math.log((N+1)/(df[l]+1))+1 for l in informative}
norm={vk:math.sqrt(sum(idf[l]**2 for l in st if l in informative)) for vk,st in sets.items()}
for p in glob.glob(os.path.join(ROOT,"parallels","*.json")):
    d=json.load(open(p,encoding="utf-8"))
    for vk,arr in d.items():
        if len(arr)>20: bad.append((vk,"too-many-parallels",len(arr)))
        prev=None
        for rec in arr:
            ov=rec["v"]
            common=(sets.get(vk,set())&sets.get(ov,set()))&informative
            sh=len(common)
            if rec.get("shared")!=sh or sh<2:
                bad.append((vk,ov,"parallel-shared",rec.get("shared"),sh))
                continue
            den=norm.get(vk,0)*norm.get(ov,0)
            score=sum(idf[l]**2 for l in common)/den if den else 0
            if abs(rec.get("score",0)-round(score,3))>0.001:
                bad.append((vk,ov,"parallel-score",rec.get("score"),round(score,3)))
            if score<0.18:
                bad.append((vk,ov,"weak-parallel",score))
            rank=(-rec["score"],-rec["shared"],tuple(map(int,ov.split(":"))))
            if prev is not None and rank<prev:
                bad.append((vk,ov,"parallel-order"))
            prev=rank

# Protect representative root prose corrections.
protect={
"f-l-n":"so-and-so","r-w-d6":"garden","z-h-q":"vanish","h-z-m":"defeat",
"a-y-m":"unmarried","n-f-h7":"slight touch","z-m-l":"wrapped","w-d6-n":"woven",
"j-y-d":"neck","sh-w-k":"armed strength","a-f-l":"set","n-j-w":"secret consultation",
"j-r-m":"criminals","d6-3-f":"weakness","z-k-w":"purification","f-s-q":"rebellion",
"s6-l-w":"prayer","f-t-n":"trial"
}
for r,needle in protect.items():
    p=os.path.join(ROOT,"root",r+".json")
    if not os.path.exists(p): bad.append((r,"missing-root")); continue
    m=json.load(open(p,encoding="utf-8")).get("meaning","").lower()
    if needle.lower() not in m: bad.append((r,"prose-regressed",needle))

print(f"phrases={len(idx['phrases'])} parallel_files={len(glob.glob(os.path.join(ROOT,'parallels','*.json')))} failures={len(bad)}")
for x in bad[:80]: print(x)
sys.exit(1 if bad else 0)
