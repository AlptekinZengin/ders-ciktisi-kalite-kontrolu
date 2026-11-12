# Etiketleme Kural Rehberi: Ders Öğrenme Çıktısı Kalitesi ve Bloom Basamağı

Amaç: farklı etiketleyiciler aynı cümleye aynı etiketi versin. Örnekler `ornek_300.csv` dosyasındaki `no` ile verilir. Bu örneklerin etiketi Alptekin onaylayana kadar **öneridir**, doğru cevap anahtarı değildir.

Dayanak: iki aşamalı yaklaşım (önce yapı/kalite, sonra Bloom) Yolcu (2019)'dan; revize basamaklar Anderson ve Krathwohl (2001)'den. Newton, Da Silva ve Peters (2020) fiil listelerinin kurumlar arasında az örtüştüğünü ve "kaçınılacak fiiller" listesi çıkardığını gösterir; bu yüzden **fiil tablosu tek başına karar vermez, bağlam kuralları gerekir**. Aşağıdaki Türkçe fiil tabloları bu çalışmanın **çalışma önerisidir**, bir kaynaktan çevrilmemiştir.

## 1. Karar sırası

1. Cümlede **öğrencinin yapacağı bir eylem** (fiil ya da fiilimsi) var mı? Yoksa → **CIKTI_DEGIL**. Dur.
2. Eylem **dışarıdan görülüp ölçülebilir** mi (bir ürün, işlem, cevap üretir mi)? Hayır → **BELIRSIZ**. Dur.
3. Evet → **DUZGUN**. Şimdi Bloom: eylem bilişsel mi? Değilse `BILISSEL_DEGIL`, bilişselse 4. bölümdeki tabloyla basamak seç.
4. Emin değilsen 5. bölümdeki "güven" ve "gerekçe" kuralını uygula.

Test sorusu (2. adım): "Bir hoca bu cümleye bakıp öğrencinin başardığını kanıtlayacak bir sınav sorusu ya da ödev yazabilir mi?" Evet → DUZGUN.

## 2. Kalite sınıfları

**DUZGUN**: Ölçülebilir öğrenci eylemi var. Örnekler: 10 (Basit elektrik devrelerini analiz eder), 51 (Blok zincir teknolojisini açıklar), 86 (Denge denklemlerini kullanarak ... statik büyüklükleri hesaplar), 107 (Dosya sistemi ... izinlerini yapılandırır), 60 (Sonlu elemanlar yöntemini kullanarak ... problemleri çözer).
Sınır: eylem var ama nesne çok genel ("Yeni ürünler geliştirebilir", 120; "Pazar araştırması yapar", 134) → DUZGUN, güven orta.

**BELIRSIZ**: Cümle çıktı gibi kurulmuş ama eylem ölçülemez: bilir, öğrenir, anlar, kavrar, bilgi sahibi olur, farkındalık kazanır, beceri kazanır/geliştirir, hâkimiyet sağlar, gelişir. Örnekler: 43 (Sistemlerin anatomik yapılarını bilir), 188 (Küreselleşmeyi anlar), 189 (... hakkında bilgi sahibi olur), 75 (... kuramlarını öğrenir), 221 (Teknik hakimiyet sağlar).
Sınır: "Algoritmik düşünebilir" (57), "Algılama gücü gelişir" (35) → BELIRSIZ (-ebilir eki eylemi ölçülebilir yapmaz).

