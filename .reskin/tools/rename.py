import pathlib

root = pathlib.Path(r"E:\workspace\chuangye\solana\705\website\src")
files = [p for p in root.rglob("*") if p.suffix in {".vue", ".css", ".js"}]
class_pairs = [
    ("atlas-", "tty-"), ("deck-", "pag-"), ("quay-", "wrk-"), ("board-", "tbl-"),
    ("opt-", "pfx-"), ("leaf-", "doc-"), ("lab-", "log-"), ("port-", "wal-"),
]
state_pairs = [
    ("is-anchor-end", "end"), ("is-lit", "on"), ("is-rise", "up"), ("is-fall", "down"),
    ("is-chord", "sel"), ("is-loud", "loud"), ("is-income", "inc"),
    ("is-open", "open"), ("is-linked", "linked"), ("sr-only", "vh"),
]
var_pairs = [
    ("--star-faint", "--faint"), ("--star-mute", "--muted"), ("--star-2", "--ink-2"),
    ("--star", "--ink"), ("--beam-2", "--accent-2"), ("--beam", "--accent"),
    ("--hair-2", "--line-2"), ("--hair", "--line"), ("--deck-3", "--surface-3"),
    ("--deck-2", "--surface-2"), ("--deck", "--surface"), ("--void-2", "--bg-2"),
    ("--void", "--bg"), ("--r-pill", "--radius-pill"), ("--r-lg", "--radius-lg"),
    ("--r-md", "--radius-md"), ("--r-sm", "--radius-sm"), ("--label-track", "--track-label"),
    ("--dur", "--motion"), ("--pad", "--gutter"), ("--fit", "--max-w"), ("--dock-h", "--strip-h"),
]
color_pairs = [
    ("rgba(64, 179, 255,", "rgba(255, 45, 45,"),
    ("rgba(167, 139, 250,", "rgba(255, 0, 200,"),
    ("rgba(11, 12, 21,", "rgba(10, 14, 20,"),
    ("rgba(18, 18, 30,", "rgba(18, 26, 36,"),
    ("rgba(25, 25, 39,", "rgba(24, 37, 51,"),
    ("rgba(5, 6, 13,", "rgba(5, 7, 10,"),
    ("#04060d", "#050608"),
    ("#6bc4ff", "#ff6b6b"),
    ("#1b6ea8", "#a30000"),
    ("#0a2c44", "#2a0303"),
    ("#40b3ff", "#ff0000"),
    ("#12121e", "#182533"),
    ("#f5f4fa", "#F4F7FA"),
    ("#d7d5e4", "#D7DDE4"),
    ("#a9a7bd", "#8FA3B5"),
    ("#8e8ca3", "#7C8FA3"),
    ("#262536", "#1E2A36"),
    ("#34334a", "#2A3B4C"),
    ("#0b0c15", "#111A24"),
    ("#05060d", "#05070c"),
]
changed = {}
for path in files:
    text = path.read_text(encoding="utf-8")
    before = text
    for old, new in var_pairs + class_pairs + state_pairs + color_pairs:
        text = text.replace(old, new)
    if text != before:
        path.write_text(text, encoding="utf-8")
        changed[str(path.relative_to(root))] = sum(1 for a, b in zip(before.splitlines(), text.splitlines()) if a != b)
print("files changed:", len(changed))
for k, v in sorted(changed.items()):
    print(f"  {k}: {v} lines")
