(function () {
'use strict';

var BLOOM = {
  HATIRLAMA: [1, 'Hatırlama'], ANLAMA: [2, 'Anlama'], UYGULAMA: [3, 'Uygulama'],
  ANALIZ: [4, 'Analiz'], DEGERLENDIRME: [5, 'Değerlendirme'], YARATMA: [6, 'Yaratma'],
  BILISSEL_DEGIL: [0, 'Bilişsel değil']
};
var BLOOM_RENK = ['#B9BEC6', '#929BA8', '#6B788B', '#48596F', '#304159', '#1B2A41'];
var BLOOM_ALAN = ['hatirlama', 'anlama', 'uygulama', 'analiz', 'degerlendirme', 'yaratma'];
var BLOOM_AD = ['Hatırlama', 'Anlama', 'Uygulama', 'Analiz', 'Değerlendirme', 'Yaratma'];
var KALITE_AD = { DUZGUN: 'Düzgün', BELIRSIZ: 'Belirsiz', CIKTI_DEGIL: 'Çıktı değil', INGILIZCE: 'İngilizce' };
var KALITE_SINIF = { DUZGUN: 'good', BELIRSIZ: 'unclear', CIKTI_DEGIL: 'not', INGILIZCE: 'english' };

var MSG_SUNUCU = 'Sunucuya ulaşılamadı. baslat.bat dosyasının açık olduğundan emin olun.';
var MSG_RAPOR = 'Rapor verisi alınamadı. baslat.bat dosyasının açık olduğundan emin olun.';

function $(id) { return document.getElementById(id); }

function el(tag, cls, text) {
  var e = document.createElement(tag);
  if (cls) e.className = cls;
  if (text !== undefined && text !== null) e.textContent = text;
  return e;
}

function clear(node) { while (node.firstChild) node.removeChild(node.firstChild); }

function sayi(x) { return Number(x) || 0; }

function yuzde(x, basamak) {
  var d = basamak === undefined ? 1 : basamak;
  return '%' + sayi(x).toFixed(d).replace('.', ',');
}

function yuzdeKisa(x) {
  var v = sayi(x);
  return yuzde(v, v >= 1 || v === 0 ? 0 : 1);
}

function binlik(n) {
  return String(Math.round(sayi(n))).replace(/\B(?=(\d{3})+(?!\d))/g, '.');
}

function baslikYazim(s) {
  var kucuk = String(s).toLocaleLowerCase('tr');
  return kucuk.replace(/(^|[\s(\-\/])(\p{L}+)/gu, function (m, ayrac, kelime) {
    if (kelime === 've') return ayrac + kelime;
    return ayrac + kelime.charAt(0).toLocaleUpperCase('tr') + kelime.slice(1);
  });
}

function bar(parcalar, cls) {
  var b = el('div', 'bar' + (cls ? ' ' + cls : ''));
  parcalar.forEach(function (p) {
    var s = el('span', p.cls || '');
    s.style.width = Math.max(0, p.w) + '%';
    if (p.renk) s.style.background = p.renk;
    b.appendChild(s);
  });
  return b;
}

/* ---------- Sekmeler ---------- */
var raporBasladi = false;

function showScreen() {
  var rapor = location.hash === '#rapor';
  $('dene-ekran').hidden = rapor;
  $('rapor-ekran').hidden = !rapor;
  $('dene-tab').classList.toggle('active', !rapor);
  $('rapor-tab').classList.toggle('active', rapor);
  if (rapor) $('rapor-tab').setAttribute('aria-current', 'page'); else $('rapor-tab').removeAttribute('aria-current');
  if (!rapor) $('dene-tab').setAttribute('aria-current', 'page'); else $('dene-tab').removeAttribute('aria-current');
  if (rapor && !raporBasladi) { raporBasladi = true; raporYukle(); }
}

/* ---------- Sekme 1: Cümleni dene ---------- */
var kutu = $('cumleler');
var dugme = $('kontrol');
var sonuclar = $('sonuclar');
var BOS_METIN = 'Sonuçlar burada görünecek.';
var calisiyor = false;

function bosDurum(metin) {
  clear(sonuclar);
  sonuclar.appendChild(el('p', 'muted', metin));
}

function satirlar() {
  return kutu.value.split(/\r?\n/).map(function (s) { return s.trim(); }).filter(function (s) { return s.length > 0; });
}

function kontrolEt() {
  if (calisiyor) return;
  var liste = satirlar();
  if (liste.length === 0) { bosDurum('Önce en az bir cümle yazın.'); return; }
  if (liste.length > 200) { bosDurum('En çok 200 cümle kontrol edilebilir.'); return; }
  calisiyor = true;
  dugme.disabled = true;
  dugme.textContent = 'Kontrol ediliyor…';
  fetch('/api/kontrol', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ cumleler: liste })
  }).then(function (r) {
    return r.json().then(function (j) { return { ok: r.ok, veri: j }; }, function () { return { ok: r.ok, veri: null }; });
  }).then(function (s) {
    if (!s.ok) {
      var h = s.veri && typeof s.veri.hata === 'string' ? s.veri.hata : 'Kontrol sırasında bir hata oluştu.';
      bosDurum(h);
    } else {
      sonuclariCiz(s.veri);
    }
  }).catch(function (e) {
    bosDurum(e instanceof TypeError ? MSG_SUNUCU : 'Sonuçlar gösterilemedi.');
  }).then(function () {
    calisiyor = false;
    dugme.disabled = false;
    dugme.textContent = 'Kontrol et';
  });
}

