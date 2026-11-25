(function () {
'use strict';

function low(s) { return s.replace(/I/gu, 'ı').replace(/İ/gu, 'i').toLowerCase(); }

var FIIL_EK = /(ir|ır|ur|ür|ar|er|r|ebilir|abilir|ebilmek|abilmek|ebilme|abilme|mek|mak|me|ma|ecektir|acaktır|ecek|acak|ilir|ılır|ulur|ülür|irler|ırlar|urlar|ürler|erler|arlar)$/u;
var BEL_KOK = ['öğren', 'kavra', 'anla', 'bil', 'edin', 'kazan', 'geliş', 'sahip', 'takip', 'farkında', 'algıla'];
var BEL_IFADE = /b[iıİ]lg[iıİ] sah[iıİ]b[iıİ]|hakk[ıiİ]nda b[iıİ]lg[iıİ]|b[iıİ]lg[iıİ]s[iıİ] olur|fark[ıiİ]ndal[ıiİ]k|önem[iıİ]n[iıİ]|b[iıİ]lg[iıİ]len/iu;
var OLC_KOK = ['hesapla', 'uygula', 'analiz', 'tasarla', 'geliştirir', 'geliştirebil', 'çöz', 'açıkla', 'tanımla', 'karşılaştır', 'değerlendir', 'kullan', 'oluştur', 'yaz', 'hazırla', 'seç', 'ölç', 'çiz', 'kur', 'yorumla', 'sınıflandır', 'listele', 'planla', 'üret', 'yap', 'belirle', 'ifade'];

function kokVar(sozcuk, kokler) {
  return kokler.some(function (kok) { return sozcuk.indexOf(kok) === 0; });
}

function kural(s) {
  var k = low(s);
  var w = k.match(/[a-zçğıöşüâîû]+/gu) || [];
  var fiiller = w.filter(function (x) { return FIIL_EK.test(x) && x.length > 3; });
  if (!fiiller.length) return 'CIKTI_DEGIL';
  var olc = fiiller.some(function (x) { return kokVar(x, OLC_KOK); });
  var bel = BEL_IFADE.test(k) || fiiller.some(function (x) { return kokVar(x, BEL_KOK); });
  return bel && !olc ? 'BELIRSIZ' : 'DUZGUN';
}

var TR = /[çğıöşüÇĞİÖŞÜ]/u;
// Python re.I ayrıca ı, İ, ſ ve K harflerini ASCII eşlerine dahil eder.
// Python \w: Unicode harfler, sayılar ve alt çizgi.
var EN = /(?<![\p{L}\p{N}_])(the|and|of|to|w[iıİ]ll|be able|[sſ]tudent[sſ]?|under[sſ]tand|de[sſ]cr[iıİ]be|expla[iıİ]n|apply)(?![\p{L}\p{N}_])/iu;
function ing(s) { return !TR.test(s) && EN.test(s); }

var _B = 'açıklar';
var ONERI = {
  bilgi: ['açıklar', 'karşılaştırır'], kavra: ['örnekle açıklar', 'uygular'],
  ogren: ['uygular', 'açıklar'], bilir: ['tanımlar', 'listeler'],
  farkinda: ['örnek verir', 'tartışır'], beceri: ['uygular', 'gösterir']
};
var _OL = ['olur', 'olunur', 'olurlar', 'olabilir', 'olabilirler', 'olmak', 'olma'];
var _EDIN = ['edinir', 'edinirler', 'edinebilir', 'edinebilirler', 'edinmek', 'edinme'];
var _KAZAN = ['kazanır', 'kazanırlar', 'kazanabilir', 'kazanabilirler', 'kazanmak', 'kazanma'];
var _EDER = ['eder', 'ederler', 'edebilir', 'edebilirler', 'etmek', 'etme'];
var _SAGLA = ['sağlar', 'sağlarlar', 'sağlayabilir', 'sağlayabilirler', 'sağlamak', 'sağlama'];
var _TANIM = [];
function tanimEkle(onek, ekler, grup) {
  ekler.forEach(function (ek) { _TANIM.push([onek + ek, grup]); });
}
['bilgi sahibi ', 'fikir sahibi '].forEach(function (o) { tanimEkle(o, _OL, 'bilgi'); });
['hakkında bilgi ', 'bilgi '].forEach(function (o) { tanimEkle(o, _EDIN, 'bilgi'); });
tanimEkle('bilgi ', _KAZAN, 'beceri');
tanimEkle('bilinç ', _KAZAN, 'farkinda');
tanimEkle('farkındalık ', _KAZAN, 'farkinda');
tanimEkle('beceri ', _KAZAN, 'beceri');
tanimEkle('farkında ', _OL, 'farkinda');
tanimEkle('takip ', _EDER, 'beceri');
['hakimiyet ', 'hâkimiyet '].forEach(function (o) { tanimEkle(o, _SAGLA, 'beceri'); });
tanimEkle('', ['gelişir', 'gelişirler', 'gelişebilir', 'gelişmek', 'gelişme'], 'beceri');
tanimEkle('öğren', ['ir', 'irler', 'ebilir', 'ebilirler', 'mek', 'me'], 'ogren');
tanimEkle('an', ['lar', 'larlar', 'layabilir', 'layabilirler', 'lamak', 'lama'], 'kavra');
tanimEkle('kavra', ['r', 'rlar', 'yabilir', 'yabilirler', 'mak', 'ma'], 'kavra');
tanimEkle('bil', ['ir', 'irler', 'ebilir', 'ebilirler', 'mek', 'me'], 'bilir');
tanimEkle('tan', ['ır', 'ırlar', 'ıyabilir', 'ıyabilirler', 'ımak', 'ıma'], 'bilir');
var _GRUP = Object.create(null);
_TANIM.forEach(function (t) { _GRUP[t[0]] = t[1]; });
var BELIRSIZ = Object.keys(_GRUP).map(function (k) { return [k, _GRUP[k]]; })
  .sort(function (a, b) { return b[0].length - a[0].length; });
var _HARF = 'a-zçğıöşüâîû0-9_';
// Python \s ayrıca U+001C–001F ve U+0085'i içerir; U+FEFF'i içermez.
var BOSLUK = '[\\t-\\r\\x1c-\\x20\\x85\\xa0\\u1680\\u2000-\\u200a\\u2028\\u2029\\u202f\\u205f\\u3000]';
var _DESEN = new RegExp('(?<![' + _HARF + '])(?:' + BELIRSIZ.map(function (t) {
  return t[0].replace(/ /gu, BOSLUK + '+');
}).join('|') + ')(?![' + _HARF + '])', 'gu');

function kucult(s) {
  return Array.from(s).map(function (ch) {
    if (ch === 'I') return 'ı';
    if (ch === 'İ') return 'i';
    var l = ch.toLowerCase();
    return Array.from(l).length === 1 ? l : ch;
  }).join('');
}

function _grup(ifade_kucuk) {
  return _GRUP[ifade_kucuk.replace(new RegExp(BOSLUK + '+', 'gu'), ' ')] || 'beceri';
}

function belirsiz_bul(cumle) {
  var k = kucult(cumle);
  var aralik = [];
  var m;
  _DESEN.lastIndex = 0;
  while ((m = _DESEN.exec(k)) !== null) aralik.push([m.index, m.index + m[0].length]);
  return aralik;
}

function uret(cumle, kalite, guven) {
  if (kalite === 'BELIRSIZ') {
    var aralik = belirsiz_bul(cumle);
    if (!aralik.length) return [[], 'Cümledeki eylem dışarıdan gözlenip ölçülemiyor; "açıklar", "uygular" ya da "karşılaştırır" gibi bir fiil deneyin.'];
    var ifade = cumle.slice(aralik[0][0], aralik[0][1]);
    var oneri = ONERI[_grup(kucult(ifade))];
    return [aralik.map(function (a) { return { bas: a[0], son: a[1] }; }),
      '"' + ifade + '" ölçülemez; "' + oneri[0] + '" ya da "' + oneri[1] + '" gibi bir fiil deneyin.'];
  }
  if (kalite === 'CIKTI_DEGIL') return [[], 'Cümlede öğrencinin yapacağı bir eylem yok; konu başlığı gibi yazılmış.'];
  if (kalite === 'INGILIZCE') return [[], 'İngilizce cümleler değerlendirilmiyor.'];
  if (guven !== undefined && guven !== null && guven < 0.6) return [[], 'Model bu cümlede emin değil; sonucu kendiniz de değerlendirin.'];
  return [[], null];
}

function degerlendir(cumleler) {
  var ozet = { toplam: cumleler.length, duzgun: 0, belirsiz: 0, cikti_degil: 0, ingilizce: 0 };
  var alan = { DUZGUN: 'duzgun', BELIRSIZ: 'belirsiz', CIKTI_DEGIL: 'cikti_degil', INGILIZCE: 'ingilizce' };
  var sonuclar = cumleler.map(function (c) {
    var kalite = ing(c) ? 'INGILIZCE' : kural(c);
    var oneri = uret(c, kalite, null);
    ozet[alan[kalite]] += 1;
    return { cumle: c, kalite: kalite, guven: null, bloom: null, bloom_guven: null, vurgular: oneri[0], not: oneri[1] };
  });
  return { ozet: ozet, sonuclar: sonuclar };
}

function hazirla(metin) {
  var kenar = new RegExp('^' + BOSLUK + '+|' + BOSLUK + '+$', 'gu');
  var cumleler = metin.split(/\r\n|[\n\r\v\f\x1c-\x1e\x85\u2028\u2029]/u).map(function (s) {
    return s.replace(kenar, '');
  }).filter(function (s) { return s.length > 0; }).map(function (s) {
    return Array.from(s).slice(0, 1000).join('');
  });
  return { cumleler: cumleler, hata: !cumleler.length ? 'Cümle bulunamadı.' :
    cumleler.length > 200 ? 'En çok 200 cümle gönderilebilir.' : null };
}

var api = { low: low, kural: kural, ing: ing, kucult: kucult, _grup: _grup,
  belirsiz_bul: belirsiz_bul, uret: uret, degerlendir: degerlendir, hazirla: hazirla };
if (typeof window !== 'undefined') window.CiktiKontrol = api;
if (typeof module !== 'undefined') module.exports = api;
})();
