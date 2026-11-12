# Bilgi listesi (ajanlar için tek doğru kaynak)

Bu dosyadaki bilgiler doğrulanmıştır. Anlatımda yalnız bunları kullan. Burada olmayan sayı, tarih, isim ya da iddia ekleme. Bilinmeyen şeyi "henüz belli değil" diye yaz.

## Kişiler ve ders
- Öğrenci: Alptekin. Ders: Yapay Zekâ. Hoca rapora yapay zekâ kullanımına izin verdi ama metindeki "yapay zekâ yazısı oranına" bakıyor.
- Vize = final projesinin ilk aşaması, yalnız rapor. Rubrik: problem tanımı ve amaç 20, literatür taraması 30, veri seti ve ön analiz 25, özgünlük ve literatür boşluğu 25. Makale biçimi, yaklaşık 12 sayfa, metin içi atıf ve kaynakça zorunlu.
- Vize teslim: 12 Kasım 2026. Final: aynı projenin çalıştığını göstermek (Alptekin beyanı). Final tarihi bu dosyada bilinmiyor.

## Konu nasıl değişti
- Eski konu: röntgen görüntülerinde elektronik atık içindeki pili bulmak (XBAT+). 9 Kasım 2026'da iptal edildi.
- Yeni konu (9 Kasım 2026): Türkçe ders öğrenme çıktılarının yapay zekâyla kalite kontrolü.
- Öğrenme çıktısı: her dersin sayfasında "bu dersi bitiren öğrenci şunları yapabilir" diye yazan 4-8 kısa cümle.
- Model her cümleye iki soru soracak: (1) Düzgün mü, belirsiz mi ("bilgi sahibi olur", "öğrenir", "anlar"), çıktı değil mi (konu başlığı, ör. "SQL deyimleri")? (2) Düzgünse Bloom basamağı: hatırlama, anlama, uygulama, analiz, değerlendirme, yaratma. El becerisi cümleleri "bilişsel değil".
- Neden önemli: YÖKAK (üniversite kalite kurulu) ve MÜDEK (mühendislik akreditasyonu) denetimlerinde bu cümleler kullanılıyor; ölçülemeyen cümle denetimde sorun çıkarır. Bir üniversitede on binlerce cümle var; elle okumak haftalar sürer.

