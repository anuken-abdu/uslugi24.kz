# -*- coding: utf-8 -*-
"""Генератор сайта «Услуги 24» (мастер на час, Астана): python3 src/build.py → dist/"""
import html, json, re, shutil, sys
from datetime import date
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from data import *

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
VER = "0611261800"
TODAY = date.today().isoformat()
E = lambda s: html.escape(str(s), quote=True)
PAGES = []
C = {c["slug"]: c for c in CATS}; WK = {w["slug"]: w for w in WORKS}
BY_CAT = {c["slug"]: [w for w in WORKS if w["cat"] == c["slug"]] for c in CATS}
def wurl(w): return f"/{w['cat']}/{w['slug']}/"
def curl(c): return f"/{c['slug']}/"

def wa(text): return f"https://wa.me/{WA_NUMBER}?text=" + re.sub(r"\s", "%20", html.escape(text))
def wa_attr(text): return f'href="{wa(text)}" target="_blank" rel="noopener"'
PH = json.loads((Path(__file__).parent / "ph_icons.json").read_text(encoding="utf-8"))
def ph(name, cls="ph"): return f'<svg class="{cls}" viewBox="0 0 256 256" aria-hidden="true" focusable="false">{PH[name + "-duotone"]}</svg>'

ICON = {
 "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>',
 "wa": '<path d="M3.5 20.5l1.2-4.3A8.5 8.5 0 1 1 8 19.4z"/><path d="M9 8.5c0 3 2.5 6.3 6 6.8l1.3-1.6-2-1-1 .9c-1-.5-2-1.5-2.4-2.5l.9-1-1-2z"/>',
 "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>', "up": '<path d="M12 19V5M6 11l6-6 6 6"/>', "back": '<path d="M19 12H5M11 6l-6 6 6 6"/>',
 "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>', "close": '<path d="M6 6l12 12M18 6L6 18"/>', "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
 "chev": '<path d="M6 9l6 6 6-6"/>', "send": '<path d="M4 12l16-8-6 16-2.5-6.5z"/>', "pin": '<path d="M12 21s7-6.2 7-12a7 7 0 1 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="9" r="2.5"/>',
 "spark": '<path d="M12 3l1.8 4.7L18.5 9.5l-4.7 1.8L12 16l-1.8-4.7L5.5 9.5l4.7-1.8z"/><path d="M18.5 15l.8 2 2 .8-2 .8-.8 2-.8-2-2-.8 2-.8z"/>',
}
def ui(n, cls="ui"): return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><g fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ICON[n]}</g></svg>'

MSG = "Здравствуйте! Нужен мастер в Астане."
def logo(dark=False):
    return (f'<a class="logo{" logo-d" if dark else ""}" href="/"><img src="/assets/logo-mark{"-d" if dark else ""}.svg" alt="" width="44" height="44">'
            f'<span class="logo-t">Услуги<i>24</i></span></a>')

def btns(msg=MSG, dark=False):
    return (f'<div class="btns"><a class="btn btn-p" href="tel:{PHONE_TEL}">{ui("phone")}Позвонить</a>'
            f'<a class="btn btn-w" {wa_attr(msg)}>{ui("wa")}Написать в WhatsApp</a></div>')

def sec(title, inner, sub="", alt=False, sid="", link=None, cls=""):
    lk = f'<a class="lnk" href="{link[1]}">{link[0]} {ui("arrow")}</a>' if link else ""
    return (f'<section class="sec{" sec-alt" if alt else ""}{" " + cls if cls else ""}"{f" id={chr(34)}{sid}{chr(34)}" if sid else ""}><div class="wrap">'
            f'<div class="sec-h"><div><h2>{title}</h2>{f"<p>{sub}</p>" if sub else ""}</div>{lk}</div>{inner}</div></section>')

def crumbs_html(cr):
    items = [("Главная", "/")] + cr
    li = "".join(f'<li><a href="{u}">{E(n)}</a></li>' if i < len(items) - 1 else f'<li aria-current="page">{E(n)}</li>' for i, (n, u) in enumerate(items))
    return f'<nav class="crumbs" aria-label="Навигация"><ol>{li}</ol></nav>'

def board(tiles, big=False):
    """Перфорированная панель с инструментами: плитки-иконки, как инструмент на стене мастерской."""
    t = "".join(f'<a class="bt{" bt-y" if y else ""}" href="{u}">{ph(i)}<span>{E(l)}</span></a>' for i, l, u, y in tiles)
    return f'<div class="board{" board-b" if big else ""}">{t}</div>'

def tape():
    return '<div class="tape" aria-hidden="true"></div>'

