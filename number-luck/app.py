# -*- coding: utf-8 -*-
"""
Number Luck — เว็บดูดวงเบอร์โทรศัพท์พม่า (3 ภาษา: ไทย/English/မြန်မာ)
รัน: streamlit run app.py
"""
import datetime as dt
from collections import Counter

import streamlit as st

from scorer import score_number, extract_core
from meanings import DIGIT
from extra import sum_analysis, myanmar_analysis
from burmese import (number_compatibility, mahabote_full_chart, mahabote_cross, DAYS,
                     day_from_name, couple_compatibility, yadaya_prescription,
                     day_key_from_date, relation, COUPLE_CLASH, GROH_THAK, couple_numbers,
                     compat_breakdown)
from mmcal import auspicious_window
from report import CAREER_BY_DIGIT
import i18n
from i18n import (UI, LANGS, star_name, pair_title_i18n, pair_desc_i18n, pair_paragraph_i18n,
                  DAYS_TR, HOUSES_TR, grade_label, compat_verdict, digit_trait,
                  SUM_TONE_TEXT, NAWIN_TEXT, CAREER_TR, YADAYA_TR, WEEKDAY_TR, MONTH_TR,
                  ASTRO_VERDICT, COUPLE_TONE, COUPLE_TEXT, MB_CROSS, DIGIT_TR,
                  NUMPAIR_UI, NUMPAIR_REL, numpair_verdict,
                  BREAKDOWN_UI, FACTOR_NAME, factor_comment,
                  HORO_UI, HORO_REASON, ZODIAC_TR, horo_reason_text)
from horoscope import weekly_fortune, monthly_fortune
from meanings import DIGIT_LONG
from cheiro import CHEIRO_UI, cheiro_compound, mulank_compat

st.set_page_config(page_title="Number Luck", page_icon="🔮", layout="centered")

