"""
Собирает index.html, i18n.js и responsive.css из запечённого макета.

На вход идёт результат tools/bake.mjs - снятый из браузера DOM артефакта
Claude Design. Здесь он превращается в готовую страницу: голова с мета-тегами
и выбором языка, тело без рантайма, словарь для английской версии и адаптив.

Запуск из корня репозитория:
    node tools/bake.mjs "file://$PWD/source/FidRid Landing.dc.html" build/baked-raw.html
    python3 tools/assemble.py [путь-к-baked-raw.html]
"""

import re, os, json, html, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'build', 'baked-raw.html')
OUT = ROOT

# Дизайн-система приехала из макета в папке с длинным служебным именем;
# в репозитории она лежит как css/, поэтому ссылки переписываются на неё.
DS = 'css'

raw = open(SRC, encoding='utf-8').read()

# --- 1. DICT из дизайн-скрипта ---
m = re.search(r'const DICT = \{(.*?)\n\};', raw, re.S)
assert m, 'DICT не найден'
dict_body = m.group(1)

# --- 2. Тело: содержимое #dc-root ---
i = raw.find('<div id="dc-root">')
j = raw.rfind('<script type="text/x-dc"')
assert i > 0 and j > i, 'не нашёл границы контента'
body = raw[i:j].rstrip()
# отрезаем хвост после закрытия dc-root
k = body.rfind('</div>')
body = body[:k+6]

# --- 3. hover-стили (.scp*) и авторские стили из helmet ---
head_raw = raw[:raw.find('<body')]
styles = re.findall(r'<style[^>]*>(.*?)</style>', head_raw, re.S)
hover_css = next((s.strip() for s in styles if '.scp' in s), '')
author_css = next((s.strip() for s in styles if 'fr-rise' in s), '')

os.makedirs(OUT, exist_ok=True)

# В разметке макета на месте документов стояли заглушки-якоря. Подменяем их
# страницами документов: язык там выбирается сам, поэтому ссылка одна на оба
# языка, а PDF предлагается уже внутри страницы.
SUPPORT_EMAIL = 'taxers.59botanic@icloud.com'
FOOTER_LINKS = {
    '#terms': 'legal/terms/',
    '#privacy': 'legal/privacy/',
    '#pdn': 'legal/consent/',
}
for anchor, path in FOOTER_LINKS.items():
    body = body.replace('href="%s"' % anchor, 'href="%s"' % path)

# Support URL в App Store Connect должен давать способ связаться, поэтому
# «Поддержка» ведёт на почту, а не на секцию с вопросами.
body = body.replace(
    '<a data-dc-tpl="300" href="#faq">Поддержка</a>',
    '<a data-dc-tpl="300" href="mailto:%s">Поддержка</a>' % SUPPORT_EMAIL)

TITLE_RU = 'FidRid — каналы в ленту'
TITLE_EN = 'FidRid — channels into a feed'
DESC_RU = ('FidRid забирает телеграм-каналы в отдельную ленту со сторис, фильтрами и своими '
           'статусами прочтения. В телеграме остаётся личка. iPhone, бесплатно, без рекламы.')
DESC_EN = ('FidRid moves your Telegram channels into a separate feed with stories, filters and its own '
           'read states. Telegram keeps the private chats. iPhone, free, no ads.')

