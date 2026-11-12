## 2. Bundan sonra ne olacak?

Şimdiye kadar veriyi topladık, kaynakları taradık, kuralları yazdık ve vize raporunu hazırladık. Geriye iki yol kalıyor: önce vizeyi teslim etmek, sonra finale doğru asıl işi yapmak. Bu bölümde ikisini sırayla anlatıyorum.

### 2.1 Vize için kalan işler (10-12 Kasım)

Vize yalnızca rapordan oluşuyor ve rapor hazır. Teslime kadar üç iş var.

**Adım 1: Alptekin raporu baştan sona okuyacak.** Rapor yapay zekâ yardımıyla ve senin sesinle yazıldı, ama onu sahiplenecek kişi sensin. Okurken şunlara bak: Anlattıkların senin yaptıklarınla uyuşuyor mu? Anlamadığın bir cümle var mı? Hoca sana bir şey sorsa cevaplayabilir misin? Takıldığın yeri işaretlemen yeterli, düzeltmeyi birlikte yaparız. Sayılar veriden otomatik doldurulduğu için bir sayıyı değiştirmek gerekirse tek komutla rapor yeniden üretilir.

**Adım 2: Yapay zekâ yazı oranı testi.** Hocamız rapor yazarken yapay zekâ kullanmana izin verdi, ama metindeki "yapay zekâ yazısı oranına" bakıyor. Bu yüzden teslimden önce kendimiz de bakacağız. Raporu bir tespit aracına bölüm bölüm yükleyeceğiz. Neden bölüm bölüm? Çünkü bütün rapora tek puan veren bir araç, hangi kısmın sorunlu olduğunu göstermez. Bölüm bölüm bakınca yüksek çıkan yerleri tek tek görürüz. Bu yerleri birlikte yeniden yazacağız. Yeniden yazarken senin kendi cümlelerin, kendi örneklerin ve yaptığın işe dair somut ayrıntıların metne girmesi hem oranı düşürür hem de raporu gerçekten senin yapar.

**Adım 3: 12 Kasım'da teslim.** Rapor Word ve PDF olarak masaüstünde "Vize-Raporu-Kalite" adıyla duruyor. Son sürümü seçip teslim edeceksin. Teslimden önce makale biçimi, metin içi atıflar ve kaynakça bir kez daha kontrol edilecek, çünkü rubrikte bunlar zorunlu.

### 2.2 Final yolculuğu

Final, aynı projenin çalıştığını göstermek. Vize raporunda bu iş için beş adımlık bir plan sözü verdik. Bunları sırayla anlatıyorum.

**Adım 1: Etiketli veriyi 300 cümleden yaklaşık 800 cümleye çıkarmak.**
Etiketli veri, cevabı yazılı bir soru bankası gibidir. Model bu soruları ve cevaplarını görerek öğrenir. Elimizde şu an 300 çözümlü soru var, bunu yaklaşık 800'e çıkaracağız. Ama rastgele cümle eklemeyeceğiz. Model, en emin olmadığı cümleleri seçecek ve Alptekin onları etiketleyecek. Tıpkı bir öğrencinin zorlandığı soru tiplerinden daha çok çözmesi gibi. Özellikle "çıktı değil" (sadece 12 örnek var) ve üst Bloom basamakları (değerlendirme, yaratma) için bu önemli, çünkü bu sınıflarda örnek çok az.
*Zorluk:* Orta. Teknik taraf kolay, asıl yük etiketlemede.
*Alptekin'in payı:* Cümleleri rehbere göre tek tek etiketlemek. Bu işi senin yerine kimse yapamaz, çünkü doğru cevabı belirleyen sensin.

**Adım 2: 100 cümleyi model tahminini görmeden yeniden etiketlemek.**
300 cümleyi kontrol ettiğinde modelin cevabını görüyordun. Cevabı görerek kontrol etmek, cevap anahtarına bakarak sınav kâğıdı okumaya benzer: insan farkında olmadan ona yaklaşır. Bu yüzden 100 cümleyi, modelin ne dediğini görmeden baştan etiketleyeceksin. Sonra senin ilk ve ikinci cevabının ne kadar tuttuğuna bakacağız. Tutarlılık düşükse kuralın kendisi muğlak demektir ve rehberi düzeltiriz.
*Zorluk:* Kolay.
*Alptekin'in payı:* Kör etiketleme (yani tahmin gizliyken). Bu adımda kendi kendini taklit etmemek önemli.

