# Literatür taraması (doğrulanmış) — Türkçe ders öğrenme çıktılarının YZ ile kalite kontrolü

Tarih: 2026-11-09. Her kaynak WebFetch/WebSearch ile açıldı; bibliyografik alanlar açılan sayfadan (yayıncı, arXiv, Crossref, OpenAlex, DergiPark PDF, kurumsal depo) alındı. "Özetten" = sayı yalnız abstract/özet sayfasında görüldü, tam metin okunmadı.

---

## 1. Doğrulanmış kaynaklar

### Başlık 1 — Bloom basamağına göre metin sınıflama

> Not: **Soru sınıflama** (sınav/ödev maddesi; çoğu 600 soruluk Yahya et al. veri seti ve türevleri) ile **öğrenme çıktısı (CLO/LO) sınıflama** farklı görevlerdir. Çıktı cümleleri daha kısa ve kalıplıdır (fiil + konu), fiil sinyali güçlüdür; soru cümlelerinde fiil çoğu zaman örtüktür. Aşağıda her kaynakta türü belirtildi.

**1.1 Waheed et al. (2021) — BloomNet**
- APA: Waheed, A., Goyal, M., Mittal, N., Gupta, D., Khanna, A., & Sharma, M. (2021). *BloomNet: A robust transformer based model for Bloom's learning outcome classification* (arXiv:2108.07249). arXiv. https://doi.org/10.48550/arXiv.2108.07249
- Veri: İngilizce; başlık "learning outcome" dese de deney verisi **açık uçlu sorular**: Dataset 1 (IID) 600 soru (her basamak 100), Dataset 2 (OOD) 141 soru (ar5iv tam metin).
- Yöntem: RoBERTa semantik + POS/NER dilbilimsel öznitelikler + kelime dikkati; VDCNN, LSTM, CNN, RCNN, HAN, Random Forest (TF-IDF), DistilRoBERTa, RoBERTa ile karşılaştırma.
- Sonuç (tam metin tablo): doğruluk BloomNet %87,50 (IID) / %70,40 (OOD); RoBERTa %82,00 / %68,65; RF(TF-IDF) %70,66 / %62,12; LSTM %58,50 / %47,09; CNN %60,67 / %49,79.
- Fark: Hakemsiz preprint; İngilizce soru verisi; "kötü yazılmış çıktı" sınıfı yok, her girdinin bir basamağa ait olduğunu varsayar. OOD düşüşü (~17 puan) alan kaymasına duyarlılığı gösterir — Türkçe/farklı fakülteler için önemli uyarı.

**1.2 Li et al. (2022) — BERT ile öğrenme hedefi sınıflama**
- APA: Li, Y., Raković, M., Poh, B. X., Gašević, D., & Chen, G. (2022). Automatic classification of learning objectives based on Bloom's taxonomy. In *Proceedings of the 15th International Conference on Educational Data Mining (EDM 2022)* (kısa bildiri). https://doi.org/10.5281/zenodo.6853191
  (Venue sayfada açıkça yazmıyor; EDM 2022 proceedings URL'sinden: https://educationaldatamining.org/EDM2022/proceedings/2022.EDM-short-papers.55/index.html)
- Veri: İngilizce, **öğrenme çıktısı**; Avustralya'da bir üniversiteden 5.558 dersin 21.380 öğrenme hedefi, çok etiketli (2.325'i iki etiketli). Kodlayıcı uyumu κ=0,63 → uzlaşı sonrası 0,80.
- Yöntem: NB, LR, SVM, RF, XGBoost (3.094 el yapımı öznitelik: n-gram, TF-IDF, okunabilirlik, LIWC) ve ince ayarlı BERT; basamak başına ikili sınıflandırıcılar + çok etiketli model.
- Sonuç: BERT ikili sınıflandırıcılar doğruluk 0,96–0,99, κ 0,87–0,93, F1 0,88–0,95 (ör. Understand doğruluk 0,971, F1 0,947; Create F1 0,888).
- Fark: Bizim konuya en yakın büyük çıktı veri seti; ancak İngilizce, kalite (belirsiz fiil/konu başlığı) etiketi yok — tüm hedefler sınıflanabilir varsayılmış.

**1.3 Shaikh, Daudpotta & Imran (2021) — LSTM**
- APA: Shaikh, S., Daudpotta, S. M., & Imran, A. S. (2021). Bloom's learning outcomes' automatic classification using LSTM and pretrained word embeddings. *IEEE Access, 9*, 117887–117909. https://doi.org/10.1109/ACCESS.2021.3106443
- Veri: İngilizce; hem **CLO** hem **sınav maddesi** (boyut özette yok).
- Yöntem: Önceden eğitilmiş kelime gömmeli LSTM; anahtar kelime tabanlı yöntem taban çizgisi.
- Sonuç (özetten, OpenAlex): anahtar kelime yaklaşımı ~%55; LSTM CLO'da ~%87, soru maddelerinde ~%74 doğruluk.
- Fark: Çıktı ile soruyu ayrı raporlaması değerli (çıktılar daha kolay). Kalite tespiti yok; fiil listesi yaklaşımının çakışan fiiller yüzünden yetersiz kaldığını gösteriyor — bizim "belirsiz fiil" kuralını model tabanlı yapma gerekçesi.

