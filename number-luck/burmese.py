# -*- coding: utf-8 -*-
"""
ชั้นที่ 3: ระบบวันเกิด 8 วันของพม่า + มหาโพติ (Mahabote) — Number Luck
========================================================================
อิงผลวิจัย research/burmese-indian-numerology.md (ตรวจไขว้แล้ว):
- สัปดาห์พม่ามี 8 ราศี: พุธตัดที่เที่ยงวัน → พุธบ่าย = ราหู (ยาฮู)
- แต่ละวันผูก ดาว-เลข-ทิศ-สัตว์ (ตามแท่นบูชา 8 ทิศรอบเจดีย์)
- มหาโพติ: ปีพม่า = ค.ศ. - 639 (เกิดก่อน/ใน 15 เม.ย.) หรือ - 638 (หลัง)
  mod 7 → ดาวเรือนแรก แล้วเรียงดาวลงเรือน 7 เรือน
- ความเข้ากันเบอร์-วันเกิด: ใช้คู่มิตร/ศัตรูของดาว (ตำราชาติเวร ซึ่งใช้
  ตารางเลขประจำวันแบบเดียวกับพม่า) + เลข 9 (โกนะวิน) ดีกับทุกวัน
"""
import datetime as _dt

# ---------- ตารางวันเกิด 8 วัน (ยืนยันจากวิจัย) ----------
DAYS = {
    "sun":    {"th": "วันอาทิตย์",   "num": 1, "planet": "อาทิตย์", "dir": "ตะวันออกเฉียงเหนือ", "animal": "ครุฑ",       "trait": "ผู้นำ ทะเยอทะยาน ใจกว้าง รักศักดิ์ศรี"},
    "mon":    {"th": "วันจันทร์",    "num": 2, "planet": "จันทร์",  "dir": "ตะวันออก",           "animal": "เสือ",        "trait": "อ่อนโยน ใจเย็น ช่างคิด มีเสน่ห์นุ่มนวล"},
    "tue":    {"th": "วันอังคาร",    "num": 3, "planet": "อังคาร",  "dir": "ตะวันออกเฉียงใต้",   "animal": "สิงห์",       "trait": "กล้าหาญ ซื่อตรง พลังสูง ใจร้อน"},
    "wed_am": {"th": "วันพุธ (เช้า)", "num": 4, "planet": "พุธ",     "dir": "ใต้",                "animal": "ช้างมีงา",    "trait": "ฉลาด พูดเก่ง อารมณ์ดี ปรับตัวไว"},
    "wed_pm": {"th": "วันพุธ (บ่าย) ยาฮู", "num": 8, "planet": "ราหู", "dir": "ตะวันตกเฉียงเหนือ", "animal": "ช้างไม่มีงา", "trait": "ใจถึง มีอิทธิพล ดวงแรง กล้าได้กล้าเสีย"},
    "thu":    {"th": "วันพฤหัสบดี",  "num": 5, "planet": "พฤหัส",   "dir": "ตะวันตก",            "animal": "หนู",         "trait": "ปัญญาดี มีคุณธรรม ผู้ใหญ่เมตตา น่าเชื่อถือ"},
    "fri":    {"th": "วันศุกร์",     "num": 6, "planet": "ศุกร์",   "dir": "เหนือ",              "animal": "หนูตะเภา",    "trait": "มีเสน่ห์ รักศิลปะ การเงินดี รักสวยรักงาม"},
    "sat":    {"th": "วันเสาร์",     "num": 7, "planet": "เสาร์",   "dir": "ตะวันตกเฉียงใต้",    "animal": "นาค",         "trait": "อดทน หนักแน่น จริงจัง สู้ชีวิต"},
}

# คู่มิตร/ศัตรูของเลขดาว (ตำราชาติเวร — ตารางเลขประจำวันเดียวกับพม่า)
FRIEND_PAIRS = {frozenset(p) for p in [(1, 5), (2, 4), (3, 6), (7, 8)]}
ENEMY_PAIRS = {frozenset(p) for p in [(1, 3), (2, 5), (2, 8), (3, 7), (6, 7)]}
NAWIN = 9  # โกนะวิน — มงคลกับทุกวันตามคติพม่า

