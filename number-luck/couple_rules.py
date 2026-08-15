# -*- coding: utf-8 -*-
"""
Rule lifecycle gate สำหรับดวงคู่หลายศาสตร์ — Number Luck
========================================================
ทุกกฎต้องมี source / evidence_confidence / input_quality / status
production loader ต้องอ่านเฉพาะ rule ที่ status == PRODUCTION เท่านั้น

แกน 3 ค่าความเชื่อมั่น (ห้ามรวมเป็นค่าเดียว):
  1. evidence_confidence — คุณภาพหลักฐานของกฎในศาสตร์นั้น (HIGH|MED|LOW)
  2. input_quality      — ข้อมูลบุคคลพอคำนวณหรือไม่ (exact|partial|ambiguous)
  3. scientific_evidence — หลักฐานเชิงประจักษ์ (โหราศาสตร์ = very_low เสมอ)

อิง: research/couple-multisystem-research.md และ reference ของ skill number-luck-project
"""
from dataclasses import dataclass, field

PRODUCTION = "PRODUCTION"
EXPERIMENTAL = "EXPERIMENTAL"
HOLD = "HOLD"

# scientific_evidence คงที่สำหรับโหราศาสตร์ทุกสาย
SCIENTIFIC_VERY_LOW = "very_low"


@dataclass(frozen=True)
class RuleHit:
    rule_id: str
    tradition: str                       # burmese|chinese|thai|western
    polarity: str                        # supportive|mixed|challenging|neutral
    evidence_confidence: str             # HIGH|MED|LOW
    input_quality: str                   # exact|partial|ambiguous
    source_id: str
    status: str = PRODUCTION
    convention: str | None = None
    note_key: str | None = None          # key เข้า couple_texts (หมายเหตุต่อกฎ)
    scope: str = "relationship"          # relationship | individual (ข้อมูลรายบุคคล)


@dataclass
class TraditionResult:
    tradition: str
    rules_hit: list
    limitations: list
    locked_sections: list
    data_level: int                      # 1|2|3
    detail: dict = field(default_factory=dict)

    def production_hits(self) -> list:
        return [r for r in self.rules_hit if r.status == PRODUCTION]


# ---------- แหล่งอ้างอิง (source_id → ข้อมูล) ----------
SOURCES = {
    # พม่า
    "maung_htin_aung_1959": {
        "url": "https://archive.org/details/xxVG_folk-elements-in-burmese-buddhism-by-maung-htin-aung-1959-rangoon-u-hla-maung-bu",
        "license": "หนังสือมีลิขสิทธิ์; อ้างข้อเท็จจริงเท่านั้น",
        "kind": "book_scan",
    },
    "mmcal_mit": {
        "url": "https://github.com/yan9a/mmcal",
        "license": "MIT",
        "kind": "source_code",
    },
    # จีน
    "sanmingtonghui_juan2": {
        "url": "https://zh.wikisource.org/wiki/三命通會/卷二",
        "license": "ต้นฉบับหมิงเป็นสาธารณสมบัติ; หน้า Wikisource CC BY-SA 4.0",
        "kind": "primary_text",
    },
    "hko_ganzhi": {
        "url": "https://www.hko.gov.hk/sc/gts/time/stemsandbranches.htm",
        "license": "© Hong Kong Observatory; ใช้ข้อเท็จจริง",
        "kind": "institution",
    },
    "lunar_python_mit": {
        "url": "https://github.com/6tail/lunar-python",
        "license": "MIT",
        "kind": "source_code",
    },
    # ไทย
    "nlt_154": {
        "url": "https://digital.nlt.go.th/dlib/api/items/1421",
        "license": "ระเบียนหอสมุดแห่งชาติ; ไม่มี scan ให้ตรวจสูตร",
        "kind": "institution_catalog",
    },
    "thaksa_vannavidas": {
        "url": "https://so06.tci-thaijo.org/index.php/VANNAVIDAS/article/view/48400",
        "license": "บทความวิชาการมีลิขสิทธิ์; สรุปกฎเท่านั้น",
        "kind": "academic",
    },
    "rst_thaksa": {
        "url": "http://legacy.orst.go.th/?knowledges=ทักษา-๑๘-ธันวาคม-๒๕๕๒",
        "license": "© สำนักงานราชบัณฑิตยสภา; สรุปข้อเท็จจริง",
        "kind": "institution",
    },
    # ตะวันตก
    "tropical_zodiac": {
        "url": "https://www.astro.com/swisseph/swephprg.htm",
        "license": "ระบบราศี tropical เป็นสากล; การคำนวณสุริยคติเป็นสูตรดาราศาสตร์สาธารณะ",
        "kind": "standard",
    },
    "ptolemy_marriage": {
        "url": "https://www.gutenberg.org/ebooks/70850",
        "license": "สาธารณสมบัติ (สหรัฐฯ); ใช้เป็นหลักฐานเชิงประวัติศาสตร์เท่านั้น",
        "kind": "primary_text",
    },
}


def source_url(source_id: str) -> str:
    return SOURCES.get(source_id, {}).get("url", "")
