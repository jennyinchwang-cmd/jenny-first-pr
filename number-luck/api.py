# -*- coding: utf-8 -*-
"""
Number Luck API — หลังบ้านสำหรับแอปมือถือ (FastAPI)
=====================================================
รัน:  uvicorn api:app --port 8602
เอกสารอัตโนมัติ:  http://localhost:8602/docs

Endpoints หลัก (ทุกตัวรับ ?lang=th|en|mm):
  GET /analyze?number=09...&birthdate=1995-01-01&name=Aung
  GET /horoscope/weekly?birthdate=...   /horoscope/monthly?birthdate=...
  GET /auspicious-days?days=14
  GET /couple?day1=...&day2=...&number1=...&number2=...
"""
import datetime as dt
from typing import Optional

from fastapi import FastAPI, HTTPException, Query

from scorer import score_number, extract_core
from extra import sum_analysis, myanmar_analysis
from burmese import (compat_breakdown, mahabote_full_chart, mahabote_cross,
                     couple_compatibility, couple_numbers, yadaya_prescription,
                     day_from_name, day_key_from_date, DAYS, GROH_THAK)
from mmcal import auspicious_window
from horoscope import weekly_fortune, monthly_fortune
from i18n import (star_name, pair_title_i18n, pair_desc_i18n, pair_paragraph_i18n,
                  DAYS_TR, grade_label, compat_verdict, FACTOR_NAME, factor_comment,
                  SUM_TONE_TEXT, CAREER_TR, YADAYA_TR, WEEKDAY_TR, ASTRO_VERDICT,
                  HORO_UI, ZODIAC_TR, horo_reason_text, numpair_verdict)
from report import CAREER_BY_DIGIT
from meanings import DIGIT

app = FastAPI(title="Number Luck API", version="1.0",
              description="Myanmar phone number fortune API — พม่า+จีน+อินเดีย 3 ภาษา")

VALID_LANGS = ("th", "en", "mm")


def _lang(lang: str) -> str:
    if lang not in VALID_LANGS:
        raise HTTPException(422, f"lang must be one of {VALID_LANGS}")
    return lang


def _day_name(key: str, lang: str) -> str:
    return DAYS[key]["th"] if lang == "th" else DAYS_TR[lang][key]["name"]


def _parse_date(s: Optional[str]) -> Optional[dt.date]:
    if not s:
        return None
    try:
        return dt.date.fromisoformat(s)
    except ValueError:
        raise HTTPException(422, "birthdate must be YYYY-MM-DD")


@app.get("/health")
def health():
    return {"ok": True, "version": "1.0"}


@app.get("/analyze")
def analyze(number: str, lang: str = "th", birthdate: Optional[str] = None,
            wednesday_pm: bool = False, name: Optional[str] = None):
    """วิเคราะห์เบอร์เต็มรูปแบบ: เกรด คู่เลข คำทำนาย ผลรวม นวิน + ความเข้ากันวันเกิด (ถ้าให้)"""
    lang = _lang(lang)
    core = extract_core(number)
    if not core.isdigit() or not (7 <= len(core) <= 9):
        raise HTTPException(422, "invalid Myanmar number (09 + 7-9 digits)")
    r = score_number(number)
    sm = sum_analysis(r["full"])
    mm_ = myanmar_analysis(r["full"])
    adj = round(min(100.0, max(0.0, r["grade100"] + sm["bonus"] + mm_["bonus"])), 1)

    pairs = [{"pair": p["pair"], "power": p["power"],
              "stars": pair_title_i18n(p["pair"], lang),
              "meaning": pair_desc_i18n(p["pair"], lang)} for p in r["pairs"]]
    # ย่อหน้าคำทำนาย: คู่เด่นสูงสุด 5 คู่ (ไม่ซ้ำ, ไม่นับคู่แรก)
    seen, weighted = set(), []
    for i, p in enumerate(r["pairs"][1:], start=1):
        if p["pair"] not in seen:
            seen.add(p["pair"])
            weighted.append((abs(p["power"] * p["weight"]), p))
    weighted.sort(key=lambda x: -x[0])
    readings = [{"pair": p["pair"], "positive": p["power"] >= 0,
                 "text": pair_paragraph_i18n(p["pair"], p["power"], lang)}
                for _, p in weighted[:5]]

    out = {"number": r["full"], "core": core, "grade": adj,
           "grade_label": grade_label(r["grade"], lang), "premium": adj > 97,
           "pairs": pairs, "readings": readings,
           "sum": {"total": sm["total"], "tone": sm["tone"],
                   "text": sm["text"] if lang == "th" else SUM_TONE_TEXT[lang][sm["tone"]]},
           "nawin": {"nines": r["full"].count("9"), "bonus": mm_["bonus"]}}

    bd = _parse_date(birthdate)
    day_key = None
    if not bd and name:
        day_key, _pref = day_from_name(name)
    if bd or day_key:
        bk = compat_breakdown(core, bd, wednesday_pm, day_key=day_key)
        prof = bk["base"]["profile"]
        out["compatibility"] = {
            "overall": bk["overall"], "verdict": compat_verdict(bk["overall"], lang),
            "birth_day": _day_name(prof["key"], lang),
            "factors": [{"key": f["key"], "name": FACTOR_NAME[lang][f["key"]],
                         "score": f["score"], "weight_pct": f["weight_pct"],
                         "comment": factor_comment(f, lang, star_name)}
                        for f in bk["factors"]],
            "yadaya": (yadaya_prescription(prof["key"]) if lang == "th" else
                       [t.format(dir=DAYS_TR[lang][prof["key"]]["dir"],
                                 day=_day_name(prof["key"], lang),
                                 k=GROH_THAK[prof["key"]],
                                 planet=star_name(str(prof["num"]), lang))
                        for t in YADAYA_TR[lang]]),
        }
        if bd:
            out["compatibility"]["mahabote"] = [
                {"house": c["no"], "name": c["name"], "nature": c["nature"], "planet": c["planet"]}
                for c in mahabote_full_chart(bd)]
    return out


