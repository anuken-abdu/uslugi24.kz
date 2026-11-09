# -*- coding: utf-8 -*-
"""Google Ads «Услуги 24» для веб-интерфейса: Инструменты → Массовые действия → Загрузки (xlsx).
Только самые рентабельные запросы: 10 ключей, фразовое соответствие с городом, без широкого. Запуск: python3 src/ads.py → google-ads/"""
import sys, collections
from pathlib import Path
import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Font
sys.path.insert(0, str(Path(__file__).parent))
from data import BRAND, SITE_URL

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "google-ads"
CAMP = "Услуги24 Поиск"
NEG_LIST = "Услуги24 минус-слова"
GEO = "Astana, Kazakhstan"
BUDGET = 5                      # в валюте аккаунта, поменяйте под себя
ERR = []

# Общие заголовки (≤30) и описания (≤90) — только подтверждённые факты со старого сайта
COMMON_H = ["Бесплатный выезд по Астане", "Гарантия на работу", "Скидка 10% через WhatsApp", "Приезд от 40 минут",
            "Пришлите фото — назовём цену", "Все районы Астаны", "Несколько задач за 1 приезд", "Звоните или пишите в WhatsApp",
            "Услуги 24 — мастер на час", "Цену согласуем до начала"]
COMMON_D = ["Бесплатный выезд по Астане, гарантия на работу. Скидка 10% при заявке через WhatsApp.",
            "Пришлите фото задачи в WhatsApp — назовём ориентир по цене и время приезда."]

# (группа, URL, основы запросов, свои заголовки, 2 описания, Path 1)
G = [
    ("Мастер на час", "/", ["муж на час", "мастер на час"],
     ["Мастер на час в Астане", "Муж на час в Астане", "Домашний мастер в Астане", "Сборка, сантехника, электрика", "Мелкий ремонт по дому"],
     ["Мастер на час в Астане: сборка мебели, сантехника, электрика, навеска и мелкий ремонт.",
      "Перечислите задачи — мастер возьмёт инструмент и сделает всё за один приезд."], "мастер-на-час"),
    ("Сборка мебели", "/sborka-mebeli/", ["сборка мебели", "сборщик мебели"],
     ["Сборка мебели в Астане", "Сборщик мебели на дом", "Сборка шкафов и кухонь", "Сборка мебели IKEA", "Кровати, столы, стеллажи"],
     ["Соберём шкаф, кухню, кровать, стол или мебель IKEA по схеме производителя.",
      "Выставим по уровню, отрегулируем двери и ящики, закрепим высокую мебель к стене."], "сборка-мебели"),
    ("Сантехник", "/santehnik/", ["сантехник", "вызвать сантехника"],
     ["Сантехник в Астане", "Сантехник на дом", "Замена смесителя", "Установка унитаза и раковины", "Подводки, сифоны, краны"],
     ["Заменим смеситель, подводку и сифон, установим раковину и унитаз, поменяем краны.",
      "После монтажа проверяем все соединения на протечку. Выезд по Астане бесплатный."], "сантехник"),
    ("Электрик", "/elektrik/", ["электрик", "вызвать электрика"],
     ["Электрик в Астане", "Электрик на дом", "Розетки и выключатели", "Установка люстры", "Замена проводки"],
     ["Установим розетки и выключатели, повесим люстру и светильники, подключим технику.",
      "Работаем при отключённом автомате, проверяем каждую точку после подключения."], "электрик"),
    ("Навеска телевизора", "/ustanovka/naveska-televizora/", ["повесить телевизор", "навеска телевизора"],
     ["Повесим телевизор на стену", "Навеска телевизора в Астане", "Бетон, кирпич, гипсокартон", "Кронштейн под вес ТВ", "Ровно, по уровню"],
     ["Повесим телевизор на кронштейн: на бетон, кирпич или гипсокартон, ровно по уровню.",
      "Подберём высоту и крепёж под вес телевизора, аккуратно уложим провода."], "телевизор"),
]

