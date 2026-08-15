# -*- coding: utf-8 -*-
"""
ดวงคู่พม่า — โปรไฟล์ 8 ภาค + Mahabote/Nakhat classification — Number Luck
==========================================================================
แสดงเฉพาะสิ่งที่หลักฐานรองรับ (รายบุคคล ไม่ใช่คะแนนความเข้ากัน):
  - 8 ภาควันเกิด (ดาว/สัตว์/ทิศ)  [Maung Htin Aung 1959 + Wikipedia နေ့နံ]
  - Mahabote classification (Binga/Atun/...)  [(myanmar_year - weekday) mod 7 — mmcal, MIT]
  - Nakhat classification (Ogre/Deva/Human)   [myanmar_year mod 3 — mmcal, MIT]

ตารางคู่สมรส (အိမ်ထောင်ရန်/မိတ်, ဓာတ်မိတ်/ရန်) = HOLD — หลักฐาน LOW
จึงไม่มี rule compatibility ของพม่าใน Phase 1
"""
import datetime as _dt

from couple_rules import (RuleHit, TraditionResult, PRODUCTION,
                          SCIENTIFIC_VERY_LOW)
from burmese import DAYS
from mmcal import _jdn, j2m

MAHABOTE_LABELS = ["Binga", "Atun", "Yaza", "Adipati", "Marana", "Thike", "Puti"]
NAKHAT_LABELS = ["Ogre", "Deva", "Human"]

WED_UNKNOWN = "wed_unknown"


def _my_weekday(date: _dt.date) -> int:
    return (_jdn(date) + 2) % 7          # 0=เสาร์ ... 6=ศุกร์ (ตรง mmcal)


def mahabote_class(date: _dt.date) -> int:
    """Mahabote classification 0..6 (ใช้ปีพม่าจริงจาก mmcal ไม่ใช่จุดตัด 15 เม.ย.)"""
    my = j2m(_jdn(date))["my"]
    return (my - _my_weekday(date)) % 7


def nakhat_class(date: _dt.date) -> int:
    my = j2m(_jdn(date))["my"]
    return my % 3


def _profile(day_key: str, birthdate: _dt.date) -> dict:
    """โปรไฟล์ 8 ภาคของหนึ่งคน (รองรับ wed_unknown)"""
    if day_key == WED_UNKNOWN:
        return {"key": WED_UNKNOWN, "unknown": True, "weekday_th": "วันพุธ"}
    d = DAYS[day_key]
    return {"key": day_key, "unknown": False,
            "th": d["th"], "num": d["num"], "planet": d["planet"],
            "dir": d["dir"], "animal": d["animal"], "trait": d["trait"]}


def analyze_burmese(birthdate_a: _dt.date, birthdate_b: _dt.date,
                    sector_a: str, sector_b: str) -> TraditionResult:
    pa = _profile(sector_a, birthdate_a)
    pb = _profile(sector_b, birthdate_b)
    mb_a = mahabote_class(birthdate_a)
    mb_b = mahabote_class(birthdate_b)
    nk_a = nakhat_class(birthdate_a)
    nk_b = nakhat_class(birthdate_b)

    hits = [
        RuleHit(rule_id="sector_profile_a", tradition="burmese", polarity="neutral",
                evidence_confidence="HIGH", input_quality="exact",
                source_id="maung_htin_aung_1959", status=PRODUCTION, scope="individual"),
        RuleHit(rule_id="sector_profile_b", tradition="burmese", polarity="neutral",
                evidence_confidence="HIGH", input_quality="exact",
                source_id="maung_htin_aung_1959", status=PRODUCTION, scope="individual"),
        RuleHit(rule_id="mahabote_a", tradition="burmese", polarity="neutral",
                evidence_confidence="HIGH", input_quality="exact",
                source_id="mmcal_mit", status=PRODUCTION,
                note_key="mahabote_individual", scope="individual"),
        RuleHit(rule_id="mahabote_b", tradition="burmese", polarity="neutral",
                evidence_confidence="HIGH", input_quality="exact",
                source_id="mmcal_mit", status=PRODUCTION,
                note_key="mahabote_individual", scope="individual"),
        RuleHit(rule_id="nakhat_a", tradition="burmese", polarity="neutral",
                evidence_confidence="HIGH", input_quality="exact",
                source_id="mmcal_mit", status=PRODUCTION,
                note_key="nakhat_individual", scope="individual"),
        RuleHit(rule_id="nakhat_b", tradition="burmese", polarity="neutral",
                evidence_confidence="HIGH", input_quality="exact",
                source_id="mmcal_mit", status=PRODUCTION,
                note_key="nakhat_individual", scope="individual"),
    ]

    limitations = []
    locked = ["marriage_mnemonic_pairs", "mahabote_synastry"]
    if pa["unknown"] or pb["unknown"]:
        limitations.append("wednesday_sector_unknown")

    detail = {
        "a": {"profile": pa, "mahabote": MAHABOTE_LABELS[mb_a],
              "mahabote_idx": mb_a, "nakhat": NAKHAT_LABELS[nk_a], "nakhat_idx": nk_a},
        "b": {"profile": pb, "mahabote": MAHABOTE_LABELS[mb_b],
              "mahabote_idx": mb_b, "nakhat": NAKHAT_LABELS[nk_b], "nakhat_idx": nk_b},
        "scientific_evidence": SCIENTIFIC_VERY_LOW,
    }
    return TraditionResult("burmese", hits, limitations, locked, 2, detail)
