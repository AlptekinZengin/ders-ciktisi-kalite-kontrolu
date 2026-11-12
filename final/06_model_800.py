# Final projesi, adım 6: 795 etiketli cümleyle kalite ve Bloom modelleri.
# Test kümesi = secim_grubu RASTGELE (hiçbir eğitimde kullanılmaz).
# Çalıştırma (yz-dersi klasöründe):  py -3 final/06_model_800.py
import csv, json, os, re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline, make_union
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.metrics import f1_score, accuracy_score, confusion_matrix

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = list(csv.DictReader(open(os.path.join(KOK, "final", "etiket2", "etiket_kesin_800.csv"), encoding="utf-8-sig")))


def low(s):
    return s.replace("I", "ı").replace("İ", "i").lower()


# --- 01_ilk_model.py'den aynen ---
FIIL_EK = re.compile(r"(ir|ır|ur|ür|ar|er|r|ebilir|abilir|ebilmek|abilmek|ebilme|abilme|mek|mak|me|ma|ecektir|acaktır|ecek|acak|ilir|ılır|ulur|ülür|irler|ırlar|urlar|ürler|erler|arlar)$")
BEL_KOK = ("öğren", "kavra", "anla", "bil", "edin", "kazan", "geliş", "sahip", "takip", "farkında", "algıla")
BEL_IFADE = re.compile(r"bilgi sahibi|hakkında bilgi|bilgisi olur|farkındalık|önemini|bilgilen", re.I)
OLC_KOK = ("hesapla", "uygula", "analiz", "tasarla", "geliştirir", "geliştirebil", "çöz", "açıkla", "tanımla", "karşılaştır", "değerlendir",
           "kullan", "oluştur", "yaz", "hazırla", "seç", "ölç", "çiz", "kur", "yorumla", "sınıflandır", "listele", "planla", "üret", "yap", "belirle", "ifade")


def kural(s):
    w = re.findall(r"[a-zçğıöşüâîû]+", low(s))
    fiiller = [x for x in w if FIIL_EK.search(x) and len(x) > 3]
    if not fiiller:
        return "CIKTI_DEGIL"
    olc = any(x.startswith(OLC_KOK) for x in fiiller)
    bel = BEL_IFADE.search(low(s)) or any(x.startswith(BEL_KOK) for x in fiiller)
    return "BELIRSIZ" if (bel and not olc) else "DUZGUN"


def ozellik():
    return make_union(
        TfidfVectorizer(preprocessor=low, analyzer="word", ngram_range=(1, 2), sublinear_tf=True),
        TfidfVectorizer(preprocessor=low, analyzer="char_wb", ngram_range=(2, 5), sublinear_tf=True),
    )


MODELLER = {
    "TF-IDF + SVM": lambda: make_pipeline(ozellik(), LinearSVC(class_weight="balanced")),
    "TF-IDF + lojistik regresyon": lambda: make_pipeline(ozellik(), LogisticRegression(class_weight="balanced", max_iter=2000, C=10)),
}
# ---

KAL = ["BELIRSIZ", "CIKTI_DEGIL", "DUZGUN"]


def olc(y, p, siniflar):
    f = f1_score(y, p, average=None, labels=siniflar, zero_division=0)
    return {"macro_f1": round(float(f1_score(y, p, average="macro", labels=siniflar, zero_division=0)), 3),
            "dogruluk": round(float(accuracy_score(y, p)), 3), "n": len(y),
            "sinif_f1": {s: round(float(v), 3) for s, v in zip(siniflar, f)},
            "karisiklik_satir_gercek_sutun_tahmin": confusion_matrix(y, p, labels=siniflar).tolist()}


def arr(rows, anahtar):
    return np.array([r["cumle"] for r in rows], dtype=object), np.array([r[anahtar] for r in rows])


test = [r for r in E if r["secim_grubu"] == "RASTGELE"]
ilk = [r for r in E if r["secim_grubu"] == "ILK_300"]
yeni_egitim = [r for r in E if r["secim_grubu"] not in ("ILK_300", "RASTGELE")]
assert not ({r["cumle"] for r in test} & {r["cumle"] for r in ilk + yeni_egitim})
cikti = {"test_n": len(test), "ilk_300_n": len(ilk), "yeni_egitim_n": len(yeni_egitim)}