# ---------- มหาโพติ ----------
_MB_PLANET_BY_REMAINDER = {1: "อาทิตย์", 2: "จันทร์", 3: "อังคาร", 4: "พุธ", 5: "พฤหัส", 6: "ศุกร์", 0: "เสาร์"}
_MB_SEQUENCE = ["อาทิตย์", "พุธ", "เสาร์", "อังคาร", "ศุกร์", "จันทร์", "พฤหัส"]  # ลำดับวนตายตัว
MB_HOUSES = [
    ("อนิจจัง (Impermanence)", "ภาระ", "ชีวิตช่วงต้นผันแปร ต้องปรับตัวบ่อย"),
    ("สุดโต่ง (Extremity)", "ภาระ", "ชีวิตมีจังหวะขึ้นสุดลงสุด ต้องคุมสมดุล"),
    ("ชื่อเสียง (Fame)", "บวก", "มีชื่อเสียงเกียรติยศ คนรู้จักนับหน้าถือตา"),
    ("ทรัพย์ (Wealth)", "บวก", "มีโภคทรัพย์ หาเงินเก่ง ฐานะมั่นคง"),
    ("ราชศักดิ์ (Kingly Position)", "บวก", "มีอำนาจวาสนา ได้ตำแหน่งสูง ผู้คนยำเกรง"),
    ("โรคภัย (Sickly)", "ภาระ", "ต้องใส่ใจสุขภาพเป็นพิเศษ พลังชีวิตถูกดึง"),
    ("ผู้นำ (Leader)", "บวก", "เกิดมาเป็นหัวหน้าคน มีภาวะผู้นำโดดเด่น"),
]


def day_key_from_date(birthdate: _dt.date, wednesday_pm: bool = False) -> str:
    wd = birthdate.weekday()  # Mon=0 ... Sun=6
    mapping = {6: "sun", 0: "mon", 1: "tue", 3: "thu", 4: "fri", 5: "sat"}
    if wd == 2:  # Wednesday
        return "wed_pm" if wednesday_pm else "wed_am"
    return mapping[wd]


def mahabote(birthdate: _dt.date) -> dict:
    """คำนวณผังมหาโพติอย่างย่อ: ดาวประจำตัวอยู่เรือนไหน"""
    y = birthdate.year
    cutoff = _dt.date(y, 4, 15)
    burmese_year = y - (639 if birthdate <= cutoff else 638)
    rem = burmese_year % 7
    first_planet = _MB_PLANET_BY_REMAINDER[rem]
    # เรียงดาวลงเรือน 1-7 เริ่มจาก first_planet ตามลำดับวน
    start = _MB_SEQUENCE.index(first_planet)
    placement = {}  # planet -> house index (0-6)
    for i in range(7):
        planet = _MB_SEQUENCE[(start + i) % 7]
        placement[planet] = i
    return {"burmese_year": burmese_year, "first_planet": first_planet, "placement": placement}


def birthday_profile(birthdate: _dt.date, wednesday_pm: bool = False) -> dict:
    """ข้อมูลดวงวันเกิดแบบพม่า + ตำแหน่งดาวในมหาโพติ"""
    key = day_key_from_date(birthdate, wednesday_pm)
    d = DAYS[key]
    mb = mahabote(birthdate)
    house_idx = mb["placement"].get(d["planet"])
    house = MB_HOUSES[house_idx] if house_idx is not None else None
    return {"key": key, **d, "mahabote": mb,
            "mb_house": {"no": house_idx + 1, "name": house[0], "nature": house[1], "desc": house[2]} if house else None}


PLANET_BY_NUM = {1: "อาทิตย์", 2: "จันทร์", 3: "อังคาร", 4: "พุธ", 5: "พฤหัส", 6: "ศุกร์", 7: "เสาร์"}
# 8=ราหู, 9=เกตุ ไม่อยู่ในผัง 7 เรือนของมหาโพติ — ตีความแยก

