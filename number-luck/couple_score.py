# -*- coding: utf-8 -*-
"""
คะแนนความเหมาะสมคู่ — ระบบผสม Number Luck (product convention ไม่ใช่ตำราเดี่ยว)
==============================================================================
รวมสัญญาณจาก 4 ศาสตร์ (ดาวประจำวัน / จีน / ไทย / ตะวันตก) เป็น % เดียว + แถบสี
น้ำหนักเป็น product decision ของ Number Luck ไม่ได้อ้างว่ามาจากตำราหนึ่งใดโดยตรง
คะแนนนี้สื่อถึง "ระดับความเหมาะสมตามคติความเชื่อ" ไม่ใช่การพิสูจน์ทางวิทยาศาสตร์
"""
from couple_rules import PRODUCTION

# ---------- น้ำหนักคะแนน (product convention) ----------
_CN = {
    "liuhe": +18,        # 六合 คู่ประสาน
    "sanhe_2of3": +10,   # 三合 2/3 กลุ่มธาตุเดียวกัน
    "same_branch": +5,   # กิ่งปีเดียวกัน
    "liuchong": -14,     # 六冲 ปะทะ
    "liuhai": -10,       # 六害 บั่นทอน
    "sanxing_zimao": -10, "sanxing_2of3": -10, "zixing": -10,  # 三刑/自刑
    "po": -4,            # 破 (experimental — น้ำหนักเบา)
}
_DAY_PLANET = {"friend": +12, "same": +6, "enemy": -12, "not_listed": 0, None: 0}
_WEST_ELEM = {"supportive": +8, "same_element": +5, "adjust": -3}
_WEST_MOD = {"same_modality": +3, "different_modality": 0}

BASELINE = 50

BANDS = [
    (75, "green", "excellent"),
    (60, "teal", "good"),
    (45, "yellow", "adjust"),
    (30, "orange", "challenging"),
    (0, "red", "difficult"),
]


def _band_of(score: int):
    for lo, band, key in BANDS:
        if score >= lo:
            return band, key
    return "red", "difficult"


def score_couple(res: dict) -> dict:
    """res: {tradition: TraditionResult} → คะแนน + แถบสี + verdict + ปัจจัยที่กระทบ"""
    points = BASELINE
    factors = []  # (tradition, rule_id, delta)

    # --- จีน: ความสัมพันธ์กิ่งดิน ---
    ch = res.get("chinese")
    if ch is not None:
        for h in ch.production_hits():
            if h.scope != "relationship":
                continue
            d = _CN.get(h.rule_id)
            if d:
                points += d
                factors.append(("chinese", h.rule_id, d))

    # --- ดาวประจำวัน (พม่า+ไทยร่วม: คู่มิตร/ศัตรู) ---
    th = res.get("thai")
    if th is not None:
        rel = th.detail.get("relation")
        d = _DAY_PLANET.get(rel, 0)
        if d:
            points += d
            factors.append(("day_planet", f"planet_{rel}", d))

    # --- ตะวันตก: ธาตุ + คุณภาพ ---
    w = res.get("western")
    if w is not None:
        wd = w.detail
        er = wd.get("element_relation")
        d = _WEST_ELEM.get(er, 0)
        if d:
            points += d
            factors.append(("western", f"elem_{er}", d))
        mr = wd.get("modality_relation")
        d = _WEST_MOD.get(mr, 0)
        if d:
            points += d
            factors.append(("western", f"mod_{mr}", d))

    score = max(0, min(100, points))
    band, verdict_key = _band_of(score)
    return {"score": score, "band": band, "verdict_key": verdict_key, "factors": factors}
