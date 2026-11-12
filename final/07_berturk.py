# Final projesi, adım 7: BERTurk (dbmdz/bert-base-turkish-cased) ince ayarı, kalite ve Bloom.
# Bölme 06_model_800.py ile aynı: test = secim_grubu RASTGELE (eğitimde kullanılmaz).
# Ayarlar sabit: max_length 64, batch 16, lr 3e-5, 5 epoch, weight decay 0.01, ısınma %10,
# sınıf ağırlıklı çapraz entropi. Doğrulama kümesi eğitim kümesinin içinden ayrılır (%10, tabakalı);
# test kümesine bakılarak hiçbir ayar değiştirilmez, son epoch'un modeli sınanır.
# Model ağırlığı/checkpoint diske yazılmaz.
# Çalıştırma:  <venv>/python final/07_berturk.py [--seeds 42 43 44] [--epochs 5] [--hizli]
import argparse, csv, json, os, time
import numpy as np
import torch
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score
from sklearn.model_selection import train_test_split
from transformers import AutoModelForSequenceClassification, AutoTokenizer, get_linear_schedule_with_warmup

ap = argparse.ArgumentParser()
ap.add_argument("--seeds", type=int, nargs="+", default=[42, 43, 44])
ap.add_argument("--epochs", type=int, default=5)
ap.add_argument("--hizli", action="store_true", help="1 epoch deneme, süre ölç, dosya yazma")
args = ap.parse_args()

MODEL = "dbmdz/bert-base-turkish-cased"
MAXLEN, BATCH, LR, WD, WARM = 64, 16, 3e-5, 0.01, 0.10
KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = list(csv.DictReader(open(os.path.join(KOK, "final", "etiket2", "etiket_kesin_800.csv"), encoding="utf-8-sig")))
KAL = ["BELIRSIZ", "CIKTI_DEGIL", "DUZGUN"]

test = [r for r in E if r["secim_grubu"] == "RASTGELE"]
egit = [r for r in E if r["secim_grubu"] != "RASTGELE"]
assert not ({r["cumle"] for r in test} & {r["cumle"] for r in egit})
duz = lambda rows: [r for r in rows if r["alptekin_kalite"] == "DUZGUN" and r["alptekin_bloom"]]
BL = sorted({r["alptekin_bloom"] for r in duz(E)})
GOREVLER = {
    "kalite": ("alptekin_kalite", KAL, egit, test),
    "bloom": ("alptekin_bloom", BL, duz(egit), duz(test)),
}
tok = AutoTokenizer.from_pretrained(MODEL)


def kodla(rows, anahtar, siniflar):
    enc = tok([r["cumle"] for r in rows], truncation=True, max_length=MAXLEN, padding=False)
    y = [siniflar.index(r[anahtar]) for r in rows]
    return [(enc["input_ids"][i], enc["token_type_ids"][i], y[i]) for i in range(len(rows))]


def yigin(ornekler):
    m = max(len(o[0]) for o in ornekler)
    ids = torch.tensor([o[0] + [0] * (m - len(o[0])) for o in ornekler])
    tt = torch.tensor([o[1] + [0] * (m - len(o[1])) for o in ornekler])
    am = torch.tensor([[1] * len(o[0]) + [0] * (m - len(o[0])) for o in ornekler])
    return ids, tt, am, torch.tensor([o[2] for o in ornekler])


@torch.no_grad()
def tahmin(model, ornekler):
    model.eval()
    p = []
    for i in range(0, len(ornekler), 64):
        ids, tt, am, _ = yigin(ornekler[i:i + 64])
        p += model(input_ids=ids, token_type_ids=tt, attention_mask=am).logits.argmax(-1).tolist()
    return p


def olc(y, p, k):
    lab = list(range(k))
    return {"macro_f1": float(f1_score(y, p, average="macro", labels=lab, zero_division=0)),
            "dogruluk": float(accuracy_score(y, p)),
            "sinif_f1": [float(v) for v in f1_score(y, p, average=None, labels=lab, zero_division=0)],
            "karisiklik": confusion_matrix(y, p, labels=lab).tolist()}


