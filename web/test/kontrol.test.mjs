import { createRequire } from 'node:module';
import { readFileSync } from 'node:fs';
import { strict as assert } from 'node:assert';
import { isDeepStrictEqual } from 'node:util';

const require = createRequire(import.meta.url);
const kontrol = require('../public/kontrol.js');
const beklenen = JSON.parse(readFileSync(new URL('./beklenen.json', import.meta.url), 'utf8'));
let fark = 0;
beklenen.forEach(function (b, i) {
  const r = kontrol.degerlendir([b.cumle]).sonuclar[0];
  const sonuc = { cumle: r.cumle, kalite: r.kalite, vurgular: r.vurgular, not: r.not };
  if (!isDeepStrictEqual(sonuc, b)) {
    fark += 1;
    if (fark <= 20) console.error(JSON.stringify({ satir: i + 1, beklenen: b, sonuc: sonuc }, null, 2));
  }
});

assert.deepEqual(kontrol.hazirla(' \n\t'), { cumleler: [], hata: 'Cümle bulunamadı.' });
assert.equal(kontrol.hazirla(Array(201).fill('Cümle.').join('\n')).hata, 'En çok 200 cümle gönderilebilir.');
assert.deepEqual(kontrol.hazirla('a'.repeat(1200)), { cumleler: ['a'.repeat(1000)], hata: null });
assert.deepEqual(kontrol.hazirla('  İlk cümle. \r\n\n İkinci cümle.\t'), {
  cumleler: ['İlk cümle.', 'İkinci cümle.'], hata: null
});
console.log('hazirla: 4/4');
// Python'un ham konumlarını yukarıdaki karşılaştırmada değiştirmiyoruz.
// Tarayıcı sözleşmesi, emoji sonrasındaki aralığın UTF-16 ile dilimlenmesini ister.
const emoji = '😀 Konu hakkında bilgi sahibi olur.';
const vurgu = kontrol.degerlendir([emoji]).sonuclar[0].vurgular[0];
assert.deepEqual(vurgu, { bas: 17, son: 34 });
assert.equal(emoji.slice(vurgu.bas, vurgu.son), 'bilgi sahibi olur');
assert.equal(kontrol.kural('bılgı sahıbı olur.'), 'BELIRSIZ');
assert.equal(kontrol.ing('étheé'), false);
assert.equal(kontrol.ing('²and²'), false);
assert.equal(kontrol.ing('deſcribe'), true);
const toplu = kontrol.degerlendir(['Çözer.', 'Öğrenir.', 'SQL', 'The system.', 'Öğrenir.']);
assert.deepEqual(toplu.ozet, { toplam: 5, duzgun: 1, belirsiz: 2, cikti_degil: 1, ingilizce: 1 });
toplu.sonuclar.forEach(function (s) {
  assert.equal(s.guven, null);
  assert.equal(s.bloom, null);
  assert.equal(s.bloom_guven, null);
});
console.log('UTF-16, Unicode ve sonuç sözleşmesi: başarılı');
console.log((beklenen.length - fark) + '/' + beklenen.length);
if (fark) process.exitCode = 1;
