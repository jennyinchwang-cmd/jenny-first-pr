# -*- coding: utf-8 -*-
"""AppTest — หน้าดวงคู่ 4 ศาสตร์ 3 ภาษา (รัน .venv-test/Scripts/python.exe, cwd=number-luck/)"""
import sys
import datetime as dt
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
from streamlit.testing.v1 import AppTest

_APP = str(Path(__file__).resolve().parent.parent / "app.py")


def _find_analyze(at):
    for b in at.button:
        if getattr(b, "key", None) == "cp_go":
            return b
    return None


def _run_couple(lang_idx):
    at = AppTest.from_file(_APP, default_timeout=180)
    at.session_state["page"] = "couple"
    at.run()
    at.radio[0].set_value(at.radio[0].options[lang_idx]).run()
    at.date_input[0].set_value(dt.date(1995, 5, 10)).run()   # พุธ
    at.date_input[1].set_value(dt.date(1996, 6, 15)).run()   # เสาร์
    # พุธ → selectbox ช่วงเกิด (เลือก "am")
    at.selectbox[0].set_value("am").run()
    _find_analyze(at).set_value(True).run()
    assert not at.exception, (lang_idx, at.exception[0].value if at.exception else None)
    return at


TOKENS = {
    "th": ["พม่า", "จีน", "ไทย", "ตะวันตก"],
    "en": ["Burmese", "Chinese", "Thai", "Western"],
    "mm": ["မြန်မာ့", "တရုတ်", "ထိုင်း", "အနောက်တိုင်း"],
}

for i, lang in enumerate(["th", "en", "mm"]):
    at = _run_couple(i)
    subs = [s.value for s in at.subheader]
    md = " ".join(str(m.value) for m in at.markdown)
    assert any("ศาสตร์" in s or "traditions" in s or "ပညာရပ်" in s for s in subs), (lang, subs)
    for token in TOKENS[lang]:
        assert token in md or token in " ".join(subs), (lang, token)
    # ห้ามมีคะแนนรวม % (metric เก่าถูกถอดแล้ว)
    assert "70%" not in md and "Overall compatibility" not in md
    print(lang, "OK —", len(md), "chars rendered")


print("APPTEST_ALL_OK")
