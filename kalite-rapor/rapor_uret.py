"""rapor.md + analiz/sayilar.json -> Vize-Raporu.docx ve Vize-Raporu.pdf
Kullanım: py -3 rapor_uret.py   (kalite-rapor klasöründen)
Önce analiz betiğini çalıştırın; sayılar sayilar.json'dan doldurulur.
"""
import csv, html, json, os, re, subprocess, sys
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

sys.stdout.reconfigure(encoding="utf-8")
D = os.path.dirname(os.path.abspath(__file__))
S = json.load(open(os.path.join(D, "analiz", "sayilar.json"), encoding="utf-8"))


def n(x):
    return f"{x:,}".replace(",", ".")


def d(x, k=1):
    return f"{x:.{k}f}".replace(".", ",")


def tl(s):
    low = lambda x: x.replace("I", "ı").replace("İ", "i").lower()
    return " ".join(low(w) if low(w) == "ve" else w[:1] + low(w[1:]) for w in s.split())


oq = S["ornek_kalite"]
T = {}
T["cumle"] = n(S["cumle"])
T["cumle_kisa"] = n(S["cumle"])
for k in ("toplanan_ders", "bos_ders", "ders_ciktili", "birim", "program_birimi", "ingilizce", "kelime_3_ve_alti",
          "ders_ici_tekrarli_ders"):
    T[k] = n(S[k])
T["ders_ici_tekrar"] = n(S["ders_ici_tekrar_satiri"])
T["lisans_cumle"] = n(S["seviye_cumle"].get("Lisans", 0))
T["onlisans_cumle"] = n(S["seviye_cumle"].get("Ön Lisans", 0))
T["ders_basina_ort"] = d(S["ders_basina_cikti_ort"])
T["ders_basina_medyan"] = str(S["ders_basina_cikti_medyan"])
T["kelime_ort"] = d(S["kelime_ort"])
T["cumle_tr"] = n(S["cumle"] - S["ingilizce"])
T["benzersiz"] = n(S["benzersiz_cumle"])
e, en = S["en_sik_tekrar"][0]
T["en_sik_tekrar"] = e[:1].upper() + e[1:] + "."
T["en_sik_tekrar_n"] = str(en)
sk = dict(S["en_sik_son_kelime"])
for key, w in (("v_aciklar", "açıklar"), ("v_bilir", "bilir"), ("v_ogrenir", "öğrenir"), ("v_kavrar", "kavrar")):
    T[key] = n(sk.get(w, 0))
orn = [r for r in csv.DictReader(open(os.path.join(D, "etiket", "ornekleme_ani_veri.csv"), encoding="utf-8-sig")) if r["cumle"].strip()]
T["ornekleme_cumle"] = n(len(orn))
for key, cl in (("duzgun", "DUZGUN"), ("belirsiz", "BELIRSIZ"), ("cikti", "CIKTI_DEGIL")):
    c, p, lo, hi = oq[cl]
    T["n_" + key] = str(c); T["p_" + key] = d(p); T["ci_" + key] = f"{d(lo)}–{d(hi)}"
T["p_sorunlu"] = d(oq["BELIRSIZ"][1] + oq["CIKTI_DEGIL"][1])
sv = S["ornek_seviye_kalite"]
T["p_bel_lisans"] = d(100 * sv["Lisans"].get("BELIRSIZ", 0) / sum(sv["Lisans"].values()))
T["p_bel_onlisans"] = d(100 * sv["Ön Lisans"].get("BELIRSIZ", 0) / sum(sv["Ön Lisans"].values()))
ob = S["ornek_bloom"]
T["b_uygulama"], T["b_anlama"], T["b_degerlendirme"] = str(ob["UYGULAMA"]), str(ob["ANLAMA"]), str(ob["DEGERLENDIRME"])
km = S["kural_karisiklik"]
ab = {"DUZGUN": "d", "BELIRSIZ": "b", "CIKTI_DEGIL": "c"}
for a in ab:
    for b in ab:
        T[f"k_{ab[a]}{ab[b]}"] = str(km.get(a, {}).get(b, 0))
f1 = S["kural_f1"]
T["f1_d"], T["f1_b"], T["f1_c"] = d(f1["DUZGUN"], 2), d(f1["BELIRSIZ"], 2), d(f1["CIKTI_DEGIL"], 2)
T["kural_macro_f1"] = d(S["kural_macro_f1"], 2)
T["kural_dogruluk"] = d(S["kural_dogruluk"])
T["kural_bel_orani"] = d(100 * sum(km[a].get("BELIRSIZ", 0) for a in km) / 300)
bl = S["birim_belirsiz_kural"]
ad = lambda s: "Rektörlüğe bağlı ortak seçmeli ders havuzu" if s.strip().upper() == "REKTÖRLÜK" else tl(s)
T["birim_max_ad"], T["birim_max"] = ad(bl[0][0]), d(bl[0][1], 0)
T["birim_min_ad"], T["birim_min"] = ad(bl[-1][0]), d(bl[-1][1], 0)