**1.4 Mohammed & Omar (2020) — değiştirilmiş TF-IDF + word2vec**
- APA: Mohammed, M., & Omar, N. (2020). Question classification based on Bloom's taxonomy cognitive domain using modified TF-IDF and word2vec. *PLoS ONE, 15*(3), e0230442. https://doi.org/10.1371/journal.pone.0230442
- Veri: İngilizce **soru**; 141 soruluk toplanmış set + Yahya et al. (2012) 600 soruluk set.
- Yöntem: TFPOS-IDF (POS ağırlıklı TF-IDF) + word2vec; SVM, LR, KNN.
- Sonuç (tam metin, PMC): ağırlıklı F1 SVM %83,7 (141 soru), %89,7 (600 soru).
- Fark: Klasik yöntemlerin güçlü taban çizgisi; soru odaklı, kalite tespiti yok.

**1.5 Gani et al. (2023) — CNN + gömme seçimi**
- APA: Gani, M. O., Ayyasamy, R. K., Sangodiah, A., & Fui, Y. T. (2023). Bloom's taxonomy-based exam question classification: The outcome of CNN and optimal pre-trained word embedding technique. *Education and Information Technologies, 28*(12), 15893–15914. https://doi.org/10.1007/s10639-023-11842-1
- Veri: İngilizce **sınav sorusu** (ayrıntı açılamadı; yalnız Crossref metadatası doğrulandı).
- Yöntem: CNN + farklı önceden eğitilmiş gömmeler (arama özetinde: soru sınıflamada özellik çıkarımının sıralı örüntüden önemli olduğu gerekçesi).
- Sonuç: Sayı doğrulanamadı (yayıncı sayfası 403).
- Fark: Soru odaklı CNN örneği; çıktı metni ve kalite boyutu yok.

**1.6 Kumar, Gulwani & Singh (2025) — klasik vs RNN vs BERT vs LLM**
- APA: Kumar, R., Gulwani, D., & Singh, S. (2025). *Automated analysis of learning outcomes and exam questions based on Bloom's taxonomy* (arXiv:2511.10903). arXiv. https://arxiv.org/abs/2511.10903
- Veri: 600 cümle (çıktı + soru karışık, oran belirtilmemiş), orijinal Bloom 6 sınıf (Knowledge…Evaluation); dil belirtilmemiş (İngilizce olduğu anlaşılıyor).
- Yöntem: NB, LR, SVM; LSTM/BiLSTM/GRU/BiGRU; BERT, RoBERTa; sıfır-atış LLM (OpenAI, Gemini, Ollama, Anthropic); eş anlamlı değiştirme ile veri artırma.
- Sonuç (özetten): veri artırmalı SVM %94 doğruluk/recall/F1; BERT ve RNN'lerde ciddi aşırı öğrenme; en iyi LLM'ler (OpenAI, Gemini) ~0,72–0,73 doğruluk.
- Fark: Küçük veri kümesinde klasik yöntemin BERT'i geçebildiğini gösteriyor — Türkçe küçük etiketli veri için önemli tasarım bulgusu. Orijinal (revize değil) taksonomi; kalite sınıfı yok.

**1.7 Almatrafi & Johri (2025) — GPT-4 istem stratejileri vs BERT**
- APA: Almatrafi, O., & Johri, A. (2025). Leveraging generative AI for course learning outcome categorization using Bloom's taxonomy. *Computers and Education: Artificial Intelligence, 8*, 100404. https://doi.org/10.1016/j.caeai.2025.100404
- Veri: İngilizce, uzman etiketli 1.000 **ders öğrenme çıktısı**, revize Bloom.
- Yöntem: GPT-4; zero-shot, few-shot, chain-of-thought, retorik durum, çoklu ikili soru istemleri; en iyi istem ince ayarlı BERT ile karşılaştırıldı.
- Sonuç (özetten, NSF PAR): en iyi istem "retorik bağlam + alan bilgisi"; çoklu ikili soru zero-shot'tan kötü; ince ayarlı BERT daha iyi; LLM–uzman uyumu "orta–önemli" (sayısal κ sayfada yok).
- Fark: Revize Bloom + çıktı + LLM açısından en yakın çalışma; İngilizce, kalite (yazım) denetimi yok.

