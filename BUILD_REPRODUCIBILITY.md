# Build Reproducibility

## Gold Master GM12 status

Deterministic builders now exist for `root/`, `interlinear/`, `browse/`, `search/`, and `suggest/`.

Run all builders:

```bash
python qa/rebuild_generated.py .
```

Check for drift without writing:

```bash
python qa/rebuild_generated.py . --check
```

`interlinear/` is derived from `surah/` plus the versioned `gold_master/GM12_INTERLINEAR_OVERRIDES.json` sidecar, which preserves presentation/provenance and intentional compound-link exceptions. Arabic search is generated from Quran surface forms, lemmas, roots and documented normalization. English search is generated from the checked-in translations.

Remaining generated layers without complete first-principles builders are `parallels/`, `dictsearch/`, and portions of `lexicon/`/`lemma/`. The raw Arabic bootstrap still depends on third-party upstream inputs and remains outside a fully self-contained build until licensing/source packaging is addressed.
