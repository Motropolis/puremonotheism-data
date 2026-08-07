import json,re,glob,os
SRC='/tmp/t292/puremonotheism-data-2.9.2/lexicon'; OUT='out2/lexicon'
prim=json.load(open('tahdhib_entries.json')); grp=json.load(open('tahdhib_groups.json'))
os.makedirs(OUT,exist_ok=True)
def norm(s):
    s=re.sub(r'[\u064B-\u0652\u0670\u0640]','',s)
    for a,b in [('أ','ا'),('إ','ا'),('آ','ا'),('ؤ','و'),('ئ','ي'),('ء','ا'),('ى','ي'),('ة','ه')]: s=s.replace(a,b)
    return s
idx={}
for k in prim: idx.setdefault(norm(k),[]).append(k)
gidx={}
for k in grp: gidx.setdefault(norm(k),[]).append(k)
WEAK=['و','ي','ا','ء']
def cands(r0):
    out=[(r0,'exact')]; r=norm(r0)
    if r!=r0: out.append((r,'exact'))
    if len(r)==3:
        if r[1]==r[2]: out.append((r[:2],'geminate-2ltr'))
        if r[2] in 'وياي':
            for w in WEAK:
                if w!=r[2]: out.append((r[:2]+w,'weak-final-swap'))
            out.append((r[:2],'weak-final-dropped'))
        if r[1] in 'وياي':
            for w in WEAK:
                if w!=r[1]: out.append((r[0]+w+r[2],'weak-mid-swap'))
    if len(r)==4 and r[:2]==r[2:]: out.append((r[:2],'reduplicated-2ltr'))
    return out
NOTE=("Arabic-only entries from public-domain classical lexica, ordered by compiler death date. "
 "Tier 'root-semantic' (Maqayis) derives all senses of a root from one core idea. Tier 'interpretive' "
 "(Mufradat) cites hadith and takes theological positions and is not equivalent evidence. Tier "
 "'earliest-disputed' (Kitab al-Ayn) marks a text whose attribution to al-Khalil ibn Ahmad (d. 786) is "
 "contested: the work records that his student al-Layth ibn al-Muzaffar completed it after his death, so "
 "the 786 date orders the entry but does not assert sole authorship. Tahdhib al-Lugha (al-Azhari, d. 980) "
 "is the earliest critical assessment of that text; al-Azhari himself calls it 'kitab al-Ayn attributed to "
 "al-Khalil'. Some Tahdhib entries are group-level: al-Azhari treats a set of root permutations together, "
 "and where a root has no entry of its own the headword shows the full permutation set. Compilation: "
 "wizsk/arabic_lexicons, GPL-3.0. Kitab al-Ayn and Tahdhib al-Lugha: OpenITI — LICENCE NOT CLEARED.")
rep={'root_level':0,'group_level':0,'unmatched':[],'routes':{}}
files=sorted(glob.glob(f'{SRC}/*.json'))
for f in files:
    d=json.load(open(f)); rar=d['root_ar']; ents=None; lvl=None
    for c,why in cands(rar):
        n=norm(c)
        if n in idx:
            ents=[{'headword':r,'text':prim[r]} for r in idx[n]]; lvl='root'; rep['routes'][why]=rep['routes'].get(why,0)+1; break
    if not ents:
        for c,why in cands(rar):
            n=norm(c)
            if n in gidx:
                ents=[{'headword':grp[r]['headword'],'text':grp[r]['text']} for r in gidx[n]]; lvl='group'; break
    if ents:
        d['classical']=[e for e in d['classical'] if e.get('id')!='tahdhib']
        d['classical'].append({'id':'tahdhib','name':'Tahdhib al-Lugha','name_ar':'تهذيب اللغة',
            'compiler':'al-Azhari','died':980,'tier':'general',
            'scope':'group' if lvl=='group' else 'root','entries':ents})
        d['classical'].sort(key=lambda e:e['died'])
        rep['root_level' if lvl=='root' else 'group_level']+=1
    else: rep['unmatched'].append({'root':d['root'],'root_ar':rar})
    d['classical_note']=NOTE
    json.dump(d,open(os.path.join(OUT,os.path.basename(f)),'w'),ensure_ascii=False)
tot=rep['root_level']+rep['group_level']
print(f"files          : {len(files):,}")
print(f"with Tahdhib   : {tot:,}  ({100*tot/len(files):.1f}%)")
print(f"  root-level   : {rep['root_level']:,}")
print(f"  group-level  : {rep['group_level']:,}")
print(f"without        : {len(rep['unmatched']):,}")
print('routes:', dict(sorted(rep['routes'].items(),key=lambda x:-x[1])))
json.dump(rep,open('out2/tahdhib_coverage_report.json','w'),ensure_ascii=False,indent=2)
