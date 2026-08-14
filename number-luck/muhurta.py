# -*- coding: utf-8 -*-
"""
ศูนย์ฤกษ์มงคล — Number Luck
============================
1) rank_days()     — หาฤกษ์กิจการ: เลือกกิจกรรม → จัดอันดับวันดี (จีน 宜/忌 + พม่า ยัตยาซา/เปียตะดา)
2) today_fortune() — ดวงวันนี้: ชงปีนักษัตร, ทิศรับทรัพย์, ผู้คุมวัน, ชั่วโมงมงคล

หลักการ (จาก research/auspicious-timing-cn-mm.md):
- 宜/忌 ใช้จาก lunar-python (6tail) สายเดียวเป็น source of truth — ไม่ hard-code เอง
- แสดงคะแนนจีน/พม่าแยกให้ผู้ใช้เห็นทั้งสองศาสตร์ ไม่ตัดสินแทนเมื่อขัดกัน
"""
import datetime as dt

from lunar_python import Solar

from burmese import DAYS, day_key_from_date, relation
from mmcal import astro_day

# ---------- กิจกรรม: ชุดคำ 宜/忌 ของ 6tail ที่นับเป็นกิจกรรมเดียวกัน ----------
ACTIVITIES = {
    "open_shop":  {"cn": {"开市", "开业", "交易", "立券", "开仓"},
                   "th": "เปิดร้าน/เปิดกิจการ", "en": "Open a business", "mm": "ဆိုင်ဖွင့်ခြင်း/လုပ်ငန်းသစ်စတင်ခြင်း", "icon": "🏪"},
    "sign":       {"cn": {"立券", "交易", "纳财", "签约"},
                   "th": "เซ็นสัญญา/ตกลงธุรกิจ", "en": "Sign a contract", "mm": "စာချုပ်ချုပ်ဆိုခြင်း", "icon": "📝"},
    "marry":      {"cn": {"嫁娶", "纳采", "订盟"},
                   "th": "แต่งงาน/หมั้น", "en": "Wedding / engagement", "mm": "ထိမ်းမြားလက်ထပ်ခြင်း/စေ့စပ်ကြောင်းလမ်းခြင်း", "icon": "💍"},
    "move":       {"cn": {"入宅", "移徙", "安床"},
                   "th": "ย้ายบ้าน/ขึ้นบ้านใหม่", "en": "Move house", "mm": "အိမ်ပြောင်းခြင်း/အိမ်တက်မင်္ဂလာ", "icon": "🏠"},
    "travel":     {"cn": {"出行", "赴任"},
                   "th": "เดินทางไกล/เริ่มงานใหม่", "en": "Travel / start a new job", "mm": "ခရီးထွက်ခြင်း/အလုပ်သစ်စတင်ခြင်း", "icon": "✈️"},
    "haircut":    {"cn": {"理发", "整容"},
                   "th": "ตัดผม/เสริมสวย", "en": "Haircut / beauty", "mm": "ဆံပင်ညှပ်ခြင်း/အလှပြင်ခြင်း", "icon": "💇"},
}

# ทิศ 財神 → 3 ภาษา
DIRECTION_TR = {
    "正东": {"th": "ตะวันออก", "en": "East", "mm": "အရှေ့"},
    "正南": {"th": "ใต้", "en": "South", "mm": "တောင်"},
    "正西": {"th": "ตะวันตก", "en": "West", "mm": "အနောက်"},
    "正北": {"th": "เหนือ", "en": "North", "mm": "မြောက်"},
    "东北": {"th": "ตะวันออกเฉียงเหนือ", "en": "Northeast", "mm": "အရှေ့မြောက်"},
    "东南": {"th": "ตะวันออกเฉียงใต้", "en": "Southeast", "mm": "အရှေ့တောင်"},
    "西北": {"th": "ตะวันตกเฉียงเหนือ", "en": "Northwest", "mm": "အနောက်မြောက်"},
    "西南": {"th": "ตะวันตกเฉียงใต้", "en": "Southwest", "mm": "အနောက်တောင်"},
}