def ph_hero(h1, lead, crumbs, msg=MSG, icon=None, label=""):
    side = f'<div class="phd-art" aria-hidden="true"><span class="pa">{ph(icon)}</span>{f"<b>{E(label)}</b>" if label else ""}</div>' if icon else ""
    return (f'<section class="phd"><div class="wrap">{crumbs_html(crumbs)}<div class="phd-in{" has-art" if icon else ""}"><div><h1>{h1}</h1><p class="lead-t">{lead}</p>{btns(msg, True)}</div>{side}</div></div>{tape()}</section>')

# ---------------------------------------------------------------- блоки
def wcount(c):
    n = len(BY_CAT[c["slug"]]); return f"{n} {plural(n, 'вид', 'вида', 'видов')} работ"

def perks_html():
    return '<section class="perks"><div class="wrap"><ul>' + "".join(f'<li>{ph(i)}<span><b>{E(t)}</b><small>{E(s)}</small></span></li>' for i, t, s in PERKS) + "</ul></div></section>"

def cat_cards(items=None):
    items = items or CATS
    out = []
    for c in items:
        ws = BY_CAT[c["slug"]][:4]
        li = "".join(f'<li><a href="{wurl(w)}">{E(w["name"])}</a></li>' for w in ws)
        out.append(f'<div class="cc"><a class="cc-h" href="{curl(c)}"><span class="cc-i">{ph(c["icon"])}</span><span><b>{E(c.get("card", c["name"]))}</b><small>{wcount(c)}</small></span></a>'
                   f'<ul>{li}</ul><a class="cc-l" href="{curl(c)}">Все работы {ui("arrow")}</a></div>')
    return f'<div class="ccs{" ccs-3" if len(items) == 3 else ""}">' + "".join(out) + "</div>"

def work_tiles(items):
    return f'<div class="wts{" wts-3" if len(items) % 4 and len(items) % 3 == 0 else ""}">' + "".join(f'<a class="wt" href="{wurl(w)}">{ph(w["icon"])}<b>{E(w["name"])}</b>{ui("arrow")}</a>' for w in items) + "</div>"

def incl_html(w):
    return '<ul class="inc">' + "".join(f'<li>{ui("check")}<span>{E(x)}</span></li>' for x in w["incl"]) + "</ul>"

def steps_html():
    return '<ol class="steps">' + "".join(f'<li>{ph(ic)}<b>{E(t)}</b><p>{E(d)}</p></li>' for ic, (t, d) in zip(STEP_ICONS, STEPS)) + "</ol>"

def factors_html():
    return '<div class="fac">' + "".join(f'<div><b>{E(t)}</b><p>{E(d)}</p></div>' for t, d in PRICE_FACTORS) + "</div>"

def prep_html():
    return '<ul class="prep">' + "".join(f'<li>{ui("check")}<span>{E(x)}</span></li>' for x in PREP) + "</ul>"

def reviews_html():
    return '<div class="rvs">' + "".join(f'<figure class="rv"><blockquote>{E(t)}</blockquote><figcaption><b>{E(n)}</b><span>{E(r)}</span></figcaption></figure>' for n, r, t in REVIEWS) + "</div>"

def faq_html(faq):
    return '<div class="faq">' + "".join(f'<details><summary>{E(q)}{ui("chev")}</summary><p>{E(a)}</p></details>' for q, a in faq) + "</div>"

def districts_html(cur=""):
    city = [d for d in DISTRICTS if not d.get("suburb")]; sub = [d for d in DISTRICTS if d.get("suburb")]
    li = lambda ds: "".join(f'<li><a href="/rayony/{d["slug"]}/"{" aria-current=page" if d["slug"] == cur else ""}>{E(d["short"])}{ui("arrow")}</a></li>' for d in ds)
    return f'<div class="geo"><div><h3>Районы Астаны</h3><ul class="dl dl-3">{li(city)}</ul></div><div><h3>Пригороды</h3><ul class="dl">{li(sub)}</ul></div></div>'

def geo_sec(cur=""):
    return sec("Выезжаем по всей Астане", districts_html(cur), "Все районы столицы. В пригороды — по договорённости.", alt=True, sid="rayony")

def article_cards():
    return '<div class="arts">' + "".join(f'<a class="art" href="/stati/{a["slug"]}/"><b>{E(a["title"])}</b><span>{E(a["desc"])}</span>{ui("arrow")}</a>' for a in ARTICLES) + "</div>"

def callout(msg=MSG):
    return f'''<section class="cta"><div class="wrap"><div class="cta-in"><div><b>Пришлите фото задачи в&nbsp;WhatsApp</b><p>Назовём ориентир по стоимости и время приезда. Скидка 10% на первое обращение через WhatsApp.</p></div>{btns(msg, True)}</div></div></section>'''