head = f'''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{TITLE_RU}</title>
<meta name="description" content="{DESC_RU}">
<meta name="theme-color" content="#05101E">
<link rel="canonical" href="https://svalia.github.io/fidrid-landing/">
<link rel="icon" type="image/svg+xml" href="assets/favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="assets/favicon-32.png">
<link rel="apple-touch-icon" sizes="180x180" href="assets/apple-touch-icon.png">

<meta property="og:type" content="website">
<meta property="og:site_name" content="FidRid">
<meta property="og:locale" content="ru_RU">
<meta property="og:locale:alternate" content="en_US">
<meta property="og:title" content="{TITLE_RU}">
<meta property="og:description" content="{DESC_RU}">
<meta property="og:url" content="https://svalia.github.io/fidrid-landing/">
<meta property="og:image" content="https://svalia.github.io/fidrid-landing/assets/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{TITLE_RU}">
<meta name="twitter:description" content="{DESC_RU}">
<meta name="twitter:image" content="https://svalia.github.io/fidrid-landing/assets/og-image.png">

<script>
// Выбор языка до первой отрисовки: сохранённый выбор -> язык браузера -> ru
(function () {{
  var saved = null;
  try {{ saved = localStorage.getItem('fidrid-lang'); }} catch (e) {{}}
  if (saved !== 'ru' && saved !== 'en') saved = null;
  var nav = (navigator.languages && navigator.languages[0]) || navigator.language || 'ru';
  var lang = saved || (/^ru/i.test(nav) ? 'ru' : 'en');
  window.__fidridLang = lang;
  document.documentElement.lang = lang;
  if (lang === 'en') {{
    document.documentElement.className += ' lang-pending';
    // страховка: если i18n.js не загрузился, контент всё равно покажется
    setTimeout(function () {{
      document.documentElement.classList.remove('lang-pending');
    }}, 1200);
  }}
}})();
</script>
<style>html.lang-pending #dc-root {{ visibility: hidden; }}</style>

<link rel="stylesheet" href="{DS}/golos-embed.css">
<link rel="stylesheet" href="{DS}/tokens/colors.css">
<link rel="stylesheet" href="{DS}/tokens/typography.css">
<link rel="stylesheet" href="{DS}/tokens/effects.css">
<link rel="stylesheet" href="{DS}/tokens/layout.css">
<link rel="stylesheet" href="{DS}/base.css">
<link rel="stylesheet" href="{DS}/styles.css">
<link rel="stylesheet" href="responsive.css">
<style>
html, body {{ height: 100%; margin: 0; }}
#dc-root, #dc-root > .sc-host {{ height: 100%; }}
{author_css}
{hover_css}
</style>'''

doc = f'''<!DOCTYPE html>
<html lang="ru">
<head>
{head}
</head>
<body>
{body}
<script src="i18n.js"></script>
</body>
</html>
'''
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(doc)

