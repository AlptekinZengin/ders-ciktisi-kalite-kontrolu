"""Birim / program / ders düzeyinde rapor tabloları, şekiller ve site verisi.
Girdi: final/tum_etiketler.csv, kalite-rapor/analiz/doluluk.csv. Çıktı: final/rapor/
Kullanım: py -3 10_program_raporu.py
"""
import os, re, json, sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.stdout.reconfigure(encoding="utf-8")
D = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(D)
OUT = os.path.join(D, "rapor")
os.makedirs(OUT, exist_ok=True)

BLUE, ORANGE, AQUA, GRAY = "#2a78d6", "#eb6834", "#1baf7a", "#8a8984"
INK, INK2 = "#0b0b0b", "#52514e"
plt.rcParams.update({"font.family": "Segoe UI", "font.size": 10, "axes.edgecolor": "#c9c8c3",
                     "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
                     "axes.spines.top": False, "axes.spines.right": False})

BLOOM = ["HATIRLAMA", "ANLAMA", "UYGULAMA", "ANALIZ", "DEGERLENDIRME", "YARATMA", "BILISSEL_DEGIL"]
UST = ["ANALIZ", "DEGERLENDIRME", "YARATMA"]

raw = pd.read_csv(os.path.join(D, "tum_etiketler.csv"), encoding="utf-8-sig", dtype=str, keep_default_na=False)
n_toplam = len(raw)
ing = raw[raw.kalite == "INGILIZCE"]
d = raw[raw.kalite != "INGILIZCE"].copy()
d["duzgun"] = (d.kalite == "DUZGUN").astype(int)
d["belirsiz"] = (d.kalite == "BELIRSIZ").astype(int)
d["cikti_degil"] = (d.kalite == "CIKTI_DEGIL").astype(int)
d["sorunlu"] = d.belirsiz + d.cikti_degil
for b in BLOOM:
    d["b_" + b] = ((d.kalite == "DUZGUN") & (d.bloom == b)).astype(int)
d["ust"] = d[["b_" + b for b in UST]].sum(axis=1)
d["ing_say"] = 0
ing_say = ing.groupby("ders_id").size()


def pct(a, b):
    return round(100.0 * a / b, 2) if b else 0.0


def stats(g, ders_say, ing_n):
    n = len(g)
    s = {"ders_sayisi": int(ders_say), "cumle_sayisi": int(n),
         "duzgun_sayi": int(g.duzgun.sum()), "belirsiz_sayi": int(g.belirsiz.sum()),
         "cikti_degil_sayi": int(g.cikti_degil.sum())}
    s["duzgun_yuzde"] = pct(s["duzgun_sayi"], n)
    s["belirsiz_yuzde"] = pct(s["belirsiz_sayi"], n)
    s["cikti_degil_yuzde"] = pct(s["cikti_degil_sayi"], n)
    sor = s["belirsiz_sayi"] + s["cikti_degil_sayi"]
    s["sorunlu_sayi"] = int(sor)
    s["sorunlu_yuzde"] = pct(sor, n)
    for b in BLOOM:
        s["bloom_" + b.lower() + "_yuzde"] = pct(g["b_" + b].sum(), s["duzgun_sayi"])
    s["ust_basamak_sayi"] = int(g.ust.sum())
    s["ust_basamak_yuzde"] = pct(g.ust.sum(), s["duzgun_sayi"])
    s["ingilizce_cumle_sayisi"] = int(ing_n)
    return s


# ---------------- ders düzeyi
ders_meta = d.groupby("ders_id").agg(ders_kodu=("ders_kodu", "first"), ders_adi=("ders_adi", "first"),
                                     program=("program", "first"), birim=("birim", "first"),
                                     seviye=("seviye", "first"), yariyil=("yariyil", "first"),
                                     cumle_sayisi=("cumle", "size"), sorunlu_sayi=("sorunlu", "sum"),
                                     cikti_degil_sayi=("cikti_degil", "sum"),
                                     ust_basamak_sayi=("ust", "sum")).reset_index()