**1.8 Sridhar et al. (2023) — GPT-4 ile öğrenme hedefi yazımı**
- APA: Sridhar, P., Doyle, A., Agarwal, A., Bogart, C., Savelka, J., & Sakr, M. (2023). *Harnessing LLMs in curricular design: Using GPT-4 to support authoring of learning objectives* (arXiv:2306.17459). arXiv. https://doi.org/10.48550/arXiv.2306.17459
- Veri: GPT-4'ün bir YZ dersi için ürettiği 127 öğrenme hedefi (İngilizce). Arama özetine göre değerlendirmede 21.380 hedefle eğitilmiş BERT sınıflandırıcı (Li et al., 2022) ve insan anotasyonu kullanıldı.
- Yöntem: Ayrıntılı yönergeli istem; çıktıların Bloom eylem fiiliyle başlayıp başlamadığı ve hedef düzeye uyumu incelendi.
- Sonuç (özetten): nitel — hedefler "makul ve iyi biçimli", beklenen Bloom düzeyine genel olarak uygun; sayısal metrik özette yok.
- Fark: Üretim odaklı (yazma), denetim değil; ama "iyi biçimli çıktı" ölçütlerini LLM'e uygulatmanın ilk örneklerinden.

**1.9 Huber & Niklaus (2025) — LLM'ler ve Bloom**
- APA: Huber, T., & Niklaus, C. (2025). LLMs meet Bloom's taxonomy: A cognitive view on large language model evaluations. In *Proceedings of the 31st International Conference on Computational Linguistics (COLING 2025)* (pp. 5211–5246). Association for Computational Linguistics. https://aclanthology.org/2025.coling-main.350/
- Veri/Yöntem: Yaygın LLM benchmark'larının Bloom basamaklarını kapsama analizi (sınıflama görevi değil).
- Sonuç (özetten): LLM'ler alt basamaklarda daha iyi; benchmark'larda üst basamak kapsama boşlukları.
- Fark: Arka plan kaynağı — LLM'in "değerlendirme/yaratma" ayrımında zorlanabileceğine dair gerekçe.

**1.10 Botas, Peixoto & Ribeiro (2026) — çok dilli BERT, çoktan seçmeli sorular**
- APA: Botas, J. F., Peixoto, A. R., & Ribeiro, E. (2026). BERT-based classification of cross-linguistic MCQs according to the Bloom taxonomy. In *15th Symposium on Languages, Applications and Technologies (SLATE 2026)* (OASIcs Vol. 144, pp. 4:1–4:17). Schloss Dagstuhl. https://doi.org/10.4230/OASIcs.SLATE.2026.4
- Veri: İngilizce ve Portekizce (+çeviri) **çoktan seçmeli soru**, 4 düzey.
- Yöntem: BERT ve ModernBERT, 40 ayar, anahtar kelime taban çizgisi.
- Sonuç (özetten): sayı yok; BERT > anahtar kelime; çeviri veri biraz daha kötü; Hatırlama en kolay, Uygulama en zor.
- Fark: İngilizce dışı dile aktarım örneği (Türkçeye benzer düşük kaynaklı senaryo için emsal); soru odaklı.

### Başlık 2 — Ders çıktısı ↔ program çıktısı otomatik eşleştirme (ABET vb.)

**2.1 Zaki et al. (2023)**
- APA: Zaki, N., Turaev, S., Shuaib, K., Krishnan, A., & Mohamed, E. (2023). Automating the mapping of course learning outcomes to program learning outcomes using natural language processing for accurate educational program evaluation. *Education and Information Technologies, 28*(12), 16723–16742. https://doi.org/10.1007/s10639-023-11877-4
- Veri: İngilizce, iki gerçek programın CLO–PLO verisi (GitHub: nzaki02/CLO-PLO, arama özetinden).
- Yöntem: NLP tabanlı otomatik eşleştirme + web aracı.
- Sonuç (özetten, UAEU kayıt): uzman eşleştirmesine göre kesinlik %83,1 ve %88,1.
- Fark: Eşleştirme yapar ama çıktının kendisinin iyi yazılıp yazılmadığını denetlemez; kötü yazılmış CLO eşleştirmeyi de bozar — bizim çalışma ön-adım olarak konumlanabilir.

**2.2 Asiri (2022) — ABET öz-değerlendirme raporlarından kısa metin madenciliği**
- APA: Asiri, Y. (2022). Short text mining for classifying educational objectives and outcomes. *Computer Systems Science and Engineering, 41*(1). https://doi.org/10.32604/csse.2022.020100
- Veri: EAC-ABET akrediteli programların 152 öz-değerlendirme raporu (SSR); PEO, SO, PES setleri.
- Yöntem: Apriori birliktelik kuralları ile "delegasyonla sınıflandırma" (CBAD), PEO→SO eşleme.
- Sonuç (tam metin): genel doğruluk verilmemiş; sınıf bazında en yüksek %55,33.
- Fark: Akreditasyon belgeleri üzerinde nadir çalışma; kısa metnin anlamsal yetersizliğini vurgular; düşük başarı, kural tabanlı yaklaşımın sınırını gösterir.

