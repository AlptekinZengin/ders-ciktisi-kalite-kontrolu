"""anlatim/*.md -> Proje-Durum-Raporu.pdf (lise diliyle anlatım). Kullanım: py -3 pdf_yap.py"""
import html, os, re, subprocess, sys

sys.stdout.reconfigure(encoding="utf-8")
D = os.path.dirname(os.path.abspath(__file__))
parts = [open(os.path.join(D, f), encoding="utf-8").read() for f in ("giris.md", "bolum1.md", "bolum2-3.md")]
md = "\n\n".join(parts)


def inl(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", t)
    t = re.sub(r"`(.+?)`", r"<code>\1</code>", t)
    return t


out, lines, i = [], md.splitlines(), 0
while i < len(lines):
    L = lines[i]
    if not L.strip() or L.strip() == "---":
        i += 1; continue
    m = re.match(r"^(#{1,4})\s+(.*)", L)
    if m:
        lv = len(m.group(1)); out.append(f"<h{lv}>{inl(m.group(2))}</h{lv}>"); i += 1; continue
    if L.startswith(">"):
        buf = []
        while i < len(lines) and lines[i].startswith(">"):
            buf.append(lines[i].lstrip("> ").rstrip()); i += 1
        out.append("<div class='box'>" + "<br>".join(inl(b) for b in buf if b) + "</div>"); continue
    if L.startswith("|"):
        rows = []
        while i < len(lines) and lines[i].startswith("|"):
            c = [x.strip() for x in lines[i].strip().strip("|").split("|")]
            if not all(re.fullmatch(r":?-+:?", x) for x in c):
                rows.append(c)
            i += 1
        out.append("<table>" + "".join("<tr>" + "".join((f"<th>{inl(x)}</th>" if r == 0 else f"<td>{inl(x)}</td>") for x in row) + "</tr>" for r, row in enumerate(rows)) + "</table>")
        continue
    if re.match(r"^\s*([-*] |\d+\. )", L):
        num = bool(re.match(r"^\s*\d+\. ", L)); items = []
        while i < len(lines) and re.match(r"^\s*([-*] |\d+\. )", lines[i]):
            ind = len(lines[i]) - len(lines[i].lstrip())
            items.append((ind, re.sub(r"^\s*([-*] |\d+\. )", "", lines[i]))); i += 1
        tg = "ol" if num else "ul"
        h = f"<{tg}>"
        for ind, it in items:
            h += f"<li{' class=sub' if ind >= 2 else ''}>{inl(it)}</li>"
        out.append(h + f"</{tg}>"); continue
    buf = [L]; i += 1
    while i < len(lines) and lines[i].strip() and not re.match(r"^(#|>|\||\s*[-*] |\s*\d+\. |---)", lines[i]):
        buf.append(lines[i]); i += 1
    out.append(f"<p>{inl(' '.join(buf))}</p>")

css = """@page{size:A4;margin:17mm 17mm 18mm 17mm}
body{font-family:'Segoe UI',Calibri,Arial,sans-serif;font-size:10.8pt;line-height:1.55;color:#1d2433;background:#fff;margin:0}
h1{font-size:21pt;color:#2f6fdb;margin:0 0 4px}h2{font-size:15pt;margin:22px 0 8px;padding-bottom:4px;border-bottom:2px solid #e8f0fd;page-break-after:avoid}
h3{font-size:12pt;margin:14px 0 5px;page-break-after:avoid}h4{font-size:11pt;margin:10px 0 4px}
p{margin:5px 0 8px}ul,ol{margin:4px 0 8px 20px;padding:0}li{margin:3px 0}li.sub{margin-left:18px;list-style:circle}
.box{background:#e8f0fd;border-left:4px solid #2f6fdb;border-radius:6px;padding:8px 12px;margin:8px 0 10px;page-break-inside:avoid}
table{width:100%;border-collapse:collapse;margin:8px 0 12px;font-size:9.6pt;page-break-inside:avoid}th,td{border:1px solid #d9dee7;padding:5px 7px;text-align:left;vertical-align:top}th{background:#f3f5f9}
code{background:#f3f5f9;padding:0 3px;border-radius:3px;font-size:9.5pt}"""
page = f"<!doctype html><html lang='tr'><head><meta charset='utf-8'><title>Proje Durum Raporu</title><style>{css}</style></head><body>{''.join(out)}</body></html>"
hp = os.path.join(D, "Proje-Durum-Raporu.html")
open(hp, "w", encoding="utf-8").write(page)
pdf = os.path.join(D, "Proje-Durum-Raporu.pdf")
subprocess.run([r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe", "--headless=new", "--disable-gpu",
                "--no-pdf-header-footer", f"--print-to-pdf={pdf}", "file:///" + hp.replace("\\", "/")], capture_output=True)
print(pdf, os.path.exists(pdf))
