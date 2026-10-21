import pathlib, re
root = pathlib.Path(r"E:\workspace\chuangye\solana\705\website\src")
css = root / "console.css"
t = css.read_text(encoding="utf-8")
t = t.replace("font: 400 clamp(40px, 6.4vw, 88px)/0.98 var(--font-display);", "font: 650 clamp(30px, 4.3vw, 62px)/1.02 var(--font-display);")
t = t.replace("font: 400 clamp(26px, 3.1vw, 42px)/1.08 var(--font-display);", "font: 650 clamp(21px, 2.2vw, 32px)/1.12 var(--font-display);")
css.write_text(t, encoding="utf-8")

repl = {
    "components/MarketWorkspace.vue": [(".wrk-display { font-size: clamp(38px, 5.4vw, 72px); }", ".wrk-display { font-size: clamp(30px, 3.6vw, 46px); }")],
    "components/DocsPage.vue": [(".doc-display { font-size: clamp(36px, 5.2vw, 68px); }", ".doc-display { font-size: clamp(28px, 3.4vw, 44px); }")],
}
for rel, pairs in repl.items():
    p = root / rel
    s = p.read_text(encoding="utf-8")
    for old, new in pairs:
        if old in s:
            s = s.replace(old, new)
    p.write_text(s, encoding="utf-8")
print("type scale tightened")
