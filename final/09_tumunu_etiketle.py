# Final projesi, adım 9: son eğitim (bütün etiketli veri) + bütün ders çıktısı cümlelerini etiketleme.
# Kalite: 795 satır, 3 sınıf, 5 epoch. Bloom: DUZGUN + bloom dolu satırlar, 7 sınıf, 13 epoch. Tohum 42.
# Test/doğrulama ayrılmaz. Modeller proje dışına kaydedilir. Tahmin benzersiz normalleştirilmiş cümle üzerinde yapılır
# (modele o normalleştirilmiş grubun ilk ham hâli verilir; BERTurk büyük/küçük harfe duyarlı olduğundan).
# Çalıştırma:  <venv>/python final/09_tumunu_etiketle.py
import collections, csv, json, os, random, re, time
import numpy as np
import pandas as pd
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer, get_linear_schedule_with_warmup

assert torch.cuda.is_available(), "CUDA yok"
DEV = torch.device("cuda")
MODEL = "dbmdz/bert-base-turkish-cased"
MAXLEN, BATCH, LR, WD, WARM, SEED = 64, 16, 3e-5, 0.01, 0.10, 42
TBATCH = 128
KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CIKIS_MODEL = r"C:\Users\Alptekin Zengin\.venvs\yz-final-model"
KAL = ["BELIRSIZ", "CIKTI_DEGIL", "DUZGUN"]


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


TR = set("çğıöşüÇĞİÖŞÜ")
EN = re.compile(r"\b(the|and|of|to|will|be able|students?|understand|describe|explain|apply)\b", re.I)
ing = lambda s: not (set(s) & TR) and bool(EN.search(s))


def norm(s):
    return low(s).strip().rstrip(".").strip()


tok = AutoTokenizer.from_pretrained(MODEL)
E = list(csv.DictReader(open(os.path.join(KOK, "final", "etiket2", "etiket_kesin_800.csv"), encoding="utf-8-sig")))
assert len(E) == 795, len(E)
DUZ = [r for r in E if r["alptekin_kalite"] == "DUZGUN" and r["alptekin_bloom"]]
BL = sorted({r["alptekin_bloom"] for r in DUZ})
assert len(DUZ) == 405 and len(BL) == 7, (len(DUZ), BL)


def kodla(rows, anahtar, siniflar):
    enc = tok([r["cumle"] for r in rows], truncation=True, max_length=MAXLEN, padding=False)
    return [(enc["input_ids"][i], enc["token_type_ids"][i], siniflar.index(rows[i][anahtar])) for i in range(len(rows))]


def yigin(o):
    m = max(len(x[0]) for x in o)
    ids = torch.tensor([x[0] + [0] * (m - len(x[0])) for x in o])
    tt = torch.tensor([x[1] + [0] * (m - len(x[0])) for x in o])
    am = torch.tensor([[1] * len(x[0]) + [0] * (m - len(x[0])) for x in o])
    return ids.to(DEV), tt.to(DEV), am.to(DEV), torch.tensor([x[2] for x in o]).to(DEV)