# ---------- นามศาสตร์พม่า: อักษรประจำวันเกิด (wet ဝဂ်) — ยืนยันจากวิจัยรอบ 2 ----------
# โรมันไนซ์เรียง "ยาวก่อนสั้น" เพื่อ match ตัวอักษรแรกของชื่อภาษาอังกฤษ
NAME_LETTERS = {
    "sun":    {"mm": "အ (สระ)",          "roman": ["A", "E", "I", "O", "U"]},
    "mon":    {"mm": "က ခ ဂ ဃ င",       "roman": ["KY", "KH", "GY", "NG", "K", "G"]},
    "tue":    {"mm": "စ ဆ ဇ ဈ ည",       "roman": ["HS", "NY", "SH", "S", "Z", "C"]},
    "wed_am": {"mm": "လ ဝ",             "roman": ["L", "W"]},
    "wed_pm": {"mm": "ယ ရ",             "roman": ["Y", "R"]},
    "thu":    {"mm": "ပ ဖ ဗ ဘ မ",       "roman": ["PH", "HP", "MY", "P", "B", "M"]},
    "fri":    {"mm": "သ ဟ",             "roman": ["TH", "H"]},
    "sat":    {"mm": "တ ထ ဒ ဓ န",       "roman": ["HT", "T", "D", "N"]},
}
_ROMAN_ORDER = sorted(
    [(pref, day) for day, v in NAME_LETTERS.items() for pref in v["roman"]],
    key=lambda x: -len(x[0]),
)


def day_from_name(name: str):
    """เดาวันเกิดจากอักษรแรกของชื่อ (โรมันไนซ์) ตามธรรมเนียมตั้งชื่อพม่า
    คืน (day_key, prefix) หรือ (None, None) ถ้าเดาไม่ได้"""
    n = (name or "").strip().upper()
    if not n:
        return None, None
    for pref, day in _ROMAN_ORDER:
        if n.startswith(pref):
            return day, pref
    return None, None


# ---------- ดวงคู่: คู่วันเกิดที่ไม่ถูกกัน (ตำราแต่งงานพม่า) ----------
# ยืนยันแน่น: อาทิตย์-พุธเช้า, พุธบ่าย(ราหู)-อังคาร | แหล่งเดียว: เสาร์-พฤหัส, ศุกร์-จันทร์
# หมายเหตุ: มีหลายสำนัก ระบบนำเสนอเป็น "ตำราหลัก" พร้อม disclaimer
COUPLE_CLASH = {
    frozenset(("sat", "thu")): "เสาร์-พฤหัส: ดาวบาปเคราะห์ใหญ่ปะทะดาวครู ต้องปรับจังหวะชีวิตเข้าหากัน",
    frozenset(("fri", "mon")): "ศุกร์-จันทร์: ความอ่อนโยนสองแบบที่แย่งกันนำ ต้องมีฝ่ายยอมถอย",
    frozenset(("sun", "wed_am")): "อาทิตย์-พุธเช้า: ครุฑกับช้าง อำนาจปะทะปัญญา ต่างคนต่างแรง",
    frozenset(("wed_pm", "tue")): "พุธบ่าย(ยาฮู)-อังคาร: ราหูปะทะอังคาร ทิศตรงข้ามกัน (NW↔SE) แรงชนแรง",
}


def couple_compatibility(day_a: str, day_b: str) -> dict:
    """ความเข้ากันของคู่วันเกิดตามคติพม่า"""
    ka, kb = DAYS[day_a], DAYS[day_b]
    pair = frozenset((day_a, day_b))
    clash = COUPLE_CLASH.get(pair)
    rel_num = relation(ka["num"], kb["num"])
    if clash:
        tone, text = "ระวัง", f"คู่เวรตามตำราแต่งงานพม่า — {clash}"
    elif rel_num == "มิตร":
        tone, text = "ดีมาก", f"ดาว{ka['planet']}กับดาว{kb['planet']}เป็นคู่มิตร เสริมพลังกันโดยธรรมชาติ"
    elif rel_num == "เสริม":
        tone, text = "ดี", f"เกิดวันเดียวกัน ({ka['th']}) เข้าใจกันง่าย นิสัยพื้นฐานใกล้เคียงกัน"
    elif rel_num == "ศัตรู":
        tone, text = "ระวัง", f"ดาว{ka['planet']}กับดาว{kb['planet']}เป็นคู่ศัตรูตามตำราชาติเวร ต้องอาศัยความเข้าใจ"
    else:
        tone, text = "กลาง", f"ดาว{ka['planet']}กับดาว{kb['planet']}เป็นกลางต่อกัน อยู่ร่วมกันได้ราบรื่น"
    return {"a": ka, "b": kb, "tone": tone, "text": text}


