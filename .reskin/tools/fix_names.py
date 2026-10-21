import pathlib
for rel in ("components/MarketWorkspace.vue",):
    p = pathlib.Path(r"E:\workspace\chuangye\solana\705\website\src") / rel
    t = p.read_text(encoding="utf-8").replace("passwal", "spec")
    p.write_text(t, encoding="utf-8")
print("done")
