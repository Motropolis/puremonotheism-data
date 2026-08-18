# PureMonotheism Phase 1 Dictionary Adjudication

## Result

- Quranic suspect blocks reviewed: **104**
- False-positive/legitimate associations cleared: **90**
- Entire wrong blocks removed: **8**
- Mixed blocks pruned at entry level: **6**
- Reviewed `filed_under` metadata added where needed: **82**
- Remaining Quranic `suspect` blocks: **0**

## Entire blocks removed
- **وري / qamus**: Article is الورة/ورور, not Quranic وري; no relevant وري lexical article.
- **اخو / qamus**: Article is الأخيخة/interjection أخ and does not define Quranic أخو sibling lexeme.
- **امو / qamus**: Entries are أم/أمه under أمم-type material, not the أمو root of أمة (bondwoman).
- **دمو / qamus**: Article is دمه/دمم (smearing/leveling), not دمو blood.
- **هدهد / maqayis**: Subentry contains no هدهد material; attached only through loose reduplicative filing.
- **هدهد / lisan**: Subentry contains no هدهد material; attached to هدد without a هدهد lexical entry.
- **عتو / qamus**: Article is عته/عتعت and only incidental عتى=حتى; not Quranic عتو haughtiness.
- **زيد / tahdhib**: Parsed Tahdhib block is corrupted/misaligned: زيد entry begins with unrelated حلق material and contains neighboring زود/زأد entries.

## Mixed blocks pruned
- **زود / tahdhib**: Kept ['زود']; removed ['زيد', 'زاد', 'زد']
- **ضان / sihah**: Kept ['ضأن']; removed ['ضون']
- **سوع / sihah**: Kept ['سوع']; removed ['سيع']
- **سوا / mufradat**: Kept ['سوأ']; removed ['سوا']
- **جزا / sihah**: Kept ['جزى']; removed ['جزأ']
- **سوي / mufradat**: Kept ['سوا']; removed ['سوأ']

## Validation after correction

- Integrity suite: **20/20 PASS**
- Accuracy suite: **15 runnable tests PASS; A1 external Quranic Corpus comparison SKIPPED because the reference morphology file is not bundled and outbound shell network is unavailable**
- Layer suite: **9/9 PASS**
- A7 wrong-root blocks: **0**
- A8 unrelated-root article collisions: **0**
- A9 wrong Lane blocks: **0**

## Notes

The source transcription itself was not rewritten merely to make a headword look cleaner. Where a classical dictionary legitimately files material under a derived or alternate heading, the relationship is represented through reviewed `filed_under` metadata instead. This preserves provenance while allowing the validator to distinguish legitimate filing conventions from actual cross-root contamination.
