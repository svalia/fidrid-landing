"""
Печатает PDF юридических документов из тех же markdown-исходников, что и сайт.

Markdown переводится в HTML тем же кодом, что в legal.py, поэтому текст PDF
совпадает со страницей на сайте. Печать - через Google Chrome в фоновом режиме;
вид повторяет первые PDF, сделанные в wkhtmltopdf.

Запуск из корня репозитория лендинга, по базовым именам документов:
    python3 tools/legal_pdf.py Privacy_Policy Consent_to_Personal_Data_Processing
Файлы _Ru.pdf и _En.pdf пишутся в legal/.
"""
import importlib.util, os, re, subprocess, sys, html as H

sys.dont_write_bytecode = True  # не оставлять __pycache__ после импорта legal.py
LANDING = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("legal", os.path.join(LANDING, "tools", "legal.py"))
legal = importlib.util.module_from_spec(spec); spec.loader.exec_module(legal)

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
CSS = """
@page { size: A4; margin: 14mm 15mm 16mm 15mm; }
body { font-family: "DejaVu Sans", "Helvetica Neue", Arial, sans-serif; color: #1a1a1a;
       font-size: 7.9pt; line-height: 1.6; }
h1 { font-size: 14.5pt; margin: 0 0 5px; }
.edition { color: #777; font-size: 7pt; margin: 0 0 10px; }
hr.top { border: 0; border-top: 1.3px solid #222; margin: 0 0 14px; }
h2 { font-size: 9.6pt; margin: 16px 0 7px; page-break-after: avoid; }
p { text-align: justify; margin: 0 0 7px; }
ul { margin: 0 0 7px 0; padding-left: 16px; } li { margin: 0 0 3px; text-align: justify; }
a { color: inherit; text-decoration: none; }
table { width: 100%; border-collapse: collapse; table-layout: fixed; margin: 5px 0 10px;
        font-size: 6.6pt; page-break-inside: auto; }
th, td { border: 1px solid #dcdde2; padding: 5px 6px; vertical-align: top; text-align: left; }
th { background: #f3f4f6; font-weight: 700; }
tr { page-break-inside: avoid; }
"""

def build(base, lang, out_pdf):
    src = open(os.path.join(legal.SOURCES, f"{base}_{lang}.md"), encoding="utf-8").read()
    lines = src.split("\n")
    title = lines[0].lstrip("# ").strip()
    edition = re.sub(r"^\*\*(.*)\*\*$", r"\1", lines[2].strip())
    body = legal.markdown_to_html("\n".join(lines[3:]))
    doc = f"""<!doctype html><html lang="{lang.lower()}"><head><meta charset="utf-8">
<title>{H.escape(title)}</title><style>{CSS}</style></head><body>
<h1>{H.escape(title)}</h1><p class="edition">{H.escape(edition)}</p><hr class="top">
{body}</body></html>"""
    tmp = out_pdf.replace(".pdf", ".print.html")
    open(tmp, "w", encoding="utf-8").write(doc)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={out_pdf}", "file://" + tmp],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(tmp)

if __name__ == "__main__":
    out_dir = os.path.join(LANDING, "legal")
    for base in sys.argv[1:]:
        for lang in ("Ru", "En"):
            out = os.path.join(out_dir, f"{base}_{lang}.pdf")
            build(base, lang, out)
            print("PDF:", os.path.basename(out))
