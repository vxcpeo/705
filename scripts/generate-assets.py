"""Generate Tabuline's website identity artwork and concept figures.

The palette, the mark geometry and the dual PNG/SVG writer all come from
``twitter/brandkit.py``; this module only composes scenes, so the site art and
the X art cannot drift apart. Nothing here re-draws the mark or hardcodes a
brand colour.

Design language: sky-white ground, soft blue gradients, rounded panels, hairline
rules and tidal arcs. Product screenshots come from ``twitter/ui/``.

Writes into ``website/public/``:

  icon.svg                 64x64    the gradient tile with the reversed mark, vector
  apple-icon.png          180x180   the same tile at app-icon size
  favicon-32.png           32x32    the same tile at tab size
  og-image.jpg + .svg    1200x630   link card
  concept-backing.*      1200x750   watchlist ledger figure
  concept-cap.*          1200x750   payoff boundary figure
  concept-settlement.*   1200x750   settlement table and share meter
  market-snapshot.json              preview identity and sample watchlist

Every scene carries a <title> and a <desc>. Both the raster and the editable
vector file are rewritten on each run, so re-running this script reproduces the
whole asset set.

Run:  python website/scripts/generate-assets.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent           # website/scripts
WEBSITE = HERE.parent                            # website
PROJECT = WEBSITE.parent                         # project root
PUBLIC = WEBSITE / "public"
TWITTER = PROJECT / "twitter"
UI = TWITTER / "ui"

if not (TWITTER / "brandkit.py").is_file():
    raise SystemExit(f"shared brand renderer missing: {TWITTER / 'brandkit.py'}")
sys.path.insert(0, str(TWITTER))

from brandkit import (ACCENT, ACCENT_DEEP, ACCENT_PALE, BG, BRAND, DOMAIN,  # noqa: E402
                      HANDLE, INK, INK_SOFT, LINE, LINE_STRONG, MUTED, NETWORK,
                      SKY, SUCCESS, SUPPORTING, TAGLINE, TICKER, Scene, mark_parts)

# --------------------------------------------------------------- sample data
# The figures are labelled SAMPLE DATA throughout. These numbers are this app's
# own model output (website/src/payoff.js) for spot $250.00, a 5% cap over 30
# days at 25% volatility and an assumed settlement of $280.00, rounded to cents.
SPOT = "$250.00"
CAP_K = "$262.50"          # spot x 1.05
SETTLEMENT = "$280.00"     # assumed, user entered
INCOME_PRICE = "$247.29"   # spot - premium
UPSIDE_PRICE = "$2.71"     # premium
INCOME_SETTLE = "$262.50"  # min(S, K)
UPSIDE_SETTLE = "$17.50"   # max(S - K, 0)
INCOME_SHARE = "98.92"     # % of spot
UPSIDE_SHARE = "1.08"      # % of spot

SAMPLE_FLAG = "SAMPLE DATA"
FOOT_RIGHT = "SAMPLE DATA / NOT LIVE"
FOOT_RULE_Y = 690

# ------------------------------------------------------------------- writers
def save_vector(scene: Scene, path: Path) -> Path:
    """Write the SVG half of a scene and nothing else."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    doc = scene.svg[:2] + ([f'<defs>{"".join(scene.defs)}</defs>'] if scene.defs else []) + scene.svg[2:]
    path.write_text("\n".join(doc + ["</svg>"]) + "\n", encoding="utf-8")
    return path


def save_raster(scene: Scene, path: Path) -> Path:
    return scene.save(path, vector=False)


def ground(s: Scene) -> None:
    s.vgrad(0, 0, s.w, s.h, "#f8f9f6", "#eceee9")
    s.grid(0, 0, s.w, s.h, step=48, color="#e1e4dd")


# ------------------------------------------------------------------ identity
def icon() -> Path:
    s = Scene(64, 64, f"{BRAND} mark",
              "The Tabuline line - a header rule, a column stem and a pale node - "
              "reversed out of a blue gradient tile.")
    s.tile_mark(0, 0, 64, r=15)
    return save_vector(s, PUBLIC / "icon.svg")


