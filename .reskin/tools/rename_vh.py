import pathlib
root = pathlib.Path(r"E:\workspace\chuangye\solana\705\website\src")
for path in list(root.rglob("*.vue")) + [root / "console.css"]:
    text = path.read_text(encoding="utf-8")
    new = text.replace('class="vh"', 'class="visually-hidden"').replace('class="vh ', 'class="visually-hidden ')
    new = new.replace(".vh {", ".visually-hidden {")
    if new != text:
        path.write_text(new, encoding="utf-8")
        print("updated", path.name)
