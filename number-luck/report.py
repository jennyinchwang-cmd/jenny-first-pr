# -*- coding: utf-8 -*-
"""
ตัวสร้างรายงานทำนายเบอร์แบบละเอียด — Number Luck (เนื้อหาของเราเอง)
====================================================================
รวม scorer (คะแนน/เกรด) + meanings (คลังความหมายคู่เลข)
→ รายงาน: เกรด, จุดเด่นรายคู่, คำทำนาย 5 ด้าน, อาชีพที่เหมาะ, ข้อควรระวัง

ใช้งาน:  python report.py 09696555939
"""
import sys
from scorer import score_number
from meanings import pair_meaning, DIGIT

# ดาวเด่นแต่ละด้าน → ใช้จัดกลุ่มว่าเบอร์นี้เด่นด้านไหน
ASPECT_LABEL = {
    "money": "💰 การเงิน", "work": "💼 การงาน", "love": "❤️ ความรัก",
    "health": "🩺 สุขภาพ", "char": "🧭 อุปนิสัย",
}
CAREER_BY_DIGIT = {
    "1": "งานบริหาร หัวหน้างาน เจ้าของกิจการ ราชการ",
    "2": "งานประสานงาน บริการ ล่าม การทูต งานฝีมือ",
    "3": "ทหาร ตำรวจ นักกีฬา วิศวกรรม งานช่าง งานท้าทาย",
    "4": "การค้า การตลาด นักขาย สื่อสารมวลชน ออนไลน์",
    "5": "ครู วิชาการ กฎหมาย ที่ปรึกษา แพทย์ งานที่ใช้ความน่าเชื่อถือ",
    "6": "การเงินการลงทุน ศิลปะ บันเทิง ความงาม ของหรูหรา ร้านอาหาร",
    "7": "อสังหาริมทรัพย์ ที่ดิน โรงงาน เกษตร งานที่ใช้ความอดทน",
    "8": "ธุรกิจต่างประเทศ ลงทุนความเสี่ยงสูง งานกลางคืน โลจิสติกส์",
    "9": "งานสายบุญ ครูบาอาจารย์ งานต่างประเทศ เทคโนโลยี งานที่ใช้บารมี",
    "0": "",
}

