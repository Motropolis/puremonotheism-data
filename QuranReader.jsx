import React, { useEffect, useMemo, useRef, useState } from "react";

const BASE = "https://cdn.jsdelivr.net/gh/Motropolis/puremonotheism-data@V1.0.0";

/* Themes. Each accent is drawn from its own surface rather than bolted on:
   ink-blue on white, burnt sienna on sepia, low-glow brass on black. */
const THEMES = {
  paper: {
    label: "Paper",
    bg: "#FFFFFF", panel: "#F4F3F0", raised: "#FFFFFF",
    ink: "#16161A", muted: "#6E6D77", faint: "#9B9AA3",
    rule: "#E6E5E1", accent: "#2F4A7D", accentSoft: "#E8EDF6",
  },
  sepia: {
    label: "Sepia",
    bg: "#F4ECD8", panel: "#EADFC2", raised: "#F9F3E4",
    ink: "#332818", muted: "#6F5F45", faint: "#95866B",
    rule: "#DCCFAE", accent: "#8A4F26", accentSoft: "#E7D6BC",
  },
  night: {
    label: "Night",
    bg: "#0D0E11", panel: "#171920", raised: "#1D2029",
    ink: "#E9E7E1", muted: "#8F8E99", faint: "#65646E",
    rule: "#252832", accent: "#C9A45C", accentSoft: "#221E17",
  },
};

const TRANSLATIONS = [
  { slug: "monotheist", label: "The Monotheist Group", year: 2007 },
  { slug: "pickthall", label: "Pickthall", year: 1930 },
  { slug: "yusufali", label: "Yusuf Ali", year: 1934 },
  { slug: "itani", label: "Talal Itani", year: 2012 },
  { slug: "shabbirahmed", label: "Shabbir Ahmed", year: 2003 },
  { slug: "shakir", label: "Shakir", year: 1980 },
  { slug: "palmer", label: "Palmer", year: 1880 },
  { slug: "rodwell", label: "Rodwell", year: 1861 },
  { slug: "sale", label: "George Sale", year: 1734 },
];

/* Settings persistence degrades to in-memory if storage is unavailable. */
const store = {
  get(k, fallback) {
    try {
      const v = window.localStorage.getItem("pm." + k);
      return v === null ? fallback : JSON.parse(v);
    } catch { return fallback; }
  },
  set(k, v) {
    try { window.localStorage.setItem("pm." + k, JSON.stringify(v)); } catch {}
  },
};

function useFonts() {
  useEffect(() => {
    const id = "pm-fonts";
    if (document.getElementById(id)) return;
    const l = document.createElement("link");
    l.id = id;
    l.rel = "stylesheet";
    l.href =
      "https://fonts.googleapis.com/css2?family=Amiri+Quran&family=Literata:ital,opsz,wght@0,7..72,400;0,7..72,500;1,7..72,400&display=swap";
    document.head.appendChild(l);
  }, []);
}