**2.3 Shiferaw et al. (2024) — BERT ile ders artikülasyon matrisi**
- APA: Shiferaw, N. A., Leandre, S. H., Sinha, A., & Rout, D. (2024). *BERT-based approach for automating course articulation matrix construction with explainable AI* (arXiv:2411.14254). arXiv. https://arxiv.org/abs/2411.14254
- Veri: CO–PO/PSO çiftleri, 0–3 hizalama düzeyi (boyut özette yok).
- Yöntem: DT, RF, XGBoost; BERT, DistilBERT, ALBERT, RoBERTa transfer öğrenme; LIME.
- Sonuç (özetten): doğruluk %98,66, F1 %98,66.
- Fark: Aşırı yüksek skor ve veri ayrıntısı eksikliği temkin gerektirir; Türkçe/MÜDEK yok; çıktı kalitesi yok.

### Başlık 3 — Müfredat/akreditasyon belgelerinde metin analizi, ölçülebilirlik denetimi

**3.1 Meda & Swart (2017)**
- APA: Meda, L., & Swart, A. J. (2017). Analysing learning outcomes in an electrical engineering curriculum using illustrative verbs derived from Bloom's taxonomy. *European Journal of Engineering Education*. http://hdl.handle.net/11462/1495
- Veri: Güney Afrika, 33 ders kılavuzunun öğrenme çıktıları (İngilizce).
- Yöntem: Nitel vaka çalışması, Bloom'dan türetilen fiil listesine göre manuel inceleme.
- Sonuç (depo özeti): çıktıların %9'u belirsiz, %10'u gözlenemez, %23'ü ölçülemez.
- Fark: Bizim "kalite" sınıflarının (belirsiz/ölçülemez) yaygınlığına dair kanıt; ama tamamen manuel.

**3.2 Butt, Anwar & Kardgar (2025) — GPT ile SMART denetimi**
- APA: Butt, A. A., Anwar, S., & Kardgar, A. (2025). *Work-in-progress: Evaluating course learning objectives with generative AI using SMART criteria* [Poster]. 2025 ASEE Annual Conference & Exposition. https://nemo.asee.org/public/conferences/365/papers/46865/view
- Veri: Kamuya açık STEM müfredatlarından 100 öğrenme hedefi (İngilizce).
- Yöntem: GPT tabanlı model vs uzman, SMART ölçütleri, Cohen κ + nitel anlaşmazlık analizi.
- Sonuç (özetten): yalnız "Relevant" boyutunda makul uyum; diğer boyutlarda tutarsız (κ sayısı sayfada yok).
- Fark: LLM ile çıktı **kalitesi** denetiminin en yakın örneği; İngilizce, Bloom basamağı ile birleşik değil, ölçülebilirlikte LLM–uzman uyumunun zayıf olduğu uyarısı.

**3.3 Fabiyi (2025) — ChatGPT'nin öğrenme çıktısı değerlendirmesi**
- APA: Fabiyi, S. (2025). What can ChatGPT not do in education? Evaluating its effectiveness in assessing educational learning outcomes. *Innovations in Education and Teaching International, 62*(2), 484–498. https://doi.org/10.1080/14703297.2024.2333395
- Veri: Örnek öğrenme çıktıları (sayı sayfada yok).
- Yöntem: ChatGPT'nin SMART uyumu ve bileşen (fiil, içerik, bağlam) tespiti, insan değerlendiricilerle karşılaştırma.
- Sonuç: Sayısal sonuç sayfada yok (başlık sınırlılık vurgusu yapıyor).
- Fark: Nitel; sistematik etiketli veri ve Türkçe yok.

**3.4 Saule, Subramanian & Bunescu (2026) — müfredat kılavuzuna göre materyal sınıflama**
- APA: Saule, E., Subramanian, K., & Bunescu, R. (2026). *Automatic classification of pedagogical materials against CS curriculum guidelines* (arXiv:2602.03962). arXiv. https://arxiv.org/abs/2602.03962
- Veri/Yöntem: Ders materyali korpusu, ACM/IEEE CS kılavuzu; klasik NLP vs LLM.
- Sonuç (özetten): manuel denetim ders başına ~1 gün; sayısal başarı özette yok.
- Fark: Akreditasyon/müfredat denetimi motivasyonunun (iş yükü) kanıtı; çıktı cümlesi kalitesi değil.

### Başlık 4 — Türkiye bağlamı ve temel kaynaklar

