import json,glob,os,sys,collections
ROOT=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else os.path.join(os.path.dirname(__file__),'..'))
bad=[]; rb=0; freq=collections.Counter()
for p in glob.glob(os.path.join(ROOT,'surah','*.json')):
 d=json.load(open(p,encoding='utf-8'))
 for v in d['verses']:
  for w in v['w']:
   if w.get('lem'): freq[w['lem']]+=1
   if w.get('r'):
    rb+=1
    if not w.get('lem'): bad.append((v['k'],w['i'],'root-without-lemma',w['r']))
anchors={'رَحْمَة':114,'شَيْطان':88,'آدَم':25,'عِيسَى':25,'حَياة':76,'رَجُل':29,'امْرَأَت':26,'جَنَّة':147,'جَهَنَّم':77,'إِيمان':45,'كُفْر':37,'غَنِيّ':24,'فَقِير':12,'بَحْر':41,'بَرّ':22,'زَكاة':32,'بَرَكَة':3,'إِنسان':71,'إِبْلِيس':11,'شَهْر':21}
for lem,n in anchors.items():
 if freq[lem]!=n: bad.append((lem,'independent-frequency-anchor',freq[lem],n))
print(f"GM2 validation: root_bearing_tokens={rb} anchors={len(anchors)} failures={len(bad)}")
for x in bad[:50]: print(x)
sys.exit(1 if bad else 0)
