# Kural tabanlı vurgu ve not üretimi (model kullanmaz).
import re

_B = "açıklar"
# Öneri fiilleri (ifade grubuna göre)
ONERI = {
    "bilgi": ("açıklar", "karşılaştırır"),
    "kavra": ("örnekle açıklar", "uygular"),
    "ogren": ("uygular", "açıklar"),
    "bilir": ("tanımlar", "listeler"),
    "farkinda": ("örnek verir", "tartışır"),
    "beceri": ("uygular", "gösterir"),
}

# Fiil biçimi eki: (gövde, [ekler]) -> gövde + ek
_OL = ["olur", "olunur", "olurlar", "olabilir", "olabilirler", "olmak", "olma"]
_EDIN = ["edinir", "edinirler", "edinebilir", "edinebilirler", "edinmek", "edinme"]
_KAZAN = ["kazanır", "kazanırlar", "kazanabilir", "kazanabilirler", "kazanmak", "kazanma"]
_EDER = ["eder", "ederler", "edebilir", "edebilirler", "etmek", "etme"]
_SAGLA = ["sağlar", "sağlarlar", "sağlayabilir", "sağlayabilirler", "sağlamak", "sağlama"]

# (kalıp sözcükleri, grup) ; kalıp sonunda fiil biçimleri eklenir
_TANIM = []
for onek in ("bilgi sahibi", "fikir sahibi"):
    _TANIM += [(onek + " " + f, "bilgi") for f in _OL]
for onek in ("hakkında bilgi", "bilgi"):
    _TANIM += [(onek + " " + f, "bilgi") for f in _EDIN]
_TANIM += [("bilgi " + f, "beceri") for f in _KAZAN]
_TANIM += [("bilinç " + f, "farkinda") for f in _KAZAN]
_TANIM += [("farkındalık " + f, "farkinda") for f in _KAZAN]
_TANIM += [("beceri " + f, "beceri") for f in _KAZAN]
_TANIM += [("farkında " + f, "farkinda") for f in _OL]
_TANIM += [("takip " + f, "beceri") for f in _EDER]
for onek in ("hakimiyet", "hâkimiyet"):
    _TANIM += [(onek + " " + f, "beceri") for f in _SAGLA]
_TANIM += [(f, "beceri") for f in ("gelişir", "gelişirler", "gelişebilir", "gelişmek", "gelişme")]
_TANIM += [("öğren" + e, "ogren") for e in ("ir", "irler", "ebilir", "ebilirler", "mek", "me")]
_TANIM += [("an" + e, "kavra") for e in ("lar", "larlar", "layabilir", "layabilirler", "lamak", "lama")]
_TANIM += [("kavra" + e, "kavra") for e in ("r", "rlar", "yabilir", "yabilirler", "mak", "ma")]
_TANIM += [("bil" + e, "bilir") for e in ("ir", "irler", "ebilir", "ebilirler", "mek", "me")]
_TANIM += [("tan" + e, "bilir") for e in ("ır", "ırlar", "ıyabilir", "ıyabilirler", "ımak", "ıma")]
# not: "anlar" biçimi için "an"+"lar" kullanıldı; "anla" gövdesi: anlayabilir, anlamak, anlama

BELIRSIZ = sorted({k: g for k, g in _TANIM}.items(), key=lambda x: -len(x[0]))
_GRUP = {k: g for k, g in BELIRSIZ}

_HARF = "a-zçğıöşüâîû0-9_"
_DESEN = re.compile(
    r"(?<![" + _HARF + r"])(?:"
    + "|".join(re.escape(k).replace(r"\ ", r"\s+") for k, _ in BELIRSIZ)
    + r")(?![" + _HARF + r"])"
)


def kucult(s):
    """Türkçe küçük harf; uzunluğu değiştirmez (konumlar korunur)."""
    out = []
    for ch in s:
        if ch == "I":
            out.append("ı")
        elif ch == "İ":
            out.append("i")
        else:
            l = ch.lower()
            out.append(l if len(l) == 1 else ch)
    return "".join(out)


def _grup(ifade_kucuk):
    return _GRUP.get(re.sub(r"\s+", " ", ifade_kucuk), "beceri")


def belirsiz_bul(cumle):
    k = kucult(cumle)
    return [(m.start(), m.end()) for m in _DESEN.finditer(k)]


def uret(cumle, kalite, guven=None):
    """-> (vurgular, not)"""
    if kalite == "BELIRSIZ":
        aralik = belirsiz_bul(cumle)
        if not aralik:
            return [], 'Cümledeki eylem dışarıdan gözlenip ölçülemiyor; "açıklar", "uygular" ya da "karşılaştırır" gibi bir fiil deneyin.'
        bas, son = aralik[0]
        o1, o2 = ONERI[_grup(kucult(cumle[bas:son]))]
        metin = '"%s" ölçülemez; "%s" ya da "%s" gibi bir fiil deneyin.' % (cumle[bas:son], o1, o2)
        return [{"bas": b, "son": s} for b, s in aralik], metin
    if kalite == "CIKTI_DEGIL":
        return [], "Cümlede öğrencinin yapacağı bir eylem yok; konu başlığı gibi yazılmış."
    if kalite == "INGILIZCE":
        return [], "İngilizce cümleler değerlendirilmiyor."
    if guven is not None and guven < 0.6:
        return [], "Model bu cümlede emin değil; sonucu kendiniz de değerlendirin."
    return [], None
