# puremonotheism.com — static data layer

Read-only reference corpus. Served from a CDN, never stored in Base44 entities.
Base44 holds only user-generated data (accounts, notes, bookmarks, posts, threads).

## Directory layout

```
/data
  /meta
    surahs.json            114 surah records, ~12 KB
    roots-index.json       ~1,651 roots for search + autocomplete, ~120 KB
  /surah
    001.json … 114.json    Arabic text + word-by-word morphology
  /root
    ktb.json … (per root)  Pre-built concordance. ONE fetch renders the page.
  /lexicon
    ktb.json … (per root)  Lane's entry, split by sense, with authorities
  /translation
    /{slug}/all.json       verse key -> string, one file per translation
    /{slug}/meta.json      translator, license, attribution string
```

## Key conventions

| Type | Format | Example |
|---|---|---|
| Verse key | `surah:ayah` | `2:255` |
| Word key | `surah:ayah:word` | `2:255:4` |
| Root key | Latin transliteration, no vowels | `ktb`, `slm`, `Alh` |

Root keys are ASCII so they work as filenames and URL segments. Keep a single
canonical mapping from the Corpus Buckwalter roots to these keys in the build
script, and never regenerate it by hand.

---

## /meta/surahs.json

```json
{
  "version": "1.0.0",
  "surahs": [
    {
      "id": 1,
      "name_ar": "الفاتحة",
      "name_en": "The Opening",
      "translit": "Al-Fatihah",
      "verses": 7,
      "order_revealed": 5
    }
  ]
}
```

Deliberately omits the Meccan/Medinan label. That classification comes from
outside the text; if you include it, mark it as external in the UI.

---

## /surah/{nnn}.json

One file per surah. Largest is Al-Baqarah at roughly 400 KB uncompressed,
well under 100 KB gzipped.

```json
{
  "id": 1,
  "verses": [
    {
      "k": "1:1",
      "ar": "بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ",
      "w": [
        {
          "i": 1,
          "ar": "بِسْمِ",
          "tr": "bis'mi",
          "r": "smw",
          "lem": "ism",
          "pos": "N",
          "seg": "P+N",
          "g": "in the name"
        }
      ]
    }
  ]
}
```

Field notes:

- `r` is null for particles and most proper nouns. The UI must handle a
  missing root without breaking the click target.
- `g` is the Corpus word-by-word gloss, not a translation. Label it as such
  in the UI or users will read it as one.
- `seg` preserves the Corpus segmentation (prefix+stem+suffix) so you can
  render clitics separately from the stem.

---

## /root/{key}.json — the concordance file

This is the file that makes the core interaction one request. Everything
needed to render a root page is inlined, including the verse text for
context. No second round trip.

```json
{
  "root": "ktb",
  "root_ar": "ك ت ب",
  "count": 319,
  "forms": [
    {
      "lem": "kitab",
      "ar": "كِتَٰب",
      "pos": "N",
      "g": "book, writ, decree",
      "count": 230,
      "occ": [0, 1, 2]
    },
    {
      "lem": "kataba",
      "ar": "كَتَبَ",
      "pos": "V",
      "form": "I",
      "g": "he wrote, he prescribed",
      "count": 39,
      "occ": [3]
    }
  ],
  "occ": [
    {
      "k": "2:2:2",
      "v": "2:2",
      "ar": "ٱلْكِتَٰبُ",
      "vt": "ذَٰلِكَ ٱلْكِتَٰبُ لَا رَيْبَ ۛ فِيهِ"
    }
  ],
  "lexicon": "ktb"
}
```

`forms[].occ` holds integer indices into the flat `occ` array, so each
occurrence is stored once no matter how many groupings reference it.
The UI groups by derived form using those indices — that grouping is the
whole point of root-first reading.

`occ[].vt` is the full verse Arabic. Translations are NOT inlined; the client
pulls them from the translation map by verse key. That keeps root files
translation-agnostic and licensing clean.

