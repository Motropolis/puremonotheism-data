#!/usr/bin/env python3
"""
Generate /surah/001.json .. /surah/114.json and /meta/surahs.json
from the Uthmani text, the simple (search) text, and chapter metadata.

Morphology roots are NOT attached here. Words carry an index and the
Uthmani form so tap targets and audio segments work immediately; the
root/lemma fields get filled in by the Corpus pass later.
"""

import json
import os
import re
import sys
import unicodedata

# Arabic diacritics and Quranic annotation marks, stripped for the search field
MARKS = re.compile(r"[\u0610-\u061A\u064B-\u065F\u0670\u06D6-\u06ED\u08D3-\u08FF]")
TATWEEL = "\u0640"


def normalize(text):
    """Fold to a diacritic-free, alef-normalized form for substring search."""
    t = MARKS.sub("", text).replace(TATWEEL, "")
    t = re.sub(r"[\u0622\u0623\u0625\u0671]", "\u0627", t)   # alef variants
    t = t.replace("\u0629", "\u0647")                        # ta marbuta
    t = re.sub(r"[\u0649]", "\u064A", t)                     # alef maqsura
    t = unicodedata.normalize("NFC", t)
    return re.sub(r"\s+", " ", t).strip()


def main(srcdir, outdir):
    uth = json.load(open(os.path.join(srcdir, "ara-quranuthmanihaf.json"), encoding="utf-8"))["quran"]
    smp = json.load(open(os.path.join(srcdir, "ara-quransimple.json"), encoding="utf-8"))["quran"]
    info = json.load(open(os.path.join(srcdir, "..", "m_info.json"), encoding="utf-8"))

    if len(uth) != 6236 or len(smp) != 6236:
        sys.exit(f"ABORT: {len(uth)} / {len(smp)} verses, expected 6236 each")

    simple = {(r["chapter"], r["verse"]): r["text"] for r in smp}

    by_surah = {}
    total_words = 0
    for r in uth:
        c, v = r["chapter"], r["verse"]
        text = r["text"].strip()
        words = [w for w in re.split(r"\s+", text) if w]
        total_words += len(words)
        by_surah.setdefault(c, []).append({
            "k": f"{c}:{v}",
            "ar": text,
            "s": normalize(simple.get((c, v), text)),
            "w": [{"i": i + 1, "ar": w} for i, w in enumerate(words)],
        })

    if len(by_surah) != 114:
        sys.exit(f"ABORT: {len(by_surah)} surahs, expected 114")

    os.makedirs(os.path.join(outdir, "surah"), exist_ok=True)
    for c in sorted(by_surah):
        with open(os.path.join(outdir, "surah", f"{c:03d}.json"), "w", encoding="utf-8") as fh:
            json.dump({"id": c, "verses": by_surah[c]}, fh,
                      ensure_ascii=False, separators=(",", ":"))

    chapters = []
    for ch in info["chapters"]:
        c = ch["chapter"]
        chapters.append({
            "id": c,
            "name_ar": ch.get("arabicname", ""),
            "name_en": ch.get("englishname", ""),
            "translit": ch.get("name", ""),
            "verses": len(by_surah[c]),
        })

    if len(chapters) != 114:
        sys.exit(f"ABORT: {len(chapters)} chapter records")

    os.makedirs(os.path.join(outdir, "meta"), exist_ok=True)
    with open(os.path.join(outdir, "meta", "surahs.json"), "w", encoding="utf-8") as fh:
        json.dump({"version": "1.1.0", "surahs": chapters}, fh,
                  ensure_ascii=False, indent=1)

    print(f"114 surah files, 6236 verses, {total_words} words (space-split)")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
