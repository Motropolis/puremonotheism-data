import json,glob,os,sys,collections
R=os.path.abspath(sys.argv[1]); bad=[]; toks={}; counts=collections.Counter()
for p in glob.glob(os.path.join(R,'surah','*.json')):
 d=json.load(open(p,encoding='utf8'))
 for v in d['verses']:
  for w in v['w']:
   k=f"{v['k']}:{w['i']}"; toks[k]=w
   if w.get('r'): counts[w['r']]+=1
continuative={'2:217:30','5:13:18','9:110:2','11:118:9','13:31:31','21:15:2','22:55:2','40:34:8'}
for k in continuative:
 if toks.get(k,{}).get('r')!='z-y-l': bad.append((k,'expected-z-y-l',toks.get(k,{}).get('r')))
if counts['z-w-l']!=4: bad.append(('z-w-l','count',counts['z-w-l'],4))
if counts['z-y-l']!=10: bad.append(('z-y-l','count',counts['z-y-l'],10))
idx=json.load(open(os.path.join(R,'meta','roots-index.json'),encoding='utf8'))
m={x['r']:x for x in idx['roots']}
if idx.get('count')!=1650: bad.append(('meta-index-count',idx.get('count'),1650))
if 'l-w-t' in m: bad.append(('l-w-t','dangling-active-index-entry'))
for rt,n in [('z-w-l',4),('z-y-l',10)]:
 if m.get(rt,{}).get('n')!=n: bad.append((rt,'meta-index-n',m.get(rt,{}).get('n'),n))
 if json.load(open(os.path.join(R,'root',rt+'.json'),encoding='utf8')).get('count')!=n: bad.append((rt,'root-count'))
 if json.load(open(os.path.join(R,'lexicon',rt+'.json'),encoding='utf8')).get('quran_frequency')!=n: bad.append((rt,'lexicon-frequency'))
print(f"GM14 validation: z-w-l={counts['z-w-l']} z-y-l={counts['z-y-l']} active_roots={idx.get('count')} failures={len(bad)}")
for x in bad: print(x)
sys.exit(1 if bad else 0)