Largest root files (`Alh`, `qwl`, `rbb`) run 200–400 KB uncompressed. If any
exceed 500 KB, shard as `{key}.0.json`, `{key}.1.json` and list the shards in
a `parts` field.

---

## /lexicon/{key}.json

Lane's entry for the same root key, so a root page needs at most two fetches
and they can fire in parallel.

```json
{
  "root": "ktb",
  "root_ar": "ك ت ب",
  "entries": [
    {
      "headword": "كَتَبَ",
      "vol": 7,
      "page": 2589,
      "senses": [
        {
          "n": 1,
          "text": "He wrote, or inscribed…",
          "authorities": ["S", "M", "K"]
        }
      ]
    }
  ],
  "attribution": "Edward William Lane, An Arabic-English Lexicon (1863-93). Digital text from the Perseus Digital Library, Tufts University, CC BY-SA 3.0 US."
}
```

**`authorities` is the field that matters most for your project.** Lane does
not supply his own definitions — he translates them from medieval Arabic
dictionaries and records which one gave which sense. Those abbreviations
(S = al-Sihah, M = al-Muhkam, K = al-Qamus, Msb = al-Misbah, T = Tahdhib)
are the provenance trail. Surface them in the UI as a hoverable chip on each
sense so a reader can see exactly which authority backs a gloss and weigh it
themselves. No other Quran site does this, and for a Quran-alone project it
converts your biggest methodological objection into a visible feature.

Parsing these out of the Perseus XML is the single fiddliest part of the
build. Budget real time for it, and ship without `authorities` populated
rather than delaying phase one — the field can fill in later.

---

## Translations

Nine English translations, all 6,236 verses, all segmented. Interpolation
counts are measured, not estimated — they come from the build script.

| Slug | Translator | Year | Status | Bracketed spans | Per verse |
|---|---|---|---|---|---|
| `monotheist` | The Monotheist Group | 2007 | verify | **0** | 0.000 |
| `itani` | Talal Itani | 2012 | verify | **0** | 0.000 |
| `sale` | George Sale | 1734 | public domain | 11 | 0.002 |
| `rodwell` | J. M. Rodwell | 1861 | public domain | 140 | 0.022 |
| `palmer` | E. H. Palmer | 1880 | public domain | 269 | 0.043 |
| `shakir` | M. H. Shakir | 1980 | disputed | 2,064 | 0.331 |
| `pickthall` | Marmaduke Pickthall | 1930 | public domain | 2,973 | 0.477 |
| `shabbirahmed` | Shabbir Ahmed | 2003 | verify | 3,959 | 0.635 |
| `yusufali` | Abdullah Yusuf Ali | 1934 | public domain | 5,313 | 0.852 |

### Reading the table

`monotheist` and `itani` contain no bracketed content anywhere. Verified by
scanning all 6,236 verses for `(` and `[` — both return zero. This is a genuine
property of those translations, not a stripped source.

The Monotheist Group edition is the one worth a close look. It was translated
on Quran-alone principles, deriving term meanings from internal Quranic usage
rather than classical commentary. For this project that is a closer
methodological match than anything else on the list, and it happens to be free
of interpolation as well.

**But it is `verify` status, not public domain.** Confirm redistribution terms
with the publisher before shipping it. Same for `itani` and `shabbirahmed`.

`pickthall` and `yusufali` are the safe defaults — unambiguously public domain,
ship today, no correspondence required.

### A caveat the table cannot show

Segmentation finds bracketed spans. It cannot find interpretation woven into
the main clause without punctuation. `shabbirahmed` averages 32.9 words per
verse against 22-25 for the others; that extra third is explanatory material
carried inline where no parser will catch it. A zero in the interpolation
column means "no bracketing convention", not "no interpretation".

Label the reader toggle **"translator additions"**, never "hide tafsir". And
state plainly on the sources page that translation is interpretation and the
Arabic is the text.

