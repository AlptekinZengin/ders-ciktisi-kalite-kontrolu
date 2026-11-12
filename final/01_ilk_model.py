# Final projesi, adım 1: 300 etiketli cümleyle ilk deneme.
# Kural tabanlı yöntem ile TF-IDF + doğrusal modelleri aynı cümlelerde karşılaştırır.
# Çalıştırma (yz-dersi klasöründe):  py -3 final/01_ilk_model.py
import csv, json, os, re, collections
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline, make_union
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.metrics import f1_score, accuracy_score, confusion_matrix

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = list(csv.DictReader(open(os.path.join(KOK, "kalite-rapor", "etiket", "etiket_kesin.csv"), encoding="utf-8-sig")))


def low(s):
    return s.replace("I", "ı").replace("İ", "i").lower()


# --- Kural tabanlı yöntem (vize raporundaki hâliyle, analiz.py'den aynen) ---
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
    # kelime (1-2'li) ve harf parçası (2-5'li) sayımları birlikte
    return make_union(
        TfidfVectorizer(preprocessor=low, analyzer="word", ngram_range=(1, 2), sublinear_tf=True),
        TfidfVectorizer(preprocessor=low, analyzer="char_wb", ngram_range=(2, 5), sublinear_tf=True),
    )


MODELLER = {
    "TF-IDF + SVM": lambda: make_pipeline(ozellik(), LinearSVC(class_weight="balanced")),
    "TF-IDF + lojistik regresyon": lambda: make_pipeline(ozellik(), LogisticRegression(class_weight="balanced", max_iter=2000, C=10)),
}


def dene(X, y, kural_fn=None, kat=5, tekrar=5):
    X, y = np.array(X, dtype=object), np.array(y)
    siniflar = sorted(set(y))
    cv = RepeatedStratifiedKFold(n_splits=kat, n_repeats=tekrar, random_state=42)
    sonuc = {}
    adlar = list(MODELLER) + (["Kural"] if kural_fn else [])
    for ad in adlar:
        f1, acc = [], []
        km = np.zeros((len(siniflar), len(siniflar)), dtype=int)
        for tr, te in cv.split(X, y):
            if ad == "Kural":
                p = [kural_fn(s) for s in X[te]]
            else:
                m = MODELLER[ad]().fit(X[tr], y[tr])
                p = m.predict(X[te])
            f1.append(f1_score(y[te], p, average="macro", labels=siniflar, zero_division=0))
            acc.append(accuracy_score(y[te], p))
            km += confusion_matrix(y[te], p, labels=siniflar)
        sonuc[ad] = {"macro_f1": round(float(np.mean(f1)), 3), "f1_sapma": round(float(np.std(f1)), 3),
                     "dogruluk": round(float(np.mean(acc)), 3),
                     "karisiklik": (km / tekrar).round(1).tolist()}
    return siniflar, sonuc


def yaz(baslik, siniflar, sonuc, n):
    print(f"\n=== {baslik} (n = {n}) ===")
    print("sınıflar:", ", ".join(siniflar))
    for ad, r in sorted(sonuc.items(), key=lambda kv: -kv[1]["macro_f1"]):
        print(f"  {ad:30s} macro-F1 {r['macro_f1']:.3f} (±{r['f1_sapma']:.3f})   doğruluk {r['dogruluk']:.3f}")


cikti = {}

# 1) Kalite: düzgün / belirsiz / çıktı değil
X = [r["cumle"] for r in E]
y = [r["alptekin_kalite"] for r in E]
s, r = dene(X, y, kural_fn=kural)
yaz("KALİTE", s, r, len(X))
cikti["kalite"] = {"n": len(X), "siniflar": s, "dagilim": dict(collections.Counter(y)), "sonuc": r}

# 2) Bloom: yalnız düzgün cümleler
D = [r for r in E if r["alptekin_kalite"] == "DUZGUN" and r["alptekin_bloom"]]
X = [r["cumle"] for r in D]
y = [r["alptekin_bloom"] for r in D]
s, r = dene(X, y)
yaz("BLOOM", s, r, len(X))
cikti["bloom"] = {"n": len(X), "siniflar": s, "dagilim": dict(collections.Counter(y)), "sonuc": r}

yol = os.path.join(KOK, "final", "sonuc_01.json")
json.dump(cikti, open(yol, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("\nKaydedildi:", yol)
