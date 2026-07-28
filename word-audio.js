/**
 * Press-and-hold word audio for puremonotheism.com
 *
 * Plays a single word from ayah-level recitation audio using precise
 * Web Audio scheduling. Handles the four things that reliably break this
 * on mobile: iOS gesture-gating, the native long-press callout, scroll
 * conflicts, and missing segment data.
 *
 * Markup contract:
 *   <span data-word="1:1:3" data-verse="1:1">ٱلرَّحْمَٰنِ</span>
 */

const AUDIO_BASE = 'https://data.puremonotheism.com/audio';
const SEG_BASE = 'https://data.puremonotheism.com/audio/segments';
const RECITER = 'husary';

const HOLD_MS = 350;      // below ~300 fires on taps, above ~500 feels broken
const MOVE_TOL = 10;      // px of finger drift before we treat it as a scroll
const PAD_S = 0.045;      // padding so words don't sound clipped
const FADE_S = 0.015;     // prevents clicks at buffer edges

const ctx = new (window.AudioContext || window.webkitAudioContext)();
const buffers = new Map();
const inflight = new Map();
const segments = new Map();
let currentSource = null;

/* ---------------------------------------------------------------------
 * 1. iOS gesture unlock
 *
 * AudioContext starts suspended and may only be resumed inside a user
 * gesture. A long-press callback fires ~350ms after touchstart and no
 * longer counts as one, so the FIRST touch anywhere in the session has
 * to do the unlocking. Skip this and audio silently never plays on
 * iPhone while working perfectly in desktop testing.
 * ------------------------------------------------------------------ */
let unlocked = false;
function unlock() {
  if (unlocked) return;
  unlocked = true;
  ctx.resume();
  const src = ctx.createBufferSource();
  src.buffer = ctx.createBuffer(1, 1, 22050);
  src.connect(ctx.destination);
  src.start(0);
}
document.addEventListener('touchstart', unlock, { once: true, passive: true });
document.addEventListener('mousedown', unlock, { once: true });

/* ---------------------------------------------------------------------
 * 2. Data loading
 * ------------------------------------------------------------------ */
async function loadSegments(surah) {
  const key = String(surah);
  if (segments.has(key)) return segments.get(key);
  const p = fetch(`${SEG_BASE}/${RECITER}/${String(surah).padStart(3, '0')}.json`)
    .then((r) => r.json())
    .then((j) => { segments.set(key, j); return j; });
  segments.set(key, p);
  return p;
}

async function loadAyah(verseKey) {
  if (buffers.has(verseKey)) return buffers.get(verseKey);
  if (inflight.has(verseKey)) return inflight.get(verseKey);

  const [s, a] = verseKey.split(':');
  const url = `${AUDIO_BASE}/${RECITER}/${s.padStart(3, '0')}${a.padStart(3, '0')}.mp3`;

  const p = fetch(url)
    .then((r) => {
      if (!r.ok) throw new Error(`audio ${r.status} for ${verseKey}`);
      return r.arrayBuffer();
    })
    // callback form: older iOS Safari does not return a promise here
    .then((ab) => new Promise((res, rej) => ctx.decodeAudioData(ab, res, rej)))
    .then((buf) => { buffers.set(verseKey, buf); inflight.delete(verseKey); return buf; })
    .catch((e) => { inflight.delete(verseKey); throw e; });

  inflight.set(verseKey, p);
  return p;
}

/**
 * Warm the cache for verses scrolling into view. Without this, the first
 * long-press on an ayah waits on a full download — Ayat al-Kursi is
 * several hundred KB. With it, every word after the first is instant.
 */
export function prefetchVerse(verseKey) {
  const surah = verseKey.split(':')[0];
  loadSegments(surah).catch(() => {});
  loadAyah(verseKey).catch(() => {});
}

/* ---------------------------------------------------------------------
 * 3. Playback
 * ------------------------------------------------------------------ */
export function stop() {
  if (!currentSource) return;
  try { currentSource.stop(); } catch (_) {}
  currentSource = null;
}

