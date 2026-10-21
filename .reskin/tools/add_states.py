import pathlib
p = pathlib.Path(r"E:\workspace\chuangye\solana\705\website\src\console.css")
t = p.read_text(encoding="utf-8")
anchor = "/* --------------------------------------------------------------- structure */"
add = """.up { color: var(--success); }
.down { color: var(--danger); }

/* --------------------------------------------------------------- structure */"""
if ".up { color: var(--success); }" not in t:
    t = t.replace(anchor, add)
    p.write_text(t, encoding="utf-8")
    print("state colors added")
else:
    print("already present")