ders_meta["sorunlu_yuzde"] = (100 * ders_meta.sorunlu_sayi / ders_meta.cumle_sayisi).round(2)
tekrar = d.groupby("ders_id").cumle.agg(lambda s: len(s) - s.str.strip().str.lower().nunique())
ders_meta["tekrar_cumle_sayisi"] = ders_meta.ders_id.map(tekrar).astype(int)
ders = ders_meta[["ders_id", "ders_kodu", "ders_adi", "program", "birim", "seviye", "yariyil", "cumle_sayisi",
                  "sorunlu_sayi", "sorunlu_yuzde", "cikti_degil_sayi", "tekrar_cumle_sayisi", "ust_basamak_sayi"]]
ders.to_csv(os.path.join(OUT, "ders.csv"), index=False, encoding="utf-8-sig")

prob = d[d.sorunlu == 1].groupby("ders_id").cumle.agg(lambda s: " | ".join(s))
duz = ders[(ders.cumle_sayisi >= 3) & (ders.sorunlu_yuzde >= 50)].sort_values(
    ["sorunlu_sayi", "sorunlu_yuzde"], ascending=False).copy()
duz["sorunlu_cumleler"] = duz.ders_id.map(prob)
duz.to_csv(os.path.join(OUT, "duzeltilecek_dersler.csv"), index=False, encoding="utf-8-sig")

# ---------------- boş dersler (doluluk.csv; anahtar: link içindeki curCourse = ders_id)
dol = pd.read_csv(os.path.join(ROOT, "kalite-rapor", "analiz", "doluluk.csv"), encoding="utf-8-sig",
                  dtype=str, keep_default_na=False)
dol["ders_id"] = dol.link.str.extract(r"curCourse=(\d+)")[0]
dol["cikti_sayisi"] = pd.to_numeric(dol.cikti_sayisi, errors="coerce").fillna(0).astype(int)
bos = dol[dol.cikti_sayisi == 0].copy()
bos_cols = ["ders_id", "ders_kodu", "ders_adi", "seviye", "program", "birim", "yariyil",
            "sayfa_tamamen_bos", "ogretim_elemani", "cikti_sayisi", "konu_haftasi", "eksikler", "link"]
bos[bos_cols].to_csv(os.path.join(OUT, "bos_dersler.csv"), index=False, encoding="utf-8-sig")
eslesme_ok = dol.ders_id.notna().all() and dol.ders_id.is_unique
ids_etiket = set(raw.ders_id)
cakisan_bos = len(set(bos.ders_id) & ids_etiket)  # boş denip etiketli cümlesi olan (beklenen 0)

# ---------------- grup tabloları
d_ing_birim = ing.groupby("birim").size()
d_ing_prog = ing.groupby(["birim", "program", "seviye"]).size()
uni_ders = d.ders_id.nunique()
uni = stats(d, uni_ders, len(ing))
UORT = uni["sorunlu_yuzde"]

bos_birim = bos.groupby("birim").size()
bos_prog = bos.groupby(["birim", "program", "seviye"]).size()

rows = []
for b, g in d.groupby("birim"):
    s = stats(g, g.ders_id.nunique(), d_ing_birim.get(b, 0))
    r = {"birim": b}
    r.update(s)
    r["uni_ort_fark_puan"] = round(s["sorunlu_yuzde"] - UORT, 2)
    r["cikti_bos_ders"] = int(bos_birim.get(b, 0))
    rows.append(r)
birim = pd.DataFrame(rows).sort_values("sorunlu_yuzde", ascending=False)
birim.to_csv(os.path.join(OUT, "birim.csv"), index=False, encoding="utf-8-sig")

rows = []
for (b, p, sv), g in d.groupby(["birim", "program", "seviye"]):
    s = stats(g, g.ders_id.nunique(), d_ing_prog.get((b, p, sv), 0))
    r = {"birim": b, "program": p, "seviye": sv}
    r.update(s)
    r["uni_ort_fark_puan"] = round(s["sorunlu_yuzde"] - UORT, 2)
    r["cikti_bos_ders"] = int(bos_prog.get((b, p, sv), 0))
    rows.append(r)
