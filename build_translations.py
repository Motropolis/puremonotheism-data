#!/usr/bin/env python3
"""
Convert downloaded editions into the puremonotheism data schema.

Reads the flat {"quran": [{chapter, verse, text}]} format, splits translator
interpolations into marked segments, and writes /translation/{slug}/.
"""

import json
import os
import re
import sys

PATTERNS = [
    ("bracket", re.compile(r"\[([^\[\]]+)\]")),
    ("paren", re.compile(r"\(([^()]+)\)")),
]

EDITIONS = [
    # file, slug, name, translator, year, status, commercial_ok, note
    ("eng-mohammedmarmadu", "pickthall", "The Meaning of the Glorious Koran",
     "Marmaduke Pickthall", 1930, "public-domain", True,
     "Almost literal. Author died 1936; text is public domain."),
    ("eng-yusufaliorig", "yusufali", "The Holy Qur'an",
     "Abdullah Yusuf Ali", 1934, "public-domain", True,
     "Original edition, not the 1946 Al-Rawaf printing or the King Fahd revision. Footnotes excluded."),
    ("eng-themonotheistgr", "monotheist", "The Quran: A Monotheist Translation",
     "The Monotheist Group", 2007, "verify", None,
     "Translated on Quran-alone principles; renders terms from internal usage rather than classical tafsir. Confirm redistribution terms with the publisher."),
    ("eng-shabbirahmed", "shabbirahmed", "The Qur'an As It Explains Itself",
     "Shabbir Ahmed", 2003, "verify", None,
     "Expansive, self-referential method. High word count per verse; much explanatory material is unbracketed and will NOT be caught by segmentation."),
    ("eng-talalitani", "itani", "Quran in English",
     "Talal Itani", 2012, "verify", None,
     "Plain modern English, very low interpolation. Widely described as freely distributable; confirm before shipping."),
    ("eng-georgesale", "sale", "The Koran", "George Sale", 1734,
     "public-domain", True, "Historical interest. Archaic and polemical framing."),
    ("eng-johnmedowsrodwe", "rodwell", "The Koran", "John Medows Rodwell", 1861,
     "public-domain", True, "Historical interest. Reorders surahs in print; this dataset uses standard order."),
    ("eng-edwardhenrypalm", "palmer", "The Qur'an", "Edward Henry Palmer", 1880,
     "public-domain", True, "Historical interest."),
    ("eng-mohammadhabibsh", "shakir", "The Holy Qur'an", "M. H. Shakir", 1980,
     "disputed", None,
     "Copyright status contested; widely alleged to derive from earlier translations. Included for comparison only."),
]


def segment(text):
    spans = []
    for src, pat in PATTERNS:
        for m in pat.finditer(text):
            spans.append((m.start(), m.end(), src))
    if not spans:
        return [{"t": text.strip()}], 0
    spans.sort()
    merged = []
    for s, e, src in spans:
        if merged and s < merged[-1][1]:
            continue
        merged.append((s, e, src))
    out, cursor, n = [], 0, 0
    for s, e, src in merged:
        before = text[cursor:s].strip()
        if before:
            out.append({"t": before})
        inner = text[s + 1:e - 1].strip()
        if inner:
            out.append({"t": inner, "i": True, "src": src})
            n += 1
        cursor = e
    tail = text[cursor:].strip()
    if tail:
        out.append({"t": tail})
    return out, n


def main(srcdir, outdir):
    catalog = []
    print(f"{'slug':<14} {'verses':>7} {'interp':>7} {'per-verse':>10} {'avg words':>10}")
    print("-" * 54)

    for fname, slug, name, translator, year, status, commercial, note in EDITIONS:
        path = os.path.join(srcdir, fname + ".json")
        if not os.path.exists(path):
            print(f"SKIP {slug}: missing {path}", file=sys.stderr)
            continue

        rows = json.load(open(path, encoding="utf-8"))["quran"]
        verses, total_interp, total_words = {}, 0, 0

        for r in rows:
            segs, n = segment(r["text"])
            verses[f"{r['chapter']}:{r['verse']}"] = segs
            total_interp += n
            total_words += len(r["text"].split())

        if len(verses) != 6236:
            print(f"ABORT {slug}: {len(verses)} verses, expected 6236", file=sys.stderr)
            sys.exit(1)

        d = os.path.join(outdir, "translation", slug)
        os.makedirs(d, exist_ok=True)

        with open(os.path.join(d, "all.json"), "w", encoding="utf-8") as fh:
            json.dump({"slug": slug, "segmented": True, "verses": verses},
                      fh, ensure_ascii=False, separators=(",", ":"))

        per_verse = total_interp / 6236
        density = ("very-low" if per_verse < 0.05 else
                   "low" if per_verse < 0.25 else
                   "medium" if per_verse < 0.6 else
                   "high" if per_verse < 1.2 else "very-high")

        meta = {
            "slug": slug, "name": name, "translator": translator, "year": year,
            "language": "en", "status": status, "commercial_ok": commercial,
            "source": "Tanzil Project via fawazahmed0/quran-api",
            "attribution": f"{translator}, {name} ({year}).",
            "verse_count": 6236, "segmented": True,
            "interpolated_spans": total_interp,
            "interpolation_density": density,
            "note": note,
        }
        with open(os.path.join(d, "meta.json"), "w", encoding="utf-8") as fh:
            json.dump(meta, fh, ensure_ascii=False, indent=2)

        catalog.append({k: meta[k] for k in
                        ("slug", "name", "translator", "year", "status",
                         "commercial_ok", "interpolation_density",
                         "interpolated_spans", "note")})

        print(f"{slug:<14} {len(verses):>7} {total_interp:>7} "
              f"{per_verse:>10.3f} {total_words/6236:>10.1f}")

    os.makedirs(os.path.join(outdir, "meta"), exist_ok=True)
    with open(os.path.join(outdir, "meta", "translations.json"), "w", encoding="utf-8") as fh:
        json.dump({"version": "1.0.0", "translations": catalog},
                  fh, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
