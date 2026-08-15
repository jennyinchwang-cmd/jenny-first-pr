# -*- coding: utf-8 -*-
"""
Cross-tradition synthesis — สรุปข้ามศาสตร์แบบ narrative ไม่หลอมเป็นคะแนนเดียว
==============================================================================
หลัก: แต่ละศาสตร์เป็น namespace แยก — ห้าม vote / เฉลี่ย / แปลงเป็น %
รายงานแค่: สัญญาณเกื้อหนุน (รายศาสตร์) · สัญญาณที่ต้องดูแล (รายศาสตร์)
           · ศาสตร์ที่ให้เฉพาะโปรไฟล์ · ข้อมูลที่ขาด ซึ่งอาจเปลี่ยนผล
"""
from couple_rules import PRODUCTION

RELATIONSHIP = "relationship"


def synthesize(results: dict) -> dict:
    """results: {tradition: TraditionResult} → สรุปข้ามศาสตร์"""
    supportive, challenging, mixed = [], [], []
    profile_only = []

    for trad, res in results.items():
        rel = [h for h in res.production_hits() if h.scope == RELATIONSHIP]
        if not rel:
            profile_only.append(trad)
            continue
        for h in rel:
            entry = {"tradition": trad, "rule_id": h.rule_id, "note_key": h.note_key}
            if h.polarity == "supportive":
                supportive.append(entry)
            elif h.polarity == "challenging":
                challenging.append(entry)
            elif h.polarity == "mixed":
                mixed.append(entry)
            # neutral relationship rules (same branch / same planet / not_listed)
            # ไม่ถูกจัดเข้า supportive/challenging — แสดงแยกกันที่การ์ดของแต่ละศาสตร์

    # ข้อมูลที่ขาดซึ่งอาจเปลี่ยนผล (รวบรวม limitations ที่สำคัญ)
    missing = []
    for trad, res in results.items():
        for lim in res.limitations:
            if lim in ("near_year_boundary", "sign_ingress_ambiguous",
                       "wednesday_sector_unknown"):
                missing.append({"tradition": trad, "limitation": lim})

    return {
        "supportive": supportive,
        "challenging": challenging,
        "mixed": mixed,
        "profile_only": profile_only,
        "missing_data": missing,
    }
