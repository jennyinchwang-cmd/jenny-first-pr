# -*- coding: utf-8 -*-
"""
ดวงคู่จีน — ชั้นเร็ว (Quick layer): ความสัมพันธ์กิ่งดินปีเกิด — Number Luck
==========================================================================
ใช้เฉพาะ "กิ่งปี" (年支) ของสองคนเทียบกฎ 六合/三合/六冲/六害/三刑/破
⚠️ นี่คือ 1 ใน 8 อักษร (八字) เท่านั้น ไม่ใช่ปาจื่อเต็ม — ห้ามฟันธงดวงคู่

แหล่งปฐมภูมิ: 《三命通會》卷二 (六合/三合/六冲/六害/三刑; 破 เป็นข้อมูลทดลอง)
ขอบปี: ใช้立春 (getYearZhiIndexByLiChun) ตามสำนัก BaZi; ประกาศ convention ไว้เสมอ
"""
import datetime as _dt

from couple_rules import (RuleHit, TraditionResult, PRODUCTION, EXPERIMENTAL,
                          SCIENTIFIC_VERY_LOW)

try:
    from lunar_python import Solar as _Solar
    _HAS_LUNAR = True
except Exception:
    _HAS_LUNAR = False

# กิ่งดิน 0..11 = 子..亥
BRANCH = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

# กิ่ง → (สัตว์, ธาตุ[canonical], หยิน/หยาง)  ตาม HKO 十二生肖 + 《三命通會》
BRANCH_INFO = {
    "子": ("鼠", "water", "หยาง"), "丑": ("牛", "earth", "หยิน"),
    "寅": ("虎", "wood", "หยาง"), "卯": ("兔", "wood", "หยิน"),
    "辰": ("龙", "earth", "หยาง"), "巳": ("蛇", "fire", "หยิน"),
    "午": ("马", "fire", "หยาง"), "未": ("羊", "earth", "หยิน"),
    "申": ("猴", "metal", "หยาง"), "酉": ("鸡", "metal", "หยิน"),
    "戌": ("狗", "earth", "หยาง"), "亥": ("猪", "water", "หยิน"),
}

_HD = "HIGH"   # มีตัวบทตรวจได้ชัด
_MD = "MED"    # มีหลายสำนัก/ต้องตีความ
_LD = "LOW"    # หลักฐานอ่อน → experimental


def _pairs(*ps):
    return {frozenset(p) for p in ps}


LIUHE = _pairs((0, 1), (2, 11), (3, 10), (4, 9), (5, 8), (6, 7))          # 六合
LIUCHONG = _pairs((0, 6), (1, 7), (2, 8), (3, 9), (4, 10), (5, 11))       # 六冲
LIUHAI = _pairs((0, 7), (1, 6), (2, 5), (3, 4), (8, 11), (9, 10))         # 六害
PO = _pairs((0, 9), (1, 4), (2, 11), (3, 6), (5, 8), (7, 10))             # 破 (ทดลอง)

SANHE_MAP = {                                                              # 三合 → ธาตุ
    frozenset({8, 0, 4}): "น้ำ",   # 申子辰
    frozenset({11, 3, 7}): "ไม้",  # 亥卯未
    frozenset({2, 6, 10}): "ไฟ",   # 寅午戌
    frozenset({5, 9, 1}): "ทอง",   # 巳酉丑
}

SANXING_TRIPLES = [frozenset({2, 5, 8}), frozenset({1, 10, 7})]            # 寅巳申, 丑戌未
ZIMAO = frozenset({0, 3})                                                   # 子卯 (無禮之刑)
ZI_XING = {4, 6, 9, 11}                                                    # 辰午酉亥 (自刑)


