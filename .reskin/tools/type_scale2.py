import pathlib
p = pathlib.Path(r"E:\workspace\chuangye\solana\705\website\src\components\ScenarioLab.vue")
t = p.read_text(encoding="utf-8")
t = t.replace(".log-display { font-size: clamp(36px, 5.4vw, 70px); }", ".log-display { font-size: clamp(28px, 3.4vw, 46px); }")
p.write_text(t, encoding="utf-8")
print("scenario display tightened")