def lead_form(title="Вызвать мастера", cat=""):
    copts = "".join(f'<option{" selected" if c["slug"] == cat else ""}>{E(c["name"])}</option>' for c in CATS)
    dopts = '<option>Не указан</option>' + "".join(f'<option>{E(d["short"])}</option>' for d in DISTRICTS)
    return f'''<section class="sec sec-dark" id="zayavka"><div class="wrap lead">
<div><h2>{title}</h2><p>Заполните форму — заявка откроется в WhatsApp с вашими данными. Приложите фото задачи, чтобы мастер сразу назвал ориентир по цене.</p>
<a class="lead-ph" href="tel:{PHONE_TEL}">{ui("phone")}{PHONE_DISPLAY}</a></div>
<form class="form" data-lead novalidate>
<div class="fld"><label for="fN">Имя</label><input id="fN" name="name" autocomplete="name"></div>
<div class="fld"><label for="fP">Телефон</label><input id="fP" name="phone" type="tel" inputmode="tel" autocomplete="tel" required placeholder="+7"></div>
<div class="fld"><label for="fV">Что сделать</label><select id="fV" name="job"><option>Нужна консультация</option>{copts}<option>Мелкий ремонт</option><option>Несколько задач</option></select></div>
<div class="fld"><label for="fD">Район</label><select id="fD" name="area">{dopts}</select></div>
<div class="fld fld-w"><label for="fM">Задача</label><textarea id="fM" name="msg" rows="3" placeholder="Например: повесить телевизор 55 дюймов на бетонную стену"></textarea></div>
<p class="f-err" hidden>Укажите телефон, чтобы мы могли связаться.</p>
<button class="btn btn-p fld-w" type="submit">{ui("wa")}Отправить в WhatsApp</button>
<p class="f-note fld-w">Нажимая кнопку, вы соглашаетесь с <a href="/privacy-policy/">политикой конфиденциальности</a>.</p></form></div></section>'''

# ---------------------------------------------------------------- schema
ORG = {"@type": "HomeAndConstructionBusiness", "@id": SITE_URL + "/#org", "name": BRAND, "url": SITE_URL + "/", "telephone": PHONE_TEL, "logo": SITE_URL + "/assets/icon-512.png",
       "image": SITE_URL + "/assets/og.png", "address": {"@type": "PostalAddress", "streetAddress": ADDRESS, "addressLocality": "Астана", "addressCountry": "KZ"},
       "areaServed": {"@type": "City", "name": "Астана"}, "contactPoint": {"@type": "ContactPoint", "telephone": PHONE_TEL, "contactType": "customer service", "areaServed": "KZ", "availableLanguage": ["ru", "kk"]}}
def service_schema(name, url, desc, area="Астана"):
    return {"@context": "https://schema.org", "@type": "Service", "name": name, "serviceType": name, "url": SITE_URL + url, "description": desc,
            "provider": {"@id": SITE_URL + "/#org"}, "areaServed": {"@type": "City" if area == "Астана" else "Place", "name": area}}
def faq_schema(faq):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}

def fit(s, n=155):
    """Description не длиннее n символов — по границе слова."""
    return s if len(s) <= n else s[:n - 1].rsplit(" ", 1)[0].rstrip(",.:;—") + "…"

# ---------------------------------------------------------------- шаблон
def nav_html():
    cats = "".join(f'<li class="has"><a href="{curl(c)}">{E(c.get("card", c["name"]))}</a><ul class="sub">'
                   + "".join(f'<li><a href="{wurl(w)}">{E(w["name"])}</a></li>' for w in BY_CAT[c["slug"]]) + "</ul></li>" for c in CATS)
    return f'''<nav class="nav" id="nav" aria-label="Меню"><ul>{cats}
<li><a href="/ceny/">Цены</a></li><li><a href="/rayony/">Районы</a></li><li><a href="/kontakty/">Контакты</a></li></ul>
<div class="nav-m">{btns(MSG, True)}</div></nav>'''

def gtag():
    """Единый тег Google — сразу после <head>. Пока клиент не прислал ID, тег не выводится."""
    if not TAG_ID: return ""
    if TAG_ID.startswith("GTM-"):
        return (f'<script async src="https://www.googletagmanager.com/gtm.js?id={TAG_ID}"></script>\n'
                "<script>\n  window.dataLayer = window.dataLayer || [];\n  function gtag(){dataLayer.push(arguments);}\n  gtag('js', new Date());\n</script>\n")
    src = f"https://www.googletagmanager.com/gtag/js?id={TAG_ID}"
    return (f'<script async src="{src}"></script>\n'
            f"<script>\n  window.dataLayer = window.dataLayer || [];\n  function gtag(){{dataLayer.push(arguments);}}\n  gtag('js', new Date());\n  gtag('config', '{TAG_ID}');\n</script>\n")

CSS = (Path(__file__).parent / "fonts.css").read_text(encoding="utf-8") + (Path(__file__).parent / "styles.css").read_text(encoding="utf-8")
CSS = re.sub(r"/\*.*?\*/", "", CSS, flags=re.S); CSS = re.sub(r"\s*\n\s*", "", CSS); CSS = re.sub(r"\s*([{};:,>])\s*", r"\1", CSS).replace(";}", "}")

