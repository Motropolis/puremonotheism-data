# PureMonotheism Data Editing Rules

These rules protect the Quran data from regressions.

1. **Canonical token layer first.** Correct a Quran word in `surah/` and its corresponding canonical/interlinear representation deliberately; do not patch only a generated search/browse file.
2. **Never infer one universal root meaning.** Root relationship does not mean every derived word has the same English meaning. Preserve Quranic polysemy.
3. **Contextual glosses are contextual.** A remote Lane/classical dictionary sense must not be promoted into an occurrence gloss merely because it belongs to the same root.
4. **Preserve source material.** Do not rewrite or delete classical source text when the problem is an editorial summary or Quran-context mapping.
5. **Keep provenance.** When replacing curated editorial data, retain the previous value in an appropriate provenance field when practical.
6. **Do not flatten compound morphology.** A token may contain multiple analyzable components. Helper/display links do not always need to be identical across layers.
7. **Do not mechanically NFC-normalize Quranic Arabic.** Quranic combining marks and orthographic sequences are intentionally preserved.
8. **Generated indexes are downstream.** After canonical root/count/link changes, regenerate or reconcile `browse/`, `suggest/`, and `search/`.
9. **Zero-occurrence dictionary roots are not Quran roots.** Dictionary-only material may remain available but must not be advertised as Quran-occurring.
10. **Run validation before release.** Execute `python qa/validate_release.py` from the repository root. A non-zero exit blocks release.
11. **Copyright/licensing is separate.** Do not interpret technical certification as permission to redistribute third-party source material.
