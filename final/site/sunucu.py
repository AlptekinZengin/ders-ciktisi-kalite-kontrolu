# Ders çıktısı kalite kontrolü: yerel sunucu (yalnız 127.0.0.1:8765).
import os
import re
import sys
import threading
import time

import torch
from flask import Flask, Response, jsonify, request, send_from_directory
from transformers import AutoModelForSequenceClassification, AutoTokenizer

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import oneri  # noqa: E402

KLASOR = os.path.dirname(os.path.abspath(__file__))
STATIK = os.path.join(KLASOR, "static")
VERI = os.path.join(os.path.dirname(KLASOR), "rapor", "site_veri.json")
MODEL_KOK = r"C:\Users\Alptekin Zengin\.venvs\yz-final-model"
MAXLEN, TBATCH = 64, 64
EN_CUMLE, EN_UZUNLUK = 200, 1000

os.makedirs(STATIK, exist_ok=True)

# ---- İngilizce ayırıcı (09_tumunu_etiketle.py ile aynı) ----
TR = set("çğıöşüÇĞİÖŞÜ")
EN = re.compile(r"\b(the|and|of|to|will|be able|students?|understand|describe|explain|apply)\b", re.I)


def ing(s):
    return not (set(s) & TR) and bool(EN.search(s))


# ---- modeller ----
t0 = time.time()
CIHAZ = "cuda" if torch.cuda.is_available() else "cpu"
DEV = torch.device(CIHAZ)


def yukle(ad):
    yol = os.path.join(MODEL_KOK, ad)
    tok = AutoTokenizer.from_pretrained(yol)
    m = AutoModelForSequenceClassification.from_pretrained(yol).to(DEV).eval()
    return tok, m


TOK_K, MOD_K = yukle("kalite")
TOK_B, MOD_B = yukle("bloom")
YUKLEME_SN = time.time() - t0
KILIT = threading.Lock()

with open(VERI, "rb") as f:
    VERI_BAYT = f.read()

print("Modeller yuklendi: %.1f sn, cihaz: %s" % (YUKLEME_SN, CIHAZ), flush=True)


@torch.no_grad()
def tahmin(tok, model, metinler):
    """metinler -> [(etiket, olasilik)]"""
    sonuc = [None] * len(metinler)
    sira = sorted(range(len(metinler)), key=lambda i: len(metinler[i]))
    for i in range(0, len(sira), TBATCH):
        idx = sira[i:i + TBATCH]
        enc = tok([metinler[j] for j in idx], truncation=True, max_length=MAXLEN,
                  padding=True, return_tensors="pt").to(DEV)
        p = torch.softmax(model(**enc).logits.float(), -1).cpu()
        for r, j in enumerate(idx):
            k = int(p[r].argmax())
            sonuc[j] = (model.config.id2label[k], float(p[r, k]))
    return sonuc


def degerlendir(cumleler):
    benzersiz = list(dict.fromkeys(cumleler))
    kal, blo = {}, {}
    en = [c for c in benzersiz if ing(c)]
    tr = [c for c in benzersiz if not ing(c)]
    for c in en:
        kal[c] = ("INGILIZCE", None)
    if tr:
        with KILIT:
            for c, r in zip(tr, tahmin(TOK_K, MOD_K, tr)):
                kal[c] = r
            duz = [c for c in tr if kal[c][0] == "DUZGUN"]
            if duz:
                for c, r in zip(duz, tahmin(TOK_B, MOD_B, duz)):
                    blo[c] = r
    sonuclar = []
    ozet = {"toplam": len(cumleler), "duzgun": 0, "belirsiz": 0, "cikti_degil": 0, "ingilizce": 0}
    for c in cumleler:
        k, g = kal[c]
        b = blo.get(c)
        vurgular, nt = oneri.uret(c, k, g)
        ozet[{"DUZGUN": "duzgun", "BELIRSIZ": "belirsiz", "CIKTI_DEGIL": "cikti_degil", "INGILIZCE": "ingilizce"}[k]] += 1
        sonuclar.append({
            "cumle": c,
            "kalite": k,
            "guven": None if g is None else round(g, 3),
            "bloom": b[0] if b else None,
            "bloom_guven": round(b[1], 3) if b else None,
            "vurgular": vurgular,
            "not": nt,
        })
    return {"ozet": ozet, "sonuclar": sonuclar}


app = Flask(__name__, static_folder=None)
app.json.ensure_ascii = False
app.json.sort_keys = False


@app.get("/")
def anasayfa():
    yol = os.path.join(STATIK, "index.html")
    if not os.path.isfile(yol):
        return Response("Ön taraf henüz yok", mimetype="text/plain; charset=utf-8")
    return send_from_directory(STATIK, "index.html", max_age=0)


@app.get("/static/<path:yol>")
def statik(yol):
    return send_from_directory(STATIK, yol, max_age=0)


@app.get("/api/durum")
def durum():
    return jsonify({"hazir": True, "cihaz": CIHAZ})


@app.get("/api/veri")
def veri():
    return Response(VERI_BAYT, mimetype="application/json; charset=utf-8")


@app.post("/api/kontrol")
def kontrol():
    govde = request.get_json(silent=True)
    ham = govde.get("cumleler") if isinstance(govde, dict) else None
    cumleler = []
    if isinstance(ham, list):
        for x in ham:
            if isinstance(x, str):
                x = x.strip()
                if x:
                    cumleler.append(x[:EN_UZUNLUK])
    if not cumleler:
        return jsonify({"hata": "Cümle bulunamadı."}), 400
    if len(cumleler) > EN_CUMLE:
        return jsonify({"hata": "En çok 200 cümle gönderilebilir."}), 400
    return jsonify(degerlendir(cumleler))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8765, debug=False, threaded=True)
