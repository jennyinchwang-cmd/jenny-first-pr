# -*- coding: utf-8 -*-
"""
ดวงรายสัปดาห์ / รายเดือน — Number Luck (หลายศาสตร์: พม่า + จีน + อินเดีย)
==========================================================================
คะแนนรายวันจากปัจจัยที่คำนวณได้จริง (ไม่มั่ว):
  🇲🇲 พม่า:  ยัตยาซา/เปียตะดา (mmcal) · ดาวประจำวัน × ดาววันเกิด (คู่มิตร/ศัตรู)
            · วันโกนะวิน (วันที่ 9, 18, 27) · วันอุโบสถ (มิติบุญ)
  🇨🇳 จีน:   วันชงปีนักษัตรผู้ใช้ · ผู้คุมวัน 破 · หวงเต้า/เฮยเต้า (lunar-python, MIT)
  🇮🇳 อินเดีย: เลขนำโชคประจำช่วงจาก Mulank ของวันเกิด
"""
import datetime as _dt

from burmese import DAYS, day_key_from_date, relation, MULANK_TABLE, _digital_root
from mmcal import astro_day

try:
    from lunar_python import Solar as _Solar
    _HAS_LUNAR = True
except Exception:
    _HAS_LUNAR = False

# นักษัตรจีน 12 ตัว (อักษรจีนจาก lunar-python)
ZODIAC_CN = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]


def user_zodiac(birthdate: _dt.date) -> str:
    """ปีนักษัตรจีนของผู้ใช้ (ตัดขอบปีตามปฏิทินจีนจริง)"""
    if not _HAS_LUNAR:
        return ""
    return _Solar.fromYmd(birthdate.year, birthdate.month, birthdate.day).getLunar().getYearShengXiao()


def day_quality(date: _dt.date, birth_key: str, zodiac: str = "") -> dict:
    """คุณภาพของหนึ่งวันสำหรับผู้ใช้หนึ่งคน — คะแนน + เหตุผล (reason keys สำหรับ i18n)"""
    score = 0
    reasons = []  # (key, params, +/-)

    # ---- พม่า: ปฏิทินโหราศาสตร์ ----
    a = astro_day(date)
    if a["yatyaza"]:
        score += 2
        reasons.append(("yatyaza", {}, +2))
    if a["pyathada"] == 1:
        score -= 2
        reasons.append(("pyathada", {}, -2))
    elif a["pyathada"] == 2:
        score -= 1
        reasons.append(("pyathada_pm", {}, -1))
    if a["sabbath"] == 1:
        reasons.append(("sabbath", {}, 0))

    # ---- พม่า: ดาวประจำวัน × ดาววันเกิด ----
    dk = day_key_from_date(date)          # วันพุธใช้ช่วงเช้าเป็นตัวแทนทั้งวัน
    dnum, bnum = DAYS[dk]["num"], DAYS[birth_key]["num"]
    rel = relation(bnum, dnum)
    if rel in ("มิตร", "เสริม"):
        score += 2
        reasons.append(("friend_day", {"daynum": dnum}, +2))
    elif rel == "ศัตรู":
        score -= 2
        reasons.append(("enemy_day", {"daynum": dnum}, -2))

    # ---- พม่า: วันโกนะวิน ----
    if date.day in (9, 18, 27):
        score += 1
        reasons.append(("nawin_day", {"d": date.day}, +1))

    # ---- จีน ----
    if _HAS_LUNAR:
        l = _Solar.fromYmd(date.year, date.month, date.day).getLunar()
        if zodiac and l.getDayChongShengXiao() == zodiac:
            score -= 3
            reasons.append(("chong", {}, -3))
        zx = l.getZhiXing()
        if zx == "破":
            score -= 1
            reasons.append(("po_day", {}, -1))
        elif zx in ("成", "開", "开"):
            score += 1
            reasons.append(("cheng_kai", {"zx": zx}, +1))
        luck = l.getDayTianShenLuck()
        if luck == "吉":
            score += 1
            reasons.append(("huangdao", {}, +1))
        elif luck == "凶":
            score -= 1
            reasons.append(("heidao", {}, -1))

    if score >= 4:
        level = "ดีมาก"
    elif score >= 2:
        level = "ดี"
    elif score >= 0:
        level = "กลาง"
    elif score >= -2:
        level = "ระวัง"
    else:
        level = "หลีกเลี่ยง"
    icon = {"ดีมาก": "🟢", "ดี": "🟩", "กลาง": "⚪", "ระวัง": "🟠", "หลีกเลี่ยง": "🔴"}[level]
    return {"date": date, "wd_key": dk, "score": score, "level": level, "icon": icon,
            "reasons": reasons, "day_planet_num": dnum}