# นักษัตรจีน → 3 ภาษา (สำหรับบอก "วันนี้ชงปี...")
SHENGXIAO_TR = {
    "鼠": {"th": "ชวด (หนู)", "en": "Rat", "mm": "ကြွက်"}, "牛": {"th": "ฉลู (วัว)", "en": "Ox", "mm": "နွား"},
    "虎": {"th": "ขาล (เสือ)", "en": "Tiger", "mm": "ကျား"}, "兔": {"th": "เถาะ (กระต่าย)", "en": "Rabbit", "mm": "ယုန်"},
    "龙": {"th": "มะโรง (มังกร)", "en": "Dragon", "mm": "နဂါး"}, "蛇": {"th": "มะเส็ง (งู)", "en": "Snake", "mm": "မြွေ"},
    "马": {"th": "มะเมีย (ม้า)", "en": "Horse", "mm": "မြင်း"}, "羊": {"th": "มะแม (แพะ)", "en": "Goat", "mm": "ဆိတ်"},
    "猴": {"th": "วอก (ลิง)", "en": "Monkey", "mm": "မျောက်"}, "鸡": {"th": "ระกา (ไก่)", "en": "Rooster", "mm": "ကြက်"},
    "狗": {"th": "จอ (หมา)", "en": "Dog", "mm": "ခွေး"}, "猪": {"th": "กุน (หมู)", "en": "Pig", "mm": "ဝက်"},
}

# เหตุผล (reason keys) → 3 ภาษา
REASON_TR = {
    "yi":        {"th": "ปฏิทินจีนระบุ 'ควรทำ' กิจกรรมนี้", "en": "Chinese almanac lists this activity as favorable (宜)", "mm": "တရုတ်ပြက္ခဒိန်အရ ဤကိစ္စအတွက် 'ပြုသင့်သည့်ရက်' (宜)"},
    "ji":        {"th": "ปฏิทินจีนระบุ 'ห้ามทำ' กิจกรรมนี้", "en": "Chinese almanac lists this activity as unfavorable (忌)", "mm": "တရုတ်ပြက္ခဒိန်အရ ဤကိစ္စအတွက် 'ရှောင်သင့်သည့်ရက်' (忌)"},
    "chong":     {"th": "วันชงปีนักษัตรของคุณ", "en": "Clashes (沖) with your zodiac year", "mm": "သင့်မွေးနှစ်ရာသီနှင့် ထိပ်တိုက် (沖) ဖြစ်သောရက်"},
    "po":        {"th": "วัน 破 (แตกหัก) ไม่เริ่มการใหญ่", "en": "破 'Break' day — avoid major starts", "mm": "破 'ကျိုးပဲ့ရက်' — အရေးကြီးကိစ္စများ မစတင်သင့်"},
    "cheng_kai": {"th": "วัน 成/開 เหมาะเริ่มสิ่งใหม่", "en": "成/開 day — good for new beginnings", "mm": "成/開 ရက် — အသစ်စတင်ရန် ကောင်းသည်"},
    "huang":     {"th": "วันหวงเต้า (เทวดาดี)", "en": "Yellow-path auspicious day (黃道)", "mm": "黃道 မင်္ဂလာရက်"},
    "hei":       {"th": "วันเฮยเต้า (เทวดาร้าย)", "en": "Black-path inauspicious day (黑道)", "mm": "黑道 အမင်္ဂလာရက်"},
    "yatyaza":   {"th": "ยัตยาซา — วันมงคลใหญ่พม่า", "en": "Yatyaza — great Burmese auspicious day", "mm": "ရက်ရာဇာ — မြန်မာ့မင်္ဂလာအထူးရက်"},
    "pyathada":  {"th": "เปียตะดา — วันร้ายพม่า", "en": "Pyathada — Burmese inauspicious day", "mm": "ပြဿဒါး — မြန်မာ့အမင်္ဂလာရက်"},
    "pyathada_pm": {"th": "เปียตะดาช่วงบ่าย — เลี่ยงทำการบ่าย", "en": "Afternoon Pyathada — avoid afternoon", "mm": "မွန်းလွဲပြဿဒါး — မွန်းလွဲပိုင်း ရှောင်ပါ"},
    "friend_day": {"th": "ดาววันนี้เป็นมิตรกับดาววันเกิดคุณ", "en": "Day's planet befriends your birth planet", "mm": "ယနေ့ဂြိုဟ်သည် သင့်မွေးနေ့ဂြိုဟ်၏ မိတ်ဂြိုဟ်ဖြစ်သည်"},
    "enemy_day":  {"th": "ดาววันนี้เป็นศัตรูกับดาววันเกิดคุณ", "en": "Day's planet opposes your birth planet", "mm": "ယနေ့ဂြိုဟ်သည် သင့်မွေးနေ့ဂြိုဟ်၏ ရန်ဂြိုဟ်ဖြစ်သည်"},
    "nawin":      {"th": "วันโกนะวิน (กำลังเลข 9)", "en": "Konawin day (power of nine)", "mm": "ကိုးနဝင်းရက်"},
    "sabbath":    {"th": "วันอุโบสถ — เหมาะทำบุญ", "en": "Sabbath day — good for merit", "mm": "ဥပုသ်နေ့ — ကုသိုလ်ပြုရန်ကောင်း"},
}

