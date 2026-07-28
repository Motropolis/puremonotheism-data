# puremonotheism-data

Static reference corpus for puremonotheism.com. Served from a CDN, never
stored in the app database.

**Live base URL:** `https://cdn.jsdelivr.net/gh/USERNAME/puremonotheism-data@v1.0.0/`

## What's here

| Path | Contents | Status |
|---|---|---|
| `/translation/{slug}/` | 9 English translations, 6,236 verses each, segmented | **complete** |
| `/meta/` | Surah list (114), root index, translation catalog | surahs complete |
| `/surah/` | Arabic Uthmani text, word-split, + search field | **complete** |
| `/root/` | Pre-built root concordance | sample |
| `/lexicon/` | Lane's Lexicon keyed by root | sample |
| `/audio/` | Ayah recitation + word timestamps | deferred |

Files marked *sample* carry a `_sample` key and show the intended shape. Run
the build pipeline in `SCHEMA.md` to populate them.

## Rules

1. **Never hand-edit generated files.** Fix the build script and re-run.
2. **Tag every release.** jsDelivr serves `@v1.0.0` immutably; `@main` is not
   safe to depend on and defeats caching.
3. **Check `status` before shipping a translation.** `public-domain` is free to
   use. `verify` and `disputed` are not cleared.

## Regenerating translations

```bash
mkdir -p /tmp/src && cd /tmp/src
BASE="https://raw.githubusercontent.com/fawazahmed0/quran-api/1/editions"
for e in eng-mohammedmarmadu eng-yusufaliorig eng-themonotheistgr \
         eng-shabbirahmed eng-talalitani eng-georgesale \
         eng-johnmedowsrodwe eng-edwardhenrypalm eng-mohammadhabibsh; do
  curl -sSL -o "$e.json" "$BASE/$e.json"
done

python3 build_translations.py /tmp/src .
```

The script aborts if any edition does not parse to exactly 6,236 verses.

See `SCHEMA.md` for full file formats and `ATTRIBUTION.md` for licence terms.
