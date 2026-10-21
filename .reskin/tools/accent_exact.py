import pathlib
root = pathlib.Path(r"E:\workspace\chuangye\solana\705\website\src")
count = 0
for path in list(root.rglob("*.vue")) + [root / "console.css"]:
    t = path.read_text(encoding="utf-8")
    n = t.replace("rgba(255, 45, 45,", "rgba(255, 0, 0,")
    if n != t:
        path.write_text(n, encoding="utf-8")
        count += 1
print("files updated:", count)