UI = {
    "th": {"best": "วันดีที่สุด", "good": "วันดี", "ok": "พอใช้", "avoid": "ควรเลี่ยง",
           "cn_score": "คะแนนจีน", "mm_score": "คะแนนพม่า",
           "chong_you": "⚠️ วันนี้ชงปีนักษัตรของคุณ ({z}) — เลี่ยงเริ่มการใหญ่",
           "no_chong": "✅ วันนี้ไม่ชงปีนักษัตรของคุณ ({z})",
           "cai_dir": "ทิศรับทรัพย์วันนี้", "lucky_hours": "ชั่วโมงมงคลวันนี้",
           "hour_note": "ยามที่เทวดาดี (黃道) และไม่ชงนักษัตรของคุณ",
           "officer": "ผู้คุมวัน", "tianshen": "เทวดาประจำวัน"},
    "en": {"best": "Best day", "good": "Good day", "ok": "Fair", "avoid": "Avoid",
           "cn_score": "Chinese score", "mm_score": "Burmese score",
           "chong_you": "⚠️ Today clashes with your zodiac ({z}) — avoid major starts",
           "no_chong": "✅ Today does not clash with your zodiac ({z})",
           "cai_dir": "Wealth direction today", "lucky_hours": "Lucky hours today",
           "hour_note": "Hours with auspicious spirits (黃道) that don't clash with your zodiac",
           "officer": "Day officer", "tianshen": "Day spirit"},
    "mm": {"best": "အကောင်းဆုံးနေ့", "good": "ကောင်းသောနေ့", "ok": "အသင့်အတင့်", "avoid": "ရှောင်သင့်",
           "cn_score": "တရုတ်ရမှတ်", "mm_score": "မြန်မာရမှတ်",
           "chong_you": "⚠️ ယနေ့သည် သင့်မွေးနှစ်ရာသီ ({z}) နှင့် ထိပ်တိုက်ဖြစ်သည် — အရေးကြီးကိစ္စများ ရှောင်ပါ",
           "no_chong": "✅ ယနေ့သည် သင့်မွေးနှစ်ရာသီ ({z}) နှင့် ထိပ်တိုက်မဖြစ်ပါ",
           "cai_dir": "ယနေ့ ဥစ္စာလာရာအရပ်", "lucky_hours": "ယနေ့ မင်္ဂလာအချိန်များ",
           "hour_note": "黃道 နတ်ကောင်းစိုးသောအချိန်ဖြစ်ပြီး သင့်မွေးနှစ်ရာသီနှင့်လည်း ထိပ်တိုက်မဖြစ်သောအချိန်များ",
           "officer": "နေ့အုပ်စိုးသူ", "tianshen": "နေ့စောင့်နတ်"},
}


def user_zodiac(birthdate: dt.date) -> str:
    return Solar.fromYmd(birthdate.year, birthdate.month, birthdate.day).getLunar().getYearShengXiao()


