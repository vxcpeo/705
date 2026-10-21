"""Generate Pretiola's website identity artwork and concept figures.

The palette, the mark geometry and the dual PNG/SVG writer all come from
``twitter/brandkit.py``; this module only composes scenes, so the site art and
the X art cannot drift apart. Nothing here re-draws the mark or hardcodes a
brand colour.

Design language: light paper ground, full-bleed ink rules, hairline registration
grids, flat state colour. No gradients, no glow, no rounded corners.

Writes into ``website/public/``:

  icon.svg                 64x64    the mark alone, vector, full bleed
  apple-icon.png          180x180   paper ground, ink rules, centred mark
  favicon-32.png           32x32    the apple icon at tab size
  og-image.jpg + .svg    1200x630   link card
  concept-backing.*      1200x750   watchlist ledger figure
  concept-cap.*          1200x750   payoff boundary figure
  concept-settlement.*   1200x750   settlement table and share meter
  market-snapshot.json              preview identity and sample watchlist

Every scene carries a <title> and a <desc>. Both the raster and the editable
vector file are rewritten on each run, so re-running this script reproduces the
whole asset set byte for byte.

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

if not (TWITTER / "brandkit.py").is_file():
    raise SystemExit(f"shared brand renderer missing: {TWITTER / 'brandkit.py'}")
sys.path.insert(0, str(TWITTER))

from brandkit import (ALERT, BRAND, CARD, DOMAIN, FLARE, HAIR, HANDLE,  # noqa: E402
                      INK, LEDGER, NETWORK, PAPER, RULE, SIGNAL, SUPPORTING,
                      TAGLINE, TICKER, Scene)

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
FOOT_RULE_Y = 700

# ------------------------------------------------------------------- writers
def save_vector(scene: Scene, path: Path) -> Path:
    """Write the SVG half of a scene and nothing else.

    ``brandkit.Scene.save`` can skip the vector twin but always rasterises, and
    the icon is the one piece delivered as vector only, so this serialises the
    same document without the raster step.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(scene.svg + ["</svg>"]) + "\n", encoding="utf-8")
    return path


def save_raster(scene: Scene, path: Path) -> Path:
    """Raster-only write, for pieces that carry no editable vector twin.

    ``icon.svg`` is the vector master for the mark, so the two icon PNGs are
    written with ``vector=False`` rather than leaving a duplicate scene file.
    """
    return scene.save(path, vector=False)


# ------------------------------------------------------------------ identity
def icon() -> Path:
    """64x64 mark at full bleed with a small paper margin, legible at 16px."""
    s = Scene(64, 64, f"{BRAND} mark",
              "The Pretiola pip: a P struck from ledger rules — a full-height ink stem, a "
              "squared top rule that turns into the bowl wall, a middle rule that closes "
              "the bowl, and a flare-orange pip set just past it — on a paper ground.")
    s.mark(32, 32, 52)  # 6px of paper on every side
    return save_vector(s, PUBLIC / "icon.svg")


def icon_tile(size: int, label: str) -> Scene:
    """Paper ground, an ink rule top and bottom, and the mark centred."""
    s = Scene(size, size, f"{BRAND} {label}",
              f"The {BRAND} mark centred between two full-width ink rules on a paper ground.")
    rule = max(3, round(size * 0.044))
    s.rect(0, 0, size, rule, INK)
    s.rect(0, size - rule, size, rule, INK)
    s.mark(size / 2, size / 2, (size - 2 * rule) * 0.78)
    return s


# ------------------------------------------------------------- figure frame
def figure(kicker: str, title: str, sub: str, alt_title: str, alt: str) -> Scene:
    """The shared 1200x750 frame used by all three concept figures."""
    s = Scene(1200, 750, alt_title, alt)
    s.rect(0, 0, 1200, 10, INK)
    s.lockup(56, 74, 30, baseline=True)
    s.text(1144, 70, f"{TICKER} / {NETWORK.upper()}", 14, RULE, "mono", "right")
    s.line([(56, 120), (1144, 120)], RULE, 2)
    s.box(56, 154, 58, 5, FLARE)
    s.text(56, 190, kicker, 13, FLARE, "mono-bold")
    s.text(56, 240, title, 40, INK, "display")
    s.text(56, 274, sub, 16, RULE, "regular")
    return s


