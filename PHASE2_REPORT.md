# PureMonotheism Data — Phase 2 Morphology, Grammar, Lemma & Root Review

## Status
Phase 2 audit and high-confidence correction pass completed on the Phase 1 corrected baseline.

This pass deliberately does not mass-rewrite disputed morphology or generated root meanings. Confirmed defects were corrected; unresolved upstream annotation weaknesses were converted into explicit review queues.

## Confirmed corrections applied

### Grammar indexes
The reverse grammar indexes were not complete relative to the word-level `g` field.

Before correction:
- `grammar/person.json` omitted the `1st` category entirely despite 323 tokens explicitly carrying 1st-person grammar.
- 706 explicit 2nd-person tokens and 2,266 explicit 3rd-person tokens were omitted from the person index, primarily pronouns.
- `grammar/number.json` omitted 181 explicit plural, 159 singular, and 24 dual tokens.
- `grammar/gender.json` omitted 17 explicit masculine tokens.

The three indexes were regenerated directly from the canonical word-level grammar strings.

After correction:
- gender masculine: 36,589 / 36,589 indexed
- gender feminine: 6,553 / 6,553
- number plural: 14,340 / 14,340
- number singular: 14,627 / 14,627
- number dual: 353 / 353
- person 1st: 323 / 323
- person 2nd: 5,258 / 5,258
- person 3rd: 14,560 / 14,560
- reverse-index mismatches: 0

### Confirmed lemma correction
`2:16:7` had lemma `رَبِحَت`, an inflected 3fs surface-form lemma. It was normalized to canonical verbal lemma `رَبِحَ` in the surah data and root forms.

### Root meaning corrections
Thirteen root summaries were corrected after comparison with the classical dictionary material already bundled in the repository:

- أيي
- قنع
- عذب
- قصم
- نتق
- عزل
- كوب
- جثم
- صفو
- نبأ
- نسو
- لعن
- صرط

These included demonstrable wrong-sense summaries such as:
- أيي incorrectly summarized as `اسم` (“name”)
- قصم summarized as a plant rather than breaking/crushing
- نتق summarized as an inn rather than pulling/shaking/uprooting
- عزل summarized by a water-bag spout instead of separation/withdrawal
- كوب summarized by games/drums while the Quranic form is `أكواب`, cups
- نسو summarized as the sciatic nerve instead of the women lexical family
- صرط containing a later bridge-over-Hell description in a lexical data field

Each corrected root now has `meaning_review_status: phase2-reviewed` and a `meaning_source` note.

## New unresolved review queues

### Verb lemma normalization
`phase2_lemma_review.json`

- 460 token occurrences remain whose verb lemma ends in an inflectional `ت` pattern.
- 129 unique lemma strings are involved.

This is a real upstream weakness: the morphology source itself documents that lemmas need further review and gives the same `ربحت -> ربح` class as an example. These records are queued, not automatically rewritten, because weak verbs, passive forms, derived forms and orthographic changes make blind suffix stripping unsafe.

### Root-assignment ambiguities
`phase2_root_assignment_ambiguities.json`

Six lemma strings occur under more than one root assignment. These are not automatically errors; several are genuine homograph/derivational questions. Each occurrence is listed for scholarly adjudication.

### Root meaning quality
`phase2_meaning_review.json`

297 root summaries remain as automated review candidates because their English meaning text has no lexical overlap with the root's Quran co-occurrence glosses. This heuristic intentionally over-flags. It is a review queue, not a claim that all 297 are wrong.

The scan nevertheless proved that the generated `meaning` layer cannot yet be treated as fully reviewed scholarly data. Only 36 of the original 1,651 roots carried any `meaning_source` metadata before this pass.

## External morphology verification limitation

The repository's A1 test expects the `mustafa0x/quran-morphology` file. That file was not bundled in the uploaded repository and could not be fetched by the local shell environment, so the full 50k+ root-assignment comparison could not be re-executed locally in this pass.

The upstream project itself states that its lemmas still need substantial review, noun-form marking is incomplete, and some POS/person/gender/number annotations have known limitations. Therefore the external dataset should be treated as a comparison source, not infallible ground truth.

## Validation after changes

- Integrity suite: 20/20 PASS
- Runnable accuracy tests: 15/15 PASS
- External A1 comparison: SKIP because reference file unavailable
- Layer tests: 9/9 PASS
- Grammar reverse-index parity added manually: 0 mismatches in all regenerated gender/number/person categories

## Phase 2 conclusion

The technical Phase 2 scan is complete, and all high-confidence defects found in this pass have been corrected. However, Phase 2 has uncovered a deeper lemma/meaning review workload that should not be falsely marked resolved:

- 460 verb-token lemma candidates / 129 unique lemmas
- 6 multi-root lemma ambiguities
- 297 root meaning review candidates

These queues are now explicit machine-readable files and should be worked down to zero or verified-exception status before the linguistic layer is called final.
