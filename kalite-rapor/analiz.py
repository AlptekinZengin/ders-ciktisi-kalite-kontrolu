"""Ön analiz: tam veri (o anki kopya) + 300 etiketli örnek. Grafikleri ve sayıları üretir.
Kullanım: py -3 analiz.py <proje_kok>  (projects/yz-dersi)
"""
import csv, json, math, os, re, sys, collections
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.stdout.reconfigure(encoding="utf-8")
KOK = sys.argv[1]
OUT = os.path.join(KOK, "kalite-rapor", "analiz")
os.makedirs(OUT, exist_ok=True)

BLUE, ORANGE, AQUA, GRAY = "#2a78d6", "#eb6834", "#1baf7a", "#8a8984"
INK, INK2 = "#0b0b0b", "#52514e"
plt.rcParams.update({"font.family": "Segoe UI", "font.size": 10, "axes.edgecolor": "#c9c8c3",
                     "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
                     "axes.spines.top": False, "axes.spines.right": False, "figure.dpi": 200})

rows = list(csv.DictReader(open(os.path.join(KOK, "veri", "karabuk_ders_ciktilari.csv"), encoding="utf-8-sig")))
S = {}
S["toplanan_ders"] = len({r["ders_id"] for r in rows})
dolu = [r for r in rows if r["cumle"].strip()]
S["bos_ders"] = S["toplanan_ders"] - len({r["ders_id"] for r in dolu})
S["cumle"] = len(dolu)
S["ders_ciktili"] = len({r["ders_id"] for r in dolu})
S["program_birimi"] = len({(r["birim"], r["program"], r["seviye"]) for r in dolu})
S["program_adi"] = len({r["program"] for r in dolu})
S["birim"] = len({r["birim"] for r in dolu})
S["seviye_cumle"] = dict(collections.Counter(r["seviye"] for r in dolu))

tr = set("çğıöşüÇĞİÖŞÜ")
EN = re.compile(r"\b(the|and|of|to|will|be able|students?|understand|describe|explain|apply)\b", re.I)
ing = lambda s: not (set(s) & tr) and bool(EN.search(s))
S["ingilizce"] = sum(ing(r["cumle"]) for r in dolu)
T = [r for r in dolu if not ing(r["cumle"])]