def figure_foot(s: Scene, note: str) -> None:
    s.line([(56, FOOT_RULE_Y), (1144, FOOT_RULE_Y)], HAIR, 1)
    s.text(56, 730, note, 12, RULE, "mono")
    s.text(1144, 730, FOOT_RIGHT, 12, RULE, "mono", "right")


def panel_head(s: Scene, x: float, y: float, w: float, label: str,
               right: str | None = None, chip: str | None = None,
               head_h: float = 46) -> float:
    """Ink bar plus ruled head band. Returns the head band's bottom edge."""
    s.rect(x, y, w, 5, INK)
    s.line([(x, y + head_h), (x + w, y + head_h)], INK, 2)
    s.text(x + 26, y + 32, label, 12, RULE, "mono")
    if chip:
        chip_w = s.text_width(chip, 10, "mono-bold") + 24
        s.rect(x + w - 26 - chip_w, y + 11, chip_w, 24, CARD, FLARE, 1)
        s.text(x + w - 26 - chip_w / 2, y + 27, chip, 10, FLARE, "mono-bold", "center")
    elif right:
        s.text(x + w - 26, y + 32, right, 12, RULE, "mono", "right")
    return y + head_h


def cell(s: Scene, x: float, y: float, w: float, h: float, label: str,
         value: str, note: str, value_color: str = INK) -> None:
    """Ruled stat cell, the figure-sized version of the site's .cells block."""
    s.rect(x, y, w, h, CARD, RULE, 2)
    s.text(x + 22, y + 34, label, 11, RULE, "mono")
    s.text(x + 22, y + 82, value, 30, value_color, "display")
    s.text(x + 22, y + 104, note, 10, RULE, "mono")


# ------------------------------------------------------------ concept figures
def concept_backing() -> Scene:
    """Watchlist concept: a ruled ledger with three sample rows."""
    s = figure(
        "SURFACE 01 / WATCHLIST", "THE BOARD.",
        "A ruled ledger of the assets on the board, with mono sample prices.",
        f"{BRAND} watchlist figure",
        "A ruled watchlist ledger panel lists three sample rows: SOL at $182.40, JUP at "
        "$1.12 and PRETIOLA, proposed and not issued, at $1.00, with a delta and a state "
        "column and a SAMPLE DATA flag. Illustrative rows only; there is no live quote "
        "feed.")
    x, y, w = 56, 306, 1088
    head = panel_head(s, x, y, w, "WATCHLIST / EXAMPLE", chip=SAMPLE_FLAG)

    # column header band
    header = head + 44
    s.line([(x, header), (x + w, header)], HAIR, 1)
    for cx, label, align in ((84, "ASSET", "left"), (270, "NAME", "left"),
                             (860, "PRICE", "right"), (1000, "DELTA 24H", "right"),
                             (1116, "STATE", "right")):
        s.text(cx, header - 14, label, 11, RULE, "mono", align)

    rows = (
        ("SOL", "Solana", "$182.40", "+2.4%", "WATCH", LEDGER),
        ("JUP", "Jupiter", "$1.12", "-0.8%", "WATCH", ALERT),
        (TICKER, BRAND, "$1.00", "--", "NOT ISSUED", RULE),
    )
    for i, (sym, name, price, delta, state, tone) in enumerate(rows):
        ry = header + i * 76
        marked = sym == TICKER
        if marked:
            s.rect(x + 1, ry, w - 2, 76, PAPER)
            s.rect(x + 1, ry, 4, 76, FLARE)
        s.line([(x, ry + 76), (x + w, ry + 76)], HAIR, 1)
        s.box(84, ry + 26, 12, 12, FLARE if marked else INK)
        s.text(112, ry + 50, sym, 20, INK, "mono-bold")
        s.text(270, ry + 49, name, 18, RULE, "regular")
        s.text(860, ry + 50, price, 20, INK, "mono-bold", "right")
        s.text(1000, ry + 50, delta, 17, tone, "mono", "right")
        s.text(1116, ry + 50, state, 12, FLARE if marked else RULE, "mono-bold", "right")

    foot = header + 3 * 76
    s.text(84, foot + 36, "ILLUSTRATIVE ROWS / NO LIVE QUOTE FEED", 11, RULE, "mono")
    s.text(1116, foot + 36, "BROWSER-LOCAL WATCHLIST", 11, RULE, "mono", "right")

    figure_foot(s, "WATCHLIST / ON-CHAIN SYMBOLS, SAMPLE VALUES")
    return s