## Yapılanlar, sırasıyla (9-10 Kasım 2026)
1. Site kontrolü: Karabük Üniversitesi Bilgi Paketi (obs.karabuk.edu.tr/oibs/bologna). Kullanım şartı sayfası ve tarama yasağı (robots.txt) bulunamadı. Sitede 170 program birimi (108 lisans, 62 ön lisans) ve 14.912 ders sayfası var.
2. Toplama programı: Claude'un yazdığı küçük bir Python programı. Yapay zekâ değil, token harcamaz. Her ders sayfasını açıp öğrenme çıktısı tablosunu olduğu gibi bir tabloya (CSV) yazıyor. Siteyi yormamak için her sayfa arasında 2-3 saniye bekledi. Dersleri karışık sırayla indirdi ki yarım veri bile bütün üniversiteyi temsil etsin.
3. Toplama 9 Kasım akşam başladı, gece boyunca sürdü, 10 Kasım sabah 09:05'te bitti. Arada Claude uygulaması yeniden başlayınca iki kez durdu; kaldığı yerden devam ettirildi. Geri sayım penceresi açıldı, uyku engeli kondu; bitince bilgisayar 09:07'de kendini kapattı (Alptekin'in isteği). Gece inmeyen 2 ders sabah tamamlandı.
4. Doğrulama: rastgele 20 ders siteden yeniden indirilip karşılaştırıldı: 20/20 birebir aynı.
5. Literatür taraması: Opus (düşük) ajan 22 kaynağı açıp doğruladı; açılamayan 10 kaynak dışarıda bırakıldı. Ana oturum OpenAlex kataloğunda 13 ek arama yaptı (DergiPark, Google Akademik ve YÖK Tez robot doğrulaması istediği için doğrudan aranamadı). Alptekin Google Akademik'e elle baktı ve en yakın çalışmayı buldu: Açar (2024), Harran Üniversitesi, yaklaşık 38 bin Türkçe çıktıyı BERT ile Bloom'a ayırmış, yaklaşık %90 doğruluk (kayıt özetine göre; tam metin kapalı). Açar'da "kötü yazılmış cümle" seçeneği yok. Raporun kaynakçasında toplam 24 kaynak var.
6. Boşluk (bizim farkımız): Bulabildiğimiz kadarıyla Türkçe çıktılarda önce yazım kalitesini kontrol eden, sonra Bloom basamağını bulan ve bunu bütün üniversiteye uygulayıp düzeltilecek dersleri listeleyen çalışma yok. Türkiye'deki benzer çalışmalar elle yapılmış (ör. Yolcu 2019: 324 kazanımın %54'ü zayıf yazılmış).
7. 300 cümlelik örnek: o anki veriden İngilizce cümleler ve birebir tekrarlar çıkarıldı, 166 program biriminden ve 300 ayrı dersten 300 cümle seçildi (194 lisans, 106 ön lisans).
8. Kural rehberi: Sonnet (orta) bir etiketleme rehberi yazdı. Rehberde 6 tartışmalı karar vardı, Alptekin hepsini verdi: "-mek/-me" ile biten eylemli cümle = düzgün; "karşılaştırır" = analiz; "takip eder" = belirsiz; el becerisi = bilişsel değil; birden fazla fiil varsa en yüksek basamak; "bilir ve uygular" gibi karışık cümle = düzgün.
9. İlk etiketler: 3 Sonnet (orta) 100'er cümleye ilk tahmini yaptı. Sonuç: 210 düzgün (%70), 78 belirsiz (%26), 12 çıktı değil (%4). Bloom (düzgünler): uygulama 67, anlama 52, analiz 27, hatırlama 26, yaratma 20, değerlendirme 10, bilişsel değil 8.
10. Kontrol: Alptekin 300 cümleyi kontrol etti, kararı modelle aynı çıktı. Sınır: modelin cevabını görerek kontrol etti; bu yüzden finalde 100 cümleyi tahmini görmeden yeniden etiketleyecek.
11. Basit kural denemesi: Elle yazılmış bir fiil kuralı (yapay zekâ değil) 300 cümlede denendi. İlk hâlinde bir hata vardı ("kuramlarını" içindeki "kur"u fiil sanıyordu), düzeltildi. Sonuç: doğruluk %87, sınıf ortalamalı başarı (macro-F1) 0,80. Bu sayı iyimser, çünkü kural aynı cümlelere bakılarak düzeltildi. Kural belirsiz cümlelerin yaklaşık dörtte birini kaçırıyor. Tipik hata: "Veri yapılarının uygulama alanlarını kavrar" cümlesinde "uygulama" ismini fiil sandı.
12. Tam veri sonuçları: 14.912 ders, 69.186 cümle, 29 birim, 168 program birimi. 214 cümle İngilizce. Cümlelerin yalnız 32.348'i birbirinden farklı (ortak dersler aynı cümleyi kullanıyor; "Öğrenciler hedef dile karşı pozitif bir tutum geliştireceklerdir." 246 ders sayfasında aynen var). 265 derste aynı çıktı ders içinde birden fazla yazılmış (458 fazla satır). En sık son kelimeler: açıklar 3.935, bilir 3.320, eder 2.712, öğrenir 2.617, olur 2.604; ilk beşin üçü belirsizlik işareti.
13. Boş ders sayfaları (Alptekin'in isteğiyle eklendi): 792 ders sayfası tamamen boş (%5,3), 1.210 derste çıktı yok (%8,1), 2.478 derste öğretim elemanı yazılmamış (%16,6), 1.000 derste haftalık konu yok (%6,7). Örnek: BBB223 Makine Öğrenme ve MLOps Yazılım Geliştirme dersinin sayfası "Kayıt Yok".
14. Birimler arası fark (basit kurala göre belirsiz oranı): en yüksek Rektörlüğe bağlı ortak seçmeli havuz %46, en düşük Mühendislik ve Doğa Bilimleri Fakültesi %15.
15. Vize raporu yazıldı: 13 sayfa, Word ve PDF, masaüstünde "Vize-Raporu-Kalite". 5 grafik, 5 tablo, 24 kaynak, sonda yapay zekâ kullanım beyanı. Birinci ağızdan öğrenci sesiyle yazıldı. Sayılar veriden otomatik dolduruluyor; veri değişirse tek komutla yeniden üretilir.
16. Ayrıca hazırlananlar: liseliye proje anlatımı PDF'i (5 sayfa, 9 Kasım), Excel kontrol tablosu, boş ders listesi (her ders için eksikler ve sayfa linki).

## Vize için kalan işler (10-12 Kasım)
- Alptekin raporu baştan sona okuyacak.
- Yapay zekâ yazı oranı testi: bir tespit aracında bölüm bölüm denenecek, yüksek çıkan bölümler birlikte yeniden yazılacak.
- 12 Kasım: teslim.

## Final planı (raporda verilen söz)
1. Etiketli veriyi 300'den yaklaşık 800 cümleye çıkarmak. Model en emin olmadığı cümleleri seçecek, Alptekin etiketleyecek (az olan "çıktı değil" ve üst basamaklar için).
2. 100 cümleyi model tahminini görmeden yeniden etiketleyip tutarlılığı ölçmek.
3. Dört yöntemi sırayla denemek ve karşılaştırmak:
   - Kural tabanlı yöntem (çıta).
   - Klasik makine öğrenmesi: kelime sayımına dayalı (TF-IDF) + SVM / lojistik regresyon. Saniyeler içinde çalışır.
   - BERTurk: Türkçe metinlerle önceden eğitilmiş dil modeli, bizim örneklerle ince ayar. Alptekin'in RTX 4060 ekran kartı ve 16 GB RAM'i yetiyor.
   - İsteğe bağlı: büyük dil modeline rehberle doğrudan sormak.
4. Başarıyı sınıf başına ölçmek (macro-F1) ve karışıklık tablosu çıkarmak. Aynı cümle hem eğitimde hem testte olmayacak; bir birim tamamen dışarıda bırakılıp hiç görmediği alanda da sınanacak.
5. En iyi modeli 69 bin cümlenin hepsine uygulayıp program düzeyinde rapor üretmek.

## Sonunda elde ne olacak (kesin olanlar)
- Karabük Üniversitesi'nin bütün derslerini kapsayan Türkçe öğrenme çıktısı veri seti (69.186 cümle).
- Yazılı etiket rehberi ve Alptekin'in kontrol ettiği etiketli örnek.
- Eğitilmiş bir sınıflandırıcı (cümleyi alıp kalite + Bloom basamağı veren model) ve dört yöntemin karşılaştırması.
- Program düzeyinde rapor: her program için boş ders sayfaları, belirsiz/çıktı değil cümle oranı, Bloom dağılımı, ders içi tekrarlar ve "düzeltilecek dersler" listesi (her dersin sayfa linkiyle).
- Final raporu.

## Karar (Alptekin, 10 Kasım 2026): B seçildi
- Finalde bir "uygulama" olacak mı? Seçenekler:
  - A) Yalnız model + program raporu (PDF/Excel). En az iş.
  - B) A + küçük bir web sayfası: cümleyi yapıştır, model "belirsiz, şu fiil sorunlu, şöyle yazabilirsin" desin; ayrıca program seçip raporunu gör. Bilgisayarda çalışır; istenirse internete konur. Finalde "çalıştığını göstermek" için en etkili seçenek.
  - C) B'nin daha büyüğü: başka üniversitelerin bilgi paketlerini de tarayan araç. Vize raporunda bu kapsam dışı dendi.
- Claude'un önerisi: B. Ama karar Alptekin'in.