def egit(gorev, rows, anahtar, siniflar, epochs):
    k = len(siniflar)
    D = kodla(rows, anahtar, siniflar)
    sayim = np.bincount([o[2] for o in D], minlength=k).astype(float)
    agirlik = torch.tensor(len(D) / (k * np.maximum(sayim, 1)), dtype=torch.float).to(DEV)
    torch.manual_seed(SEED); np.random.seed(SEED); torch.cuda.manual_seed_all(SEED)
    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL, num_labels=k, id2label={i: c for i, c in enumerate(siniflar)}, label2id={c: i for i, c in enumerate(siniflar)}).to(DEV)
    nd = ["bias", "LayerNorm.weight"]
    gr = [{"params": [p for n, p in model.named_parameters() if not any(x in n for x in nd)], "weight_decay": WD},
          {"params": [p for n, p in model.named_parameters() if any(x in n for x in nd)], "weight_decay": 0.0}]
    opt = torch.optim.AdamW(gr, lr=LR)
    adim = epochs * ((len(D) + BATCH - 1) // BATCH)
    sch = get_linear_schedule_with_warmup(opt, int(WARM * adim), adim)
    kayip = torch.nn.CrossEntropyLoss(weight=agirlik)
    g = torch.Generator().manual_seed(SEED)
    t0 = time.time()
    for ep in range(epochs):
        model.train()
        sira = torch.randperm(len(D), generator=g).tolist()
        top = 0.0
        for i in range(0, len(sira), BATCH):
            ids, tt, am, y = yigin([D[j] for j in sira[i:i + BATCH]])
            loss = kayip(model(input_ids=ids, token_type_ids=tt, attention_mask=am).logits, y)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            opt.step(); sch.step(); opt.zero_grad()
            top += loss.item() * len(y)
        print(f"  [{gorev}] epoch {ep+1}/{epochs} kayıp {top/len(D):.4f} ({time.time()-t0:.0f} sn)", flush=True)
    sure = time.time() - t0
    yol = os.path.join(CIKIS_MODEL, gorev)
    os.makedirs(yol, exist_ok=True)
    model.save_pretrained(yol)
    tok.save_pretrained(yol)
    del opt
    return model, sure, len(D)


@torch.no_grad()
def olasilik(model, metinler):
    """metinler -> (n, k) olasılık; uzunluğa göre sıralı, TBATCH'lik gruplar."""
    model.eval()
    sira = sorted(range(len(metinler)), key=lambda i: len(metinler[i]))
    cikti = np.zeros((len(metinler), model.config.num_labels), dtype=np.float32)
    for i in range(0, len(sira), TBATCH):
        idx = sira[i:i + TBATCH]
        enc = tok([metinler[j] for j in idx], truncation=True, max_length=MAXLEN, padding=True, return_tensors="pt").to(DEV)
        p = torch.softmax(model(**enc).logits.float(), -1).cpu().numpy()
        cikti[idx] = p
    return cikti


# ---- eğitim ----
T0 = time.time()
mk, sure_k, n_k = egit("kalite", E, "alptekin_kalite", KAL, 5)
mb, sure_b, n_b = egit("bloom", DUZ, "alptekin_bloom", BL, 13)
egitim_sure = time.time() - T0
print(f"eğitim: kalite {sure_k:.0f} sn (n={n_k}), bloom {sure_b:.0f} sn (n={n_b})", flush=True)

# ---- veri ----
V = pd.read_csv(os.path.join(KOK, "veri", "karabuk_ders_ciktilari.csv"), encoding="utf-8-sig", dtype=str, keep_default_na=False)
toplam = len(V)
V = V[V["cumle"].str.strip() != ""].reset_index(drop=True)
bos = toplam - len(V)
V["_ing"] = V["cumle"].map(ing)
V["_n"] = V["cumle"].map(norm)
S = V[~V["_ing"]]
temsil = {}  # norm -> ilk ham cümle
for n, c in zip(S["_n"], S["cumle"]):
    temsil.setdefault(n, c)
anahtarlar = list(temsil)
metinler = [temsil[a] for a in anahtarlar]
print(f"toplam {toplam}, boş {bos}, İngilizce {int(V['_ing'].sum())}, sınıflanan {len(S)}, benzersiz {len(anahtarlar)}", flush=True)

T1 = time.time()
pk = olasilik(mk, metinler)
kal_i = pk.argmax(1)
kal = {a: KAL[i] for a, i in zip(anahtarlar, kal_i)}
kalg = {a: float(pk[j, kal_i[j]]) for j, a in enumerate(anahtarlar)}
duz_idx = [j for j, a in enumerate(anahtarlar) if kal[a] == "DUZGUN"]
pb = olasilik(mb, [metinler[j] for j in duz_idx])
blo, blog = {}, {}
for r, j in enumerate(duz_idx):
    i = int(pb[r].argmax())
    blo[anahtarlar[j]], blog[anahtarlar[j]] = BL[i], float(pb[r, i])
tahmin_sure = time.time() - T1
print(f"tahmin {tahmin_sure:.0f} sn (bloom {len(duz_idx)} cümle)", flush=True)

# ---- çıktı ----
elle = {}
for r in E:
    elle.setdefault(norm(r["cumle"]), r)
kol_k, kol_kg, kol_b, kol_bg, kol_kural, kol_ek, kol_eb = [], [], [], [], [], [], []
for c, n, en in zip(V["cumle"], V["_n"], V["_ing"]):
    if en:
        kol_k.append("INGILIZCE"); kol_kg.append(""); kol_b.append(""); kol_bg.append(""); kol_kural.append("")
    else:
        kol_k.append(kal[n]); kol_kg.append(f"{kalg[n]:.3f}")
        kol_b.append(blo.get(n, "")); kol_bg.append(f"{blog[n]:.3f}" if n in blog else ""); kol_kural.append(kural(c))
    e = elle.get(n)
    kol_ek.append(e["alptekin_kalite"] if e else ""); kol_eb.append(e["alptekin_bloom"] if e else "")
orijinal = [c for c in V.columns if not c.startswith("_")]
O = V[orijinal].copy()
O["kalite"], O["kalite_guven"], O["bloom"], O["bloom_guven"], O["kural"], O["elle_kalite"], O["elle_bloom"] = \
    kol_k, kol_kg, kol_b, kol_bg, kol_kural, kol_ek, kol_eb
yol_csv = os.path.join(KOK, "final", "tum_etiketler.csv")
O.to_csv(yol_csv, index=False, encoding="utf-8-sig")

# ---- özet ----
Sn = O[O["kalite"] != "INGILIZCE"]
pct = lambda d, n: {k: {"sayi": int(v), "yuzde": round(100 * v / n, 2)} for k, v in sorted(d.items())}
kd = Sn["kalite"].value_counts().to_dict()
Dz = Sn[Sn["kalite"] == "DUZGUN"]
bd = Dz["bloom"].value_counts().to_dict()
ayni = (Sn["kalite"] == Sn["kural"])
capraz = {k: {m: int(((Sn["kalite"] == m) & (Sn["kural"] == k)).sum()) for m in KAL} for k in KAL}
ek = O[O["elle_kalite"] != ""]
ek_ok = (ek["kalite"] == ek["elle_kalite"])
eb = O[(O["elle_bloom"] != "") & (O["bloom"] != "")]
ozet = {
    "toplam_satir": toplam, "bos_atilan": bos, "ingilizce": int(V["_ing"].sum()), "siniflanan_satir": len(Sn),
    "benzersiz_cumle": len(anahtarlar), "cikti_satir": len(O),
    "kalite_dagilimi_satir": pct(O["kalite"].value_counts().to_dict(), len(O)),
    "bloom_dagilimi_DUZGUN_icinde": pct(bd, len(Dz)),
    "model_kural_ayni_oran": round(float(ayni.mean()), 4), "model_kural_ayni_satir": int(ayni.sum()),
    "capraz_tablo_satir_kural_sutun_model": capraz,
    "kalite_guven_alti_0_6_satir": int((Sn["kalite_guven"].astype(float) < 0.6).sum()),
    "bloom_guven_alti_0_5_satir": int((Dz["bloom_guven"].astype(float) < 0.5).sum()),
    "elle_etiketli_satir": len(ek), "elle_kalite_model_esit_oran": round(float(ek_ok.mean()), 4),
    "elle_bloom_karsilastirilan_satir": len(eb), "elle_bloom_model_esit_oran": round(float((eb["bloom"] == eb["elle_bloom"]).mean()), 4) if len(eb) else None,
    "sure_sn": {"egitim_toplam": round(egitim_sure, 1), "egitim_kalite": round(sure_k, 1), "egitim_bloom": round(sure_b, 1),
                "tahmin": round(tahmin_sure, 1)},
    "egitim": {"kalite_n": n_k, "kalite_epoch": 5, "bloom_n": n_b, "bloom_epoch": 13, "tohum": SEED,
               "model_klasoru": CIKIS_MODEL, "tahmin_metni": "benzersiz norm grubunun ilk ham cümlesi"},
}
json.dump(ozet, open(os.path.join(KOK, "final", "tum_etiketler_ozet.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ---- kontroller ----
O2 = pd.read_csv(yol_csv, encoding="utf-8-sig", dtype=str, keep_default_na=False)
k1 = len(O2) == toplam - bos
k2 = set(O2["kalite"]) <= {"DUZGUN", "BELIRSIZ", "CIKTI_DEGIL", "INGILIZCE"}
k3 = bool((O2.loc[O2["kalite"] != "DUZGUN", ["bloom", "bloom_guven"]] == "").all().all())
k3b = bool((O2.loc[O2["kalite"] == "DUZGUN", "bloom"] != "").all())
print("KONTROL satır sayısı:", k1, len(O2), toplam - bos)
print("KONTROL kalite değerleri:", k2, sorted(set(O2["kalite"])))
print("KONTROL DUZGUN dışı bloom boş:", k3, "| DUZGUN hepsinde bloom dolu:", k3b)

del mk, mb
torch.cuda.empty_cache()
rk = AutoModelForSequenceClassification.from_pretrained(os.path.join(CIKIS_MODEL, "kalite")).to(DEV)
rb = AutoModelForSequenceClassification.from_pretrained(os.path.join(CIKIS_MODEL, "bloom")).to(DEV)
print("id2label kalite:", rk.config.id2label, "| bloom:", rb.config.id2label)
tok2 = AutoTokenizer.from_pretrained(os.path.join(CIKIS_MODEL, "kalite"))
ornek = [metinler[j] for j in duz_idx[:2]] + [metinler[next(j for j, a in enumerate(anahtarlar) if kal[a] != "DUZGUN")]]
ok_y = True
for m, ad, ref_kalite in ((rk, "kalite", True), (rb, "bloom", False)):
    for s in ornek:
        n = norm(s)
        if not ref_kalite and n not in blo:
            continue
        p = olasilik(m, [s])[0]
        beklenen = kal[n] if ref_kalite else blo[n]
        ad_t = m.config.id2label[int(p.argmax())]
        ok_y &= (ad_t == beklenen)
        print(f"  yeniden yükleme {ad}: {ad_t} (beklenen {beklenen}) | {s[:70]}")
print("KONTROL yeniden yükleme aynı tahmin:", ok_y)

# ---- rapor örnekleri ----
print("\n=== EN EMİN / EN EMİN OLMADIĞI ===")
for ci, c in enumerate(KAL):
    idx = [j for j in range(len(anahtarlar)) if kal_i[j] == ci]
    idx.sort(key=lambda j: -pk[j, ci])
    for etiket, sec in (("en emin", idx[:2]), ("en emin değil", idx[-2:])):
        for j in sec:
            print(f"{c} | {etiket} | {pk[j, ci]:.3f} | {metinler[j]}")
print("\n=== MODEL-KURAL AYRIŞAN 6 ===")
rng = random.Random(SEED)
ay = Sn[~ayni].drop_duplicates("cumle")
for _, r in ay.iloc[rng.sample(range(len(ay)), 6)].iterrows():
    print(f"model {r['kalite']} ({r['kalite_guven']}) | kural {r['kural']} | {r['cumle']}")
print("\nÖZET:", json.dumps(ozet, ensure_ascii=False, indent=1))