def page(path, title, desc, body, schemas=(), crumbs=None, prio="0.7"):
    PAGES.append((path, prio))
    desc = fit(desc)
    bc = []
    if crumbs:
        items = [("Главная", "/")] + crumbs
        bc = [{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE_URL + u} for i, (n, u) in enumerate(items)]}]
    ld = "".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in [{"@context": "https://schema.org", **ORG}, *schemas, *bc])
    cfg = json.dumps({"ga": GA_ID, "ads": GADS_ID, "call": GADS_CALL_LABEL, "wa": GADS_WA_LABEL, "wan": WA_NUMBER}, ensure_ascii=False)
    foot_cats = "".join(f'<div><h3>{E(c["name"])}</h3><ul>' + "".join(f'<li><a href="{wurl(w)}">{E(w["name"])}</a></li>' for w in BY_CAT[c["slug"]][:6]) + "</ul></div>" for c in CATS)
    doc = f'''<!doctype html>
<html lang="ru">
<head>
{gtag()}<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{SITE_URL}{path}">
<meta name="robots" content="{"noindex,follow" if path == "/404" else "index,follow,max-image-preview:large"}">
<meta name="geo.region" content="KZ-AST"><meta name="geo.placename" content="Астана"><meta name="geo.position" content="51.1282;71.4304"><meta name="ICBM" content="51.1282, 71.4304">
<meta property="og:type" content="website"><meta property="og:locale" content="ru_KZ"><meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{SITE_URL}{path}">
<meta property="og:image" content="{SITE_URL}/assets/og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#15171f">
<link rel="icon" href="/favicon.ico" sizes="48x48"><link rel="icon" href="/assets/logo-mark.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="/assets/apple-touch-icon.png"><link rel="manifest" href="/site.webmanifest">
<link rel="preload" href="/assets/fonts/golos-text-cyrillic-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/unbounded-cyrillic-700-normal.woff2" as="font" type="font/woff2" crossorigin>
<style>{CSS}</style>
{ld}
</head>
<body>
<a class="skip" href="#main">К содержимому</a>
<header class="hdr"><div class="wrap hdr-in">{logo()}{nav_html()}
<div class="hdr-c"><a class="hdr-ph" href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a>
<a class="hdr-call" href="tel:{PHONE_TEL}" aria-label="Позвонить {PHONE_DISPLAY}">{ui("phone")}</a>
<a class="btn btn-w btn-s hdr-wa" {wa_attr(MSG)}>{ui("wa")}WhatsApp</a>
<button class="burger" type="button" aria-label="Открыть меню" aria-expanded="false" aria-controls="nav">{ui("menu")}{ui("close", "ui ui-x")}</button></div></div></header>
<main id="main">
{body}
</main>
<footer class="ftr"><div class="wrap ftr-g">
<div class="ftr-a">{logo(True)}<p>Мастер на час в Астане: сборка мебели, сантехника, электрика, навеска и мелкий ремонт.</p><a class="ftr-ph" href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a><p class="ftr-ad">{ui("pin")}Астана, {ADDRESS}</p></div>
{foot_cats}
<div><h3>Компания</h3><ul><li><a href="/ceny/">Цены</a></li><li><a href="/rayony/">Районы</a></li><li><a href="/stati/">Статьи</a></li><li><a href="/o-nas/">О нас</a></li><li><a href="/kontakty/">Контакты</a></li><li><a href="/privacy-policy/">Конфиденциальность</a></li></ul></div>
</div><div class="wrap ftr-b"><span>© {date.today().year} {BRAND}. Информация на сайте не является публичной офертой.</span><span>Разработка и продвижение <a href="{DEV[1]}" target="_blank" rel="noopener">{DEV[0]}</a></span></div></footer>
<div class="fab"><button class="fab-b" type="button" data-back aria-label="Назад" title="Назад">{ui("back")}</button><button class="fab-b" type="button" data-top aria-label="Наверх" title="Наверх">{ui("up")}</button></div>
<button class="chat-o" type="button" data-chat aria-label="ИИ-консультант"><span class="chat-o-i">{ui("spark")}</span><span class="chat-o-t">ИИ-консультант</span></button>
<div class="chat" id="chat" hidden role="dialog" aria-label="ИИ-консультант"><div class="chat-h"><b>{BRAND}<small>ИИ-консультант</small></b><button type="button" data-chat-x aria-label="Закрыть чат">{ui("close")}</button></div>
<div class="chat-l" aria-live="polite"></div><div class="chat-q"></div>
<form class="chat-f"><input name="q" autocomplete="off" placeholder="Напишите вопрос" aria-label="Ваш вопрос"><button type="submit" aria-label="Отправить">{ui("send")}</button></form>
<a class="chat-wa" {wa_attr("Здравствуйте! Пишу с сайта, нужен мастер.")}>{ui("wa")}Продолжить в WhatsApp</a></div>
<script>window.CFG={cfg};</script>
<script src="/assets/app.js?v={VER}" defer></script>
</body></html>'''
    out = DIST / "404.html" if path == "/404" else DIST / path.strip("/") / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True); out.write_text(doc, encoding="utf-8")