def calistir(gorev, seed, epochs):
    anahtar, siniflar, egitim_h, test_h = GOREVLER[gorev]
    k = len(siniflar)
    y_h = [r[anahtar] for r in egitim_h]
    try:
        tr, va = train_test_split(range(len(egitim_h)), test_size=0.10, random_state=seed, stratify=y_h)
    except ValueError:
        tr, va = train_test_split(range(len(egitim_h)), test_size=0.10, random_state=seed)
    tr_rows, va_rows = [egitim_h[i] for i in tr], [egitim_h[i] for i in va]
    D_tr, D_va, D_te = (kodla(x, anahtar, siniflar) for x in (tr_rows, va_rows, test_h))
    sayim = np.bincount([o[2] for o in D_tr], minlength=k).astype(float)
    agirlik = torch.tensor(len(D_tr) / (k * np.maximum(sayim, 1)), dtype=torch.float)
    torch.manual_seed(seed); np.random.seed(seed)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL, num_labels=k)
    nd = ["bias", "LayerNorm.weight"]
    gruplar = [{"params": [p for n, p in model.named_parameters() if not any(x in n for x in nd)], "weight_decay": WD},
               {"params": [p for n, p in model.named_parameters() if any(x in n for x in nd)], "weight_decay": 0.0}]
    opt = torch.optim.AdamW(gruplar, lr=LR)
    adim = epochs * ((len(D_tr) + BATCH - 1) // BATCH)
    sch = get_linear_schedule_with_warmup(opt, int(WARM * adim), adim)
    kayip = torch.nn.CrossEntropyLoss(weight=agirlik)
    g = torch.Generator().manual_seed(seed)
    t0 = time.time()
    val_egri = []
    for ep in range(epochs):
        model.train()
        sira = torch.randperm(len(D_tr), generator=g).tolist()
        top = 0.0
        for i in range(0, len(sira), BATCH):
            ids, tt, am, y = yigin([D_tr[j] for j in sira[i:i + BATCH]])
            loss = kayip(model(input_ids=ids, token_type_ids=tt, attention_mask=am).logits, y)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            opt.step(); sch.step(); opt.zero_grad()
            top += loss.item() * len(y)
        pv = tahmin(model, D_va)
        vf = float(f1_score([o[2] for o in D_va], pv, average="macro", labels=list(range(k)), zero_division=0))
        val_egri.append({"epoch": ep + 1, "egitim_kaybi": round(top / len(D_tr), 4), "val_macro_f1": round(vf, 4)})
        print(f"  [{gorev} tohum {seed}] epoch {ep+1}/{epochs} kayıp {top/len(D_tr):.4f} val mF1 {vf:.3f}  ({time.time()-t0:.0f} sn)", flush=True)
    pt = tahmin(model, D_te)
    s = olc([o[2] for o in D_te], pt, k)
    s.update({"tohum": seed, "egitim_n": len(D_tr), "val_n": len(D_va), "test_n": len(D_te),
              "sure_sn": round(time.time() - t0, 1), "val_egri": val_egri})
    del model, opt
    return s


if args.hizli:
    for gorev in GOREVLER:
        t = time.time()
        s = calistir(gorev, 42, 1)
        print(f"HIZLI {gorev}: 1 epoch {s['sure_sn']} sn (test mF1 {s['macro_f1']:.3f}), egitim_n {s['egitim_n']}", flush=True)
    raise SystemExit

s02 = json.load(open(os.path.join(KOK, "final", "sonuc_02.json"), encoding="utf-8"))
kt, bt = s02["kalite_test"], s02["bloom_test"]
al = lambda d: {"macro_f1": d["macro_f1"], "dogruluk": d["dogruluk"]}
karsilastirma = {
    "kalite": {"Kural": al(kt["Kural"]), "TF-IDF + SVM | ILK_300_ve_yeni": al(kt["TF-IDF + SVM | ILK_300_ve_yeni"]),
               "TF-IDF + lojistik regresyon | ILK_300_ve_yeni": al(kt["TF-IDF + lojistik regresyon | ILK_300_ve_yeni"])},
    "bloom": {"TF-IDF + SVM | ILK_300_ve_yeni": al(bt["TF-IDF + SVM | ILK_300_ve_yeni"]),
              "TF-IDF + lojistik regresyon | ILK_300_ve_yeni": al(bt["TF-IDF + lojistik regresyon | ILK_300_ve_yeni"])},
}
cikti = {"model": MODEL, "ayarlar": {"max_length": MAXLEN, "batch": BATCH, "lr": LR, "epoch": args.epochs, "weight_decay": WD,
                                     "isinma": WARM, "kayip": "sinif agirlikli CE", "val": "egitimin %10'u, tabakali",
                                     "sinanan_model": "son epoch", "tohumlar": args.seeds, "sapma": "np.std (ddof=0)"},
         "torch": torch.__version__, "karsilastirma_sonuc_02": karsilastirma, "berturk": {}}
yol = os.path.join(KOK, "final", "sonuc_03.json")
T0 = time.time()
for gorev, (anahtar, siniflar, egitim_h, test_h) in GOREVLER.items():
    r = {"siniflar": siniflar, "egitim_havuzu_n": len(egitim_h), "test_n": len(test_h), "tohumlar": []}
    cikti["berturk"][gorev] = r
    for seed in args.seeds:
        r["tohumlar"].append(calistir(gorev, seed, args.epochs))
        ts = r["tohumlar"]
        for m in ("macro_f1", "dogruluk"):
            v = [x[m] for x in ts]
            r[m + "_ort"], r[m + "_sapma"] = float(np.mean(v)), float(np.std(v))
        r["sinif_f1_ort"] = np.mean([x["sinif_f1"] for x in ts], axis=0).tolist()
        r["karisiklik_ort_satir_gercek_sutun_tahmin"] = np.mean([x["karisiklik"] for x in ts], axis=0).round(2).tolist()
        cikti["toplam_sure_sn"] = round(time.time() - T0, 1)
        json.dump(cikti, open(yol, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{gorev}: mF1 {r['macro_f1_ort']:.3f} ± {r['macro_f1_sapma']:.3f}, doğ {r['dogruluk_ort']:.3f}", flush=True)
print("toplam sn", cikti["toplam_sure_sn"])