# 1) Kalite
Xt, yt = arr(test, "alptekin_kalite")
kal = {"test_dagilim": {s: int((yt == s).sum()) for s in KAL}}
kal["Kural"] = olc(yt, [kural(s) for s in Xt], KAL)
for ad_set, egitim in (("yalniz_ILK_300", ilk), ("ILK_300_ve_yeni", ilk + yeni_egitim)):
    Xe, ye = arr(egitim, "alptekin_kalite")
    for ad, mk in MODELLER.items():
        np.random.seed(42)
        kal[f"{ad} | {ad_set}"] = {**olc(yt, mk().fit(Xe, ye).predict(Xt), KAL), "egitim_n": len(egitim)}
cikti["kalite_test"] = kal

# 2) Bloom (yalnız DUZGUN ve bloom dolu)
duz = lambda rows: [r for r in rows if r["alptekin_kalite"] == "DUZGUN" and r["alptekin_bloom"]]
tb = duz(test)
Xtb, ytb = arr(tb, "alptekin_bloom")
BL = sorted({r["alptekin_bloom"] for r in duz(E)})
blm = {"test_n": len(tb), "siniflar": BL, "test_dagilim": {s: int((ytb == s).sum()) for s in BL}}
for ad_set, egitim in (("yalniz_ILK_300", ilk), ("ILK_300_ve_yeni", ilk + yeni_egitim)):
    eg = duz(egitim)
    Xe, ye = arr(eg, "alptekin_bloom")
    for ad, mk in MODELLER.items():
        blm[f"{ad} | {ad_set}"] = {**olc(ytb, mk().fit(Xe, ye).predict(Xtb), BL), "egitim_n": len(eg)}
cikti["bloom_test"] = blm


# 3) Bütün dosyada 5x5 çapraz doğrulama
def cv(X, y, siniflar, kural_fn=None):
    cvs = RepeatedStratifiedKFold(n_splits=5, n_repeats=5, random_state=42)
    sonuc = {}
    for ad in list(MODELLER) + (["Kural"] if kural_fn else []):
        f1s, accs = [], []
        for tr, te in cvs.split(X, y):
            p = [kural_fn(s) for s in X[te]] if ad == "Kural" else MODELLER[ad]().fit(X[tr], y[tr]).predict(X[te])
            f1s.append(f1_score(y[te], p, average="macro", labels=siniflar, zero_division=0))
            accs.append(accuracy_score(y[te], p))
        sonuc[ad] = {"macro_f1": round(float(np.mean(f1s)), 3), "f1_sapma": round(float(np.std(f1s)), 3),
                     "dogruluk": round(float(np.mean(accs)), 3)}
    return sonuc


X, y = arr(E, "alptekin_kalite")
cikti["kalite_cv"] = {"n": len(X), "sonuc": cv(X, y, KAL, kural)}
D = duz(E)
X, y = arr(D, "alptekin_bloom")
cikti["bloom_cv"] = {"n": len(X), "sonuc": cv(X, y, BL)}

json.dump(cikti, open(os.path.join(KOK, "final", "sonuc_02.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# okunur çıktı
print(f"Test (RASTGELE) n={len(test)}; ILK_300={len(ilk)}; yeni eğitim={len(yeni_egitim)}")
print("\n== 1) KALİTE, test kümesi ==  dağılım:", kal["test_dagilim"])
for ad, r in kal.items():
    if ad == "test_dagilim":
        continue
    print(f"{ad:50s} mF1 {r['macro_f1']:.3f}  doğ {r['dogruluk']:.3f}  F1 {r['sinif_f1']}  eğitim {r.get('egitim_n','-')}")
    print("   karışıklık (satır gerçek, sütun tahmin; sıra", KAL, "):", r["karisiklik_satir_gercek_sutun_tahmin"])
print(f"\n== 2) BLOOM, test DUZGUN n={len(tb)} == dağılım:", blm["test_dagilim"])
for ad, r in blm.items():
    if isinstance(r, dict) and "macro_f1" in r:
        print(f"{ad:50s} mF1 {r['macro_f1']:.3f}  doğ {r['dogruluk']:.3f}  n {r['n']}  eğitim {r['egitim_n']}")
for k in ("kalite_cv", "bloom_cv"):
    print(f"\n== 3) {k} (n={cikti[k]['n']}) ==")
    for ad, r in cikti[k]["sonuc"].items():
        print(f"{ad:30s} mF1 {r['macro_f1']:.3f} (±{r['f1_sapma']:.3f})  doğ {r['dogruluk']:.3f}")
