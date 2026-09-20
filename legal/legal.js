/*
  Языки на страницах юридических документов.

  Обе версии текста лежат в разметке (<article data-lang="ru"> и "en"), скрипт
  показывает нужную. Правило выбора и ключ в localStorage те же, что на лендинге,
  поэтому выбор языка переносится между страницами.

  Ссылка на PDF меняется вместе с языком: русскому документу соответствует файл
  с суффиксом _Ru, английскому - _En.
*/
(function () {
  'use strict';

  var STORAGE_KEY = 'fidrid-lang';

  var LABELS = {
    ru: {
      back: 'На главную',
      pdf: 'Скачать PDF',
      disclaimer: 'FidRid — неофициальный клиент Telegram, не связанный с Telegram LLC.',
      toggle: 'EN',
      toggleTitle: 'Switch to English'
    },
    en: {
      back: 'Back to home',
      pdf: 'Download PDF',
      disclaimer: 'FidRid is an unofficial Telegram client, not affiliated with Telegram LLC.',
      toggle: 'RU',
      toggleTitle: 'Переключить на русский'
    }
  };

  var current = 'ru';

  function setLanguage(lang, remember) {
    if (lang !== 'ru' && lang !== 'en') lang = 'ru';
    current = lang;

    var articles = document.querySelectorAll('article[data-lang]');
    for (var i = 0; i < articles.length; i++) {
      articles[i].hidden = articles[i].getAttribute('data-lang') !== lang;
    }

    var labels = LABELS[lang];
    var marked = document.querySelectorAll('[data-t]');
    for (var j = 0; j < marked.length; j++) {
      var key = marked[j].getAttribute('data-t');
      if (labels[key]) marked[j].textContent = labels[key];
    }

    var pdf = document.getElementById('pdf-link');
    if (pdf) {
      pdf.setAttribute(
        'href',
        pdf.getAttribute('href').replace(/_(Ru|En)\.pdf$/, lang === 'ru' ? '_Ru.pdf' : '_En.pdf')
      );
    }

    var article = document.querySelector('article[data-lang="' + lang + '"]');
    var heading = article && article.querySelector('h1');
    var description = document.querySelector('meta[name="description"]');
    if (heading && description) description.setAttribute('content', heading.textContent.trim());

    var titles = window.__fidridTitles;
    if (titles && titles[lang]) document.title = titles[lang];

    var toggle = document.getElementById('lang-toggle');
    if (toggle) {
      toggle.textContent = labels.toggle;
      toggle.setAttribute('aria-label', labels.toggleTitle);
    }

    document.documentElement.lang = lang;

    if (remember) {
      try { localStorage.setItem(STORAGE_KEY, lang); } catch (e) {}
    }
  }

  function init() {
    var toggle = document.getElementById('lang-toggle');
    if (toggle) {
      toggle.addEventListener('click', function () {
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