**4.1 Özer & Bayram (2026)**
- APA: Özer, Ş. K., & Bayram, İ. (2026). Türkiye'deki bir vakıf üniversitesinde mühendislik ders izlencelerinin öğrenme çıktıları ve ölçme araçları açısından incelenmesi [An examination of learning outcomes and assessment instruments in engineering course syllabi at a foundation university in Türkiye]. *Çukurova Üniversitesi Eğitim Fakültesi Dergisi, 55*(1), 154–195. https://doi.org/10.14812/cuefd.1633101
- Veri: 6 mühendislik bölümü, 125 izlence, 738 öğrenme çıktısı (2021–2022). Çıktılar İngilizce mi Türkçe mi PDF ilk sayfasında belirtilmiyor.
- Yöntem: Revize Bloom'a göre manuel kodlama + açıklık/ölçülebilirlik kontrol listesi.
- Sonuç (PDF özet): %65,7 üst düzey basamak; bazı çıktılarda ölçülemez fiil / tek çıktıda çoklu davranış; izlencelerin %40'ında 6'dan fazla çıktı.
- Fark: Bizim iki görevin (kalite + basamak) Türkiye'de **elle** yapıldığı en güncel emsal; otomasyon yok — doğrudan boşluk kanıtı.

**4.2 Yolcu (2019)**
- APA: Yolcu, H. H. (2019). Malzeme bilimi ve nano mühendislik programının öğrenme çıktılarının analizi [Analyzing learning outcomes in a materials science & nano engineering curriculum]. *Yükseköğretim ve Bilim Dergisi, 9*(3), 581–586. https://doi.org/10.5961/jhes.2019.356
- Veri: Özel bir üniversite, 41 ders, 324 kazanım.
- Yöntem: Doküman incelemesi; önce yapı (iyi/zayıf yapılandırılmış), sonra iyi yapılandırılmışları revize Bloom'a göre sınıflama.
- Sonuç (PDF özet): kazanımların %54'ü zayıf yapılandırılmış; iyi yapılandırılmışlar en çok hatırlama ve uygulamada.
- Fark: **Bizim iki aşamalı tasarımın (önce kalite, düzgünse basamak) birebir manuel karşılığı.** Otomatik değil; en güçlü motivasyon kaynağı.

**4.3 Demiröz (2025)**
- APA: Demiröz, E. (2025). Yönetim bilişim sistemleri eğitim programının "anlama odaklı tasarım" perspektifinden değerlendirilmesi [Assessment of management information systems curriculum from "understand by design" perspective]. *Trakya Üniversitesi Sosyal Bilimler Dergisi, 27*(Ek Sayı), 117–140. https://doi.org/10.26468/trakyasobed.1494801
- Veri: Bologna sitesindeki YBS lisans programı ve ders öğrenme çıktıları (Türkçe); 476 özel öğrenme hedefi, 14 program çıktısı.
- Yöntem: Bloom'a göre manuel analiz, program–ders tutarlılığı.
- Sonuç (PDF özet): 476 hedefin %30'u geçerli/güvenilir ölçme için uygun değil; kalanlar alt bilişsel düzeylerde yığılmış; 14 PÇ'nin tamamı üst düzeyde.
- Fark: Bologna bilgi paketi verisinin kullanılabilirliğini ve kalite sorununun ölçeğini gösterir; manuel.

**4.4 Schweter (2020) — BERTurk**
- APA: Schweter, S. (2020). *BERTurk – BERT models for Turkish* (Version 1.0.0) [Computer software]. Zenodo. https://doi.org/10.5281/zenodo.3770924
- Not: Zenodo kaydı "Software", 27 Nisan 2020; daha yeni sürüm mevcut. Model ailesi: cased/uncased, 32k/128k sözlük (GitHub stefan-it/turkish-bert, arama özetinden: 35 GB veri).

**4.5 Anderson & Krathwohl (2001) — revize taksonomi**
- APA: Anderson, L. W., & Krathwohl, D. R. (Eds.). (2001). *A taxonomy for learning, teaching, and assessing: A revision of Bloom's taxonomy of educational objectives* (Complete ed.). Addison Wesley Longman. ISBN 978-0-321-08405-7
- Not: eduq.info kataloğundan doğrulandı (yayıncı "Addison Wesley Longman"; yer bilgisi sayfada yok, yaygın atıfta "New York: Longman"). Kısaltılmış baskı ISBN 978-0-8013-1903-7 (arama özetinden). Eserin editörlü olduğu bilgisi katalogda "authors" olarak geçti; kesinlik için kütüphane kaydına bakılmalı.

---

## 2. Doğrulanamayanlar (ana listeye alınmadı)