def icon_tile(size: int) -> Scene:
    s = Scene(size, size, f"{BRAND} app icon",
              f"The {BRAND} gradient tile with the reversed mark, at {size} pixels.")
    s.tile_mark(0, 0, size, r=size * 0.235)
    return s


# ------------------------------------------------------------- figure frame
def figure(kicker: str, title: str, sub: str, alt_title: str, alt: str) -> Scene:
    s = Scene(1200, 750, alt_title, alt)
    ground(s)
    s.lockup(56, 76, 30, baseline=True)
    s.text(1144, 70, f"{TICKER} / {NETWORK.upper()}", 13, MUTED, "mono", "right")
    s.line([(56, 118), (1144, 118)], LINE, 1)
    s.rect(56, 150, 42, 5, fill=ACCENT, r=2.5)
    s.text(56, 188, kicker, 13, ACCENT_DEEP, "mono-bold")
    s.text(56, 238, title, 40, INK, "display")
    s.text(56, 272, sub, 15, MUTED)
    return s


def figure_foot(s: Scene, note: str) -> None:
    s.line([(56, FOOT_RULE_Y), (1144, FOOT_RULE_Y)], LINE, 1)
    s.text(56, 722, note, 11, MUTED, "mono")
    s.text(1144, 722, FOOT_RIGHT, 11, MUTED, "mono", "right")


def panel(s: Scene, x: float, y: float, w: float, h: float, label: str,
          right: str | None = None, chip: str | None = None) -> float:
    s.rect(x, y, w, h, fill="#ffffff", stroke=LINE, r=18)
    s.vgrad(x, y, w, 54, "#f4f9ff", "#ffffff", r=18)
    s.line([(x, y + 54), (x + w, y + 54)], LINE, 1)
    s.text(x + 24, y + 33, label, 11, MUTED, "mono")
    if chip:
        cw = s.text_width(chip, 10, "mono-bold") + 26
        s.rect(x + w - 24 - cw, y + 15, cw, 26, fill="#eef7ff", stroke=LINE, r=13)
        s.circle(x + w - 24 - cw + 13, y + 28, 6, ACCENT)
        s.text(x + w - 24 - cw + 22, y + 32, chip, 10, ACCENT_DEEP, "mono-bold")
    elif right:
        s.text(x + w - 24, y + 33, right, 11, MUTED, "mono", "right")
    return y + 54


def cell(s: Scene, x: float, y: float, w: float, h: float, label: str,
         value: str, note: str, value_color: str = INK) -> None:
    s.rect(x, y, w, h, fill="#ffffff", stroke=LINE, r=16)
    s.text(x + 20, y + 30, label, 10, MUTED, "mono")
    s.text(x + 20, y + 72, value, 28, value_color, "display")
    s.text(x + 20, y + 94, note, 9, MUTED, "mono")


