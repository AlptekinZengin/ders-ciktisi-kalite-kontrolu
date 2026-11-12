# Proje Durum Raporu

Yapay Zekâ dersi vize ve final projesi · Türkçe ders öğrenme çıktılarının yapay zekâyla kalite kontrolü · 10 Kasım 2026

> **Tek paragrafta:** Üniversitelerde her dersin "bu dersi bitiren öğrenci şunları yapabilir" diye yazılmış cümleleri var. Bu cümlelerin bir kısmı kötü yazılmış ya da hiç yazılmamış. Biz Karabük Üniversitesi'nin 14.912 dersinin sayfasını indirip 69.186 cümle topladık, 300 tanesini elle kontrol ettik, sorunların ne kadar yaygın olduğunu ölçtük ve bunların hepsini 13 sayfalık bir vize raporuna yazdık. Finalde, bu cümleleri kendisi okuyup "düzgün mü, belirsiz mi, ne kadar zor bir beceri istiyor?" diyen bir yapay zekâ modeli eğiteceğiz ve hangi derslerin düzeltilmesi gerektiğini gösteren bir rapor çıkaracağız.

## Bu raporu kimler hazırladı?

Bu raporun bölümlerini ajanlara dağıttık. Hangi bölümü kimin yazdığı:

| Bölüm | Kim yazdı | Model ve düşünme düzeyi |
|---|---|---|
| Doğru bilgi listesi (ajanların dayandığı tek kaynak) | Ana oturum | Claude Opus 5.5 |
| 1. Şimdiye kadar ne yaptık? | Ajan 1 | Claude Sonnet, orta |
| 2. Bundan sonra ne olacak? ve 3. Sonunda elimizde ne olacak? | Ajan 2 | Claude Sonnet, orta |
| Kontrol, birleştirme, PDF | Ana oturum | Claude Opus 5.5 |

Projenin kendisinde şimdiye kadar çalışan ajanlar: literatür taraması için 1 Opus (düşük), kural rehberi ve 300 cümlenin ilk tahmini için 3 Sonnet (orta). Veriyi toplayan program bir yapay zekâ değil, sıradan bir Python programı; token harcamadı.