def _rel_with_special(a: int, b: int) -> str:
    """ความสัมพันธ์เลขคู่ รวมกรณีพิเศษ 9 (นวิน) และ 0 (สูญ)"""
    if 9 in (a, b):
        return "นวิน"
    if 0 in (a, b):
        return "สูญ"
    return relation(a, b)


def couple_numbers(core_a: str, core_b: str) -> dict:
    """
    ความเข้ากันของเบอร์ 2 เบอร์ (เบอร์คู่รัก/หุ้นส่วน — ขายซิมเป็นคู่)
    หลัก: เทียบ 'เลขท้าย' (ชะตาหลักของแต่ละเบอร์) + 'ดาวเด่น' ของสองเบอร์
    ด้วยตารางคู่มิตร/ศัตรู + โบนัสนวินเมื่อทั้งคู่มีเลข 9
    """
    from collections import Counter
    tail_a, tail_b = int(core_a[-1]), int(core_b[-1])
    rel_tail = _rel_with_special(tail_a, tail_b)

    def top_digit(core):
        cnt = Counter(int(c) for c in core if c != "0")
        return cnt.most_common(1)[0][0] if cnt else 0

    top_a, top_b = top_digit(core_a), top_digit(core_b)
    rel_top = _rel_with_special(top_a, top_b)
    nines_a, nines_b = core_a.count("9"), core_b.count("9")

    score = 50.0
    score += {"มิตร": 20, "เสริม": 15, "นวิน": 15, "กลาง": 0, "สูญ": -5, "ศัตรู": -20}[rel_tail]
    score += {"มิตร": 15, "เสริม": 10, "นวิน": 10, "กลาง": 0, "สูญ": -3, "ศัตรู": -15}[rel_top]
    if nines_a >= 1 and nines_b >= 1:
        score += 5
    if nines_a >= 2 and nines_b >= 2:
        score += 5
    score = max(0.0, min(100.0, score))
    return {"score": round(score, 1),
            "tail": {"a": tail_a, "b": tail_b, "rel": rel_tail},
            "top": {"a": top_a, "b": top_b, "rel": rel_top},
            "nines": {"a": nines_a, "b": nines_b}}


# ---------- บทสรุปความเข้ากันแบบละเอียด (5 ปัจจัย) ----------
# ตาราง Mulank (เลขวันเกิด 1-9) × ผลรวมเบอร์ — สายเลขศาสตร์อินเดีย (mobile numerology)
MULANK_TABLE = {
    1: ({1, 3, 5, 6, 7, 9}, {2, 4, 8}),
    2: ({1, 3, 5, 7}, {2, 4, 6, 8, 9}),
    3: ({1, 3, 5, 7, 9}, {2, 4, 6, 8}),
    4: ({1, 3, 5, 6, 7}, {2, 4, 8, 9}),
    5: ({1, 3, 5, 6, 7, 9}, {2, 4, 8}),
    6: ({1, 5, 6, 7}, {2, 3, 4, 8, 9}),
    7: ({1, 3, 5, 6, 7, 9}, {2, 4, 8}),
    8: ({3, 5, 6, 7}, {1, 2, 4, 8, 9}),
    9: ({1, 3, 5, 7}, {2, 4, 6, 8, 9}),
}


def _digital_root(n: int) -> int:
    while n > 9:
        n = sum(int(c) for c in str(n))
    return n if n > 0 else 9


