# Ders çıktısı kalite kontrolü

Üniversite bilgi paketlerindeki ders öğrenme çıktısı cümlelerinin hepsi iyi yazılmış değil: bir kısmı belirsiz, bir kısmı ise hiç öğrenme çıktısı değil (konu başlığı gibi). Bu projede Karabük Üniversitesi bilgi paketindeki Türkçe ders çıktısı cümleleri yapay zekâ ile kontrol edildi. Her cümle üç sınıftan birine ayrıldı: düzgün, belirsiz, çıktı değil. Düzgün cümleler ayrıca Bloom basamağına (hatırlama, anlama, uygulama, analiz, değerlendirme, yaratma, bilişsel değil) yerleştirildi.

Çalışma, Yapay Zekâ dersinin vize ve final projesidir. Sahibi: Alptekin Zengin. Vize aşamasında veri toplandı, ön analiz yapıldı ve etiket rehberi yazıldı. Final aşamasında kural tabanlı yöntem, TF-IDF modelleri, BERTurk ve iki büyük dil modeli aynı test cümleleri üzerinde karşılaştırıldı; en uygun model tüm veriye uygulandı ve bir web sayfası hazırlandı.

## Öne çıkan sonuçlar

### Tüm üniversite

Veri dosyasında 69.186 cümle satırı var (13.679 ders, 29 birim, 168 program; 1.210 dersin çıktı bölümü boş). Bunların 214'ü İngilizce olduğu için sınıflandırılmadı; 68.972 cümle etiketlendi. Etiketleme final modelleriyle yapıldı (`final/tum_etiketler.csv`).

| Sınıf | Cümle | Oran |
|---|---|---|
| Düzgün | 46.076 | %66,8 |
| Belirsiz | 20.816 | %30,18 |
| Çıktı değil | 2.080 | %3,02 |

Düzgün cümlelerin Bloom dağılımı (düzgün cümlelere oranla): hatırlama %13,5, anlama %28,42, uygulama %31,09, analiz %12,05, değerlendirme %6,11, yaratma %6,97, bilişsel değil %1,86. Üst basamaklar (analiz, değerlendirme, yaratma) toplamı %25,13.

| Seviye | Ders | Cümle | Düzgün | Sorunlu (belirsiz + çıktı değil) | Üst basamak |
|---|---|---|---|---|---|
| Lisans | 10.700 | 54.310 | %67,77 | %32,23 | %26,97 |
| Ön lisans | 2.979 | 14.662 | %63,22 | %36,78 | %17,84 |

Kaynak: `final/rapor/universite.json`.

### Yöntemlerin karşılaştırması

| Yöntem | Kalite doğruluk | Kalite macro-F1 | Bloom doğruluk | Bloom macro-F1 |
|---|---|---|---|---|
| Kural tabanlı | 0,910 | 0,881 | - | - |
| TF-IDF + SVM | 0,870 | 0,810 | 0,683 | 0,543 |
| TF-IDF + lojistik regresyon | 0,870 | 0,800 | 0,698 | 0,569 |
| BERTurk (ince ayar) | 0,963 | 0,956 | 0,721 | 0,622 |
| GPT-6.1 Sol | 0,980 | 0,984 | 0,871 | 0,846 |
| Claude Haiku | 0,970 | 0,975 | 0,903 | 0,878 |