# ---------------------------------------------------------------- страницы
HERO_TILES = [("dresser", "Шкафы", "sborka-shkafa"), ("drop", "Смесители", "ustanovka-smesitelya"), ("television", "Телевизоры", "naveska-televizora"),
              ("lamp-pendant", "Люстры", "ustanovka-lyustry"), (None, "", None), ("plug", "Розетки", "ustanovka-rozetok"),
              ("cooking-pot", "Кухни", "sborka-kuhni"), ("squares-four", "Ламинат", "ukladka-laminata"), ("bed", "Кровати", "sborka-krovati")]

def build_home():
    tiles = [(i, l, wurl(WK[s]), False) if i else ("toolbox", "Все работы", "#uslugi", True) for i, l, s in HERO_TILES]
    body = f'''<section class="hero"><div class="wrap hero-in"><div class="hero-t">
<h1>Мастер на&nbsp;час в&nbsp;<em>Астане</em></h1>
<p class="lead-t">Сборка мебели, сантехника, электрика, навеска телевизоров и&nbsp;люстр. Несколько задач — за&nbsp;один приезд.</p>
{btns()}</div>
<div class="hero-v">{board(tiles)}</div></div>{tape()}</section>
{perks_html()}
{sec("Виды работ", cat_cards(), "Выберите направление — внутри подробности по каждой работе.", sid="uslugi")}
{sec("Популярные работы", work_tiles([WK[s] for s in POPULAR]), "С чем обращаются чаще всего.", alt=True)}
{callout()}
{sec("Как мы работаем", steps_html())}
{sec("От чего зависит стоимость", factors_html(), "Ориентир называем по фото, точную цену — до начала работ.", alt=True, link=("Подробнее о ценах", "/ceny/"))}
{sec("Как подготовиться к приезду", prep_html(), link=("Памятка", "/stati/kak-podgotovitsya-k-priezdu-mastera/"))}
{geo_sec()}
{sec("Полезно знать", article_cards(), link=("Все статьи", "/stati/"))}
{sec("Отзывы клиентов", reviews_html())}
{sec("Частые вопросы", faq_html(FAQ), alt=True)}
{lead_form()}'''
    page("/", f"Мастер на час в Астане — сборка мебели, сантехник, электрик | {BRAND}",
         "Муж на час в Астане: сборка мебели, сантехник, электрик, навеска телевизора, карнизов и люстр. Бесплатный выезд, гарантия, −10% через WhatsApp.",
         body, [service_schema("Мастер на час", "/", "Сборка мебели, сантехнические и электромонтажные работы, навеска и мелкий ремонт в Астане."), faq_schema(FAQ)], prio="1.0")

def build_cats():
    for c in CATS:
        url = curl(c); ws = BY_CAT[c["slug"]]
        faq = [(f"Сколько стоят услуги: {c['name'].lower()}?", "Зависит от вида и объёма работ. Пришлите фото — назовём ориентир, точную цену согласуем до начала работ.")] + FAQ[1:6]
        others = [x for x in CATS if x is not c]
        body = f'''{ph_hero(E(c["h1"]), E(c["lead"]), [(c["name"], url)], f"Здравствуйте! Нужен мастер: {c['name'].lower()}.", c["icon"], wcount(c))}
{sec(wcount(c)[0].upper() + wcount(c)[1:], work_tiles(ws))}
<section class="sec sec-alt"><div class="wrap two"><div class="prose">{"".join(f"<p>{E(x)}</p>" for x in c["body"])}</div><div>{steps_html()}</div></div></section>
{callout(f"Здравствуйте! Нужен мастер: {c['name'].lower()}.")}
{sec("Вопросы", faq_html(faq))}
{sec("Другие направления", cat_cards(others), alt=True)}
{lead_form(f"Заявка: {c['name'].lower()}", c["slug"])}'''
        names = ", ".join(w["name"].lower() for w in ws[:4])
        page(url, f"{c['h1']} — вызов мастера | {BRAND}", f"{c['h1']}: {names}. Бесплатный выезд, гарантия на работу, −10% через WhatsApp.",
             body, [service_schema(c["h1"].replace(" в Астане", ""), url, c["lead"]), faq_schema(faq)], crumbs=[(c["name"], url)], prio="0.9")

