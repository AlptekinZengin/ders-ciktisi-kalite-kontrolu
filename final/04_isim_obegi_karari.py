# Alptekin kararı (2026-11-10): "-ilmesi/-ması" ile biten isim öbekleri (isaret = ISIM_OBEGI) CIKTI_DEGIL sayılır.
# 03_kontrol_tablosu.py'den SONRA çalıştırılır; tahmin_500.csv ve Kontrol-Tablosu-2.xlsx içindeki model tahminini günceller.
import csv, os, collections
import openpyxl

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "etiket2")
NOT = "Karar: -ilmesi/-ması isim öbeği = çıktı değil"

yol = os.path.join(D, "tahmin_500.csv")
R = list(csv.DictReader(open(yol, encoding="utf-8-sig")))
once = collections.Counter()
for r in R:
    if "ISIM_OBEGI" in r["isaret"] and r["model_kalite"] != "CIKTI_DEGIL":
        once[r["model_kalite"]] += 1
        r["model_gerekce"] = f"{NOT} (ilk tahmin: {r['model_kalite']} {r['model_bloom']})".replace(" )", ")")
        r["model_kalite"], r["model_bloom"] = "CIKTI_DEGIL", ""
with open(yol, "w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(R[0].keys()))
    w.writeheader(); w.writerows(R)

x = os.path.join(D, "Kontrol-Tablosu-2.xlsx")
wb = openpyxl.load_workbook(x)
s = wb["Kontrol"]
b = {c.value: i for i, c in enumerate(s[1])}
harita = {r["no"]: r for r in R}
n = 0
for row in s.iter_rows(min_row=2):
    r = harita[str(row[b["no"]].value)]
    if row[b["model_kalite"]].value != r["model_kalite"]:
        row[b["model_kalite"]].value = r["model_kalite"]
        row[b["model_bloom"]].value = None
        row[b["model_gerekce"]].value = r["model_gerekce"]
        n += 1
wb.save(x)
print("değişen (ilk tahmine göre):", dict(once), "| xlsx'te güncellenen satır:", n)
print("yeni dağılım:", dict(collections.Counter(r["model_kalite"] for r in R)))