export async function playWord(wordKey) {
  const [s, a, w] = wordKey.split(':');
  const verseKey = `${s}:${a}`;

  const seg = await loadSegments(s);
  const bounds = seg?.verses?.[verseKey]?.w?.[w];

  // Alignment leaves a small number of words unsegmented. Report it so the
  // caller can show a muted state rather than playing the wrong word.
  if (!bounds) return { ok: false, reason: 'no-segment' };

  let buf;
  try {
    buf = await loadAyah(verseKey);
  } catch (_) {
    return { ok: false, reason: 'load-failed' };
  }

  stop();

  const start = Math.max(0, bounds[0] / 1000 - PAD_S);
  const end = Math.min(buf.duration, bounds[1] / 1000 + PAD_S);
  const dur = end - start;
  if (dur <= 0) return { ok: false, reason: 'bad-segment' };

  const src = ctx.createBufferSource();
  const gain = ctx.createGain();
  src.buffer = buf;
  src.connect(gain).connect(ctx.destination);

  const t0 = ctx.currentTime;
  gain.gain.setValueAtTime(0, t0);
  gain.gain.linearRampToValueAtTime(1, t0 + FADE_S);
  gain.gain.setValueAtTime(1, t0 + Math.max(FADE_S, dur - FADE_S));
  gain.gain.linearRampToValueAtTime(0, t0 + dur);

  src.start(t0, start, dur);
  currentSource = src;
  src.onended = () => { if (currentSource === src) currentSource = null; };

  return { ok: true, ms: Math.round(dur * 1000) };
}

/* ---------------------------------------------------------------------
 * 4. Gesture handling
 *
 * A tap opens the root panel. A hold plays audio. The timer distinguishes
 * them, and finger drift cancels — otherwise every scroll through the
 * mushaf triggers playback.
 * ------------------------------------------------------------------ */
let timer = null;
let origin = null;
let target = null;

function clearHold() {
  if (timer) { clearTimeout(timer); timer = null; }
}

function releaseTarget() {
  if (target) target.classList.remove('is-playing');
  target = null;
  origin = null;
}

function onDown(e) {
  const el = e.target.closest('[data-word]');
  if (!el) return;
  const pt = e.touches ? e.touches[0] : e;
  origin = [pt.clientX, pt.clientY];
  target = el;

  timer = setTimeout(async () => {
    timer = null;                     // marks this as a completed hold
    el.classList.add('is-playing');
    if (navigator.vibrate) navigator.vibrate(8);   // Android only; iOS Safari ignores it
    const r = await playWord(el.dataset.word);
    if (!r.ok) {
      el.classList.remove('is-playing');
      el.classList.add('no-audio');
      setTimeout(() => el.classList.remove('no-audio'), 900);
    } else {
      setTimeout(() => el.classList.remove('is-playing'), r.ms + 80);
    }
  }, HOLD_MS);
}

function onMove(e) {
  if (!timer || !origin) return;
  const pt = e.touches ? e.touches[0] : e;
  if (Math.hypot(pt.clientX - origin[0], pt.clientY - origin[1]) > MOVE_TOL) {
    clearHold();
    releaseTarget();
  }
}

function onUp() {
  // timer still pending => released early => this was a tap, not a hold
  if (timer) {
    clearHold();
    if (target) document.dispatchEvent(
      new CustomEvent('word:select', { detail: { word: target.dataset.word } })
    );
    releaseTarget();
  } else {
    origin = null;   // hold already fired; leave is-playing to its own timeout
    target = null;
  }
}

export function attach(root = document) {
  root.addEventListener('touchstart', onDown, { passive: true });
  root.addEventListener('touchmove', onMove, { passive: true });
  root.addEventListener('touchend', onUp);
  root.addEventListener('touchcancel', () => { clearHold(); releaseTarget(); });
  root.addEventListener('mousedown', onDown);
  root.addEventListener('mousemove', onMove);
  root.addEventListener('mouseup', onUp);
  root.addEventListener('mouseleave', () => { clearHold(); releaseTarget(); });

  // Suppress the iOS text-selection callout on held words
  root.addEventListener('contextmenu', (e) => {
    if (e.target.closest('[data-word]')) e.preventDefault();
  });
}

/* Required CSS — without the first rule, iOS shows the magnifier and
   selection handles instead of firing your handler:

   [data-word] {
     -webkit-touch-callout: none;
     -webkit-user-select: none;
     user-select: none;
     touch-action: pan-y;
     cursor: pointer;
   }
   [data-word].is-playing { background: var(--accent-soft); border-radius: 3px; }
   [data-word].no-audio   { opacity: 0.45; }
*/