def build_works():
    for w in WORKS:
        c = C[w["cat"]]; url = wurl(w)
        faq = w["faq"] + [FAQ[0], FAQ[1], FAQ[3]]
        same = [x for x in BY_CAT[c["slug"]] if x is not w]
        k = BY_CAT[c["slug"]].index(w) % max(1, len(same)); same = (same[k:] + same[:k])[:4]
        body = f'''{ph_hero(E(w["h1"]), E(w["intro"]), [(c["name"], curl(c)), (w["name"], url)], f"Здравствуйте! Нужно: {w['name'].lower()}.", w["icon"])}
<section class="sec"><div class="wrap two"><div><h2>Что входит в работу</h2>{incl_html(w)}</div><div><h2>Как заказать</h2><p class="txt">Опишите задачу и пришлите фото в WhatsApp. Назовём ориентир по стоимости, согласуем время, мастер приедет с инструментом и крепежом под вашу задачу.</p>
{btns(f"Здравствуйте! Нужно: {w['name'].lower()}.")}</div></div></section>
{sec("От чего зависит стоимость", factors_html(), alt=True)}
{sec("Как мы работаем", steps_html())}
{callout(f"Здравствуйте! Нужно: {w['name'].lower()}.")}
{sec("Вопросы", faq_html(faq), alt=True)}
{sec("Другие работы", work_tiles(same), link=(c["name"], curl(c)))}
{geo_sec()}
{lead_form(f"Заявка: {w['name'].lower()}", c["slug"])}'''
        page(url, f"{w['h1']} — мастер на дом | {BRAND}", f"{w['h1']}: {w['intro'][0].lower()}{w['intro'][1:]} Бесплатный выезд, гарантия.",
             body, [service_schema(w["name"], url, w["intro"]), faq_schema(faq)], crumbs=[(c["name"], curl(c)), (w["name"], url)], prio="0.8")

def build_districts():
    body = f'''{ph_hero("Мастер на час по районам Астаны", "Выезжаем во все районы столицы. В пригороды — по договорённости.", [("Районы", "/rayony/")], "Здравствуйте! Нужен мастер, мой район:", "map-pin")}
{sec("Районы и пригороды", districts_html())}{lead_form()}'''
    page("/rayony/", f"Мастер на час по районам Астаны | {BRAND}", "Мастер на час в районах Алматы, Байконыр, Есиль, Нура, Сарыарка, Сарайшык. Сборка мебели, сантехник, электрик.", body, crumbs=[("Районы", "/rayony/")], prio="0.8")
    for d in DISTRICTS:
        url = f"/rayony/{d['slug']}/"
        spots = "".join(f"<li>{E(x)}</li>" for x in d["spots"])
        go = "Выезжаем по договорённости — уточните адрес при заявке." if d.get("suburb") else "Да, выезд по Астане бесплатный. Время приезда согласуем при заявке."
        faq = [(f"Выезжаете {d['loc']}?", go), (f"Сколько стоит вызвать мастера {d['loc']}?", FAQ[0][1])] + FAQ[3:6]
        body = f'''{ph_hero(f"Мастер на час {E(d['loc'])}", E(d["about"]), [("Районы", "/rayony/"), (d["short"], url)], f"Здравствуйте! Нужен мастер, {d['name']}.", "map-pin", d["short"])}
<section class="sec"><div class="wrap two"><div><h2>Где работаем</h2><ul class="bl">{spots}</ul></div><div><h2>Как вызвать мастера</h2><p class="txt">Позвоните или напишите в WhatsApp, укажите адрес {d['loc']} и задачу, приложите фото. Назовём ориентир по стоимости и согласуем время.</p></div></div></section>
{sec("Виды работ", cat_cards(), alt=True)}
{sec("Популярные работы", work_tiles([WK[s] for s in POPULAR]))}
{callout(f"Здравствуйте! Нужен мастер, {d['name']}.")}
{sec("Вопросы", faq_html(faq), alt=True)}
{sec("Другие районы", districts_html(d["slug"]))}
{lead_form(f"Заявка — {d['short']}")}'''
        page(url, f"Мастер на час {d['loc']} (Астана) | {BRAND}", f"Муж на час {d['loc']}: сборка мебели, сантехник, электрик, навеска телевизора. {d['about']}",
             body, [service_schema(f"Мастер на час {d['loc']}", url, d["about"], d["name"]), faq_schema(faq)], crumbs=[("Районы", "/rayony/"), (d["short"], url)], prio="0.7")