def compat_breakdown(core: str, birthdate: _dt.date = None, wednesday_pm: bool = False,
                     day_key: str = None) -> dict:
    """
    บทสรุปความเข้ากันเบอร์↔วันเกิดแบบละเอียด — คะแนนแยก 5 ปัจจัย + รวมถ่วงน้ำหนัก
      1. digits   (35%) ความสัมพันธ์รายหลัก (ดาววันเกิด × ทุกหลัก ถ่วงตำแหน่ง)
      2. tail     (20%) เลขท้ายเบอร์ (ชะตาหลัก) × ดาววันเกิด
      3. nawin    (10%) พลังนวิน (จำนวนเลข 9)
      4. sum      (20%) ผลรวมเบอร์ × เลขวันเกิด (ตำราอินเดีย Mulank — ต้องมีวันที่เกิด)
      5. mahabote (15%) ดาวเด่นของเบอร์ × เรือนมหาโพติเจ้าชะตา (ต้องมีปีเกิด)
    ปัจจัยที่ข้อมูลไม่พอจะถูกตัดออกและกระจายน้ำหนักให้ตัวที่เหลือ
    """
    comp = number_compatibility(core, birthdate, wednesday_pm, day_key)
    prof = comp["profile"]
    bnum = prof["num"]
    factors = []

    # 1) รายหลัก
    factors.append({"key": "digits", "score": comp["score"], "weight": 35,
                    "data": {"detail": comp["detail"]}})

    # 2) เลขท้าย
    tail = int(core[-1])
    rel_t = "นวิน" if tail == 9 else ("สูญ" if tail == 0 else relation(bnum, tail))
    tail_score = {"มิตร": 100, "เสริม": 95, "นวิน": 90, "กลาง": 55, "สูญ": 40, "ศัตรู": 15}[rel_t]
    factors.append({"key": "tail", "score": tail_score, "weight": 20,
                    "data": {"tail": tail, "rel": rel_t, "bnum": bnum}})

    # 3) นวิน
    nines = core.count("9")
    nawin_score = {0: 50, 1: 65, 2: 80, 3: 90}.get(nines, 100)
    factors.append({"key": "nawin", "score": nawin_score, "weight": 10, "data": {"nines": nines}})

    # 4) ผลรวม × Mulank (ต้องรู้วันที่เกิด)
    if birthdate is not None:
        mulank = _digital_root(birthdate.day)
        root = _digital_root(sum(int(c) for c in "09" + core))
        seek, avoid = MULANK_TABLE[mulank]
        if root in seek:
            sum_score, sum_rel = 100, "ดี"
        elif root in avoid:
            sum_score, sum_rel = 20, "เลี่ยง"
        else:
            sum_score, sum_rel = 55, "กลาง"
        factors.append({"key": "sum", "score": sum_score, "weight": 20,
                        "data": {"mulank": mulank, "root": root, "rel": sum_rel,
                                 "seek": sorted(seek), "avoid": sorted(avoid)}})

    # 5) มหาโพติ (ต้องรู้ปีเกิด)
    if birthdate is not None:
        cross = mahabote_cross(core, birthdate)
        pos = sum(1 for h in cross["hits"] if h["nature"] == "บวก")
        neg = sum(1 for h in cross["hits"] if h["nature"] != "บวก")
        mb_score = max(0, min(100, 55 + 25 * pos - 15 * neg))
        factors.append({"key": "mahabote", "score": mb_score, "weight": 15,
                        "data": {"pos": pos, "neg": neg, "hits": cross["hits"]}})

    # รวมถ่วงน้ำหนัก (กระจายน้ำหนักปัจจัยที่ขาดให้ตัวที่เหลือ)
    wsum = sum(f["weight"] for f in factors)
    overall = round(sum(f["score"] * f["weight"] for f in factors) / wsum, 1)
    for f in factors:
        f["weight_pct"] = round(f["weight"] / wsum * 100)
    return {"overall": overall, "factors": factors, "profile": prof, "base": comp}


# ---------- ยะดะยา: ใบสั่งแก้เคล็ดตามวันเกิด ----------
# จำนวนอิง "กำลังดาว" (groh thak) ของมหาโพติ — ยืนยันจากวิจัยรอบ 2 ว่าตรงเลขกำลังวันไทย (รวม 108)
# การใช้เป็นจำนวนถวาย/ปล่อยสัตว์เป็นแนวปฏิบัติที่เราออกแบบตามหลัก ไม่ใช่กฎตายตัวสากล
GROH_THAK = {"sun": 6, "mon": 15, "tue": 8, "wed_am": 17, "wed_pm": 12, "thu": 19, "fri": 21, "sat": 10}


