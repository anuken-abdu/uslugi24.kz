(function () {
  "use strict";
  var KB = {"phone": "+7 702 891 02 57", "works": [["Сборка кровати", "/sborka-mebeli/sborka-krovati/", "sborka-krovati"], ["Сборка шкафа", "/sborka-mebeli/sborka-shkafa/", "sborka-shkafa"], ["Сборка стола", "/sborka-mebeli/sborka-stola/", "sborka-stola"], ["Сборка кухни", "/sborka-mebeli/sborka-kuhni/", "sborka-kuhni"], ["Сборка мебели IKEA", "/sborka-mebeli/sborka-mebeli-ikea/", "sborka-mebeli-ikea"], ["Сборка стеллажа", "/sborka-mebeli/sborka-stellazha/", "sborka-stellazha"], ["Сборка дивана", "/sborka-mebeli/sborka-divana/", "sborka-divana"], ["Установка смесителя", "/santehnik/ustanovka-smesitelya/", "ustanovka-smesitelya"], ["Установка раковины", "/santehnik/ustanovka-rakoviny/", "ustanovka-rakoviny"], ["Замена гофры и сифона", "/santehnik/zamena-gofry/", "zamena-gofry"], ["Установка унитаза", "/santehnik/ustanovka-unitaza/", "ustanovka-unitaza"], ["Замена кранов", "/santehnik/zamena-kranov/", "zamena-kranov"], ["Замена подводки", "/santehnik/gibkie-podvodki/", "gibkie-podvodki"], ["Замена душевого шланга", "/santehnik/dushevoy-shlang/", "dushevoy-shlang"], ["Полки в ванной", "/santehnik/polki-v-vannoy/", "polki-v-vannoy"], ["Установка розеток", "/elektrik/ustanovka-rozetok/", "ustanovka-rozetok"], ["Замена выключателей", "/elektrik/zamena-vyklyuchateley/", "zamena-vyklyuchateley"], ["Установка светильников", "/elektrik/ustanovka-svetilnikov/", "ustanovka-svetilnikov"], ["Установка люстры", "/elektrik/ustanovka-lyustry/", "ustanovka-lyustry"], ["Подключение техники", "/elektrik/podklyuchenie-tehniki/", "podklyuchenie-tehniki"], ["Замена проводки", "/elektrik/zamena-provodki/", "zamena-provodki"], ["Замена лампочек", "/elektrik/zamena-lampochek/", "zamena-lampochek"], ["Установка диммера", "/elektrik/ustanovka-dimmera/", "ustanovka-dimmera"], ["Навеска телевизора", "/ustanovka/naveska-televizora/", "naveska-televizora"], ["Установка карниза", "/ustanovka/ustanovka-karniza/", "ustanovka-karniza"], ["Зеркала и картины", "/ustanovka/zerkala-i-kartiny/", "zerkala-i-kartiny"], ["Установка плинтуса", "/ustanovka/ustanovka-plintusa/", "ustanovka-plintusa"], ["Укладка ламината", "/ustanovka/ukladka-laminata/", "ukladka-laminata"], ["Укладка линолеума", "/ustanovka/ukladka-linoleuma/", "ukladka-linoleuma"], ["Вырезка в столешнице", "/ustanovka/vyrezka-stoleshnicy/", "vyrezka-stoleshnicy"], ["Установка фурнитуры", "/ustanovka/ustanovka-furnitury/", "ustanovka-furnitury"], ["Врезка замков", "/ustanovka/vrezka-zamkov/", "vrezka-zamkov"]], "cats": [["Сборка мебели", "/sborka-mebeli/", "sborka-mebeli"], ["Сантехник", "/santehnik/", "santehnik"], ["Электрик", "/elektrik/", "elektrik"], ["Установка и навеска", "/ustanovka/", "ustanovka"]], "districts": [["Алматинский", "в районе Алматы", "/rayony/almaty/", 0], ["Байконыр", "в районе Байконыр", "/rayony/baykonyr/", 0], ["Есиль", "в районе Есиль", "/rayony/esil/", 0], ["Нура", "в районе Нура", "/rayony/nura/", 0], ["Сарыарка", "в районе Сарыарка", "/rayony/saryarka/", 0], ["Сарайшык", "в районе Сарайшык", "/rayony/sarayshyk/", 0], ["Косшы", "в Косшы", "/rayony/kosshy/", 1], ["Коянды", "в Коянды", "/rayony/koyandy/", 1], ["Талапкер", "в Талапкере", "/rayony/talapker/", 1]]};
  var CFG = window.CFG || {};
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  function waUrl(t) { return "https://wa.me/" + CFG.wan + "?text=" + encodeURIComponent(t); }

  /* ---------- конверсии Google Ads / GA4 ---------- */
  function conv(kind) {
    if (typeof window.gtag !== "function") return;
    var label = kind === "call" ? CFG.call : CFG.wa;
    if (CFG.ads && label) window.gtag("event", "conversion", { send_to: CFG.ads + "/" + label, value: 1.0, currency: "USD", transport_type: "beacon" });
    if (CFG.ga) window.gtag("event", kind === "call" ? "phone_click" : "whatsapp_click", { page_path: location.pathname, transport_type: "beacon" });
  }
  document.addEventListener("click", function (e) {
    var a = e.target.closest("a");
    if (!a) return;
    var h = a.getAttribute("href") || "";
    if (h.indexOf("tel:") === 0) conv("call");
    else if (h.indexOf("wa.me") > -1) conv("wa");
  });

  /* ---------- меню ---------- */
  var burger = $(".burger"), nav = $("#nav");
  function setNav(o) {
    if (!burger || !nav) return;
    nav.classList.toggle("open", o); burger.setAttribute("aria-expanded", o ? "true" : "false");
    burger.setAttribute("aria-label", o ? "Закрыть меню" : "Открыть меню"); document.body.classList.toggle("lock", o);
  }
  if (burger) burger.addEventListener("click", function () { setNav(!nav.classList.contains("open")); });
  if (nav) nav.addEventListener("click", function (e) { if (e.target.closest("a")) setNav(false); });
  window.addEventListener("resize", function () { if (window.innerWidth > 1180) setNav(false); });

  /* ---------- назад / наверх ---------- */
  var fab = $(".fab");
  var ftr = $(".ftr");
  function onScroll() {
    if (fab) fab.classList.toggle("on", window.pageYOffset > 500);
    // у самого низа страницы плавающие кнопки становятся полупрозрачными, чтобы не закрывать подвал
    var end = ftr ? ftr.getBoundingClientRect().top < window.innerHeight - 40 : false;
    document.body.classList.toggle("at-end", end);
  }
  window.addEventListener("scroll", onScroll, { passive: true }); onScroll();
  $$("[data-top]").forEach(function (b) { b.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: "smooth" }); }); });
  $$("[data-back]").forEach(function (b) {
    b.addEventListener("click", function () {
      var ref = document.referrer, same = ref && ref.indexOf(location.host) > -1;
      if (same && history.length > 1) history.back(); else location.href = "/";
    });
  });

  /* ---------- заявка → WhatsApp (+ расширенные конверсии: телефон передаётся в Google в хешированном виде) ---------- */
  function e164(ph) { var d = ph.replace(/\D/g, ""); if (d.length === 11 && d[0] === "8") d = "7" + d.slice(1); if (d.length === 10) d = "7" + d; return "+" + d; }
  $$("form[data-lead]").forEach(function (f) {
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      var ph = (f.elements.phone.value || "").replace(/[^\d+]/g, ""), err = $(".f-err", f);
      if (ph.replace(/\D/g, "").length < 10) { err.hidden = false; f.elements.phone.focus(); return; }
      err.hidden = true;
      var t = "Здравствуйте! Заявка с сайта.\nРабота: " + f.elements.job.value + "\nРайон: " + f.elements.area.value +
        (f.elements.msg.value.trim() ? "\nЗадача: " + f.elements.msg.value.trim() : "") +
        (f.elements.name.value.trim() ? "\nИмя: " + f.elements.name.value.trim() : "") + "\nТелефон: " + ph;
      if (typeof window.gtag === "function") window.gtag("set", "user_data", { phone_number: e164(ph) });
      conv("wa");
      if (typeof window.gtag === "function" && CFG.ga) window.gtag("event", "generate_lead", { method: "form", transport_type: "beacon" });
      window.open(waUrl(t), "_blank", "noopener");
    });
  });

  /* ---------- чат: ИИ через /api/chat, без ключа — встроенный автоответчик ---------- */
  var chat = $("#chat"), list = chat && $(".chat-l", chat), qbox = chat && $(".chat-q", chat), opener = $(".chat-o");
  var hist = [], started = false, busy = false;
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function add(text, who, html) {
    var d = document.createElement("div"); d.className = "msg " + (who === "u" ? "msg-u" : "msg-b");
    if (html) d.innerHTML = html; else d.textContent = text;
    list.appendChild(d); list.scrollTop = list.scrollHeight; return d;
  }
  function quick(items) {
    qbox.innerHTML = "";
    items.forEach(function (q) { var b = document.createElement("button"); b.type = "button"; b.textContent = q; b.addEventListener("click", function () { ask(q); }); qbox.appendChild(b); });
  }
  function low(s) { return s.toLowerCase().replace(/ё/g, "е"); }
  // встроенный автоответчик: работает без ИИ-ключа и при сбое сети
  var INTENTS = [
    [/цен|стоим|сколько стоит|прайс|почем|по чем|тариф|сколько будет|дорого|расцен/, "Стоимость зависит от вида и объёма работ, типа стены и того, нужен ли демонтаж старого. Пришлите фото задачи в WhatsApp — назовём ориентир, точную цену согласуем до начала работ. Выезд по Астане бесплатный.", "/ceny/"],
    [/скидк|акци|дешевл|процент/, "При первом обращении через WhatsApp — скидка 10%. Кнопка WhatsApp — под чатом."],
    [/гаранти/, "На выполненную работу даём гарантию. Срок и условия мастер назовёт до начала работ."],
    [/выезд|приезд платн|за выезд|вызов платн/, "Выезд мастера по Астане бесплатный. В Косшы, Коянды и Талапкер — по договорённости."],
    [/срочн|сегодня|сейчас|завтра|как быстро|когда можете|через сколько|выходн|вечер/, "Время согласуем при заявке — по возможности приезжаем от 40 минут. Напишите адрес и задачу в WhatsApp или позвоните " + KB.phone + "."],
    [/материал|купить|сам куплю|комплектующ|крепеж|крепёж|дюбел|анкер/, "Обычно материалы и технику покупает заказчик, а мастер заранее подскажет, что и сколько нужно. Крепёж под вашу стену мастер подберёт — уточните при заявке."],
    [/несколько|пару задач|список|заодно|ещё и|еще и|муж на час|мастер на час|мелк|по дому|разн/, "Да, можно перечислить несколько задач — мастер возьмёт нужный инструмент и выполнит всё за один приезд. Напишите список и приложите фото.", "/"],
    [/юр\.|юрлиц|юридич|офис|тоо|(^|\s)ип(\s|$)|организац|договор|ндс|счет|счёт|безнал/, "По работам в офисе и документам для организаций подскажет менеджер по телефону " + KB.phone + "."],
    [/оплат|налич|kaspi|каспи|перевод|карт/, "Способ оплаты уточнит мастер при заявке."],
    [/район|адрес|где вы|куда|левый берег|правый берег|пригород|косшы|коянды|талапкер/, "Выезжаем во все районы Астаны: Алматинский, Байконыр, Есиль, Нура, Сарыарка, Сарайшык. В Косшы, Коянды и Талапкер — по договорённости.", "/rayony/"],
    [/гипсокартон|гкл|бетон|кирпич|стен/, "Крепёж подбираем под стену и вес предмета: для бетона и кирпича — анкеры и дюбели, для гипсокартона — специальный крепёж или крепление к профилю. Перед сверлением проверяем, нет ли скрытой проводки и труб."],
    [/теч|протек|капает|потоп|залива/, "Если течёт сильно — сразу перекройте воду краном на вводе или на стояке. Затем позвоните " + KB.phone + ": мастер заменит подводку, смеситель, сифон или кран.", "/santehnik/"],
    [/искр|запах гар|горит|дым|бьет ток|бьёт ток|выбива/, "Если искрит или пахнет гарью — отключите автомат в щитке и не пользуйтесь розеткой. Позвоните " + KB.phone + ": электрик найдёт причину.", "/elektrik/"],
    [/сантех|вод[аы]|канализ|слив|засор/, "Сантехник: замена смесителей, подводок, сифонов и кранов, установка раковин и унитазов.", "/santehnik/"],
    [/электр|свет|провод|автомат|щит/, "Электрик: розетки, выключатели, светильники, люстры, подключение техники, замена проводки.", "/elektrik/"],
    [/мебел|собрать|сборк|разобрать|разбор/, "Собираем корпусную и мягкую мебель: кровати, шкафы, кухни, столы, стеллажи, диваны, мебель IKEA.", "/sborka-mebeli/"],
    [/повес|навес|просверл|сверл|закреп/, "Навеска: телевизоры, карнизы, зеркала, картины, полки. Крепёж подбираем под стену и вес.", "/ustanovka/"],
    [/(^|\s)бот|робот|ты кто|живой|человек|оператор/, "Я ИИ-консультант сайта. Живой мастер ответит по телефону или в WhatsApp — кнопка ниже."],
    [/спасиб|рахмет|благодар/, "Пожалуйста! Оставьте номер или напишите в WhatsApp — мастер свяжется."],
    [/привет|здравств|салем|сәлем|добрый|ассалам/, "Здравствуйте! Подскажу по сборке мебели, сантехнике, электрике и навеске в Астане. Что нужно сделать?"]
  ];
  // ключи для распознавания конкретных работ (основы слов)
  var WKEY = { "sborka-krovati": "кроват", "sborka-shkafa": "шкаф(?!чик)|купе|гардероб", "sborka-stola": "(^|\\s)стол(?!еш)|стола|столы", "sborka-kuhni": "кухн|гарнитур", "sborka-mebeli-ikea": "ikea|икеа|икея", "sborka-stellazha": "стеллаж|комод|тумб", "sborka-divana": "диван|кресл",
    "ustanovka-smesitelya": "смесител|кран на кухн", "ustanovka-rakoviny": "раковин|мойдодыр|умывальн", "zamena-gofry": "гофр|сифон", "ustanovka-unitaza": "унитаз|бачок|бачк", "zamena-kranov": "шаров|кран[аы]? на ввод|(^|\\s)кран", "gibkie-podvodki": "подводк|шланг.{0,6}(стирал|посудом)", "dushevoy-shlang": "душ|лейк", "polki-v-vannoy": "полк.{0,15}ванн|ванн.{0,15}полк|шкафчик",
    "ustanovka-rozetok": "розет", "zamena-vyklyuchateley": "выключат", "ustanovka-svetilnikov": "светильн|бра|точечн|спот", "ustanovka-lyustry": "люстр", "podklyuchenie-tehniki": "варочн|духов|вытяжк|стиральн|посудомо|подключ", "zamena-provodki": "проводк", "zamena-lampochek": "лампоч|лампу|лампы", "ustanovka-dimmera": "диммер|яркост",
    "naveska-televizora": "телевиз|(^|\\s)тв(\\s|$)|кронштейн", "ustanovka-karniza": "карниз|штор|жалюз", "zerkala-i-kartiny": "зеркал|картин|рамк|часы", "ustanovka-plintusa": "плинтус", "ukladka-laminata": "ламинат", "ukladka-linoleuma": "линолеум", "vyrezka-stoleshnicy": "столешн", "ustanovka-furnitury": "ручк|петл|доводчик|фурнитур|направляющ", "vrezka-zamkov": "замок|замк|личинк|защелк|защёлк" };
  function local(q) {
    var s = low(q);
    if (s.replace(/\D/g, "").length >= 10) return { t: "Спасибо! Чтобы заявка точно дошла, отправьте номер мастеру в WhatsApp кнопкой ниже." };
    var pr = /цен|стоим|сколько|почем|прайс/.test(s);
    var ws = KB.works || [];
    if (!/теч|протек|искр|горит|скидк|гаранти/.test(s)) for (var i = 0; i < ws.length; i++) {
      var key = WKEY[ws[i][2]]; if (!key || !new RegExp(key).test(s)) continue;
      if (pr) return { t: ws[i][0] + ": стоимость зависит от объёма и сложности. Пришлите фото в WhatsApp — назовём ориентир, точную цену согласуем до начала работ.", u: ws[i][1] };
      return { t: "Да, делаем: " + ws[i][0].toLowerCase() + ". Пришлите фото задачи и адрес — назовём ориентир по стоимости и время приезда. Подробно — на странице.", u: ws[i][1] };
    }
    var ds = KB.districts || [];
    for (var j = 0; j < ds.length; j++) {
      var n = low(ds[j][0]).slice(0, Math.max(4, ds[j][0].length - 2));
      if (s.indexOf(n) > -1) return { t: (ds[j][3] ? "Выезжаем " + ds[j][1] + " по договорённости." : "Да, выезжаем " + ds[j][1] + ", выезд бесплатный.") + " Что нужно сделать?", u: ds[j][2] };
    }
    for (var k = 0; k < INTENTS.length; k++) if (INTENTS[k][0].test(s)) return { t: INTENTS[k][1], u: INTENTS[k][2] };
    return { t: "Уточню у мастера. Опишите задачу и район или позвоните " + KB.phone + "." };
  }
  function reply(r) {
    var h = esc(r.t) + (r.u ? '<br><a href="' + r.u + '">Открыть страницу</a>' : "");
    add("", "b", h);
  }
  function ask(q) {
    q = String(q || "").trim(); if (!q || busy) return;
    add(q, "u"); hist.push({ role: "user", content: q });
    busy = true; var wait = add("…", "b");
    var done = function (txt) { busy = false; wait.remove(); hist.push({ role: "assistant", content: txt }); add(txt, "b"); };
    var ctrl = window.AbortController ? new AbortController() : null; var to = setTimeout(function () { if (ctrl) ctrl.abort(); }, 15000);
    fetch("/api/chat", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ messages: hist.slice(-12), page: location.pathname }), signal: ctrl ? ctrl.signal : undefined })
      .then(function (r) { clearTimeout(to); if (!r.ok) throw 0; return r.json(); })
      .then(function (d) { if (!d || !d.text) throw 0; done(d.text); })
      .catch(function () { busy = false; wait.remove(); var r = local(q); hist.push({ role: "assistant", content: r.t }); reply(r); if (qbox) qbox.innerHTML = ""; });
  }
  function openChat() {
    chat.hidden = false; if (opener) opener.hidden = true;
    if (!started) { started = true; add("Здравствуйте! Я ИИ-консультант «Услуги 24». Подскажу по сборке мебели, сантехнике, электрике и навеске. Что нужно сделать?", "b"); quick(["Сколько стоит?", "Повесить телевизор", "Собрать шкаф", "Заменить смеситель", "Как быстро приедете?", "Есть скидка?"]); }
    setTimeout(function () { var i = $("input", chat); if (i && window.innerWidth > 767) i.focus(); }, 50);
  }
  if (chat) {
    $$("[data-chat]").forEach(function (b) { b.addEventListener("click", openChat); });
    $("[data-chat-x]", chat).addEventListener("click", function () { chat.hidden = true; if (opener) opener.hidden = false; });
    $(".chat-f", chat).addEventListener("submit", function (e) { e.preventDefault(); var i = this.elements.q; ask(i.value); i.value = ""; });
  }
  document.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    if (chat && !chat.hidden) { chat.hidden = true; if (opener) opener.hidden = false; }
    setNav(false);
  });
})();
