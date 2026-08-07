import re, json
P=('0375AH-master/data/0370AbuMansurAzhari/0370AbuMansurAzhari.TahdhibLugha/'
   '0370AbuMansurAzhari.TahdhibLugha.Shamela0007031-ara1')
AR='\u0621-\u064A'
b=open(P,encoding='utf-8').read().split('#META#Header#End#')[-1]
s=re.sub(r'\n#{3,}\s*\|?\s*','\n\x01',b); s=re.sub(r'\n#\s*','\n\x02',s); s=re.sub(r'\n~~\s*',' ',s)
for pat,rep in [(r'PageV\d+P\d+',' '),(r'\bms\d+\b',' '),(r'«\s*\d+\s*»',''),(r'\(\s*\d+\s*\)',''),(r'@[A-Z]+@',' ')]:
    s=re.sub(pat,rep,s)
s=s.replace('[','').replace(']',''); s=re.sub(r'[ \t]+',' ',s)
INV=re.compile(rf'[\x01\x02]\s*\(?\s*((?:[{AR}]{{2,5}}\s*[،,]\s*|\([{AR}]{{2,5}}\)\s*[،,]?\s*){{1,15}}\(?[{AR}]{{2,5}}\)?)\s*\)?\s*[\.:]?\s*(?:مستعمل\S*|يستعمل\S*)?\s*\.?\s*(?=\n)')
primary=json.load(open('tahdhib_entries.json')); groups={}
for m in INV.finditer(s):
    roots=[r.strip('() ') for r in re.split(r'[،,]',m.group(1))]
    roots=[r for r in roots if 2<=len(r)<=5 and re.fullmatch(rf'[{AR}]+',r)]
    if len(roots)<2: continue
    nxt=s.find('\x01',m.end()); body=s[m.end(): nxt if nxt>0 else len(s)]
    body=re.sub(r'\s+',' ',body.replace('\x02',' ').replace('\x01',' ')).strip()
    if len(body)<60: continue
    label='، '.join(roots)
    for r in roots:
        if r not in primary and r not in groups: groups[r]={'headword':label,'text':body}
json.dump(groups,open('tahdhib_groups.json','w'),ensure_ascii=False)
print(f'primary   : {len(primary):,}\ngroup-level: {len(groups):,}')
for p in ['قول','نور','بين','خير']:
    g=groups.get(p); print(f'  {p:5s}',"not recovered" if not g else g['headword'][:34]+' | '+g['text'][:44])
