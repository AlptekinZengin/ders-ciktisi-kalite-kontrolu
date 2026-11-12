# Final projesi, adım 5: iki etiket dosyasını birleştirir (300 + yeni 500 - İngilizce).
# Çalıştırma (yz-dersi klasöründe):  py -3 final/05_etiket_birlestir.py
import os
import pandas as pd

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ilk = pd.read_csv(os.path.join(KOK, "kalite-rapor", "etiket", "etiket_kesin.csv"), encoding="utf-8-sig", dtype=str, keep_default_na=False)
yeni = pd.read_csv(os.path.join(KOK, "final", "etiket2", "tahmin_500.csv"), encoding="utf-8-sig", dtype=str, keep_default_na=False)
kon = pd.read_excel(os.path.join(KOK, "final", "etiket2", "Kontrol-Tablosu-2.xlsx"), sheet_name="Kontrol", dtype=str).fillna("")
kon["no"] = kon["no"].astype(str)
assert kon["no"].is_unique and set(kon["no"]) == set(yeni["no"])
kon = kon.set_index("no")

KAYNAK_DEGISTI = "Alptekin tabloda değiştirdi (2026-11-10)"
KAYNAK_ONAY = "Alptekin 500 cümleyi kontrol etti, model tahminini onayladı (2026-11-10)"

satirlar = []
dolu = 0
farkli = 0
for _, r in yeni.iterrows():
    k = kon.loc[r["no"]]
    assert k["cumle"] == r["cumle"], r["no"]
    ak, ab = k["alptekin_kalite"].strip(), k["alptekin_bloom"].strip()
    if ak:
        dolu += 1
        if ak != r["model_kalite"] or ab != r["model_bloom"]:
            farkli += 1
        kal, blm, kay = ak, ab, KAYNAK_DEGISTI
    else:
        kal, blm, kay = r["model_kalite"], r["model_bloom"], KAYNAK_ONAY
    d = {c: r.get(c, "") for c in ilk.columns}
    d.update({"no": str(int(r["no"]) + 300), "alptekin_kalite": kal, "alptekin_bloom": blm, "alptekin_kaynak": kay,
              "secim_grubu": r["secim_grubu"], "isaret": r["isaret"]})
    satirlar.append(d)

ilk2 = ilk.copy()
ilk2["secim_grubu"] = "ILK_300"
ilk2["isaret"] = ""
son = pd.concat([ilk2, pd.DataFrame(satirlar)], ignore_index=True)

ing = son["isaret"].str.split(";").apply(lambda l: "INGILIZCE" in l)
print("Alptekin hücresi dolu:", dolu, "| model tahmininden farklı:", farkli)
print("Çıkarılan İngilizce satır:", int(ing.sum()))
son = son[~ing].reset_index(drop=True)

# kontroller
assert not son["cumle"].duplicated().any(), "tekrar eden cümle var"
assert set(son["alptekin_kalite"]) <= {"DUZGUN", "BELIRSIZ", "CIKTI_DEGIL"}, set(son["alptekin_kalite"])
kotu = son[(son["alptekin_kalite"] != "DUZGUN") & (son["alptekin_bloom"] != "")]
if len(kotu):
    print("UYARI: DUZGUN olmayan ama bloom dolu:", len(kotu))
    print(kotu[["no", "alptekin_kalite", "alptekin_bloom", "secim_grubu"]].to_string())
bos = son[(son["alptekin_kalite"] == "DUZGUN") & (son["alptekin_bloom"] == "")]
print("DUZGUN ama bloom boş:", len(bos))

yol = os.path.join(KOK, "final", "etiket2", "etiket_kesin_800.csv")
son.to_csv(yol, index=False, encoding="utf-8-sig")
print("Satır:", len(son))
print(son["secim_grubu"].value_counts().to_string())
print(son["alptekin_kalite"].value_counts().to_string())
print(son["alptekin_bloom"].replace("", "(boş)").value_counts().to_string())