# ------------------------------------------------------------ concept figures
def concept_backing() -> Scene:
    s = figure(
        "SURFACE 01 / WATCHLIST", "THE BOARD.",
        "A watchlist with sample prices beside a sandbox unit quote.",
        f"{BRAND} watchlist figure",
        "A light watchlist panel lists three sample rows: SOL at $182.40, JUP at "
        f"$1.12 and {TICKER}, proposed and not issued, at $1.00, with a delta and a "
        "state column and a SAMPLE DATA flag. Illustrative rows only; no live quote.")
    x, y, w, h = 56, 300, 700, 360
    head = panel(s, x, y, w, h, "WATCHLIST / EXAMPLE", chip=SAMPLE_FLAG)

    header = head + 40
    s.line([(x, header), (x + w, header)], LINE, 1)
    for cx, label, align in ((80, "ASSET", "left"), (210, "NAME", "left"),
                             (500, "PRICE", "right"), (610, "DELTA 24H", "right"),
                             (x + w - 24, "STATE", "right")):
        s.text(cx, header - 12, label, 10, MUTED, "mono", align)

    rows = (("SOL", "Solana", "$182.40", "+2.4%", "WATCH", SUCCESS),
            ("JUP", "Jupiter", "$1.12", "-0.8%", "WATCH", ACCENT_DEEP),
            (TICKER, BRAND, "$1.00", "--", "NOT ISSUED", MUTED))
    for i, (sym, name, price, delta, state, tone) in enumerate(rows):
        ry = header + i * 78
        marked = sym == TICKER
        if marked:
            s.rect(x + 1, ry, w - 2, 78, fill="#f4f9ff", r=0)
            s.rect(x + 1, ry, 4, 78, fill=ACCENT)
        s.line([(x, ry + 78), (x + w, ry + 78)], LINE, 1)
        s.circle(88, ry + 32, 22, ACCENT if marked else "#e8f3ff")
        s.text(88, ry + 38, sym[0], 11, "#ffffff" if marked else INK_SOFT,
               "mono-bold", "center")
        s.text(112, ry + 50, sym, 17, INK, "mono-bold")
        s.text(210, ry + 49, name, 16, INK_SOFT)
        s.text(500, ry + 50, price, 18, INK, "mono-bold", "right")
        s.text(610, ry + 50, delta, 15, tone, "mono", "right")
        s.text(x + w - 24, ry + 50, state, 11, ACCENT_DEEP if marked else MUTED,
               "mono-bold", "right")

    foot = header + 3 * 78
    s.text(80, foot + 34, "ILLUSTRATIVE ROWS / NO LIVE QUOTE FEED", 10, MUTED, "mono")
    s.text(x + w - 24, foot + 34, "BROWSER-LOCAL WATCHLIST", 10, MUTED, "mono", "right")

    qx, qy, qw, qh = 776, 300, 368, 360
    s.vgrad(qx, qy, qw, qh, ACCENT_DEEP, ACCENT, r=20)
    s.text(qx + 26, qy + 46, "UNIT QUOTE / SANDBOX", 11, ACCENT_PALE, "mono-bold")
    s.text(qx + 26, qy + 112, "Modelled value", 12, ACCENT_PALE, "mono")
    s.text(qx + 26, qy + 166, "$180.42", 42, "#ffffff", "display")
    s.line([(qx + 26, qy + 196), (qx + qw - 26, qy + 196)], "#ffffff")
    for i, (label, value) in enumerate((("SAMPLE SPOT", "$182.40"),
                                        ("CAP PRICE K", "$191.52"),
                                        ("LEG", "Income"))):
        ry = qy + 232 + i * 38
        s.text(qx + 26, ry, label, 10, ACCENT_PALE, "mono")
        s.text(qx + qw - 26, ry, value, 13, "#ffffff", "mono-bold", "right")

    figure_foot(s, "WATCHLIST / ON-CHAIN SYMBOLS, SAMPLE VALUES")
    return s


