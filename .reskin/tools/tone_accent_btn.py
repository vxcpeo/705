import pathlib
p = pathlib.Path(r"E:\workspace\chuangye\solana\705\website\src\console.css")
t = p.read_text(encoding="utf-8")
old = """.tty-btn--accent {
  border-color: transparent;
  background: var(--accent-2);
  color: #050608;
  box-shadow: 0 0 26px rgba(255, 0, 200, 0.3);
}
.tty-btn--accent:hover { background: #ff5ce0; border-color: transparent; }"""
new = """.tty-btn--accent {
  border-color: rgba(255, 0, 200, 0.5);
  background: rgba(255, 0, 200, 0.1);
  color: #ff8ce6;
  box-shadow: none;
}
.tty-btn--accent:hover { background: rgba(255, 0, 200, 0.18); border-color: #ff00c8; color: #ffb3ef; }"""
if old in t:
    t = t.replace(old, new)
    p.write_text(t, encoding="utf-8")
    print("accent button toned down")
else:
    print("pattern not found")
