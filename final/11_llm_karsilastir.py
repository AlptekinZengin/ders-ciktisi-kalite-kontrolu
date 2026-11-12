"""İki LLM'in (GPT-6.1 Sol, Claude Haiku) 100 cümlelik tahminlerini puanlar; sonuc_05.json yazar."""
import json
from pathlib import Path
import pandas as pd
from sklearn.metrics import f1_score, accuracy_score, confusion_matrix, cohen_kappa_score

K = Path(__file__).parent
KAL = ["BELIRSIZ", "CIKTI_DEGIL", "DUZGUN"]
BLOOM = ["ANALIZ", "ANLAMA", "BILISSEL_DEGIL", "DEGERLENDIRME", "HATIRLAMA", "UYGULAMA", "YARATMA"]


def olc(y, p, siniflar):  # 06_model_800.py ile aynı tanım
    f = f1_score(y, p, average=None, labels=siniflar, zero_division=0)
    return {"macro_f1": round(float(f1_score(y, p, average="macro", labels=siniflar, zero_division=0)), 3),
            "dogruluk": round(float(accuracy_score(y, p)), 3), "n": len(y),
            "sinif_f1": {s: round(float(v), 3) for s, v in zip(siniflar, f)},
            "karisiklik_satir_gercek_sutun_tahmin": confusion_matrix(y, p, labels=siniflar).tolist()}


def oku(yol):
    return pd.read_csv(yol, encoding="utf-8-sig", dtype=str, keep_default_na=False)


anahtar = oku(K / "etiket2" / "etiket_kesin_800.csv")
test = anahtar[anahtar["secim_grubu"] == "RASTGELE"][["no", "cumle", "alptekin_kalite", "alptekin_bloom"]].reset_index(drop=True)
assert len(test) == 100

MOD = {"GPT-6.1 Sol": "gpt_tahmin.csv", "Claude Haiku": "haiku_tahmin.csv"}
tahmin, bicim, sonuc = {}, {}, {}
for ad, dosya in MOD.items():
    d = oku(K / "llm" / dosya)
    sorunlar = []
    if len(d) != 100: sorunlar.append(f"satir sayisi {len(d)}")
    if d["no"].duplicated().any(): sorunlar.append("tekrarlayan no")
    if set(d["no"]) != set(test["no"]): sorunlar.append("no kumesi test ile eslesmiyor")
    if not set(d["kalite"]) <= set(KAL): sorunlar.append(f"izinsiz kalite: {sorted(set(d['kalite']) - set(KAL))}")
    dz = d[d["kalite"] == "DUZGUN"]
    if not set(dz["bloom"]) <= set(BLOOM): sorunlar.append(f"DUZGUN satirda izinsiz bloom: {sorted(set(dz['bloom']) - set(BLOOM))}")
    bos_degil = d[(d["kalite"] != "DUZGUN") & (d["bloom"] != "")]
    if len(bos_degil): sorunlar.append(f"DUZGUN olmayan {len(bos_degil)} satirda bloom dolu")
    bicim[ad] = {"tamam": not sorunlar, "sorunlar": sorunlar, "satir": len(d)}
    tahmin[ad] = test.merge(d.rename(columns={"kalite": "tk", "bloom": "tb"}), on="no", how="left")

for ad, m in tahmin.items():
    kal = olc(m["alptekin_kalite"], m["tk"], KAL)
    g = m[m["alptekin_kalite"] == "DUZGUN"]  # 63 cümle
    # (a) uçtan uca
    pa = g["tb"].where(g["tk"] == "DUZGUN", "YOK")
    a = olc(g["alptekin_bloom"], pa, BLOOM)
    a["yok_sayisi"] = int((pa == "YOK").sum())
    a["karisiklik_not"] = "sutunlar 7 Bloom sinifi; YOK tahminleri karisikliga girmez (satir toplami 63'ten kucuk olabilir)"
    # (b) ikisi de düzgün
    gb = g[g["tk"] == "DUZGUN"]
    b = olc(gb["alptekin_bloom"], gb["tb"], BLOOM)
    b["cumle_sayisi"] = len(gb)
    sonuc[ad] = {"kalite": kal, "bloom_uctan_uca_a": a, "bloom_ikisi_de_duzgun_b": b}