export default function QuranReader() {
  useFonts();

  const [themeKey, setThemeKey] = useState(() => store.get("theme", "paper"));
  const [transSlug, setTransSlug] = useState(() => store.get("trans", "pickthall"));
  const [surahId, setSurahId] = useState(() => store.get("surah", 1));
  const [arSize, setArSize] = useState(() => store.get("arSize", 30));
  const [enSize, setEnSize] = useState(() => store.get("enSize", 17));
  const [showAdds, setShowAdds] = useState(() => store.get("adds", false));

  const [surahs, setSurahs] = useState(null);
  const [verses, setVerses] = useState(null);
  const [trans, setTrans] = useState(null);
  const [loadingTrans, setLoadingTrans] = useState(false);
  const [error, setError] = useState(null);
  const [sheet, setSheet] = useState(null); // 'surah' | 'settings' | null

  const t = THEMES[themeKey];
  const transCache = useRef(new Map());
  const scrollRef = useRef(null);

  useEffect(() => { store.set("theme", themeKey); }, [themeKey]);
  useEffect(() => { store.set("trans", transSlug); }, [transSlug]);
  useEffect(() => { store.set("surah", surahId); }, [surahId]);
  useEffect(() => { store.set("arSize", arSize); }, [arSize]);
  useEffect(() => { store.set("enSize", enSize); }, [enSize]);
  useEffect(() => { store.set("adds", showAdds); }, [showAdds]);

  useEffect(() => {
    fetch(`${BASE}/meta/surahs.json`)
      .then((r) => r.json())
      .then((d) => setSurahs(d.surahs))
      .catch(() => setError("Couldn't load the surah list. Check your connection and reload."));
  }, []);

  useEffect(() => {
    setVerses(null);
    fetch(`${BASE}/surah/${String(surahId).padStart(3, "0")}.json`)
      .then((r) => r.json())
      .then((d) => setVerses(d.verses))
      .catch(() => setError("Couldn't load this surah. Try another, or reload."));
    if (scrollRef.current) scrollRef.current.scrollTo({ top: 0 });
  }, [surahId]);

  useEffect(() => {
    const cached = transCache.current.get(transSlug);
    if (cached) { setTrans(cached); return; }
    setLoadingTrans(true);
    fetch(`${BASE}/translation/${transSlug}/all.json`)
      .then((r) => r.json())
      .then((d) => {
        transCache.current.set(transSlug, d.verses);
        setTrans(d.verses);
      })
      .catch(() => setError("Couldn't load that translation. Pick another."))
      .finally(() => setLoadingTrans(false));
  }, [transSlug]);

  const surah = useMemo(
    () => surahs?.find((s) => s.id === surahId),
    [surahs, surahId]
  );
  const transMeta = TRANSLATIONS.find((x) => x.slug === transSlug);

  const S = {
    page: {
      minHeight: "100vh", background: t.bg, color: t.ink,
      fontFamily: "'Literata', Georgia, serif",
      transition: "background 200ms ease, color 200ms ease",
      WebkitTapHighlightColor: "transparent",
    },
    bar: {
      position: "sticky", top: 0, zIndex: 20,
      display: "flex", alignItems: "center", gap: 8,
      padding: "10px 12px",
      background: t.bg, borderBottom: `1px solid ${t.rule}`,
      backdropFilter: "saturate(180%) blur(8px)",
    },
    barBtn: {
      flex: 1, minWidth: 0, textAlign: "left",
      background: "transparent", border: "none", color: t.ink,
      padding: "6px 4px", cursor: "pointer", font: "inherit",
    },
    icon: {
      flexShrink: 0, width: 40, height: 40, borderRadius: 10,
      display: "grid", placeItems: "center",
      background: t.panel, color: t.ink, border: `1px solid ${t.rule}`,
      cursor: "pointer", fontSize: 15, fontWeight: 500,
      fontFamily: "system-ui, sans-serif",
    },
    scroll: { padding: "8px 16px 96px", maxWidth: 720, margin: "0 auto" },
    verse: { padding: "22px 0", borderBottom: `1px solid ${t.rule}` },
    vnum: {
      fontFamily: "ui-monospace, SFMono-Regular, Menlo, monospace",
      fontSize: 11, letterSpacing: "0.06em", color: t.accent,
      marginBottom: 14, display: "inline-block",
      padding: "2px 8px", borderRadius: 999,
      background: t.accentSoft,
    },
    arabic: {
      fontFamily: "'Amiri Quran', serif",
      direction: "rtl", textAlign: "right",
      fontSize: arSize, lineHeight: 2.15, color: t.ink,
      marginBottom: 16, wordSpacing: "0.06em",
    },
    english: { fontSize: enSize, lineHeight: 1.75, color: t.muted },
    add: {
      color: t.faint,
      borderBottom: `1px dotted ${t.faint}`,
      paddingBottom: 1,
    },
    sheetWrap: {
      position: "fixed", inset: 0, zIndex: 50,
      background: "rgba(0,0,0,0.45)",
      display: "flex", alignItems: "flex-end",
    },
    sheet: {
      width: "100%", maxHeight: "82vh", overflowY: "auto",
      background: t.raised, borderTop: `1px solid ${t.rule}`,
      borderRadius: "18px 18px 0 0", padding: "10px 0 28px",
      boxShadow: "0 -8px 40px rgba(0,0,0,0.18)",
    },
    grab: {
      width: 38, height: 4, borderRadius: 2, background: t.rule,
      margin: "6px auto 14px",
    },
    sheetH: {
      fontFamily: "system-ui, sans-serif", fontSize: 12, fontWeight: 500,
      letterSpacing: "0.07em", textTransform: "uppercase", color: t.faint,
      padding: "16px 20px 8px",
    },
    row: {
      display: "flex", alignItems: "center", justifyContent: "space-between",
      gap: 12, padding: "13px 20px", background: "transparent",
      border: "none", width: "100%", cursor: "pointer",
      color: t.ink, font: "inherit", textAlign: "left",
      fontFamily: "system-ui, sans-serif", fontSize: 15,
    },
    seg: {
      display: "flex", gap: 6, padding: "4px 20px 8px",
    },
    segBtn: (on) => ({
      flex: 1, padding: "11px 8px", borderRadius: 10, cursor: "pointer",
      fontFamily: "system-ui, sans-serif", fontSize: 14, fontWeight: 500,
      background: on ? t.accent : t.panel,
      color: on ? (themeKey === "night" ? "#141414" : "#FFFFFF") : t.muted,
      border: `1px solid ${on ? t.accent : t.rule}`,
      transition: "background 150ms ease",
    }),
    toggle: (on) => ({
      width: 46, height: 27, borderRadius: 999, flexShrink: 0,
      background: on ? t.accent : t.rule,
      position: "relative", transition: "background 180ms ease",
    }),
    knob: (on) => ({
      position: "absolute", top: 3, left: on ? 22 : 3,
      width: 21, height: 21, borderRadius: "50%", background: "#fff",
      transition: "left 180ms cubic-bezier(.4,0,.2,1)",
      boxShadow: "0 1px 3px rgba(0,0,0,0.28)",
    }),
  };

  if (error) {
    return (
      <div style={{ ...S.page, display: "grid", placeItems: "center", padding: 32 }}>
        <div style={{ textAlign: "center", maxWidth: 340 }}>
          <p style={{ fontSize: 16, marginBottom: 16 }}>{error}</p>
          <button style={{ ...S.icon, width: "auto", padding: "10px 18px" }}
                  onClick={() => window.location.reload()}>
            Reload
          </button>
        </div>
      </div>
    );
  }

  return (
    <div style={S.page}>
      <header style={S.bar}>
        <button style={S.icon} onClick={() => setSurahId((n) => Math.max(1, n - 1))}
                disabled={surahId === 1} aria-label="Previous surah">‹</button>

        <button style={S.barBtn} onClick={() => setSheet("surah")}>
          <div style={{
            fontFamily: "system-ui, sans-serif", fontSize: 16, fontWeight: 500,
            whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis",
          }}>
            {surah ? `${surah.translit}` : "Loading"}
            <span style={{ color: t.faint, fontWeight: 400 }}> ▾</span>
          </div>
          <div style={{ fontSize: 12, color: t.faint, fontFamily: "system-ui, sans-serif" }}>
            {surah ? `${surah.name_en} · ${surah.verses} verses` : "\u00A0"}
          </div>
        </button>

        <button style={S.icon} onClick={() => setSurahId((n) => Math.min(114, n + 1))}
                disabled={surahId === 114} aria-label="Next surah">›</button>
        <button style={S.icon} onClick={() => setSheet("settings")} aria-label="Reading settings">Aa</button>
      </header>

      <main ref={scrollRef} style={S.scroll}>
        {surah && (
          <div style={{ textAlign: "center", padding: "26px 0 10px" }}>
            <div style={{ fontFamily: "'Amiri Quran', serif", fontSize: 27, marginBottom: 8 }}>
              {surah.name_ar}
            </div>
            <div style={{ fontSize: 12, color: t.faint, fontFamily: "system-ui, sans-serif",
                          letterSpacing: "0.08em", textTransform: "uppercase" }}>
              Surah {surah.id}
            </div>
          </div>
        )}

        {!verses && <Skeleton t={t} />}

        {verses?.map((v) => (
          <article key={v.k} style={S.verse}>
            <div style={S.vnum}>{v.k}</div>
            <div style={S.arabic}>{v.ar}</div>
            <div style={S.english}>
              {loadingTrans && !trans ? (
                <span style={{ color: t.faint }}>Loading translation…</span>
              ) : (
                renderTranslation(trans?.[v.k], showAdds, S.add)
              )}
            </div>
          </article>
        ))}
      </main>

      {sheet === "surah" && (
        <SurahSheet t={t} S={S} surahs={surahs} current={surahId}
                    onPick={(id) => { setSurahId(id); setSheet(null); }}
                    onClose={() => setSheet(null)} />
      )}

      {sheet === "settings" && (
        <div style={S.sheetWrap} onClick={() => setSheet(null)}>
          <div style={S.sheet} onClick={(e) => e.stopPropagation()}>
            <div style={S.grab} />

            <div style={S.sheetH}>Theme</div>
            <div style={S.seg}>
              {Object.entries(THEMES).map(([k, v]) => (
                <button key={k} style={S.segBtn(k === themeKey)} onClick={() => setThemeKey(k)}>
                  {v.label}
                </button>
              ))}
            </div>

            <div style={S.sheetH}>Translation</div>
            {TRANSLATIONS.map((x) => (
              <button key={x.slug} style={S.row} onClick={() => setTransSlug(x.slug)}>
                <span>
                  {x.label}
                  <span style={{ color: t.faint, fontSize: 13 }}> · {x.year}</span>
                </span>
                {x.slug === transSlug && <span style={{ color: t.accent }}>✓</span>}
              </button>
            ))}

            <div style={S.sheetH}>Translator additions</div>
            <button style={S.row} onClick={() => setShowAdds((v) => !v)}>
              <span style={{ paddingRight: 8 }}>
                Show translator additions
                <span style={{ display: "block", fontSize: 12, color: t.faint, marginTop: 3,
                               lineHeight: 1.45, fontFamily: "system-ui, sans-serif" }}>
                  Words the translator supplied that have no counterpart in the Arabic.
                </span>
              </span>
              <span style={S.toggle(showAdds)}><span style={S.knob(showAdds)} /></span>
            </button>

            <div style={S.sheetH}>Arabic size</div>
            <Slider t={t} min={22} max={46} value={arSize} onChange={setArSize} />

            <div style={S.sheetH}>Translation size</div>
            <Slider t={t} min={14} max={24} value={enSize} onChange={setEnSize} />

            <div style={{ padding: "18px 20px 0", fontSize: 11, lineHeight: 1.6,
                          color: t.faint, fontFamily: "system-ui, sans-serif" }}>
              Arabic text: Tanzil Project. Translation: {transMeta?.label}, {transMeta?.year}.
              Translation is interpretation; the Arabic is the text.
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

/* Renders segmented translation. Interpolated spans are dropped entirely when
   the toggle is off — the whole point is reading without them. */
function renderTranslation(segs, showAdds, addStyle) {
  if (!segs) return null;
  const parts = showAdds ? segs : segs.filter((s) => !s.i);
  return parts.map((s, i) => (
    <span key={i} style={s.i ? addStyle : undefined}>
      {s.t}
      {i < parts.length - 1 ? " " : ""}
    </span>
  ));
}

function Slider({ t, min, max, value, onChange }) {
  return (
    <div style={{ padding: "2px 20px 10px", display: "flex", alignItems: "center", gap: 12 }}>
      <input type="range" min={min} max={max} value={value}
             onChange={(e) => onChange(Number(e.target.value))}
             style={{ flex: 1, accentColor: t.accent }} />
      <span style={{ fontFamily: "ui-monospace, monospace", fontSize: 12,
                     color: t.faint, width: 26, textAlign: "right" }}>{value}</span>
    </div>
  );
}

function SurahSheet({ t, S, surahs, current, onPick, onClose }) {
  const [q, setQ] = useState("");
  const list = (surahs || []).filter((s) => {
    const n = q.trim().toLowerCase();
    if (!n) return true;
    return String(s.id) === n || s.translit.toLowerCase().includes(n) ||
           s.name_en.toLowerCase().includes(n);
  });
  return (
    <div style={S.sheetWrap} onClick={onClose}>
      <div style={S.sheet} onClick={(e) => e.stopPropagation()}>
        <div style={S.grab} />
        <div style={{ padding: "0 16px 10px" }}>
          <input value={q} onChange={(e) => setQ(e.target.value)}
                 placeholder="Find a surah by name or number"
                 style={{
                   width: "100%", padding: "12px 14px", borderRadius: 10,
                   border: `1px solid ${t.rule}`, background: t.panel, color: t.ink,
                   fontFamily: "system-ui, sans-serif", fontSize: 15, outline: "none",
                 }} />
        </div>
        {list.map((s) => (
          <button key={s.id} style={S.row} onClick={() => onPick(s.id)}>
            <span style={{ display: "flex", gap: 12, alignItems: "baseline", minWidth: 0 }}>
              <span style={{ fontFamily: "ui-monospace, monospace", fontSize: 12,
                             color: t.faint, width: 24, flexShrink: 0 }}>{s.id}</span>
              <span style={{ minWidth: 0 }}>
                {s.translit}
                <span style={{ display: "block", fontSize: 12, color: t.faint }}>{s.name_en}</span>
              </span>
            </span>
            <span style={{ fontFamily: "'Amiri Quran', serif", fontSize: 17,
                           color: s.id === current ? t.accent : t.muted }}>
              {s.name_ar?.replace("سُوْرَةُ ", "")}
            </span>
          </button>
        ))}
        {list.length === 0 && (
          <div style={{ padding: "24px 20px", color: t.faint,
                        fontFamily: "system-ui, sans-serif", fontSize: 14 }}>
            No surah matches that. Try a number from 1 to 114.
          </div>
        )}
      </div>
    </div>
  );
}

function Skeleton({ t }) {
  return (
    <div style={{ padding: "20px 0" }}>
      {[0, 1, 2].map((i) => (
        <div key={i} style={{ marginBottom: 34 }}>
          <div style={{ height: 12, width: 52, background: t.panel, borderRadius: 999, marginBottom: 16 }} />
          <div style={{ height: 22, background: t.panel, borderRadius: 5, marginBottom: 10 }} />
          <div style={{ height: 22, background: t.panel, borderRadius: 5, width: "72%", marginLeft: "28%" }} />
        </div>
      ))}
    </div>
  );
}
