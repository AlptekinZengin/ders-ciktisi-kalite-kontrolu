# Final projesi, adım 2: etiketlenecek 500 yeni cümleyi seçer (4 grup, seed 42).
# Çalıştırma (yz-dersi klasöründe):  py -3 final/02_cumle_sec.py
import os, re, json, collections
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline, make_union
from sklearn.linear_model import LogisticRegression

SEED = 42
KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CIK = os.path.join(KOK, "final", "etiket2")
os.makedirs(CIK, exist_ok=True)


def low(s):
    return s.replace("I", "ı").replace("İ", "i").lower()


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


TR = set("çğıöşüÇĞİÖŞÜ")
EN = re.compile(r"\b(the|and|of|to|will|be able|students?|understand|describe|explain|apply)\b", re.I)
ing = lambda s: not (set(s) & TR) and bool(EN.search(s))


def norm(s):
    return low(s).strip().rstrip(".").strip()


def model():
    return make_pipeline(ozellik(), LogisticRegression(class_weight="balanced", max_iter=2000, C=10))


# 1) havuz
V = pd.read_csv(os.path.join(KOK, "veri", "karabuk_ders_ciktilari.csv"), encoding="utf-8-sig", dtype=str, keep_default_na=False)
E = pd.read_csv(os.path.join(KOK, "kalite-rapor", "etiket", "etiket_kesin.csv"), encoding="utf-8-sig", dtype=str, keep_default_na=False)
n_ham = len(V)
V = V[V["cumle"].str.strip() != ""]
V = V[~V["cumle"].map(ing)]
V = V.assign(_n=V["cumle"].map(norm))
V = V[V["_n"] != ""].drop_duplicates("_n", keep="first")
eski = set(E["cumle"].map(norm))
V = V[~V["_n"].isin(eski)].reset_index(drop=True)
print("havuz:", len(V))

# 2) modeller
mk = model().fit(E["cumle"].tolist(), E["alptekin_kalite"].tolist())
D = E[(E["alptekin_kalite"] == "DUZGUN") & (E["alptekin_bloom"] != "")]
mb = model().fit(D["cumle"].tolist(), D["alptekin_bloom"].tolist())

# 3) havuz tahminleri
V["kural"] = V["cumle"].map(kural)
pk = mk.predict_proba(V["cumle"].tolist())
pb = mb.predict_proba(V["cumle"].tolist())
kc, bc = mk.classes_, mb.classes_
V["k_tahmin"] = kc[pk.argmax(1)]
V["b_tahmin"] = bc[pb.argmax(1)]
sk = np.sort(pk, axis=1)
V["k_fark"] = sk[:, -1] - sk[:, -2]
sb = np.sort(pb, axis=1)
V["b_fark"] = sb[:, -1] - sb[:, -2]

rng = np.random.RandomState(SEED)
secilen = {}  # indeks -> grup
ders_say = collections.Counter()
prog_say = collections.Counter()


def al(idx, grup, kisitli):
    if idx in secilen:
        return False
    r = V.loc[idx]
    if kisitli and (ders_say[r["ders_id"]] >= 1 or prog_say[r["program"]] >= 8):
        return False
    secilen[idx] = grup
    ders_say[r["ders_id"]] += 1
    prog_say[r["program"]] += 1
    return True


def sec(adaylar, n, grup, kisitli=True):
    c = 0
    for i in adaylar:
        if c >= n:
            break
        c += al(i, grup, kisitli)
    return c


def rastgele_sirala(idx):
    idx = np.array(list(idx))
    return list(idx[rng.permutation(len(idx))])


sayi = {}
sayi["RASTGELE"] = sec(rastgele_sirala(V.index), 100, "RASTGELE", kisitli=False)
sayi["CIKTI_DEGIL_ADAY"] = sec(rastgele_sirala(V.index[V["kural"] == "CIKTI_DEGIL"]), 150, "CIKTI_DEGIL_ADAY")
kar_sira = list(V["k_fark"].sort_values(kind="stable").index)
sayi["KALITE_KARARSIZ"] = sec(kar_sira, 150, "KALITE_KARARSIZ")
duz = V[V["k_tahmin"] == "DUZGUN"]
a = sec(list(duz["b_fark"].sort_values(kind="stable").index), 50, "BLOOM")
yuksek = duz.index[duz["b_tahmin"].isin(["DEGERLENDIRME", "YARATMA", "ANALIZ"])]
b = sec(rastgele_sirala([i for i in yuksek if i not in secilen]), 50, "BLOOM")
sayi["BLOOM"] = a + b
bloom_alt = {"belirsiz_fark": a, "ust_duzey_rastgele": b}
hedef = {"RASTGELE": 100, "CIKTI_DEGIL_ADAY": 150, "KALITE_KARARSIZ": 150, "BLOOM": 100}
toplam_eksik = sum(hedef[g] - sayi[g] for g in hedef)
tamam = 0
if toplam_eksik:
    tamam = sec(kar_sira, toplam_eksik, "KALITE_KARARSIZ")
    sayi["KALITE_KARARSIZ"] += tamam