def _day_signals(date: dt.date, activity_cn: set, zodiac: str, birth_key: str | None):
    """คะแนน+เหตุผลของหนึ่งวัน — คืน (cn_score, mm_score, reasons, excluded)"""
    l = Solar.fromYmd(date.year, date.month, date.day).getLunar()
    cn, mm, reasons, excluded = 0, 0, [], False

    yi, ji = set(l.getDayYi()), set(l.getDayJi())
    if activity_cn & yi:
        cn += 3
        reasons.append(("yi", +3))
    if activity_cn & ji:
        cn -= 4
        reasons.append(("ji", -4))
        excluded = True
    if zodiac and l.getDayChongShengXiao() == zodiac:
        cn -= 4
        reasons.append(("chong", -4))
        excluded = True
    zx = l.getZhiXing()
    if zx == "破":
        cn -= 2
        reasons.append(("po", -2))
    elif zx in ("成", "開", "开"):
        cn += 1
        reasons.append(("cheng_kai", +1))
    if l.getDayTianShenLuck() == "吉":
        cn += 1
        reasons.append(("huang", +1))
    else:
        cn -= 1
        reasons.append(("hei", -1))

    a = astro_day(date)
    if a["yatyaza"]:
        mm += 2
        reasons.append(("yatyaza", +2))
    if a["pyathada"] == 1:
        mm -= 2
        reasons.append(("pyathada", -2))
    elif a["pyathada"] == 2:
        mm -= 1
        reasons.append(("pyathada_pm", -1))
    if a["sabbath"] == 1:
        reasons.append(("sabbath", 0))
    if birth_key:
        dk = day_key_from_date(date)
        rel = relation(DAYS[birth_key]["num"], DAYS[dk]["num"])
        if rel in ("มิตร", "เสริม"):
            mm += 1
            reasons.append(("friend_day", +1))
        elif rel == "ศัตรู":
            mm -= 1
            reasons.append(("enemy_day", -1))
    if date.day in (9, 18, 27):
        mm += 1
        reasons.append(("nawin", +1))
    return cn, mm, reasons, excluded


def rank_days(activity: str, start: dt.date, days: int = 30,
              birthdate: dt.date | None = None, wed_pm: bool = False) -> list:
    """จัดอันดับวันสำหรับกิจกรรม — คืน list of dict เรียงวันดีสุดก่อน"""
    act = ACTIVITIES[activity]["cn"]
    zodiac = user_zodiac(birthdate) if birthdate else ""
    birth_key = day_key_from_date(birthdate, wed_pm) if birthdate else None
    out = []
    for i in range(days):
        d = start + dt.timedelta(days=i)
        cn, mm, reasons, excluded = _day_signals(d, act, zodiac, birth_key)
        total = cn + mm
        if excluded:
            level = "avoid"
        elif total >= 4:
            level = "best"
        elif total >= 2:
            level = "good"
        elif total >= 0:
            level = "ok"
        else:
            level = "avoid"
        out.append({"date": d, "cn": cn, "mm": mm, "total": total,
                    "level": level, "reasons": reasons, "excluded": excluded})
    out.sort(key=lambda x: (x["excluded"], -x["total"], x["date"]))
    return out


def lucky_hours(date: dt.date, zodiac: str = "") -> list:
    """ยามมงคลของวัน: เทวดา 吉 และไม่ชงนักษัตรผู้ใช้"""
    l = Solar.fromYmd(date.year, date.month, date.day).getLunar()
    hours = []
    for t in l.getTimes():
        if t.getTianShenLuck() != "吉":
            continue
        if zodiac and t.getChongShengXiao() == zodiac:
            continue
        span = f"{t.getMinHm()}–{t.getMaxHm()}"
        if span not in [h["span"] for h in hours]:
            hours.append({"span": span, "ganzhi": t.getGanZhi()})
    return hours


def today_fortune(date: dt.date, birthdate: dt.date | None = None, wed_pm: bool = False) -> dict:
    """ดวงวันนี้: ชง, ทิศทรัพย์, ผู้คุมวัน, เทวดา, ชั่วโมงมงคล + สัญญาณพม่า"""
    l = Solar.fromYmd(date.year, date.month, date.day).getLunar()
    zodiac = user_zodiac(birthdate) if birthdate else ""
    birth_key = day_key_from_date(birthdate, wed_pm) if birthdate else None
    cn, mm, reasons, _ = _day_signals(date, set(), zodiac, birth_key)
    a = astro_day(date)
    return {
        "date": date,
        "zodiac": zodiac,
        "chong_today": bool(zodiac and l.getDayChongShengXiao() == zodiac),
        "chong_target": l.getDayChongShengXiao(),
        "cai_direction": l.getDayPositionCaiDesc(),
        "officer": l.getZhiXing(),
        "tianshen": l.getDayTianShen(),
        "tianshen_luck": l.getDayTianShenLuck(),
        "hours": lucky_hours(date, zodiac),
        "yatyaza": bool(a["yatyaza"]),
        "pyathada": a["pyathada"],
        "sabbath": a["sabbath"] == 1,
        "score": cn + mm,
        "reasons": reasons,
    }