def concept_cap() -> Scene:
    """Cap concept: a value axis, the flare cap line K, income below and upside above."""
    s = figure(
        "SURFACE 02 / CAP MODEL", "THE BOUNDARY.",
        "Cap K splits per-unit value: income below the line, upside above it.",
        f"{BRAND} payoff boundary figure",
        "A ruled value axis carries a flare cap line marked K at $262.50. The area below "
        "K is labelled INCOME at $247.29 per unit and the area above it UPSIDE at $2.71 "
        "per unit, with an ink price path running from the $250.00 spot to the assumed "
        "$280.00 settlement. Illustrative model values only.")
    x, y, w, h = 56, 306, 700, 378
    head = panel_head(s, x, y, w, "VALUE AXIS / PER UNIT", chip=SAMPLE_FLAG)

    axis_x, plot_top, plot_bottom = 170, 372, 666
    right = x + w - 28                                   # 728
    step = (plot_bottom - plot_top) / 50.0               # $235..$285 over the plot

    def axis_y(value: float) -> float:
        return plot_bottom - (value - 235.0) * step

    y_k, y_s, y_spot = axis_y(262.5), axis_y(280.0), axis_y(250.0)

    # income area sits on paper; the upside area keeps the card ground.
    # A flat colour edge marks each side of K.
    s.rect(axis_x + 1, y_k + 1, right - axis_x - 1, plot_bottom - y_k - 1, PAPER)
    s.rect(axis_x + 1, y_k + 1, 5, plot_bottom - y_k - 1, LEDGER)
    s.rect(axis_x + 1, y_s + 1, 5, y_k - y_s - 2, ALERT)

    # value axis and rulings
    for value, color in ((285.0, HAIR), (280.0, HAIR), (270.0, HAIR),
                         (250.0, HAIR), (240.0, HAIR)):
        gy = axis_y(value)
        s.line([(axis_x, gy), (right, gy)], color, 1)
        s.text(axis_x - 16, gy + 4, f"${value:,.2f}".replace(".00", ""), 11, RULE,
               "mono", "right")
    s.text(axis_x - 16, y_k + 4, CAP_K, 11, FLARE, "mono-bold", "right")
    s.line([(axis_x, plot_top), (axis_x, plot_bottom)], INK, 2)
    s.line([(axis_x, plot_bottom), (right, plot_bottom)], INK, 2)

    # the settlement reference and the flare cap line
    s.line([(axis_x, y_s), (right, y_s)], SIGNAL, 2)
    s.text(right, y_s - 10, f"S / {SETTLEMENT}", 12, SIGNAL, "mono-bold", "right")
    s.line([(axis_x, y_k), (right, y_k)], FLARE, 3)
    s.text(right, y_k - 12, f"K / {CAP_K}", 12, FLARE, "mono-bold", "right")

    # per-unit model price inside each area
    s.text(200, y_k + 40, "INCOME", 13, LEDGER, "mono-bold")
    s.text(200, y_k + 92, INCOME_PRICE, 34, INK, "display")
    s.text(200 + s.text_width(INCOME_PRICE, 34, "display") + 16, y_k + 92,
           "PER UNIT", 10, RULE, "mono")
    s.text(200, y_k + 118, "VALUE UP TO K", 10, RULE, "mono")

    s.text(200, y_s + 36, "UPSIDE", 13, ALERT, "mono-bold")
    s.text(200, y_s + 84, UPSIDE_PRICE, 34, INK, "display")
    s.text(200 + s.text_width(UPSIDE_PRICE, 34, "display") + 16, y_s + 84,
           "PER UNIT", 10, RULE, "mono")

    # the price path: spot, rising through K, to the assumed settlement
    path = [(420, y_spot), (480, y_spot - 8), (530, y_spot - 26), (575, y_spot - 56),
            (620, y_spot - 94), (660, y_spot - 134), (700, y_s)]
    s.line(path, INK, 3)
    s.box(415, y_spot - 5, 10, 10, INK)
    s.box(694, y_s - 6, 12, 12, FLARE)
    s.text(420, y_spot + 28, f"SPOT / {SPOT}", 11, RULE, "mono")

    # right column: the cap, the settlement and the summed per-unit price
    cx, cw, ch = 784, 360, 120
    cell(s, cx, 306, cw, ch, "CAP K", CAP_K, "SPOT x 1.05 / USER SET", FLARE)
    cell(s, cx, 435, cw, ch, "SETTLEMENT S", SETTLEMENT, "ASSUMED / USER ENTERED", SIGNAL)
    cell(s, cx, 564, cw, ch, "SPOT PRICE / PER UNIT", SPOT,
         f"{INCOME_PRICE} INCOME + {UPSIDE_PRICE} UPSIDE")

    figure_foot(s, "ILLUSTRATIVE MODEL / NO LIVE QUOTE")
    return s