# Минус-слова (фразовое соответствие): работа, обучение, товары, соцсервисы, другие города, «не наши» услуги и мусор под «муж на час»
NEG = ["вакансия", "вакансии", "работа", "работу", "требуется", "требуются", "резюме", "зарплата", "подработка", "обучение", "курсы", "учиться",
       "своими руками", "как", "видео", "youtube", "схема", "инструкция", "скачать", "форум",
       "купить", "магазин", "продажа", "продам", "оптом", "бу", "б/у", "olx", "крыша", "kaspi", "каспи", "2гис", "naimi", "найми", "профи",
       "алматы", "шымкент", "караганда", "кокшетау", "павлодар", "актобе",
       "под ключ", "ремонт холодильника", "ремонт холодильников", "ремонт стиральной", "ремонт стиральных", "ремонт телевизора", "ремонт телевизоров",
       "автоэлектрик", "авто", "автомобиля", "газ", "газовой", "горгаз", "аварийная служба", "водоканал", "астана су", "кск", "оси", "жкх", "акимат", "энергосбыт",
       "лицензия", "допуск", "разряд", "изготовление", "на заказ", "мебельный цех", "грузчик", "грузчики", "газель",
       "знакомства", "интим", "секс", "эскорт", "фильм", "сериал", "песня", "анекдот", "смотреть", "онлайн", "маникюр", "массаж", "парикмахер", "тату"]

def chk(t, n, what):
    if len(t) > n: ERR.append(f"{what} >{n}: {t} ({len(t)})")
    return t

def headlines(hs):
    out = []
    for t in hs + COMMON_H:
        if t.lower() not in {x.lower() for x in out}: out.append(t)
    return out[:15]

def xlsx(path, cols, rows):
    wb = Workbook(); ws = wb.active; ws.title = "Upload"; ws.append(cols)
    for c in ws[1]: c.font = Font(bold=True)
    for r in rows: ws.append([r.get(c, "") for c in cols])
    for i, c in enumerate(cols, 1): ws.column_dimensions[ws.cell(1, i).column_letter].width = max(14, min(48, len(c) + 4))
    wb.save(path)

def campaigns_file(path, template):
    wb = openpyxl.load_workbook(template)
    for n in list(wb.sheetnames):
        if n.startswith("(Example)"): del wb[n]
    ws = wb[wb.sheetnames[0]]
    hdr = [c.value for c in ws[2]]
    if "EU political ads" not in hdr:
        ws.cell(1, len(hdr) + 1, "#Required: EU political ads"); ws.cell(2, len(hdr) + 1, "EU political ads"); hdr.append("EU political ads")
    r = {"Action": "Add", "Campaign status": "Paused", "Campaign": CAMP, "Campaign type": "Search", "Networks": "Google search",
         "Budget": BUDGET, "Budget type": "Daily", "Bid strategy type": "Maximize clicks", "Location": GEO, "EU political ads": "No"}
    ws.append([r.get(h) for h in hdr])
    wb.save(path)