**CIKTI_DEGIL**: Öğrenci eylemi yok. Konu başlığı, isim öbeği, yarım ifade, ders içeriği, hocanın işi. Örnekler: 2 (Sinyal ve sistemlerin temel kavramları.), 270 (Çevre uygulamaları), 259 (savunma ve hücum duruşları, hücum sistemleri), 85 (Analiz ve Sentez kapasitesi), 53 (İşletmelerin vergi dairesine, SGK'ya ... yükümlülükleri).
Hocanın işi: 83 ("... tanımlayabilmesine olanak verecektir"), 172 ("... hakkında bilgilendirme").
Sınır: 8 ve 204 gibi "öğrenilmesi" / "önemi" ile biten uzun isim öbekleri → CIKTI_DEGIL.

## 3. Türkçeye özgü kurallar

| Durum | Kural | Örnek |
|---|---|---|
| -ebilir/-abilir | Ek eylemi ölçülebilir yapmaz; **kökteki fiile** bak. | 11 "belirleyebilir" → DUZGUN; 57 "düşünebilir" → BELIRSIZ |
| -me/-ma/-mek ile biten, nesneli ve eylem kökü ölçülebilir | **DUZGUN** sayılır (öğrenci eylemi anlaşılıyor), güven orta. | 110 "Patent başvuru dosyası hazırlayabilmek", 153, 217, 280, 101 |
| -me/-ma/-mek, fiil belirsiz | BELIRSIZ | 47 "bilgi sahibi olmak", 93 "iletişim becerilerini geliştirmek", 154 |
| -me/-ma, nesnesiz ya da yalnız konu | CIKTI_DEGIL | 85, 204 |
| Edilgen "öğretilir/öğrenilir" | Özne öğrenci değilse de "öğrenilir" belirsiz fiil sayılır → BELIRSIZ. Edilgen ama ölçülebilir fiil ("hazırlanır") → DUZGUN, güven orta. | 14 "Üretim Planları Öğrenilir", 295 |
| "Öğrenciler ... yapacaklardır / edinirler" kalıbı | Kalıbı (öğrenciler, bu dersi alan, dönem sonunda, -acaktır) **at**; geriye kalan fiile bak. | 79 "takip edebileceklerdir", 158 "tanımlayabileceklerdir" → DUZGUN; 155 "bilgiler edinirler" → BELIRSIZ |
| "Becerisi/yeteneği kazanır" | Kazanılan beceri ölçülebilir eylemse DUZGUN, genelse BELIRSIZ. | 46 "hesaplama ... çözme yeteneği kazanır" → DUZGUN; 21 "gerekli becerileri kazanır" → BELIRSIZ |
| Yazım/imla hatası | Kaliteyi **etkilemez**. Fiil tanınıyorsa etiketle; gerekçeye "yazım" yaz. | 20 "kulanabilmek", 37 "kulanır", 203 "Literratur tarayabilir" |
| Birden çok fiil | Ölçülebilir **en az bir** fiil varsa DUZGUN. Belirsiz fiil yanında ölçülebilir fiil varsa belirsiz kısım yok sayılır. | 125 "bilir ve uygulayabilir" → DUZGUN; 156 "bilir, karşılaştırır ve yorumlar" → DUZGUN |
| Fiilsiz ama anlaşılır | Yalnız isim varsa CIKTI_DEGIL. Eylem kökü ve nesnesi varsa (-ma/-me) yukarıdaki kural. | 54 "R'da Grafikler ve tablolar oluşturma" → DUZGUN (orta) |
| Çok genel ama eylemli | Eylem ölçülebilirse DUZGUN, güven orta. Fiilin kendisi boşsa ("yapabilir", nesne yok) BELIRSIZ. | 120 → DUZGUN; 42 "Nüans Yapabilir" → BELIRSIZ (düşük) |
| Dil karışık / bozuk | Türkçe kısım esas alınır. Okunamayan ya da anlamı kopuk → CIKTI_DEGIL. | 108 (Türkçe + İngilizce kopya), 94 "Plans trains in railways," → CIKTI_DEGIL (düşük), 124 |

"Takip eder" (12, 29, 131, 195): tek başına gözlenebilir ürün vermez. Karar: BELIRSIZ (Alptekin kararı, Karar 3).

## 4. Bloom (yalnız DUZGUN ise)

Tabloya göre **cümlenin ana ölçülebilir fiili ve nesnesi** bakılır. Tablo bir sözlük değil, başlangıç noktasıdır.

| Basamak | Fiiller (çalışma önerisi) |
|---|---|
| HATIRLAMA | tanımlar, sayar, listeler, adlandırır, tanır, hatırlar, ezberler, belirtir, söyler, eşleştirir, yazar (ezberden), bulur (bilgiyi), isimlendirir, işaretler |
| ANLAMA | açıklar, özetler, yorumlar, örneklendirir, sınıflandırır, ilişkilendirir, tahmin eder, anlatır, tarif eder, tasvir eder, çevirir, ifade eder, ayırt eder |
| UYGULAMA | uygular, kullanır, hesaplar, çözer, yapar, kurar, çizer, hazırlar, yapılandırır, kodlar, gösterir, yürütür, uyarlar, işletir |
| ANALIZ | analiz eder, karşılaştırır, inceler, ayrıştırır, çözümler, irdeler, sorgular, ayırt eder (ögelere ayırarak), tespit eder (neden/arıza), ilişkisini çözer, test eder, kategorize eder |
| DEGERLENDIRME | değerlendirir, eleştirir, yargılar, savunur, gerekçelendirir, karar verir, önceliklendirir, denetler, doğrular, puanlar, seçer (ölçütle gerekçelendirerek) |
| YARATMA | tasarlar, geliştirir (yeni ürün/algoritma), oluşturur (özgün), planlar, üretir, kurgular, sentezler, formüle eder, modeller, besteler, inşa eder |

**Bağlama göre değişen fiiller**: kural, "fiil önceden verilmiş bilgiyi mi çağırıyor, bilinen yöntemi mi çalıştırıyor, yoksa yeni bir bütün mü kuruyor?"

- **seçer**: listeden seçme → HATIRLAMA; ölçütle gerekçelendirerek seçme → DEGERLENDIRME.
- **belirler**: bilinen değeri/özelliği saptama → ANLAMA/HATIRLAMA (74 "özelliklerini belirler"); neden-sonuç tespiti → ANALIZ; yöntem ve süreç tasarlama → YARATMA (136).
- **yorumlar**: verilen bilgiyi kendi sözleriyle açma → ANLAMA (139, 3); ölçüte göre yargı → DEGERLENDIRME.
- **kullanır**: bilinen aracı/yöntemi çalıştırma → UYGULAMA (37, 148). Nesne kavramsalsa emin değilsen UYGULAMA, güven orta.
- **geliştirir / hazırlar / planlar / oluşturur**: kalıp izleyerek yeniden üretme → UYGULAMA; kendi ürünü/tasarımı → YARATMA.
- **tartışır**: sav-karşısav üretme → DEGERLENDIRME; konuyu anlatma → ANLAMA.
- **karşılaştırır**: her zaman ANALIZ (Alptekin kararı, Karar 2).

**Birden çok ölçülebilir fiil**: **en yüksek basamak** seçilir. Gerekçe: çıktıyı sınayan soru, cümledeki en zor eylemi içermek zorundadır; "ana fiil" ise kişiye göre değişir ve uyumu düşürür. Örnekler: 16 "kurar ve analiz eder" → ANALIZ; 78 "anlar ve uygular" → UYGULAMA; 248 "anlayıp analiz edebilir" → ANALIZ. İstisna: belirsiz fiil (bilir, anlar, öğrenir) basamağa katılmaz; 65 "öğrenir ve örneklendirir" → ANLAMA.

**Bilişsel olmayan ama düzgün cümleler**: Bloom alanına girmez, `bloom = BILISSEL_DEGIL`. Kural: ana eylem bedensel/duyusal yürütmeyse (çalmak, pişirmek, el becerisi, ses/beden kullanımı) ya da duyuşsal tutumsa (değer verir, savunur kimlik olarak) bu etiket. Hesap, çizim planı, kod yazma, rapor hazırlama gibi **zihinsel işlem** ağırlıklıysa bilişsel say. Örnekler: 63 ("32'lik değerleri çalar"), 122 (sağ ve sol eli kullanır), 164 (müzikal icra), 4 (kalıp yapar), 89 (pişirir) → BILISSEL_DEGIL. 300 ("ezberden okuyacak şekilde ezberler") → HATIRLAMA. Gerekçe: Anderson ve Krathwohl yalnız bilişsel süreç boyutunu tanımlar; psikomotor ve duyuşsal basamağı zorla UYGULAMA'ya sokmak uyumu bozar. Alternatif için Açık Karar 4.

## 5. Kararsız kalınca

- `guven = yuksek`: tek fiil, tabloda açık, bağlam kuralı gerekmedi.
- `guven = orta`: iki sınıf arasında kaldın ama bir kural seni bir tarafa itti (örn. -me ile biten DUZGUN, çok genel ama eylemli).
- `guven = dusuk`: kuralla da karar veremedin ya da cümle bozuk/anlamsız. Gerekçeye "emin değilim" ve **iki aday etiketi** yaz.
- Gerekçe en çok 15 kelime, somut: "Fiil: hesaplar, UYGULAMA tablosunda" ya da "Nesnesiz isim öbeği, eylem yok".
- Kararsız kalıp sessizce tahmin etme; düşük güven bir bulgudur, hata değildir.

## 6. KARARLAR (Alptekin onayladı, 2026-11-09)

1. **-me/-ma/-mek ile biten eylemli cümleler** (110, 153, 193, 217, 280): DUZGUN; Bloom fiile göre verilir. Eylemsiz isim öbekleri ("Analiz ve Sentez kapasitesi") CIKTI_DEGIL kalır.
2. **"karşılaştırır"**: ANALIZ.
3. **"takip eder / takip edebilir"** (12, 29, 131, 195): BELIRSIZ.
4. **Psikomotor/duyuşsal düzgün cümleler** (63, 122, 164, 4, 89): kalite DUZGUN, bloom `BILISSEL_DEGIL`.
5. **Çoklu fiilde basamak**: ölçülebilir fiiller arasından en yüksek basamak.
6. **Belirsiz + ölçülebilir karma cümle** ("bilir ve uygular", 125, 220): DUZGUN; belirsiz kısım yok sayılır, basamak ölçülebilir fiile göre.

## 7. Çıktı biçimi

UTF-8 CSV, başlık satırıyla, sütunlar:

`no,kalite,bloom,guven,gerekce`

- `kalite`: DUZGUN | BELIRSIZ | CIKTI_DEGIL
- `bloom`: HATIRLAMA | ANLAMA | UYGULAMA | ANALIZ | DEGERLENDIRME | YARATMA | BILISSEL_DEGIL; kalite DUZGUN değilse **boş**.
- `guven`: yuksek | orta | dusuk
- `gerekce`: en çok 15 kelime, virgül içeriyorsa tırnak içine al.

Örnek satırlar:
`10,DUZGUN,ANALIZ,yuksek,Fiil: analiz eder`
`43,BELIRSIZ,,yuksek,"bilir: ölçülemez fiil"`
`2,CIKTI_DEGIL,,yuksek,"Konu başlığı, eylem yok"`

## Ek karar (Alptekin, 2026-11-10)

- Son kelimesi "-ilmesi / -ılması / -ması / -mesi" ile biten isim öbekleri (ör. "Stratejilerin uygulanması", "Temanın işlenmesi") **CIKTI_DEGIL** sayılır. (Alptekin: "Evet, çıktı değil")
