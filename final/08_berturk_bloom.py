# Final projesi, adım 8: BERTurk Bloom, ekran kartı, erken durdurma.
# Bölme 06/07 ile aynı: test = secim_grubu RASTGELE + DUZGUN + bloom dolu (eğitimde/ayar seçiminde kullanılmaz).
# Eğitim havuzunun %15'i tabakalı doğrulama (tohuma bağlı). Doğrulama macro-F1 5 epoch iyileşmezse durur;
# doğrulamada en iyi epoch'un ağırlıklarıyla (bellekte tutulur, diske yazılmaz) teste girilir.
# Çalıştırma:  <venv>/python final/08_berturk_bloom.py
import copy, csv, json, os, time
import numpy as np
import torch
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score
from sklearn.model_selection import train_test_split
from transformers import AutoModelForSequenceClassification, AutoTokenizer, get_linear_schedule_with_warmup

assert torch.cuda.is_available(), "CUDA yok"
DEV = torch.device("cuda")
MODEL = "dbmdz/bert-base-turkish-cased"
MAXLEN, BATCH, LR, WD, WARM, MAXEP, SABIR, VAL = 64, 16, 3e-5, 0.01, 0.10, 20, 5, 0.15
SEEDS = [42, 43, 44, 45, 46]
KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = list(csv.DictReader(open(os.path.join(KOK, "final", "etiket2", "etiket_kesin_800.csv"), encoding="utf-8-sig")))
test = [r for r in E if r["secim_grubu"] == "RASTGELE"]
egit = [r for r in E if r["secim_grubu"] != "RASTGELE"]
assert not ({r["cumle"] for r in test} & {r["cumle"] for r in egit})
duz = lambda rows: [r for r in rows if r["alptekin_kalite"] == "DUZGUN" and r["alptekin_bloom"]]
BL = sorted({r["alptekin_bloom"] for r in duz(E)})
pool, test_h = duz(egit), duz(test)
K = len(BL)
tok = AutoTokenizer.from_pretrained(MODEL)


def kodla(rows):
    enc = tok([r["cumle"] for r in rows], truncation=True, max_length=MAXLEN, padding=False)
    return [(enc["input_ids"][i], enc["token_type_ids"][i], BL.index(rows[i]["alptekin_bloom"])) for i in range(len(rows))]


def yigin(o):
    m = max(len(x[0]) for x in o)
    ids = torch.tensor([x[0] + [0] * (m - len(x[0])) for x in o])
    tt = torch.tensor([x[1] + [0] * (m - len(x[0])) for x in o])
    am = torch.tensor([[1] * len(x[0]) + [0] * (m - len(x[0])) for x in o])
    return ids.to(DEV), tt.to(DEV), am.to(DEV), torch.tensor([x[2] for x in o]).to(DEV)


@torch.no_grad()
def tahmin(model, o):
    model.eval()
    p = []
    for i in range(0, len(o), 64):
        ids, tt, am, _ = yigin(o[i:i + 64])
        p += model(input_ids=ids, token_type_ids=tt, attention_mask=am).logits.argmax(-1).tolist()
    return p


def mf1(y, p):
    return float(f1_score(y, p, average="macro", labels=list(range(K)), zero_division=0))