@app.get("/horoscope/weekly")
def horoscope_weekly(lang: str = "th", birthdate: Optional[str] = None,
                     wednesday_pm: bool = False, name: Optional[str] = None):
    lang = _lang(lang)
    bd = _parse_date(birthdate)
    day_key = None
    if not bd:
        if not name:
            raise HTTPException(422, "need birthdate or name")
        day_key, _ = day_from_name(name)
        if not day_key:
            raise HTTPException(422, "cannot infer day from name")
    w = weekly_fortune(bd, wednesday_pm, day_key=day_key)
    return {"overall": w["overall"],
            "zodiac": ZODIAC_TR.get(w["zodiac"], {}).get(lang, w["zodiac"]),
            "lucky_numbers": w["lucky_numbers"],
            "days": [{"date": d["date"].isoformat(), "day": _day_name(d["wd_key"], lang),
                      "icon": d["icon"], "score": d["score"],
                      "level": HORO_UI[lang]["level"][d["level"]],
                      "reasons": [horo_reason_text(r, lang) for r in d["reasons"]]}
                     for d in w["days"]]}


@app.get("/horoscope/monthly")
def horoscope_monthly(lang: str = "th", birthdate: Optional[str] = None,
                      wednesday_pm: bool = False, name: Optional[str] = None):
    lang = _lang(lang)
    bd = _parse_date(birthdate)
    day_key = None
    if not bd:
        if not name:
            raise HTTPException(422, "need birthdate or name")
        day_key, _ = day_from_name(name)
        if not day_key:
            raise HTTPException(422, "cannot infer day from name")
    m = monthly_fortune(bd, wednesday_pm, day_key=day_key)

    def _dates(lst):
        return [d["date"].isoformat() for d in lst]
    return {"overall": m["overall"], "good_days": _dates(m["good"]), "bad_days": _dates(m["bad"]),
            "top3": _dates(m["top3"]), "yatyaza": _dates(m["yatyaza_days"]),
            "pyathada": _dates(m["pyathada_days"]), "chong": _dates(m["chong_days"]),
            "sabbath": _dates(m["sabbath_days"])}


@app.get("/auspicious-days")
def auspicious_days(lang: str = "th", days: int = Query(14, ge=1, le=60)):
    lang = _lang(lang)
    win = auspicious_window(dt.date.today(), days)
    out = []
    for a in win:
        if a["yatyaza"]:
            v = ASTRO_VERDICT[lang]["yat"]
        elif a["pyathada"] == 1:
            v = ASTRO_VERDICT[lang]["pya"]
        elif a["pyathada"] == 2:
            v = ASTRO_VERDICT[lang]["pya2"]
        else:
            v = ASTRO_VERDICT[lang]["norm"]
        out.append({"date": a["date"].isoformat(), "day": WEEKDAY_TR[lang][a["wd"]],
                    "icon": a["icon"], "yatyaza": bool(a["yatyaza"]),
                    "pyathada": a["pyathada"], "verdict": v})
    return {"days": out}


@app.get("/couple")
def couple(lang: str = "th", birthdate1: Optional[str] = None, birthdate2: Optional[str] = None,
           number1: Optional[str] = None, number2: Optional[str] = None):
    lang = _lang(lang)
    out = {}
    if birthdate1 and birthdate2:
        k1 = day_key_from_date(_parse_date(birthdate1))
        k2 = day_key_from_date(_parse_date(birthdate2))
        cc = couple_compatibility(k1, k2)
        out["days"] = {"person1": _day_name(k1, lang), "person2": _day_name(k2, lang),
                       "tone": cc["tone"], "text": cc["text"]}
    if number1 and number2:
        c1, c2 = extract_core(number1), extract_core(number2)
        if all(c.isdigit() and 7 <= len(c) <= 9 for c in (c1, c2)):
            np_ = couple_numbers(c1, c2)
            out["numbers"] = {"score": np_["score"], "verdict": numpair_verdict(np_["score"], lang),
                              "tail": np_["tail"], "top": np_["top"]}
    if not out:
        raise HTTPException(422, "need birthdate1+birthdate2 or number1+number2")
    return out
