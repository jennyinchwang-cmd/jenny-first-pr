# -*- coding: utf-8 -*-
"""
ดวงคู่ตะวันตก — Sun-sign overview (วันเกิดอย่างเดียว) — Number Luck
===================================================================
เลเยอร์ date-only: ราศีอาทิตย์ + ธาตุ + คุณภาพ (Modality)
⚠️ ไม่ใช่ full synastry — ไม่มีลัคนา/เรือน/มุมดาวข้ามดวง (ต้องมีเวลา+สถานที่)

คำนวณลองจิจูดสุริยะแบบ tropical ด้วยสูตรดาราศาสตร์สาธารณะ (Meeus low-precision,
ความแม่น ~0.01°) — พอแยกราศีได้ ยกเว้นช่วงคาบเกี่ยวกับวันเปลี่ยนราศีซึ่งจะ flag ไว้
"""
import datetime as _dt
import math

from couple_rules import (RuleHit, TraditionResult, PRODUCTION,
                          SCIENTIFIC_VERY_LOW)

SIGN_NAMES = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
              "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

# ธาตุ ตาม index ราศี
ELEMENTS = {0: "fire", 1: "earth", 2: "air", 3: "water", 4: "fire", 5: "earth",
            6: "air", 7: "water", 8: "fire", 9: "earth", 10: "air", 11: "water"}
# คุณภาพ (Modality)
MODALITIES = {0: "cardinal", 1: "fixed", 2: "mutable", 3: "cardinal", 4: "fixed",
              5: "mutable", 6: "cardinal", 7: "fixed", 8: "mutable", 9: "cardinal",
              10: "fixed", 11: "mutable"}

_ELEMENT_KEY = {"fire": "fire", "earth": "earth", "air": "air", "water": "water"}


def _julian_day(year: int, month: int, day: float) -> float:
    """Julian Day (Meeus)"""
    if month <= 2:
        year -= 1
        month += 12
    a = math.floor(year / 100)
    b = 2 - a + math.floor(a / 4)
    return math.floor(365.25 * (year + 4716)) + math.floor(30.6001 * (month + 1)) + day + b - 1524.5


def sun_longitude(date: _dt.date, hour: float = 0.0) -> float:
    """ลองจิจูดสุริยะปรากฏ (tropical, องศา 0–360)"""
    jd = _julian_day(date.year, date.month, date.day + hour / 24.0)
    T = (jd - 2451545.0) / 36525.0
    L0 = (280.46646 + T * (36000.76983 + T * 0.0003032)) % 360.0
    M = (357.52911 + T * (35999.05029 - 0.0001537 * T)) % 360.0
    Mr = math.radians(M)
    e = 0.016708634 - T * (0.000042037 + 0.0000001267 * T)
    C = ((1.914602 - T * (0.004817 + 0.000014 * T)) * math.sin(Mr)
         + (0.019993 - 0.000101 * T) * math.sin(2 * Mr)
         + 0.000289 * math.sin(3 * Mr))
    true_long = L0 + C
    omega = 125.04 - 1934.136 * T
    apparent = true_long - 0.00569 - 0.00478 * math.sin(math.radians(omega))
    return apparent % 360.0


def _sign_of(lon: float) -> int:
    return int(lon) // 30 % 12


def sun_sign(date: _dt.date) -> dict:
    """ราศีอาทิตย์ + ระดับองศา + flag ถ้าคาบเกี่ยวกับวันเปลี่ยนราศี"""
    lon0 = sun_longitude(date, 0.0)
    lon24 = sun_longitude(date, 24.0)
    idx0, idx24 = _sign_of(lon0), _sign_of(lon24)
    ingress = idx0 != idx24
    idx = idx0 if not ingress else idx24  # ถ้าคาบเกี่ยว ใช้ค่าราศีปลายวัน (พร้อม flag)
    return {"sign_index": idx, "sign": SIGN_NAMES[idx],
            "element": ELEMENTS[idx], "modality": MODALITIES[idx],
            "degree": round(lon0 % 30, 2),
            "longitude": round(lon0, 3), "ingress_ambiguous": ingress}


def element_relation(el_a: str, el_b: str) -> str:
    """หมวดความสัมพันธ์ธาตุ (narrative ไม่ใช่คะแนน)"""
    if el_a == el_b:
        return "same_element"
    pair = frozenset((el_a, el_b))
    if pair == frozenset(("fire", "air")) or pair == frozenset(("earth", "water")):
        return "supportive"
    return "adjust"


def modality_relation(mod_a: str, mod_b: str) -> str:
    return "same_modality" if mod_a == mod_b else "different_modality"


def analyze_western(birthdate_a: _dt.date, birthdate_b: _dt.date) -> TraditionResult:
    sa = sun_sign(birthdate_a)
    sb = sun_sign(birthdate_b)

    hits = [
        RuleHit(rule_id="sun_sign_a", tradition="western", polarity="neutral",
                evidence_confidence="HIGH", input_quality="exact",
                source_id="tropical_zodiac", status=PRODUCTION, scope="individual"),
        RuleHit(rule_id="sun_sign_b", tradition="western", polarity="neutral",
                evidence_confidence="HIGH", input_quality="exact",
                source_id="tropical_zodiac", status=PRODUCTION, scope="individual"),
        RuleHit(rule_id="element_relation", tradition="western",
                polarity="supportive" if element_relation(sa["element"], sb["element"]) == "supportive"
                else ("neutral" if element_relation(sa["element"], sb["element"]) == "same_element" else "mixed"),
                evidence_confidence="HIGH", input_quality="exact",
                source_id="tropical_zodiac", status=PRODUCTION,
                note_key="element_narrative"),
    ]

    limitations = ["sun_sign_only", "not_full_synastry"]
    locked = ["ascendant", "houses", "full_synastry", "composite"]
    if sa["ingress_ambiguous"] or sb["ingress_ambiguous"]:
        limitations.append("sign_ingress_ambiguous")

    detail = {
        "a": sa, "b": sb,
        "element_relation": element_relation(sa["element"], sb["element"]),
        "modality_relation": modality_relation(sa["modality"], sb["modality"]),
        "scientific_evidence": SCIENTIFIC_VERY_LOW,
    }
    return TraditionResult("western", hits, limitations, locked, 2, detail)