def concept_cap() -> Scene:
    s = figure(
        "SURFACE 02 / CAP MODEL", "THE BOUNDARY.",
        "Cap K splits per-unit value: income below the line, upside above it.",
        f"{BRAND} payoff boundary figure",
        "A light value axis carries an accent cap line marked K at $262.50. The area "
        "below K is labelled INCOME at $247.29 per unit and the area above it UPSIDE "
        "at $2.71 per unit, with an ink price path from the $250.00 spot to the "
        "assumed $280.00 settlement. Illustrative model values only.")
    x, y, w, h = 56, 300, 700, 360
    head = panel(s, x, y, w, h, "VALUE AXIS / PER UNIT", chip=SAMPLE_FLAG)

    axis_x, plot_top, plot_bottom = 150, 372, 640
    right = x + w - 26
    step = (plot_bottom - plot_top) / 50.0

    def axis_y(value: float) -> float:
        return plot_bottom - (value - 235.0) * step

    y_k, y_s, y_spot = axis_y(262.5), axis_y(280.0), axis_y(250.0)

    s.vgrad(axis_x, y_k, right - axis_x, plot_bottom - y_k, "#f4f9ff", "#e8f3ff", opacity=0.9)
    s.rect(axis_x, y_k, 4, plot_bottom - y_k, fill=SUCCESS)
    s.rect(axis_x, y_s, 4, y_k - y_s, fill=ACCENT)

    for value in (285.0, 280.0, 270.0, 250.0, 240.0):
        gy = axis_y(value)
        s.line([(axis_x, gy), (right, gy)], LINE, 1)
        s.text(axis_x - 14, gy + 4, f"${value:,.2f}".replace(".00", ""), 10, MUTED,
               "mono", "right")
    s.text(axis_x - 14, y_k + 4, CAP_K, 10, ACCENT_DEEP, "mono-bold", "right")
    s.line([(axis_x, plot_top), (axis_x, plot_bottom)], LINE_STRONG, 1.5)
    s.line([(axis_x, plot_bottom), (right, plot_bottom)], LINE_STRONG, 1.5)

    s.line([(axis_x, y_s), (right, y_s)], ACCENT_DEEP, 1.5, dash="5 5")
    s.text(right, y_s - 10, f"S / {SETTLEMENT}", 10, ACCENT_DEEP, "mono-bold", "right")
    s.line([(axis_x, y_k), (right, y_k)], ACCENT, 2.5)
    s.text(right, y_k - 10, f"K / {CAP_K}", 10, ACCENT_DEEP, "mono-bold", "right")

    s.text(176, y_k + 40, "INCOME", 12, SUCCESS, "mono-bold")
    s.text(176, y_k + 84, INCOME_PRICE, 30, INK, "display")
    s.text(176, y_k + 106, "VALUE UP TO K / PER UNIT", 9, MUTED, "mono")
    s.text(176, y_s + 26, "UPSIDE", 11, ACCENT_DEEP, "mono-bold")
    s.text(176, y_s + 70, UPSIDE_PRICE, 26, INK, "display")
    s.text(176, y_s + 88, "VALUE ABOVE K / PER UNIT", 8, MUTED, "mono")

    path = [(430, y_spot), (490, y_spot - 8), (540, y_spot - 26), (585, y_spot - 56),
            (630, y_spot - 94), (666, y_spot - 134), (right - 6, y_s)]
    s.line(path, INK, 2.5)
    s.circle(430, y_spot, 9, INK)
    s.circle(right - 6, y_s, 10, ACCENT)
    s.text(430, y_spot + 26, f"SPOT / {SPOT}", 10, MUTED, "mono")

    cx, cw, ch = 784, 360, 112
    cell(s, cx, 300, cw, ch, "CAP K", CAP_K, "SPOT x 1.05 / USER SET", ACCENT_DEEP)
    cell(s, cx, 424, cw, ch, "SETTLEMENT S", SETTLEMENT, "ASSUMED / USER ENTERED", ACCENT_DEEP)
    cell(s, cx, 548, cw, ch, "SPOT PRICE / PER UNIT", SPOT,
         f"{INCOME_PRICE} INCOME + {UPSIDE_PRICE} UPSIDE")

    figure_foot(s, "ILLUSTRATIVE MODEL / NO LIVE QUOTE")
    return s