def concept_settlement() -> Scene:
    """Settlement concept: a ruled table plus a two-leg share meter."""
    s = figure(
        "SURFACE 03 / SETTLEMENT", "THE SPLIT.",
        "One assumed settlement, split at K, and the share each leg carries.",
        f"{BRAND} settlement split figure",
        "A ruled settlement table splits one assumed $280.00 settlement into income of "
        "$262.50, the part up to K, and upside of $17.50, the part above K. A two-leg "
        "meter shows the per-unit price share as flat bars: income 98.92% and upside "
        "1.08% of the $250.00 spot. Illustrative model values only.")
    tx, ty, tw, th = 56, 306, 660, 378
    head = panel_head(s, tx, ty, tw, "SETTLEMENT TABLE / PER UNIT", right=f"S = {SETTLEMENT}")

    header = head + 40
    s.line([(tx, header), (tx + tw, header)], HAIR, 1)
    for cx, label, align in ((84, "COMPONENT", "left"), (300, "FORMULA", "left"),
                             (688, "VALUE", "right")):
        s.text(cx, header - 14, label, 11, RULE, "mono", align)

    rows = (("INCOME", "min(S, K)", INCOME_SETTLE, LEDGER),
            ("UPSIDE", "max(S - K, 0)", UPSIDE_SETTLE, ALERT),
            ("TOTAL", "S", SETTLEMENT, INK))
    for i, (name, formula, value, tone) in enumerate(rows):
        ry = header + i * 80
        if i == len(rows) - 1:
            s.line([(tx, ry), (tx + tw, ry)], INK, 2)
        s.line([(tx, ry + 80), (tx + tw, ry + 80)], HAIR, 1)
        s.text(84, ry + 50, name, 17, tone, "mono-bold")
        s.text(300, ry + 49, formula, 15, RULE, "mono")
        s.text(688, ry + 50, value, 26, INK, "mono-bold", "right")

    s.text(84, header + 3 * 80 + 32, "ILLUSTRATIVE SETTLEMENT / NOT AN AUCTION RESULT",
           11, RULE, "mono")

    # two-leg meter: flat filled bars, true proportions
    mx, my, mw, mh = 752, 306, 392, 378
    panel_head(s, mx, my, mw, "SHARE METER / PER UNIT", right="OF SPOT")
    bar_x, bar_y, bar_w, bar_h = 778, 400, 340, 52
    income_w = round(bar_w - 4, 4) * (float(INCOME_SHARE) / 100.0)
    s.rect(bar_x, bar_y, bar_w, bar_h, CARD, INK, 2)
    s.rect(bar_x + 2, bar_y + 2, income_w, bar_h - 4, LEDGER)
    s.rect(bar_x + 2 + income_w, bar_y + 2, bar_w - 4 - income_w, bar_h - 4, ALERT)
    s.text(bar_x, bar_y - 14, "INCOME", 12, LEDGER, "mono-bold")
    s.text(bar_x + bar_w, bar_y - 14, "UPSIDE", 12, ALERT, "mono-bold", "right")
    s.line([(bar_x + bar_w - 2, bar_y + bar_h + 4), (bar_x + bar_w - 2, bar_y + bar_h + 26)],
           ALERT, 1)

    s.text(bar_x, 500, "INCOME SHARE", 11, RULE, "mono")
    s.text(bar_x, 542, f"{INCOME_SHARE}%", 34, LEDGER, "display")
    s.text(bar_x, 566, f"{INCOME_PRICE} PER UNIT", 11, RULE, "mono")
    s.text(bar_x + bar_w, 500, "UPSIDE SHARE", 11, RULE, "mono", "right")
    s.text(bar_x + bar_w, 542, f"{UPSIDE_SHARE}%", 34, ALERT, "display", "right")
    s.text(bar_x + bar_w, 566, f"{UPSIDE_PRICE} PER UNIT", 11, RULE, "mono", "right")

    s.line([(bar_x, 590), (bar_x + bar_w, 590)], HAIR, 1)
    s.text(bar_x, 616, "SPOT", 11, RULE, "mono")
    s.text(bar_x + bar_w, 616, SPOT, 13, INK, "mono-bold", "right")
    s.text(bar_x, 640, "INCOME + UPSIDE", 11, RULE, "mono")
    s.text(bar_x + bar_w, 640, f"{INCOME_PRICE} + {UPSIDE_PRICE}", 13, INK, "mono-bold",
           "right")
    s.line([(bar_x, 652), (bar_x + bar_w, 652)], HAIR, 1)
    s.text(bar_x, 678, "SUM", 11, RULE, "mono")
    s.text(bar_x + bar_w, 678, SPOT, 13, INK, "mono-bold", "right")

    figure_foot(s, "ILLUSTRATIVE SPLIT / NO EXECUTION")
    return s