function ozetMetni(o) {
  var toplam = sayi(o.toplam);
  var parcalar = [];
  if (sayi(o.duzgun) > 0) parcalar.push(sayi(o.duzgun) + ' düzgün');
  if (sayi(o.belirsiz) > 0) parcalar.push(sayi(o.belirsiz) + ' belirsiz');
  if (sayi(o.cikti_degil) > 0) parcalar.push(sayi(o.cikti_degil) + ' çıktı değil');
  if (sayi(o.ingilizce) > 0) parcalar.push(sayi(o.ingilizce) + ' İngilizce');
  return toplam + ' cümle: ' + parcalar.join(', ');
}

function sonuclariCiz(veri) {
  clear(sonuclar);
  var o = veri.ozet || {};
  var liste = Array.isArray(veri.sonuclar) ? veri.sonuclar : [];
  var toplam = sayi(o.toplam) || liste.length;
  o.toplam = toplam;
  sonuclar.appendChild(el('h2', 'summary', ozetMetni(o)));
  var oran = function (n) { return toplam > 0 ? sayi(n) * 100 / toplam : 0; };
  sonuclar.appendChild(bar([
    { cls: 'good-bg', w: oran(o.duzgun) },
    { cls: 'unclear-bg', w: oran(o.belirsiz) },
    { cls: 'not-bg', w: oran(o.cikti_degil) },
    { cls: 'eng-bg', w: oran(o.ingilizce) }
  ], 'summary-bar'));
  liste.forEach(function (r) { sonuclar.appendChild(satirCiz(r)); });
}

function cumleDugumu(r) {
  var p = el('p', 'sentence');
  var c = typeof r.cumle === 'string' ? r.cumle : '';
  var araliklar = [];
  if (r.kalite === 'BELIRSIZ' && Array.isArray(r.vurgular)) {
    var onceki = 0;
    r.vurgular.forEach(function (v) {
      if (!v || !Number.isInteger(v.bas) || !Number.isInteger(v.son)) return;
      if (v.bas < onceki || v.son <= v.bas || v.son > c.length) return;
      araliklar.push(v);
      onceki = v.son;
    });
  }
  if (araliklar.length === 0) { p.textContent = c; return p; }
  var konum = 0;
  araliklar.forEach(function (v) {
    if (v.bas > konum) p.appendChild(document.createTextNode(c.slice(konum, v.bas)));
    p.appendChild(el('span', 'problem', c.slice(v.bas, v.son)));
    konum = v.son;
  });
  if (konum < c.length) p.appendChild(document.createTextNode(c.slice(konum)));
  return p;
}

function merdiven(seviye, ad) {
  var m = el('div', 'ladder');
  var adimlar = el('div', 'steps');
  for (var i = 1; i <= 6; i++) adimlar.appendChild(el('i', i === seviye ? 'chosen' : ''));
  m.appendChild(adimlar);
  m.appendChild(el('p', 'ladder-label', ad));
  return m;
}

function satirCiz(r) {
  var kalite = KALITE_SINIF[r.kalite] ? r.kalite : 'CIKTI_DEGIL';
  var duzgun = kalite === 'DUZGUN';
  var satir = el('div', 'result ' + KALITE_SINIF[kalite]);
  var metin = duzgun ? el('div') : satir;
  metin.appendChild(cumleDugumu(r));
  var meta = el('p', 'meta');
  meta.appendChild(el('span', 'status', KALITE_AD[kalite]));
  if (kalite !== 'INGILIZCE' && typeof r.guven === 'number') {
    meta.appendChild(document.createTextNode(' · güven %' + Math.min(99, Math.round(r.guven * 100))));
  }
  metin.appendChild(meta);
  var not = typeof r.not === 'string' && r.not ? r.not : null;
  if (not) {
    metin.appendChild(el('p', 'suggestion', (kalite === 'BELIRSIZ' ? 'Öneri: ' : '') + not));
  }
  if (duzgun) {
    satir.appendChild(metin);
    var b = BLOOM[r.bloom] || BLOOM.BILISSEL_DEGIL;
    satir.appendChild(merdiven(b[0], b[1]));
  }
  return satir;
}