**Adım 3: Dört yöntemi sırayla denemek.**
Bunu bir merdiven gibi düşün. Her basamak bir öncekinden daha güçlü ama daha ağır.
- *Birinci basamak, kural tabanlı yöntem:* Elle yazılmış basit bir fiil kuralı. Yapay zekâ değil. Bu bizim çıtamız, yani "en azından bunu geçmeliyiz" çizgisi. Yapıldı bile: 300 cümlede doğruluk %87, macro-F1 0,80 çıktı.
- *İkinci basamak, klasik makine öğrenmesi:* Bilgisayar cümlelerdeki kelimeleri sayar ve hangi kelimelerin hangi etiketle birlikte geldiğini öğrenir (teknik adı TF-IDF ile SVM veya lojistik regresyon). Saniyeler içinde çalışır.
- *Üçüncü basamak, BERTurk:* Milyonlarca Türkçe metni okuyarak dili öğrenmiş hazır bir yapay zekâ. Biz ona kendi işimizi öğreteceğiz. Buna ince ayar deniyor: dilin genelini zaten biliyor, ona sadece "bizim cümlelerde etiket nasıl verilir" gösteriliyor. Alptekin'in RTX 4060 ekran kartı ve 16 GB RAM'i buna yetiyor.
- *Dördüncü basamak, isteğe bağlı: büyük dil modeli:* Hazır bir büyük modele rehberi verip cümleleri doğrudan sormak.

**Neden en güçlü olan her zaman kazanmaz?** Çünkü güçlü yöntemler çok örnekle beslenince parlıyor. Bizim 800 civarı etiketli cümlemiz var, bu küçük bir veri. Çok güçlü bir model az örnekle bazen ezberlemeye kayar ve basit kuralın bile gerisinde kalabilir. Ayrıca bizim işimizin bir kısmı zaten kurala uygun: "açıklar", "bilir" gibi fiillere bakmak çoğu zaman işi çözer. Bu yüzden dördünü de deneyip sonucu karşılaştırmak, tek bir yönteme güvenmekten daha dürüst. Bazen basit olan kazanır ve bu da raporda yazılacak geçerli bir sonuç.
*Zorluk:* Kolaydan zora doğru. Kural ve klasik yöntem kolay, BERTurk daha zor, büyük dil modeli yöntemi isteğe bağlı olduğu için zorunlu değil.
*Alptekin'in payı:* Hangi yöntemin ne sonuç verdiğini anlamak ve raporda kendi cümlelerinle anlatmak. Kodu ben yazarım, ama sonuçları yorumlayan sen olacaksın.

**Adım 4: Başarıyı sınıf başına ölçmek ve karışıklık tablosu çıkarmak.**
Ayrıntısı 2.3'te. Burada önemli olan iki kural var: Aynı cümle hem eğitimde hem testte olmayacak. Ayrıca bir birimi tamamen dışarıda bırakıp modeli hiç görmediği bir alanda da sınayacağız.
*Zorluk:* Orta.
*Alptekin'in payı:* Tabloları okuyup "model nerede yanılıyor, neden" sorusuna kendi gözüyle bakmak.

**Adım 5: En iyi modeli 69 bin cümlenin hepsine uygulayıp program düzeyinde rapor üretmek.**
Bu, projenin gerçek ürünü. Seçtiğimiz en iyi model 69.186 cümlenin hepsini okuyacak. Her program için rapor çıkacak. Elle yapılsa haftalar sürecek iş, bilgisayarda çok kısa sürede biter.
*Zorluk:* Teknik olarak kolay, çünkü araçlar hazır. Ama sonuçları kontrol etmek özen ister.
*Alptekin'in payı:* Raporun doğru göründüğünü örneklerle yoklamak, birkaç programı kendi gözünle açıp kontrol etmek.

### 2.3 Başarıyı nasıl ölçeceğiz

Sadece "yüzde kaç doğru" demek yetmez. Bizim 300 cümlemizin %70'i zaten "düzgün". Hiç düşünmeden her cümleye "düzgün" diyen tembel bir öğrenci de %70 alır, ama aslında bize lazım olan şeyi, belirsiz cümleleri hiç bulamamıştır.