def main():
    OUT.mkdir(exist_ok=True)
    for f in OUT.glob("*"):
        if f.is_file(): f.unlink()
    H = [f"Headline {i}" for i in range(1, 16)]; D = [f"Description {i}" for i in range(1, 5)]
    grp, kws, ads, txt = [], [], [], []
    seen = collections.Counter()
    for name, path, base, hs, ds, p1 in G:
        grp.append({"Action": "Add", "Campaign": CAMP, "Ad group": name, "Ad group state": "Enabled"})
        words = []
        for b in base:
            words.append(f'"{b} астана"')
        words = list(dict.fromkeys(words))
        for w in words:
            seen[w] += 1; plain = w.strip('"[]')
            kws.append({"Action": "Add", "Campaign": CAMP, "Ad group": name, "Keyword": w})
            for ng in NEG:
                if f" {ng} " in f" {plain} ": ERR.append(f"минус «{ng}» режет «{plain}»")
        heads = headlines(hs); descs = ds + COMMON_D
        if len(heads) != 15: ERR.append(f"{name}: заголовков {len(heads)}")
        url = SITE_URL + path
        r = {"Action": "Add", "Campaign": CAMP, "Ad group": name, "Ad type": "Responsive search ad", "Final URL": url, "Path 1": chk(p1, 15, "path1"), "Path 2": "астана"}
        for i, h in enumerate(heads): r[H[i]] = chk(h, 30, "headline")
        for i, d in enumerate(descs): r[D[i]] = chk(d, 90, "description")
        ads.append(r)
        txt += [f"Группа: {name} ({len(words)} ключей)", f"URL: {url}", "Ключи: " + ", ".join(words), "Заголовки: " + " | ".join(heads), "Описания: " + " | ".join(descs), ""]
    dup = [k for k, v in seen.items() if v > 1]
    if dup: ERR.append(f"дубли между группами: {dup[:6]}")
    if ERR: print("\n".join(ERR[:40])); raise SystemExit(1)
    campaigns_file(OUT / "0-sozdat-kampaniyu.xlsx", ROOT / "src" / "templates" / "Create_New_Campaigns.xlsx")
    xlsx(OUT / "1-gruppy.xlsx", ["Action", "Campaign", "Ad group", "Ad group state"], grp)
    xlsx(OUT / "2-klyuchevye-slova.xlsx", ["Action", "Campaign", "Ad group", "Keyword"], kws)
    xlsx(OUT / "3-obyavleniya.xlsx", ["Action", "Campaign", "Ad group", "Ad type"] + H + D + ["Path 1", "Path 2", "Final URL"], ads)
    xlsx(OUT / "4-minus-slova-v-spisok.xlsx", ["Action", "Negative keyword list name", "Negative keyword", "Keyword or list", "Match type"],
         [{"Action": "Add", "Negative keyword list name": NEG_LIST, "Negative keyword": x, "Keyword or list": "Keyword", "Match type": "Phrase Match"} for x in NEG])
    xlsx(OUT / "5-privyazat-spisok-k-kampanii.xlsx", ["Action", "Negative keyword", "Keyword or list", "Campaign"],
         [{"Action": "Add", "Negative keyword": NEG_LIST, "Keyword or list": "List", "Campaign": CAMP}])
    ext = ["", "РАСШИРЕНИЯ (добавить вручную: Объявления → Ресурсы)",
           "Уточнения: Бесплатный выезд · Гарантия на работу · Приезд от 40 минут · Скидка 10% через WhatsApp · Все районы Астаны · Несколько задач за 1 приезд",
           "Быстрые ссылки:"] + [f"  {n} — {SITE_URL}{p}" for n, p, *_ in G[1:]] + [f"  Цены — {SITE_URL}/ceny/", f"  Контакты — {SITE_URL}/kontakty/",
           f"Звонок: +7 702 891 02 57", "",
           "НАСТРОЙКИ ПОСЛЕ ЗАГРУЗКИ (важно, иначе сольётся бюджет):",
           "  • Сети: только Google Поиск — снять «Поисковые партнёры» и «Контекстно-медийная сеть»",
           "  • AI Max для поисковых кампаний — выключен; «Широкое соответствие» на уровне кампании — выключено",
           "  • Местоположение: «Присутствие: люди, которые находятся в выбранных местах» (не «интересуются»)",
           "  • Язык: русский и казахский",
           "  • Через 2–3 дня: Ключевые слова → Поисковые запросы, мусор — в список минус-слов"]
    head = [f"КАМПАНИЯ: {CAMP} (создаётся файлом 0, на паузе)", f"Местоположение: {GEO}", f"Бюджет: {BUDGET} в день (в валюте аккаунта)",
            f"Групп: {len(grp)}, ключей: {len(kws)}, минус-слов: {len(NEG)}", ""]
    (OUT / "6-teksty-i-nastroyki.txt").write_text("\n".join(head + txt + ext) + "\n", encoding="utf-8")
    print("групп", len(grp), "ключей", len(kws), "объявлений", len(ads), "минус", len(NEG))

if __name__ == "__main__":
    main()
