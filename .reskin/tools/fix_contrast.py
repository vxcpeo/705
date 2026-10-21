import pathlib
root = pathlib.Path(r"E:\workspace\chuangye\solana\705\website\src")
files = list(root.rglob("*.vue")) + [root / "console.css"]
total = 0
for path in files:
    text = path.read_text(encoding="utf-8")
    before = text
    text = text.replace("color: var(--accent);", "color: var(--accent-safe);")
    text = text.replace(".tty-switch > .is-on", ".tty-switch > .on")
    if text != before:
        path.write_text(text, encoding="utf-8")
        total += 1
print("updated", total, "files")
home = root / "components" / "HomePage.vue"
text = home.read_text(encoding="utf-8")
needle = "@media (max-width: 1080px) {\n  .pag-deck { grid-template-columns: minmax(0, 1fr); }"
addition = """.pag-col--rail .pag-quote-in { grid-template-columns: minmax(0, 1fr); }
.pag-col--rail .pag-split-grid { grid-template-columns: minmax(0, 1fr); }
.pag-col--rail .pag-split-readout { grid-template-columns: minmax(0, 1fr); }

@media (max-width: 1080px) {
  .pag-deck { grid-template-columns: minmax(0, 1fr); }"""
if needle in text and ".pag-col--rail .pag-quote-in" not in text:
    text = text.replace(needle, addition)
    home.write_text(text, encoding="utf-8")
    print("home rail override added")
