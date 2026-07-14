# -*- coding: utf-8 -*-
"""
ปฏิทินพม่า + วันโหราศาสตร์ (ยัตยาซา/เปียตะดา) — Number Luck
=============================================================
Port จาก ceMmDateTime.js (mmcal) ของ Dr. Yan Naing Aye — MIT License
https://github.com/yan9a/mmcal  (อัลกอริทึม cool-emerald มาตรฐาน de facto)
Port เฉพาะส่วนที่ใช้: แปลงวันที่ → ปฏิทินพม่า, ยัตยาซา (วันมงคล),
เปียตะดา (วันอัปมงคล รวมเปียตะดาช่วงบ่าย), วันอุโบสถ, ทิศหัวนาค
รองรับ ค.ศ. 1855 เป็นต้นไป (ศักราชพม่ายุค 2-3)
"""
import datetime as _dt
import math

_SY = 1577917828.0 / 4320000.0     # solar year 365.2587565
_LM = 1577917828.0 / 53433336.0    # lunar month 29.53058795
_MO = 1954168.050623               # epoch ME 0 (MMT)

MONTH_NAMES = {
    0: "วาโสแรก (1st Waso)", 1: "ดะกู (Tagu)", 2: "กะโซน (Kason)", 3: "นะโหย่ง (Nayon)",
    4: "วาโส (Waso)", 5: "วากอง (Wagaung)", 6: "ต่อสะลีน (Tawthalin)",
    7: "สะดีงจุต (Thadingyut)", 8: "ดะซาวโมน (Tazaungmon)", 9: "นะด่อ (Nadaw)",
    10: "ปยาโท (Pyatho)", 11: "ดะโบ่ดแว (Tabodwe)", 12: "ดะบอง (Tabaung)",
    13: "ดะกูปลาย (Late Tagu)", 14: "กะโซนปลาย (Late Kason)",
}
WEEKDAY_TH = ["เสาร์", "อาทิตย์", "จันทร์", "อังคาร", "พุธ", "พฤหัสบดี", "ศุกร์"]  # 0=สdays


def _jdn(date: _dt.date) -> int:
    """Julian Day Number (เที่ยงวันท้องถิ่น) จากวันที่เกรกอเรียน"""
    a = (14 - date.month) // 12
    y = date.year + 4800 - a
    m = date.month + 12 * a - 3
    return date.day + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045


def _my_const(my: int) -> dict:
    """ค่าคงที่ยุคปฏิทิน (port GetMyConst — เฉพาะยุค 2-3, ME >= 1217)"""
    EW = 0
    if my >= 1312:      # ยุค 3 (หลังเอกราช)
        EI, WO, NM = 3, -0.5, 8
        fme = [(1377, 1)]
        wte = [1344, 1345]
    elif my >= 1217:    # ยุค 2 (อาณานิคม)
        EI, WO, NM = 2, -1, 4
        fme = [(1234, 1), (1261, -1)]
        wte = [1263, 1264]
    else:
        raise ValueError(f"รองรับเฉพาะ ME >= 1217 (ค.ศ. 1855+) ได้: {my}")
    for k, v in fme:
        if k == my:
            WO += v
    if my in wte:
        EW = 1
    return {"EI": EI, "WO": WO, "NM": NM, "EW": EW}


def _cal_watat(my: int) -> dict:
    c = _my_const(my)
    TA = (_SY / 12 - _LM) * (12 - c["NM"])
    ed = (_SY * (my + 3739)) % _LM
    if ed < TA:
        ed += _LM
    fm = round(_SY * my + _MO - ed + 4.5 * _LM + c["WO"])
    watat = 0
    if c["EI"] >= 2:
        TW = _LM - (_SY / 12 - _LM) * c["NM"]
        if ed >= TW:
            watat = 1
    watat ^= c["EW"]
    return {"fm": fm, "watat": watat}


def _cal_my(my: int) -> dict:
    yd, werr, fm = 0, 0, 0
    y2 = _cal_watat(my)
    myt = y2["watat"]
    while True:
        yd += 1
        y1 = _cal_watat(my - yd)
        if y1["watat"] != 0 or yd >= 3:
            break
    if myt:
        nd = (y2["fm"] - y1["fm"]) % 354
        myt = nd // 31 + 1
        fm = y2["fm"]
        if nd not in (30, 31):
            werr = 1
    else:
        fm = y1["fm"] + 354 * yd
    tg1 = y1["fm"] + 354 * yd - 102
    return {"myt": myt, "tg1": tg1, "fm": fm, "werr": werr}