# ders başına çıktı
per = collections.Counter(r["ders_id"] for r in dolu)
v = sorted(per.values())
S["ders_basina_cikti_ort"] = round(sum(v) / len(v), 2)
S["ders_basina_cikti_medyan"] = v[len(v) // 2]
S["ders_basina_cikti_min_max"] = [v[0], v[-1]]
# uzunluk
L = sorted(len(r["cumle"].split()) for r in T)
S["kelime_ort"] = round(sum(L) / len(L), 1)
S["kelime_medyan"] = L[len(L) // 2]
S["kelime_3_ve_alti"] = sum(1 for x in L if x <= 3)

# tekrarlar
norm = lambda s: re.sub(r"[\s\.\,;:]+$", "", re.sub(r"\s+", " ", s.strip().lower()))
cnt = collections.Counter(norm(r["cumle"]) for r in T)
S["benzersiz_cumle"] = len(cnt)
S["tekrarli_cumle_satiri"] = sum(c for c in cnt.values() if c > 1)
ders_ici = collections.Counter((r["ders_id"], norm(r["cumle"])) for r in T)
S["ders_ici_tekrar_satiri"] = sum(c - 1 for c in ders_ici.values() if c > 1)
S["ders_ici_tekrarli_ders"] = len({d for (d, _), c in ders_ici.items() if c > 1})
# farklı derslerde aynı cümle
dset = collections.defaultdict(set)
for r in T:
    dset[norm(r["cumle"])].add(r["ders_id"])
S["en_sik_tekrar"] = [(k, len(d)) for k, d in sorted(dset.items(), key=lambda kv: -len(kv[1]))[:5]]

# son kelime (fiil yaklaşığı)
def son(s):
    w = re.findall(r"[a-zçğıöşüâîû]+", s.lower())
    return w[-1] if w else ""
sonk = collections.Counter(son(r["cumle"]) for r in T)
S["en_sik_son_kelime"] = sonk.most_common(20)

# kural tabanlı belirsizlik işareti (taban çizgisi taslağı)
# Kural tabanlı taban çizgisi: kelimeleri ayırır, fiil gibi biten kelimelere bakar.
FIIL_EK = re.compile(r"(ir|ır|ur|ür|ar|er|r|ebilir|abilir|ebilmek|abilmek|ebilme|abilme|mek|mak|me|ma|ecektir|acaktır|ecek|acak|ilir|ılır|ulur|ülür|irler|ırlar|urlar|ürler|erler|arlar)$")
BEL_KOK = ("öğren", "kavra", "anla", "bil", "edin", "kazan", "geliş", "sahip", "takip", "farkında", "algıla")
BEL_IFADE = re.compile(r"bilgi sahibi|hakkında bilgi|bilgisi olur|farkındalık|önemini|bilgilen", re.I)
OLC_KOK = ("hesapla", "uygula", "analiz", "tasarla", "geliştirir", "geliştirebil", "çöz", "açıkla", "tanımla", "karşılaştır", "değerlendir",
           "kullan", "oluştur", "yaz", "hazırla", "seç", "ölç", "çiz", "kur", "yorumla", "sınıflandır", "listele", "planla", "üret", "yap", "belirle", "ifade")
def _low(s):
    return s.replace("I", "ı").replace("İ", "i").lower()
def kural(s):
    w = re.findall(r"[a-zçğıöşüâîû]+", _low(s))
    fiiller = [x for x in w if FIIL_EK.search(x) and len(x) > 3]
    if not fiiller:
        return "CIKTI_DEGIL"
    olc = any(x.startswith(OLC_KOK) for x in fiiller)
    bel = BEL_IFADE.search(_low(s)) or any(x.startswith(BEL_KOK) for x in fiiller)
    if bel and not olc:
        return "BELIRSIZ"
    return "DUZGUN"

# 300 örnek
E = list(csv.DictReader(open(os.path.join(KOK, "kalite-rapor", "etiket", "etiket_kesin.csv"), encoding="utf-8-sig")))
kq = collections.Counter(r["alptekin_kalite"] for r in E)
n = len(E)
def ci(k):
    p = k / n
    h = 1.96 * math.sqrt(p * (1 - p) / n)
    return [round(100 * p, 1), round(100 * max(0, p - h), 1), round(100 * min(1, p + h), 1)]
S["ornek_kalite"] = {k: [c] + ci(c) for k, c in kq.items()}
kb = collections.Counter(r["alptekin_bloom"] for r in E if r["alptekin_bloom"])
S["ornek_bloom"] = dict(kb)
sev = collections.defaultdict(collections.Counter)
for r in E:
    sev[r["seviye"]][r["alptekin_kalite"]] += 1
S["ornek_seviye_kalite"] = {k: dict(v) for k, v in sev.items()}
# kural tabanlı ile karşılaştırma
pairs = [(r["alptekin_kalite"], kural(r["cumle"])) for r in E]
S["kural_dogruluk"] = round(100 * sum(a == b for a, b in pairs) / n, 1)
labs = ["DUZGUN", "BELIRSIZ", "CIKTI_DEGIL"]
f1s = {}
for c in labs:
    tp = sum(a == c and b == c for a, b in pairs); fp = sum(a != c and b == c for a, b in pairs); fn = sum(a == c and b != c for a, b in pairs)
    pr = tp / (tp + fp) if tp + fp else 0; rc = tp / (tp + fn) if tp + fn else 0
    f1s[c] = round(2 * pr * rc / (pr + rc), 3) if pr + rc else 0
S["kural_f1"] = f1s
S["kural_macro_f1"] = round(sum(f1s.values()) / 3, 3)
S["kural_karisiklik"] = {a: dict(collections.Counter(b for x, b in pairs if x == a)) for a in labs}

# birim düzeyinde kural tabanlı belirsiz oranı (tam veri, kaba gösterge)
bu = collections.defaultdict(lambda: [0, 0])
for r in T:
    bu[r["birim"]][1] += 1
    bu[r["birim"]][0] += kural(r["cumle"]) == "BELIRSIZ"
bu = {k: v for k, v in bu.items() if v[1] >= 150}
S["birim_belirsiz_kural"] = sorted(((k, round(100 * a / b, 1), b) for k, (a, b) in bu.items()), key=lambda x: -x[1])

json.dump(S, open(os.path.join(OUT, "sayilar.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

def title_case_tr(s):
    low = lambda x: x.replace("I", "ı").replace("İ", "i").lower()
    out = []
    for w in s.split():
        lw = low(w)
        out.append(lw if lw in ("ve",) else w[:1] + low(w[1:]))
    return " ".join(out)

# Şekil 1: Bloom dağılımı (örnek)
order = ["HATIRLAMA", "ANLAMA", "UYGULAMA", "ANALIZ", "DEGERLENDIRME", "YARATMA", "BILISSEL_DEGIL"]
lab = ["Hatırlama", "Anlama", "Uygulama", "Analiz", "Değerlendirme", "Yaratma", "Bilişsel değil"]
vals = [kb.get(o, 0) for o in order]
fig, ax = plt.subplots(figsize=(6.4, 3.0))
cols = [BLUE] * 6 + [GRAY]
b = ax.bar(lab, vals, color=cols, width=0.6)
for r_, v_ in zip(b, vals):
    ax.text(r_.get_x() + r_.get_width() / 2, v_ + 1, str(v_), ha="center", va="bottom", fontsize=9, color=INK)
ax.set_ylabel("Cümle sayısı"); ax.set_ylim(0, max(vals) * 1.18)
ax.yaxis.grid(True, color="#ecebe7"); ax.set_axisbelow(True)
plt.xticks(rotation=0, fontsize=8.5)
plt.tight_layout(); plt.savefig(os.path.join(OUT, "sekil_bloom.png")); plt.close()

# Şekil 2: kalite seviye bazında (100% yığılmış yatay)
fig, ax = plt.subplots(figsize=(6.4, 1.9))
kl = [("DUZGUN", "Düzgün", BLUE), ("BELIRSIZ", "Belirsiz", ORANGE), ("CIKTI_DEGIL", "Çıktı değil", AQUA)]
ys = ["Ön Lisans", "Lisans"]
for i, s_ in enumerate(ys):
    tot = sum(sev[s_].values()); left = 0
    for k, l, c in kl:
        w = 100 * sev[s_].get(k, 0) / tot
        ax.barh(i, w, left=left, color=c, height=0.55, edgecolor="white", linewidth=2, label=l if i == 0 else None)
        if w >= 6:
            ax.text(left + w / 2, i, f"%{w:.0f}", ha="center", va="center", color="white", fontsize=9, fontweight="bold")
        left += w
ax.set_yticks(range(len(ys))); ax.set_yticklabels([f"{s_} (n={sum(sev[s_].values())})" for s_ in ys])
ax.set_xlim(0, 100); ax.set_xlabel("Cümle yüzdesi")
ax.legend(ncol=3, frameon=False, loc="lower center", bbox_to_anchor=(0.5, 1.0), fontsize=9)
plt.tight_layout(); plt.savefig(os.path.join(OUT, "sekil_kalite_seviye.png")); plt.close()

# Şekil 3: en sık son kelimeler
top = sonk.most_common(15)[::-1]
fig, ax = plt.subplots(figsize=(6.4, 3.8))
belk = re.compile(r"^(bilir|öğrenir|kavrar|anlar|olur|edinir|kazanır)$")
ax.barh([t[0] for t in top], [t[1] for t in top], color=[ORANGE if belk.match(t[0]) else BLUE for t in top], height=0.62)
for i, (w, c) in enumerate(top):
    ax.text(c + 8, i, str(c), va="center", fontsize=8.5, color=INK)
ax.set_xlabel("Cümle sayısı (cümlenin son kelimesi)")
ax.xaxis.grid(True, color="#ecebe7"); ax.set_axisbelow(True)
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=BLUE, label="Ölçülebilir ya da nötr"), Patch(color=ORANGE, label="Belirsizlik işareti olan")], frameon=False, fontsize=8.5, loc="lower right")
plt.tight_layout(); plt.savefig(os.path.join(OUT, "sekil_son_kelime.png")); plt.close()

# Şekil 4: birim bazında kural tabanlı belirsiz oranı
bl = S["birim_belirsiz_kural"]
bl = bl[:8] + bl[-7:] if len(bl) > 15 else bl
fig, ax = plt.subplots(figsize=(6.4, 0.3 * len(bl) + 0.9))
names = [("Rektörlük (ortak seçmeli havuz)" if x[0].strip() == "REKTÖRLÜK" else title_case_tr(x[0]).replace("Meslek Yüksekokulu", "MYO").replace("Türkiye Odalar ve Borsalar Birliği", "TOBB")) for x in bl][::-1]
ax.barh(names, [x[1] for x in bl][::-1], color=BLUE, height=0.62)
for i, x in enumerate(bl[::-1]):
    ax.text(x[1] + 0.4, i, f"%{x[1]:.0f}", va="center", fontsize=8.5, color=INK2)
ax.set_xlabel("Kural tabanlı ölçüte göre belirsiz cümle oranı (%)")
ax.tick_params(axis="y", labelsize=8.5)
ax.xaxis.grid(True, color="#ecebe7"); ax.set_axisbelow(True)
plt.tight_layout(); plt.savefig(os.path.join(OUT, "sekil_birim.png")); plt.close()

# Şekil 5: ders başına çıktı sayısı
fig, ax = plt.subplots(figsize=(6.4, 2.4))
cc = collections.Counter(v)
xs = list(range(1, min(15, max(v)) + 1))
ax.bar(xs, [cc.get(x, 0) for x in xs], color=BLUE, width=0.7)
ax.set_xlabel("Bir dersteki öğrenme çıktısı sayısı"); ax.set_ylabel("Ders sayısı")
ax.set_xticks(xs); ax.yaxis.grid(True, color="#ecebe7"); ax.set_axisbelow(True)
plt.tight_layout(); plt.savefig(os.path.join(OUT, "sekil_ders_basina.png")); plt.close()

print(json.dumps(S, ensure_ascii=False, indent=1))
