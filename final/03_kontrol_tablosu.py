import re
import sys
from pathlib import Path

import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

BASE = Path(__file__).resolve().parent / "etiket2"

ornek = pd.read_csv(BASE / "ornek_500.csv", encoding="utf-8-sig", dtype=str, keep_default_na=False)
parts = []
for i in (1, 2, 3):
    t = pd.read_csv(BASE / f"tahmin_{i}.csv", encoding="utf-8-sig", dtype=str, keep_default_na=False)
    t["model_etiketleyen"] = f"Sonnet {i}"
    parts.append(t)
tah = pd.concat(parts, ignore_index=True)
tah = tah.rename(columns={"kalite": "model_kalite", "bloom": "model_bloom",
                          "guven": "model_guven", "gerekce": "model_gerekce"})

if tah["no"].duplicated().any():
    print("DUPLIKE no:", tah.loc[tah["no"].duplicated(), "no"].tolist())
    sys.exit(1)
eksik = sorted(set(ornek["no"]) - set(tah["no"]), key=int)
fazla = sorted(set(tah["no"]) - set(ornek["no"]), key=int)
if eksik or fazla or len(ornek) != 500:
    print("ESLESMEYEN: tahminsiz no", eksik, "ornekte olmayan no", fazla)
    sys.exit(1)

df = ornek.merge(tah, on="no", how="left")
df["_n"] = df["no"].astype(int)
df = df.sort_values("_n").reset_index(drop=True)

EN_WORDS = set("""the and of to in a an with is are can will be for students student course
by on as that this their it or from at using use able understand explain apply analyze design
develop knowledge basic skills learn learning at upon successful completion have has which
into about how interpret illustrate analyze postcolonial literary works weaken colonial discourse vocabulary conversation electrical circuits excitation production lines perspectives many what these those other such also not may should students' main concepts
methods principles systems system data software analysis introduction understanding
techniques fundamentals theory ability work working problems problem solving""".split())
TR_CHARS = set("çğıöşüÇĞİÖŞÜ")
MANUEL_BOZUK = {"81", "148"}  # kullanicinin belirttigi yarim/bozuk cumleler
ISIM_RE = re.compile(r"(ması|mesi|ılması|ilmesi|ulması|ülmesi|nması|nmesi)$")


def words(s):
    return re.findall(r"[^\W\d_]+", s)


def isaretler(r):
    out = []
    if r["model_guven"].strip().lower() == "dusuk":
        out.append("DUSUK_GUVEN")
    c = r["cumle"].strip()
    w = [x.lower().replace("ı", "i") if x[:1] == "ı" and x[1:].isascii() else x.lower() for x in words(c)]
    if w:
        ratio = sum(x in EN_WORDS for x in w) / len(w)
        if ratio >= 0.5 or (ratio >= 0.3 and not any(ch in TR_CHARS for ch in c)):
            out.append("INGILIZCE")
    if w and ISIM_RE.search(w[-1]):
        out.append("ISIM_OBEGI")
    if len(w) < 2 or c.endswith(",") or "¸" in c or r["no"] in MANUEL_BOZUK or (len(w) >= 20 and not re.search(r"[.!?]$", c)):
        out.append("BOZUK")
    return ";".join(out)


df["isaret"] = df.apply(isaretler, axis=1)

cols = ["no", "cumle", "ders_kodu", "ders_adi", "program", "birim", "seviye", "yariyil", "ders_id",
        "secim_grubu", "model_kalite", "model_bloom", "model_guven", "model_gerekce",
        "model_etiketleyen", "isaret"]
out = df[cols]
out.to_csv(BASE / "tahmin_500.csv", index=False, encoding="utf-8-sig")

# Excel
xl = out.copy()
xl["_n"] = xl["no"].astype(int)
xl["_has"] = (xl["isaret"] != "").map({True: 0, False: 1})
xl = xl.sort_values(["_has", "_n"]).reset_index(drop=True)
xcols = ["no", "cumle", "ders_adi", "program", "model_kalite", "model_bloom", "model_guven",
         "model_gerekce", "isaret"]