def build_report(raw_number: str) -> str:
    r = score_number(raw_number)
    core = r["core"]
    pairs = r["pairs"]           # [{'pair','power','weight'}...]
    lines = []
    ap = lines.append

    from extra import sum_analysis, myanmar_analysis
    sm = sum_analysis(r["full"])
    mm = myanmar_analysis(r["full"])
    adj = round(min(100.0, max(0.0, r["grade100"] + sm["bonus"] + mm["bonus"])), 1)

    ap(f"═══ รายงานวิเคราะห์เบอร์ {r['full']} ═══")
    ap(f"แกนเบอร์ (ตัดรหัส 09): {core}")
    ap(f"เกรดโครงสร้างคู่เลข: {r['grade100']}/100  ({r['grade']})")
    ap(f"ตัวเสริม: ผลรวม {sm['bonus']:+.1f} | มิติพม่า {mm['bonus']:+.1f}")
    ap(f"เกรดสุทธิ: {adj}/100" + ("  ⭐ ระดับพรีเมียม (เกิน 97)" if adj > 97 else ""))
    ap("")

    # ---- 1) แจกแจงรายคู่ ----
    ap("── โครงสร้างคู่เลข ──")
    weighted = []
    for i, p in enumerate(pairs):
        m = pair_meaning(p["pair"])
        contrib = p["power"] * p["weight"]
        weighted.append((contrib, p, m, i))
        star = "★" if abs(contrib) >= 5 else " "
        note = " (คู่ท้าย-น้ำหนักสูงสุด)" if i == 7 else (" (คู่แรก-ไม่นับคะแนน)" if i == 0 else "")
        ap(f"{star} คู่ {p['pair']} [{m['title']}] พลัง {p['power']:+d}{note}")
        ap(f"    ↳ {m['desc']}")
    ap("")

    # ---- 2) ผลคำทำนายโชคชะตา แบบย่อหน้ายาว + น้ำหนัก % ----
    from meanings import pair_paragraph
    # เลือกคู่ที่มีอิทธิพล (ไม่นับคู่แรก) — ไม่ซ้ำคู่กัน เรียงตาม |อิทธิพล|
    seen_pairs, influential = set(), []
    for x in sorted(weighted[1:], key=lambda t: -abs(t[0])):
        if x[1]["pair"] not in seen_pairs:
            seen_pairs.add(x[1]["pair"])
            influential.append(x)
    influential = influential[:5]
    # แปลงอิทธิพลเป็นน้ำหนัก % (ปัดเป็นขั้นละ 5 รวม 100)
    mags = [max(abs(c), 0.5) for c, _, _, _ in influential]
    total = sum(mags)
    pct = [round(m_ / total * 20) * 5 for m_ in mags]
    diff = 100 - sum(pct)
    pct[0] += diff  # ปรับเศษให้คู่เด่นสุด
    ap("── ผลคำทำนายโชคชะตา (น้ำหนักรวม 100%) ──")
    for (contrib, p, m, i), w in zip(influential, pct):
        tone = "จุดแข็ง" if contrib >= 0 else "จุดต้องระวัง"
        ap(f"◆ น้ำหนักคำทำนาย {w}% — {tone} (คู่ {p['pair']} ตำแหน่งที่ {i+1})")
        ap(f"  {pair_paragraph(p['pair'], p['power'])}")
        ap("")

    # ---- 2.5) ผลรวมเบอร์ + มิติพม่า ----
    ap("── ผลรวมเบอร์ (ศาสตร์ประกอบ) ──")
    tone_icon = {"ดี": "✚", "ระวัง": "⚠", "กลาง": "•"}[sm["tone"]]
    ap(f"  ผลรวมทุกหลัก = {sm['total']}  {tone_icon} {sm['text']}")
    ap(f"  ดาวประจำผลรวม: เลข {sm['root']} ({sm['root_star']}) — {sm['root_text']}")
    ap("  หมายเหตุ: ตามหลักวิชา คู่เลขมีน้ำหนักมากกว่าผลรวม ผลรวมเป็นเพียงตัวเสริม")
    ap("")
    ap("── มิติเลขศาสตร์พม่า (นวิน) ──")
    for n in mm["notes"]:
        ap(f"  ★ {n}")
    ap("")

    # ---- 3) ดาวเด่น + อาชีพ ----
    from collections import Counter
    cnt = Counter(core)
    top_digits = [d for d, _ in cnt.most_common() if d != "0"][:3]
    ap("── ดาวเด่นประจำเบอร์ ──")
    for d in top_digits:
        ap(f"  เลข {d} ({DIGIT[d]['name']}) x{cnt[d]} ตัว — {DIGIT[d]['trait']}")
    careers = [CAREER_BY_DIGIT[d] for d in top_digits if CAREER_BY_DIGIT[d]]
    ap("")
    ap("── อาชีพที่ส่งเสริม ──")
    for c in careers:
        ap(f"  • {c}")
    ap("")

    # ---- 4) จุดแข็ง/ข้อควรระวัง ----
    pos = [x for x in weighted[1:] if x[0] > 0]
    neg = [x for x in weighted[1:] if x[0] < 0]
    ap("── สรุป ──")
    ap(f"  จุดแข็ง: คู่เลขบวก {len(pos)}/7 คู่" + (" — โครงสร้างเบอร์สะอาดมาก" if not neg else ""))
    if neg:
        worst = min(neg, key=lambda x: x[0])
        ap(f"  ข้อควรระวัง: คู่ {worst[1]['pair']} — {worst[2]['desc']}")
    else:
        ap("  ไม่มีคู่เสียในตำแหน่งที่มีน้ำหนักเลย")
    tail = pairs[7]
    ap(f"  คู่ท้าย ({tail['pair']}) คือชะตาหลักของเบอร์ — {pair_meaning(tail['pair'])['desc']}")
    return "\n".join(lines)


if __name__ == "__main__":
    num = sys.argv[1] if len(sys.argv) > 1 else "09696555939"
    print(build_report(num))