prog = pd.DataFrame(rows).sort_values("sorunlu_yuzde", ascending=False)
prog.to_csv(os.path.join(OUT, "program.csv"), index=False, encoding="utf-8-sig")
# cümlesi hiç olmayan ama boş dersi olan programlar
prog_keys = set(zip(prog.birim, prog.program, prog.seviye))
bos_dışı = {k: int(v) for k, v in bos_prog.items() if k not in prog_keys}

# ---------------- universite.json
uni_json = dict(uni)
uni_json["universite"] = "Karabük Üniversitesi"
uni_json["birim_sayisi"] = int(d.birim.nunique())
uni_json["program_sayisi"] = int(len(prog))
uni_json["cikti_bos_ders"] = int(len(bos))
uni_json["toplam_satir_ingilizce_dahil"] = int(n_toplam)
uni_json["seviye"] = {}
for sv, g in d.groupby("seviye"):
    s = stats(g, g.ders_id.nunique(), (ing.seviye == sv).sum())
    s["cikti_bos_ders"] = int((bos.seviye == sv).sum())
    uni_json["seviye"][sv] = s
with open(os.path.join(OUT, "universite.json"), "w", encoding="utf-8") as f:
    json.dump(uni_json, f, ensure_ascii=False, indent=2)

# ---------------- site_veri.json
dz = duz.copy()
dz["_p"] = list(zip(dz.birim, dz.program, dz.seviye))
dz_by = {k: g.head(15) for k, g in dz.groupby("_p")}
prob_rows = d[d.sorunlu == 1][["ders_id", "cumle", "kalite"]]
prob_by = {k: [{"cumle": c, "kalite": q} for c, q in zip(g.cumle, g.kalite)] for k, g in prob_rows.groupby("ders_id")}
STAT_KEYS = [c for c in prog.columns if c not in ("birim", "program", "seviye", "cikti_bos_ders")]
birimler = []
for _, br in birim.iterrows():
    pr_list = []
    for _, pr in prog[prog.birim == br.birim].iterrows():
        key = (pr.birim, pr.program, pr.seviye)
        dl = []
        if key in dz_by:
            for _, c in dz_by[key].iterrows():
                dl.append({"ders_kodu": c.ders_kodu, "ders_adi": c.ders_adi, "cumle_sayisi": int(c.cumle_sayisi),
                           "sorunlu_sayi": int(c.sorunlu_sayi), "cumleler": prob_by.get(c.ders_id, [])})
        pr_list.append({"ad": pr.program, "seviye": pr.seviye,
                        "istatistikler": {k: (v.item() if hasattr(v, "item") else v) for k, v in pr[STAT_KEYS].items()},
                        "duzeltilecek": dl, "bos_ders_sayisi": int(pr.cikti_bos_ders)})
    birimler.append({"ad": br.birim,
                     "istatistikler": {k: (v.item() if hasattr(v, "item") else v)
                                       for k, v in br[STAT_KEYS + ["cikti_bos_ders"]].items()},
                     "programlar": pr_list})
site = {"universite": uni_json, "birimler": birimler}
site_path = os.path.join(OUT, "site_veri.json")
with open(site_path, "w", encoding="utf-8") as f:
    json.dump(site, f, ensure_ascii=False)
site_mb = os.path.getsize(site_path) / 1e6