def yadaya_prescription(day_key: str, problem: str = "ทั่วไป") -> list:
    """ใบสั่งแก้เคล็ดแนวยะดะยาตามวันเกิด (เนื้อหาของเรา อิงหลักที่วิจัยยืนยัน)"""
    d = DAYS[day_key]
    k = GROH_THAK[day_key]
    return [
        f"ทำบุญที่มุมทิศ{d['dir']}ของเจดีย์ (แท่นประจำ{d['th']}) รดน้ำพระประจำวัน {k} ขัน",
        f"ปล่อยปลาหรือนก {k} ตัว (ตามกำลังดาว{d['planet']}) หรือ 9 ตัวตามคติโกนะวิน",
        f"ถวายเทียน 9 เล่ม ดอกไม้ 9 ดอก ตามธรรมเนียมบูชาเก้าเทพ (Phaya Kozu) ของพม่า",
        "สวดมนต์ระลึกพุทธคุณ 9 ประการ (อิติปิโส) 9 จบ ก่อนเริ่มใช้เบอร์ใหม่",
        "เริ่มใช้เบอร์ในวันยัตยาซา (วันมงคลตามปฏิทินพม่า) เลี่ยงวันเปียตะดา",
    ]


def mahabote_full_chart(birthdate: _dt.date) -> list:
    """ผังมหาโพติเต็ม: รายการ 7 เรือน (ชื่อ, ธรรมชาติ, ดาวที่สถิต)"""
    mb = mahabote(birthdate)
    by_house = {h: p for p, h in mb["placement"].items()}
    return [{"no": i + 1, "name": MB_HOUSES[i][0], "nature": MB_HOUSES[i][1],
             "desc": MB_HOUSES[i][2], "planet": by_house[i]} for i in range(7)]


def mahabote_cross(core: str, birthdate: _dt.date) -> dict:
    """
    วิเคราะห์ไขว้: ดาวเด่นของเบอร์ (จากเลขที่ปรากฏบ่อย) ไปสถิตเรือนไหน
    ในผังมหาโพติของเจ้าชะตา → เบอร์ไปกระตุ้น/เติมพลังเรือนนั้น
    """
    from collections import Counter
    mb = mahabote(birthdate)
    cnt = Counter(int(c) for c in core if c != "0")
    dominant = [d for d, _ in cnt.most_common(3)]
    hits, notes = [], []
    for d in dominant:
        n = cnt[d]
        if d in PLANET_BY_NUM:
            planet = PLANET_BY_NUM[d]
            hi = mb["placement"][planet]
            name, nature, desc = MB_HOUSES[hi]
            if nature == "บวก":
                msg = (f"เลข {d} (ดาว{planet}) เด่นในเบอร์ ×{n} — ไปสถิต 'เรือน {hi+1} {name}' "
                       f"ซึ่งเป็นเรือนมงคลในผังชะตาของคุณ → เบอร์ช่วยเติมพลังด้านนี้: {desc}")
            else:
                msg = (f"เลข {d} (ดาว{planet}) เด่นในเบอร์ ×{n} — ไปสถิต 'เรือน {hi+1} {name}' "
                       f"ซึ่งเป็นเรือนภาระของคุณ → เบอร์กระตุ้นจุดนี้ ควรมีสติเรื่อง{name.split(' ')[0]} "
                       f"({desc}) และเสริมด้วยการทำบุญตามวันเกิด")
            hits.append({"digit": d, "count": n, "planet": planet, "house_no": hi + 1,
                         "house": name, "nature": nature, "msg": msg})
        elif d == 8:
            notes.append(f"เลข 8 (ราหู) เด่นในเบอร์ ×{n} — ราหูอยู่เหนือผัง 7 เรือน "
                         "ให้พลังอิทธิพล ความกล้าเสี่ยง และลาภแบบฉับพลัน ต้องมีสติคุม")
        elif d == 9:
            notes.append(f"เลข 9 (เกตุ/นวิน) เด่นในเบอร์ ×{n} — พลังบุญบารมีเหนือผังชะตา "
                         "หนุนทุกเรือนตามคติโกนะวินของพม่า")
    return {"hits": hits, "notes": notes}