Not: Test kümesi 100 rastgele cümledir. Bloom ölçümleri yöntemler arasında birebir aynı cümle kümesinde değildir: BERTurk ve TF-IDF için 63 cümle, büyük modeller için 62 cümle. BERTurk satırı birden fazla rastgele tohumun ortalamasıdır (kalite 3 tohum, Bloom 5 tohum; Bloom için en iyi doğrulama epoch'u seçilmiştir). Kural tabanlı yöntem yalnız kaliteyi ölçer. Büyük modellerin değerleri `final/Veri-Analizi.ipynb` 12. bölümde hesaplanır. Ayrıntılar: `final/sonuc_02.json`, `sonuc_03.json`, `sonuc_04.json` ve `final/llm/`.

## Klasör haritası

```
veri/                 Ham veri
kalite-rapor/         Vize aşaması
final/                Final aşaması
```

### veri/

- `karabuk_ders_ciktilari.csv`: Karabük Üniversitesi ders çıktısı cümleleri (üniversite, seviye, birim, program, ders kodu ve adı, yarıyıl, çıktı sırası, cümle, ders kimliği).

### kalite-rapor/ (vize aşaması)

- `analiz.py`: ön analiz; tam veri ve 300 etiketli örnek üzerinde grafikleri ve sayıları üretir (`analiz/`).
- `doluluk.py`: indirilmiş ders sayfalarında hangi bölümlerin boş olduğunu çıkarır (`analiz/doluluk*.csv`). Siteye istek atmaz, yerel kopyaları okur. Toplama programının kendisi bu depoda yok.
- `etiket/`: 300 cümlelik etiketleme çalışması: `Kural-Rehberi.md` (etiket rehberi), `Kontrol-Tablosu.xlsx`, örnek ve tahmin dosyaları, `etiket_kesin.csv` (onaylanmış etiketler).
- `rapor.md`, `rapor_dolu.md`, `rapor_uret.py`: vize raporunun metni ve onu Word/PDF'e çeviren betik. Çıktılar: `Vize-Raporu.docx`, `.html`, `.pdf`.
- `literatur-dogrulanmis.md`: kaynakça notları.
- `anlatim/`, `Proje-Anlatimi.*`: projenin sade dille anlatımı.
- `geri_sayim.ps1`: veri toplama sırasında kullanılan yardımcı betik (bu bilgisayara özgü yolları var).

### final/ (final aşaması)

Numaralı betikler sırayla çalışacak şekilde yazılmıştır:

- `01_ilk_model.py`: 300 etiketli cümleyle ilk deneme; kural tabanlı yöntem ile TF-IDF + doğrusal modeller karşılaştırılır (`sonuc_01.json`).
- `02_cumle_sec.py`: etiketlenecek 500 yeni cümleyi 4 gruptan seçer (tohum 42).
- `03_kontrol_tablosu.py`: seçilen cümleler ve model tahminleriyle Excel kontrol tablosu üretir (`etiket2/Kontrol-Tablosu-2.xlsx`).
- `04_isim_obegi_karari.py`: "-ilmesi/-ması" ile biten isim öbeklerinin "çıktı değil" sayılması kararını tahmin dosyasına ve tabloya uygular.
- `05_etiket_birlestir.py`: ilk 300 ve yeni 500 etiketi (İngilizce hariç) tek dosyada (`etiket2/etiket_kesin_800.csv`) birleştirir.
- `06_model_800.py`: 795 etiketli cümleyle kalite ve Bloom için TF-IDF modelleri (`sonuc_02.json`).
- `07_berturk.py`: BERTurk (dbmdz/bert-base-turkish-cased) ince ayarı, kalite sınıflandırması (`sonuc_03.json`).
- `08_berturk_bloom.py`: BERTurk Bloom sınıflandırması, ekran kartı ve erken durdurmayla, 5 tohum (`sonuc_04.json`).
- `09_tumunu_etiketle.py`: tüm etiketli veriyle son modelleri eğitir ve bütün ders çıktısı cümlelerini etiketler (`tum_etiketler.csv`, `tum_etiketler_ozet.json`). Eğitilen modelleri proje dışına kaydeder.
- `10_program_raporu.py`: birim, program ve ders düzeyinde rapor tabloları, şekiller ve web sayfası verisi (`rapor/`).
- `11_llm_karsilastir.py`: GPT-6.1 Sol ve Claude Haiku'nun 100 cümlelik tahminlerini puanlar (`sonuc_05.json`).
- `12_notebook_uret.py`: `Veri-Analizi.ipynb` dosyasını üretir.

Diğer klasör ve dosyalar:

- `Veri-Analizi.ipynb` (ve `.pdf`): bütün analizlerin derlemesi; altı yöntemin karşılaştırması 12. bölümdedir.
- `etiket2/`: ikinci etiketleme turunun (500 cümle) girdi, tahmin ve onaylanmış etiket dosyaları.
- `llm/`: büyük dil modellerinin karşılaştırması: `test_100.csv` (test cümleleri), `gpt_tahmin.csv`, `haiku_tahmin.csv`, `haiku2_tahmin.csv`.
- `rapor/`: birim, program ve ders düzeyinde çıktı tabloları (`birim.csv`, `program.csv`, `ders.csv`, `bos_dersler.csv`, `duzeltilecek_dersler.csv`), özet json dosyaları ve şekiller.
- `site/`: yerel web sayfası. `sunucu.py` (Flask sunucusu), `oneri.py` (kural tabanlı vurgu ve not), `sina_api.py` (çalışan sunucuyu deneyen yardımcı betik), `baslat.bat` (Windows başlatıcı), `static/` (sayfa), `gorev/` (sayfa ve sunucu için yazılan görev tanımları).
- `tasarim/`: web sayfasının tasarım taslağı ve ekran görüntüleri.

### web/ (çevrimiçi sürüm: https://ciktianaliz.com)

Sitenin sunucusuz sürümü; Cloudflare'de yalnız durağan dosya olarak yayınlanır.

- `public/`: sayfa. `kontrol.js` kural tabanlı kalite kontrolünü ve `oneri.py`'deki vurgu/not üretimini JavaScript'e taşır; kontrol ziyaretçinin tarayıcısında yapılır, cümleler sunucuya gönderilmez. `veri.json`, `final/rapor/site_veri.json` dosyasının kopyasıdır (bölüm raporu, BERTurk tahminleri).
- Çevrimiçi sürümde BERTurk modeli yoktur: cümle kalitesi kural tabanlı bulunur (sınamada 100 cümlede 91 doğru), Bloom basamağı ve güven gösterilmez.
- `test/`: JavaScript ile Python kuralının aynı sonucu verdiğini sınar. `python test/uret_beklenen.py` ardından `node test/kontrol.test.mjs` (`web/` içinde). Sonuç 1509/1510; tek fark emoji içeren cümlede karakter konumunun UTF-16 ile sayılmasıdır, vurgulanan metin aynıdır.
- `kaynak/`: testin kullandığı Python kuralı, `oneri.py` ve 1.500 örnek cümle.
- Yayın: `npx wrangler deploy` (`web/` içinde, `wrangler.jsonc`).

## Kurulum ve çalıştırma

Python 3.12 ile bir sanal ortam kurun ve bağımlılıkları yükleyin (CUDA'lı torch için `requirements.txt` başındaki nota bakın):

```
py -3.12 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Betikler, depo kökünden `py -3 final/<betik>.py` biçiminde çalıştırılacak şekilde yazılmıştır; kendi konumlarına göre göreli yol kullanırlar.

**Veri analizi defteri:** `final/Veri-Analizi.ipynb` dosyasını Jupyter veya VS Code ile açın (`ipykernel` kuruludur). Defterin sonuçları kayıtlıdır, çalıştırmadan da okunabilir. Yeniden üretmek için `python final/12_notebook_uret.py` ve ardından `python -m jupyter nbconvert --to notebook --execute --inplace final/Veri-Analizi.ipynb` komutları kullanılır (nbconvert ve nbclient kuruludur; `jupyter` komutu için gerekirse `jupyterlab` ya da `notebook` paketini de ekleyin).

**Modelleri yeniden eğitme:** Eğitilmiş modeller 846 MB olduğu için depoda yoktur. `final/09_tumunu_etiketle.py` etiketli veriyle (`final/etiket2/etiket_kesin_800.csv`) iki modeli (kalite ve Bloom) eğitir ve bütün cümleleri etiketler. NVIDIA GPU (CUDA) gerekir; GPU ile yaklaşık 2 dakika sürer (kayıtlı süre: eğitim 69,7 sn, tahmin 53,9 sn). İlk çalıştırmada BERTurk ağırlıkları internetten indirilir. Betik modelleri kendi sabit yoluna yazar; aşağıdaki "Bilinen sınırlar" bölümüne bakın.

**Web sayfası:** Önce modeller üretilmiş olmalıdır. Windows'ta `final/site/baslat.bat` dosyasını çalıştırın ya da sanal ortamdan `python final/site/sunucu.py` komutunu verin. Sayfa yalnız yerel makinede açılır: http://127.0.0.1:8765

## Bilinen sınırlar ve dikkat edilecekler

- **Sabit Windows yolları.** Aşağıdaki dosyalarda sanal ortam ve model klasörü için bu bilgisayara özgü yollar yazılıdır; başka bir bilgisayarda çalıştırmadan önce elle düzeltilmelidir (kod bu depoda değiştirilmedi):
  - `final/09_tumunu_etiketle.py` (satır 18): model klasörü
  - `final/site/sunucu.py` (satır 18): model klasörü
  - `final/site/baslat.bat` (satır 14): sanal ortamdaki python.exe
  - `final/tum_etiketler_ozet.json` (satır 93): eğitimde kullanılan model klasörünün kaydı (yalnız bilgi)
  - `final/site/gorev/gorev-arka.md`, `gorev-on.md`: görev tanımlarında proje, sanal ortam ve model yolları (yalnız metin)
  - `kalite-rapor/geri_sayim.ps1`: veri toplama sırasındaki geçici klasör yolları
- **Etiketler.** Etiketler yapay zekâ önerisi görülerek onaylandı; bağımsız bir ikinci etiketleme yoktur.
- **Cevap anahtarı.** Cevap anahtarı bir Claude modelinden (Sonnet) geldi. Claude Haiku aynı aileden olduğu için onun yüksek skoru bu yakınlıktan şişmiş olabilir.
- **Tek üniversite.** Veri yalnız Karabük Üniversitesi'ne aittir; sonuçlar başka üniversitelere genellenemez.
- **Küçük test kümesi.** Test kümesi yalnız 100 cümledir (Bloom için 62-63). Fark küçükse yorum yapmak güvenli değildir. Bloom'da en iyi küçük model (BERTurk) 100 cümlede yaklaşık 72 doğru biliyor; üst basamaklar ve az örnekli sınıflar (ör. bilişsel değil, yaratma) en çok karıştırılanlardır.
- **Kişisel veri.** `final/rapor/bos_dersler.csv` ve `kalite-rapor/analiz/doluluk.csv` dosyalarındaki `ogretim_elemani` sütununda bu depoda ad ve e-posta yerine yalnız `var` işareti bulunur (boş hücre: öğretim elemanı girilmemiş). Analizler yalnız bu bilginin dolu ya da boş olmasını kullanır. `kalite-rapor/analiz/doluluk_program.csv` yalnız sayısal özet içerir.
- **Haiku sonuçları.** `final/sonuc_05.json` Haiku'nun ilk çalıştırmasını (`llm/haiku_tahmin.csv`) puanlar; yukarıdaki tablo ve defterin 12. bölümü `llm/haiku2_tahmin.csv` dosyasını kullanır. İlk çalıştırma cevap anahtarının da bulunduğu klasörde yapıldığı ve modelin anahtara bakmadığı doğrulanamadığı için, ölçüm yalnız test cümleleri ile kural rehberinin bulunduğu ayrı bir klasörde tekrarlandı; geçerli sayılan sonuç bu ikinci çalıştırmadır (Bloom doğruluk 0,903; ilk çalıştırmada 0,968).

## Veri kaynağı

Veri, Karabük Üniversitesi Bilgi Paketi'nin (herkese açık Bologna sayfaları) ders sayfalarından Kasım 2026'da toplandı. İstekler arasında 2-3 saniye beklendi. Verinin hakları üniversiteye aittir; burada yalnız ders projesi amacıyla bulunur.

## Yapay zekâ kullanımı

Kod ve metinlerin hazırlanmasında yapay zekâ araçları kullanıldı: Anthropic Claude; karşılaştırmada ayrıca OpenAI GPT. Kararlar ve etiket onayı proje sahibine aittir.