# --- 4. i18n.js ---
i18n = '''/*
  Двуязычность лендинга FidRid (ru / en).

  Язык выбирается так: сохранённый выбор пользователя -> язык браузера -> русский.
  Первичный выбор делает короткий скрипт в <head>, чтобы страница не мигала
  русским текстом перед показом английского. Здесь выполняется сам перевод.

  Разметка написана по-русски, перевод подменяет текстовые узлы по словарю DICT.
  Узлы внутри [data-nolang] не трогаем (кнопка переключения языка).
*/
(function () {
  'use strict';

  var DICT = {''' + dict_body + '''
  };

  // Атрибуты и метаданные переводим отдельно: текстовым обходом их не достать
  var ATTR_DICT = {
    'QR-код на страницу приложения в App Store': 'App Store QR code'
  };

  var META = {
    ru: {
      title: ''' + json.dumps(TITLE_RU, ensure_ascii=False) + ''',
      description: ''' + json.dumps(DESC_RU, ensure_ascii=False) + ''',
      locale: 'ru_RU'
    },
    en: {
      title: ''' + json.dumps(TITLE_EN, ensure_ascii=False) + ''',
      description: ''' + json.dumps(DESC_EN, ensure_ascii=False) + ''',
      locale: 'en_US'
    }
  };

  var STORAGE_KEY = 'fidrid-lang';
  var root = document.getElementById('dc-root') || document.body;
  var originals = null;      // узел -> исходный русский текст
  var originalAttrs = null;  // [элемент, атрибут, исходное значение]
  var current = 'ru';

  function translateTextNodes() {
    originals = new Map();
    var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    var nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);

    for (var i = 0; i < nodes.length; i++) {
      var node = nodes[i];
      if (node.parentElement && node.parentElement.closest('[data-nolang]')) continue;
      var m = /^(\\s*)([\\s\\S]*?)(\\s*)$/.exec(node.nodeValue);
      if (!m || !m[2]) continue;
      var hit = DICT[m[2]];
      if (hit) {
        originals.set(node, node.nodeValue);
        node.nodeValue = m[1] + hit + m[3];
      }
    }
  }

  function translateAttributes() {
    originalAttrs = [];
    var attrs = ['alt', 'title', 'aria-label', 'placeholder'];
    var all = root.querySelectorAll('[alt], [title], [aria-label], [placeholder]');
    for (var i = 0; i < all.length; i++) {
      for (var a = 0; a < attrs.length; a++) {
        var name = attrs[a];
        var value = all[i].getAttribute(name);
        if (!value) continue;
        var hit = ATTR_DICT[value] || DICT[value];
        if (!hit) continue;
        originalAttrs.push([all[i], name, value]);
        all[i].setAttribute(name, hit);
      }
    }
  }

  function restore() {
    if (originals) {
      originals.forEach(function (text, node) { node.nodeValue = text; });
      originals = null;
    }
    if (originalAttrs) {
      for (var i = 0; i < originalAttrs.length; i++) {
        originalAttrs[i][0].setAttribute(originalAttrs[i][1], originalAttrs[i][2]);
      }
      originalAttrs = null;
    }
  }

  function applyMeta(lang) {
    var meta = META[lang];
    document.title = meta.title;
    setMeta('name', 'description', meta.description);
    setMeta('property', 'og:title', meta.title);
    setMeta('property', 'og:description', meta.description);
    setMeta('property', 'og:locale', meta.locale);
    setMeta('name', 'twitter:title', meta.title);
    setMeta('name', 'twitter:description', meta.description);
  }

  function setMeta(attr, key, value) {
    var el = document.head.querySelector('meta[' + attr + '="' + key + '"]');
    if (el) el.setAttribute('content', value);
  }

  function setLanguage(lang, remember) {
    if (lang !== 'ru' && lang !== 'en') lang = 'ru';
    current = lang;

    restore();
    if (lang === 'en') {
      translateTextNodes();
      translateAttributes();
    }

    document.documentElement.lang = lang;
    applyMeta(lang);
    updateButton();
    document.documentElement.classList.remove('lang-pending');

    if (remember) {
      try { localStorage.setItem(STORAGE_KEY, lang); } catch (e) {}
    }
  }

  function button() {
    return document.querySelector('[data-nolang]');
  }

  function updateButton() {
    var btn = button();
    if (!btn) return;
    // внутри кнопки лежит span с подписью, поставленный сборкой лендинга
    var label = btn.querySelector('span') || btn;
    label.textContent = current === 'ru' ? 'EN' : 'RU';
    btn.setAttribute('aria-label', current === 'ru' ? 'Switch to English' : 'Переключить на русский');
  }

  function init() {
    var btn = button();
    if (btn) {
      btn.addEventListener('click', function () {
        setLanguage(current === 'ru' ? 'en' : 'ru', true);
      });
    }
    setLanguage(window.__fidridLang || 'ru', false);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
'''
open(os.path.join(OUT, 'i18n.js'), 'w', encoding='utf-8').write(i18n)

# --- 5. responsive.css ---
# Лендинг собран из макета с инлайновыми стилями и без медиа-запросов.
# Переопределяем их снаружи: селекторы цепляются за содержимое атрибута style,
# потому что других зацепок в разметке нет.
responsive = '''/* Адаптив лендинга FidRid.

   Разметка пришла из макета с инлайновыми стилями и без медиа-запросов,
   поэтому правила ниже цепляются за содержимое атрибута style и перебивают
   инлайн через !important. Ширины подобраны по точкам, где ломается вёрстка:
   900px - двухколоночные секции перестают помещаться,
   720px - навигация в шапке наезжает на кнопки.
*/

/* Двухколоночные секции (герой и "Как это работает") складываются в одну */
@media (max-width: 900px) {
  [style*="grid-template-columns: minmax(0px, 1.05fr)"],
  [style*="grid-template-columns: minmax(0px, 1fr) minmax(0px, 0.8fr)"] {
    grid-template-columns: minmax(0, 1fr) !important;
  }
}

/* Шапка: убираем текстовые пункты меню, оставляем переключатель языка и кнопку */
@media (max-width: 720px) {
  header[data-el="Z"] > nav > a[href^="#"] {
    display: none !important;
  }
  header[data-el="Z"] > nav {
    gap: 12px !important;
  }
}

/* Узкий экран: уменьшаем QR-коды, чтобы они не съедали высоту первого экрана */
@media (max-width: 520px) {
  img[src="assets/qr-code.svg"] {
    width: 132px !important;
    height: 132px !important;
  }
}
'''
open(os.path.join(OUT, 'responsive.css'), 'w', encoding='utf-8').write(responsive)
print('index.html:', len(doc), 'байт')
print('i18n.js:', len(i18n), 'байт')
print('responsive.css:', len(responsive), 'байт')
