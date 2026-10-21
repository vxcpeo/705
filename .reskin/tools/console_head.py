"""Replace the top of console.css with the Abyss Console token + shell layer."""
from __future__ import annotations

from pathlib import Path

CSS = Path(r"E:\workspace\chuangye\solana\705\website\src\console.css")
text = CSS.read_text(encoding="utf-8")
marker = "/* --------------------------------------------------------------- typography */"
index = text.index(marker)
tail = text[index:]

head = """/* Pretiola — Abyss Console.
 *
 * A dense terminal console: black ground, one red signal accent, a status strip,
 * a command line and three panes (commands, data, readout). Linear, not spatial.
 *
 * Rules of this system:
 *   1. The ground is the abyss; surfaces are thin lines over it, never slabs.
 *   2. Type is a console: Trebuchet display, Segoe body, mono for every label.
 *   3. Depth comes from hairlines and one soft accent glow, never from shadows.
 *   4. Every route is a command line followed by a pane deck.
 *   5. Navigation is a command rail of numbered commands, not a floating dock.
 */

/* ----------------------------------------------------------------- tokens */
:root {
  color-scheme: dark;

  /* ground */
  --bg: #000000;
  --bg-2: #05080c;
  --surface: #0d141b;
  --surface-2: #111a24;
  --surface-3: #182533;

  /* ink */
  --ink: #F4F7FA;
  --ink-2: #D7DDE4;
  --muted: #9FB1C1;
  --faint: #8698A9;

  /* signal */
  --accent: #ff0000;
  --accent-safe: #ff5f5f;
  --accent-2: #ff00c8;
  --success: #5CE1A0;
  --danger: #FF7A7A;
  --warning: #F2C94C;

  /* lines */
  --line: #1E2A36;
  --line-2: #2A3B4C;
  --glow: 0 0 60px rgba(255, 0, 0, 0.12);

  /* shape */
  --radius-pill: 999px;
  --radius-xs: 6px;
  --radius-sm: 10px;
  --radius-md: 16px;
  --radius-lg: 24px;

  /* type */
  --font-display: 'Trebuchet MS', 'Segoe UI', sans-serif;
  --font-body: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
  --font-mono: 'Cascadia Mono', ui-monospace, Consolas, 'SFMono-Regular', monospace;
  --track-label: 0.14em;

  /* motion */
  --motion: 240ms;
  --ease: cubic-bezier(.22, 1, .36, 1);

  /* metrics */
  --gutter: clamp(14px, 2.6vw, 34px);
  --max-w: 1500px;
  --strip-h: 30px;
  --rail-w: 212px;
}

* { box-sizing: border-box; }

html {
  min-width: 320px;
  background: var(--bg);
  scroll-behavior: smooth;
  -webkit-text-size-adjust: 100%;
}

body {
  margin: 0;
  min-width: 320px;
  background-color: var(--bg);
  color: var(--ink);
  font: 400 15px/1.6 var(--font-body);
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
}

/* a fine console grid, painted behind everything; no stars, no nebula */
body::before {
  content: '';
  position: fixed;
  inset: 0;
  z-index: 0;
  pointer-events: none;
  background-image:
    linear-gradient(rgba(143, 163, 181, 0.045) 1px, transparent 1px),
    linear-gradient(90deg, rgba(143, 163, 181, 0.045) 1px, transparent 1px);
  background-size: 48px 48px, 48px 48px;
  mask-image: linear-gradient(180deg, rgba(0, 0, 0, 0.9), rgba(0, 0, 0, 0.2));
}

button, input, textarea, select { font: inherit; color: inherit; }
a { color: inherit; }
img { display: block; max-width: 100%; }
output { font-variant-numeric: tabular-nums; }
svg { display: block; }

:focus-visible {
  outline: 2px solid var(--accent-safe);
  outline-offset: 3px;
  border-radius: 2px;
}

::selection { background: var(--accent); color: #050608; }

/* Screen-reader utility. The clip technique keeps a real 1x1 box, which the
   accessibility tooling and the layout both rely on. */
.vh {
  position: absolute !important;
  width: 1px !important;
  height: 1px !important;
  padding: 0 !important;
  margin: -1px !important;
  overflow: hidden !important;
  clip: rect(0, 0, 0, 0) !important;
  clip-path: inset(50%) !important;
  white-space: nowrap !important;
  border: 0 !important;
}

.tty-skip {
  position: fixed;
  z-index: 200;
  top: 0;
  left: 0;
  transform: translateY(-160%);
  padding: 10px 18px;
  background: var(--accent);
  color: #050608;
  font: 600 11px/1 var(--font-mono);
  letter-spacing: var(--track-label);
  text-transform: uppercase;
  text-decoration: none;
}
.tty-skip:focus-visible { transform: none; }

/* ----------------------------------------------------------- console shell */
.tty-frame {
  position: relative;
  z-index: 1;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.tty-console {
  flex: 1 1 auto;
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: var(--max-w);
  margin-inline: auto;
  min-width: 0;
  border-inline: 1px solid var(--line);
}

/* status strip: the top line of the console, 30px of facts */
.tty-status {
  position: sticky;
  top: 0;
  z-index: 60;
  display: grid;
  grid-template-columns: auto minmax(0, 1fr) auto;
  align-items: center;
  gap: 20px;
  min-height: var(--strip-h);
  padding: 0 var(--gutter);
  border-bottom: 1px solid var(--line);
  background: rgba(0, 0, 0, 0.88);
  backdrop-filter: blur(18px);
  color: var(--muted);
  font: 500 10px/1.3 var(--font-mono);
  letter-spacing: 0.11em;
  text-transform: uppercase;
}

.tty-status-brand {
  display: inline-flex;
  align-items: center;
  gap: 9px;
  color: var(--ink);
  text-decoration: none;
  letter-spacing: 0.06em;
}
.tty-status-brand img { width: 18px; height: 18px; }

.tty-status-cells {
  display: flex;
  align-items: center;
  gap: 18px;
  min-width: 0;
  overflow: hidden;
  white-space: nowrap;
}
.tty-status-cell { display: inline-flex; align-items: center; gap: 6px; flex: none; }
.tty-status-cell i {
  width: 6px;
  height: 6px;
  background: var(--success);
}
.tty-status-cell b { color: var(--ink); font-weight: 500; letter-spacing: 0.04em; }
.tty-status-tail {
  color: var(--faint);
  text-align: right;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* command line: route title, prompt and the console actions */
.tty-command {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  align-items: center;
  gap: 16px;
  padding: 10px var(--gutter);
  border-bottom: 1px solid var(--line);
  background: linear-gradient(90deg, rgba(255, 0, 0, 0.05), transparent 42%);
}
.tty-command-line { display: flex; align-items: baseline; gap: 10px; min-width: 0; }
.tty-prompt {
  color: var(--accent-safe);
  font: 600 14px/1 var(--font-mono);
}
.tty-command-title {
  margin: 0;
  font: 650 clamp(15px, 1.2vw, 19px)/1.25 var(--font-display);
  letter-spacing: -0.02em;
  color: var(--ink);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.tty-command-actions { display: flex; align-items: center; gap: 8px; }
.tty-command-more {
  display: none;
  place-items: center;
  width: 38px;
  height: 38px;
  border: 1px solid var(--line-2);
  border-radius: var(--radius-sm);
  background: var(--surface);
  color: var(--ink);
  cursor: pointer;
}
.tty-command-more[aria-expanded='true'] {
  border-color: var(--accent);
  color: var(--accent-safe);
}

/* the deck: command rail plus the data stage */
.tty-deck {
  flex: 1 1 auto;
  display: grid;
  grid-template-columns: var(--rail-w) minmax(0, 1fr);
  align-items: stretch;
  min-height: 0;
}

.tty-nav {
  display: flex;
  flex-direction: column;
  gap: 2px;
  padding: 12px 10px;
  border-right: 1px solid var(--line);
  background: rgba(13, 20, 27, 0.5);
}
.tty-nav-label {
  margin: 0 0 6px;
  padding: 0 8px;
  color: var(--faint);
  font: 500 9px/1.4 var(--font-mono);
  letter-spacing: 0.18em;
  text-transform: uppercase;
}
.tty-nav-link {
  display: grid;
  grid-template-columns: 24px minmax(0, 1fr);
  grid-template-areas:
    'num label'
    'num note';
  gap: 0 6px;
  padding: 7px 8px;
  border-left: 2px solid transparent;
  border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
  color: var(--muted);
  text-decoration: none;
  transition: color 160ms var(--ease), background-color 160ms var(--ease);
}
.tty-nav-link b {
  grid-area: num;
  color: var(--faint);
  font: 500 10px/1.5 var(--font-mono);
}
.tty-nav-link span {
  grid-area: label;
  font: 500 13px/1.3 var(--font-body);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.tty-nav-link small {
  grid-area: note;
  color: var(--faint);
  font: 400 9px/1.3 var(--font-mono);
  letter-spacing: 0.14em;
  text-transform: uppercase;
}
.tty-nav-link:hover {
  color: var(--ink);
  background: rgba(255, 255, 255, 0.03);
}
.tty-nav-link:hover b { color: var(--accent-safe); }
.tty-nav-link[aria-current='page'] {
  color: var(--ink);
  border-left-color: var(--accent);
  background: rgba(255, 0, 0, 0.08);
}
.tty-nav-link[aria-current='page'] b { color: var(--accent-safe); }

/* the data stage: route content lives here, in blocks */
.tty-stage {
  display: flex;
  flex-direction: column;
  min-width: 0;
  background: var(--bg);
}
.tty-scene {
  position: relative;
  padding: clamp(18px, 2.2vw, 30px) var(--gutter);
  min-width: 0;
  border-bottom: 1px solid var(--line);
}
.tty-scene:last-child { border-bottom: 0; }
.tty-scene-in {
  width: 100%;
  max-width: none;
  margin-inline: 0;
  min-width: 0;
}
.tty-scene--flush { padding-inline: var(--gutter); }

/* a two-column pane deck used inside a route */
.tty-panes {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 340px);
  gap: 0;
  min-width: 0;
}
.tty-pane { min-width: 0; padding: clamp(16px, 1.8vw, 26px) var(--gutter); }
.tty-pane + .tty-pane {
  border-left: 1px solid var(--line);
  background: rgba(13, 20, 27, 0.35);
}

/* hint strip at the foot of the console */
.tty-hint {
  display: grid;
  grid-template-columns: auto minmax(0, 1fr) auto;
  align-items: center;
  gap: 18px;
  padding: 8px var(--gutter);
  border-top: 1px solid var(--line);
  background: var(--surface);
  color: var(--muted);
  font: 500 10px/1.4 var(--font-mono);
  letter-spacing: 0.1em;
  text-transform: uppercase;
}
.tty-hint b { color: var(--ink); font-weight: 500; }
.tty-hint-links {
  display: flex;
  gap: 14px;
  margin: 0;
  padding: 0;
  list-style: none;
  min-width: 0;
  overflow: hidden;
  white-space: nowrap;
}
.tty-hint-links a { color: var(--muted); text-decoration: none; }
.tty-hint-links a:hover { color: var(--accent-safe); }
.tty-hint-tail { color: var(--faint); text-align: right; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

/* colophon inside the stage */
.tty-colophon {
  display: grid;
  gap: 12px;
  padding: clamp(18px, 2.2vw, 30px) var(--gutter);
  border-top: 1px solid var(--line);
  background: var(--surface);
}
.tty-colophon-in { display: grid; gap: 12px; min-width: 0; }
.tty-colophon-brand { display: flex; align-items: center; gap: 10px; }
.tty-colophon-brand img { width: 20px; height: 20px; }
.tty-colophon-brand b { font: 650 15px/1 var(--font-display); letter-spacing: -0.01em; }
.tty-colophon-copy { margin: 0; color: var(--muted); font: 400 12px/1.6 var(--font-body); }
.tty-colophon-links {
  display: flex;
  flex-wrap: wrap;
  gap: 6px 16px;
  margin: 0;
  padding: 0;
  list-style: none;
  color: var(--muted);
  font: 500 11px/1.6 var(--font-mono);
}
.tty-colophon-links a { text-decoration: none; }
.tty-colophon-links a:hover { color: var(--accent-safe); }
.tty-tiny { margin: 0; color: var(--faint); font: 400 11px/1.6 var(--font-mono); }

.tty-station {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 1px;
  margin: 0;
  background: var(--line);
  border: 1px solid var(--line);
}
.tty-station > div { padding: 8px 10px; background: var(--surface-2); min-width: 0; }
.tty-station dt {
  margin: 0;
  color: var(--faint);
  font: 500 9px/1.4 var(--font-mono);
  letter-spacing: 0.16em;
  text-transform: uppercase;
}
.tty-station dd { margin: 3px 0 0; color: var(--ink); font: 500 11px/1.4 var(--font-mono); }
.tty-station dd.is-hold { color: var(--muted); }

/* ------------------------------------------------------------- responsive */
@media (max-width: 1080px) {
  :root { --rail-w: 180px; }
  .tty-panes { grid-template-columns: minmax(0, 1fr); }
  .tty-pane + .tty-pane { border-left: 0; border-top: 1px solid var(--line); }
}

@media (max-width: 860px) {
  .tty-console { border-inline: 0; }
  .tty-deck { grid-template-columns: minmax(0, 1fr); }
  .tty-nav {
    flex-direction: row;
    gap: 4px;
    padding: 6px var(--gutter);
    border-right: 0;
    border-bottom: 1px solid var(--line);
    overflow-x: auto;
    scrollbar-width: thin;
  }
  .tty-nav-label { display: none; }
  .tty-nav-link {
    grid-template-columns: auto minmax(0, 1fr);
    grid-template-areas: 'num label';
    gap: 0 6px;
    flex: none;
    border-left: 0;
    border-bottom: 2px solid transparent;
    border-radius: var(--radius-sm) var(--radius-sm) 0 0;
    padding: 6px 10px;
  }
  .tty-nav-link small { display: none; }
  .tty-nav-link[aria-current='page'] { border-left-color: transparent; border-bottom-color: var(--accent); }
  .tty-command { grid-template-columns: minmax(0, 1fr) auto; padding-block: 8px; }
  .tty-status-cells { gap: 12px; }
  .tty-status-tail { display: none; }
  .tty-station { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .tty-hint { grid-template-columns: minmax(0, 1fr) auto; }
  .tty-hint-links { display: none; }
}

@media (max-width: 560px) {
  .tty-status { grid-template-columns: minmax(0, 1fr) auto; }
  .tty-status-cells { display: none; }
  .tty-command-title { font-size: 15px; }
  .tty-command-actions .tty-btn--ghost { display: none; }
}

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.001ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.001ms !important;
    scroll-behavior: auto !important;
  }
}

"""

CSS.write_text(head + tail, encoding="utf-8")
print("console.css rewritten:", len(head), "head bytes,", len(tail), "tail bytes")