def concept_settlement() -> Scene:
    s = figure(
        "SURFACE 03 / SETTLEMENT", "THE SPLIT.",
        "One assumed settlement, split at K, and the share each leg carries.",
        f"{BRAND} settlement split figure",
        "A light settlement table splits one assumed $280.00 settlement into income of "
        "$262.50, the part up to K, and upside of $17.50, the part above K. A two-leg "
        "meter shows the per-unit price share as rounded bars: income 98.92% and "
        "upside 1.08% of the $250.00 spot. Illustrative model values only.")
    tx, ty, tw, th = 56, 300, 648, 360
    head = panel(s, tx, ty, tw, th, "SETTLEMENT TABLE / PER UNIT", right=f"S = {SETTLEMENT}")

    header = head + 38
    s.line([(tx, header), (tx + tw, header)], LINE, 1)
    for cx, label, align in ((80, "COMPONENT", "left"), (286, "FORMULA", "left"),
                             (tx + tw - 24, "VALUE", "right")):
        s.text(cx, header - 12, label, 10, MUTED, "mono", align)

    rows = (("INCOME", "min(S, K)", INCOME_SETTLE, SUCCESS),
            ("UPSIDE", "max(S - K, 0)", UPSIDE_SETTLE, ACCENT_DEEP),
            ("TOTAL", "S", SETTLEMENT, INK))
    for i, (name, formula, value, tone) in enumerate(rows):
        ry = header + i * 76
        if i == len(rows) - 1:
            s.line([(tx, ry), (tx + tw, ry)], INK, 1.5)
        s.line([(tx, ry + 76), (tx + tw, ry + 76)], LINE, 1)
        s.text(80, ry + 48, name, 15, tone, "mono-bold")
        s.text(286, ry + 48, formula, 13, MUTED, "mono")
        s.text(tx + tw - 24, ry + 48, value, 22, INK, "mono-bold", "right")

    s.text(80, header + 3 * 76 + 30, "ILLUSTRATIVE SETTLEMENT / NOT AN AUCTION RESULT",
           10, MUTED, "mono")

    mx, my, mw, mh = 724, 300, 420, 360
    panel(s, mx, my, mw, mh, "SHARE METER / PER UNIT", right="OF SPOT")
    bar_x, bar_y, bar_w, bar_h = 754, 404, 360, 46
    income_w = round(bar_w - 4, 4) * (float(INCOME_SHARE) / 100.0)
    s.rect(bar_x, bar_y, bar_w, bar_h, fill="#eef7ff", stroke=LINE, r=23)
    s.rect(bar_x + 2, bar_y + 2, max(28, income_w), bar_h - 4, fill=SUCCESS, r=21)
    s.circle(bar_x + 2 + max(28, income_w) + 4, bar_y + bar_h / 2, 18, ACCENT)

    s.text(bar_x, bar_y - 14, "INCOME", 11, SUCCESS, "mono-bold")
    s.text(bar_x + bar_w, bar_y - 14, "UPSIDE", 11, ACCENT_DEEP, "mono-bold", "right")

    s.text(bar_x, bar_y + 96, "INCOME SHARE", 10, MUTED, "mono")
    s.text(bar_x, bar_y + 134, f"{INCOME_SHARE}%", 30, SUCCESS, "display")
    s.text(bar_x, bar_y + 156, f"{INCOME_PRICE} PER UNIT", 10, MUTED, "mono")
    s.text(bar_x + bar_w, bar_y + 96, "UPSIDE SHARE", 10, MUTED, "mono", "right")
    s.text(bar_x + bar_w, bar_y + 134, f"{UPSIDE_SHARE}%", 30, ACCENT_DEEP, "display", "right")
    s.text(bar_x + bar_w, bar_y + 156, f"{UPSIDE_PRICE} PER UNIT", 10, MUTED, "mono", "right")

    s.line([(bar_x, bar_y + 184), (bar_x + bar_w, bar_y + 184)], LINE, 1)
    for i, (label, value) in enumerate((("SPOT", SPOT),
                                        ("INCOME + UPSIDE", f"{INCOME_PRICE} + {UPSIDE_PRICE}"),
                                        ("SUM", SPOT))):
        ry = bar_y + 216 + i * 30
        s.text(bar_x, ry, label, 10, MUTED, "mono")
        s.text(bar_x + bar_w, ry, value, 11, INK, "mono-bold", "right")
        s.line([(bar_x, ry + 12), (bar_x + bar_w, ry + 12)], LINE, 1)

    figure_foot(s, "ILLUSTRATIVE SPLIT / NO EXECUTION")
    return s


