#!/usr/bin/env python3
import json,glob,os,sys,unicodedata,collections
ROOT=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else os.path.join(os.path.dirname(__file__),'..'))
bad=[]; sur={}; inter={}; verses=set()
for folder,target in [('surah',sur),('interlinear',inter)]:
 files=sorted(glob.glob(os.path.join(ROOT,folder,'*.json')))
 if len(files)!=114: bad.append((folder,'file-count',len(files),114))
 for p in files:
  try: d=json.load(open(p,encoding='utf-8'))
  except Exception as e: bad.append((p,'json-parse',str(e))); continue
  for v in d.get('verses',[]):
   if folder=='surah': verses.add(v.get('k'))
   for exp,w in enumerate(v.get('w',[]),1):
    k=f"{v.get('k')}:{w.get('i')}"
    if w.get('i')!=exp: bad.append((k,folder,'word-order'))
    if k in target: bad.append((k,folder,'duplicate-token'))
    target[k]=w
    if not isinstance(w.get('ar'),str) or not w.get('ar','').strip(): bad.append((k,folder,'empty-ar'))
if set(sur)!=set(inter): bad.append(('token-key-parity',len(set(sur)^set(inter))))
actual=collections.Counter(w['r'] for w in sur.values() if w.get('r'))
roots={os.path.splitext(os.path.basename(p))[0]:p for p in glob.glob(os.path.join(ROOT,'root','*.json'))}
lex={os.path.splitext(os.path.basename(p))[0] for p in glob.glob(os.path.join(ROOT,'lexicon','*.json'))}
for rt,n in actual.items():
 if rt not in roots: bad.append((rt,'missing-root'))
 else:
  d=json.load(open(roots[rt],encoding='utf-8'))
  if d.get('count')!=n: bad.append((rt,'root-count',d.get('count'),n))
 if rt not in lex: bad.append((rt,'missing-lexicon'))
for p in glob.glob(os.path.join(ROOT,'lexicon','*.json')):
 d=json.load(open(p,encoding='utf-8'))
 if 'summary' in d and isinstance(d['summary'],str) and not d['summary'].strip(): bad.append((p,'empty-summary'))
for p in glob.glob(os.path.join(ROOT,'search','*.json')):
 d=json.load(open(p,encoding='utf-8'))
 for k in d:
  if any(unicodedata.category(c)=='Cf' for c in k): bad.append((p,'format-control-search-key',repr(k)))
zero={rt for rt,p in roots.items() if json.load(open(p,encoding='utf-8')).get('count')==0}
for p in glob.glob(os.path.join(ROOT,'suggest','*.json')):
 for x in json.load(open(p,encoding='utf-8')):
  if x.get('t')=='r' and x.get('r') in zero: bad.append((p,'zero-count-root-suggestion',x['r']))
print(f"PureMonotheism release validation: verses={len(verses)} words={len(sur)} roots={len(actual)} failures={len(bad)}")
for x in bad[:50]: print('FAIL',x)
sys.exit(1 if bad else 0)
