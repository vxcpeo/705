import pathlib
p = pathlib.Path(r"E:\workspace\chuangye\solana\705\website\src\console.css")
t = p.read_text(encoding="utf-8")
t = t.replace("  border-radius: var(--radius-pill);\n  background: transparent;\n  color: var(--ink);\n  font: 500 10px/1 var(--font-mono);",
              "  border-radius: var(--radius-sm);\n  background: transparent;\n  color: var(--ink);\n  font: 500 11px/1 var(--font-mono);")
t = t.replace(".tty-btn--accent:hover { background: #b9a2ff; border-color: transparent; }",
              ".tty-btn--accent:hover { background: #ff5ce0; border-color: transparent; }")
t = t.replace(".tty-btn--accent {\n  border-color: transparent;\n  background: var(--accent-2);\n  color: #0a0616;",
              ".tty-btn--accent {\n  border-color: transparent;\n  background: var(--accent-2);\n  color: #050608;")
t = t.replace("  .tty-hint { grid-template-columns: minmax(0, 1fr) auto; }\n  .tty-hint-links { display: none; }",
              "  .tty-hint { grid-template-columns: minmax(0, 1fr); }")
p.write_text(t, encoding="utf-8")
print("console tweaks applied")
