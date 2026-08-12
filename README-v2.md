# puremonotheism data v2.4.0 — full-dictionary build

## What changed from v1
- Cap removed entirely (`cap: null`). Largest entry: Lane ~108k chars. UI should fold long entries.
- Lane rebuilt from parent+child rows: 3.6→19.9 MB on the Quranic set; 3 false matches fixed (w-n-y, kh-r-b, dh-q-n).
- The old "qamus" table was a MODERN dictionary mislabeled as al-Fayruzabadi (contained الكهرباء, الطائرة...). Replaced with the genuine al-Qamus al-Muhit (OpenITI Shamela0007283, Muassasat al-Risala ed.).
- al-Ayn & Tahdhib re-parsed from OpenITI full texts (segmentation + root matching, narrative openers like قال: excluded).
- Root universe expanded 1,650 → 14,001 (union of 8 dictionaries).

## Layout
- lexicon_full/{slug}.json — one file per root. New fields:
  - quranic: bool; quran_frequency: null for non-Quranic roots
  - classical[].match_type: "root" | "loose" | "loose-wide" (non-exact = flagged for audit)
  - classical[].source: exact digitization provenance
  - lane_match_type: "root" | "subentry" | null
- roots-index-full.json — master index: {r, ar, q, n, d:[dict ids], aliases?}
- browse/alpha-XXXX.json — per-first-letter root lists (28 shards)
- browse/dict-{id}.json — per-dictionary root inventories
- browse/browse-manifest.json
- dictsearch/ds-XXXX.json — token → [root slugs] over ALL dictionary text (31 shards, 337k tokens)
  Client: normalize query (strip diacritics, unify hamza/ya/ta-marbuta), try bare + de-prefixed forms,
  rank exact root-key matches (via roots-index) above text mentions.

## Audit (task 6) — completed
- 118 fake roots deleted (verbal artifacts like يقول/وقول, letter names, ال-prefixed leakage);
  their salvageable dictionary blocks rekeyed to base roots (match_type: "rekeyed").
- ~30 sihah upstream headword typos rekeyed to correct roots (match_type: "rekeyed-typo"),
  incl. بخل, وزغ, حدد, ذيف — several "upstream gaps" turned out to be typo-misfiled entries.
- 9 false loose-tier matches dropped (e.g. خاخ pulling أخ text).
- 60 residual flags marked in-data as "suspect": true (mostly hamza-geminate roots the
  mechanical trace cannot verify, plus Lane cross-reference stubs). audit_flags.json included.

## Known open items
- 12 reduplicated quadriliteral Quranic roots (زلزل etc.) have no root key in any classical dictionary;
  they resolve via loose tier. Alias layer included in index.
- Task 8 singleton verification done: 259 segmentation artifacts (conjugated forms like
  سطاها/بحرت, wa-prefixed entry tails like والكر) reattached to their base roots
  (entries carry "reattached_from"). 2,967 surviving single-source roots — mostly genuine
  rare words and proper nouns in the two largest dictionaries — flagged "s1": true in the
  index so the UI can label them "attested in one dictionary only".
- Task 7 cross-fill done from OpenITI (Lisan Shamela0001687 mARkdown, Sihah Shamela0023235,
  Maqayis Shamela0021710, Mufradat Shamela0023636); entries carry match_type "crossfill-*".
  Residual Quranic gaps: lisan 12, sihah 20, maqayis 22, mufradat 92 — dominated by
  reduplicated quadriliterals these dictionaries file under biliteral headings (covered by
  other dictionaries per root), plus words al-Raghib's selective Mufradat genuinely omits.
- Full false-match audit pending (task 6).


## Test suite (v2.11.4)
build/testsuite.py — 20 integrity + 6 accuracy tests, all passing:
structural schema, index/disk parity, chronological ordering, provenance completeness,
metadata consistency, anachronism scan, truncation, duplicates, encoding, script sanity,
quranic-flag agreement, word-link referential integrity (all 77,430 tokens), occurrence
count consistency, verse-position validity, function-word targets, browse parity,
per-dictionary counts, search round-trip; plus Corpus root agreement (50,266/0 disagree),
root-traceability of entry text, curated proper-noun glosses, death-date correctness,
lemma uncapping, and Quranic-root reachability.

v2.11.4 changes: pruned 244 loose-tier blocks whose text belonged to a DIFFERENT root
(حدح pulling دح, دعد pulling عد, عرجن pulling عرج); 39 untraceable blocks kept but
marked suspect; 22 ellipses verified source-native and marked source_ellipsis;
search index seeded with root keys so every root is findable by its own name;
index/browse rebuilt; 3 remaining proper-noun glosses curated.