# ---------------- ozet.json
big = prog[prog.cumle_sayisi >= 100]
cols = ["birim", "program", "seviye", "cumle_sayisi", "sorunlu_yuzde", "ust_basamak_yuzde"]
ozet = {
    "sorunlu_en_yuksek_10": big.sort_values("sorunlu_yuzde", ascending=False).head(10)[cols].to_dict("records"),
    "sorunlu_en_dusuk_10": big.sort_values("sorunlu_yuzde").head(10)[cols].to_dict("records"),
    "ust_basamak_en_yuksek_5": big.sort_values("ust_basamak_yuzde", ascending=False).head(5)[cols].to_dict("records"),
    "ust_basamak_en_dusuk_5": big.sort_values("ust_basamak_yuzde").head(5)[cols].to_dict("records"),
    "birim_siralamasi": birim[["birim", "cumle_sayisi", "sorunlu_yuzde", "ust_basamak_yuzde", "uni_ort_fark_puan"]].to_dict("records"),
    "duzeltilecek_ders_sayisi": int(len(duz)),
    "bos_ders_sayisi": int(len(bos)),
    "en_az_100_cumleli_program_sayisi": int(len(big)),
}
with open(os.path.join(OUT, "ozet.json"), "w", encoding="utf-8") as f:
    json.dump(ozet, f, ensure_ascii=False, indent=2)

# ---------------- şekiller
def kisalt(s, n=44):
    _l = lambda x: x.replace("I", "ı").replace("İ", "i").lower()
    s = " ".join(_l(w) if _l(w) == "ve" else w[:1] + _l(w[1:]) for w in s.split())
    return s if len(s) <= n else s[:n - 1] + "…"


b2 = birim.sort_values("sorunlu_yuzde")
fig, ax = plt.subplots(figsize=(8.5, 8))
ax.barh([kisalt(x) for x in b2.birim], b2.sorunlu_yuzde, color=BLUE, height=0.65)
for i, v in enumerate(b2.sorunlu_yuzde):
    ax.text(v + 0.4, i, f"%{v:.1f}", va="center", fontsize=8.5, color=INK2)
ax.axvline(UORT, color=ORANGE, ls="--", lw=1.4)
ax.text(UORT + 0.3, -0.9, f"Üniversite ortalaması %{UORT:.1f}", color=ORANGE, fontsize=9, va="top")
ax.set_xlabel("Sorunlu cümle yüzdesi (belirsiz + çıktı değil)")
ax.xaxis.grid(True, color="#ecebe7"); ax.set_axisbelow(True)
ax.set_title("Birimlere göre sorunlu çıktı cümlesi oranı", loc="left", color=INK)
fig.tight_layout(); fig.savefig(os.path.join(OUT, "sekil_birim_sorunlu.png"), dpi=150); plt.close(fig)

etk = ["Hatırlama", "Anlama", "Uygulama", "Analiz", "Değerlendirme", "Yaratma", "Bilişsel değil"]
vals = [uni["bloom_" + b.lower() + "_yuzde"] for b in BLOOM]
cl = [BLUE] * 3 + [AQUA] * 3 + [GRAY]
fig, ax = plt.subplots(figsize=(8, 4.5))
bars = ax.bar(etk, vals, color=cl, width=0.62)
for r_, v in zip(bars, vals):
    ax.text(r_.get_x() + r_.get_width() / 2, v + 0.5, f"%{v:.1f}", ha="center", fontsize=9, color=INK)
ax.set_ylabel("Düzgün cümleler içinde yüzde")
ax.yaxis.grid(True, color="#ecebe7"); ax.set_axisbelow(True)
plt.xticks(fontsize=8.5)
ax.set_title("Bloom düzeyi dağılımı (düzgün cümleler)", loc="left", color=INK)
fig.tight_layout(); fig.savefig(os.path.join(OUT, "sekil_bloom_genel.png"), dpi=150); plt.close(fig)

fig, axes = plt.subplots(1, 2, figsize=(10, 4.2))
svs = ["Lisans", "Ön Lisans"]
w = 0.26
for k, (lab, c) in enumerate([("duzgun_yuzde", AQUA), ("belirsiz_yuzde", ORANGE), ("cikti_degil_yuzde", GRAY)]):
    pass
ax = axes[0]
for k, (lab, key, c) in enumerate([("Düzgün", "duzgun_yuzde", AQUA), ("Belirsiz", "belirsiz_yuzde", ORANGE),
                                    ("Çıktı değil", "cikti_degil_yuzde", GRAY)]):
    v = [uni_json["seviye"][s][key] for s in svs]
    xs = np.arange(2) + (k - 1) * w
    ax.bar(xs, v, w, color=c, label=lab)
    for x_, v_ in zip(xs, v):
        ax.text(x_, v_ + 0.8, f"%{v_:.1f}", ha="center", fontsize=8.5, color=INK)