def relation(a: int, b: int) -> str:
    if a == b:
        return "เสริม"       # เลขเดียวกัน = เสริมพลังตัวเอง
    if frozenset((a, b)) in FRIEND_PAIRS:
        return "มิตร"
    if frozenset((a, b)) in ENEMY_PAIRS:
        return "ศัตรู"
    return "กลาง"


def number_compatibility(core: str, birthdate: _dt.date = None, wednesday_pm: bool = False,
                         day_key: str = None) -> dict:
    """
    ความเข้ากันของเบอร์ (แกน 9 หลัก) กับวันเกิดผู้ใช้
    กติกา (ระบบของเรา อิงหลักที่วิจัยยืนยัน):
      - เทียบ "เลขวันเกิด" กับเลขทุกหลักในเบอร์ ถ่วงน้ำหนักตามตำแหน่ง (ท้ายหนักสุด)
      - เลขวันเกิดตัวเอง = เสริม (+2) | เลขดาวมิตร = +2 | เลขดาวศัตรู = -3 | เลขกลาง = 0
      - เลข 9 (โกนะวิน) = +2 กับทุกวันเกิด ตามคติพม่า
      - เลขท้ายสุดคูณน้ำหนักพิเศษ (ชะตาหลักของเบอร์)
    ผลลัพธ์: คะแนน 0-100 + คำอธิบายรายหลัก
    """
    if birthdate is not None:
        prof = birthday_profile(birthdate, wednesday_pm)
    elif day_key:
        prof = {"key": day_key, **DAYS[day_key], "mahabote": None, "mb_house": None}
    else:
        raise ValueError("ต้องระบุ birthdate หรือ day_key อย่างใดอย่างหนึ่ง")
    bnum = prof["num"]
    base_w = [0.4, 0.6, 0.6, 0.8, 0.8, 1.0, 1.0, 1.2, 2.0]  # เต็ม 9 หลัก ท้ายหนักสุด
    weights = base_w[-len(core):]                             # เบอร์สั้นยึดน้ำหนักจากท้าย
    detail, raw, wsum = [], 0.0, 0.0
    for i, ch in enumerate(core):
        d = int(ch)
        if d == NAWIN:
            pts, rel = 2.0, "นวิน"
        elif d == 0:
            pts, rel = -0.5, "สูญ"
        else:
            rel = relation(bnum, d)
            pts = {"เสริม": 2.0, "มิตร": 2.0, "ศัตรู": -3.0, "กลาง": 0.0}[rel]
        raw += pts * weights[i]
        wsum += 2.0 * weights[i]  # เพดานคือทุกหลักได้ +2
        detail.append({"digit": d, "relation": rel, "points": pts, "weight": weights[i]})
    # แปลงเป็น 0-100 (raw อยู่ช่วง [-1.5*wsum, wsum])
    score = max(0.0, min(100.0, (raw / wsum) * 60 + 40))  # กลางๆ ~40, เต็ม 100
    if score >= 75:
        verdict = "เข้ากันดีมาก — เบอร์นี้หนุนดวงวันเกิดของคุณ"
    elif score >= 55:
        verdict = "เข้ากันดี — ส่งเสริมกันเป็นส่วนใหญ่"
    elif score >= 40:
        verdict = "พอใช้ — ไม่หนุนไม่ฉุดชัดเจน"
    else:
        verdict = "ควรระวัง — มีเลขที่เป็นศัตรูกับดาววันเกิดหลายตำแหน่ง"
    return {"profile": prof, "score": round(score, 1), "verdict": verdict, "detail": detail}


if __name__ == "__main__":
    import sys
    bd = _dt.date(1998, 5, 17)  # ตัวอย่าง
    r = number_compatibility("696555939", bd)
    p = r["profile"]
    print(f"เกิด {bd} = {p['th']} ดาว{p['planet']} เลข {p['num']} ทิศ{p['dir']} สัตว์{p['animal']}")
    print(f"มหาโพติ: ปีพม่า {p['mahabote']['burmese_year']} ดาว{p['planet']}อยู่เรือน {p['mb_house']['no']} {p['mb_house']['name']} ({p['mb_house']['nature']})")
    print(f"ความเข้ากันกับเบอร์: {r['score']}/100 — {r['verdict']}")