def build_articles():
    for a in ARTICLES:
        url = f"/stati/{a['slug']}/"
        parts = ["<ul>" + "".join(f"<li>{E(i)}</li>" for i in x) + "</ul>" if t == "ul" else f"<{t}>{E(x)}</{t}>" for t, x in a["body"]]
        body = f'''<section class="phd phd-s"><div class="wrap">{crumbs_html([("Статьи", "/stati/"), (a["title"], url)])}<h1>{E(a["title"])}</h1><p class="lead-t">{E(a["desc"])}</p></div>{tape()}</section>
<section class="sec"><div class="wrap"><article class="prose">{"".join(parts)}{btns("Здравствуйте! Прочитал статью, нужен мастер.")}</article></div></section>
{sec("Другие статьи", article_cards(), alt=True)}{lead_form()}'''
        sch = {"@context": "https://schema.org", "@type": "Article", "headline": a["title"], "description": a["desc"], "datePublished": TODAY, "dateModified": TODAY,
               "author": {"@id": SITE_URL + "/#org"}, "publisher": {"@id": SITE_URL + "/#org"}, "mainEntityOfPage": SITE_URL + url, "inLanguage": "ru"}
        page(url, f"{a['title']} | {BRAND}", a["desc"], body, [sch], crumbs=[("Статьи", "/stati/"), (a["title"], url)], prio="0.6")
    body = f'''{ph_hero("Статьи", "Памятки и советы: как подготовиться к приезду мастера, повесить телевизор и не допустить протечки.", [("Статьи", "/stati/")], "Здравствуйте! Есть вопрос.")}
{sec("Все статьи", article_cards())}'''
    page("/stati/", f"Статьи и советы мастера | {BRAND}", "Как подготовиться к приезду мастера, на какой высоте вешать телевизор, когда менять подводку.", body, crumbs=[("Статьи", "/stati/")], prio="0.6")

def build_misc():
    groups = "".join(f'<div class="pg"><h3><a href="{curl(c)}">{E(c["name"])}</a></h3><ul>' + "".join(f'<li><a href="{wurl(w)}">{E(w["name"])}</a><span>по фото</span></li>' for w in BY_CAT[c["slug"]]) + "</ul></div>" for c in CATS)
    body = f'''{ph_hero("Цены на услуги мастера", "Ориентир называем по фото задачи, точную стоимость — до начала работ. Выезд по Астане бесплатный.", [("Цены", "/ceny/")], "Здравствуйте! Хочу узнать стоимость работ.", "tag")}
{sec("От чего зависит цена", factors_html())}
{sec("Работы", f'<div class="pgs">{groups}</div>', "Пришлите фото в WhatsApp — назовём ориентир по любой работе из списка.", alt=True)}
{sec("Как мы работаем", steps_html())}{sec("Вопросы", faq_html(FAQ[:6]), alt=True)}{lead_form("Узнать стоимость")}'''
    page("/ceny/", f"Цены на услуги мастера на час в Астане | {BRAND}", "Стоимость сборки мебели, услуг сантехника и электрика в Астане: от чего зависит цена. Ориентир по фото, бесплатный выезд.", body, [faq_schema(FAQ[:6])], crumbs=[("Цены", "/ceny/")], prio="0.8")
    body = f'''{ph_hero(f"О компании «{BRAND}»", "Мастер на час в Астане: сборка мебели, сантехника, электрика, установка и навеска.", [("О нас", "/o-nas/")], MSG, "toolbox")}
<section class="sec"><div class="wrap two"><div class="prose"><h2>Чем занимаемся</h2><p>Выполняем бытовые работы, на которые обычно не хватает времени или инструмента: собираем мебель, меняем сантехнику, устанавливаем розетки и светильники, вешаем телевизоры, карнизы и зеркала.</p><p>Работаем по всем районам Астаны. Выезд бесплатный, на выполненную работу даём гарантию, при первом обращении через WhatsApp — скидка 10%.</p></div><div><ul class="dl">{"".join(f'<li><a href="{curl(x)}">{E(x["name"])}{ui("arrow")}</a></li>' for x in CATS)}</ul></div></div></section>
{perks_html()}{sec("Как мы работаем", steps_html(), alt=True)}{lead_form()}'''
    page("/o-nas/", f"О компании {BRAND} — мастер на час в Астане", f"{BRAND}: сборка мебели, сантехник, электрик, навеска и мелкий ремонт в Астане.", body, crumbs=[("О нас", "/o-nas/")], prio="0.5")
    body = f'''{ph_hero("Контакты", "Позвоните или напишите в WhatsApp — ответим на вопросы и назовём ориентир по стоимости.", [("Контакты", "/kontakty/")], MSG, "chats")}
<section class="sec"><div class="wrap cont"><div><span>Телефон и WhatsApp</span><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></div><div><span>Адрес</span><b>Астана, {ADDRESS}</b></div><div><span>Написать</span><a {wa_attr(MSG)}>WhatsApp</a></div></div></section>
{geo_sec()}{lead_form()}'''
    page("/kontakty/", f"Контакты — {BRAND}, мастер на час в Астане", f"Телефон и WhatsApp {PHONE_DISPLAY}. Астана, {ADDRESS}. Сборка мебели, сантехник, электрик.", body, crumbs=[("Контакты", "/kontakty/")], prio="0.6")
    body = f'''<section class="phd phd-s"><div class="wrap">{crumbs_html([("Политика конфиденциальности", "/privacy-policy/")])}<h1>Политика конфиденциальности</h1></div>{tape()}</section>
<section class="sec"><div class="wrap"><div class="prose"><p>Сайт не хранит персональные данные на своих серверах. Имя, телефон и описание задачи из формы заявки передаются в WhatsApp только после того, как вы сами нажмёте кнопку отправки.</p>
<p>Вопросы в чате на сайте обрабатываются ИИ-консультантом для ответа и не используются для рекламы. Не указывайте в чате лишние личные данные.</p>
<p>Для статистики посещений и оценки рекламы могут использоваться сервисы Google Analytics и Google Ads. При отправке формы номер телефона может передаваться в Google в зашифрованном виде для учёта обращений. Вопросы о данных можно задать по телефону {PHONE_DISPLAY}.</p></div></div></section>'''
    page("/privacy-policy/", f"Политика конфиденциальности — {BRAND}", "Как сайт обрабатывает данные из формы заявки, чата и статистику посещений.", body, crumbs=[("Политика конфиденциальности", "/privacy-policy/")], prio="0.2")
    body = f'''<section class="phd"><div class="wrap"><div class="phd-in"><h1>Страница не найдена</h1><p class="lead-t">Возможно, адрес изменился. Перейдите на главную или выберите работу.</p><div class="btns"><a class="btn btn-p" href="/">На главную</a><a class="btn btn-w" href="/ceny/">Все работы</a></div></div></div>{tape()}</section>'''
    page("/404", f"Страница не найдена — {BRAND}", "Страница не найдена.", body, prio="0")

