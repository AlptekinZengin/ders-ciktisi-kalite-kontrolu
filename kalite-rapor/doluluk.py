"""Bilgi paketi doluluk kontrolü: indirilmiş ders sayfalarında hangi bölümlerin boş olduğunu çıkarır.
Siteye istek atmaz; yalnız toplama programının sakladığı kopyaları okur.
Kullanım: py -3 doluluk.py <kbu_cache_klasoru>
Çıktı: analiz/doluluk.csv (ders başına) ve analiz/doluluk_program.csv (program başına)
"""
import csv, html, json, os, re, sys, collections

sys.stdout.reconfigure(encoding="utf-8")
CACHE = sys.argv[1]
D = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(D, "analiz")
courses = json.load(open(os.path.join(CACHE, "_courses.json"), encoding="utf-8"))


def text(t):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", t))).strip()


def grid_rows(t, gid):
    m = re.search(r'id="%s".*?</table>' % gid, t, re.S)
    if not m:
        return 0
    n = 0
    for row in re.findall(r"<tr[^>]*myid=.*?</tr>", m.group(0), re.S):
        tds = re.findall(r"<td[^>]*>(.*?)</td>", row, re.S)
        if any(text(x) for x in tds[1:]):
            n += 1
    return n


def after(tx, label, n=120):
    i = tx.find(label)
    return tx[i + len(label): i + len(label) + n] if i >= 0 else None


rows = []
for c in courses:
    p = os.path.join(CACHE, f"course_{c['cid']}.html")
    if not os.path.exists(p):
        continue
    t = open(p, encoding="utf-8", errors="replace").read()
    tx = text(t)
    veren = after(tx, "Dersi Verenler")
    veren = "" if veren is None else re.split(r"Dersin Yardımcıları|Dersin Staj", veren)[0].strip()
    r = {
        "seviye": c["seviye"], "birim": c["birim"], "program": c["program"], "ders_kodu": c["ders_kodu"],
        "ders_adi": c["ders_adi"], "yariyil": c["yariyil"],
        "link": f"https://obs.karabuk.edu.tr/oibs/bologna/progCourseDetails.aspx?curCourse={c['cid']}&lang=tr",
        "sayfa_tamamen_bos": "evet" if "Kayıt Yok" in tx[:400] else "",
        "ogretim_elemani": "" if veren in ("", "Yok") else veren,
        "cikti_sayisi": grid_rows(t, "grdOgrenmeCiktilari"),
        "konu_haftasi": grid_rows(t, "grdDersKonu"),
    }
    eksik = []
    if r["sayfa_tamamen_bos"]:
        eksik.append("sayfa tamamen boş")
    else:
        if not r["ogretim_elemani"]:
            eksik.append("öğretim elemanı")
        if r["cikti_sayisi"] == 0:
            eksik.append("öğrenme çıktıları")
        if r["konu_haftasi"] == 0:
            eksik.append("haftalık konular")
    r["eksikler"] = ", ".join(eksik)
    rows.append(r)

f = list(rows[0].keys())
with open(os.path.join(OUT, "doluluk.csv"), "w", newline="", encoding="utf-8-sig") as fh:
    w = csv.DictWriter(fh, fieldnames=f); w.writeheader(); w.writerows(rows)

prog = collections.defaultdict(lambda: collections.Counter())
for r in rows:
    k = (r["seviye"], r["birim"], r["program"])
    prog[k]["ders"] += 1
    prog[k]["tamamen_bos"] += bool(r["sayfa_tamamen_bos"])
    prog[k]["ciktisiz"] += r["cikti_sayisi"] == 0
    prog[k]["hocasiz"] += not r["ogretim_elemani"]
with open(os.path.join(OUT, "doluluk_program.csv"), "w", newline="", encoding="utf-8-sig") as fh:
    w = csv.writer(fh)
    w.writerow(["seviye", "birim", "program", "incelenen_ders", "tamamen_bos", "ciktisi_bos", "ogretim_elemani_yok", "ciktisi_bos_yuzde"])
    for k, v in sorted(prog.items(), key=lambda kv: -kv[1]["ciktisiz"] / kv[1]["ders"]):
        w.writerow([*k, v["ders"], v["tamamen_bos"], v["ciktisiz"], v["hocasiz"], round(100 * v["ciktisiz"] / v["ders"], 1)])

n = len(rows)
tb = sum(bool(r["sayfa_tamamen_bos"]) for r in rows)
cb = sum(r["cikti_sayisi"] == 0 for r in rows)
hb = sum(not r["ogretim_elemani"] for r in rows)
kb = sum(r["konu_haftasi"] == 0 for r in rows)
sev = {s: [r for r in rows if r["seviye"] == s] for s in ("Lisans", "Ön Lisans")}
bir = collections.defaultdict(lambda: [0, 0])
for r in rows:
    bir[r["birim"]][0] += 1; bir[r["birim"]][1] += r["cikti_sayisi"] == 0
bir = sorted(((k, 100 * v[1] / v[0], v[0]) for k, v in bir.items() if v[0] >= 100), key=lambda x: -x[1])
json.dump({"incelenen": n, "toplam": len(courses), "tamamen_bos": tb, "ciktisiz": cb, "hocasiz": hb, "konusuz": kb,
           "ciktisiz_lisans_yuzde": 100 * sum(r["cikti_sayisi"] == 0 for r in sev["Lisans"]) / max(1, len(sev["Lisans"])),
           "ciktisiz_onlisans_yuzde": 100 * sum(r["cikti_sayisi"] == 0 for r in sev["Ön Lisans"]) / max(1, len(sev["Ön Lisans"])),
           "birim_ciktisiz": bir},
          open(os.path.join(OUT, "doluluk.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"incelenen ders: {n} / {len(courses)}")
print(f"tamamen boş sayfa: {tb} (%{100*tb/n:.1f})")
print(f"öğrenme çıktısı boş: {cb} (%{100*cb/n:.1f})")
print(f"öğretim elemanı yazılmamış: {hb} (%{100*hb/n:.1f})")
print(f"haftalık konu boş: {kb} (%{100*kb/n:.1f})")
