import re, pathlib
root = pathlib.Path(r"E:\workspace\chuangye\solana\705\website\src")

# Remove the dead orbit rules from HomePage (conic-gradient alone flips the archetype).
home = root / "components" / "HomePage.vue"
text = home.read_text(encoding="utf-8")
text = re.sub(r"\n\.pag-orbit \{.*?\n\}\n\.pag-ring \{.*?\n\.pag-core \{.*?\n\}\n", "\n", text, flags=re.S)
text = text.replace("  .pag-orbit { top: -8%; right: -18%; width: min(78vw, 560px); opacity: 0.75; }\n", "")
text = text.replace("  scroll-snap-type: x mandatory;\n", "")
text = text.replace("  scroll-snap-align: start;\n", "")
text = text.replace("  scroll-snap-type: x mandatory;", "")
text = text.replace("scroll-snap-align: start; ", "")
home.write_text(text, encoding="utf-8")

for path in [root / "console.css", root / "components" / "DocsPage.vue"]:
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"^\s*scroll-snap-(?:type|align):[^;]+;\n", "", text, flags=re.M)
    path.write_text(text, encoding="utf-8")

print("remaining markers:")
for path in [root / "console.css", *root.rglob("*.vue")]:
    text = path.read_text(encoding="utf-8").lower()
    for word in ("orbit", "conic-gradient", "scroll-snap", "<aside", "bento", "marquee"):
        if word in text:
            print(" ", path.name, "->", word)