DL = json.load(open(os.path.join(D, "analiz", "doluluk.json"), encoding="utf-8"))
T["dl_incelenen"] = n(DL["incelenen"])
for key in ("tamamen_bos", "ciktisiz", "hocasiz", "konusuz"):
    T["dl_" + key] = n(DL[key]); T["dl_p_" + key] = d(100 * DL[key] / DL["incelenen"])
T["dl_p_lisans"] = d(DL["ciktisiz_lisans_yuzde"]); T["dl_p_onlisans"] = d(DL["ciktisiz_onlisans_yuzde"])
bm = DL["birim_ciktisiz"][0]
T["dl_birim_max_ad"] = "Rektörlüğe bağlı ortak seçmeli ders havuzu" if bm[0].strip().upper() == "REKTÖRLÜK" else tl(bm[0])
T["dl_birim_max"] = d(bm[1], 0)

md = open(os.path.join(D, "rapor.md"), encoding="utf-8").read()
eksik = sorted(set(re.findall(r"\{\{(\w+)\}\}", md)) - set(T))
if eksik:
    sys.exit("Doldurulamayan alanlar: " + ", ".join(eksik))
md = re.sub(r"\{\{(\w+)\}\}", lambda m: T[m.group(1)], md)
open(os.path.join(D, "rapor_dolu.md"), "w", encoding="utf-8").write(md)

# ---------- ayrıştırma ----------
blocks = []
lines = md.splitlines()
i = 0
meta = []
while i < len(lines):
    L = lines[i]
    if L.startswith("% "):
        meta.append(L[2:]); i += 1; continue
    if not L.strip():
        i += 1; continue
    if L.startswith("## "):
        blocks.append(("h1", L[3:])); i += 1; continue
    if L.startswith("### "):
        blocks.append(("h2", L[4:])); i += 1; continue
    m = re.match(r"!\[(.*?)\]\((.*?)\)", L)
    if m:
        blocks.append(("img", m.group(1), m.group(2))); i += 1; continue
    if L.startswith("|"):
        rows = []
        while i < len(lines) and lines[i].startswith("|"):
            cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
            if not all(re.fullmatch(r"-+", c) for c in cells):
                rows.append(cells)
            i += 1
        blocks.append(("table", rows)); continue
    if re.match(r"^(- |\d+\. )", L):
        items = []
        num = bool(re.match(r"^\d+\. ", L))
        while i < len(lines) and re.match(r"^(- |\d+\. )", lines[i]):
            items.append(re.sub(r"^(- |\d+\. )", "", lines[i])); i += 1
        blocks.append(("list", num, items)); continue
    para = [L]; i += 1
    while i < len(lines) and lines[i].strip() and not re.match(r"^(#|\||!\[|- |\d+\. |% )", lines[i]):
        para.append(lines[i]); i += 1
    blocks.append(("p", " ".join(para)))

INLINE = re.compile(r"(\*\*.+?\*\*|\*.+?\*)")


def runs(par, text, size=None, bold=False, italic=False):
    for part in INLINE.split(text):
        if not part:
            continue
        b, it = bold, italic
        if part.startswith("**"):
            part, b = part[2:-2], True
        elif part.startswith("*"):
            part, it = part[1:-1], True
        r = par.add_run(part); r.bold = b; r.italic = it
        if size:
            r.font.size = Pt(size)


# ---------- Word ----------
doc = Document()
sec = doc.sections[0]
sec.page_height, sec.page_width = Cm(29.7), Cm(21.0)
for side in ("left_margin", "right_margin"):
    setattr(sec, side, Cm(2.3))
sec.top_margin = sec.bottom_margin = Cm(2.2)
st = doc.styles["Normal"]
st.font.name = "Times New Roman"; st.font.size = Pt(11)
st.element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
st.paragraph_format.space_after = Pt(5)
st.paragraph_format.line_spacing = 1.15
for hn, sz in (("Heading 1", 13), ("Heading 2", 11.5)):
    h = doc.styles[hn]; h.font.name = "Times New Roman"; h.font.size = Pt(sz); h.font.bold = True
    h.font.color.rgb = RGBColor(0, 0, 0); h.element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    h.paragraph_format.space_before = Pt(10); h.paragraph_format.space_after = Pt(4)
    h.paragraph_format.keep_with_next = True

p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
runs(p, meta[0], size=15, bold=True)
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; runs(p, meta[1], size=11.5)
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; runs(p, meta[2], size=10, italic=True)