# ------------------------------------------------------------------ og card
def og_image() -> Scene:
    s = Scene(1200, 630, f"{BRAND} | {NETWORK} market terminal",
              f"{TAGLINE} {SUPPORTING}")
    ground(s)
    s.lockup(56, 74, 30, baseline=True)
    s.text(1144, 68, HANDLE, 13, MUTED, "mono", "right")
    s.line([(56, 112), (1144, 112)], LINE, 1)
    s.text(58, 152, "SOLANA MARKET TERMINAL / PREVIEW", 12, MUTED, "mono")
    s.text(56, 232, "Read the chain.", 44, INK, "display")
    s.text(56, 288, "Price the boundary.", 44, INK, "display")
    s.text(56, 358, "Keep the record.", 42, ACCENT_DEEP, "display")
    s.text(58, 404, "Watchlists / payoff boundary / browser-local journal", 15, MUTED)
    s.browser(UI / "home-top-1440.png", 648, 156, 496, 300, r=8,
              crop=(0, 0, 1440, 870), chrome=True, url=DOMAIN)
    s.line([(56, 546), (1144, 546)], LINE, 1)
    s.text(56, 582, DOMAIN, 12, MUTED, "mono")
    s.text(600, 582, f"{TICKER} / PROPOSED, NOT ISSUED", 12, MUTED, "mono", "center")
    s.text(1144, 582, f"{NETWORK} / market terminal preview", 12, MUTED, "mono", "right")
    return s


# ------------------------------------------------------------------ snapshot
def snapshot() -> Path:
    """The public market-snapshot stub, kept for compatibility."""
    payload = {
        "schemaVersion": 1,
        "status": "preview",
        "brand": BRAND,
        "network": NETWORK,
        "token": {
            "symbol": TICKER,
            "status": "proposed-unissued",
            "contractAddress": None,
            "quote": None,
        },
        "watchlist": [
            {"symbol": "SOL", "quote": None, "priceStatus": "illustrative"},
            {"symbol": "JUP", "quote": None, "priceStatus": "illustrative"},
            {"symbol": "BONK", "quote": None, "priceStatus": "illustrative"},
            {"symbol": "USDC", "quote": None, "priceStatus": "illustrative"},
        ],
        "resources": {
            "domain": DOMAIN,
            "handle": HANDLE,
            "status": ("targets from a point-in-time availability screen; neither is "
                       "registered, reserved or owned by this work"),
        },
        "note": ("No market data provider or Solana program integration is configured. "
                 "Visible prices and markets are local model examples, not live listings."),
        "disclaimer": (f"{BRAND} / {TICKER} is a product preview on {NETWORK}. Illustrative "
                       "values only: no live feed, no wallet action, no custody and no "
                       "execution. There is no contract address; nothing here is an offer "
                       "or a solicitation."),
    }
    path = PUBLIC / "market-snapshot.json"
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path


# -------------------------------------------------------------------- driver
def generate() -> int:
    PUBLIC.mkdir(parents=True, exist_ok=True)
    written: list[Path] = [
        icon(),
        save_raster(icon_tile(180), PUBLIC / "apple-icon.png"),
        save_raster(icon_tile(32), PUBLIC / "favicon-32.png"),
    ]
    og_image().save(PUBLIC / "og-image.jpg")
    written += [PUBLIC / "og-image.jpg", PUBLIC / "og-image.svg"]
    for stem, scene in (("concept-backing", concept_backing()),
                        ("concept-cap", concept_cap()),
                        ("concept-settlement", concept_settlement())):
        scene.save(PUBLIC / f"{stem}.webp")
        written.append(PUBLIC / f"{stem}.webp")
        written.append(PUBLIC / f"{stem}.svg")
    written.append(snapshot())

    print(f"{BRAND} website assets -> {PUBLIC}")
    for path in sorted(written):
        print(f"  {path.name:<26} {path.stat().st_size:>9,d} bytes")
    print(f"{len(written)} files, {sum(p.stat().st_size for p in written):,d} bytes total.")
    return 0


if __name__ == "__main__":
    raise SystemExit(generate())