wb = Workbook()
ws = wb.active
ws.title = "Kontrol"
heads = xcols + ["alptekin_kalite", "alptekin_bloom", "not"]
ws.append(heads)
hfill = PatternFill("solid", fgColor="DCE6F7")
for c in ws[1]:
    c.font = Font(bold=True)
    c.fill = hfill
    c.alignment = Alignment(vertical="center", wrap_text=True)
yellow = PatternFill("solid", fgColor="FFF9C4")
wrap = Alignment(vertical="top", wrap_text=True)
for _, r in xl.iterrows():
    row = [int(r["no"])] + [r[c] for c in xcols[1:]] + ["", "", ""]
    ws.append(row)
    rr = ws.max_row
    for c in ws[rr]:
        c.alignment = wrap
        if r["isaret"]:
            c.fill = yellow
widths = {"A": 6, "B": 70, "C": 28, "D": 28, "E": 14, "F": 16, "G": 11, "H": 36, "I": 22,
          "J": 18, "K": 18, "L": 30}
for k, v in widths.items():
    ws.column_dimensions[k].width = v
ws.freeze_panes = "C2"
n = len(xl) + 1
dv1 = DataValidation(type="list", formula1='"DUZGUN,BELIRSIZ,CIKTI_DEGIL"', allow_blank=True)
dv2 = DataValidation(type="list",
                     formula1='"HATIRLAMA,ANLAMA,UYGULAMA,ANALIZ,DEGERLENDIRME,YARATMA,BILISSEL_DEGIL"',
                     allow_blank=True)
ws.add_data_validation(dv1)
ws.add_data_validation(dv2)
dv1.add(f"J2:J{n}")
dv2.add(f"K2:K{n}")

# Ozet
oz = wb.create_sheet("Ozet")


def block(title, series_or_df, start):
    oz.cell(start, 1, title).font = Font(bold=True)
    r = start + 1
    if isinstance(series_or_df, pd.Series):
        oz.cell(r, 1, "deger").font = Font(bold=True)
        oz.cell(r, 2, "sayi").font = Font(bold=True)
        for k, v in series_or_df.items():
            r += 1
            oz.cell(r, 1, str(k))
            oz.cell(r, 2, int(v))
    else:
        oz.cell(r, 1, series_or_df.index.name or "").font = Font(bold=True)
        for j, cn in enumerate(series_or_df.columns, start=2):
            oz.cell(r, j, str(cn)).font = Font(bold=True)
        for k, row in series_or_df.iterrows():
            r += 1
            oz.cell(r, 1, str(k))
            for j, v in enumerate(row, start=2):
                oz.cell(r, j, int(v))
    return r + 2


p = 1
p = block("model_kalite", out["model_kalite"].value_counts(), p)
p = block("model_bloom", out["model_bloom"].replace("", "(bos)").value_counts(), p)
tur = pd.Series([t for s in out["isaret"] if s for t in s.split(";")]).value_counts()
tur = pd.concat([tur, pd.Series({"(en az bir isaret)": int((out["isaret"] != "").sum())})])
p = block("isaret turleri", tur, p)
ct = pd.crosstab(out["secim_grubu"], out["model_kalite"], margins=True, margins_name="Toplam")
p = block("secim_grubu x model_kalite", ct, p)
oz.column_dimensions["A"].width = 28
for col in "BCDEF":
    oz.column_dimensions[col].width = 14

wb.save(BASE / "Kontrol-Tablosu-2.xlsx")

print(out["model_kalite"].value_counts().to_string())
print(out["model_bloom"].replace("", "(bos)").value_counts().to_string())
print(tur.to_string())
print(ct.to_string())
for t in ["INGILIZCE", "BOZUK"]:
    print("==", t)
    for _, r in out[out["isaret"].str.contains(t)].iterrows():
        print(r["no"], "|", r["cumle"], "|", r["isaret"])