in_ref = False
for b in blocks:
    k = b[0]
    if k == "h1":
        doc.add_heading(b[1], level=1); in_ref = b[1].startswith("Kaynakça")
    elif k == "h2":
        doc.add_heading(b[1], level=2)
    elif k == "p":
        t = b[1]
        par = doc.add_paragraph()
        if re.match(r"^Tablo \d+\.", t):
            par.paragraph_format.keep_with_next = True; par.paragraph_format.space_before = Pt(6)
            runs(par, t, size=10, bold=False, italic=True)
        elif in_ref:
            par.paragraph_format.left_indent = Cm(1); par.paragraph_format.first_line_indent = Cm(-1)
            par.paragraph_format.space_after = Pt(3); runs(par, t, size=10)
        else:
            par.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY; runs(par, t)
    elif k == "list":
        for it in b[2]:
            par = doc.add_paragraph(style="List Number" if b[1] else "List Bullet")
            par.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY; runs(par, it)
    elif k == "img":
        par = doc.add_paragraph(); par.alignment = WD_ALIGN_PARAGRAPH.CENTER
        par.paragraph_format.keep_with_next = True
        par.add_run().add_picture(os.path.join(D, b[2]), width=Cm(12.5))
        cap = doc.add_paragraph(); cap.alignment = WD_ALIGN_PARAGRAPH.CENTER; runs(cap, b[1], size=10, italic=True)
    elif k == "table":
        rows = b[1]
        tb = doc.add_table(rows=len(rows), cols=len(rows[0])); tb.style = "Table Grid"; tb.alignment = WD_TABLE_ALIGNMENT.CENTER
        for ri, row in enumerate(rows):
            for ci, cell in enumerate(row):
                c = tb.cell(ri, ci); c.text = ""
                pp = c.paragraphs[0]; pp.paragraph_format.space_after = Pt(0)
                runs(pp, cell, size=9, bold=(ri == 0))
        doc.add_paragraph().paragraph_format.space_after = Pt(2)
out_docx = os.path.join(D, "Vize-Raporu.docx")
doc.save(out_docx)

# ---------- HTML -> PDF ----------
def inl(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"\*(.+?)\*", r"<i>\1</i>", t)
    return t

H = ["<!doctype html><html lang='tr'><head><meta charset='utf-8'><title>Vize Raporu</title><style>",
     "@page{size:A4;margin:22mm 23mm 22mm 23mm}body{font-family:'Times New Roman',serif;font-size:11pt;line-height:1.38;color:#000;background:#fff}",
     "h1.t{font-size:15pt;text-align:center;margin:0 0 6px}.au{text-align:center;margin:0}.inf{text-align:center;font-style:italic;font-size:10pt;margin:2px 0 14px}",
     "h2{font-size:13pt;margin:16px 0 5px;page-break-after:avoid}h3{font-size:11.5pt;margin:11px 0 4px;page-break-after:avoid}",
     "p{margin:0 0 6px;text-align:justify}ul,ol{margin:0 0 6px 18px;padding:0}li{text-align:justify;margin:2px 0}",
     "table{border-collapse:collapse;margin:3px auto 10px;font-size:9pt;page-break-inside:avoid}td,th{border:1px solid #444;padding:3px 5px;vertical-align:top}th{background:#eee}",
     ".cap{font-style:italic;font-size:10pt;text-align:left;margin:8px 0 2px;page-break-after:avoid}figure{margin:6px 0 10px;text-align:center;page-break-inside:avoid}",
     "figure img{width:72%}figcaption{font-style:italic;font-size:10pt}.ref{padding-left:1cm;text-indent:-1cm;font-size:10pt;text-align:left;margin-bottom:3px}",
     "</style></head><body>",
     f"<h1 class='t'>{inl(meta[0])}</h1><p class='au'>{inl(meta[1])}</p><p class='inf'>{inl(meta[2])}</p>"]
in_ref = False
for b in blocks:
    k = b[0]
    if k == "h1":
        H.append(f"<h2>{inl(b[1])}</h2>"); in_ref = b[1].startswith("Kaynakça")
    elif k == "h2":
        H.append(f"<h3>{inl(b[1])}</h3>")
    elif k == "p":
        cls = " class='cap'" if re.match(r"^Tablo \d+\.", b[1]) else (" class='ref'" if in_ref else "")
        H.append(f"<p{cls}>{inl(b[1])}</p>")
    elif k == "list":
        tg = "ol" if b[1] else "ul"
        H.append(f"<{tg}>" + "".join(f"<li>{inl(x)}</li>" for x in b[2]) + f"</{tg}>")
    elif k == "img":
        src = "file:///" + os.path.join(D, b[2]).replace("\\", "/")
        H.append(f"<figure><img src='{src}'><figcaption>{inl(b[1])}</figcaption></figure>")
    elif k == "table":
        rows = b[1]
        H.append("<table>" + "".join("<tr>" + "".join((f"<th>{inl(c)}</th>" if ri == 0 else f"<td>{inl(c)}</td>") for c in r) + "</tr>" for ri, r in enumerate(rows)) + "</table>")
H.append("</body></html>")
hp = os.path.join(D, "Vize-Raporu.html")
open(hp, "w", encoding="utf-8").write("".join(H))
pdf = os.path.join(D, "Vize-Raporu.pdf")
edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
subprocess.run([edge, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--allow-file-access-from-files",
                f"--print-to-pdf={pdf}", "file:///" + hp.replace("\\", "/")], check=False, capture_output=True)
print("docx:", out_docx); print("pdf:", pdf, os.path.exists(pdf))
