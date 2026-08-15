# -*- coding: utf-8 -*-
"""Unit tests — ดวงคู่หลายศาสตร์ (รันด้วย .venv-test/Scripts/python.exe)"""
import sys
import datetime as dt
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.stdout.reconfigure(encoding="utf-8")

from chinese_couple import branch_rules, BRANCH, analyze_chinese
from thai_couple import thaksa_profile, planet_relation, analyze_thai
from western_couple import sun_sign, analyze_western, element_relation, modality_relation
from burmese_couple import analyze_burmese, mahabote_class, nakhat_class, WED_UNKNOWN
from convergence import synthesize


def test_chinese_rules():
    # branch indices: 0子 1丑 2寅 3卯 4辰 5巳 6午 7未 8申 9酉 10戌 11亥
    assert "liuhe" in [h.rule_id for h in branch_rules(0, 1)]          # 子丑
    assert "liuhe" in [h.rule_id for h in branch_rules(2, 11)]         # 寅亥
    assert "liuchong" in [h.rule_id for h in branch_rules(0, 6)]       # 子午
    assert "liuhai" in [h.rule_id for h in branch_rules(0, 7)]         # 子未
    assert "sanhe_2of3" in [h.rule_id for h in branch_rules(8, 4)]     # 申辰 (ขาด子)
    assert "sanxing_zimao" in [h.rule_id for h in branch_rules(0, 3)]  # 子卯
    assert "zixing" in [h.rule_id for h in branch_rules(4, 4)]         # 辰辰
    assert "po" in [h.rule_id for h in branch_rules(0, 9)]             # 子酉
    assert "same_branch" in [h.rule_id for h in branch_rules(2, 2)]
    # 寅亥 เป็นทั้ง 六合 และ 破
    ids = [h.rule_id for h in branch_rules(2, 11)]
    assert "liuhe" in ids and "po" in ids
    # 破 ต้องเป็น experimental
    po = [h for h in branch_rules(0, 9) if h.rule_id == "po"][0]
    assert po.status == "EXPERIMENTAL"


def test_thai_thaksa():
    # ตัวอย่างจาก reference: อาทิตย์(1) → บริวาร=1 อายุ=2 เดช=3 ศรี=4 มูละ=7 อุตสาหะ=5 มนตรี=8 กาลกิณี=6
    t = thaksa_profile(1)
    assert t == {"บริวาร": 1, "อายุ": 2, "เดช": 3, "ศรี": 4, "มูละ": 7, "อุตสาหะ": 5, "มนตรี": 8, "กาลกิณี": 6}
    assert planet_relation(1, 5) == "friend"
    assert planet_relation(1, 3) == "enemy"
    assert planet_relation(2, 8) == "not_listed"   # 2-8 ยังไม่มีหลักฐาน
    assert planet_relation(4, 8) == "enemy"


def test_western_signs():
    assert sun_sign(dt.date(2020, 3, 21))["sign"] == "Aries"
    assert sun_sign(dt.date(2020, 8, 15))["sign"] == "Leo"
    assert sun_sign(dt.date(2020, 12, 25))["sign"] == "Capricorn"
    assert sun_sign(dt.date(2020, 7, 1))["element"] == "water"      # Cancer
    assert element_relation("fire", "air") == "supportive"
    assert element_relation("fire", "water") == "adjust"
    assert element_relation("earth", "earth") == "same_element"


def test_burmese_range():
    for d in [dt.date(1995, 5, 9), dt.date(1980, 1, 1), dt.date(2001, 12, 31), dt.date(2026, 4, 14)]:
        assert 0 <= mahabote_class(d) <= 6
        assert 0 <= nakhat_class(d) <= 2


def test_wed_unknown():
    r = analyze_burmese(dt.date(1995, 5, 9), dt.date(1996, 6, 15), WED_UNKNOWN, "sat")
    assert "wednesday_sector_unknown" in r.limitations
    assert r.detail["a"]["profile"]["unknown"] is True
    t = analyze_thai(WED_UNKNOWN, "sat")
    assert "wednesday_sector_unknown" in t.limitations
    assert t.detail["a"]["num"] is None


def test_synthesis_no_blend():
    res = {
        "burmese": analyze_burmese(dt.date(1995, 5, 9), dt.date(1996, 6, 15), "wed_am", "sat"),
        "chinese": analyze_chinese(dt.date(1996, 5, 1), dt.date(1997, 5, 1)),   # rat+ox 六合
        "thai": analyze_thai("sun", "thu"),                                      # 1-5 มิตร
        "western": analyze_western(dt.date(1995, 8, 15), dt.date(1995, 12, 25)),
    }
    syn = synthesize(res)
    assert "chinese" in {e["tradition"] for e in syn["supportive"]}
    assert "thai" in {e["tradition"] for e in syn["supportive"]}
    assert "burmese" in syn["profile_only"]       # พม่าให้โปรไฟล์อย่างเดียว
    assert "score" not in syn                      # ห้ามมีคะแนนรวม


if __name__ == "__main__":
    for fn in [test_chinese_rules, test_thai_thaksa, test_western_signs,
               test_burmese_range, test_wed_unknown, test_synthesis_no_blend]:
        fn()
        print("OK", fn.__name__)
    print("ALL_TESTS_PASSED")
