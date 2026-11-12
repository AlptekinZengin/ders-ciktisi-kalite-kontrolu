## 1. Şimdiye kadar ne yaptık?

Bu bölümde, projenin ilk iki gününü (9 ve 10 Kasım 2026) baştan sona anlatıyorum. Önce konunun ne olduğunu, sonra veriyi nasıl topladığımızı, başkalarının ne yaptığını, elle etiketlediğimiz örneği ve ilk denemeleri göreceksin. Her adımda üç şeyi söylüyorum: ne yaptık, neden yaptık, ne bulduk.

### 1.1 Konu neydi, neden değişti, yeni konu ne?

Önce eski konu vardı: röntgen görüntülerinde elektronik atığın içindeki pili bulmak (XBAT+). 9 Kasım 2026'da bu konuyu iptal ettik ve yenisine geçtik.

**Yeni konu, tek cümleyle:** Türkçe yazılmış ders öğrenme çıktılarının kalitesini yapay zekâyla denetlemek.

Şimdi bunu açalım. Bir üniversitede her dersin bir sayfası var. O sayfada "bu dersi bitiren öğrenci şunları yapabilir" diye başlayan 4 ile 8 kısa cümle yazıyor. İşte bu cümlelere **öğrenme çıktısı** diyoruz. Ehliyet kursunu düşün: "Aracı geri geri park eder" ölçülebilir bir hedeftir, çünkü eğitmen arabaya binip bakar ve ya yapabiliyordur ya yapamıyordur. "Direksiyon hakkında bilgi sahibi olur" ise ölçülemez; neyi yaparsa "bilgi sahibi" sayılacağı belli değildir. Öğrenme çıktıları da böyle yazılmalıdır.

Bizim bakacağımız kalite üç türlü olabilir:

- **Düzgün cümle:** Öğrencinin ne yapacağı açık. Ör. "Yolluk ve besleyici hacmini hesaplayabilir." Hesaplayıp hesaplayamadığına sınavda bakılabilir.
- **Belirsiz cümle:** "Bilgi sahibi olur", "öğrenir", "anlar" gibi. Ne yapılacağı ölçülemiyor.
- **Çıktı olmayan cümle:** Aslında bir konu başlığı. Ör. "SQL deyimleri". Öğrenci bununla ne yapacak, belli değil.

Cümle düzgünse ikinci bir soru soruyoruz: Bu cümle zihinde hangi basamağı istiyor? Bunun için **Bloom basamakları** denen bir merdiven kullanıyoruz. Altta hatırlama var, sonra anlama, uygulama, analiz, değerlendirme ve en üstte yaratma. Merdiven alttan yukarı doğru zorlaşıyor: bir şeyi ezbere söylemek, onu kullanmaktan kolaydır; onu kullanmak da yeni bir şey yaratmaktan kolaydır. Bir de merdivene hiç girmeyen cümleler var: el becerisi anlatanlar. Bunlara "bilişsel değil" diyoruz.

Model, yani cümleleri okuyacak yapay zekâ programı, her cümleye iki soru soracak: düzgün mü, belirsiz mi, çıktı değil mi? Düzgünse hangi basamakta?

**Neden önemli?** YÖKAK (üniversitelerin kalitesine bakan kurul) ve MÜDEK (mühendislik programlarını akredite eden kuruluş) denetimlerinde bu cümleler kullanılıyor. Ölçülemeyen bir cümle denetimde sorun çıkarıyor. Bir üniversitede on binlerce cümle var; hepsini elle okumak haftalar sürer. Yapay zekâ bu işin ilk eleğini yapabilirse, insan yalnız sorunlu olanlara bakar.

> **Neden?** Konuyu Alptekin değiştirdi. Yeni konu, üniversitelerin kalite çalışmalarında gerçek bir ihtiyaca dayanıyor ve verisi herkesin açabildiği bir sitede duruyor.

### 1.2 Veriyi nereden ve nasıl topladık?

**Kaynak.** Karabük Üniversitesi Bilgi Paketi (obs.karabuk.edu.tr/oibs/bologna). Herkesin açabildiği bir site. Önce siteyi kontrol ettik: kullanım şartı sayfası ve tarama yasağını belirten dosya (robots.txt) bulunamadı. Sitede 170 program birimi var (108 lisans, 62 ön lisans) ve toplam 14.912 ders sayfası.

**Toplayan program.** Claude küçük bir Python programı yazdı. Python, program yazmak için kullanılan bir dil. Bu program yapay zekâ değil; yalnızca bir sayfayı açıp tablodaki yazıyı kopyalayan bir yardımcı. Bu yüzden token harcamıyor (token, yapay zekânın okuduğu ve yazdığı her parçanın sayıldığı kullanım ölçüsü). Program her ders sayfasını açıyor, öğrenme çıktısı tablosunu olduğu gibi bir CSV dosyasına yazıyor. CSV, Excel'in açabildiği basit tablo dosyası.