### File shape

`/translation/{slug}/all.json` — flat verse-key map, roughly 850 KB to 1.4 MB.
Fetch once, cache in memory, reuse across reader and concordance views.

```json
{
  "slug": "pickthall",
  "segmented": true,
  "verses": {
    "2:2": [
      { "t": "This is the Scripture whereof there is no doubt, a guidance unto those who ward off" },
      { "t": "evil", "i": true, "src": "paren" }
    ]
  }
}
```

Segments with `i: true` had no counterpart in the Arabic. `src` records whether
the span came from parentheses or square brackets — some translators use
brackets for grammatical necessity and parentheses for commentary, so keep the
distinction even if the UI ignores it initially.

`/translation/{slug}/meta.json` carries translator, year, status, measured
interpolation count, and the attribution string. Render attribution in the UI.

---

## Required attribution

These are license conditions, not courtesies. Put them in a persistent
footer or an /about/sources page.

- **Arabic text** — Tanzil Project, CC BY-ND. Distributed unmodified.
- **Morphology** — Quranic Arabic Corpus v0.4, © 2011 Kais Dukes, GNU GPL.
  The license requires the source be clearly indicated **and** a link made
  to http://corpus.quran.com so users can track changes. The link is
  mandatory. The license also states verbatim copies may be distributed but
  changing the file is not allowed — if you adopt a corrected fork, document
  that you have done so and what changed.
- **Lexicon** — Lane, public domain; Perseus digital text CC BY-SA 3.0 US.
  Share-alike attaches to the derived text.

---

## Build pipeline

A one-time script, run locally, output committed as versioned files:

1. Parse `quranic-corpus-morphology-0.4.txt` into word records.
2. Join against Tanzil Uthmani text on verse key. Assert 6,236 verses and
   77,430 words before continuing — a silent join failure here corrupts
   every downstream file.
3. Emit `/surah/*.json`.
4. Invert the word records by root, emit `/root/*.json`.
5. Parse Lane XML, key by root, emit `/lexicon/*.json`.
6. Emit `/meta/*.json` and per-translation maps.
7. Gzip everything, verify no file exceeds 500 KB, publish under a version tag.

Never edit the output by hand. Fix the script and re-run, or the corpus and
the concordance will drift apart.

---

## Audio layer

```
/audio
  /{reciter}/001001.mp3 … 114006.mp3     6,236 ayah files
  /segments/{reciter}/001.json … 114.json  word timestamps, ms
  /segments/{reciter}/meta.json            reciter, reading, source, license
```

Segment file shape:

```json
{
  "reciter": "husary",
  "reading": "Hafs an Asim",
  "surah": 1,
  "verses": {
    "1:1": { "d": 5980, "w": { "1": [340, 980], "2": [1040, 1720] } }
  }
}
```

`d` is total ayah duration in ms. `w` maps word index to `[start_ms, end_ms]`.
A word index may be **absent** — alignment does not resolve every word. Treat a
missing entry as "no audio for this word" and show a muted state. Never fall
back to playing the neighbouring segment.

Word indices here must match `w[].i` in the surah files exactly. Add an
assertion to the build script comparing word counts per verse across the two
sources; a one-word drift silently shifts audio for the rest of the ayah and is
very hard to spot by ear.

Store reciter and reading in `meta.json` and display them. Recitation reaches
us through named transmission chains rather than from the text itself, so for a
Quran-alone project the honest framing is that audio is a pronunciation aid
with a stated provenance, not an authority. Same principle as the lexicon
`authorities` field — label the source and let the reader weigh it.

### Storage estimate

At 64 kbps mono, 6,236 ayah files run roughly 1.5-2 GB per reciter. Cloudflare
R2's free tier covers a single reciter comfortably; budget for the second.
Serve with a long `Cache-Control` and immutable version paths — these files
never change.
