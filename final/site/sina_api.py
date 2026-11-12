# Sunucu çalışırken çalıştırılır: python sina_api.py
import json
import sys
import time
import urllib.error
import urllib.request

TABAN = "http://127.0.0.1:8765"
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def istek(yol, gövde=None):
    veri = None if gövde is None else json.dumps(gövde, ensure_ascii=False).encode("utf-8")
    r = urllib.request.Request(TABAN + yol, data=veri, headers={"Content-Type": "application/json"},
                               method="POST" if veri is not None else "GET")
    t = time.time()
    try:
        with urllib.request.urlopen(r, timeout=120) as y:
            return y.status, json.loads(y.read().decode("utf-8")), time.time() - t
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode("utf-8")), time.time() - t


def kontrol(cumleler):
    return istek("/api/kontrol", {"cumleler": cumleler})


def vurgulu(s):
    return [s["cumle"][v["bas"]:v["son"]] for v in s["vurgular"]]


ON = ["Verilen problemi uygun yapay zekâ yöntemiyle çözer.",
      "Yapay zekâ süreçleri hakkında bilgi sahibi olur.",
      "SQL deyimleri",
      "İki sıralama algoritmasını çalışma süresi açısından karşılaştırır.",
      "Verilen gereksinimlere göre bir veri tabanı tasarlar.",
      "Temel ağ kavramlarını tanımlar.",
      "Nesne yönelimli programlamanın önemini kavrar.",
      "Bir devrenin akım ve gerilim değerlerini hesaplar."]

print("durum:", istek("/api/durum")[:2])
st, v, _ = istek("/api/veri")
print("veri:", st, "birim", len(v["birimler"]), "program", sum(len(b["programlar"]) for b in v["birimler"]),
      "| universite.birim_sayisi", v["universite"].get("birim_sayisi"), "program_sayisi", v["universite"].get("program_sayisi"))

st, y, sure1 = kontrol(ON)
print("\n8 cumle: HTTP", st, "ilk istek %.2f sn" % sure1, y["ozet"])
for s in y["sonuclar"]:
    print(" -", s["cumle"], "|", s["kalite"], s["guven"], "|", s["bloom"], s["bloom_guven"], "| vurgu:", vurgulu(s), "| not:", s["not"])
st, _, sure2 = kontrol(ON)
print("ikinci istek %.2f sn" % sure2)

print("\nbos istek:", kontrol([])[:2], kontrol(["  ", ""])[:2])
st, y, _ = kontrol(["a b c"] * 201)
print("201 cumle:", st, y)
st, y, _ = kontrol(["a b c"] * 200)
print("200 cumle:", st, y["ozet"] if st == 200 else y)

st, y, _ = kontrol(["Students will be able to explain the basic concepts."])
print("\ningilizce:", st, y["sonuclar"][0])

for c in ("Öğrenci programı yapabilir.", "Proje planlar ve kavramları tanımlar."):
    s = kontrol([c])[1]["sonuclar"][0]
    print("vurgu olmamali:", c, "|", s["kalite"], "| vurgu:", vurgulu(s), "| TAMAM" if not s["vurgular"] else "| HATA")

s = kontrol(["KAVRAMLARI ÖĞRENİR"])[1]["sonuclar"][0]
print("buyuk harf:", s["kalite"], s["guven"], "| vurgu:", vurgulu(s), "| not:", s["not"])

# oneri.py kendi başına (sunucudan bağımsız) birim sınaması
sys.path.insert(0, __file__.rsplit("\\", 1)[0] if "\\" in __file__ else ".")
try:
    import oneri
    ok = True
    for c, beklenen in (("Yapay zekâ süreçleri hakkında bilgi sahibi olur.", "bilgi sahibi olur"),
                        ("Öğrenci programı yapabilir.", None), ("Olanlar ve planlar.", None),
                        ("Kavramları tanımlar.", None), ("Konuyu kavrar ve bilir.", "kavrar"),
                        ("KAVRAMLARI ÖĞRENİR", "ÖĞRENİR")):
        vg, nt = oneri.uret(c, "BELIRSIZ")
        bulunan = c[vg[0]["bas"]:vg[0]["son"]] if vg else None
        ok &= (bulunan == beklenen)
        print("oneri:", c, "->", bulunan, "|", "TAMAM" if bulunan == beklenen else "HATA (beklenen %r)" % beklenen)
except ImportError:
    print("oneri.py bulunamadi (yalniz sunucu klasorunden calistirin)")