| Kaynak (aramada görülen) | Neden |
|---|---|
| Sangodiah ve ark.? (2022). Identifying optimal baseline variant of unsupervised term weighting in question classification based on Bloom taxonomy. *Mendel*. (Arama özeti: SVM norm. TF-IDF %72,4, NB %63,0; en iyi %74,0) | DOAJ 403, VUT dspace bot koruması; yazar listesi görülmedi |
| Yahya, A. A., Osman, A., Taleb, A. M., & Alattab, A. A. (2013). Analyzing the cognitive level of classroom questions using machine learning techniques. *Procedia – Social and Behavioral Sciences, 97*, 587–595 | Yalnız arama özeti; sayfa açılmadı. 600 soruluk set Yahya et al. (2012)'ye atfediliyor |
| YÖK Açık Bilim tezi: "Türkçe dilinde yapılmış açık uçlu sınavların doğal dil işleme ile otomatik olarak değerlendirilmesi" (KNN %97, özet) | Sayfa iki kez "socket closed"; yazar/yıl görülmedi. Not: öğrenci **cevabı** değerlendirmesi, çıktı değil — Türkçe Bloom+NLP için tek ipucu, mutlaka elle kontrol edilmeli |
| IndoBERT-LSTM, JISEBI (2025), %88,75 doğruluk | Sayfa 502 |
| IJERT, BERT+XGBoost CO–PO eşleme | Açılmadı; preprint benzeri |
| TYMM-2024 Ortaokul Türkçe 106 öğrenme çıktısı (Bloom), Fen Bilimleri 143 çıktı, fizik programı 106 çıktı (DergiPark) | PDF'ler indirilmedi/okunmadı; yalnız arama özeti |
| ONCAT (Ontario) "Automating gap analysis of learning outcomes through NLP" | Bağlantı reddedildi |
| IAFOR ECE2025 NLP ile izlence değerlendirme | 403 |
| ASEE "Developing a curriculum mapping tool…" (ABET SO ikili kodlama) | Açılmadı |
| Türk üniversitesi kılavuzları (Toros, Tarsus, Bakırçay, Nevşehir): "bilir, anlar, öğrenir, kavrar" kaçınılacak fiiller | Gri literatür; tek tek açılmadı. Raporda "belirsiz fiil" tanımı için kurumsal kılavuz olarak atıf yapılacaksa bir tanesi açılıp doğrulanmalı |

---

## 3. Boşluk

Bulabildiğimiz kadarıyla:

**(a) Türkçe öğrenme çıktılarında cümle kalitesi tespiti (otomatik):** Bulunamadı. Türkiye'de kalite tespiti yalnız **manuel doküman analizi** olarak yapılmış: Yolcu (2019) kazanımların %54'ünü zayıf yapılandırılmış buldu; Demiröz (2025) 476 hedefin %30'unu ölçmeye uygun değil buldu; Özer & Bayram (2026) ölçülemez fiil ve çoklu davranış sorunlarını raporladı. Uluslararası literatürde LLM ile kalite denetimi (SMART) yalnız İngilizce ve küçük ölçekte (Butt et al., 2025: 100 hedef; Fabiyi, 2025) ve LLM–uzman uyumu zayıf/tutarsız.

**(b) Türkçe öğrenme çıktılarında otomatik Bloom sınıflaması:** Bulunamadı. Otomatik Bloom sınıflamasının tamamı İngilizce (Li et al., 2022; Shaikh et al., 2021; Almatrafi & Johri, 2025) veya başka diller (Endonezce, Portekizce). Türkçede yalnız açık uçlu sınav **cevaplarını** NLP ile değerlendiren bir tez ipucu var (doğrulanamadı). Türkçe çıktı/sorular üzerine Bloom çalışmalarının hepsi manuel içerik analizi.

**(c) YÖKAK/MÜDEK bağlamında otomatik denetim:** Bulunamadı. Bulunan kurumsal belgeler (ders–program çıktısı matrisleri, izleme raporları) manuel ya da yalnız matris hesabı yapan bilgi sistemleri. Otomatik CLO–PLO eşleştirme İngilizce/ABET-NBA bağlamında var (Zaki et al., 2023; Shiferaw et al., 2024; Asiri, 2022) ama hiçbiri eşleştirmeden önce çıktı kalitesini denetlemiyor.

**Özgünlük cümlesi önerisi:** Literatürdeki sınıflandırıcılar her girdinin geçerli bir Bloom basamağına ait olduğunu varsayar; "kötü yazılmış çıktı" (belirsiz fiil, konu başlığı) bir **ön sınıf** olarak modellenmez. Önerilen çalışma (1) kalite reddi + (2) revize Bloom sınıflamasını tek boru hattında, Türkçe Bologna verisinde ve YÖKAK/MÜDEK düzeltme listesi çıktısıyla birleştirir; Yolcu (2019)'un manuel iki aşamalı yöntemini otomatikleştirir. Ayrıca literatürdeki ana yöntem tartışması (küçük veride SVM ≥ BERT: Kumar et al., 2025; büyük veride BERT > LLM: Almatrafi & Johri, 2025; Li et al., 2022) Türkçe ve BERTurk ile hiç sınanmamış.

---