İki önlem aldık:

- **Siteyi yormamak için** her sayfa arasında 2-3 saniye bekledi. Kapıyı art arda çalmak yerine arada nefes aldırdık.
- **Dersleri karışık sırayla indirdi.** Sırayla indirseydi ilk saatlerde yalnız birkaç fakülteyi görürdük. Karışık sırada yarım kalan veri bile bütün üniversiteyi temsil eder. Kâğıt destesini karıştırıp üstten çekmek gibi.

**Gece süreci.** Toplama 9 Kasım akşamı başladı, gece boyunca sürdü ve 10 Kasım sabahı 09:05'te bitti. Yol boyunca şunlar oldu:

- Claude uygulaması yeniden başlayınca program iki kez durdu. İki seferde de kaldığı yerden devam ettirdik.
- Alptekin'in bilgisayarını gece açık tutmak için ekranda bir geri sayım penceresi açıldı ve bilgisayarın uykuya geçmesi engellendi.
- İş bitince bilgisayar 09:07'de kendini kapattı; bu Alptekin'in isteğiydi.
- Gece inmeyen 2 ders vardı. Onları sabah ayrıca tamamladık.

**Doğrulama.** İndirdiğimiz verinin doğru olduğundan emin olmak için rastgele 20 ders seçip siteden yeniden indirdik ve karşılaştırdık. 20 dersin 20'si birebir aynı çıktı. Kopyalama hatası yok.

> **Neden?** Üzerinde çalışacağımız verinin gerçek, eksiksiz ve siteye zarar vermeden alınmış olması, sonraki her sonucun güvenilir olması için şart.

### 1.3 Başkaları ne yapmış?

Aynı işi daha önce biri yapmış mı diye literatüre baktık. Literatür, bir konuda daha önce yazılmış bilimsel çalışmaların toplamı.

Bu işi bir ajanla yürüttük (ajan, ana yapay zekâya yardım eden ikinci bir yapay zekâ çalışanı). Ajan 22 kaynağı açıp gerçekten var mı, söylediğini söylüyor mu diye doğruladı. Açılamayan 10 kaynağı dışarıda bıraktık. Ana oturumda ayrıca OpenAlex adlı bilimsel kataloğa 13 ek arama yaptık. DergiPark, Google Akademik ve YÖK Tez ise "robot değil misin?" doğrulaması istediği için bizim programlarımızla doğrudan aranamadı. Alptekin Google Akademik'e kendisi elle baktı.

Alptekin en yakın çalışmayı bulmuş oldu: **Açar (2024)**, Harran Üniversitesi. Bu çalışma yaklaşık 38 bin Türkçe çıktıyı BERT adlı bir dil modeliyle Bloom basamaklarına ayırmış, yaklaşık %90 doğruluk bildirmiş. (Bu bilgi kayıt özetinden; tam metne erişemedik.) Dikkat çekici nokta: Açar'da "kötü yazılmış cümle" diye bir seçenek yok. Her cümle bir basamağa konuyor.

**Bizim farkımız** şu: Bulabildiğimiz kadarıyla Türkçe çıktılarda önce yazım kalitesini kontrol eden, sonra Bloom basamağını bulan ve bunu bütün bir üniversiteye uygulayıp düzeltilecek dersleri listeleyen bir çalışma yok. Türkiye'deki benzer çalışmalar elle yapılmış. Örneğin Yolcu (2019) 324 kazanımı incelemiş ve %54'ünün zayıf yazıldığını bulmuş.

Raporun kaynakçasında toplam 24 kaynak var.

> **Neden?** Hocanın rubriğinde literatür taraması ve özgünlük ayrı ayrı puanlanıyor; ayrıca aynı işi tekrar yapmamak için başkasının nerede durduğunu bilmemiz gerekiyordu.

### 1.4 300 cümle ve etiketleme

Yapay zekâya bir şeyi öğretmek için önce örnek göstermek gerekir. Öğretmenin sınav kağıdını doğru cevaplarla önceden hazırlaması gibi, bizim de elimizde "doğru cevabı bilinen" cümleler olmalı. Cümlenin yanına doğru cevabı yazmaya **etiketleme** diyoruz.