# ------------------------------------------------------------------ og card
def og_image() -> Scene:
    """1200x630 link card: lockup, the primary line and a framed mark panel."""
    s = Scene(1200, 630, f"{BRAND} | {NETWORK} market terminal",
              f"{TAGLINE} {SUPPORTING}")
    s.rect(0, 0, 1200, 8, INK)
    s.lockup(56, 72, 28, baseline=True)
    s.text(1144, 68, HANDLE, 14, RULE, "mono", "right")
    s.line([(56, 112), (1144, 112)], RULE, 2)

    # framed registration grid holding the mark
    s.rect(824, 158, 320, 320, CARD, RULE, 2)
    s.grid(824, 158, 320, 320, step=32, color=HAIR)
    s.rect(824, 158, 320, 5, FLARE)
    s.mark(984, 318, 200)
    s.text(984, 452, "THE PRETIOLA PIP", 13, RULE, "mono", "center")

    s.box(56, 158, 58, 5, FLARE)
    s.text(56, 232, "READ THE CHAIN.", 54, INK, "display")
    s.text(56, 288, "PRICE THE BOUNDARY.", 54, INK, "display")
    s.text(56, 372, "KEEP THE RECORD.", 34, FLARE, "display")
    s.text(56, 420, "WATCHLIST / PAYOFF BOUNDARY / RESEARCH JOURNAL", 13, RULE, "mono")
    s.line([(56, 452), (780, 452)], HAIR, 1)

    s.line([(56, 546), (1144, 546)], RULE, 2)
    s.text(56, 584, DOMAIN, 13, RULE, "mono")
    s.text(600, 584, f"{TICKER} / PROPOSED, NOT ISSUED", 13, RULE, "mono", "center")
    s.text(1144, 584, f"{NETWORK} / market terminal preview", 13, RULE, "mono", "right")
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
        save_raster(icon_tile(180, "app icon"), PUBLIC / "apple-icon.png"),
        save_raster(icon_tile(32, "tab icon"), PUBLIC / "favicon-32.png"),
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

    produced = {p.name for p in written}
    stale = sorted(p.name for p in PUBLIC.iterdir()
                   if p.is_file() and p.name not in produced)
    if stale:
        print("Present in public/ but not written by this script: " + ", ".join(stale))
    return 0


if __name__ == "__main__":
    raise SystemExit(generate())