## 4. Yapılan aramalar (sorgu listesi)

İngilizce:
1. BloomNet Bloom's taxonomy classification learning objectives
2. automatic classification of learning outcomes Bloom taxonomy BERT
3. exam question classification Bloom taxonomy SVM Naive Bayes TF-IDF
4. ChatGPT GPT-4 classify Bloom's taxonomy learning objectives evaluation
5. GPT-4 prompt classification course learning outcomes revised Bloom's taxonomy rhetorical context BERT comparison
6. Bloom taxonomy question classification CNN LSTM deep learning Laddha OR Mohammed OR Shaikh
7. Mohammed Omar 2020 PLoS ONE question classification Bloom TFPOS-IDF word2vec
8. Shaikh Daudpota Imran "Bloom's Learning Outcomes' Automatic Classification Using LSTM…" IEEE Access DOI
9. Yahya Osman Taleb Alattab 2013 analyzing cognitive level of classroom questions…
10. automatic mapping course outcomes to ABET student outcomes NLP
11. "automating the mapping of course learning outcomes to program learning outcomes" natural language processing
12. Zaki 2023 CLO PLO mapping Education and Information Technologies precision 83.1
13. learning outcomes quality NLP measurable verbs automated audit curriculum syllabus analysis
14. large language model evaluate quality of learning objectives measurable verbs rubric automated feedback
15. BERTurk Schweter zenodo 2020 dbmdz Turkish BERT
16. Anderson Krathwohl 2001 A taxonomy for learning, teaching, and assessing Longman ISBN

Türkçe:
17. öğrenme çıktıları Bloom taksonomisi analiz dergipark
18. ders öğrenme çıktıları analizi mühendislik ölçülemeyen fiiller izlence Bloom 738
19. Türkçe soru sınıflandırma Bloom taksonomisi makine öğrenmesi
20. MÜDEK program çıktıları ders çıktıları eşleştirme otomatik metin madenciliği
21. Bologna bilgi paketi öğrenme çıktıları inceleme ölçülebilir fiil "bilir" "anlar" çalışma
22. Bloom taksonomisi derin öğrenme BERT Türkçe sınav soruları otomatik sınıflandırma makale
23. YÖKAK öğrenme çıktıları yapay zeka otomatik değerlendirme program çıktısı

Sınırlılık: Arama motoru ABD tabanlı; DergiPark'ın kendi arama arayüzü, Google Scholar, YÖK Tez Merkezi ve TR Dizin doğrudan sorgulanamadı. Boşluk iddiası "bulabildiğimiz kadarıyla" düzeyindedir; teslimden önce YÖK Tez Merkezi'nde "öğrenme çıktısı" + "doğal dil işleme" ve DergiPark'ta "öğrenme çıktısı sınıflandırma" elle aranmalı.

## Ek tarama: boşluk kontrolü (ana oturum, 2026-11-09)

DergiPark araması ve Google Akademik robot doğrulaması istedi; YÖK Tez arama formu "Geçersiz sorgulama" döndü. Doğrulama geçilmedi. Yerine DergiPark makalelerinin çoğunu dizinleyen OpenAlex API'si ile 13 sorgu yapıldı (Türkçe: "öğrenme çıktıları bloom", "öğrenme çıktıları makine öğrenmesi", "öğrenme çıktıları doğal dil işleme", "kazanımlar bloom sınıflandırma otomatik", "program çıktıları akreditasyon metin madenciliği", "ders öğrenme çıktıları analizi", "bloom taksonomisi derin öğrenme", "bloom taksonomisi makine öğrenmesi soru sınıflandırma"; İngilizce: "Turkish learning outcomes Bloom taxonomy classification", "Turkish questions Bloom taxonomy machine learning", "Turkish course learning outcomes natural language processing", "Bloom taxonomy BERT Turkish", "learning outcomes quality measurable verbs automatic").

Sonuç: Türkçe öğrenme çıktılarını otomatik sınıflayan ya da kalitesini denetleyen bir çalışma çıkmadı. Türkçe Bloom çalışmalarının tamamı elle doküman analizi (ör. coğrafya, kimya, fen programı kazanımları). Yakın ama farklı görevde üç doğrulanmış kaynak (OpenAlex kaydı ve özeti okundu):

