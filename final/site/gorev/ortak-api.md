# Ortak sözleşme: sunucu ile sayfa arasındaki konuşma

Sunucu yalnız 127.0.0.1:8765 adresinde çalışır. Alan adları ve değerler AYNEN aşağıdaki gibidir; iki taraf da buna göre yazılır.

## GET /
`final/site/static/index.html`. Diğer dosyalar `/static/<yol>` altında (`final/site/static/`).

## GET /api/durum
`{"hazir": true, "cihaz": "cuda"}` (cihaz: "cuda" ya da "cpu")

## GET /api/veri
`final/rapor/site_veri.json` içeriği, değiştirilmeden:
- `universite`: genel istatistikler (aşağıdaki "istatistik alanları" + `birim_sayisi`, `program_sayisi`, `cikti_bos_ders`)
- `birimler`: liste; her biri `{ad, istatistikler, programlar}`
- `programlar[]`: `{ad, seviye ("Lisans" | "Ön Lisans"), istatistikler, duzeltilecek, bos_ders_sayisi}`
- `duzeltilecek[]` (en çok 15 ders): `{ders_kodu, ders_adi, cumle_sayisi, sorunlu_sayi, cumleler: [{cumle, kalite ("BELIRSIZ" | "CIKTI_DEGIL")}]}`
- İstatistik alanları: `ders_sayisi, cumle_sayisi, duzgun_sayi, belirsiz_sayi, cikti_degil_sayi, duzgun_yuzde, belirsiz_yuzde, cikti_degil_yuzde, sorunlu_sayi, sorunlu_yuzde, bloom_hatirlama_yuzde, bloom_anlama_yuzde, bloom_uygulama_yuzde, bloom_analiz_yuzde, bloom_degerlendirme_yuzde, bloom_yaratma_yuzde, bloom_bilissel_degil_yuzde, ust_basamak_sayi, ust_basamak_yuzde, ingilizce_cumle_sayisi, uni_ort_fark_puan`. Yüzdeler 0–100 arası sayıdır (ör. 53.87). Birim adları BÜYÜK HARFLE gelir (ör. "TEKNOLOJİ FAKÜLTESİ").

## POST /api/kontrol
İstek gövdesi (JSON): `{"cumleler": ["...", "..."]}`

Kurallar: her cümle baş/son boşluktan arındırılır, boş olanlar atılır; en çok 200 cümle; 1000 karakterden uzun cümle 1000'e kırpılır.

Hata yanıtları (HTTP 400): `{"hata": "En çok 200 cümle gönderilebilir."}` ya da `{"hata": "Cümle bulunamadı."}`

Başarılı yanıt (HTTP 200):
```json
{
  "ozet": {"toplam": 8, "duzgun": 5, "belirsiz": 2, "cikti_degil": 1, "ingilizce": 0},
  "sonuclar": [
    {
      "cumle": "Yapay zekâ süreçleri hakkında bilgi sahibi olur.",
      "kalite": "BELIRSIZ",
      "guven": 0.99,
      "bloom": null,
      "bloom_guven": null,
      "vurgular": [{"bas": 30, "son": 47}],
      "not": "\"bilgi sahibi olur\" ölçülemez; \"açıklar\" ya da \"karşılaştırır\" gibi bir fiil deneyin."
    }
  ]
}
```
- `kalite`: `DUZGUN` | `BELIRSIZ` | `CIKTI_DEGIL` | `INGILIZCE`
- `guven`: 0–1 arası sayı (3 basamak); `INGILIZCE`'de `null`
- `bloom`: yalnız `DUZGUN`'da dolu: `HATIRLAMA` | `ANLAMA` | `UYGULAMA` | `ANALIZ` | `DEGERLENDIRME` | `YARATMA` | `BILISSEL_DEGIL`; değilse `null`
- `bloom_guven`: yalnız `DUZGUN`'da 0–1; değilse `null`
- `vurgular`: cümlede altı çizilecek ifadelerin karakter konumları; `cumle.slice(bas, son)` (JavaScript) = `cumle[bas:son]` (Python). Yoksa `[]`. Aralıklar çakışmaz, `bas`'a göre sıralıdır.
- `not`: ekranda gösterilecek hazır Türkçe metin ya da `null`
- Sonuçlar gönderilen sırayla döner; aynı cümle iki kez gelirse iki satır döner.
