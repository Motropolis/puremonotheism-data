# Tahdhib al-Lugha merge — built on v2.9.2

Adds al-Azhari's *Tahdhib al-Lugha* (d. 370/980) as a **seventh** classical
dictionary, sorting second — after Kitab al-Ayn (786), before al-Sihah (1002).
Built on top of published v2.9.2, so both new dictionaries are present.
Replace `lexicon/` only; nothing else is touched.

## Coverage — 1,607 of 1,650 roots (97.4%)

| | roots |
|---|---|
| root-level entry | 1,556 |
| group-level entry | 51 |
| no entry | 43 |

Match routes: exact 1,238 · geminate-2ltr 140 · weak-final-swap 111 ·
weak-mid-swap 37 · weak-final-dropped 18 · reduplicated-2ltr 12.

**The weak-final problem you flagged originally is real here.** Al-Ayn's
edition files weak-final roots with waw, matching the Corpus, so only 23 needed
a swap. Tahdhib files them with alif/ya — `صلو` → `صلى` — and 111 roots needed
the swap. This is the case that silently produced zero matches before.

## `scope` — a new field on this entry only

Al-Azhari treats sets of root permutations together. A chapter opens with an
inventory:

    قول، قيل، قلا، لقا، ليق، يلق، ولق، وقل، (ألق)

and the discussion then runs under whichever permutation carries the material.
Roots named only in the inventory have no entry of their own — `قول` is one,
which matters, since it is among the most frequent roots in the Quran.

Those 51 roots carry `"scope": "group"`, and the headword shows the full
permutation set rather than a single root, so it is visible in the data that
the text is about the group. Root-level entries carry `"scope": "root"`.

**If the UI cannot show that distinction, drop the 51 group entries rather
than presenting them as root entries.** They are honest as labelled and
misleading unlabelled.

A looser recovery heuristic was tried and rejected: it matched ordinary prose
lines and produced 20,351 false attributions, e.g. `قول` bound to a poem about
carnelian. Missing data beats wrong data. The 43 unmatched roots — mostly
hollow roots such as `نور`, `بين`, `ثوب`, `خير` — are listed in
`tahdhib_coverage_report.json` for manual review.

## Source and caveats

`OpenITI/0375AH`, `0370AbuMansurAzhari.TahdhibLugha`, 8 vols, two witnesses;
Shamela0007031 primary, JK007040 adding 26 roots. **Unvocalised**, as al-Ayn is.

Tiered `general`, not `interpretive` — Tahdhib is a general lexicon. But note it
quotes hadith more heavily than al-Ayn does; the salat entry opens with a
prophetic report. If that matters for your purposes, `interpretive` is arguable.

`ATTRIBUTION.md` still unedited. Same OpenITI licence question as al-Ayn.

## One thing worth reading

Al-Azhari's introduction describes his sources as including
*"kitab al-Ayn **attributed to** al-Khalil"* (`كتاب العين المنسوب إلى الخليل`)
— an independent tenth-century witness that the attribution was already
qualified. That is the `earliest-disputed` tier, stated by the earliest critic.