- Kara, A., Avinç Kara, Z., & Yıldırım, S. (2025). Answer-based and reference-based BERT models for automatic scoring of Turkish short answers: The decisive role of task complexity. *International Journal of Assessment Tools in Education, 12*(4), 905–925. https://doi.org/10.21449/ijate.1687429 — Türkçe BERT eğitimde kullanılmış; ama öğrenci cevabı puanlama, 246 fizik öğrencisi, 4 soru. Çıktı cümlesi değil.
- Aslan Yılmaz, K., & Deniz, K. Z. (2024). Natural language processing and machine learning applications for assessment and evaluation in education: Opportunities and new approaches. *Eğitimde ve Psikolojide Ölçme ve Değerlendirme Dergisi*. https://doi.org/10.21031/epod.1551568 — Türkçe örneklerle NLP'nin ölçme-değerlendirmede kullanımı (madde üretimi, metin madenciliği); öğrenme çıktısı denetimi yok.
- Newton, P. M., Da Silva, A., & Peters, L. G. (2020). A pragmatic master list of action verbs for Bloom's taxonomy. *Frontiers in Education, 5*. https://doi.org/10.3389/feduc.2020.00107 — 35 kurumdan 47 fiil listesi; listeler arasında uyum çok az; "kaçınılacak fiiller" listesi çıkarılmış. Kural rehberi ve kural tabanlı taban çizgisi için doğrudan kullanılabilir.

Not: Anahtar kelime çıkmaması "yok" demek değildir; raporda "bulabildiğimiz kadarıyla" dili kullanılacak ve bu sınır (DergiPark/YÖK Tez kendi aramaları yapılamadı) yöntem kısmında yazılacak.

- Google Akademik: Alptekin elle baktı, Türkçe öğrenme çıktılarını otomatik denetleyen çalışma bulmadı (Alptekin beyanı, 2026-11-09).

- **Alptekin'in bulduğu yakın çalışma (2026-11-09, doğrulanmadı):** H. Açar, "Öğrenme çıktılarının derin öğrenme ile Bloom taksonomisi'ne göre sınıflandırılması" (Google Akademik kaydı xWP76ssuw4QJ). Künye (yıl, yayın yeri, veri) henüz okunamadı: Google Akademik ana oturumu engelledi, OpenAlex/Crossref/web aramasında çıkmadı. Doğrulanırsa boşluk iddiası daralır: Türkçe çıktıların Bloom sınıflaması denenmiş olur; bizim farkımız kalite tespiti (belirsiz / çıktı değil) ve program düzeyi rapor olur.
  - Alptekin özetin ilk kısmını yapıştırdı (2026-11-09): eski Bloom basamakları (bilgi, kavrama, uygulama, analiz, sentez, değerlendirme) kullanılıyor; amaç ders öğrenme çıktılarını Bloom seviyesine göre sınıflamak ve değerlendirme öğeleriyle uygunluğu sağlamak; gerekçe "binlerce çıktıyı elle eşleştirme" yükü. Özet cümlesiyle web araması sonuç vermedi; yayın yeri, yıl, veri ve sonuç hâlâ bilinmiyor.
  - **Güncelleme (2026-11-09):** Kayıt Harran Üniversitesi açık arşivinde: http://acikerisim.harran.edu.tr:8080/jspui/handle/11513/4182 (yazar H. Açar). Arşiv sunucusu ana oturumdan açılmadı; Alptekin'e göre tam metin erişime açık değil. Elimizdeki bilgi Google Akademik'in kayıt özetinden (Alptekin yapıştırdı), tam metin okunmadı; yıl ve tür (tez/makale) bilinmiyor.
  - Özete göre: Harran Üniversitesi öğrenme çıktıları; 2023 (6.224) ve 2024 (32.097; rehberlik öncesi 15.368, sırası 5.438, sonrası 11.291). 11 sınıf: bilişsel 6 + duyuşsal 4 + psikomotor 1. Word2Vec-LSTM, FastText-LSTM, BERT-LSTM; en iyi BERT, doğruluk ~%90 (2023) ve %91,25 (2024 rehberlik sırası). Az örnekli Yaratma/Değerlendirme sınıflarında karışıklık. Kalite sınıfı (belirsiz / çıktı değil) yok; tek üniversite.
  - Raporda kullanım: yakın çalışma olarak anılacak, sayılar "kayıt özetine göre" diye verilecek; kaynakçada yıl Alptekin'den teyit edilmeden yazılmayacak.
  - Boşluk yeniden yazımı: Türkçe çıktıların Bloom sınıflaması denenmiş (Açar); yazım kalitesini denetleyen, çok programlı bir üniversitede düzeltilecek dersleri raporlayan çalışma bulunamadı. Not: "rehberlik eğitimi sonrası" doğruluğun artması, yazım kalitesi iyileşince sınıflamanın kolaylaştığını düşündürüyor; bizim iki adımlı tasarımımızı destekleyen bir ipucu (yorum, doğrulanmadı).
  - Yıl: 2024 (Alptekin, Google Akademik kaydından, 2026-11-09). Kaynakça satırı (tür bilinmediği için arşiv kaydı olarak): Açar, H. (2024). *Öğrenme çıktılarının derin öğrenme ile Bloom taksonomisi'ne göre sınıflandırılması*. Harran Üniversitesi Açık Erişim Arşivi. http://acikerisim.harran.edu.tr:8080/jspui/handle/11513/4182
