# -*- coding: utf-8 -*-
"""
ดวงคู่ไทย — ทักษา + คู่มิตร/คู่ศัตรูดาวประจำวัน — Number Luck
==============================================================
เลขดาวไทย 1–8: 1 อาทิตย์ · 2 จันทร์ · 3 อังคาร · 4 พุธกลางวัน ·
               5 พฤหัสบดี · 6 ศุกร์ · 7 เสาร์ · 8 ราหู/พุธกลางคืน
(ตรงกับเลขวันใน burmese.DAYS — แต่แยก namespace ไม่ปนกับคู่เวรพม่า)

ทักษา: ลำดับดาว 1→2→3→4→7→5→8→6 (วนรอบ) จับ 8 ภูมิ
        บริวาร→อายุ→เดช→ศรี→มูละ→อุตสาหะ→มนตรี→กาลกิณี

คู่มิตร/ศัตรู = category (friend/enemy/not_listed) ไม่ใช่คะแนนความรัก
"""
import datetime as _dt

from couple_rules import (RuleHit, TraditionResult, PRODUCTION,
                          SCIENTIFIC_VERY_LOW)
from burmese import DAYS

WED_UNKNOWN = "wed_unknown"

_THAI_DAY_NUM = {"sun": 1, "mon": 2, "tue": 3, "wed_am": 4, "thu": 5, "fri": 6, "sat": 7, "wed_pm": 8}

# ลำดับดาวในวงทักษา (วนรอบ)
THAKSA_ORDER = [1, 2, 3, 4, 7, 5, 8, 6]
# 8 ภูมิ
THAKSA_REGIONS = ["บริวาร", "อายุ", "เดช", "ศรี", "มูละ", "อุตสาหะ", "มนตรี", "กาลกิณี"]

# คู่มิตร (confidence ปานกลาง — ตรวจแหล่งไทยทั่วไปได้ตรงกัน)
THAI_FRIEND = {frozenset(p) for p in [(1, 5), (2, 4), (3, 6), (7, 8)]}
# คู่ศัตรู (เฉพาะ 4 คู่ที่ตรวจได้; 2–8 และ 3–7 ในโค้ดเดิมยังไม่มีหลักฐาน)
THAI_ENEMY = {frozenset(p) for p in [(1, 3), (4, 8), (6, 7), (2, 5)]}

_MD = "MED"
_HD = "HIGH"


def day_key_to_num(day_key: str) -> int:
    return _THAI_DAY_NUM[day_key]


def thaksa_profile(day_num: int) -> dict:
    """ผังทักษารายบุคคล: คืน {region_name: star_num} ตามลำดับภูมิ"""
    if day_num not in THAKSA_ORDER:
        raise ValueError(f"เลขดาวไทยต้องเป็น 1-8 ได้: {day_num}")
    pos = THAKSA_ORDER.index(day_num)
    return {THAKSA_REGIONS[i]: THAKSA_ORDER[(pos + i) % 8] for i in range(8)}


def planet_relation(num_a: int, num_b: int) -> str:
    """category: same | friend | enemy | not_listed (ไม่ใช่คะแนน)"""
    if num_a == num_b:
        return "same"
    pair = frozenset((num_a, num_b))
    if pair in THAI_FRIEND:
        return "friend"
    if pair in THAI_ENEMY:
        return "enemy"
    return "not_listed"


def analyze_thai(day_key_a: str, day_key_b: str) -> TraditionResult:
    """day_key_a/b เป็น key ใน burmese.DAYS หรือ WED_UNKNOWN"""
    na = _THAI_DAY_NUM.get(day_key_a)
    nb = _THAI_DAY_NUM.get(day_key_b)

    hits, limitations, locked = [], ["thai_planet_med", "thaksa_derived_app"], ["mahasomphong", "lagna_bhava"]

    detail = {"a": {"key": day_key_a, "num": na}, "b": {"key": day_key_b, "num": nb},
              "relation": None, "b_in_a": [], "a_in_b": [],
              "scientific_evidence": SCIENTIFIC_VERY_LOW}

    # คู่มิตร/ศัตรู — ต้องรู้เลขดาวทั้งสองฝ่าย (พุธไม่ทราบช่วง = แยก 4/8 ไม่ได้)
    if na is None or nb is None:
        limitations.append("wednesday_sector_unknown")
    else:
        rel = planet_relation(na, nb)
        detail["relation"] = rel
        if rel in ("friend", "enemy"):
            polarity = "supportive" if rel == "friend" else "challenging"
            hits.append(RuleHit(
                rule_id=f"planet_{rel}", tradition="thai", polarity=polarity,
                evidence_confidence=_MD, input_quality="exact",
                source_id="nlt_154", status=PRODUCTION,
                note_key="thai_planet_category"))
        elif rel == "same":
            hits.append(RuleHit(
                rule_id="planet_same", tradition="thai", polarity="neutral",
                evidence_confidence=_MD, input_quality="exact",
                source_id="nlt_154", status=PRODUCTION))

    # ทักษารายบุคคล (คำนวณเฉพาะฝ่ายที่รู้เลขดาว)
    ta = thaksa_profile(na) if na is not None else None
    tb = thaksa_profile(nb) if nb is not None else None
    detail["a"]["thaksa"] = ta
    detail["b"]["thaksa"] = tb

    # cross-chart = derived_application (เฉพาะเมื่อรู้ทั้งสองฝ่าย)
    if ta is not None and tb is not None:
        b_in_a = [r for r, s in ta.items() if s == nb]
        a_in_b = [r for r, s in tb.items() if s == na]
        detail["b_in_a"] = b_in_a
        detail["a_in_b"] = a_in_b
        for region in b_in_a:
            hits.append(RuleHit(
                rule_id="thaksa_overlay", tradition="thai", polarity="neutral",
                evidence_confidence=_HD, input_quality="exact",
                source_id="thaksa_vannavidas", status=PRODUCTION,
                note_key="thaksa_derived", scope="individual"))

    return TraditionResult("thai", hits, limitations, locked, 1, detail)