# ธีม "ราตรีส้มทอง" — token/แนวทางอยู่ที่ design/DESIGN.md
from pathlib import Path
_css = Path(__file__).parent / "design" / "streamlit_theme.css"
st.markdown(f"<style>{_css.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

# ---------- Language selector ----------
lang = st.radio("ภาษา / Language / ဘာသာ", options=list(LANGS.keys()),
                format_func=lambda k: LANGS[k], horizontal=True, index=0)
T = UI[lang]


def day_name(key: str) -> str:
    return DAYS[key]["th"] if lang == "th" else DAYS_TR[lang][key]["name"]


def day_animal(key: str) -> str:
    return DAYS[key]["animal"] if lang == "th" else DAYS_TR[lang][key]["animal"]


def day_dir(key: str) -> str:
    return DAYS[key]["dir"] if lang == "th" else DAYS_TR[lang][key]["dir"]


def day_trait(key: str) -> str:
    return DAYS[key]["trait"] if lang == "th" else DAYS_TR[lang][key]["trait"]


def house_name(idx: int) -> str:
    from burmese import MB_HOUSES
    return MB_HOUSES[idx][0] if lang == "th" else HOUSES_TR[lang][idx][0]


def house_nature(idx: int) -> str:
    from burmese import MB_HOUSES
    nat = MB_HOUSES[idx][1]
    if lang == "th":
        return nat
    return T["nature_pos"] if nat == "บวก" else T["nature_neg"]


def house_desc(idx: int) -> str:
    from burmese import MB_HOUSES
    return MB_HOUSES[idx][2] if lang == "th" else HOUSES_TR[lang][idx][2]


import os as _os
_ASSET_DIR = _os.path.join(_os.path.dirname(__file__), "assets")
_DAY_IMG = {"sun": "day_sun_garuda.png", "mon": "day_mon_tiger.png", "tue": "day_tue_lion.png",
            "wed_am": "day_wed_elephant.png", "wed_pm": "day_rahu_elephant.png",
            "thu": "day_thu_rat.png", "fri": "day_fri_guineapig.png", "sat": "day_sat_naga.png"}


def _asset(name):
    p = _os.path.join(_ASSET_DIR, name)
    return p if _os.path.exists(p) else None


_hero = _asset("hero_banner.png")
if _hero:
    st.image(_hero, use_container_width=True)
st.markdown(f"""
<div class="nl-eyebrow">✦&ensp;Myanmar Number Astrology&ensp;✦</div>
<div class="nl-title">🔮 Number <span class="hl">Luck</span></div>
<p class="nl-lede">{T["tagline"]}</p>
""", unsafe_allow_html=True)

# ---------- เมนูหน้าแรก: เลือกก่อนว่าอยากดูดวงเรื่องไหน ----------
from muhurta import (ACTIVITIES, rank_days, today_fortune, REASON_TR,
                     UI as MUI, DIRECTION_TR, SHENGXIAO_TR)
from mmcal import astro_day as _astro_day

MENU = {
    "number": {"img": "menu_number.png",
               "th": "ดูดวงเบอร์โทร", "en": "Phone Number Reading", "mm": "ဖုန်းနံပါတ် ဗေဒင်",
               "sub": {"th": "เกรดเบอร์ · คู่เลข · คำทำนายครบทุกศาสตร์",
                       "en": "Grade, number pairs & full reading",
                       "mm": "အဆင့် · ဂဏန်းအတွဲ · ဟောစာတမ်းအပြည့်အစုံ"}},
    "muhurta": {"img": "menu_muhurta.png",
                "th": "หาฤกษ์มงคล", "en": "Auspicious Dates", "mm": "မင်္ဂလာရက် ရွေးရန်",
                "sub": {"th": "เปิดร้าน แต่งงาน ย้ายบ้าน — จีน+พม่า 30 วัน",
                        "en": "Business, wedding, moving — CN+MM, 30 days",
                        "mm": "ဆိုင်ဖွင့် · လက်ထပ် · အိမ်ပြောင်း — တရုတ်+မြန်မာ ရက် ၃၀"}},
    "today": {"img": "menu_today.png",
              "th": "ดวงวันนี้", "en": "Today's Fortune", "mm": "ယနေ့ ဗေဒင်",
              "sub": {"th": "วันนี้ชงไหม · ทิศรับทรัพย์ · ชั่วโมงมงคล",
                      "en": "Zodiac clash · wealth direction · lucky hours",
                      "mm": "ထိပ်တိုက်ရက် · ဥစ္စာလာရာအရပ် · မင်္ဂလာအချိန်"}},
    "couple": {"img": "menu_couple.png",
               "th": "ดวงคู่", "en": "Couple Compatibility", "mm": "စုံတွဲ လိုက်ဖက်မှု",
               "sub": {"th": "เบอร์คู่รัก · วันเกิดคู่เวรคู่มิตร",
                       "en": "Number pair & birthday match",
                       "mm": "ဖုန်းနံပါတ်တွဲ · မွေးနေ့ မိတ်/ရန်"}},
}
_BACK = {"th": "⬅️ กลับหน้าแรก", "en": "⬅️ Home", "mm": "⬅️ ပင်မစာမျက်နှာ"}

if "page" not in st.session_state:
    st.session_state.page = "home"


def _goto(p):
    st.session_state.page = p


page = st.session_state.page

if page != "home":
    st.button(_BACK[lang], on_click=_goto, args=("home",))

# ============ หน้าแรก: ไอคอนเมนู ============
if page == "home":
    cols = st.columns(2)
    for i, (key, m) in enumerate(MENU.items()):
        with cols[i % 2]:
            img = _asset(m["img"])
            if img:
                st.image(img, use_container_width=True)
            st.button(m[lang], key=f"menu_{key}", use_container_width=True,
                      type="primary", on_click=_goto, args=(key,))
            st.caption(m["sub"][lang])
    st.markdown("""
<div class="nl-foot">
  <div class="stars">✦ ✦ ✦</div>
  <a class="nl-pill" href="https://ft.jbacworkhub.com">🌐 ft.jbacworkhub.com</a>
</div>
""", unsafe_allow_html=True)
    st.stop()

# ============ หน้าหาฤกษ์มงคล ============
if page == "muhurta":
    M = MUI[lang]
    st.subheader({"th": "📅 หาฤกษ์มงคลทำกิจการ (จีน 通勝 + พม่า)",
                  "en": "📅 Find an Auspicious Date (Chinese almanac + Burmese)",
                  "mm": "📅 မင်္ဂလာရက် ရွေးခြင်း (တရုတ် + မြန်မာ)"}[lang])
    act = st.selectbox({"th": "อยากทำอะไร", "en": "What are you planning?", "mm": "ဘာလုပ်ချင်ပါသလဲ"}[lang],
                       options=list(ACTIVITIES),
                       format_func=lambda k: ACTIVITIES[k]["icon"] + " " + ACTIVITIES[k][lang])
    use_bd_m = st.checkbox(T["bd_check"], value=True, key="mu_ubd")
    bd_m = st.date_input(T["bd_label"], value=dt.date(1995, 1, 1),
                         min_value=dt.date(1930, 1, 1), max_value=dt.date.today(), key="mu_bd")
    wed_pm_m = st.checkbox(T["wed_pm"], value=False, key="mu_wp") if bd_m.weekday() == 2 else False
    if st.button({"th": "🔍 หาฤกษ์ 30 วันข้างหน้า", "en": "🔍 Rank the next 30 days",
                  "mm": "🔍 နောက် ရက် ၃၀ ရှာရန်"}[lang], type="primary", use_container_width=True):
        with st.spinner("..."):
            res = rank_days(act, dt.date.today(), 30, bd_m if use_bd_m else None, wed_pm_m)
        lvl_txt = {"best": "🟢 " + M["best"], "good": "🟢 " + M["good"],
                   "ok": "⚪ " + M["ok"], "avoid": "🔴 " + M["avoid"]}
        b = res[0]
        why_b = " · ".join(REASON_TR[k][lang] for k, v in b["reasons"] if v > 0) or "—"
        st.success(f"**{M['best']}: {b['date'].strftime('%d/%m/%Y')} "
                   f"({WEEKDAY_TR[lang][_astro_day(b['date'])['wd']]})** — {why_b}")
        rows = []
        for x in res[:10]:
            why = " · ".join(REASON_TR[k][lang] for k, _v in x["reasons"][:3]) or "—"
            rows.append({T["col_date"]: x["date"].strftime("%d/%m"),
                         T["col_day"]: WEEKDAY_TR[lang][_astro_day(x["date"])["wd"]],
                         "": lvl_txt[x["level"]],
                         M["cn_score"]: f"{x['cn']:+d}", M["mm_score"]: f"{x['mm']:+d}",
                         T["col_why"] if "col_why" in T else "✧": why})
        st.dataframe(rows, use_container_width=True, hide_index=True)
        avoid = [x for x in res if x["excluded"]][:5]
        if avoid:
            st.warning("🚫 " + M["avoid"] + ": " +
                       ", ".join(sorted(x["date"].strftime("%d/%m") for x in avoid)))
        st.caption({"th": "อิงปฏิทินจีนสาย 6tail (通勝) + ปฏิทินโหราศาสตร์พม่า — ความเชื่อวัฒนธรรม โปรดใช้วิจารณญาณ",
                    "en": "Based on the 6tail Chinese almanac + Burmese astrological calendar — cultural belief, use judgment",
                    "mm": "6tail တရုတ်ပြက္ခဒိန် + မြန်မာဗေဒင်ပြက္ခဒိန် အခြေခံ — ယုံကြည်မှုအရသာ"}[lang])
    st.stop()

# ============ หน้าดวงวันนี้ ============
if page == "today":
    M = MUI[lang]
    st.subheader({"th": "☀️ ดวงวันนี้ของคุณ", "en": "☀️ Your Fortune Today",
                  "mm": "☀️ ယနေ့ သင့်ကံကြမ္မာ"}[lang])
    use_bd_t = st.checkbox(T["bd_check"], value=True, key="td_ubd")
    bd_t = st.date_input(T["bd_label"], value=dt.date(1995, 1, 1),
                         min_value=dt.date(1930, 1, 1), max_value=dt.date.today(), key="td_bd")
    wed_pm_t = st.checkbox(T["wed_pm"], value=False, key="td_wp") if bd_t.weekday() == 2 else False
    tf = today_fortune(dt.date.today(), bd_t if use_bd_t else None, wed_pm_t)
    c1, c2, c3 = st.columns(3)
    c1.metric({"th": "วันที่", "en": "Date", "mm": "နေ့စွဲ"}[lang], tf["date"].strftime("%d/%m/%Y"))
    cai = DIRECTION_TR.get(tf["cai_direction"], {}).get(lang, tf["cai_direction"])
    c2.metric(M["cai_dir"], cai)
    c3.metric({"th": "คะแนนวันนี้", "en": "Day score", "mm": "ယနေ့အမှတ်"}[lang], f"{tf['score']:+d}")
    if tf["zodiac"]:
        z = SHENGXIAO_TR.get(tf["zodiac"], {}).get(lang, tf["zodiac"])
        if tf["chong_today"]:
            st.warning(M["chong_you"].format(z=z))
        else:
            st.success(M["no_chong"].format(z=z))
    if tf["yatyaza"]:
        st.success("⭐ " + REASON_TR["yatyaza"][lang])
    if tf["pyathada"] == 1:
        st.warning("⚠️ " + REASON_TR["pyathada"][lang])
    elif tf["pyathada"] == 2:
        st.info(REASON_TR["pyathada_pm"][lang])
    if tf["sabbath"]:
        st.info("🙏 " + REASON_TR["sabbath"][lang])
    st.markdown(f"**{M['lucky_hours']}** — " +
                (" · ".join(h["span"] for h in tf["hours"]) or "—"))
    st.caption(M["hour_note"])
    with st.expander({"th": "เหตุผลของคะแนนวันนี้", "en": "Why this score?",
                      "mm": "အမှတ်အကြောင်းရင်း"}[lang]):
        for k, v in tf["reasons"]:
            icon = "🟢" if v > 0 else ("🔴" if v < 0 else "⚪")
            st.write(f"{icon} {REASON_TR[k][lang]} ({v:+d})")
    st.stop()

# ============ หน้าดวงคู่ ============
if page == "couple":
    st.subheader(NUMPAIR_UI[lang]["head"])
    cn1 = st.text_input(T["phone_label"] + " ①", placeholder="09XXXXXXXXX", key="cp_n1")
    cn2 = st.text_input(NUMPAIR_UI[lang]["num2_label"] + " ②", placeholder="09XXXXXXXXX", key="cp_n2")
    use_bd_c = st.checkbox(T["couple_check"], value=False, key="cp_ubd")
    cbd1 = st.date_input(T["bd_label"] + " ①", value=dt.date(1995, 1, 1),
                         min_value=dt.date(1930, 1, 1), max_value=dt.date.today(), key="cp_b1")
    cbd2 = st.date_input(T["bd2_label"] + " ②", value=dt.date(1996, 6, 15),
                         min_value=dt.date(1930, 1, 1), max_value=dt.date.today(), key="cp_b2")
    if st.button(T["analyze"], type="primary", use_container_width=True, key="cp_go"):
        c1_, c2_ = extract_core(cn1), extract_core(cn2)
        ok = all(c.isdigit() and 7 <= len(c) <= 9 for c in (c1_, c2_))
        if not ok and not use_bd_c:
            st.error(T["bad_number"])
        if ok:
            np_ = couple_numbers(c1_, c2_)
            st.metric(NUMPAIR_UI[lang]["score"], f"{np_['score']}/100")
            v = numpair_verdict(np_["score"], lang)
            (st.success if np_["score"] >= 55 else (st.info if np_["score"] >= 40 else st.warning))(v)
            st.write("• " + NUMPAIR_UI[lang]["tail_line"].format(a=np_["tail"]["a"], b=np_["tail"]["b"])
                     + " — " + NUMPAIR_REL[lang][np_["tail"]["rel"]])
            st.write("• " + NUMPAIR_UI[lang]["top_line"].format(
                a=np_["top"]["a"], sa=star_name(str(np_["top"]["a"]), lang),
                b=np_["top"]["b"], sb=star_name(str(np_["top"]["b"]), lang))
                + " — " + NUMPAIR_REL[lang][np_["top"]["rel"]])
        if use_bd_c:
            k1 = day_key_from_date(cbd1)
            k2 = day_key_from_date(cbd2)
            cc = couple_compatibility(k1, k2)
            st.markdown(f"{T['person1']}: **{day_name(k1)}** ({day_animal(k1)}) × "
                        f"{T['person2']}: **{day_name(k2)}** ({day_animal(k2)})")
            if lang == "th":
                tone_txt, body = cc["tone"], cc["text"]
            else:
                tone_txt = COUPLE_TONE[lang][cc["tone"]]
                p1, p2 = star_name(str(DAYS[k1]["num"]), lang), star_name(str(DAYS[k2]["num"]), lang)
                if frozenset((k1, k2)) in COUPLE_CLASH:
                    body = COUPLE_TEXT[lang]["clash"]
                else:
                    rel = relation(DAYS[k1]["num"], DAYS[k2]["num"])
                    body = COUPLE_TEXT[lang][rel].format(p1=p1, p2=p2, d=day_name(k1))
            if cc["tone"] in ("ดีมาก", "ดี"):
                st.success(f"{tone_txt} — {body}")
            elif cc["tone"] == "กลาง":
                st.info(f"{tone_txt} — {body}")
            else:
                st.warning(f"{tone_txt} — {body}")
                st.caption(T["couple_note"])
    st.stop()

# ============ หน้าดูดวงเบอร์ (โค้ดเดิมด้านล่าง) ============

# ---------- Inputs ----------
number = st.text_input(T["phone_label"], placeholder="09XXXXXXXXX")

with st.expander(T["bd_expander"]):
    use_bd = st.checkbox(T["bd_check"], value=False)
    bd = st.date_input(T["bd_label"], value=dt.date(1995, 1, 1),
                       min_value=dt.date(1930, 1, 1), max_value=dt.date.today())
    wed_pm = False
    if bd.weekday() == 2:
        wed_pm = st.checkbox(T["wed_pm"], value=False)
    owner_name = st.text_input(T["name_label"], placeholder="Aung Aung")

with st.expander(T["couple_expander"]):
    use_couple = st.checkbox(T["couple_check"], value=False)
    number2 = st.text_input(NUMPAIR_UI[lang]["num2_label"], placeholder="09XXXXXXXXX", key="num2")
    bd2 = st.date_input(T["bd2_label"], value=dt.date(1996, 6, 15),
                        min_value=dt.date(1930, 1, 1), max_value=dt.date.today(), key="bd2")
    wed_pm2 = False
    if bd2.weekday() == 2:
        wed_pm2 = st.checkbox(T["wed_pm2"], value=False, key="wp2")

go = st.button(T["analyze"], type="primary", use_container_width=True)

# ---------- หน้ารอผล: กงล้อราศีพม่าหมุน ----------
import base64 as _b64
import time as _time

_LOADING_TXT = {
    "th": ("คำทำนายกำลังจะมา...", "กงล้อราศีพม่ากำลังคำนวณดวงเบอร์ของคุณ"),
    "en": ("Your prophecy is coming...", "The Burmese zodiac wheel is reading your number"),
    "mm": ("ဗေဒင်ဟောစာ လာနေပါပြီ...", "မြန်မာ့ရာသီစက်ဝန်းက သင့်နံပါတ်ကို တွက်ချက်နေသည်"),
}


def _show_loading(placeholder, lang):
    wheel = _asset("loading_wheel.webp")
    if not wheel:
        return
    b64 = _b64.b64encode(open(wheel, "rb").read()).decode()
    head, sub = _LOADING_TXT[lang]
    placeholder.markdown(f"""
<style>
@keyframes nl-spin {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}
@keyframes nl-pulse {{ 0%,100% {{ opacity: .55; }} 50% {{ opacity: 1; }} }}
@keyframes nl-glow {{ 0%,100% {{ filter: drop-shadow(0 0 18px rgba(255,150,50,.35)); }}
                      50% {{ filter: drop-shadow(0 0 42px rgba(255,170,60,.75)); }} }}
.nl-loadwrap {{ position: fixed; inset: 0; z-index: 999999;
  background: radial-gradient(ellipse at center, #101b30 0%, #0a1220 65%, #060b16 100%);
  display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 26px; }}
.nl-wheel {{ width: min(58vw, 340px); height: auto; border-radius: 50%;
  animation: nl-spin 7s linear infinite, nl-glow 2.6s ease-in-out infinite; }}
.nl-loadhead {{ font-size: 1.35rem; font-weight: 700; color: #ffb45e; letter-spacing: .04em;
  animation: nl-pulse 1.8s ease-in-out infinite; text-align: center; padding: 0 18px; }}
.nl-loadsub {{ font-size: .9rem; color: #8fa3c4; text-align: center; padding: 0 24px;
  animation: nl-pulse 2.4s ease-in-out infinite; }}
.nl-stars {{ color: #ffcf87; letter-spacing: 14px; animation: nl-pulse 2s ease-in-out infinite; }}
</style>
<div class="nl-loadwrap">
  <img class="nl-wheel" src="data:image/webp;base64,{b64}" alt="">
  <div class="nl-loadhead">🔮 {head}</div>
  <div class="nl-loadsub">{sub}</div>
  <div class="nl-stars">✦ ✦ ✦</div>
</div>
""", unsafe_allow_html=True)

if go and number:
    core = extract_core(number)
    if not core.isdigit() or not (7 <= len(core) <= 9):
        st.error(T["bad_number"])
        st.stop()

    # หน้ารอผลเต็มจอ: กงล้อหมุน + ข้อความ "คำทำนายกำลังจะมา"
    _overlay = st.empty()
    _show_loading(_overlay, lang)
    _time.sleep(4.2)

    r = score_number(number)
    sm = sum_analysis(r["full"])
    mm = myanmar_analysis(r["full"])
    adj = round(min(100.0, max(0.0, r["grade100"] + sm["bonus"] + mm["bonus"])), 1)
    _overlay.empty()  # ปิดหน้ารอผล แล้วโชว์คำทำนาย

    # ---------- Header ----------
    st.divider()
    st.markdown(f"""
<div class="nl-result">
  <div class="num">{r["full"]}</div>
  <div class="grade">{grade_label(r["grade"], lang)} · {adj}/100</div>
</div>
""", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric(T["grade_net"], f"{adj}/100")
    c2.metric(T["grade_level"], grade_label(r["grade"], lang))
    c3.metric(T["bonus"], f"{sm['bonus'] + mm['bonus']:+.1f}")
    if adj > 97:
        st.success(T["premium"])
    st.progress(min(1.0, adj / 100))

    # ---------- Pair structure ----------
    st.subheader(T["pairs_head"])
    rows = []
    for i, p in enumerate(r["pairs"]):
        note = T["tail_note"] if i == 7 else (T["head_note"] if i == 0 else "")
        rows.append({T["col_pair"]: p["pair"], T["col_star"]: pair_title_i18n(p["pair"], lang),
                     T["col_power"]: p["power"], T["col_meaning"]: pair_desc_i18n(p["pair"], lang),
                     T["col_note"]: note})
    st.dataframe(rows, use_container_width=True, hide_index=True)

    # ---------- Weighted fortune paragraphs ----------
    st.subheader(T["fortune_head"])
    weighted, seen = [], set()
    for i, p in enumerate(r["pairs"]):
        if i == 0:
            continue
        contrib = p["power"] * p["weight"]
        if p["pair"] not in seen:
            seen.add(p["pair"])
            weighted.append((abs(contrib), contrib, p, i))
    weighted.sort(key=lambda x: -x[0])
    top = weighted[:5]
    mags = [max(w[0], 0.5) for w in top]
    total = sum(mags)
    pct = [round(m_ / total * 20) * 5 for m_ in mags]
    pct[0] += 100 - sum(pct)
    for (mag, contrib, p, i), w in zip(top, pct):
        tone = T["strength"] if contrib >= 0 else T["caution"]
        with st.expander(f"{tone} — {T['pair_word']} {p['pair']} ({T['weight']} {w}%)", expanded=(w == max(pct))):
            st.write(pair_paragraph_i18n(p["pair"], p["power"], lang))

    # ---------- Sum + Nawin ----------
    st.subheader(T["sum_head"])
    colA, colB = st.columns(2)
    with colA:
        icon = {"ดี": "🟢", "ระวัง": "🔴", "กลาง": "⚪"}[sm["tone"]]
        st.markdown(f"**{T['sum_all']} = {sm['total']}** {icon}")
        st.write(sm["text"] if lang == "th" else SUM_TONE_TEXT[lang][sm["tone"]])
        root_trait = sm["root_text"] if lang == "th" else DIGIT_TR[lang][str(sm["root"])]["trait"]
        st.caption(f"{T['sum_root']}: {sm['root']} ({star_name(str(sm['root']), lang)}) — {root_trait}")
    with colB:
        st.markdown(f"**{T['nawin_head']}**")
        if lang == "th":
            for n in mm["notes"]:
                st.write("★ " + n)
        else:
            digits = r["full"]
            nines = digits.count("9")
            tot = sum(int(c) for c in digits)
            notes = []
            if nines >= 4:
                notes.append(NAWIN_TEXT[lang]["n4"].format(n=nines))
            elif nines >= 2:
                notes.append(NAWIN_TEXT[lang]["n2"].format(n=nines))
            if "999" in digits:
                notes.append(NAWIN_TEXT[lang]["999"])
            if tot % 9 == 0:
                notes.append(NAWIN_TEXT[lang]["div9"].format(t=tot))
            if "37" in digits:
                notes.append(NAWIN_TEXT[lang]["37"])
            if not notes:
                notes.append(NAWIN_TEXT[lang]["none"])
            for n in notes:
                st.write("★ " + n)

    # ---------- ชั้น 4: เลขผสมสากล Cheiro ----------
    CU = CHEIRO_UI[lang]
    ch = cheiro_compound(sm["total"])
    st.subheader(CU["head"])
    if ch["compound"]:
        ch_icon = {"ดี": "🟢", "ระวัง": "🔴", "กลาง": "⚪"}[ch["tone"]]
        st.markdown(f"**{CU['compound']}: {sm['total']} → {ch['compound']} — "
                    f"\u201c{ch['name'][lang]}\u201d** {ch_icon} ({CU['tone'][ch['tone']]})")
        st.write(ch["text"][lang])
    else:
        st.write(CU["single"])
    st.caption(CU["note"])

    # ---------- Birthday compatibility ----------
    name_day, name_pref = day_from_name(owner_name) if owner_name else (None, None)
    if use_bd or name_day:
        st.subheader(T["bd_head"])
        if use_bd:
            bk = compat_breakdown(core, bd, wed_pm)
            comp = bk["base"]
            if name_day:
                actual = day_key_from_date(bd, wed_pm)
                if name_day == actual:
                    st.success(T["name_match"].format(name=owner_name, pref=name_pref, day=day_name(actual)))
                else:
                    st.info(T["name_mismatch"].format(name=owner_name, pref=name_pref,
                                                      nday=day_name(name_day), aday=day_name(actual)))
        else:
            st.caption(T["name_guess"].format(name=owner_name, pref=name_pref))
            bk = compat_breakdown(core, day_key=name_day)
            comp = bk["base"]
        prof = comp["profile"]
        k = prof["key"]
        img = _asset(_DAY_IMG.get(k, ""))
        if img:
            col_img, col_txt = st.columns([1, 3])
            with col_img:
                st.image(img, use_container_width=True)
            with col_txt:
                st.markdown(f"{T['born_on']}**{day_name(k)}** — {T['planet']}**{star_name(str(prof['num']), lang)}** "
                            f"| {T['day_num']} **{prof['num']}**")
                st.markdown(f"{T['direction']}: {day_dir(k)} | {T['animal']}: {day_animal(k)}")
                st.caption(f"{T['bd_trait']}: {day_trait(k)}")
        else:
            st.markdown(f"{T['born_on']}**{day_name(k)}** — {T['planet']}**{star_name(str(prof['num']), lang)}** "
                        f"| {T['day_num']} **{prof['num']}** | {T['direction']}: {day_dir(k)} | {T['animal']}: {day_animal(k)}")
            st.caption(f"{T['bd_trait']}: {day_trait(k)}")
        if prof.get("mb_house"):
            h = prof["mb_house"]
            hi = h["no"] - 1
            st.caption(T["mb_line"].format(planet=star_name(str(prof['num']), lang), no=h["no"],
                                           house=house_name(hi), nature=house_nature(hi), desc=house_desc(hi)))
        st.metric(T["compat_score"], f"{bk['overall']}%")
        verdict = compat_verdict(bk["overall"], lang)
        if bk["overall"] >= 55:
            st.success(verdict)
        elif bk["overall"] >= 40:
            st.info(verdict)
        else:
            st.warning(verdict)
        rel_icons = {"มิตร": "🟢", "เสริม": "🟢", "นวิน": "⭐", "กลาง": "⚪", "ศัตรู": "🔴", "สูญ": "⚫"}
        chips = " ".join(f"{rel_icons[d['relation']]}{d['digit']}" for d in comp["detail"])
        st.caption(f"{T['digit_by_digit']}: {chips}  |  {T['legend']}")

        # ---------- บทสรุปความเข้ากันแบบละเอียด 5 ปัจจัย ----------
        B = BREAKDOWN_UI[lang]
        with st.expander(B["head"] + f" — {bk['overall']}%", expanded=True):
            src_label = {"digits": B["src_mm"], "tail": B["src_mm"], "nawin": B["src_mm"],
                         "sum": B["src_in"], "mahabote": B["src_mm"]}
            for f in bk["factors"]:
                icon = "🟢" if f["score"] >= 70 else ("🟡" if f["score"] >= 45 else "🔴")
                st.markdown(f"{icon} **{FACTOR_NAME[lang][f['key']]}** · "
                            f"{f['score']:.0f}/100 ({B['weight']} {f['weight_pct']}%) · _{src_label[f['key']]}_")
                st.progress(min(1.0, f["score"] / 100))
                st.caption(factor_comment(f, lang, star_name))
            best = max(bk["factors"], key=lambda x: x["score"])
            worst = min(bk["factors"], key=lambda x: x["score"])
            st.success(f"**{B['verdict_top']}:** {FACTOR_NAME[lang][best['key']]} ({best['score']:.0f}/100) — "
                       + factor_comment(best, lang, star_name))
            if worst["score"] < 55:
                st.warning(f"**{B['verdict_low']}:** {FACTOR_NAME[lang][worst['key']]} ({worst['score']:.0f}/100) — "
                           + factor_comment(worst, lang, star_name))

        # ---------- ชั้น 4: ความเข้ากันแบบอินเดีย (Mulank) ----------
        if use_bd:
            mk = mulank_compat(bd.day, sm["total"])
            with st.expander(CU["mulank_head"], expanded=False):
                st.markdown(CU["mulank_line"].format(
                    d=bd.day, m=mk["mulank"], pm=mk["mulank_planet"][lang],
                    r=mk["root"], pr=mk["root_planet"][lang]))
                if mk["score"] >= 1:
                    st.success(mk["verdict"][lang])
                elif mk["score"] == 0:
                    st.info(mk["verdict"][lang])
                else:
                    st.warning(mk["verdict"][lang])
                st.caption(CU["note"])

        # ---------- Mahabote full chart (ต้องมีปีเกิด) ----------
        if use_bd:
            with st.expander(T["mahabote_head"], expanded=True):
                chart = mahabote_full_chart(bd)
                _PLANET_NUM = {"อาทิตย์": 1, "จันทร์": 2, "อังคาร": 3, "พุธ": 4,
                               "พฤหัส": 5, "ศุกร์": 6, "เสาร์": 7}
                chart_rows = []
                for c in chart:
                    idx = c["no"] - 1
                    nat_icon = "🟢 " if c["nature"] == "บวก" else "🟠 "
                    chart_rows.append({T["col_house"]: c["no"], T["col_house_name"]: house_name(idx),
                                       T["col_nature"]: nat_icon + house_nature(idx),
                                       T["col_sit"]: star_name(str(_PLANET_NUM[c["planet"]]), lang)})
                st.dataframe(chart_rows, use_container_width=True, hide_index=True)
                cross = mahabote_cross(core, bd)
                for h in cross["hits"]:
                    hi = h["house_no"] - 1
                    if lang == "th":
                        msg = h["msg"]
                    else:
                        key = "pos" if h["nature"] == "บวก" else "neg"
                        msg = MB_CROSS[lang][key].format(d=h["digit"], planet=star_name(str(h["digit"]), lang),
                                                         n=h["count"], no=h["house_no"],
                                                         house=house_name(hi), desc=house_desc(hi))
                    (st.success if h["nature"] == "บวก" else st.warning)(msg)
                cnt0 = Counter(int(c) for c in core if c != "0")
                for d in (8, 9):
                    if d in [x for x, _ in cnt0.most_common(3)]:
                        if lang == "th":
                            continue  # โน้ตไทยแสดงใน cross["notes"] แล้ว
                        st.info(MB_CROSS[lang][f"r{d}"].format(n=cnt0[d]))
                if lang == "th":
                    for n in cross["notes"]:
                        st.info(n)

        # ---------- Yadaya ----------
        with st.expander(T["yadaya_head"], expanded=(comp["score"] < 55)):
            st.caption(T["yadaya_cap"])
            if lang == "th":
                for line in yadaya_prescription(k):
                    st.write("• " + line)
            else:
                kk = GROH_THAK[k]
                for tpl in YADAYA_TR[lang]:
                    st.write("• " + tpl.format(dir=day_dir(k), day=day_name(k), k=kk,
                                               planet=star_name(str(prof["num"]), lang)))

        # ---------- Weekly / Monthly horoscope ----------
        H = HORO_UI[lang]
        st.subheader(H["head"])
        if use_bd:
            wk = weekly_fortune(bd, wed_pm)
            mo = monthly_fortune(bd, wed_pm)
        else:
            wk = weekly_fortune(day_key=name_day)
            mo = monthly_fortune(day_key=name_day)
        tab_w, tab_m = st.tabs([H["week_tab"], H["month_tab"]])
        with tab_w:
            c1, c2, c3 = st.columns(3)
            c1.metric(H["overall_week"], f"{wk['overall']:.0f}%")
            if wk["zodiac"]:
                c2.metric(H["your_zodiac"], ZODIAC_TR.get(wk["zodiac"], {}).get(lang, wk["zodiac"]))
            c3.metric(H["lucky_nums"], " ".join(str(n) for n in wk["lucky_numbers"]))
            rows = []
            for d in wk["days"]:
                why = " · ".join(horo_reason_text(r, lang) for r in d["reasons"]) or "—"
                rows.append({"": d["icon"], H["col_date"]: d["date"].strftime("%d/%m"),
                             H["col_day"]: day_name(d["wd_key"]),
                             H["col_level"]: H["level"][d["level"]], H["col_why"]: why})
            st.dataframe(rows, use_container_width=True, hide_index=True)
            b, w_ = wk["best"], wk["worst"]
            st.success(f"**{H['best_day']}:** {b['date'].strftime('%d/%m')} ({day_name(b['wd_key'])}) — "
                       + (" · ".join(horo_reason_text(r, lang) for r in b["reasons"]) or "—"))
            if w_["score"] < 0:
                st.warning(f"**{H['caution_day']}:** {w_['date'].strftime('%d/%m')} ({day_name(w_['wd_key'])}) — "
                           + " · ".join(horo_reason_text(r, lang) for r in w_["reasons"]))
            # จุดเด่นรายด้านจากดาวของวันดีที่สุด
            pn = str(b["day_planet_num"])
            asp_src = DIGIT_LONG if lang == "th" else DIGIT_TR[lang]
            st.markdown(f"**{H['aspects_head']}** — {star_name(pn, lang)}")
            for asp_key, asp_label in [("money", H["asp_money"]), ("work", H["asp_work"]),
                                       ("love", H["asp_love"]), ("health", H["asp_health"])]:
                st.write(f"{asp_label}: {asp_src[pn][asp_key]}")
        with tab_m:
            c1, c2, c3 = st.columns(3)
            c1.metric(H["overall_month"], f"{mo['overall']:.0f}%")
            c2.metric(H["good_days"], len(mo["good"]))
            c3.metric(H["bad_days"], len(mo["bad"]))
            st.markdown(f"**{H['top3']}:** " + " · ".join(
                f"{d['date'].strftime('%d/%m')} ({day_name(d['wd_key'])})" for d in mo["top3"]))
            st.markdown(f"🟢 **{H['yat_days']}:** " + ", ".join(d["date"].strftime("%d/%m") for d in mo["yatyaza_days"]))
            st.markdown(f"🔴 **{H['pya_days']}:** " + ", ".join(d["date"].strftime("%d/%m") for d in mo["pyathada_days"]))
            if mo["chong_days"]:
                st.markdown(f"⚡ **{H['chong_days']}:** " + ", ".join(d["date"].strftime("%d/%m") for d in mo["chong_days"]))
            st.markdown(f"🙏 **{H['sab_days']}:** " + ", ".join(d["date"].strftime("%d/%m") for d in mo["sabbath_days"]))

    # ---------- Couple ----------
    core2 = extract_core(number2) if (use_couple and number2) else ""
    has_num2 = core2.isdigit() and (7 <= len(core2) <= 9)
    if use_couple and has_num2:
        st.subheader(NUMPAIR_UI[lang]["head"])
        np_ = couple_numbers(core, core2)
        st.metric(NUMPAIR_UI[lang]["score"], f"{np_['score']}/100")
        v = numpair_verdict(np_["score"], lang)
        if np_["score"] >= 55:
            st.success(v)
        elif np_["score"] >= 40:
            st.info(v)
        else:
            st.warning(v)
        st.write("• " + NUMPAIR_UI[lang]["tail_line"].format(a=np_["tail"]["a"], b=np_["tail"]["b"])
                 + " — " + NUMPAIR_REL[lang][np_["tail"]["rel"]])
        st.write("• " + NUMPAIR_UI[lang]["top_line"].format(
            a=np_["top"]["a"], sa=star_name(str(np_["top"]["a"]), lang),
            b=np_["top"]["b"], sb=star_name(str(np_["top"]["b"]), lang))
            + " — " + NUMPAIR_REL[lang][np_["top"]["rel"]])
        if np_["nines"]["a"] >= 1 and np_["nines"]["b"] >= 1:
            st.write("• ⭐ " + NUMPAIR_UI[lang]["nawin_line"])

    if use_couple and use_bd:
        st.subheader(T["couple_head"])
        k1 = day_key_from_date(bd, wed_pm)
        k2 = day_key_from_date(bd2, wed_pm2)
        cc = couple_compatibility(k1, k2)
        st.markdown(f"{T['person1']}: **{day_name(k1)}** ({day_animal(k1)}) × "
                    f"{T['person2']}: **{day_name(k2)}** ({day_animal(k2)})")
        if lang == "th":
            tone_txt, body = cc["tone"], cc["text"]
        else:
            tone_txt = COUPLE_TONE[lang][cc["tone"]]
            p1, p2 = star_name(str(DAYS[k1]["num"]), lang), star_name(str(DAYS[k2]["num"]), lang)
            if frozenset((k1, k2)) in COUPLE_CLASH:
                body = COUPLE_TEXT[lang]["clash"]
            else:
                rel = relation(DAYS[k1]["num"], DAYS[k2]["num"])
                body = COUPLE_TEXT[lang][rel].format(p1=p1, p2=p2, d=day_name(k1))
        if cc["tone"] in ("ดีมาก", "ดี"):
            st.success(f"{tone_txt} — {body}")
        elif cc["tone"] == "กลาง":
            st.info(f"{tone_txt} — {body}")
        else:
            st.warning(f"{tone_txt} — {body}")
            st.caption(T["couple_note"])
    elif use_couple and not use_bd and not has_num2:
        st.info(T["couple_need_bd"])

    # ---------- Auspicious days ----------
    st.subheader(T["aus_head"])
    st.caption(T["aus_cap"])
    win = auspicious_window(dt.date.today(), 14)
    aus_rows = []
    for a in win:
        if a["yatyaza"]:
            v = ASTRO_VERDICT[lang]["yat"]
        elif a["pyathada"] == 1:
            v = ASTRO_VERDICT[lang]["pya"]
        elif a["pyathada"] == 2:
            v = ASTRO_VERDICT[lang]["pya2"]
        else:
            v = ASTRO_VERDICT[lang]["norm"]
        month = a["month_th"].split(" ")[0] if lang == "th" else MONTH_TR[lang].get(a["mm"], str(a["mm"]))
        aus_rows.append({"": a["icon"], T["col_date"]: a["date"].strftime("%d/%m/%Y"),
                         T["col_day"]: WEEKDAY_TR[lang][a["wd"]], T["col_mmonth"]: month, T["col_luck"]: v})
    st.dataframe(aus_rows, use_container_width=True, hide_index=True)
    best = [a for a in win if a["yatyaza"]]
    if best:
        st.success(T["aus_best"].format(date=best[0]["date"].strftime("%d/%m/%Y"),
                                        day=WEEKDAY_TR[lang][best[0]["wd"]]))

    # ---------- Stars & careers ----------
    st.subheader(T["stars_head"])
    cnt = Counter(core)
    tops = [d for d, _ in cnt.most_common() if d != "0"][:3]
    for d in tops:
        st.write(f"**{d} ({star_name(d, lang)}) ×{cnt[d]}** — {digit_trait(d, lang)}")
    careers_src = CAREER_BY_DIGIT if lang == "th" else CAREER_TR[lang]
    careers = [careers_src[d] for d in tops if careers_src.get(d)]
    st.write(f"{T['career_line']}: " + " · ".join(careers))

    st.divider()
    st.caption(T["disclaimer"])
elif go:
    st.warning(T["need_number"])

# ---------- Footer ----------
st.markdown("""
<div class="nl-foot">
  <div class="stars">✦ ✦ ✦</div>
  <a class="nl-pill" href="https://ft.jbacworkhub.com">🌐 ft.jbacworkhub.com</a>
</div>
""", unsafe_allow_html=True)