Bu yüzden **macro-F1** kullanacağız. Bunu her sınıfın notunu ayrı ayrı hesaplayıp ortalamasını almak gibi düşün. "Düzgün" sınıfından, "belirsiz" sınıfından ve "çıktı değil" sınıfından ayrı ayrı not çıkar, sonra üçünün ortalaması alınır. Tembel öğrenci "belirsiz" sınıfından sıfır alınca ortalaması çöker, böylece kandırılmamış oluruz. Elimizdeki kural tabanlı yöntemin 0,80'i bu ölçüyle bulundu, 1,00 mükemmel demek.

**Test kümesi** sınavda daha önce görülmemiş sorulara benzer. Modeli çözümlü sorularla eğitiriz, ama notunu görmediği sorularla veririz. Aynı cümle hem eğitimde hem testte olursa model cevabı ezberlemiş olur ve not şişer. Bu riski iki yerde önleyeceğiz: Aynı cümlenin iki tarafta birden bulunmamasına dikkat edeceğiz, çünkü 69 bin cümlenin yalnız 32.348'i birbirinden farklı ve ortak dersler aynı cümleyi tekrar tekrar kullanıyor. Ayrıca bir birimi tamamen kenarda tutacağız. Mühendislik fakültesinde öğrenen model, hiç görmediği bir fakültede de iyi çalışıyorsa gerçekten genelleyebiliyor demektir.

**Karışıklık tablosu** ise bir hata haritası. Satırlarda gerçek etiket, sütunlarda modelin dediği yer alır. Modelin hangi sınıfı hangisiyle karıştırdığını bir bakışta görürüz. Örneğin "analiz" cümlelerine sık sık "uygulama" mı diyor? Bu tablo, sorunun tam olarak nerede olduğunu gösterir.

### 2.4 Riskler ve önlemler

**Az etiket.** Üst Bloom basamaklarından ve "çıktı değil" cümlelerinden çok az örneğimiz var. Az örnekten öğrenmek zor. *Önlem:* Model en emin olmadığı cümleleri seçecek ve etiketleme bu sınıflara yoğunlaşacak. Yine de bazı sınıflarda sonuç zayıf kalabilir, bunu da raporda açıkça yazacağız.

**Tek etiketleyici.** Şimdilik doğru cevabı yalnız Alptekin belirliyor. Başka biri bakınca farklı karar verebilir. Ayrıca 300 cümleyi modelin cevabını görerek kontrol ettin, bu yüzden "model seninle aynı çıktı" sonucu olduğundan iyimser olabilir. *Önlem:* 100 cümleyi kör olarak yeniden etiketleyeceksin ve kendi tutarlılığını ölçeceğiz. Başka bir kişinin de bakması mümkün olursa daha güçlü olur, ama bu planlarda henüz yok.

**Bloom'un tartışmalı olması.** Bloom basamakları kesin sınırlarla ayrılmış değil. "Karşılaştırır" analiz mi, anlama mı? İki uzman farklı diyebilir. Bu yüzden rehberde altı tartışmalı kararı sen verdin, ör. "karşılaştırır = analiz". *Önlem:* Kararlar yazılı rehberde duruyor ve raporda "bizim kuralımız bu" diye açıkça söylüyoruz. Model Bloom'un tek doğrusunu değil, rehberimizin kuralını öğreniyor.

**Tek üniversite.** Veri yalnız Karabük Üniversitesi'nden. Başka üniversitenin yazım alışkanlıkları farklı olabilir. *Önlem:* Bir birimi tamamen dışarıda bırakıp sınamak bunu kısmen gösterir. Sonuçları "Karabük için" diye sunacağız, "bütün Türkiye için" demeyeceğiz.

## 3. Sonunda elimizde ne olacak?

### 3.1 Kesin olanlar

Aşağıdakiler, plan tutarsa elimizde bulunacak şeylerin listesi. Her biri kime neye yarıyor:

- **Karabük Üniversitesi'nin bütün derslerini kapsayan Türkçe öğrenme çıktısı veri seti (69.186 cümle).** Bu, bütün üniversitenin ders sayfalarından toplanmış cümlelerin düzenli hâli. Kalite birimi, hangi derslerde ne yazıldığını tek yerde görebilir. Başka bir araştırmacı da bu veriyle kendi çalışmasını yapabilir.
- **Yazılı etiket rehberi ve Alptekin'in kontrol ettiği etiketli örnek.** Rehber, "düzgün cümle nedir, Bloom basamağı nasıl belirlenir" sorularının yazılı cevabı. Ders hocaları kendi cümlesini bu rehbere göre yazabilir. Etiketli örnek ise modelin ders kitabı gibi.
- **Eğitilmiş bir sınıflandırıcı ve dört yöntemin karşılaştırması.** Sınıflandırıcı, bir cümleyi alıp "düzgün mü, belirsiz mi, Bloom basamağı ne" diye cevap veren model. Kalite birimi bunu yeni gelen cümleleri hızlıca taramak için kullanabilir. Karşılaştırma ise "bu iş için ağır modele gerek var mı, yoksa basit yöntem yetiyor mu" sorusunun cevabı.
- **Program düzeyinde rapor.** Her program için şunlar olacak: boş ders sayfaları, belirsiz ve "çıktı değil" cümle oranı, Bloom dağılımı, ders içindeki tekrarlar ve "düzeltilecek dersler" listesi. Her dersin sayfa linki de yanında olacak. Bölüm başkanı kendi programına bakıp "şu on dersi düzeltelim" diyebilir. Ders hocası da kendi dersine tek tıkla ulaşır.
- **Final raporu.** Bütün bunların hikâyesi: ne yaptık, ne bulduk, nerede yanıldık.

### 3.2 Bir uygulamamız olacak mı?

**Karar verildi (10 Kasım 2026): Alptekin B seçeneğini seçti.** Finalde model ve program raporunun yanında küçük bir web sayfası da olacak. Seçenekler şunlardı:

| Seçenek | Ne var | Ne kadar iş | Finalde etkisi |
|---|---|---|---|
| **A** | Yalnız model ve program raporu (PDF/Excel) | En az iş | Sonuçlar tabloda görünür, ama "çalıştığını göstermek" için elle açıklama gerekir |
| **B** | A'ya ek olarak küçük bir web sayfası | Orta | Canlı gösterilebilir, "çalıştığını göstermek" için en etkili seçenek |
| **C** | B'nin büyüğü: başka üniversitelerin bilgi paketlerini de tarayan araç | En çok iş | Vize raporunda kapsam dışı denmişti, bu yüzden planla çelişir |

Claude da B'yi önermişti; karar Alptekin'in.

B seçilirse ekranı şöyle düşünebilirsin. Bu yalnız bir canlandırma; gerçek tasarım henüz yapılmadı. Sayfanın üstünde büyük bir yazı kutusu var ve "Öğrenme çıktısı cümlenizi buraya yapıştırın" yazıyor. Kutuya "Öğrenci, veri tabanı kavramını öğrenir." yazıp düğmeye basıyorsun. Birkaç saniye içinde altta bir sonuç kutusu açılıyor. Kutu kırmızıya boyanmış, çünkü cümle "belirsiz". Yanında kısa bir açıklama var: "Burada 'öğrenir' fiili ölçülemez." Hemen altında bir öneri yazıyor: "Şöyle yazabilirsin: 'Veri tabanı tablolarını tasarlar.'" Aynı cümleyi yeni hâliyle yapıştırınca kutu yeşile dönüyor ve yanında Bloom basamağı çıkıyor: "tasarlar" fiili olduğu için "yaratma". Sayfanın başka bir köşesinde bir program seçme listesi var. Bir program seçince o programın raporu açılıyor: belirsiz cümle oranı, Bloom dağılımı ve düzeltilecek derslerin listesi, her biri ders sayfasına giden bir link olarak. Bu sayfa Alptekin'in bilgisayarında çalışır, istenirse internete de konabilir.

Sunumda bu ekranı canlı kullanmak, hocaya "çalışıyor" demekten çok daha ikna edici olur. B ek iş demek; bu yüzden final planına bir adım olarak eklendi.

### 3.3 Kapanış

Proje bittiğinde Alptekin'in elinde şunlar birikmiş olacak: Karabük'ün bütün derslerinden toplanmış ve temizlenmiş gerçek bir veri seti, kendi elinle etiketlenmiş ve kendi tutarlılığı ölçülmüş bir örnek, dört yöntemi aynı sınavda yarıştırıp sonucunu açıklayan bir model karşılaştırması, her program için hazır bir kalite raporu ve bütün bunları anlatan bir final raporu. Bir de bunları canlı gösteren küçük bir web sayfası. Bunların hepsinin altında ise asıl kalıcı kazanç duruyor: veriyi toplamayı, bir kural rehberi yazmayı, bir yapay zekâ modelini eğitip dürüstçe sınamayı ve sonucu başkasına anlatmayı bir kez baştan sona yaşamış olmak.
