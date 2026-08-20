#!/usr/bin/env python3
"""Generate realistic product UI screenshots for the PharmaBrain landing."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = Path(__file__).resolve().parents[1] / "images" / "products"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1440, 900
NAVY = (11, 31, 58)
NAVY2 = (18, 42, 74)
TEAL = (13, 155, 138)
TEAL_D = (10, 122, 110)
AI_BG = (230, 247, 244)
BG = (244, 247, 251)
WHITE = (255, 255, 255)
TEXT = (22, 36, 54)
MUTED = (107, 124, 143)
LINE = (226, 232, 240)
SOFT = (236, 241, 247)
GREEN = (47, 163, 107)
AMBER = (217, 149, 42)
RED = (214, 82, 82)
BLUE = (58, 110, 165)
PURPLE = (99, 102, 241)

FONT_R = "/System/Library/Fonts/Supplemental/Arial.ttf"
FONT_B = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"


def font(size, bold=False):
    return ImageFont.truetype(FONT_B if bold else FONT_R, size)


def rr(draw, xy, r, fill=None, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=width)


def shadow(base, box, r=16, blur=18, alpha=40):
    x0, y0, x1, y1 = box
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle((x0 + 4, y0 + 8, x1 + 4, y1 + 10), radius=r, fill=(0, 0, 0, alpha))
    return Image.alpha_composite(base, layer.filter(ImageFilter.GaussianBlur(blur)))


def text(draw, xy, s, size=14, bold=False, fill=TEXT, anchor="lt"):
    draw.text(xy, s, font=font(size, bold), fill=fill, anchor=anchor)


def chip(draw, x, y, label, bg, fg, pad_x=10):
    f = font(12, True)
    tw = f.getlength(label)
    rr(draw, (x, y, x + tw + pad_x * 2, y + 22), 11, fill=bg)
    draw.text((x + pad_x, y + 11), label, font=f, fill=fg, anchor="lm")
    return int(tw + pad_x * 2 + 8)


def progress(draw, x, y, w, pct, color=TEAL):
    rr(draw, (x, y, x + w, y + 8), 4, fill=SOFT)
    rr(draw, (x, y, x + int(w * pct), y + 8), 4, fill=color)


def chrome(product, nav, active):
    img = Image.new("RGBA", (W, H), (*BG, 255))
    d = ImageDraw.Draw(img)

    # window chrome
    rr(d, (0, 0, W, H), 0, fill=BG)
    d.rectangle((0, 0, W, 52), fill=WHITE)
    d.line((0, 52, W, 52), fill=LINE, width=1)
    for i, c in enumerate([(255, 95, 87), (255, 189, 46), (39, 201, 63)]):
        d.ellipse((16 + i * 18, 18, 28 + i * 18, 30), fill=c)

    text(d, (88, 26), "ФарМозг", 16, True, NAVY, "lm")
    d.rectangle((178, 18, 179, 34), fill=LINE)
    text(d, (192, 26), product, 15, True, TEXT, "lm")

    rr(d, (520, 12, 920, 40), 8, fill=BG)
    text(d, (536, 26), "Поиск по записям, документам, ID…", 12, False, MUTED, "lm")

    rr(d, (1288, 12, 1418, 40), 8, fill=AI_BG)
    text(d, (1353, 26), "AI включён", 12, True, TEAL_D, "mm")

    # sidebar
    d.rectangle((0, 52, 228, H), fill=NAVY)
    text(d, (20, 76), "НАВИГАЦИЯ", 10, True, (140, 168, 196))
    y = 98
    for item in nav:
        on = item == active
        if on:
            rr(d, (10, y - 8, 218, y + 24), 8, fill=NAVY2)
            d.rectangle((10, y - 8, 14, y + 24), fill=TEAL)
        text(d, (28, y + 8), item, 13, on, WHITE if on else (186, 204, 222), "lm")
        y += 40
    text(d, (20, H - 48), "Закрытый контур  ·  GxP", 11, False, (140, 168, 196))
    return img


def ai_panel(draw, x, title, items, actions=None):
    rr(draw, (x, 68, W - 24, H - 24), 16, fill=WHITE, outline=LINE)
    rr(draw, (x, 68, W - 24, 118), 16, fill=AI_BG)
    draw.rectangle((x, 102, W - 24, 118), fill=AI_BG)
    text(draw, (x + 20, 93), "✦  " + title, 15, True, TEAL_D, "lm")
    y = 138
    for kind, heading, body in items:
        color = {"ok": GREEN, "warn": AMBER, "risk": RED, "ai": TEAL}.get(kind, TEAL)
        rr(draw, (x + 16, y, W - 40, y + 92), 12, fill=BG)
        ddot = (x + 28, y + 18, x + 36, y + 26)
        draw.ellipse(ddot, fill=color)
        text(draw, (x + 46, y + 16), heading, 13, True)
        # wrap body
        words = body.split()
        line, yy = "", y + 38
        f = font(12)
        for w in words:
            test = (line + " " + w).strip()
            if f.getlength(test) > 250:
                text(draw, (x + 46, yy), line, 12, False, MUTED)
                yy += 16
                line = w
            else:
                line = test
        if line:
            text(draw, (x + 46, yy), line, 12, False, MUTED)
        y += 104
    if actions:
        ay = H - 78
        for i, a in enumerate(actions):
            fill = TEAL if i == 0 else WHITE
            fg = WHITE if i == 0 else TEXT
            ww = 130 if i == 0 else 118
            rr(draw, (x + 16 + i * 142, ay, x + 16 + i * 142 + ww, ay + 36), 8, fill=fill, outline=None if i == 0 else LINE)
            text(draw, (x + 16 + i * 142 + ww / 2, ay + 18), a, 12, True, fg, "mm")


def field(draw, x, y, w, label, value, ai=False):
    text(draw, (x, y), label, 11, True, MUTED)
    rr(draw, (x, y + 18, x + w, y + 52), 8, fill=WHITE, outline=TEAL if ai else LINE, width=2 if ai else 1)
    text(draw, (x + 12, y + 35), value, 13, False, TEXT, "lm")
    if ai:
        text(draw, (x + w - 10, y + 35), "AI", 10, True, TEAL, "rm")


def table(draw, x, y, w, headers, rows, colw=None):
    if colw is None:
        colw = [w // len(headers)] * len(headers)
    rr(draw, (x, y, x + w, y + 36 + 36 * len(rows)), 12, fill=WHITE, outline=LINE)
    xx = x + 16
    for i, h in enumerate(headers):
        text(draw, (xx, y + 18), h, 11, True, MUTED, "lm")
        xx += colw[i]
    draw.line((x, y + 36, x + w, y + 36), fill=LINE)
    for ri, row in enumerate(rows):
        yy = y + 36 + ri * 36
        if ri % 2 == 0:
            draw.rectangle((x + 1, yy, x + w - 1, yy + 36), fill=(250, 252, 254))
        xx = x + 16
        for i, cell in enumerate(row):
            if isinstance(cell, tuple):
                chip(draw, xx, yy + 7, cell[0], cell[1], cell[2])
            else:
                text(draw, (xx, yy + 18), str(cell), 13, False, TEXT, "lm")
            xx += colw[i]


def kpi(draw, x, y, w, label, value, sub, color=TEAL):
    rr(draw, (x, y, x + w, y + 92), 14, fill=WHITE, outline=LINE)
    text(draw, (x + 16, y + 18), label, 11, True, MUTED)
    text(draw, (x + 16, y + 48), value, 22, True, TEXT)
    text(draw, (x + 16, y + 74), sub, 11, False, color)


SCREENS = []


def add(spec):
    SCREENS.append(spec)


# ---------- screens ----------
add(dict(
    file="eln.png", product="AI-ELN  ·  Experiment EXP-1842",
    nav=["Experiments", "Protocols", "Samples", "Results", "Reports"], active="Experiments",
    draw=lambda d: (
        text(d, (252, 80), "Experiment  EXP-1842", 22, True),
        chip(d, 252, 112, "In progress", (232, 244, 255), BLUE),
        field(d, 252, 150, 430, "Цель эксперимента", "Оценить стабильность API при 40 °C / 75% RH", True),
        field(d, 698, 150, 250, "Методика", "ICH Q1A(R2)", False),
        field(d, 252, 220, 340, "Образец", "API-Batch B-09 / 12.4 mg", False),
        field(d, 608, 220, 340, "Параметры к фиксации  ·  AI", "t, RH, assay, impurity A/B, pH", True),
        table(d, 252, 300, 696, ["Этап", "Параметр", "План", "Факт"],
              [["1. Подготовка", "Температура", "40.0 °C", "40.1 °C"],
               ["2. Экспозиция", "Влажность", "75 % RH", "74.8 % RH"],
               ["3. Assay HPLC", "Содержание", "98.0–102.0", ("99.2 %", AI_BG, TEAL_D)]],
              [200, 170, 160, 140]),
    ),
    ai=("Experiment Assistant", [
        ("ai", "Структура эксперимента", "Предложены 5 этапов и 8 обязательных параметров по цели и методике ICH Q1A."),
        ("warn", "Result Review", "Impurity B = 0.42% — выше исторического диапазона 0.18–0.31% (n=14)."),
        ("ok", "Next Experiment", "Снизить RH до 60% и добавить точку на 14 день. Похожий EXP-1711."),
    ], ["Принять draft", "Изменить"]),
))

add(dict(
    file="lims.png", product="AI-LIMS  ·  Sample SMP-4419",
    nav=["Samples", "Test Requests", "Results", "Specifications", "OOS", "COA"], active="Results",
    draw=lambda d: (
        text(d, (252, 80), "Test Result  ·  Sample SMP-4419", 22, True),
        chip(d, 252, 112, "Specification check", AI_BG, TEAL_D),
        kpi(d, 252, 150, 218, "Assay", "101.4 %", "Spec 98.0–102.0", GREEN),
        kpi(d, 486, 150, 218, "Impurity A", "0.18 %", "Spec ≤ 0.20", AMBER),
        kpi(d, 720, 150, 218, "pH", "5.1", "Spec 4.5–5.5", GREEN),
        table(d, 252, 268, 696, ["Тест", "Метод", "Результат", "vs history"],
              [["Assay", "HPLC-UV", "101.4 %", ("OK", (226, 245, 234), GREEN)],
               ["Impurity A", "HPLC", "0.18 %", ("High vs hist.", (255, 243, 224), AMBER)],
               ["ID", "FTIR", "Corresponds", ("OK", (226, 245, 234), GREEN)],
               ["Microbial", "Ph. Eur. 2.6.12", "In progress", ("—", SOFT, MUTED)]],
              [170, 170, 160, 170]),
    ),
    ai=("Result Check", [
        ("warn", "Близко к пределу spec", "Impurity A 0.18% при лимите 0.20%. Исторический mean 0.11% (σ=0.03)."),
        ("ai", "Sample Classification", "Готовый продукт, серия FP-2026-07. Рекомендованы Assay, ID, Impurities, Micro."),
        ("ok", "COA Assistant", "Draft Certificate of Analysis готов из утверждённых результатов."),
    ], ["Создать OOS", "Draft COA"]),
))

add(dict(
    file="sdms.png", product="AI-SDMS  ·  Dataset DS-77",
    nav=["Datasets", "Experiments", "Instruments", "Projects", "Documents"], active="Datasets",
    draw=lambda d: (
        text(d, (252, 80), "Dataset  ·  HPLC_stability_40C.raw", 20, True),
        chip(d, 252, 112, "Classified: chromatogram", AI_BG, TEAL_D),
        field(d, 252, 150, 330, "Experiment", "EXP-1842  ·  Stability API", True),
        field(d, 598, 150, 350, "Sample / Result", "SMP-4419  →  Assay 101.4%", True),
        field(d, 252, 220, 696, "Извлечённые metadata", "Instrument Agilent 1260  ·  Method M-HPLC-04  ·  2026-08-12 14:22", True),
        table(d, 252, 300, 696, ["Похожие эксперименты", "Параметры", "Assay", "Match"],
              [["EXP-1711", "40 °C / 75% RH", "99.8 %", "0.92"],
               ["EXP-1680", "40 °C / 75% RH", "100.1 %", "0.88"],
               ["EXP-1544", "25 °C / 60% RH", "101.0 %", "0.61"]],
              [200, 200, 140, 120]),
    ),
    ai=("Scientific Search", [
        ("ai", "Классификация файла", "HPLC RAW chromatogram. Metadata извлечены из header и имени файла."),
        ("ok", "Связи", "Dataset → EXP-1842 → SMP-4419 → Result Assay."),
        ("ai", "Вопрос лаборатории", "«Какие эксперименты 40°C дали impurity B > 0.3%?» — 4 записи."),
    ], ["Привязать", "Задать вопрос"]),
))

add(dict(
    file="edc.png", product="AI-EDC  ·  Subject 014-088  ·  Visit 3",
    nav=["Subjects", "CRF", "Visits", "Lab Results", "AE", "Queries"], active="CRF",
    draw=lambda d: (
        text(d, (252, 80), "CRF  ·  Vital Signs  ·  Visit 3", 22, True),
        chip(d, 252, 112, "Data Review", (255, 243, 224), AMBER),
        field(d, 252, 150, 220, "SBP, mmHg", "168", True),
        field(d, 488, 150, 220, "DBP, mmHg", "94", False),
        field(d, 724, 150, 220, "HR, bpm", "78", False),
        field(d, 252, 220, 220, "Weight, kg", "81.2", False),
        field(d, 488, 220, 220, "AE related", "Hypertension (ongoing)", True),
        table(d, 252, 300, 696, ["Поле", "Значение", "Связанные данные", "Статус"],
              [["SBP", "168", "Baseline 128; AE Hypertension", ("Contradiction", (255, 232, 232), RED)],
               ["Concomitant", "Lisinopril 10 mg", "Started Visit 2", ("OK", (226, 245, 234), GREEN)],
               ["Lab K+", "3.1 mmol/L", "Low vs protocol", ("Query draft", (255, 243, 224), AMBER)]],
              [160, 170, 230, 130]),
    ),
    ai=("Query Assistant", [
        ("risk", "Противоречие данных", "SBP 168 не согласуется с baseline 128 и AE «Hypertension» без change in medication."),
        ("ai", "Draft query", "Please confirm SBP at Visit 3 and whether antihypertensive dose was changed."),
        ("ok", "Medical Coding", "Hypertension → MedDRA 10020772 Essential hypertension."),
    ], ["Создать query", "Принять код"]),
))

add(dict(
    file="ctms.png", product="AI-CTMS  ·  Study PB-301",
    nav=["Studies", "Countries", "Sites", "Investigators", "Milestones", "Issues"], active="Sites",
    draw=lambda d: (
        text(d, (252, 80), "Site risk  ·  PB-301", 22, True),
        kpi(d, 252, 120, 218, "Sites at risk", "7 / 42", "score > 70", RED),
        kpi(d, 486, 120, 218, "Recruitment", "186 / 240", "forecast 11 нед.", AMBER),
        kpi(d, 720, 120, 218, "Open issues", "23", "12 без owner", AMBER),
        table(d, 252, 236, 696, ["Site", "Recruit", "Queries", "Risk", "Forecast"],
              [["RU-014 Moscow", "18 / 24", "12.4%", ("82", (255, 232, 232), RED), "stock-out 18d"],
               ["RU-021 Kazan", "11 / 16", "4.1%", ("44", (226, 245, 234), GREEN), "on track"],
               ["KZ-003 Almaty", "6 / 12", "9.8%", ("71", (255, 243, 224), AMBER), "slow"],
               ["BY-002 Minsk", "9 / 10", "3.2%", ("28", (226, 245, 234), GREEN), "ahead"]],
              [180, 120, 110, 110, 150]),
    ),
    ai=("Site Risk & Forecast", [
        ("risk", "Site RU-014", "Высокий query rate, 3 protocol deviations, отставание recruitment."),
        ("ai", "Visit Report", "Заметки CRA преобразованы в структурированный отчёт: 4 action items."),
        ("ok", "Action Tracker", "Из minutes steering committee созданы 6 Action с owner и due date."),
    ], ["Открыть issue", "Прогноз"]),
))

add(dict(
    file="etmf.png", product="AI-eTMF  ·  Study PB-301  ·  Site RU-014",
    nav=["Documents", "Artifacts", "Studies", "Sites", "Reviews", "Completeness"], active="Documents",
    draw=lambda d: (
        text(d, (252, 80), "Document classification", 22, True),
        chip(d, 252, 112, "CV_Ivanov_PI_v3.pdf", SOFT, TEXT),
        field(d, 252, 150, 330, "Artifact", "01.02.03  Investigator CV", True),
        field(d, 598, 150, 350, "Study / Site", "PB-301  ·  RU-014 Moscow", True),
        field(d, 252, 220, 330, "Document type", "Curriculum Vitae", True),
        field(d, 598, 220, 350, "Metadata", "Date 12.03.2026  ·  PI Ivanov A.S.", True),
        table(d, 252, 300, 696, ["Обязательный Artifact", "Статус", "Проблема"],
              [["FDA 1572 / Local equivalent", ("Missing", (255, 232, 232), RED), "Нет файла"],
               ["Financial disclosure", ("QA fail", (255, 243, 224), AMBER), "Версия 1.1, нужна 1.2"],
               ["IB acknowledgement", ("Complete", (226, 245, 234), GREEN), "—"]],
              [260, 150, 250]),
    ),
    ai=("TMF Completeness", [
        ("ai", "Классификация", "Investigator CV, Study PB-301, Site RU-014. Обязательные поля заполнены."),
        ("risk", "Inspection Readiness", "По Site RU-014 отсутствует 4 Artifact и 2 документа не той версии."),
        ("warn", "Cross-document", "Дата в CV не совпадает с датой в Site Staff List."),
    ], ["Разместить", "Список gaps"]),
))

add(dict(
    file="rtsm.png", product="AI-RTSM  ·  Drug inventory",
    nav=["Subjects", "Randomization", "Inventory", "Shipments", "Depots", "Forecast"], active="Inventory",
    draw=lambda d: (
        text(d, (252, 80), "Trial supply  ·  Product X  50 mg", 22, True),
        kpi(d, 252, 120, 218, "Sites stock-out", "5", "в ближайшие 21 день", RED),
        kpi(d, 486, 120, 218, "Next shipment", "420 pack", "рекомендация AI", TEAL),
        kpi(d, 720, 120, 218, "Anomaly", "Site RU-014", "расход +38%", AMBER),
        table(d, 252, 236, 696, ["Site", "On hand", "Burn rate", "Stock-out", "Next qty"],
              [["RU-014", "48", "4.2 /нед", "18 дней", "72"],
               ["RU-021", "110", "2.1 /нед", "> 60 дней", "0"],
               ["KZ-003", "22", "3.0 /нед", "12 дней", "60"]],
              [140, 120, 140, 140, 120]),
    ),
    ai=("Supply Forecast", [
        ("risk", "Stock-out RU-014", "Прогноз исчерпания 18 дней при текущем recruitment."),
        ("ai", "Перераспределение", "Можно переместить 40 упаковок с RU-021 (избыток)."),
        ("warn", "Необычный расход", "Site RU-014: расход +38% к плану рандомизации."),
    ], ["Создать shipment", "Перераспределить"]),
))

add(dict(
    file="startup.png", product="AI-Study Startup  ·  Site RU-033",
    nav=["Sites", "Feasibility", "Countries", "Documents", "Tasks", "Contracts"], active="Feasibility",
    draw=lambda d: (
        text(d, (252, 80), "Site suitability  ·  RU-033", 22, True),
        kpi(d, 252, 120, 218, "Suitability", "78 / 100", "протокол PB-301", TEAL),
        kpi(d, 486, 120, 218, "Docs missing", "6", "из 18 обязательных", AMBER),
        kpi(d, 720, 120, 218, "Ready date", "12 окт", "прогноз по задачам", BLUE),
        table(d, 252, 236, 696, ["Требование протокола", "Ответ Site", "Match"],
              [["ICU on site", "Yes", ("OK", (226, 245, 234), GREEN)],
               ["MRI 3T", "1.5T only", ("Gap", (255, 243, 224), AMBER)],
               ["Target pop. /мес", "4–6", ("OK", (226, 245, 234), GREEN)]],
              [260, 200, 180]),
    ),
    ai=("Startup Assistant", [
        ("ai", "Feasibility extract", "Данные извлечены из опросника и презентации клиники."),
        ("warn", "Документы", "Отсутствуют: ethics approval, CDA signed, lab certifications."),
        ("ok", "Прогноз готовности", "12 октября при текущем темпе закрытия задач."),
    ], ["Чек-лист docs", "Сохранить score"]),
))

add(dict(
    file="ecoa.png", product="AI-eCOA  ·  Patient 014-088",
    nav=["Questionnaires", "Responses", "Visits", "Assessments", "Alerts"], active="Responses",
    draw=lambda d: (
        text(d, (252, 80), "ePRO diary  ·  Subject 014-088", 22, True),
        chip(d, 252, 112, "Adherence alert", (255, 232, 232), RED),
        kpi(d, 252, 150, 218, "Adherence 14д", "61 %", "ниже порога 80%", RED),
        kpi(d, 486, 150, 218, "Pain score", "6 → 8", "рост 3 дня подряд", AMBER),
        kpi(d, 720, 150, 218, "Alerts", "2 open", "pattern + score", AMBER),
        table(d, 252, 268, 696, ["День", "Заполнено", "Pain", "Паттерн"],
              [["D12", "07:02", "6", "OK"],
               ["D13", "—", "—", ("Missed", (255, 232, 232), RED)],
               ["D14", "23:48", "8", ("Late + copy", (255, 243, 224), AMBER)],
               ["D15", "23:51", "8", ("Identical text", (255, 243, 224), AMBER)]],
              [120, 160, 120, 250]),
    ),
    ai=("Response Patterns", [
        ("risk", "Несоблюдение режима", "Пропуски и заполнение после полуночи 4 дня из 7."),
        ("warn", "Одинаковые ответы", "Свободный текст D14–D15 совпадает. Возможна низкая вовлечённость."),
        ("ai", "Summary динамики", "Боль растёт, сон ухудшается. Alert по комбинации Pain≥8 и missed dose."),
    ], ["Создать alert", "Summary"]),
))

add(dict(
    file="rim.png", product="AI-RIM  ·  Product Cardioxil 20 mg",
    nav=["Products", "Substances", "Manufacturers", "Activities", "Authorities", "Commitments"], active="Products",
    draw=lambda d: (
        text(d, (252, 80), "Product  ·  Cardioxil 20 mg tablets", 20, True),
        field(d, 252, 130, 330, "Substance", "Cardioxilum  ·  INN confirmed", True),
        field(d, 598, 130, 350, "Manufacturer", "Site A, Moscow  ·  GMP cert 2027", False),
        field(d, 252, 200, 696, "Regulatory activity", "Variation type IB  ·  EMA + Minzdrav  ·  in progress", False),
        table(d, 252, 286, 696, ["Связь", "Объект", "Статус", "Противоречие"],
              [["Product→MAH", "PharmaBrain LLC", "Active", "—"],
               ["Manufacturer", "Site A vs dossier Site B", "Mismatch", ("Data conflict", (255, 232, 232), RED)],
               ["Commitment", "PSUR 30.09.2026", "Open", ("Extracted", AI_BG, TEAL_D)]],
              [180, 250, 120, 140]),
    ),
    ai=("Regulatory metadata", [
        ("risk", "Противоречие продукта", "В Module 3 указан Site B, в RIM — Site A."),
        ("ai", "Correspondence", "Письмо регулятора классифицировано как Request for information."),
        ("ok", "Commitment", "Из письма извлечено обязательство: предоставить PSUR до 30.09.2026."),
    ], ["Создать задачу", "Сверить dossier"]),
))

add(dict(
    file="ectd.png", product="AI-eCTD  ·  Sequence 0024",
    nav=["Submissions", "Sequences", "Documents", "Modules", "Validation", "Questions"], active="Documents",
    draw=lambda d: (
        text(d, (252, 80), "Submission  ·  eCTD seq 0024", 22, True),
        chip(d, 252, 112, "Validation: 2 errors, 5 warnings", (255, 243, 224), AMBER),
        field(d, 252, 150, 430, "Документ", "2.7.3 Summary of Clinical Efficacy.docx", False),
        field(d, 698, 150, 250, "Module / leaf", "m2.7.3  ·  replace", True),
        table(d, 252, 230, 696, ["Check", "Seq 0023", "Seq 0024", "Impact"],
              [["Module 2.5", "v3", "v4", "Related 2.7.3 outdated"],
               ["3.2.P.5.1", "spec v8", "spec v8", "OK"],
               ["1.2 Admin", "complete", "missing annex", ("Required", (255, 232, 232), RED)]],
              [180, 150, 170, 180]),
    ),
    ai=("Submission Assistant", [
        ("ai", "Место в dossier", "Документ относится к Module 2.7.3, lifecycle operation: replace."),
        ("warn", "Связанные обновления", "Изменение 2.5 требует обновления 2.7.3 и 5.3.5.1."),
        ("ok", "Draft ответа", "Подготовлен ответ на вопрос регулятора Q-14 на основе утверждённого dossier."),
    ], ["Draft ответа", "Сравнить seq"]),
))

add(dict(
    file="regint.png", product="AI-Regulatory Intelligence",
    nav=["Regulations", "Authorities", "Changes", "Products", "Impact", "Actions"], active="Changes",
    draw=lambda d: (
        text(d, (252, 80), "Regulatory change  ·  EMA Q&A update", 20, True),
        chip(d, 252, 112, "Impact assessment", (232, 244, 255), BLUE),
        field(d, 252, 150, 696, "Источник", "EMA  ·  Nitrosamines Q&A rev. 21  ·  published 04.08.2026", False),
        table(d, 252, 230, 696, ["Изменение", "Затронутый Product", "Process", "Действие"],
              [["New testing limit", "Cardioxil 20 mg", "QC spec", "Review spec"],
               ["Documentation", "Cardioxil 5/20", "Module 3.2.P.5", "Update dossier"],
               ["Supplier", "API Cardioxilum", "Change control", "Open CC"]],
              [200, 180, 160, 140]),
    ),
    ai=("Change extraction", [
        ("ai", "Новые требования", "Извлечены 3 изменившихся пункта относительно rev. 20."),
        ("ok", "Затронутые объекты", "2 Products, QC spec, Module 3, incoming inspection SOP."),
        ("ai", "Пересмотреть", "Список: SOP-QC-044, spec SP-API-12, eCTD 3.2.P.5.1."),
    ], ["Impact draft", "Создать Action"]),
))

add(dict(
    file="safety.png", product="AI-Safety Case  ·  CASE-2026-1184",
    nav=["Cases", "Sources", "Patients", "Drugs", "Events", "Narratives"], active="Cases",
    draw=lambda d: (
        text(d, (252, 80), "Incoming source  ·  potential ICSR", 20, True),
        chip(d, 252, 112, "Duplicate check: 1 possible", (255, 243, 224), AMBER),
        field(d, 252, 150, 330, "Patient", "Male, 62 y  ·  initials I.A.", True),
        field(d, 598, 150, 350, "Drug / Event", "Cardioxil 20 mg  ·  Angioedema", True),
        field(d, 252, 220, 330, "Dates", "Onset 08.08.2026  ·  received 11.08", True),
        field(d, 598, 220, 350, "MedDRA", "10002424 Angioedema  ·  PT", True),
        table(d, 252, 300, 696, ["Проверка", "Результат", "Комментарий"],
              [["ICSR?", ("Yes", AI_BG, TEAL_D), "Serious, labelled unexpected"],
               ["Duplicate", "CASE-2026-1171", "Same patient + event + 3 days"],
               ["Missing", "Outcome, lot number", "Follow-up questions drafted"]],
              [160, 200, 300]),
    ),
    ai=("Case intake", [
        ("ai", "Это ICSR", "Серьёзное незарегистрированное событие. Обязательные элементы извлечены."),
        ("warn", "Возможный duplicate", "CASE-2026-1171: тот же reporter и препарат, onset ±3 дня."),
        ("ok", "Draft narrative", "Сформирован narrative и 4 follow-up вопроса по отсутствующим данным."),
    ], ["Создать Case", "Связать duplicate"]),
))

add(dict(
    file="signal.png", product="AI-Signal Management  ·  SIG-044",
    nav=["Signals", "Products", "Events", "Evidence", "Assessments", "Actions"], active="Signals",
    draw=lambda d: (
        text(d, (252, 80), "Signal  ·  Cardioxil — Angioedema", 22, True),
        kpi(d, 252, 120, 218, "PRR", "3.8", "выше порога 2.0", RED),
        kpi(d, 486, 120, 218, "Cases", "27", "4 источника", TEAL),
        kpi(d, 720, 120, 218, "Trend 12м", "+46%", "частота растёт", AMBER),
        table(d, 252, 236, 696, ["Evidence", "Источник", "N", "Роль"],
              [["ICSRs spontaneous", "Safety DB", "19", "Primary"],
               ["Literature", "PubMed / EMEA", "5", "Supporting"],
               ["Clinical AE", "PB-301", "3", "Supporting"]],
              [240, 180, 80, 160]),
    ),
    ai=("Signal detection", [
        ("risk", "Необычная комбинация", "Drug–Event PRR 3.8, χ² значим. Рост частоты с Q1 2026."),
        ("ai", "Объединение источников", "27 сообщений схлопнуты в один потенциальный сигнал SIG-044."),
        ("ok", "Draft assessment", "Подготовлен Signal Assessment: biological plausibility + labelledness."),
    ], ["Draft assessment", "Открыть Action"]),
))

add(dict(
    file="pvrpt.png", product="AI-PV Aggregate  ·  PBRER 2026",
    nav=["PSUR/PBRER", "DSUR", "RMP", "Sections", "Data Sources", "References"], active="PSUR/PBRER",
    draw=lambda d: (
        text(d, (252, 80), "PBRER  ·  Cardioxil  ·  DLP 30.06.2026", 20, True),
        chip(d, 252, 112, "Section 2.3  Draft ready", AI_BG, TEAL_D),
        field(d, 252, 150, 696, "Раздел", "2.3 Cumulative subject exposure  ·  источники: CTS, Safety DB, previous PBRER", True),
        table(d, 252, 230, 696, ["Утверждение в тексте", "Источник", "Согласовано"],
              [["Exposure 14 220 PY", "CTS extract 12.07", ("Linked", (226, 245, 234), GREEN)],
               ["Fatal cases = 4", "Safety DB", ("Linked", (226, 245, 234), GREEN)],
               ["RMP measure MEA-02", "RMP v4.1", ("Mismatch vs PSUR", (255, 232, 232), RED)]],
              [240, 180, 230]),
    ),
    ai=("Aggregate reporting", [
        ("ai", "Draft раздела", "Текст 2.3 собран из CTS и Safety DB, утверждения связаны со источниками."),
        ("warn", "Сравнение с прошлым", "В предыдущем PBRER exposure 11 040 PY — рост объяснён в draft."),
        ("risk", "Несоответствие RMP", "MEA-02 в RMP v4.1 не отражена в текущем PBRER."),
    ], ["Принять draft", "Сверить RMP"]),
))

add(dict(
    file="qms.png", product="AI-QMS  ·  Deviation DEV-2026-0194",
    nav=["Deviations", "Investigations", "CAPA", "Changes", "Risks", "Audits", "Complaints"], active="Deviations",
    draw=lambda d: (
        text(d, (252, 80), "Deviation  DEV-2026-0194", 22, True),
        chip(d, 252, 112, "Line 3  ·  Granulation", SOFT, TEXT),
        field(d, 252, 150, 696, "Описание события", "Температура грануляции 68.4 °C при допуске 62–66 °C, batch B-4418, длительность 11 мин.", False),
        field(d, 252, 220, 330, "Категория  ·  AI", "Process parameter excursion", True),
        field(d, 598, 220, 350, "Severity  ·  AI", "Major  ·  влияние на CQA возможно", True),
        table(d, 252, 300, 696, ["Похожие случаи", "Линия", "Root cause", "Дата"],
              [["DEV-2025-0881", "Line 3", "Sensor drift", "11.2025"],
               ["DEV-2025-0640", "Line 3", "Steam valve lag", "08.2025"],
               ["DEV-2024-1512", "Line 1", "Recipe error", "12.2024"]],
              [180, 120, 200, 140]),
    ),
    ai=("Deviation Assistant", [
        ("ai", "Категория и severity", "Process excursion, Major. Похожие DEV на линии 3 — sensor drift."),
        ("ok", "Investigation draft", "Вероятные причины: калибровка датчика T, клапан пара, загрузка. Предложен план."),
        ("ai", "CAPA draft", "Калибровка weekly + interlock 66.5 °C. Effectiveness: повторные DEV −70% после DEV-0881."),
    ], ["Подтвердить", "Изменить"]),
))

add(dict(
    file="edms.png", product="AI-EDMS  ·  SOP-QC-044 v6.2",
    nav=["Documents", "SOPs", "Versions", "Reviews", "Approvals", "Changes"], active="SOPs",
    draw=lambda d: (
        text(d, (252, 80), "SOP-QC-044  ·  HPLC assay of API", 20, True),
        chip(d, 252, 112, "v6.1 → v6.2  in review", (232, 244, 255), BLUE),
        table(d, 252, 150, 696, ["Пункт", "v6.1", "v6.2", "Тип"],
              [["5.2 Sample prep", "10 mL flask", "25 mL flask", ("Changed", (255, 243, 224), AMBER)],
               ["7.1 SST", "RSD ≤ 2.0%", "RSD ≤ 1.5%", ("Changed", (255, 243, 224), AMBER)],
               ["9.2 Ref SOP-QC-012", "v3.0", "v3.0 (obsolete)", ("Broken link", (255, 232, 232), RED)]],
              [180, 170, 190, 140]),
        field(d, 252, 330, 696, "Summary для reviewers  ·  AI", "Изменены dilution и SST; ссылка на SOP-QC-012 устарела — действует v4.1.", True),
    ),
    ai=("Document compare", [
        ("ai", "Классификация", "Analytical SOP, QC, HPLC. Metadata: owner QC, effective TBD."),
        ("warn", "Изменённые пункты", "5.2 и 7.1. Требуется оценка влияния на валидацию метода."),
        ("risk", "Устаревшая ссылка", "SOP-QC-012 v3.0 заменена на v4.1 02.2026."),
    ], ["Draft summary", "Назначить review"]),
))

add(dict(
    file="audit.png", product="AI-Audit  ·  AUD-2026-07 GMP",
    nav=["Audits", "Checklists", "Evidence", "Findings", "CAPA", "Reports"], active="Checklists",
    draw=lambda d: (
        text(d, (252, 80), "Internal audit  ·  Warehouse & EM", 20, True),
        kpi(d, 252, 120, 218, "Checklist", "64 items", "GMP + SOP-WH-02", TEAL),
        kpi(d, 486, 120, 218, "Evidence mapped", "51 / 64", "13 без доказательства", AMBER),
        kpi(d, 720, 120, 218, "Findings", "8", "2 critical draft", RED),
        table(d, 252, 236, 696, ["Пункт", "Evidence", "Finding", "Связь"],
              [["5.3 FEFO", "WMS log Jun", ("Minor", (255, 243, 224), AMBER), "DEV-0188"],
               ["6.1 EM limits", "Missing Q2", ("Major", (255, 232, 232), RED), "CAPA-441"],
               ["8.2 Training", "LMS record", ("OK", (226, 245, 234), GREEN), "—"]],
              [160, 160, 150, 160]),
    ),
    ai=("Audit Assistant", [
        ("ai", "Checklist", "Сформирован по GMP склад + SOP-WH-02, риск-ориентированные пункты выделены."),
        ("warn", "Evidence", "13 пунктов без вложения. EM Q2 не приложен."),
        ("ok", "Draft report", "Findings классифицированы, связанные DEV/CAPA проставлены."),
    ], ["Draft report", "Создать finding"]),
))

add(dict(
    file="lms.png", product="AI-Training / LMS  ·  SOP-QC-044",
    nav=["Courses", "Materials", "Employees", "Competency", "Assessments", "Records"], active="Materials",
    draw=lambda d: (
        text(d, (252, 80), "Training from SOP-QC-044 v6.2", 20, True),
        chip(d, 252, 112, "Refresher after SOP change", AI_BG, TEAL_D),
        field(d, 252, 150, 696, "Draft material", "Модуль: изменение dilution 10→25 mL и новый SST RSD ≤ 1.5%.", True),
        table(d, 252, 230, 696, ["Сотрудник", "Ошибки в тесте", "Тема gaps", "Следующий шаг"],
              [["Петрова А.В.", "2 / 10", "SST / system suitability", "Individual test"],
               ["Иванов С.Н.", "0 / 10", "—", "Record complete"],
               ["Ким О.Л.", "4 / 10", "Sample prep, calc", "Refresher + retest"]],
              [180, 160, 200, 150]),
    ),
    ai=("Training Assistant", [
        ("ai", "Материал из SOP", "Сгенерирован refresher только по изменённым пунктам 5.2 и 7.1."),
        ("ok", "Вопросы", "12 вопросов с акцентом на SST и расчёт концентрации."),
        ("warn", "Индивидуальный тест", "Для Ким О.Л. — вопросы по sample prep, где были ошибки."),
    ], ["Назначить курс", "Сгенерировать тест"]),
))

add(dict(
    file="mes.png", product="AI-MES  ·  Batch B-4418",
    nav=["Orders", "Batches", "Operations", "Parameters", "Materials", "Review"], active="Batches",
    draw=lambda d: (
        text(d, (252, 80), "Batch B-4418  ·  Granulation", 22, True),
        kpi(d, 252, 120, 218, "Deviation risk", "72 %", "vs successful batches", RED),
        kpi(d, 486, 120, 218, "Temp max", "68.4 °C", "limit 66.0", RED),
        kpi(d, 720, 120, 218, "Yield forecast", "94.1 %", "hist. 96.8%", AMBER),
        table(d, 252, 236, 696, ["Parameter", "Actual", "Normal range", "Связь с риском"],
              [["Granulation T", "68.4", "62–66 °C", ("High", (255, 232, 232), RED)],
               ["Impeller rpm", "142", "135–150", ("OK", (226, 245, 234), GREEN)],
               ["Binder rate", "1.8", "1.5–2.2", ("OK", (226, 245, 234), GREEN)]],
              [180, 130, 160, 180]),
    ),
    ai=("Process intelligence", [
        ("risk", "Отклонение параметра", "T выше нормального диапазона 11 мин. Вероятность batch deviation 72%."),
        ("ai", "Сравнение с успешными", "B-4401/4407 держали T ≤ 65.2. Наибольший вклад — датчик пара."),
        ("ok", "Batch Review draft", "Краткое summary для QA: excursion, impact on CQA, proposed disposition."),
    ], ["Открыть DEV", "Draft review"]),
))

add(dict(
    file="ebr.png", product="AI-eBR  ·  Batch Record B-4418",
    nav=["Batch Records", "Steps", "Materials", "Equipment", "Exceptions", "Review"], active="Batch Records",
    draw=lambda d: (
        text(d, (252, 80), "Electronic Batch Record  B-4418", 20, True),
        chip(d, 252, 112, "12 entries require review", (255, 243, 224), AMBER),
        table(d, 252, 150, 696, ["Step", "Поле", "Значение", "Check"],
              [["4.2 Weighing", "API actual", "12.41 kg", ("OK", (226, 245, 234), GREEN)],
               ["5.1 Granulation", "Temperature", "68.4 °C", ("Out of range", (255, 232, 232), RED)],
               ["5.1 Granulation", "Operator sign", "—", ("Missing", (255, 232, 232), RED)],
               ["6.3 Drying", "LOD", "1.1%", ("vs 5.1 conflict", (255, 243, 224), AMBER)]],
              [180, 160, 150, 180]),
        field(d, 252, 360, 696, "Batch Summary  ·  AI", "Критичное: T-excursion и отсутствует подпись шага 5.1. Остальные CPP в допуске.", True),
    ),
    ai=("eBR checks", [
        ("risk", "Обязательные поля", "Нет подписи оператора на шаге 5.1 после excursion."),
        ("warn", "Противоречие", "LOD 1.1% нетипичен после перегрева грануляции — требуется review."),
        ("ok", "Review list", "12 записей для QA review, draft Batch Summary сформирован."),
    ], ["Список review", "Принять summary"]),
))

add(dict(
    file="cmms.png", product="AI-CMMS  ·  Granulator GR-03",
    nav=["Equipment", "Work Orders", "Failures", "Plans", "Spare Parts", "Reports"], active="Equipment",
    draw=lambda d: (
        text(d, (252, 80), "Equipment  GR-03  ·  High-shear granulator", 20, True),
        kpi(d, 252, 120, 218, "Failure risk 30д", "64 %", "повышенный", RED),
        kpi(d, 486, 120, 218, "PM due", "28 авг", "рекомендация AI", TEAL),
        kpi(d, 720, 120, 218, "Open WO", "2", "steam valve + sensor", AMBER),
        table(d, 252, 236, 696, ["Сигнал", "Вероятная причина", "Запчасть", "Действие"],
              [["T overshoot", "PT100 drift / steam valve", "Valve kit VK-12", "WO draft"],
               ["Vibration 2x", "Bearing wear", "Bearing 6310", "Inspect"],
               ["Alarm 44", "Seal leak history", "Seal S-03", "Stock check"]],
              [160, 250, 160, 120]),
    ),
    ai=("Predictive maintenance", [
        ("risk", "Риск отказа", "GR-03 в группе повышенного риска на 30 дней (T overshoot + vibration)."),
        ("ai", "Причины по описанию", "«Температура плавает» → калибровка PT100 (0.62) или клапан пара (0.24)."),
        ("ok", "Work Order draft", "PM 28 авг + запчасти VK-12 и PT100 на основании истории GR-03."),
    ], ["Создать WO", "Назначить PM"]),
))

add(dict(
    file="em.png", product="AI-Environmental Monitoring  ·  Grade B",
    nav=["Points", "Samples", "Results", "Excursions", "Investigations", "Alerts"], active="Excursions",
    draw=lambda d: (
        text(d, (252, 80), "Excursion  EM-2026-062  ·  Point B-12", 20, True),
        kpi(d, 252, 120, 218, "CFU", "12", "alert 5 / action 10", RED),
        kpi(d, 486, 120, 218, "Excursion risk", "41 %", "7-дневный прогноз", AMBER),
        kpi(d, 720, 120, 218, "Repeat point", "B-12", "3 за квартал", RED),
        table(d, 252, 236, 696, ["Точка", "Текущее", "История median", "Статус"],
              [["B-12 air", "12 CFU", "2", ("Action", (255, 232, 232), RED)],
               ["B-12 surface", "4", "1", ("Alert", (255, 243, 224), AMBER)],
               ["B-11 air", "1", "1", ("OK", (226, 245, 234), GREEN)]],
              [160, 150, 180, 160]),
    ),
    ai=("EM intelligence", [
        ("risk", "Сдвиг vs история", "B-12 устойчиво выше собственного baseline. Повторяющаяся точка."),
        ("ai", "Похожие excursion", "EM-2025-198: HVAC filter + personnel flow. Совпадение 0.81."),
        ("ok", "Investigation draft", "Гипотезы: фильтр HVAC, вход персонала, уборка. План отбора доп. проб."),
    ], ["Draft investigation", "Открыть alert"]),
))

add(dict(
    file="wms.png", product="AI-WMS  ·  Warehouse WH-01",
    nav=["Materials", "Stock", "Batches", "Locations", "Shipments", "Picking"], active="Stock",
    draw=lambda d: (
        text(d, (252, 80), "Expiry & FEFO  ·  Cold zone 2–8 °C", 20, True),
        kpi(d, 252, 120, 218, "Risk expiry 30д", "9 batches", "FEFO нарушен в 2", AMBER),
        kpi(d, 486, 120, 218, "Safety stock", "Cardioxil 20", "ниже на 14%", RED),
        kpi(d, 720, 120, 218, "Anomaly moves", "3", "ночные перемещения", AMBER),
        table(d, 252, 236, 696, ["Batch", "Expiry", "Qty", "FEFO / place"],
              [["FP-24011", "12.09.2026", "840", ("Pick first", AI_BG, TEAL_D)],
               ["FP-24008", "02.10.2026", "1 200", "Aisle B / slot 14"],
               ["FP-23190", "28.08.2026", "60", ("Expiry risk", (255, 232, 232), RED)]],
              [150, 150, 120, 230]),
    ),
    ai=("Warehouse AI", [
        ("warn", "Просрочка", "FP-23190 истекает через 8 дней при текущем отгрузочном плане."),
        ("ai", "FEFO sequence", "Следующий picking: FP-24011 → FP-24008. Сейчас в очереди наоборот."),
        ("ok", "Размещение", "Рекомендован слот C-02 ближе к отгрузке для короткого срока."),
    ], ["FEFO очередь", "Переместить"]),
))

add(dict(
    file="tms.png", product="AI-TMS  ·  Shipment SH-9021",
    nav=["Shipments", "Routes", "Carriers", "Temperature", "Deliveries", "Exceptions"], active="Shipments",
    draw=lambda d: (
        text(d, (252, 80), "Shipment SH-9021  ·  2–8 °C", 22, True),
        kpi(d, 252, 120, 218, "ETA", "16:40", "риск задержки 34%", AMBER),
        kpi(d, 486, 120, 218, "Temp risk", "22 %", "участок МКАД, +28 °C", AMBER),
        kpi(d, 720, 120, 218, "Exception", "1 open", "door open 4 min", AMBER),
        table(d, 252, 236, 696, ["Плечо", "Carrier", "Temp", "Статус"],
              [["Depot → Hub", "ColdLog", "5.1 °C", ("OK", (226, 245, 234), GREEN)],
               ["Hub → Site RU-014", "MedTrans", "7.4 °C", ("Watch", (255, 243, 224), AMBER)],
               ["Alt. route", "via A-104", "ETA 17:10", ("Safer temp", AI_BG, TEAL_D)]],
              [200, 150, 140, 170]),
    ),
    ai=("Transportation risk", [
        ("warn", "Задержка", "Пробка на основном маршруте. Вероятность срыва слота 34%."),
        ("ai", "Temperature excursion", "Прогноз 22% на участке без тени. Альтернатива A-104 снижает риск."),
        ("ok", "Exception", "Door open классифицирован как handling delay, не как cold-chain break."),
    ], ["Сменить маршрут", "Открыть exception"]),
))

add(dict(
    file="supply.png", product="AI-Supply Planning  ·  Cardioxil",
    nav=["Demand", "Forecast", "Inventory", "Production", "POs", "Suppliers"], active="Forecast",
    draw=lambda d: (
        text(d, (252, 80), "Demand & supply  ·  Cardioxil 20 mg", 20, True),
        kpi(d, 252, 120, 218, "Demand 90д", "1.24M pack", "+8% vs plan", TEAL),
        kpi(d, 486, 120, 218, "Stock-out risk", "18 %", "октябрь, SKU 20 mg", AMBER),
        kpi(d, 720, 120, 218, "Supplier delay", "Site API-B", "риск 0.31", RED),
        table(d, 252, 236, 696, ["Сценарий", "Production", "Safety stock", "Stock-out"],
              [["Base", "3 batches", "keep", "18%"],
               ["+1 batch Sep", "4 batches", "keep", ("6%", (226, 245, 234), GREEN)],
               ["API delay 14d", "2 batches", "raise +20%", ("41%", (255, 232, 232), RED)]],
              [180, 150, 160, 160]),
    ),
    ai=("Planning models", [
        ("ai", "Прогноз demand", "Рост 8% за счёт сезона и нового региона. Необходимый volume: +1 batch в сентябре."),
        ("warn", "Stock-out", "Без доп. серии риск 18% в октябре."),
        ("risk", "Supplier", "API-B: повышенный риск задержки по lead time и качественным претензиям."),
    ], ["Моделировать", "Изменить план"]),
))

add(dict(
    file="crm.png", product="AI-CRM  ·  HCP Dr. Sokolova",
    nav=["HCPs", "Accounts", "Interactions", "Call Reports", "Territories", "Opportunities"], active="HCPs",
    draw=lambda d: (
        text(d, (252, 80), "HCP  ·  Соколова Е.В., кардиолог", 20, True),
        field(d, 252, 130, 696, "Summary взаимодействий  ·  AI", "4 визита YTD. Интерес к Cardioxil у пациентов с ХСН. Запрос: comparators vs standard.", True),
        table(d, 252, 220, 696, ["Дата", "Тип", "Call report", "Commitment"],
              [["12.08", "Visit", "Efficacy in NYHA II–III", "Send approved slide kit"],
               ["03.06", "Congress", "Safety questions", "—"],
               ["18.03", "Email", "Dosing in CKD", ("Label section 4.2", AI_BG, TEAL_D)]],
              [100, 120, 250, 200]),
    ),
    ai=("Medical CRM", [
        ("ai", "Следующая задача", "Визит с approved content: HFrEF evidence kit v3 (MLR approved)."),
        ("ok", "Классификация call", "Scientific exchange, не промо. Извлечён commitment: отправить slide kit."),
        ("ai", "Контент", "Подобран approved материал MLR-2026-118, off-label claims отсутствуют."),
    ], ["Создать задачу", "Подбор контента"]),
))

add(dict(
    file="mlr.png", product="AI-MLR  ·  Content MLR-2026-118",
    nav=["Content", "Claims", "References", "Reviews", "Comments", "Approvals"], active="Content",
    draw=lambda d: (
        text(d, (252, 80), "Promotional review  ·  leave piece v2", 20, True),
        chip(d, 252, 112, "3 claims without reference", (255, 243, 224), AMBER),
        table(d, 252, 150, 696, ["Claim", "Reference", "vs SmPC", "Статус"],
              [["Reduces HF hosp. 21%", "Study PB-301 p.12", "Consistent", ("OK", (226, 245, 234), GREEN)],
               ["Best in class safety", "—", "Not in label", ("No ref", (255, 232, 232), RED)],
               ["Once daily, any meal", "SmPC 4.2", "Wording drift", ("Edit", (255, 243, 224), AMBER)]],
              [230, 180, 140, 120]),
        field(d, 252, 330, 696, "Вопросы reviewers  ·  AI", "1) Удалить «best in class». 2) Вернуть формулировку SmPC 4.2 про приём с пищей.", True),
    ),
    ai=("MLR Assistant", [
        ("ai", "Извлечение claims", "Найдено 7 утверждений, 5 со ссылками, 2 без подтверждения."),
        ("risk", "Off-label / no ref", "«Best in class safety» нет в approved label и references."),
        ("warn", "Версии", "v2 расходится с v1 в 3 абзацах и со SmPC в пункте приёма пищи."),
    ], ["Список вопросов", "Отправить в review"]),
))

add(dict(
    file="knowledge.png", product="AI Knowledge Assistant",
    nav=["QMS", "eTMF", "SOP/EDMS", "RIM", "LIMS", "CTMS"], active="QMS",
    draw=lambda d: (
        text(d, (252, 80), "Вопрос по разрешённым источникам", 20, True),
        rr(d, (252, 118, 948, 170), 12, fill=WHITE, outline=LINE),
        text(d, (268, 144), "Какие отклонения по линии 3 за 6 месяцев связаны с температурой грануляции?", 13, False, TEXT, "lm"),
        table(d, 252, 190, 696, ["Ответ / источник", "Тип", "ID", "Ссылка"],
              [["DEV-0194 T=68.4 °C", "Deviation", "QMS", "Open record"],
               ["DEV-0881 sensor drift", "Deviation", "QMS", "Closed"],
               ["SOP-PR-015 §6.2 limits", "SOP", "EDMS", "v5.0 §6.2"]],
              [280, 130, 100, 150]),
        text(d, (252, 370), "Ответ со ссылками на конкретные записи, без изменения исходных данных.", 12, False, MUTED),
    ),
    ai=("Grounded answer", [
        ("ok", "Источники", "Ответ собран из QMS, SOP-PR-015 и batch B-4418. Показаны ID записей."),
        ("ai", "Цитирование", "Каждый тезис привязан к документу или записи. Нет данных вне контура."),
        ("ok", "Следующий шаг", "Можно передать в Agent Layer для draft CAPA после подтверждения."),
    ], ["Открыть записи", "В агент"]),
))

add(dict(
    file="agent.png", product="AI Agent Layer  ·  QMS actions",
    nav=["Allowed actions", "Evidence", "Drafts", "Approvals", "Audit trail"], active="Drafts",
    draw=lambda d: (
        text(d, (252, 80), "Задача агента по линии №3", 20, True),
        field(d, 252, 130, 696, "Запрос", "Покажи открытые DEV за 6 мес, найди повторяющиеся причины, подготовь draft CAPA.", False),
        table(d, 252, 210, 696, ["Шаг", "Результат", "Статус"],
              [["1. Поиск в QMS", "14 deviations, Line 3", ("Done", (226, 245, 234), GREEN)],
               ["2. Группировка причин", "Sensor drift 6; valve 4", ("Done", (226, 245, 234), GREEN)],
               ["3. Evidence pack", "DEV list + SOP-PR-015", ("Done", (226, 245, 234), GREEN)],
               ["4. Draft CAPA ×2", "Не создан без подтверждения", ("Waiting user", (255, 243, 224), AMBER)]],
              [220, 280, 180]),
    ),
    ai=("Human in the loop", [
        ("ok", "Evidence показан", "Агент не пишет в систему до подтверждения. Есть полный audit trail шагов."),
        ("ai", "Draft CAPA 1", "Калибровка PT100 weekly + interlock. Root cause: sensor drift."),
        ("ai", "Draft CAPA 2", "Замена steam valve kit + PM. Root cause: valve lag."),
    ], ["Подтвердить CAPA", "Отклонить"]),
))


def render(spec):
    img = chrome(spec["product"], spec["nav"], spec["active"]).convert("RGBA")
    d = ImageDraw.Draw(img)
    # main card
    img = shadow(img, (240, 64, 960, H - 24), 18, 16, 28)
    d = ImageDraw.Draw(img)
    rr(d, (240, 64, 960, H - 24), 18, fill=WHITE)
    spec["draw"](d)
    title, items, actions = spec["ai"]
    img = shadow(img, (980, 68, W - 24, H - 24), 16, 14, 24)
    d = ImageDraw.Draw(img)
    ai_panel(d, 980, title, items, actions)
    out = OUT / spec["file"]
    img.convert("RGB").save(out, "PNG", optimize=True)
    print("wrote", out.name)


def main():
    for spec in SCREENS:
        render(spec)
    print(f"done: {len(SCREENS)} screens")


if __name__ == "__main__":
    main()