def calistir(seed):
    y_h = [r["alptekin_bloom"] for r in pool]
    tr, va = train_test_split(range(len(pool)), test_size=VAL, random_state=seed, stratify=y_h)
    D_tr, D_va, D_te = (kodla(x) for x in ([pool[i] for i in tr], [pool[i] for i in va], test_h))
    sayim = np.bincount([o[2] for o in D_tr], minlength=K).astype(float)
    agirlik = torch.tensor(len(D_tr) / (K * np.maximum(sayim, 1)), dtype=torch.float).to(DEV)
    torch.manual_seed(seed); np.random.seed(seed); torch.cuda.manual_seed_all(seed)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL, num_labels=K).to(DEV)
    nd = ["bias", "LayerNorm.weight"]
    gr = [{"params": [p for n, p in model.named_parameters() if not any(x in n for x in nd)], "weight_decay": WD},
          {"params": [p for n, p in model.named_parameters() if any(x in n for x in nd)], "weight_decay": 0.0}]
    opt = torch.optim.AdamW(gr, lr=LR)
    adim = MAXEP * ((len(D_tr) + BATCH - 1) // BATCH)  # çizelge en çok 20 epoch üzerinden
    sch = get_linear_schedule_with_warmup(opt, int(WARM * adim), adim)
    kayip = torch.nn.CrossEntropyLoss(weight=agirlik)
    g = torch.Generator().manual_seed(seed)
    t0 = time.time()
    egri, en_iyi, en_ep, en_state, bekle = [], -1.0, 0, None, 0
    yv = [o[2] for o in D_va]
    for ep in range(1, MAXEP + 1):
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
        vf = mf1(yv, tahmin(model, D_va))
        egri.append({"epoch": ep, "egitim_kaybi": round(top / len(D_tr), 4), "val_macro_f1": round(vf, 4)})
        print(f"  [tohum {seed}] epoch {ep} kayıp {top/len(D_tr):.4f} val mF1 {vf:.3f} ({time.time()-t0:.0f} sn)", flush=True)
        if vf > en_iyi:
            en_iyi, en_ep, bekle = vf, ep, 0
            en_state = {k: v.detach().clone() for k, v in model.state_dict().items()}
        else:
            bekle += 1
            if bekle >= SABIR:
                break
    model.load_state_dict(en_state)
    yt = [o[2] for o in D_te]
    pt = tahmin(model, D_te)
    lab = list(range(K))
    s = {"tohum": seed, "durdugu_epoch": ep, "en_iyi_epoch": en_ep, "val_macro_f1": round(en_iyi, 4),
         "test_macro_f1": mf1(yt, pt), "test_dogruluk": float(accuracy_score(yt, pt)),
         "sinif_f1": [float(v) for v in f1_score(yt, pt, average=None, labels=lab, zero_division=0)],
         "karisiklik": confusion_matrix(yt, pt, labels=lab).tolist(),
         "egitim_n": len(D_tr), "val_n": len(D_va), "test_n": len(D_te), "sure_sn": round(time.time() - t0, 1), "val_egri": egri}
    del model, opt, en_state
    torch.cuda.empty_cache()
    return s


s02 = json.load(open(os.path.join(KOK, "final", "sonuc_02.json"), encoding="utf-8"))["bloom_test"]
s03 = json.load(open(os.path.join(KOK, "final", "sonuc_03.json"), encoding="utf-8"))["berturk"]["bloom"]
al = lambda d: {"macro_f1": d["macro_f1"], "dogruluk": d["dogruluk"], "sinif_f1": d["sinif_f1"]}
cikti = {"model": MODEL, "torch": torch.__version__, "cihaz": torch.cuda.get_device_name(0), "siniflar": BL,
         "ayarlar": {"max_length": MAXLEN, "batch": BATCH, "lr": LR, "weight_decay": WD, "isinma": WARM, "kayip": "sinif agirlikli CE",
                     "grad_clip": 1.0, "max_epoch": MAXEP, "sabir": SABIR, "val_orani": VAL, "tohumlar": SEEDS,
                     "sinanan_model": "val macro-F1 en iyi epoch", "sapma": "np.std (ddof=0)"},
         "egitim_havuzu_n": len(pool), "test_n": len(test_h),
         "karsilastirma": {
             "SVM | ILK_300_ve_yeni": al(s02["TF-IDF + SVM | ILK_300_ve_yeni"]),
             "lojistik | ILK_300_ve_yeni": al(s02["TF-IDF + lojistik regresyon | ILK_300_ve_yeni"]),
             "onceki_BERTurk_sonuc_03 (10% val, 5 epoch, son epoch)": {
                 "macro_f1_ort": s03["macro_f1_ort"], "macro_f1_sapma": s03["macro_f1_sapma"],
                 "dogruluk_ort": s03["dogruluk_ort"], "dogruluk_sapma": s03["dogruluk_sapma"] if "dogruluk_sapma" in s03 else None,
                 "sinif_f1_ort": s03["sinif_f1_ort"]}},
         "tohumlar": []}
yol = os.path.join(KOK, "final", "sonuc_04.json")
T0 = time.time()
for seed in SEEDS:
    cikti["tohumlar"].append(calistir(seed))
    ts = cikti["tohumlar"]
    for m in ("test_macro_f1", "test_dogruluk", "val_macro_f1"):
        v = [x[m] for x in ts]
        cikti[m + "_ort"], cikti[m + "_sapma"] = float(np.mean(v)), float(np.std(v))
    cikti["sinif_f1_ort"] = np.mean([x["sinif_f1"] for x in ts], axis=0).tolist()
    cikti["toplam_sure_sn"] = round(time.time() - T0, 1)
    json.dump(cikti, open(yol, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("test mF1 %.3f ± %.3f doğ %.3f  toplam sn %s" % (cikti["test_macro_f1_ort"], cikti["test_macro_f1_sapma"], cikti["test_dogruluk_ort"], cikti["toplam_sure_sn"]))
