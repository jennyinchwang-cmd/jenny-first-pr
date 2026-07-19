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

if go and number:
    core = extract_core(number)
    if not core.isdigit() or not (7 <= len(core) <= 9):
        st.error(T["bad_number"])
        st.stop()

    r = score_number(number)
    sm = sum_analysis(r["full"])
    mm = myanmar_analysis(r["full"])
    adj = round(min(100.0, max(0.0, r["grade100"] + sm["bonus"] + mm["bonus"])), 1)

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