print("grup sayıları:", sayi, "eksik:", toplam_eksik, "tamamlanan:", tamam)

S = V.loc[list(secilen)].copy()
S["secim_grubu"] = [secilen[i] for i in S.index]
S = S.sample(frac=1, random_state=SEED).reset_index(drop=True)
S.insert(0, "no", range(1, len(S) + 1))
kol = ["no", "cumle", "ders_kodu", "ders_adi", "program", "birim", "seviye", "yariyil", "ders_id", "secim_grubu"]
S[kol].to_csv(os.path.join(CIK, "ornek_500.csv"), index=False, encoding="utf-8-sig")
P = S[[k for k in kol if k != "secim_grubu"]]
for j, (a_, b_) in enumerate([(0, 167), (167, 334), (334, 500)], 1):
    P.iloc[a_:b_].to_csv(os.path.join(CIK, f"parca_{j}.csv"), index=False, encoding="utf-8-sig")

# yeniden etiketleme: 300 cümleden 100
Y = E.sample(n=100, random_state=SEED).reset_index(drop=True)
Y = pd.DataFrame({"no": Y["no"], "cumle": Y["cumle"], "kalite": "", "bloom": ""})
Y.to_csv(os.path.join(CIK, "yeniden_100.csv"), index=False, encoding="utf-8-sig")

ozet = {
    "ham_satir": n_ham,
    "havuz_buyuklugu": len(V),
    "secilen_toplam": len(S),
    "grup_sayilari": sayi,
    "bloom_alt_gruplar": bloom_alt,
    "eksik_tamamlanan_KALITE_KARARSIZ": tamam,
    "farkli_program": int(S["program"].nunique()),
    "farkli_ders_id": int(S["ders_id"].nunique()),
    "en_cok_cumle_olan_program": max(collections.Counter(S["program"]).values()),
    "seviye_dagilimi": dict(S["seviye"].value_counts()),
    "kural_sonucu_dagilimi": dict(S["kural"].value_counts()),
    "kalite_modeli_tahmin_dagilimi": dict(S["k_tahmin"].value_counts()),
    "not": "RASTGELE grubu kısıtsızdır ama seçimi ders/program sayaçlarına işlenir; sonraki gruplar kalan kotayla sınırlıdır.",
}
json.dump(ozet, open(os.path.join(CIK, "secim_ozet.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=int)

# kontroller
O = pd.read_csv(os.path.join(CIK, "ornek_500.csv"), encoding="utf-8-sig", dtype=str, keep_default_na=False)
ps = [pd.read_csv(os.path.join(CIK, f"parca_{j}.csv"), encoding="utf-8-sig", dtype=str) for j in (1, 2, 3)]
yy = pd.read_csv(os.path.join(CIK, "yeniden_100.csv"), encoding="utf-8-sig", dtype=str, keep_default_na=False)
print("KONTROL satır 500:", len(O) == 500)
print("KONTROL tekrar yok:", O["cumle"].map(norm).is_unique)
print("KONTROL eski 300 yok:", not (set(O["cumle"].map(norm)) & eski))
print("KONTROL İngilizce yok:", not O["cumle"].map(ing).any())
print("KONTROL parça toplamı:", [len(p) for p in ps], sum(len(p) for p in ps) == 500, "secim_grubu yok:", all("secim_grubu" not in p.columns for p in ps))
print("KONTROL yeniden_100:", len(yy), (yy["kalite"] == "").all() and (yy["bloom"] == "").all(), list(yy.columns))
print("KONTROL ders_id tekrarı (RASTGELE dışı):", O[O.secim_grubu != "RASTGELE"]["ders_id"].duplicated().sum())
print(json.dumps(ozet, ensure_ascii=False, indent=1, default=int))
for g, d in O.groupby("secim_grubu"):
    print("\n", g)
    for c in d["cumle"].head(3):
        print("  -", c)
