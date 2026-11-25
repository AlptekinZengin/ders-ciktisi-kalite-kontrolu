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
