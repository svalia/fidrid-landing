"""
Собирает HTML-страницы юридических документов из markdown-исходников.

Исходники лежат в Legal/_sources рядом с PDF: править markdown проще, чем PDF,
а App Store Connect и поисковики читают HTML охотнее, чем скачиваемый файл.

Каждая страница содержит обе языковые версии сразу; какую показать, решает
legal.js по тому же правилу, что и лендинг, и по тому же ключу в localStorage,
так что выбор языка переносится между страницами.

Запуск из корня репозитория лендинга:
    python3 tools/legal.py
"""

import html
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCES = os.path.join(ROOT, 'legal', '_sources')

# slug страницы -> (файл без языкового суффикса, подпись в футере лендинга)
DOCUMENTS = {
    'terms': ('Terms_of_Use', 'Условия использования', 'Terms of Use'),
    'privacy': ('Privacy_Policy', 'Политика конфиденциальности', 'Privacy Policy'),
    'consent': ('Consent_to_Personal_Data_Processing',
                'Обработка персональных данных', 'Personal Data Processing'),
}

SUPPORT_EMAIL = 'taxers.59botanic@icloud.com'


def inline(text):
    """Жирный текст, почта и экранирование. Ссылок и кода в исходниках нет."""
    text = html.escape(text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(
        r'([\w.%-]+@[\w.-]+\.[A-Za-z]{2,})',
        r'<a href="mailto:\1">\1</a>',
        text,
    )
    return text


def render_table(rows):
    """Первая строка - шапка, вторая - разделитель выравнивания, дальше данные."""
    cells = [[c.strip() for c in row.strip().strip('|').split('|')] for row in rows]
    head, body = cells[0], cells[2:]
    out = ['<div class="table-scroll"><table>', '<thead><tr>']
    out += ['<th>%s</th>' % inline(c) for c in head]
    out.append('</tr></thead><tbody>')
    for row in body:
        out.append('<tr>' + ''.join('<td>%s</td>' % inline(c) for c in row) + '</tr>')
    out.append('</tbody></table></div>')
    return '\n'.join(out)


def markdown_to_html(text):
    lines = text.split('\n')
    out, i = [], 0

    while i < len(lines):
        line = lines[i].rstrip()

        if not line:
            i += 1
            continue

        heading = re.match(r'^(#{1,4})\s+(.*)$', line)
        if heading:
            level = len(heading.group(1))
            out.append('<h%d>%s</h%d>' % (level, inline(heading.group(2)), level))
            i += 1
            continue

        if line.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].startswith('|'):
                rows.append(lines[i])
                i += 1
            if len(rows) >= 2:
                out.append(render_table(rows))
            continue

        if line.startswith('- '):
            items = []
            while i < len(lines) and lines[i].startswith('- '):
                items.append('<li>%s</li>' % inline(lines[i][2:].strip()))
                i += 1
            out.append('<ul>\n' + '\n'.join(items) + '\n</ul>')
            continue

        # абзац: собираем до пустой строки или до начала другого блока
        paragraph = []
        while i < len(lines):
            current = lines[i].rstrip()
            if not current or current.startswith(('#', '|', '- ')):
                break
            paragraph.append(current)
            i += 1
        out.append('<p>%s</p>' % inline(' '.join(paragraph)))

    return '\n'.join(out)


def tab_title(title):
    """Названия документов уже содержат «FidRid», второй раз его не добавляем."""
    return title if 'FidRid' in title else '%s - FidRid' % title


def read_document(base, lang):
    path = os.path.join(SOURCES, '%s_%s.md' % (base, 'Ru' if lang == 'ru' else 'En'))
    with open(path, encoding='utf-8') as f:
        text = f.read()
    title = re.search(r'^#\s+(.*)$', text, re.M)
    return title.group(1).strip() if title else base, markdown_to_html(text)


PAGE = '''<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{tab_ru}</title>
<script>window.__fidridTitles = {{ ru: "{tab_ru}", en: "{tab_en}" }};</script>
<meta name="description" content="{title_ru}">
<meta name="theme-color" content="#05101E">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://svalia.github.io/fidrid-landing/legal/{slug}/">
<link rel="icon" type="image/svg+xml" href="../../assets/favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="../../assets/favicon-32.png">
<link rel="apple-touch-icon" sizes="180x180" href="../../assets/apple-touch-icon.png">

<script>
// Выбор языка до первой отрисовки, ключ общий с лендингом
(function () {{
  var saved = null;
  try {{ saved = localStorage.getItem('fidrid-lang'); }} catch (e) {{}}
  if (saved !== 'ru' && saved !== 'en') saved = null;
  var nav = (navigator.languages && navigator.languages[0]) || navigator.language || 'ru';
  window.__fidridLang = saved || (/^ru/i.test(nav) ? 'ru' : 'en');
  document.documentElement.lang = window.__fidridLang;
}})();
</script>

<link rel="stylesheet" href="../../css/golos-embed.css">
<link rel="stylesheet" href="../../css/tokens/colors.css">
<link rel="stylesheet" href="../../css/tokens/typography.css">
<link rel="stylesheet" href="../../css/tokens/layout.css">
<link rel="stylesheet" href="../legal.css">
</head>
<body>

<header>
  <a class="brand" href="../../">
    <img src="../../assets/favicon.svg" alt="" width="32" height="32">
    <span>FidRid</span>
  </a>
  <nav>
    <a class="back" href="../../" data-t="back">На главную</a>
    <button type="button" id="lang-toggle" data-nolang="1">EN</button>
  </nav>
</header>

<main>
  <article data-lang="ru">
{body_ru}
  </article>
  <article data-lang="en" hidden>
{body_en}
  </article>

  <p class="download">
    <a id="pdf-link" href="../{base}_Ru.pdf" target="_blank" rel="noopener" data-t="pdf">
      Скачать PDF
    </a>
  </p>
</main>

<footer>
  <span data-t="disclaimer">FidRid — неофициальный клиент Telegram, не связанный с Telegram LLC.</span>
  <a href="mailto:{email}">{email}</a>
</footer>

<script src="../legal.js"></script>
</body>
</html>
'''


def main():
    for slug, (base, _, _) in DOCUMENTS.items():
        title_ru, body_ru = read_document(base, 'ru')
        title_en, body_en = read_document(base, 'en')

        out_dir = os.path.join(ROOT, 'legal', slug)
        os.makedirs(out_dir, exist_ok=True)

        page = PAGE.format(
            tab_ru=html.escape(tab_title(title_ru)),
            tab_en=html.escape(tab_title(title_en)),
            slug=slug,
            base=base,
            title_ru=html.escape(title_ru),
            title_en=html.escape(title_en),
            body_ru=body_ru,
            body_en=body_en,
            email=SUPPORT_EMAIL,
        )
        with open(os.path.join(out_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(page)
        print('legal/%s/index.html: %d байт' % (slug, len(page)))


if __name__ == '__main__':
    main()