def weekly_fortune(birthdate: _dt.date = None, wednesday_pm: bool = False,
                   day_key: str = None, start: _dt.date = None) -> dict:
    """ดวง 7 วันข้างหน้า (เริ่มวันนี้)"""
    bkey = day_key or day_key_from_date(birthdate, wednesday_pm)
    zodiac = user_zodiac(birthdate) if birthdate else ""
    start = start or _dt.date.today()
    days = [day_quality(start + _dt.timedelta(days=i), bkey, zodiac) for i in range(7)]
    avg = sum(d["score"] for d in days) / 7
    overall = round(max(5, min(98, 55 + avg * 9)), 0)      # แปลงเป็น % อ่านง่าย
    best = max(days, key=lambda d: d["score"])
    worst = min(days, key=lambda d: d["score"])
    # เลขนำโชคช่วงนี้: เลขวันเกิด + ดาวมิตร + 9 (นวิน) + Mulank seek (ถ้ารู้วันที่เกิด)
    lucky = {DAYS[bkey]["num"], 9}
    from burmese import FRIEND_PAIRS
    for p in FRIEND_PAIRS:
        if DAYS[bkey]["num"] in p:
            lucky |= set(p)
    mulank = None
    if birthdate:
        mulank = _digital_root(birthdate.day)
        lucky |= set(list(MULANK_TABLE[mulank][0])[:3])
    return {"days": days, "overall": overall, "best": best, "worst": worst,
            "birth_key": bkey, "zodiac": zodiac, "mulank": mulank,
            "lucky_numbers": sorted(lucky)}


def monthly_fortune(birthdate: _dt.date = None, wednesday_pm: bool = False,
                    day_key: str = None, start: _dt.date = None, days: int = 30) -> dict:
    """ภาพรวม 30 วันข้างหน้า"""
    bkey = day_key or day_key_from_date(birthdate, wednesday_pm)
    zodiac = user_zodiac(birthdate) if birthdate else ""
    start = start or _dt.date.today()
    all_days = [day_quality(start + _dt.timedelta(days=i), bkey, zodiac) for i in range(days)]
    good = [d for d in all_days if d["score"] >= 2]
    bad = [d for d in all_days if d["score"] <= -2]
    avg = sum(d["score"] for d in all_days) / len(all_days)
    overall = round(max(5, min(98, 55 + avg * 9)), 0)
    top3 = sorted(all_days, key=lambda d: -d["score"])[:3]
    chong_days = [d for d in all_days if any(r[0] == "chong" for r in d["reasons"])]
    yat_days = [d for d in all_days if any(r[0] == "yatyaza" for r in d["reasons"])]
    pya_days = [d for d in all_days if any(r[0] in ("pyathada", "pyathada_pm") for r in d["reasons"])]
    sab_days = [d for d in all_days if any(r[0] == "sabbath" for r in d["reasons"])]
    return {"days": all_days, "overall": overall, "good": good, "bad": bad, "top3": top3,
            "chong_days": chong_days, "yatyaza_days": yat_days, "pyathada_days": pya_days,
            "sabbath_days": sab_days, "birth_key": bkey, "zodiac": zodiac}


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    w = weekly_fortune(_dt.date(1995, 1, 1), start=_dt.date(2026, 7, 15))
    print(f"สัปดาห์นี้ {w['overall']:.0f}% | นักษัตร {w['zodiac']} | เลขนำโชค {w['lucky_numbers']}")
    for d in w["days"]:
        rs = ",".join(r[0] for r in d["reasons"])
        print(f"  {d['icon']} {d['date']} score={d['score']:+d} [{rs}]")
    m = monthly_fortune(_dt.date(1995, 1, 1), start=_dt.date(2026, 7, 15))
    print(f"เดือนนี้ {m['overall']:.0f}% | วันดี {len(m['good'])} | วันระวัง {len(m['bad'])} | วันชง {len(m['chong_days'])}")