function ekle(cumle) {
  var simdiki = kutu.value;
  if (simdiki.trim() === '') kutu.value = cumle;
  else kutu.value = simdiki.replace(/\s+$/, '') + '\n' + cumle;
  kontrolEt();
}

dugme.addEventListener('click', kontrolEt);
kutu.addEventListener('keydown', function (e) {
  if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) { e.preventDefault(); kontrolEt(); }
});
$('temizle').addEventListener('click', function () {
  kutu.value = '';
  bosDurum(BOS_METIN);
  kutu.focus();
});
Array.prototype.forEach.call(document.querySelectorAll('.example'), function (b) {
  b.addEventListener('click', function () { ekle(b.textContent); });
});

/* ---------- Sekme 2: Bölüm raporu ---------- */
var veri = null;
var faculty = $('faculty');
var department = $('department');
var icerik = $('rapor-icerik');
var birimler = [];

function raporYukle() {
  clear(icerik);
  icerik.appendChild(el('p', 'muted', 'Yükleniyor…'));
  fetch('/api/veri').then(function (r) {
    if (!r.ok) throw new Error('http');
    return r.json();
  }).then(function (j) {
    if (!j || !Array.isArray(j.birimler)) throw new Error('bicim');
    veri = j;
    raporKur();
  }).catch(function () {
    clear(icerik);
    icerik.appendChild(el('p', 'muted', MSG_RAPOR));
    raporBasladi = false;
  });
}

function raporKur() {
  birimler = veri.birimler.filter(function (b) { return Array.isArray(b.programlar) && b.programlar.length > 0; })
    .slice().sort(function (a, b) { return String(a.ad).localeCompare(String(b.ad), 'tr'); });
  clear(faculty);
  birimler.forEach(function (b, i) {
    var o = el('option', '', baslikYazim(b.ad));
    o.value = String(i);
    faculty.appendChild(o);
  });
  if (birimler.length === 0) { clear(icerik); icerik.appendChild(el('p', 'muted', MSG_RAPOR)); return; }
  faculty.selectedIndex = 0;
  bolumleriDoldur();
}

function bolumleriDoldur() {
  var b = birimler[Number(faculty.value)];
  var progs = b.programlar.slice().sort(function (x, y) {
    return String(x.ad).localeCompare(String(y.ad), 'tr') || String(x.seviye).localeCompare(String(y.seviye), 'tr');
  });
  b._sirali = progs;
  clear(department);
  progs.forEach(function (p, i) {
    var o = el('option', '', p.ad + ' (' + p.seviye + ')');
    o.value = String(i);
    department.appendChild(o);
  });
  department.selectedIndex = 0;
  bolumCiz();
}

function bigStat(deger, cls, etiket, ek) {
  var s = el('div', 'stat');
  s.appendChild(el('p', 'number' + (cls ? ' ' + cls : ''), deger));
  s.appendChild(el('p', 'stat-label', etiket));
  if (ek) s.appendChild(el('p', 'benchmark', ek));
  return s;
}