# uyum
gp, hk = tahmin["GPT-6.1 Sol"], tahmin["Claude Haiku"]
ort = gp.merge(hk[["no", "tk", "tb"]], on="no", suffixes=("_g", "_h"))
ayni = int((ort["tk_g"] == ort["tk_h"]).sum())
ikisi_yanlis = ort[(ort["tk_g"] != ort["alptekin_kalite"]) & (ort["tk_h"] != ort["alptekin_kalite"])]
uyum = {"kalitede_ayni_etiket": ayni, "n": 100,
        "cohen_kappa": round(float(cohen_kappa_score(ort["tk_g"], ort["tk_h"], labels=KAL)), 3),
        "ikisi_de_yanildi_n": len(ikisi_yanlis),
        "ikisi_de_yanildi_liste": [{"no": r.no, "cumle": r.cumle, "dogru": r.alptekin_kalite, "GPT": r.tk_g, "Haiku": r.tk_h}
                                   for r in ikisi_yanlis.itertuples()]}
yanlislar = {}
for ad, m in tahmin.items():
    y = m[m["tk"] != m["alptekin_kalite"]]
    yanlislar[ad] = [{"no": r.no, "cumle": r.cumle, "dogru": r.alptekin_kalite, "tahmin": r.tk} for r in y.itertuples()]

# karşılaştırma tablosu
s2 = json.load(open(K / "sonuc_02.json", encoding="utf-8"))
s3 = json.load(open(K / "sonuc_03.json", encoding="utf-8"))
s4 = json.load(open(K / "sonuc_04.json", encoding="utf-8"))
kt, bt = s2["kalite_test"], s2["bloom_test"]
tablo = []
def sat(ad, kf, kd, bf=None, bd=None, af=None, ad_=None):
    tablo.append({"yontem": ad, "kalite_macro_f1": kf, "kalite_dogruluk": kd, "bloom_macro_f1": bf, "bloom_dogruluk": bd,
                  "bloom_uctan_uca_macro_f1": af, "bloom_uctan_uca_dogruluk": ad_})
sat("Kural", kt["Kural"]["macro_f1"], kt["Kural"]["dogruluk"])
for ad, an in [("TF-IDF + SVM", "TF-IDF + SVM"), ("TF-IDF + lojistik", "TF-IDF + lojistik regresyon")]:
    k = kt[an + " | ILK_300_ve_yeni"]; b = bt[an + " | ILK_300_ve_yeni"]
    sat(ad + " (ILK_300 + yeni)", k["macro_f1"], k["dogruluk"], b["macro_f1"], b["dogruluk"])
sat("BERTurk (kalite 3 tohum ort.; Bloom uzun egitim 5 tohum ort.)",
    round(s3["berturk"]["kalite"]["macro_f1_ort"], 3), round(s3["berturk"]["kalite"]["dogruluk_ort"], 3),
    round(s4["test_macro_f1_ort"], 3), round(s4["test_dogruluk_ort"], 3))
for ad in MOD:
    r = sonuc[ad]
    sat(ad, r["kalite"]["macro_f1"], r["kalite"]["dogruluk"], r["bloom_ikisi_de_duzgun_b"]["macro_f1"],
        r["bloom_ikisi_de_duzgun_b"]["dogruluk"], r["bloom_uctan_uca_a"]["macro_f1"], r["bloom_uctan_uca_a"]["dogruluk"])

cikti = {"not": "BERTurk ve TF-IDF Bloom sonuclari, kalite etiketi dogru verilmis 63 cumlede olculmustu; bu yuzden onlarla en adil kiyas (b) 'ikisi de duzgun dediginde'dir, (a) 'uctan uca' daha zorlu bir olcudur.",
         "bicim_kontrolu": bicim, "modeller": sonuc, "uyum": uyum, "kalite_yanlislari": yanlislar, "karsilastirma_tablosu": tablo}
(K / "sonuc_05.json").write_text(json.dumps(cikti, ensure_ascii=False, indent=1), encoding="utf-8")

# özet çıktı
print("BICIM:", json.dumps(bicim, ensure_ascii=False))
for r in tablo: print(r)
for ad in MOD:
    print(ad, "kalite karisiklik", sonuc[ad]["kalite"]["karisiklik_satir_gercek_sutun_tahmin"], "sinif_f1", sonuc[ad]["kalite"]["sinif_f1"])
    print("  (a) yok:", sonuc[ad]["bloom_uctan_uca_a"]["yok_sayisi"], " (b) n:", sonuc[ad]["bloom_ikisi_de_duzgun_b"]["cumle_sayisi"])
print("UYUM", {k: v for k, v in uyum.items() if k != "ikisi_de_yanildi_liste"})
for x in uyum["ikisi_de_yanildi_liste"][:10]: print(x)
