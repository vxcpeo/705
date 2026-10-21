import json, pathlib
root = pathlib.Path(r"E:\workspace\chuangye\solana\705\website\.reskin")
base = json.loads((root / "baseline" / "content-contract.json").read_text(encoding="utf-8"))
cur = json.loads((root / "content-contract.json").read_text(encoding="utf-8"))
def m(d, key):
    return {i["value"]: i["count"] for i in d[key]}
for key in ("visibleText", "hiddenText"):
    b, c = m(base, key), m(cur, key)
    print("==", key)
    for k in sorted(set(b) | set(c)):
        if b.get(k, 0) != c.get(k, 0):
            print(f"  {k!r}: {b.get(k,0)} -> {c.get(k,0)}")
