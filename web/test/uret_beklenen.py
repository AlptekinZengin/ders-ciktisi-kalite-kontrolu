"""Model yüklemeden Python kurallarından karşılaştırma verisi üretir."""
import json
from pathlib import Path
import re
import sys

KOK = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0, str(KOK / "kaynak"))
import oneri

metin = (KOK / "kaynak/kural_kaynak.py").read_text(encoding="utf-8")
kurallar = {"re": re}
exec(metin[metin.index("def low(s):"):metin.index("def norm(s):")], kurallar)

cumleler = (KOK / "kaynak/ornek_cumleler.txt").read_text(encoding="utf-8").splitlines()
cumleler += [
    "... !? ;,",
    "İSTATİSTİK HAKKINDA BİLGİ SAHİBİ OLUR, ANALİZ YAPAR.",
    "Students will be able to explain the system.",
    "<ve> & bilgi sahibi olur.",
    "Yapay zekâ hakkında bilgi sahibi olur.",
    "😀 Konu hakkında bilgi sahibi olur.",
    "Bilgi\t\t sahibi\u0085olur ve öğrenir.",
    "étheé ²and² _apply_ öğrenci",
    "BİLGİ SAHİBİ OLUR VE ÖĞRENİR.",
    "Verilen problemi çözer. 😀",
]

beklenen = []
for c in cumleler:
    kalite = "INGILIZCE" if kurallar["ing"](c) else kurallar["kural"](c)
    vurgular, not_ = oneri.uret(c, kalite, None)
    beklenen.append({"cumle": c, "kalite": kalite, "vurgular": vurgular, "not": not_})

hedef = KOK / "test/beklenen.json"
hedef.write_text(json.dumps(beklenen, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"{len(beklenen)} cümle yazıldı: test/beklenen.json")