def j2m(jdn: int) -> dict:
    """Julian Day Number → วันที่พม่า (my, mm, md, myt)"""
    my = math.floor((jdn - 0.5 - _MO) / _SY)
    yo = _cal_my(my)
    dd = jdn - yo["tg1"] + 1
    b = yo["myt"] // 2
    c = 1 // (yo["myt"] + 1)
    myl = 354 + (1 - c) * 30 + b
    mmt = (dd - 1) // myl
    dd -= mmt * myl
    a = (dd + 423) // 512
    mm = math.floor((dd - b * a + c * a * 30 + 29.26) / 29.544)
    e = (mm + 12) // 16
    f = (mm + 11) // 16
    md = dd - math.floor(29.544 * mm - 29.26) - b * e + c * f * 30
    mm += f * 3 - e * 4 + 12 * mmt
    return {"myt": yo["myt"], "my": my, "mm": mm, "md": md}


def cal_yatyaza(mm: int, wd: int) -> int:
    m1 = mm % 4
    wd1 = m1 // 2 + 4
    wd2 = ((1 - m1 // 2) + m1 % 2) * (1 + 2 * (m1 % 2))
    return 1 if wd in (wd1, wd2) else 0


def cal_pyathada(mm: int, wd: int) -> int:
    """0=ปกติ, 1=เปียตะดา, 2=เปียตะดาช่วงบ่าย"""
    m1 = mm % 4
    wda = [1, 3, 3, 0, 2, 1, 2]
    p = 0
    if m1 == 0 and wd == 4:
        p = 2
    if m1 == wda[wd]:
        p = 1
    return p


def cal_sabbath(md: int, mm: int, myt: int) -> int:
    mml = 30 - mm % 2
    if mm == 3:
        mml += myt // 2
    if md in (8, 15, 23, mml):
        return 1
    if md in (7, 14, 22, mml - 1):
        return 2
    return 0


def cal_nagahle(mm: int) -> int:
    """ทิศหัวนาค [0=ตะวันตก, 1=เหนือ, 2=ตะวันออก, 3=ใต้]"""
    if mm <= 0:
        mm = 4
    return (mm % 12) // 3


def astro_day(date: _dt.date) -> dict:
    """สรุปวันโหราศาสตร์พม่าของวันที่หนึ่งวัน"""
    jdn = _jdn(date)
    wd = (jdn + 2) % 7          # 0=เสาร์ ... 6=ศุกร์
    m = j2m(jdn)
    yat = cal_yatyaza(m["mm"], wd)
    pya = cal_pyathada(m["mm"], wd)
    sab = cal_sabbath(m["md"], m["mm"], m["myt"])
    if yat:
        verdict, icon = "ยัตยาซา — วันมงคล เหมาะเริ่มสิ่งใหม่/เปิดเบอร์", "✅"
    elif pya == 1:
        verdict, icon = "เปียตะดา — วันอัปมงคล ควรเลี่ยงเริ่มการใหญ่", "🔴"
    elif pya == 2:
        verdict, icon = "เปียตะดาช่วงบ่าย — เช้าใช้ได้ เลี่ยงช่วงบ่าย", "🟠"
    else:
        verdict, icon = "วันปกติ", "⚪"
    return {"date": date, "weekday_th": WEEKDAY_TH[wd], "wd": wd,
            "my": m["my"], "mm": m["mm"], "md": m["md"],
            "month_th": MONTH_NAMES.get(m["mm"], str(m["mm"])),
            "yatyaza": yat, "pyathada": pya, "sabbath": sab,
            "verdict": verdict, "icon": icon}


def auspicious_window(start: _dt.date, days: int = 14) -> list:
    """ตารางฤกษ์ล่วงหน้า N วัน (สำหรับ 'ฤกษ์เปิดเบอร์')"""
    return [astro_day(start + _dt.timedelta(days=i)) for i in range(days)]


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    today = _dt.date(2026, 7, 14)
    for a in auspicious_window(today, 14):
        print(f"{a['icon']} {a['date']} ({a['weekday_th']:<8}) ME {a['my']} "
              f"{a['month_th']} วันที่ {a['md']:>2}  {a['verdict']}")