def branch_index_of(birthdate: _dt.date, convention: str = "lichun"):
    """คืน (branch_index, near_boundary) — near_boundary=เกิดช่วงคาบเกี่ยวกับขอบปี"""
    if not _HAS_LUNAR:
        return None, False
    lunar = _Solar.fromYmd(birthdate.year, birthdate.month, birthdate.day).getLunar()
    idx_li = lunar.getYearZhiIndexByLiChun()
    idx_lny = lunar.getYearZhiIndex()
    near = idx_li != idx_lny            # เกิดระหว่างวันตรุษจีนกับ立春
    return (idx_li if convention == "lichun" else idx_lny), near


def _hit(rule_id, polarity, conf, source, status=PRODUCTION, note_key=None, convention=None):
    return RuleHit(rule_id=rule_id, tradition="chinese", polarity=polarity,
                   evidence_confidence=conf, input_quality="exact",
                   source_id=source, status=status, note_key=note_key,
                   convention=convention)


def branch_rules(ia: int, ib: int) -> list:
    """ตรวจทุกกฎระหว่างสองกิ่งดิน (index 0..11)"""
    hits = []
    pair = frozenset((ia, ib))
    if ia == ib:
        hits.append(_hit("same_branch", "neutral", _HD, "hko_ganzhi",
                         note_key="same_branch"))
    if pair in LIUHE:
        hits.append(_hit("liuhe", "supportive", _HD, "sanmingtonghui_juan2",
                         convention="lichun_year"))
    for group, elem in SANHE_MAP.items():
        if ia in group and ib in group:
            hits.append(_hit("sanhe_2of3", "supportive", _HD, "sanmingtonghui_juan2",
                             note_key="sanhe_2of3"))
            break
    if pair in LIUCHONG:
        hits.append(_hit("liuchong", "challenging", _HD, "sanmingtonghui_juan2",
                         note_key="chong_not_fatal"))
    if pair in LIUHAI:
        hits.append(_hit("liuhai", "challenging", _HD, "sanmingtonghui_juan2"))
    if pair == ZIMAO:
        hits.append(_hit("sanxing_zimao", "challenging", _MD, "sanmingtonghui_juan2",
                         note_key="xing_context"))
    for group in SANXING_TRIPLES:
        if ia in group and ib in group:
            hits.append(_hit("sanxing_2of3", "challenging", _MD, "sanmingtonghui_juan2",
                             note_key="xing_2of3"))
            break
    if ia == ib and ia in ZI_XING:
        hits.append(_hit("zixing", "challenging", _MD, "sanmingtonghui_juan2",
                         note_key="xing_context"))
    if pair in PO:
        hits.append(_hit("po", "mixed", _LD, "sanmingtonghui_juan2",
                         status=EXPERIMENTAL, note_key="po_experimental"))
    return hits


def analyze_chinese(birthdate_a: _dt.date, birthdate_b: _dt.date,
                    convention: str = "lichun") -> TraditionResult:
    limitations, locked = [], []
    if not _HAS_LUNAR:
        limitations.append("no_lunar")
        return TraditionResult("chinese", [], limitations, ["bazi", "time_pillar"], 0, {})

    ia, na = branch_index_of(birthdate_a, convention)
    ib, nb = branch_index_of(birthdate_b, convention)
    hits = branch_rules(ia, ib)

    locked.append("full_bazi")
    locked.append("time_pillar")
    limitations.append("quick_layer_only")
    if na or nb:
        limitations.append("near_year_boundary")

    detail = {
        "convention": "lichun" if convention == "lichun" else "lunar_new_year",
        "chart_completeness": "1/8_branches",   # ใช้แค่กิ่งปี = 1 ใน 8 ตัวอักษร
        "a": {"branch": BRANCH[ia], "info": BRANCH_INFO[BRANCH[ia]], "near": na},
        "b": {"branch": BRANCH[ib], "info": BRANCH_INFO[BRANCH[ib]], "near": nb},
        "scientific_evidence": SCIENTIFIC_VERY_LOW,
    }
    return TraditionResult("chinese", hits, limitations, locked, 2, detail)
