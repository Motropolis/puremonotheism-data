# Changelog

## v4.0.1 / GM14 — 2026-08-18

### Regression corrections
- Restored eight continuative `ما زال / لا يزال` tokens from `z-w-l` to `z-y-l`.
- Canonical counts are now `z-w-l = 4` and `z-y-l = 10`.
- Regenerated root, browse, search, suggestion, and interlinear downstream artifacts.
- Regenerated `meta/roots-index.json` from active `root/` files; removed dangling `l-w-t` active-root entry and set active root count to 1,650.
- Added `qa/rebuild_meta_roots_index.py` and made the active root index part of the generated-data rebuild gate.


## RC1 — 2026-08-18

First corpus release candidate after structured technical and linguistic QA.

### Certified
- 77,430 canonical Quran word tokens synchronized across surah/interlinear layers.
- 50,267 root-bearing tokens and 1,650 canonical Quran roots reconciled.
- Root, lemma, function-word, pronoun, muqattaʿat, dictionary and generated-index links audited.
- Contextual gloss, morphology, dictionary-summary, polysemy, count, ID, encoding, duplicate/orphan and generated-index audits completed.
- Invisible Unicode search-key controls removed.
- Stale browse/suggestion counts synchronized.
- Dead Quran-root suggestions removed.
- Empty lexicon summaries repaired.
- Final adversarial QA and corpus certification passed with zero blocking failures.

### Deferred
- Copyright, licensing and redistribution-rights review.
