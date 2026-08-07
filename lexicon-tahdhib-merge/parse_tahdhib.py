#!/usr/bin/env python3
"""Extract root -> text from Tahdhib al-Lugha (al-Azhari, d. 370/980)."""
import re, json, os

D = '0375AH-master/data/0370AbuMansurAzhari/0370AbuMansurAzhari.TahdhibLugha'
AR = '\u0621-\u064A'
WITNESSES = [('shamela', '0370AbuMansurAzhari.TahdhibLugha.Shamela0007031-ara1'),
             ('jk',      '0370AbuMansurAzhari.TahdhibLugha.JK007040-ara1')]

# words that end in ':' but are discourse markers, not headwords
STOP = set("""قال وقال قلت وقلت يقال ويقال أي أى وأي ومنه منه وقيل قيل
أخبرنا حدثنا أنشد وأنشد ثعلب أبو وأبو الليث وقال الله عمرو زيد سلمة وروى روى شمر وشمر الفراء أحمد محمد أنشدني قوله وقوله يعني منها وهو وهي
غيره وغيره أراد وأراد تقول وتقول قال أبو وفي وفى وذلك يريد
الأصمعي معناه ومعناه الواحد والجمع وجمعه جمعه""".split())

HEAD_COMMA = re.compile(
    rf'(?:\x02\s*|\x01\s*|\.\s+|\n)((?:[{AR}]{{2,5}}\s*[،,]\s*){{0,15}}[{AR}]{{2,5}})\s*:\s')
HEAD_PAREN = re.compile(
    rf'(?:\x02\s*|\x01\s*|\.\s+|\n)\(\s*((?:[{AR}]{{2,5}}[ ،,]+){{0,15}}[{AR}]{{2,5}})\s*\)\s*:\s')

def parse(path):
    b = open(path, encoding='utf-8').read().split('#META#Header#End#')[-1]
    s = b
    s = re.sub(r'\n#{3,}\s*\|?\s*', '\n\x01', s)
    s = re.sub(r'\n#\s*', '\n\x02', s)
    s = re.sub(r'\n~~\s*', ' ', s)
    s = re.sub(r'PageV\d+P\d+', ' ', s)
    s = re.sub(r'\bms\d+\b', ' ', s)
    s = re.sub(r'«\s*\d+\s*»', '', s)
    s = re.sub(r'\(\s*\d+\s*\)', '', s)
    s = re.sub(r'@[A-Z]+@', ' ', s)
    s = s.replace('[', '').replace(']', '')
    s = re.sub(r'[ \t]+', ' ', s)

    out = {}
    marks = []
    found = list(HEAD_COMMA.finditer(s)) + list(HEAD_PAREN.finditer(s))
    for m in sorted(found, key=lambda x: x.start()):
        head = m.group(1)
        roots = [r.strip() for r in re.split(r'[،, ]+', head) if r.strip()]
        if any(r in STOP for r in roots):      # discourse marker, not a headword
            continue
        if marks and m.start(1) <= marks[-1][1]:
            continue
        marks.append((m.start(1), m.end(), roots))

    for i, (st, en, roots) in enumerate(marks):
        stop = marks[i + 1][0] if i + 1 < len(marks) else len(s)
        txt = s[en:stop].replace('\x01', ' ').replace('\x02', ' ')
        txt = re.sub(r'\s+', ' ', txt).strip()
        txt = re.sub(rf'(?:[{AR}]{{2,5}}\s*[،,]\s*)*[{AR}]{{2,5}}$', '', txt).strip()
        if len(txt) < 15 or txt.startswith('(مستعمل'):
            continue
        for r in roots:
            if 2 <= len(r) <= 5:
                out.setdefault(r, []).append(txt)
    return {r: ' '.join(v) for r, v in out.items()}


merged, prov = {}, {}
for name, fn in WITNESSES:
    p = os.path.join(D, fn)
    if not os.path.exists(p):
        continue
    got = parse(p)
    new = sum(1 for r in got if r not in merged)
    for r, v in got.items():
        merged.setdefault(r, v); prov.setdefault(r, name)
    print(f'{name:8s} roots={len(got):6,}  new={new:6,}  cumulative={len(merged):6,}')

json.dump(merged, open('tahdhib_entries.json', 'w'), ensure_ascii=False)
print(f'\nTOTAL roots {len(merged):,}   text {sum(len(v) for v in merged.values()):,} chars')
for p in ['صلو', 'رحم', 'رب', 'أله', 'خشع', 'حمد', 'قرأ', 'كفر']:
    v = merged.get(p)
    print(f'  {p:5s} {"MISS" if not v else v[:70]}')