**Neden 300, nasıl seçildi?** 69 bin cümleyi elle etiketlemek mümkün değil; 300 cümle ilk deneme için yönetilebilir bir sayı. Seçimi dikkatle yaptık: o anki veriden İngilizce cümleleri ve birebir tekrarları çıkardık, sonra 166 program biriminden ve 300 ayrı dersten birer cümle aldık. Sonuçta 194 lisans, 106 ön lisans cümlesi oldu. Böylece örnek tek bir bölümün değil, üniversitenin genelinin küçük bir kopyası gibi.

**Kural rehberi.** Sonnet (Claude'un bir modeli) bir etiketleme rehberi yazdı. Rehberde 6 tartışmalı karar çıktı ve hepsini Alptekin verdi:

1. "-mek/-me" ile biten eylemli cümle **düzgün** sayılır.
2. "Karşılaştırır" fiili **analiz** basamağındadır.
3. "Takip eder" **belirsiz** sayılır; neyi yapınca "takip etmiş" olunduğu belli değil.
4. El becerisi anlatan cümleler **bilişsel değil** sayılır.
5. Cümlede birden fazla fiil varsa **en yüksek basamak** geçerlidir.
6. "Bilir ve uygular" gibi karışık cümle **düzgün** sayılır.

**İlk tahmin.** 3 Sonnet, 100'er cümleye ilk tahmini yaptı. Sonuç:

- 300 cümlenin 210'u düzgün (%70), 78'i belirsiz (%26), 12'si çıktı değil (%4).
- Düzgünlerin Bloom dağılımı: uygulama 67, anlama 52, analiz 27, hatırlama 26, yaratma 20, değerlendirme 10, bilişsel değil 8.

Yani cümlelerin yaklaşık dörtte biri belirsiz. Bu zaten başta şüphelendiğimiz sorundu.

**Alptekin'in kontrolü ve sınırı.** Alptekin 300 cümlenin hepsine baktı ve kararı modelle aynı çıktı. Ama burada dürüst olmamız gereken bir sınır var: Alptekin, modelin cevabını görerek kontrol etti. Bir öğretmenin, öğrencinin cevabını görüp "doğru" demesi ile cevabı görmeden kendi çözümünü yazması aynı şey değil. Bu yüzden finalde 100 cümleyi model tahminini görmeden yeniden etiketleyecek; böylece aynı şeye iki kez bağımsız bakıp tutarlılığı ölçeceğiz.

> **Neden?** Modelin "iyi" mi "kötü" mü olduğunu anlamak için, doğru cevabı insanın onayladığı bir ölçü cetveline ihtiyacımız var.

### 1.5 Basit kural denemesi

Yapay zekâ kurmadan önce şunu sorduk: Basit bir kuralla bu iş ne kadar çözülüyor? Çözülüyorsa büyük model gereksiz olabilir; çözülmüyorsa büyük modelin neden gerektiğini göstermiş oluruz. Buna "çıta" diyoruz, yani aşılması gereken en düşük seviye.

**Ne yaptı?** Elle yazılmış bir fiil kuralı (yapay zekâ değil) 300 cümlede denendi.

**İlk hata ve düzeltme.** İlk hâlinde bir hata vardı: "kuramlarını" kelimesinin içindeki "kur" parçasını fiil sanıyordu. Hatayı bulup düzelttik.

**Sonuç.** Doğruluk %87, sınıf ortalamalı başarı (macro-F1) 0,80. Macro-F1, her sınıfa eşit ağırlık veren bir puan; az görülen sınıfta kötü olan bir yöntemi gizlemez.

**Bu sonuç neden iyimser?** Çünkü kuralı, aynı cümlelere bakarak düzelttik. Sınav sorularını görüp cevap anahtarını ona göre yazmak gibi: puan yüksek çıkar ama gerçek bir sınavda aynı olmaz. Bu yüzden %87'yi kesin sonuç gibi okumuyoruz; hiç görmediği cümlelerde kuralın biraz daha düşük kalması bekleniyor. Finalde bunu ayrı cümlelerle ölçeceğiz.

Kuralın bir zayıflığı daha var: belirsiz cümlelerin yaklaşık dörtte birini kaçırıyor.

**Tipik hata:** "Veri yapılarının uygulama alanlarını kavrar" cümlesinde kural "uygulama" kelimesini "uygular" fiili sandı (oysa burada isim) ve aslında belirsiz olan cümleyi düzgün saydı. Kelimeye bakıp cümlenin anlamına bakmamanın sınırı bu.

> **Neden?** Büyük modelin değerini ölçebilmek için, hiç yapay zekâ kullanmayan basit bir yöntemin nereye kadar gelebildiğini bilmemiz gerekiyordu.

### 1.6 Tam veriden çıkan bulgular

Şimdi 300 cümlelik örneği bırakıp bütün veriye bakalım. Her sayının yanına ne anlama geldiğini yazıyorum.

- **14.912 ders, 69.186 cümle, 29 birim, 168 program birimi.** Üniversitenin bütün ders sayfaları elimizde. (Sitede 170 program birimi var; bunlardan 2'sinin sitede hiç ders listesi olmadığı için cümleler 168 programdan geliyor.)
- **214 cümle İngilizce.** Bunlar Türkçe kalite denetimine girmez, ayrı tutuyoruz.
- **Cümlelerin yalnız 32.348'i birbirinden farklı.** Yani 69 binin yarısına yakını başka bir cümlenin kopyası. Sebebi ortak dersler: aynı dersi birçok program okutuyor ve herkes aynı cümleyi kullanıyor. Örneğin "Öğrenciler hedef dile karşı pozitif bir tutum geliştireceklerdir." cümlesi 246 ders sayfasında aynen duruyor. Pratik sonuç: bir cümleyi düzeltirsek yüzlerce sayfa birden düzelir.
- **265 derste aynı çıktı ders içinde birden fazla yazılmış** (458 fazla satır). Aynı cümle bir derste gereksiz yere tekrar edilmiş.
- **En sık son kelimeler:** açıklar 3.935, bilir 3.320, eder 2.712, öğrenir 2.617, olur 2.604. Türkçede fiil cümlenin sonunda gelir, bu yüzden son kelime çoğu zaman çıktının fiilidir. İlk beşin üçü ("bilir", "öğrenir", "olur") belirsizlik işareti; yani en çok kullanılan fiillerin bir kısmı ölçülemeyen fiiller.
- **Boş ders sayfaları** (Alptekin'in isteğiyle eklendi):
  - 792 ders sayfası tamamen boş (%5,3). Örnek: BBB223 Makine Öğrenme ve MLOps Yazılım Geliştirme dersinin sayfasında yalnız "Kayıt Yok" yazıyor.
  - 1.210 derste çıktı yok (%8,1).
  - 2.478 derste öğretim elemanı yazılmamış (%16,6).
  - 1.000 derste haftalık konu yok (%6,7).

  Bunlar yazım kalitesinden önce gelen bir sorun: yazılmamış bir şeyin kalitesi ölçülemez.
- **Birimler arası fark.** Basit kurala göre belirsiz çıkan cümle oranı Rektörlüğe bağlı ortak seçmeli havuzda %46 ile en yüksek, Mühendislik ve Doğa Bilimleri Fakültesi'nde %15 ile en düşük. Yani sorun her yerde aynı yoğunlukta değil; bazı birimlerin yardıma daha çok ihtiyacı var.

Burada bir not: bu oranlar basit kuralın tahmini. Kural iyimser olduğu için kesin değerler değil, genel resim olarak okunmalı.

> **Neden?** Proje "yalnız bir örnekte çalışıyor" olmasın diye, hangi sorunun ne kadar yaygın olduğunu bütün veride görmek istedik.

### 1.7 Vize raporu

Vize, final projesinin ilk aşaması ve yalnız rapordan oluşuyor. Rapor makale biçiminde, yaklaşık 12 sayfa olacak; metin içi atıf ve kaynakça zorunlu. Hoca dört şeyi puanlıyor: problem tanımı ve amaç 20, literatür taraması 30, veri seti ve ön analiz 25, özgünlük ve literatür boşluğu 25 puan. Teslim tarihi 12 Kasım 2026.

Rapor yazıldı:

- 13 sayfa, Word ve PDF olarak.
- Masaüstünde "Vize-Raporu-Kalite" adıyla duruyor.
- İçinde 5 grafik, 5 tablo ve 24 kaynak var.
- Birinci ağızdan, öğrenci sesiyle yazıldı.
- Sonunda yapay zekâ kullanım beyanı var. Hoca yapay zekâ kullanımına izin verdi ama metindeki "yapay zekâ yazısı oranına" bakıyor.

Sayılar elle yazılmadı: veriden otomatik dolduruluyor. Veri değişirse tek komutla rapor yeniden üretilir ve sayılar kendiliğinden güncellenir. Bu, "rapordaki sayı ile veri tutmuyor" hatasını baştan engelliyor.

Rapora ek olarak şunlar da hazırlandı: lise düzeyinde proje anlatımı PDF'i (5 sayfa, 9 Kasım), Excel kontrol tablosu ve boş ders listesi (her ders için eksikler ve sayfa linki).

> **Neden?** Vize puanını rubriğin dört başlığına göre alabilmek ve sayıları el hatasından korumak için raporu bir kez yazıp sayıları veriden otomatik çekecek şekilde kurduk.