def build_files():
    PAGES[:] = [p for p in PAGES if p[0] != "/404"]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'] + \
         [f"<url><loc>{SITE_URL}{u}</loc><lastmod>{TODAY}</lastmod><priority>{p}</priority></url>" for u, p in PAGES] + ["</urlset>"]
    (DIST / "sitemap.xml").write_text("\n".join(sm), encoding="utf-8")
    bots = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "PerplexityBot", "Google-Extended", "YandexBot", "Bingbot"]
    (DIST / "robots.txt").write_text("".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots) + f"User-agent: *\nAllow: /\nDisallow: /api/\n\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8")
    llms = [f"# {BRAND} — {BRAND_SUB}", "", "> Мастер на час (муж на час) в Астане: сборка мебели, сантехник, электрик, установка и навеска, мелкий ремонт.", "",
            f"- Телефон и WhatsApp: {PHONE_DISPLAY}", f"- Адрес: Астана, {ADDRESS}", f"- Сайт: {SITE_URL}/",
            "- Выезд по Астане бесплатный; приезд от 40 минут (время согласуется при заявке).", "- Гарантия на выполненную работу; скидка 10% на первое обращение через WhatsApp.",
            "- Стоимость: ориентир по фото задачи, точная цена — до начала работ.", ""]
    for c in CATS:
        llms += [f"## {c['name']}: {SITE_URL}{curl(c)}", c["lead"]] + [f"- {w['name']}: {SITE_URL}{wurl(w)}" for w in BY_CAT[c["slug"]]] + [""]
    llms += ["## Районы"] + [f"- {d['name']}: {SITE_URL}/rayony/{d['slug']}/" for d in DISTRICTS] + ["", "## Частые вопросы"] + [f"- {q} {a}" for q, a in FAQ] + \
            ["", "## Статьи"] + [f"- {a['title']}: {SITE_URL}/stati/{a['slug']}/" for a in ARTICLES]
    (DIST / "llms.txt").write_text("\n".join(llms) + "\n", encoding="utf-8")
    (DIST / "site.webmanifest").write_text(json.dumps({"name": f"{BRAND} — {BRAND_SUB}", "short_name": BRAND, "start_url": "/", "display": "standalone", "background_color": "#15171f", "theme_color": "#15171f",
        "icons": [{"src": "/assets/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "/assets/icon-512.png", "sizes": "512x512", "type": "image/png"}]}, ensure_ascii=False), encoding="utf-8")
    shutil.copytree(ROOT / "assets", DIST / "assets", dirs_exist_ok=True)
    kb = {"phone": PHONE_DISPLAY, "works": [[w["name"], wurl(w), w["slug"]] for w in WORKS], "cats": [[c["name"], curl(c), c["slug"]] for c in CATS],
          "districts": [[d["short"], d["loc"], f"/rayony/{d['slug']}/", 1 if d.get("suburb") else 0] for d in DISTRICTS]}
    js = (ROOT / "src" / "app.js").read_text(encoding="utf-8").replace("/*__KB__*/{}", json.dumps(kb, ensure_ascii=False))
    (DIST / "assets" / "app.js").write_text(js, encoding="utf-8")
    if (ROOT / "assets" / "favicon.ico").exists(): shutil.copy(ROOT / "assets" / "favicon.ico", DIST / "favicon.ico")

if __name__ == "__main__":
    if DIST.exists(): shutil.rmtree(DIST)
    DIST.mkdir()
    build_home(); build_cats(); build_works(); build_districts(); build_articles(); build_misc(); build_files()
    print("pages:", len(PAGES))
