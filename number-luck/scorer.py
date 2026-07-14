"""
เครื่องคิดคะแนนเบอร์มงคล — สูตรของเราเอง (Number Luck)
========================================================
- ระบบของเราเอง 100% ไม่พึ่ง berlnw ตอนใช้งาน (เป๊ะเสมอ อธิบายได้)
- โครงสร้าง:
    1) แต่ละ "คู่เลขติดกัน" มีค่าพลัง (pair_power) ตามตำราเลขศาสตร์ -10..+10
    2) ถ่วงน้ำหนักตามตำแหน่ง (pos_weight) — คู่ท้ายสำคัญสุด, หลักแรกไม่คิด
    3) รวมแล้วปรับสเกลเป็นเกรด 0-100 (สอบเทียบให้อยู่ย่านที่คุ้นเคย)
- แก้ค่าคู่เลขได้ที่ our_model.json / pairs_table.csv

ใช้งาน:
    from scorer import score_number
    score_number("09751899888")
"""
import json, os, re

_M = json.load(open(os.path.join(os.path.dirname(__file__), "our_model.json"), encoding="utf-8"))
PAIR_POWER = _M["pair_power"]      # 100 ค่า (index = คู่เลข 00-99)
POS_WEIGHT = _M["pos_weight"]      # 8 ตำแหน่ง
_A1, _A0 = _M["cal_a1"], _M["cal_a0"]

# เกรดของเรา (อิงย่าน berlnw เพื่อความคุ้นเคย)
GRADE_BANDS = [
    (85, "ดีมาก"),
    (70, "ดี"),
    (50, "ดีพอใช้"),
    (20, "พอใช้"),
    (0,  "ไม่ดี"),
    (-999, "เสีย"),
]
PREMIUM_CUTOFF = 97   # "เบอร์เกิน 97"


def extract_core(raw: str) -> str:
    """รับเบอร์พม่าดิบ -> แกนเบอร์ 9 หลัก (ตัดรหัส 09)"""
    digits = re.sub(r"\D", "", str(raw))
    if digits.startswith("09"):
        digits = digits[2:]
    elif len(digits) == 10 and digits.startswith("9"):
        digits = digits[1:]
    return digits


def grade_of(g100: float) -> str:
    for lo, name in GRADE_BANDS:
        if g100 >= lo:
            return name
    return "เสีย"


def analyze_core(core: str) -> dict:
    """รองรับแกนเบอร์ 7-9 หลัก (MPT เก่า 7 หลัก / ค่ายใหม่ 9 หลัก)
    น้ำหนักตำแหน่งยึดจากท้าย (คู่ท้ายสำคัญสุดเสมอ) และปรับสเกลให้เทียบเกรดเดียวกัน"""
    if not core.isdigit() or not (7 <= len(core) <= 9):
        raise ValueError(f"แกนเบอร์ต้องเป็นตัวเลข 7-9 หลัก ได้: {core!r}")
    npairs = len(core) - 1
    weights = POS_WEIGHT[-npairs:]          # ยึดตำแหน่งท้าย
    pairs = []
    raw = 0.0
    for pos in range(npairs):
        p = int(core[pos]) * 10 + int(core[pos + 1])
        power = PAIR_POWER[p]
        w = weights[pos]
        raw += w * power
        pairs.append({"pair": f"{core[pos]}{core[pos+1]}", "power": power, "weight": w})
    raw *= sum(POS_WEIGHT) / sum(weights)   # ปรับสเกลเบอร์สั้นให้เทียบเกรดเดียวกัน
    g100 = _A1 * raw + _A0
    g100 = max(0.0, min(100.0, g100))
    return {"raw": raw, "grade100": round(g100, 1), "grade": grade_of(g100), "pairs": pairs}


def score_number(raw: str) -> dict:
    core = extract_core(raw)
    a = analyze_core(core)
    return {
        "input": raw,
        "full": "09" + core,
        "core": core,
        "grade100": a["grade100"],
        "grade": a["grade"],
        "premium": a["grade100"] > PREMIUM_CUTOFF,
        "pairs": a["pairs"],
    }


if __name__ == "__main__":
    import sys
    for n in (sys.argv[1:] or ["09666355536", "09689169999", "09751899888", "09962888999"]):
        r = score_number(n)
        pr = " ".join(f"{p['pair']}({p['power']:+d})" for p in r["pairs"])
        print(f"{r['full']}  เกรด {r['grade100']:>5}  {r['grade']}"
              + ("  ⭐เกิน97" if r["premium"] else ""))
        print(f"    คู่เลข: {pr}")