ax.set_xticks(range(2)); ax.set_xticklabels(svs); ax.set_ylabel("Cümle yüzdesi")
ax.set_title("Kalite", loc="left", color=INK); ax.legend(frameon=False, fontsize=8.5)
ax.yaxis.grid(True, color="#ecebe7"); ax.set_axisbelow(True)
ax = axes[1]
v = [uni_json["seviye"][s]["ust_basamak_yuzde"] for s in svs]
ax.bar(svs, v, 0.5, color=BLUE)
for i, v_ in enumerate(v):
    ax.text(i, v_ + 0.15, f"%{v_:.1f}", ha="center", fontsize=9, color=INK)
ax.set_ylabel("Düzgün cümleler içinde yüzde")
ax.set_title("Üst basamak (analiz + değerlendirme + yaratma)", loc="left", color=INK, fontsize=10)
ax.yaxis.grid(True, color="#ecebe7"); ax.set_axisbelow(True)
fig.tight_layout(); fig.savefig(os.path.join(OUT, "sekil_seviye.png"), dpi=150); plt.close(fig)

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.hist(big.sorunlu_yuzde, bins=np.arange(0, 105, 5), color=BLUE, edgecolor="white")
ax.axvline(UORT, color=ORANGE, ls="--", lw=1.4)
ax.text(UORT + 1, ax.get_ylim()[1] * 0.95, f"Üniversite %{UORT:.1f}", color=ORANGE, fontsize=9, va="top")
ax.set_xlabel("Sorunlu cümle yüzdesi"); ax.set_ylabel("Program sayısı")
ax.yaxis.grid(True, color="#ecebe7"); ax.set_axisbelow(True)
ax.set_title(f"Programların sorunlu yüzde dağılımı (en az 100 cümle, n={len(big)})", loc="left", color=INK)
fig.tight_layout(); fig.savefig(os.path.join(OUT, "sekil_program_dagilim.png"), dpi=150); plt.close(fig)

# ---------------- kontroller
exp = n_toplam - len(ing)
pcols = [c for c in birim.columns if c.endswith("_yuzde")]
yuzde_ok = bool(((birim[pcols] >= 0) & (birim[pcols] <= 100)).all().all() and
                ((prog[pcols] >= 0) & (prog[pcols] <= 100)).all().all() and
                ((ders.sorunlu_yuzde >= 0) & (ders.sorunlu_yuzde <= 100)).all())
with open(site_path, encoding="utf-8") as f:
    s2 = json.load(f)
site_prog = sum(len(b["programlar"]) for b in s2["birimler"])
print("INGILIZCE satir:", len(ing), "beklenen toplam:", exp)
print("birim toplam:", int(birim.cumle_sayisi.sum()), "program toplam:", int(prog.cumle_sayisi.sum()), "ders toplam:", int(ders.cumle_sayisi.sum()))
print("toplamlar esit:", int(birim.cumle_sayisi.sum()) == int(prog.cumle_sayisi.sum()) == exp == uni["cumle_sayisi"])
print("yuzdeler 0-100:", yuzde_ok)
print("site_veri program:", site_prog, "program.csv:", len(prog), "esit:", site_prog == len(prog), "MB: %.2f" % site_mb)
print("bos ders:", len(bos), "anahtar benzersiz/tam:", eslesme_ok, "bos ama etiketli:", cakisan_bos,
      "cumlesiz programdaki bos:", sum(bos_dışı.values()), "birim bos toplam:", int(birim.cikti_bos_ders.sum()),
      "program bos toplam:", int(prog.cikti_bos_ders.sum()))
print("duzeltilecek:", len(duz), "ders sayisi:", len(ders), "birim:", len(birim), "program:", len(prog))