function bolumCiz() {
  var b = birimler[Number(faculty.value)];
  var p = b._sirali[Number(department.value)];
  var st = p.istatistikler || {};
  var uni = veri.universite || {};
  clear(icerik);

  var baslik = el('section', 'department');
  baslik.appendChild(el('h2', '', p.ad));
  baslik.appendChild(el('p', '', baslikYazim(b.ad) + ' · ' + p.seviye + ' · ' + binlik(st.ders_sayisi) + ' ders · ' + binlik(st.cumle_sayisi) + ' cümle'));
  icerik.appendChild(baslik);

  var rakamlar = el('div', 'stats');
  rakamlar.appendChild(bigStat(yuzde(st.sorunlu_yuzde), sayi(st.sorunlu_yuzde) > sayi(uni.sorunlu_yuzde) ? 'warn' : '', 'Sorunlu cümle', 'Üniversite ortalaması ' + yuzde(uni.sorunlu_yuzde)));
  rakamlar.appendChild(bigStat(yuzde(st.ust_basamak_yuzde), '', 'Üst basamaklardaki cümle', 'Üniversite ortalaması ' + yuzde(uni.ust_basamak_yuzde)));
  rakamlar.appendChild(bigStat(binlik(p.bos_ders_sayisi), '', 'Çıktısı boş ders', null));
  icerik.appendChild(rakamlar);

  var kalite = el('section', 'distribution');
  kalite.appendChild(el('h3', '', 'Kalite dağılımı'));
  kalite.appendChild(bar([
    { cls: 'good-bg', w: sayi(st.duzgun_yuzde) },
    { cls: 'unclear-bg', w: sayi(st.belirsiz_yuzde) },
    { cls: 'not-bg', w: sayi(st.cikti_degil_yuzde) }
  ]));
  var lk = el('div', 'legend');
  [['good-bg', 'Düzgün', st.duzgun_yuzde], ['unclear-bg', 'Belirsiz', st.belirsiz_yuzde], ['not-bg', 'Çıktı değil', st.cikti_degil_yuzde]].forEach(function (x) {
    var s = el('span');
    s.appendChild(el('i', x[0]));
    s.appendChild(document.createTextNode(x[1] + ' ' + yuzde(x[2])));
    lk.appendChild(s);
  });
  kalite.appendChild(lk);
  icerik.appendChild(kalite);

  var bloom = el('section', 'distribution');
  bloom.appendChild(el('h3', '', 'Basamak dağılımı (düzgün cümleler)'));
  if (sayi(st.duzgun_sayi) === 0) {
    bloom.appendChild(el('p', 'muted', 'Düzgün cümle yok.'));
  } else {
    var parcalar = [];
    var etiketler = [];
    BLOOM_ALAN.forEach(function (a, i) {
      var v = sayi(st['bloom_' + a + '_yuzde']);
      parcalar.push({ w: v, renk: BLOOM_RENK[i] });
      etiketler.push({ renk: BLOOM_RENK[i], ad: BLOOM_AD[i], v: v });
    });
    var bd = sayi(st.bloom_bilissel_degil_yuzde);
    parcalar.push({ cls: 'not-bg', w: bd });
    etiketler.push({ cls: 'not-bg', ad: 'Bilişsel değil', v: bd });
    bloom.appendChild(bar(parcalar));
    var lb = el('div', 'legend bloom-legend');
    etiketler.forEach(function (x) {
      var s = el('span');
      var i = el('i', x.cls || '');
      if (x.renk) i.style.background = x.renk;
      s.appendChild(i);
      s.appendChild(document.createTextNode(x.ad + ' ' + yuzdeKisa(x.v)));
      lb.appendChild(s);
    });
    bloom.appendChild(lb);
  }
  icerik.appendChild(bloom);

  icerik.appendChild(tabloCiz(p.duzeltilecek));
}

function tabloCiz(dersler) {
  var bolum = el('section', 'repair');
  var th = el('div', 'table-heading');
  th.appendChild(el('h2', '', 'Düzeltilecek dersler'));
  th.appendChild(el('p', '', 'Cümlelerinin en az yarısı sorunlu olan dersler (en çok 15)'));
  bolum.appendChild(th);
  if (!Array.isArray(dersler) || dersler.length === 0) {
    bolum.appendChild(el('p', 'muted', 'Bu bölümde düzeltilecek ders bulunamadı.'));
    return bolum;
  }
  var sarmal = el('div', 'table-wrap');
  var t = el('table');
  var ust = el('thead');
  var ur = el('tr');
  ['Kod', 'Ders', 'Cümle', 'Sorunlu'].forEach(function (h) { ur.appendChild(el('th', '', h)); });
  ust.appendChild(ur);
  t.appendChild(ust);
  var gov = el('tbody');
  dersler.forEach(function (d) {
    var tr = el('tr', 'row');
    tr.tabIndex = 0;
    tr.setAttribute('role', 'button');
    tr.setAttribute('aria-expanded', 'false');
    var k = el('td');
    var tg = el('span', 'toggle', '+');
    tg.setAttribute('aria-hidden', 'true');
    k.appendChild(tg);
    k.appendChild(document.createTextNode(d.ders_kodu));
    tr.appendChild(k);
    tr.appendChild(el('td', '', d.ders_adi));
    tr.appendChild(el('td', '', String(sayi(d.cumle_sayisi))));
    tr.appendChild(el('td', '', String(sayi(d.sorunlu_sayi))));
    var acik = null;
    function degistir() {
      if (acik) {
        gov.removeChild(acik);
        acik = null;
        tr.setAttribute('aria-expanded', 'false');
        tg.textContent = '+';
        return;
      }
      acik = el('tr', 'expanded');
      var td = el('td');
      td.colSpan = 4;
      (Array.isArray(d.cumleler) ? d.cumleler : []).forEach(function (c) {
        td.appendChild(el('p', c.kalite === 'CIKTI_DEGIL' ? 'not' : '', c.cumle));
      });
      acik.appendChild(td);
      gov.insertBefore(acik, tr.nextSibling);
      tr.setAttribute('aria-expanded', 'true');
      tg.textContent = '−';
    }
    tr.addEventListener('click', degistir);
    tr.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); degistir(); }
    });
    gov.appendChild(tr);
  });
  t.appendChild(gov);
  sarmal.appendChild(t);
  bolum.appendChild(sarmal);
  return bolum;
}

faculty.addEventListener('change', bolumleriDoldur);
department.addEventListener('change', bolumCiz);

addEventListener('hashchange', showScreen);
showScreen();
})();
