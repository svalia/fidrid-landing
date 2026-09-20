/*
  Двуязычность лендинга FidRid (ru / en).

  Язык выбирается так: сохранённый выбор пользователя -> язык браузера -> русский.
  Первичный выбор делает короткий скрипт в <head>, чтобы страница не мигала
  русским текстом перед показом английского. Здесь выполняется сам перевод.

  Разметка написана по-русски, перевод подменяет текстовые узлы по словарю DICT.
  Узлы внутри [data-nolang] не трогаем (кнопка переключения языка).
*/
(function () {
  'use strict';

  var DICT = {
  "Как работает": "How it works",
  "Безопасность": "Security",
  "Вопросы": "FAQ",
  "Скачать": "Get the app",
  "Неофициальный клиент Telegram": "Unofficial Telegram client",
  "Каналы\u00a0— в ленту.": "Channels\u00a0— into a feed.",
  "Телеграм\u00a0— в покой.": "Telegram\u00a0— into peace.",
  "У вас 300 каналов и одна мама, которая пишет в том же списке. FidRid забирает каналы себе — красивой лентой, как в соцсети. В телеграме остаются люди.": "You follow 300 channels and one mum — and they all live in the same list. FidRid takes the channels into a proper feed, the way a social app does. Telegram keeps the people.",
  "Скачать в App Store": "Download on the App Store",
  "iPhone · бесплатно · без рекламы": "iPhone · free · no ads",
  "Наведите камеру телефона": "Point your phone camera",
  "2 минуты": "2 minutes",
  "на настройку с нуля": "to set up from scratch",
  "Вход по коду": "Code sign-in",
  "официальное API, без ботов и паролей": "official API, no bots, no passwords",
  "1 список": "One list",
  "в личке — только люди": "in Telegram — people only",
  "Лента не прочитанных": "Unread feed",
  "Пиксель и…": "Pixel & D…",
  "Сухая выж…": "Dry Diges…",
  "Зона турб…": "Turbulenc…",
  "Кофе в 7:00": "Coffee at 7",
  "Все 1 241": "All 1,241",
  "Работа": "Work",
  "Новости": "News",
  "Пиксель и точка": "Pixel & Dot",
  "Что не так с сеткой": "What's wrong with grids",
  "в мобильных лентах": "in mobile feeds",
  "Разбор на пальцах.": "A plain-language breakdown.",
  "Почему 4 колонки на телефоне — это боль, а 2 — нет. С примерами и линейкой.": "Why 4 columns on a phone hurt and 2 don't. With examples and a ruler.",
  "4 часа назад": "4 hours ago",
  "Лента": "Feed",
  "Каналы": "Channels",
  "Настройки": "Settings",
  "Профиль": "Profile",
  "Один список не может быть и мессенджером, и медиа": "One list can't be a messenger and a media outlet at once",
  "Каналы кричат громче людей — просто потому, что их больше. Разводим их по разным приложениям.": "Channels shout louder than people — simply because there are more of them. So we move them to a different app.",
  "До": "Before",
  "После": "After",
  "Сухая выжимка": "Dry Digest",
  "Дайджест за среду: 14 пунктов": "Wednesday digest: 14 items",
  "Зона турбулентности": "Turbulence Zone",
  "Срочно: ещё одна срочная новость": "Breaking: another breaking story",
  "Мама": "Mum",
  "Ты поел? Позвони, пожалуйста": "Have you eaten? Please call",
  "Ночная смена": "Night Shift",
  "Пост, который вы точно пролистаете": "A post you'll definitely scroll past",
  "Мама лежит между двумя дайджестами. Найти её — квест.": "Mum is buried between two digests. Finding her is a quest.",
  "Костя Л.": "Chris L.",
  "Скинул смету, глянь вечером": "Sent the estimate, check tonight",
  "Ремонт, 4 участника": "Renovation, 4 members",
  "Плитку привезут в четверг": "Tiles arrive on Thursday",
  "87 каналов уехали в FidRid": "87 channels moved to FidRid",
  "Каналы никуда не делись — они замьючены и в архиве. И читаются отдельно.": "The channels didn't go anywhere — they're muted and archived. You just read them elsewhere.",
  "Три шага": "Three steps",
  "Настройка короче, чем один дайджест": "Setup is shorter than one digest",
  "Входите под своим аккаунтом": "Sign in with your account",
  "Обычный вход по коду через официальное API. Никаких ботов, пересылок и «дай логин от аккаунта».": "A normal code sign-in through the official API. No bots, no forwarding, no «give us your login».",
  "Отмечаете, что читать": "Pick what you want to read",
  "Список всех ваших каналов с тумблерами и поиском. Нужные — в ленту, остальные оставьте как есть.": "All your channels with toggles and search. The ones you want go to the feed; leave the rest as they are.",
  "Жмёте «замьютить и в архив»": "Tap «mute and archive»",
  "Одним действием сразу для всех выбранных. Телеграм пустеет, лента наполняется. Откатить можно тем же тумблером.": "One action for everything you selected. Telegram empties out, the feed fills up. The same toggle undoes it.",
  "⌕ Поиск каналов": "⌕ Search channels",
  "✓ Массовые действия": "✓ Bulk actions",
  "Показывать все": "Show all",
  "Тихий бэклог": "Quiet Backlog",
  "Лента, которая ведёт себя как лента": "A feed that actually behaves like a feed",
  "Сторис из каналов": "Stories from channels",
  "Кто написал за последние часы — кружками сверху. Пролистать пять каналов быстрее, чем открыть один чат.": "Who posted in the last few hours, as circles on top. Flicking through five channels is faster than opening one chat.",
  "Фильтры и папки": "Filters and folders",
  "«Работа» отдельно, «Новости» отдельно. Утром — рабочее, вечером — всё остальное.": "«Work» apart, «News» apart. Work in the morning, everything else at night.",
  "Свои статусы прочтения": "Your own read states",
  "Пост непрочитан, пока вы его не увидели здесь. Счётчик в телеграме при этом молчит.": "A post stays unread until you've seen it here. The Telegram badge stays quiet.",
  "Массовые действия": "Bulk actions",
  "Замьютить и заархивировать 80 каналов разом. Вручную это вечер жизни.": "Mute and archive 80 channels in one go. By hand that's an evening of your life.",
  "Честно про доступ": "Straight talk about access",
  "Вы пускаете приложение в свой аккаунт. Вот что оно там делает": "You're letting an app into your account. Here's what it does there",
  "Официальное API": "Official API",
  "Тот же протокол, на котором работают все сторонние клиенты телеграма. Пароль вы вводите не нам, а в окно входа телеграма.": "The same protocol every third-party Telegram client runs on. You type the code into Telegram's own login, not into us.",
  "Аккаунт не под угрозой": "Your account is safe",
  "Мы не рассылаем, не вступаем в каналы и не пишем от вашего имени. Всё, что делает FidRid, — читает и выключает уведомления там, где вы попросили.": "We don't send anything, don't join channels and never post on your behalf. All FidRid does is read, and mute where you asked it to.",
  "Главное": "Key point",
  "Ваши сообщения не покидают телефон": "Your messages never leave your phone",
  "Лента собирается": "The feed is assembled",
  "на устройстве": "on your device",
  ". Мы не храним ваши сообщения на сервере, не пересылаем их третьим лицам и не продаём статистику чтения — её просто негде взять.": ". We don't keep your messages on a server, don't pass them to third parties and don't sell reading stats — there's nowhere to take them from.",
  "Ничего не теряется": "Nothing gets lost",
  "Мьют и архив — штатные функции телеграма. Каналы остаются на месте, посты никуда не деваются, вернуть всё можно одним тумблером.": "Mute and archive are Telegram's own features. Channels stay where they are, posts stay where they are, and one toggle brings it all back.",
  "Вопросы, которые вы уже придумали": "The questions you've already thought of",
  "Сколько стоит?": "How much does it cost?",
  "Ничего. Приложение бесплатное, рекламы внутри нет.": "Nothing. The app is free and has no ads.",
  "Меня не забанят за сторонний клиент?": "Will I get banned for using a third-party client?",
  "Сторонние клиенты телеграм разрешает — на этом держится половина его экосистемы. Баны прилетают за спам и массовые рассылки; FidRid не делает ни того, ни другого.": "Telegram allows third-party clients — half its ecosystem is built on them. Bans come for spam and mass messaging; FidRid does neither.",
  "А личные чаты вы видите?": "Can you see my private chats?",
  "FidRid показывает только каналы, которые вы сами включили. Личка в приложение не попадает — в этом вся идея.": "FidRid shows only the channels you switched on yourself. Private chats never enter the app — that's the whole point.",
  "Что будет с непрочитанными, если я замьючу канал?": "What happens to unread posts if I mute a channel?",
  "Ничего. Мьют убирает звук и бейдж, архив — из основного списка. Посты остаются в телеграме и появляются в ленте FidRid.": "Nothing. Mute removes the sound and the badge, archive removes it from the main list. Posts stay in Telegram and show up in the FidRid feed.",
  "Android будет?": "Will there be an Android version?",
  "Пока только iPhone. Android в планах — о старте напишем в канале проекта.": "iPhone only for now. Android is planned — we'll announce it in the project channel.",
  "Верните телеграму его работу": "Give Telegram its job back",
  "Личные сообщения — в телеграме. Каналы — в ленте. Две минуты на настройку, и список чатов снова помещается на один экран.": "Private messages in Telegram. Channels in the feed. Two minutes of setup and your chat list fits on one screen again.",
  "iPhone 14.0 и новее · бесплатно": "iPhone 14.0 and later · free",
  "FidRid — неофициальный клиент Telegram, не связанный с Telegram LLC.": "FidRid is an unofficial Telegram client, not affiliated with Telegram LLC.",
  "Условия использования": "Terms of Use",
  "Политика конфиденциальности": "Privacy Policy",
  "Обработка персональных данных": "Personal Data Processing",
  "Поддержка": "Support",
  "П": "P", "С": "D", "З": "T", "К": "C", "Т": "B", "М": "M", "Н": "N", "Р": "R"
  };

  // Атрибуты и метаданные переводим отдельно: текстовым обходом их не достать
  var ATTR_DICT = {
    'QR-код на страницу приложения в App Store': 'App Store QR code'
  };

  var META = {
    ru: {
      title: "FidRid — каналы в ленту",
      description: "FidRid забирает телеграм-каналы в отдельную ленту со сторис, фильтрами и своими статусами прочтения. В телеграме остаётся личка. iPhone, бесплатно, без рекламы.",
      locale: 'ru_RU'
    },
    en: {
      title: "FidRid — channels into a feed",
      description: "FidRid moves your Telegram channels into a separate feed with stories, filters and its own read states. Telegram keeps the private chats. iPhone, free, no ads.",
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
      var m = /^(\s*)([\s\S]*?)(\s*)$/.exec(node.nodeValue);
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
