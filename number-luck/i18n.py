# -*- coding: utf-8 -*-
"""
คลังแปล 3 ภาษา (ไทย/English/မြန်မာ) — Number Luck
====================================================
- UI: ข้อความหน้าเว็บทั้งหมด
- เนื้อหา: ดาว/คู่เลข/วันเกิด/เรือนมหาโพติ/อาชีพ/ยะดะยา
ภาษาไทยใช้ต้นฉบับใน meanings.py/burmese.py — EN/MM ใช้คลังนี้
"""
from meanings import DIGIT, DIGIT_LONG, SPECIAL, pair_meaning, pair_paragraph

LANGS = {"th": "ไทย", "en": "English", "mm": "မြန်မာ"}

# ---------------- UI strings ----------------
UI = {
"th": {
    "title": "🔮 Number Luck", "tagline": "วิเคราะห์เบอร์โทรศัพท์พม่า — ศาสตร์คู่เลข + โกนะวิน + ดวงวันเกิด 8 วันแบบพม่า",
    "phone_label": "เบอร์โทรศัพท์ (เช่น 09696555939)",
    "bd_expander": "🎂 ใส่วันเกิดหรือชื่อ (เช็คความเข้ากันเบอร์กับดวงเจ้าของ)",
    "bd_check": "ต้องการเช็คความเข้ากันกับวันเกิด", "bd_label": "วันเกิด",
    "wed_pm": "เกิดวันพุธหลังเที่ยง (ราศียาฮู/ราหู)",
    "name_label": "หรือพิมพ์ชื่อ (ภาษาอังกฤษ เช่น Aung, Kyaw, Su) — ระบบเดาวันเกิดจากอักษรแรกตามธรรมเนียมพม่า",
    "couple_expander": "🫶 เช็คดวงคู่ (คู่รัก/หุ้นส่วน)", "couple_check": "ต้องการเช็คดวงคู่",
    "bd2_label": "วันเกิดคนที่ 2", "wed_pm2": "คนที่ 2 เกิดวันพุธหลังเที่ยง",
    "analyze": "🔍 วิเคราะห์เบอร์", "bad_number": "รูปแบบเบอร์ไม่ถูกต้อง — ต้องเป็นเบอร์พม่า 09 ตามด้วย 7-9 หลัก (รองรับทุกค่าย MPT/ATOM/Ooredoo/Mytel) เช่น 09696555939",
    "need_number": "กรุณาใส่เบอร์โทรศัพท์ก่อนครับ",
    "grade_net": "เกรดสุทธิ", "grade_level": "ระดับ", "bonus": "ตัวเสริม",
    "premium": "⭐ ระดับพรีเมียม (เกิน 97) — เบอร์หายาก คุณภาพสูงสุด",
    "pairs_head": "🔢 โครงสร้างคู่เลข",
    "col_pair": "คู่", "col_star": "ดาว", "col_power": "พลัง", "col_meaning": "ความหมาย", "col_note": "หมายเหตุ",
    "tail_note": "คู่ท้าย (ชะตาหลัก)", "head_note": "คู่แรก (ไม่นับคะแนน)",
    "fortune_head": "🔮 ผลคำทำนายโชคชะตา",
    "strength": "🟢 จุดแข็ง", "caution": "🔴 จุดต้องระวัง", "weight": "น้ำหนักคำทำนาย",
    "pair_word": "คู่",
    "sum_head": "➕ ผลรวมเบอร์ & มิติพม่า", "sum_all": "ผลรวมทุกหลัก",
    "sum_root": "ดาวประจำผลรวม", "nawin_head": "นวิน (โกนะวิน) 🇲🇲",
    "bd_head": "🎂 ความเข้ากันกับดวงวันเกิด (ระบบ 8 วันพม่า)",
    "born_on": "เกิด", "planet": "ดาว", "day_num": "เลขประจำวัน", "direction": "ทิศ", "animal": "สัตว์ประจำวัน",
    "bd_trait": "อุปนิสัยตามวันเกิด", "compat_score": "คะแนนความเข้ากัน",
    "digit_by_digit": "รายหลัก (09-)", "legend": "🟢มิตร/เสริม ⭐นวิน ⚪กลาง 🔴ศัตรู",
    "name_match": "ชื่อ \"{name}\" (อักษร {pref}) ตรงกับ{day}ตามธรรมเนียมพม่า — ชื่อสอดคล้องดวงวันเกิด ✓",
    "name_mismatch": "ชื่อ \"{name}\" (อักษร {pref}) เป็นอักษรของ{nday} แต่วันเกิดจริงคือ{aday} — พม่าถือว่าใช้ได้ แต่ชื่อไม่ตรงวัน",
    "name_guess": "เดาวันเกิดจากชื่อ \"{name}\" (อักษรแรก {pref}) ตามธรรมเนียมตั้งชื่อพม่า",
    "mahabote_head": "🏛️ ผังมหาโพติเต็ม 7 เรือน + เบอร์นี้เติมเรือนไหนของคุณ",
    "col_house": "เรือน", "col_house_name": "ชื่อเรือน", "col_nature": "ธรรมชาติ", "col_sit": "ดาวที่สถิต",
    "nature_pos": "บวก", "nature_neg": "ภาระ",
    "mb_line": "มหาโพติ: ดาว{planet}สถิตเรือน {no} {house} ({nature}) — {desc}",
    "yadaya_head": "🛕 วิธีเสริมดวงตามวันเกิด (แนวยะดะยา)",
    "yadaya_cap": "ยะดะยา (ယတြာ) คือธรรมเนียมแก้เคล็ดของพม่า — โหรจะ 'สั่งใบยา' ด้วยเลข วัน และทิศ",
    "couple_head": "🫶 ดวงคู่ (คู่รัก/หุ้นส่วน)", "person1": "คนที่ 1", "person2": "คนที่ 2",
    "couple_need_bd": "🫶 ดวงคู่: กรุณาติ๊ก 'เช็คความเข้ากันกับวันเกิด' และใส่วันเกิดคนที่ 1 ด้วยครับ",
    "couple_note": "ตำราคู่เวรมีหลายสำนัก ผลนี้อิงตำราแต่งงานพม่ากระแสหลัก — แก้เคล็ดได้ด้วยการทำบุญร่วมกันตามวันเกิดทั้งสอง",
    "aus_head": "📅 ฤกษ์เปิดเบอร์ 14 วันข้างหน้า (ปฏิทินโหราศาสตร์พม่า)",
    "aus_cap": "ยัตยาซา (ရက်ရာဇာ) = วันมงคล | เปียตะดา (ပြဿဒါး) = วันอัปมงคล — คำนวณตามอัลกอริทึมปฏิทินพม่ามาตรฐาน",
    "col_date": "วันที่", "col_day": "วัน", "col_mmonth": "เดือนพม่า", "col_luck": "ฤกษ์",
    "aus_best": "แนะนำเปิดใช้เบอร์วันแรกที่เป็นยัตยาซา: **{date} ({day})**",
    "stars_head": "⭐ ดาวเด่นประจำเบอร์ & อาชีพที่ส่งเสริม", "career_line": "💼 เหมาะกับ",
    "disclaimer": "⚠️ คำทำนายอิงหลักเลขศาสตร์และความเชื่อทางวัฒนธรรม เพื่อเป็นแนวทางประกอบการตัดสินใจเท่านั้น",
    "lang_label": "ภาษา / Language / ဘာသာ",
},
"en": {
    "title": "🔮 Number Luck", "tagline": "Myanmar phone number analysis — digit pairs + Konawin + Myanmar 8-day birth astrology",
    "phone_label": "Phone number (e.g. 09696555939)",
    "bd_expander": "🎂 Enter birthday or name (check compatibility with the owner)",
    "bd_check": "Check compatibility with my birthday", "bd_label": "Birthday",
    "wed_pm": "Born Wednesday after noon (Rahu/Yahu sign)",
    "name_label": "Or type a name (English letters, e.g. Aung, Kyaw, Su) — birth day inferred from the first letter per Myanmar tradition",
    "couple_expander": "🫶 Couple check (partner/business)", "couple_check": "Check couple compatibility",
    "bd2_label": "Person 2's birthday", "wed_pm2": "Person 2 born Wednesday after noon",
    "analyze": "🔍 Analyze number", "bad_number": "Invalid format — must be a Myanmar number: 09 followed by 7-9 digits (all carriers: MPT/ATOM/Ooredoo/Mytel), e.g. 09696555939",
    "need_number": "Please enter a phone number first",
    "grade_net": "Overall grade", "grade_level": "Level", "bonus": "Modifiers",
    "premium": "⭐ Premium tier (above 97) — rare, top-quality number",
    "pairs_head": "🔢 Digit-Pair Structure",
    "col_pair": "Pair", "col_star": "Stars", "col_power": "Power", "col_meaning": "Meaning", "col_note": "Note",
    "tail_note": "Final pair (main destiny)", "head_note": "First pair (not scored)",
    "fortune_head": "🔮 Fortune Reading",
    "strength": "🟢 Strength", "caution": "🔴 Caution", "weight": "reading weight",
    "pair_word": "Pair",
    "sum_head": "➕ Number Sum & Myanmar Dimension", "sum_all": "Sum of all digits",
    "sum_root": "Ruling star of the sum", "nawin_head": "Nawin (Konawin) 🇲🇲",
    "bd_head": "🎂 Compatibility with Your Birth Day (Myanmar 8-Day System)",
    "born_on": "Born on", "planet": "Planet", "day_num": "Day number", "direction": "Direction", "animal": "Birth animal",
    "bd_trait": "Birth-day character", "compat_score": "Compatibility score",
    "digit_by_digit": "Digit by digit (09-)", "legend": "🟢 friend/self ⭐ nawin ⚪ neutral 🔴 enemy",
    "name_match": "The name \"{name}\" (letter {pref}) matches {day} per Myanmar tradition — name aligns with the birth day ✓",
    "name_mismatch": "The name \"{name}\" (letter {pref}) belongs to {nday}, but the actual birth day is {aday} — acceptable, though the name doesn't match the day",
    "name_guess": "Birth day inferred from the name \"{name}\" (first letter {pref}) per Myanmar naming tradition",
    "mahabote_head": "🏛️ Full Mahabote Chart — which of your houses does this number boost?",
    "col_house": "House", "col_house_name": "House name", "col_nature": "Nature", "col_sit": "Occupying planet",
    "nature_pos": "favorable", "nature_neg": "burden",
    "mb_line": "Mahabote: {planet} sits in House {no} {house} ({nature}) — {desc}",
    "yadaya_head": "🛕 Merit Remedies by Birth Day (Yadaya)",
    "yadaya_cap": "Yadaya (ယတြာ) is Myanmar's remedial tradition — astrologers 'prescribe' remedies using numbers, days and directions",
    "couple_head": "🫶 Couple Reading (partner/business)", "person1": "Person 1", "person2": "Person 2",
    "couple_need_bd": "🫶 Couple reading: please tick 'Check compatibility with my birthday' and enter Person 1's birthday",
    "couple_note": "Schools differ; this follows mainstream Myanmar marriage tradition — remedy: make merit together per both birth days",
    "aus_head": "📅 Auspicious Days to Activate (next 14 days, Myanmar astrological calendar)",
    "aus_cap": "Yatyaza (ရက်ရာဇာ) = auspicious | Pyathada (ပြဿဒါး) = inauspicious — computed with the standard Myanmar calendar algorithm",
    "col_date": "Date", "col_day": "Day", "col_mmonth": "Myanmar month", "col_luck": "Reading",
    "aus_best": "Recommended first Yatyaza day to activate: **{date} ({day})**",
    "stars_head": "⭐ Dominant Stars & Recommended Careers", "career_line": "💼 Suited for",
    "disclaimer": "⚠️ Readings are based on numerology and cultural beliefs — for guidance only",
    "lang_label": "ภาษา / Language / ဘာသာ",
},
"mm": {
    "title": "🔮 Number Luck", "tagline": "မြန်မာဖုန်းနံပါတ် ဗေဒင် — ဂဏန်းတွဲ + ကိုးနဝင်း + မြန်မာ့ရှစ်ရက်သားသမီး",
    "phone_label": "ဖုန်းနံပါတ် (ဥပမာ 09696555939)",
    "bd_expander": "🎂 မွေးနေ့ သို့မဟုတ် အမည် ထည့်ပါ (ပိုင်ရှင်နှင့် ကိုက်ညီမှုစစ်ရန်)",
    "bd_check": "မွေးနေ့နှင့် ကိုက်ညီမှု စစ်ဆေးလိုသည်", "bd_label": "မွေးနေ့",
    "wed_pm": "ဗုဒ္ဓဟူးနေ့ မွန်းလွဲပိုင်း မွေး (ရာဟု)",
    "name_label": "သို့မဟုတ် အမည်ရိုက်ထည့်ပါ (အင်္ဂလိပ်စာလုံး ဥပမာ Aung, Kyaw, Su) — ပထမစာလုံးဖြင့် မွေးနေ့ခန့်မှန်းသည်",
    "couple_expander": "🫶 စုံတွဲစစ်ဆေးမှု (ချစ်သူ/လုပ်ဖော်ကိုင်ဖက်)", "couple_check": "စုံတွဲကိုက်ညီမှု စစ်လိုသည်",
    "bd2_label": "ဒုတိယလူ၏ မွေးနေ့", "wed_pm2": "ဒုတိယလူ ဗုဒ္ဓဟူးမွန်းလွဲမွေး",
    "analyze": "🔍 နံပါတ်စစ်ဆေးမည်", "bad_number": "ပုံစံမမှန်ပါ — မြန်မာနံပါတ် 09 နောက် ၇-၉ လုံး (MPT/ATOM/Ooredoo/Mytel အားလုံး) ဥပမာ 09696555939",
    "need_number": "ဖုန်းနံပါတ် အရင်ထည့်ပါ",
    "grade_net": "စုစုပေါင်းရမှတ်", "grade_level": "အဆင့်", "bonus": "ဖြည့်စွက်ရမှတ်",
    "premium": "⭐ ပရီမီယံအဆင့် (၉၇ ကျော်) — ရှားပါး အရည်အသွေးအမြင့်ဆုံးနံပါတ်",
    "pairs_head": "🔢 ဂဏန်းတွဲဖွဲ့စည်းပုံ",
    "col_pair": "တွဲ", "col_star": "ဂြိုဟ်", "col_power": "စွမ်းအား", "col_meaning": "အဓိပ္ပာယ်", "col_note": "မှတ်ချက်",
    "tail_note": "နောက်ဆုံးတွဲ (အဓိကကံကြမ္မာ)", "head_note": "ပထမတွဲ (ရမှတ်မတွက်)",
    "fortune_head": "🔮 ကံကြမ္မာဟောစာတမ်း",
    "strength": "🟢 အားသာချက်", "caution": "🔴 သတိပြုရန်", "weight": "ဟောကိန်းအလေးချိန်",
    "pair_word": "တွဲ",
    "sum_head": "➕ ဂဏန်းပေါင်းလဒ်နှင့် မြန်မာ့ရှုထောင့်", "sum_all": "ဂဏန်းအားလုံးပေါင်းလဒ်",
    "sum_root": "ပေါင်းလဒ်၏ အုပ်စိုးဂြိုဟ်", "nawin_head": "နဝင်း (ကိုးနဝင်း) 🇲🇲",
    "bd_head": "🎂 မွေးနေ့နှင့် ကိုက်ညီမှု (မြန်မာ့ရှစ်ရက်စနစ်)",
    "born_on": "မွေးနေ့", "planet": "ဂြိုဟ်", "day_num": "နေ့ဂဏန်း", "direction": "အရပ်", "animal": "နေ့နံသတ္တဝါ",
    "bd_trait": "မွေးနေ့စရိုက်", "compat_score": "ကိုက်ညီမှုရမှတ်",
    "digit_by_digit": "ဂဏန်းတစ်လုံးချင်း (09-)", "legend": "🟢မိတ် ⭐နဝင်း ⚪ကြားနေ 🔴ရန်",
    "name_match": "အမည် \"{name}\" (စာလုံး {pref}) သည် {day} နှင့် ကိုက်ညီသည် — အမည်နှင့်မွေးနေ့ ညီညွတ်သည် ✓",
    "name_mismatch": "အမည် \"{name}\" (စာလုံး {pref}) သည် {nday} စာလုံးဖြစ်သော်လည်း အမှန်မွေးနေ့မှာ {aday} ဖြစ်သည်",
    "name_guess": "အမည် \"{name}\" (ပထမစာလုံး {pref}) ဖြင့် မွေးနေ့ခန့်မှန်းထားသည်",
    "mahabote_head": "🏛️ မဟာဘုတ်ဇယားအပြည့် — ဤနံပါတ်က သင့်ဘယ်အိမ်ကို ဖြည့်ပေးသလဲ",
    "col_house": "အိမ်", "col_house_name": "အိမ်အမည်", "col_nature": "သဘာဝ", "col_sit": "တည်သောဂြိုဟ်",
    "nature_pos": "ကောင်း", "nature_neg": "ဝန်ထုပ်",
    "mb_line": "မဟာဘုတ် — {planet}သည် အိမ် {no} {house} ({nature}) တွင်တည်သည် — {desc}",
    "yadaya_head": "🛕 မွေးနေ့အလိုက် ကံမြှင့်နည်း (ယတြာ)",
    "yadaya_cap": "ယတြာသည် မြန်မာ့ယုံကြည်မှုအရ ကံဆိုးချေဖျက်နည်းဖြစ်သည် — ဗေဒင်ဆရာက ဂဏန်း၊ နေ့၊ အရပ်တို့ဖြင့် ညွှန်ကြားသည်",
    "couple_head": "🫶 စုံတွဲဟောစာတမ်း (ချစ်သူ/လုပ်ဖော်ကိုင်ဖက်)", "person1": "ပထမလူ", "person2": "ဒုတိယလူ",
    "couple_need_bd": "🫶 စုံတွဲစစ်ရန် — 'မွေးနေ့နှင့်ကိုက်ညီမှုစစ်' ကို အမှန်ခြစ်ပြီး ပထမလူ၏မွေးနေ့ ထည့်ပါ",
    "couple_note": "ကျမ်းအမျိုးမျိုးရှိသည် — ဤရလဒ်သည် မြန်မာ့ထုံးတမ်းအဓိကကျမ်းကို အခြေခံသည်။ မွေးနေ့နှစ်ခုအလိုက် အတူကုသိုလ်ပြု၍ ယတြာချေနိုင်သည်",
    "aus_head": "📅 နံပါတ်စတင်သုံးရန် မင်္ဂလာနေ့များ (ရှေ့ ၁၄ ရက် — မြန်မာ့ပြက္ခဒိန်)",
    "aus_cap": "ရက်ရာဇာ = မင်္ဂလာနေ့ | ပြဿဒါး = မကောင်းသောနေ့ — စံမြန်မာပြက္ခဒိန် အယ်လဂိုရီသမ်ဖြင့် တွက်ချက်သည်",
    "col_date": "နေ့စွဲ", "col_day": "နေ့", "col_mmonth": "မြန်မာလ", "col_luck": "ဟောကိန်း",
    "aus_best": "ပထမဆုံး ရက်ရာဇာနေ့ **{date} ({day})** တွင် စတင်အသုံးပြုရန် အကြံပြုသည်",
    "stars_head": "⭐ ထင်ရှားသောဂြိုဟ်များနှင့် သင့်တော်သောအလုပ်များ", "career_line": "💼 သင့်တော်သည်",
    "disclaimer": "⚠️ ဟောစာတမ်းသည် ဂဏန်းဗေဒင်နှင့် ယဉ်ကျေးမှုယုံကြည်မှုအပေါ် အခြေခံသည် — လမ်းညွှန်အဖြစ်သာ အသုံးပြုပါ",
    "lang_label": "ภาษา / Language / ဘာသာ",
},
}

# ---------------- ดาวประจำเลข ----------------
STAR = {
    "0": {"th": "สุญตา", "en": "Void", "mm": "သုည"},
    "1": {"th": "อาทิตย์", "en": "Sun", "mm": "နေ (တနင်္ဂနွေ)"},
    "2": {"th": "จันทร์", "en": "Moon", "mm": "လ (တနင်္လာ)"},
    "3": {"th": "อังคาร", "en": "Mars", "mm": "အင်္ဂါ"},
    "4": {"th": "พุธ", "en": "Mercury", "mm": "ဗုဒ္ဓဟူး"},
    "5": {"th": "พฤหัส", "en": "Jupiter", "mm": "ကြာသပတေး"},
    "6": {"th": "ศุกร์", "en": "Venus", "mm": "သောကြာ"},
    "7": {"th": "เสาร์", "en": "Saturn", "mm": "စနေ"},
    "8": {"th": "ราหู", "en": "Rahu", "mm": "ရာဟု"},
    "9": {"th": "เกตุ", "en": "Ketu", "mm": "ကိတ်"},
}

# ---------------- ลักษณะดาวรายด้าน (EN/MM — ไทยใช้ meanings.py) ----------------
DIGIT_TR = {
"en": {
 "0": {"trait": "emptiness, uncertainty", "money": "finances fluctuate unpredictably", "work": "work lacks continuity", "love": "drifting, unclear relationships", "health": "low vitality, tires easily", "char": "indecisive, lacks direction"},
 "1": {"trait": "leadership, confidence", "money": "earns through one's own ability; income grows with responsibility", "work": "strong leadership; suited to management and ownership", "love": "loves with dignity, a dependable partner", "health": "strong body, quick recovery; watch stress", "char": "confident, decisive, honors pride"},
 "2": {"trait": "gentleness, negotiation, imagination", "money": "money flows in through coordination and goodwill", "work": "excels at detail, service and liaison work", "love": "romantic and attentive; lasting love", "health": "health follows mood; mind at ease keeps the body well", "char": "gentle, compromising, imaginative"},
 "3": {"trait": "courage, high energy, hot temper", "money": "earns boldly and fast, spends fast — needs saving discipline", "work": "thrives in competitive, hands-on, challenging work", "love": "passionate and jealous; stable with self-control", "health": "beware accidents, sharp objects, overexertion", "char": "brave, direct, action-first; sometimes impatient"},
 "4": {"trait": "communication, trade, wit", "money": "money comes from speech and wit; trade brings wealth", "work": "born communicator; sales, marketing, online work", "love": "fun to talk to, charming with words", "health": "watch stress and the nervous system", "char": "quick-minded, adaptable, reads people well"},
 "5": {"trait": "wisdom, virtue, elders' favor", "money": "steady finances with patronage and good credit", "work": "prospers in academia, law, teaching, consulting", "love": "rational, stable, faithful", "health": "generally good health, mindful self-care", "char": "calm, principled, trustworthy"},
 "6": {"trait": "charm, wealth, the arts", "money": "money flows well; earns from beauty and entertainment, but spends well too", "work": "finance, art, fashion, food, luxury — clients adore", "love": "strong charm, never lacks admirers; beware love triangles", "health": "cares for oneself well; watch indulgence", "char": "excellent taste, sweet, sociable"},
 "7": {"trait": "endurance, obstacles, strength", "money": "money comes through sweat; saving is hard", "work": "outworks everyone; land, factories, heavy industry", "love": "love is tested; patience and long waits", "health": "watch bones, joints, chronic fatigue", "char": "patient, steadfast, keeps feelings inside"},
 "8": {"trait": "risk, windfalls, influence", "money": "destined for windfalls; wins big but must manage risk", "work": "international business, investment, night work, bold ventures", "love": "intense, magnetic; beware improper relationships", "health": "watch intoxicants and burning the candle", "char": "big-hearted, daring, influential"},
 "9": {"trait": "merit, divinity, success", "money": "unexpected fortune keeps arriving; merit multiplies wealth", "work": "continuous advancement, early promotion, elders' favor", "love": "fulfilled love guided by past merit", "health": "protected and safe; recovers remarkably", "char": "innate charisma, sharp intuition, spiritual"},
},
"mm": {
 "0": {"trait": "ဟင်းလင်းမှု၊ မသေချာမှု", "money": "ငွေကြေး မတည်ငြိမ်", "work": "အလုပ် ဆက်တိုက်မဖြစ်", "love": "ချစ်ရေး မရေရာ", "health": "ခွန်အားနည်း ပင်ပန်းလွယ်", "char": "ဆုံးဖြတ်ချက် နှေးတတ်"},
 "1": {"trait": "ခေါင်းဆောင်မှု၊ ယုံကြည်မှု", "money": "ကိုယ့်စွမ်းရည်ဖြင့် ရှာဖွေ တာဝန်နှင့်အတူ ဝင်ငွေတိုး", "work": "ခေါင်းဆောင်စွမ်းရည်မြင့် စီမံခန့်ခွဲမှုနှင့် ကိုက်ညီ", "love": "ဂုဏ်သိက္ခာရှိစွာ ချစ်တတ် အားကိုးရသော ဘဝဖော်", "health": "ကျန်းမာသန်စွမ်း စိတ်ဖိစီးမှုသတိပြု", "char": "ယုံကြည်မှုရှိ ပြတ်သားပြီး ဂုဏ်သိက္ခာမြတ်နိုး"},
 "2": {"trait": "နူးညံ့မှု၊ ညှိနှိုင်းမှု၊ စိတ်ကူးဉာဏ်", "money": "ညှိနှိုင်းမှုနှင့် စေတနာဖြင့် ငွေဝင်", "work": "အသေးစိတ်၊ ဝန်ဆောင်မှု၊ ဆက်သွယ်ရေးအလုပ် တော်သည်", "love": "ရိုမန်းတစ်ဆန်ပြီး ဂရုစိုက်တတ် ချစ်ရေးတည်မြဲ", "health": "စိတ်ချမ်းသာလျှင် ကိုယ်ကျန်းမာ", "char": "နူးညံ့ ညှိနှိုင်းတတ် စိတ်ကူးကောင်း"},
 "3": {"trait": "သတ္တိ၊ စွမ်းအင်မြင့်၊ စိတ်မြန်", "money": "ရဲရင့်စွာ မြန်မြန်ရှာ မြန်မြန်သုံး — စုဆောင်းစည်းကမ်းလို", "work": "ပြိုင်ဆိုင်မှုနှင့် စိန်ခေါ်မှုရှိသော အလုပ်တွင် တော်သည်", "love": "ပြင်းထန်စွာချစ် မနာလိုတတ် စိတ်ထိန်းလျှင် တည်ငြိမ်", "health": "မတော်တဆမှုနှင့် အလွန်အကျွံ သတိပြု", "char": "ရဲရင့် ပွင့်လင်း လက်တွေ့သမား တစ်ခါတစ်ရံ စိတ်မြန်"},
 "4": {"trait": "ဆက်သွယ်ရေး၊ ကုန်သွယ်မှု၊ ဉာဏ်ရည်", "money": "စကားနှင့်ဉာဏ်ဖြင့် ငွေရှာ ကုန်သွယ်၍ ကြွယ်ဝ", "work": "အရောင်း၊ စျေးကွက်၊ အွန်လိုင်းလုပ်ငန်း တော်သည်", "love": "စကားချိုပြီး ဆွဲဆောင်မှုရှိ", "health": "စိတ်ဖိစီးမှုနှင့် အာရုံကြော သတိပြု", "char": "ဉာဏ်မြန် လိုက်လျောညီထွေ လူကိုနားလည်"},
 "5": {"trait": "ပညာ၊ ကိုယ်ကျင့်တရား၊ လူကြီးမေတ္တာ", "money": "ငွေကြေးတည်ငြိမ် လူကြီးထောက်ပံ့ ယုံကြည်စိတ်ချရ", "work": "ပညာရေး၊ ဥပဒေ၊ သင်ကြားရေး၊ အတိုင်ပင်ခံ တိုးတက်", "love": "ကျိုးကြောင်းညီ တည်ငြိမ် သစ္စာရှိ", "health": "ကျန်းမာရေးကောင်း ကိုယ့်ကိုဂရုစိုက်", "char": "စိတ်အေး မူရှိ ယုံကြည်လေးစားခံရ"},
 "6": {"trait": "ဆွဲဆောင်မှု၊ ဥစ္စာ၊ အနုပညာ", "money": "ငွေလည်ပတ်ကောင်း အလှနှင့်ဖျော်ဖြေရေးမှ ရှာနိုင် သုံးလည်းသုံးတတ်", "work": "ငွေကြေး၊ အနုပညာ၊ ဖက်ရှင်၊ အစားအသောက်၊ ဇိမ်ခံပစ္စည်း — ဖောက်သည်ချစ်", "love": "ဆွဲဆောင်မှုပြင်း ချစ်သူမပြတ် — ချစ်သုံးပွင့်ဆိုင် သတိ", "health": "ကိုယ့်ကိုဂရုစိုက်ကောင်း အပျော်အပါး သတိ", "char": "အရသာမြင့် ချိုသာ လူမှုရေးကောင်း"},
 "7": {"trait": "ခံနိုင်ရည်၊ အခက်အခဲ၊ ကြံ့ခိုင်မှု", "money": "ချွေးနှင့်ရသောငွေ စုဆောင်းရခက်", "work": "အလုပ်ကြမ်းခံနိုင် မြေ၊ စက်ရုံ၊ လယ်ယာ တော်သည်", "love": "ချစ်ရေး စမ်းသပ်ခံရ စောင့်ဆိုင်းရ", "health": "အရိုးအဆစ်နှင့် နာတာရှည်ပင်ပန်းမှု သတိပြု", "char": "သည်းခံ တည်ကြည် ခံစားချက် သိမ်းထားတတ်"},
 "8": {"trait": "စွန့်စားမှု၊ လာဘ်လာဘ၊ သြဇာ", "money": "လာဘ်ကြီးရတတ် ရဲရင့်စွာ ရ/ရှုံး — စွန့်စားမှုထိန်းရမည်", "work": "နိုင်ငံရပ်ခြားစီးပွား၊ ရင်းနှီးမြှုပ်နှံမှု၊ ညအလုပ်", "love": "ပြင်းထန်ဆွဲဆောင် — မသင့်တော်သောဆက်ဆံရေး သတိ", "health": "မူးယစ်ပစ္စည်းနှင့် အလွန်အကျွံ သတိပြု", "char": "ရက်ရော ရဲရင့် သြဇာရှိ"},
 "9": {"trait": "ဘုန်းကံ၊ နတ်ကောင်းစောင့်ရှောက်၊ အောင်မြင်မှု", "money": "မမျှော်လင့်သော လာဘ်ဝင်မြဲ ကုသိုလ်နှင့် ဥစ္စာတိုး", "work": "ရာထူးမြန်တက် လူကြီးချစ်ခင် တိုးတက်မှုမပြတ်", "love": "ကုသိုလ်ကံပါသော အချစ် ပြည့်ဝ", "health": "ဘေးကင်း လျင်မြန်စွာ ပြန်ကောင်း", "char": "ဘုန်းတန်ခိုး အာရုံထက်မြက် တရားကိုင်းရှိုင်း"},
},
}

# ---------------- คู่พิเศษ (EN/MM) ----------------
SPECIAL_TR = {
"en": {
 "15": "A leader with wisdom; elders' favor; rapid advancement in management and government",
 "51": "Wisdom crowns authority; entrusted with high positions; strong patronage",
 "24": "Charm in negotiation; superb at trade; money flows from many directions",
 "42": "Words turn to gold; a golden salesperson; customers keep coming back",
 "45": "Wit plus wisdom; a natural scholar and planner; ideal for academia and consulting",
 "54": "Elders support your voice; a gifted teacher; a trusted speaker",
 "46": "Trading beautiful things prospers; wealth streams in through charm of speech",
 "64": "Charm plus eloquence — whatever you sell, people buy; money never dries up",
 "56": "Wisdom paired with charm; beloved by elders; stable finances, smooth life",
 "65": "Charm with virtue; luck through elders; suited to positions of trust",
 "59": "Wisdom joined with merit; divine protection; good deeds bear fruit fast; a shining life",
 "95": "Old merit fuels wisdom; great teachers appear; suited to scholarship and spiritual paths",
 "69": "Charm and charisma; adored and aided by benefactors; money flows steadily",
 "96": "Charisma amplifies charm; shining fame; suited to entertainment and social spheres",
 "89": "Grand windfalls; influence paired with charisma; unexpected fortune favors the bold",
 "98": "Charisma governs risk; skilled at fortune; handles big money; thrives abroad",
 "78": "Endurance ends in great reward; hard work turns to wealth; real estate and industry",
 "87": "Iron will to grind; wealth earned through perseverance",
 "99": "Merit upon merit; the highest success; heavily protected by the divine",
 "66": "Wealth upon charm; abundant riches; a life of beauty and comfort",
 "55": "Wisdom doubled; exceptional favor from elders; continuous success; deeply trusted",
 "44": "Eloquence doubled; masterful talker — but beware talking too much",
 "22": "Sensitivity doubled; dreamy artistic soul; beware overthinking",
 "11": "Leader upon leader; fiercely decisive — beware clashing with others",
 "88": "Rahu doubled; very high risk; wins big, loses big — mindfulness required",
 "77": "Saturn doubled; heavy obstacles; twice the fatigue; a fighter's life",
 "33": "Mars doubled; overflowing energy; very hot-tempered — beware accidents and conflict",
 "00": "Void doubled; weak life force; plans rarely materialize",
 "13": "Power meets fire; dares every fight — beware emotion over reason",
 "31": "Charging leader; suited to challenges — military, police, athletics",
 "28": "Sensitivity meets risk; beware deception in money and love",
 "82": "Influence over a fragile heart; generous outside, tender inside; beware love entanglements",
 "27": "Moon meets Saturn; love faces obstacles; patient waiting wears the heart",
 "72": "Weight pressing on gentleness; bottled-up stress — beware accumulation",
 "34": "Fire meets tongue; quick words, quick temper — words can make enemies",
 "43": "Blunt to the point of pain; decisive speech — beware the mouth ruining fortune",
 "17": "Power under burden; carries great loads; a leader wearier than most",
 "71": "Obstacles before authority; must prove oneself harder than others",
 "06": "Wealth leaks away; money comes but won't stay — beware extravagance",
 "60": "Drifting charm; unstable love; finances stall in phases",
 "02": "A sensitive heart with no anchor; moody; hard to decide",
 "20": "Many dreams, little substance; lacks the push to finish",
 "07": "Void meets weight; a stuck period; everything drags — great patience needed",
 "70": "Effort without return at times; beware working for nothing",
 "01": "Power on emptiness — strong starts that fade; build a support team",
 "10": "A leader hitting voids — life stalls in phases; always keep a backup plan",
 "03": "Void meets fire — restless without direction; beware rash decisions",
 "30": "Fire that gutters mid-way — strong push, weak finish; guard your momentum",
 "04": "Void meets speech — much talk, little substance; beware promises you can't keep",
 "40": "Words without weight — easily forgotten; build credibility through results",
 "05": "Void meets wisdom — great ideas rarely executed; a patron's push helps",
 "50": "Wisdom facing void — knowledge is ready but chances come late; wait for timing",
 "08": "Void meets Rahu — baseless risk; easy come, easy go",
 "80": "Rahu into void — windfalls that don't last; beware leaking wealth",
 "09": "Void meets Ketu — merit protects, but your own effort must fill the gap",
 "90": "Merit ending in void — blessed, but carelessness is forbidden",
 "12": "Leader with gentleness — firm outside, soft inside; leads with heart, loved by the team",
 "21": "Gentleness lifting a leader — negotiation opens doors; elders adore you",
 "14": "Power with eloquence — commands clearly; an executive who negotiates well",
 "41": "Speech backing power — people follow your word; highly credible",
 "16": "A charming leader — beloved and followed; perfect for leading and selling",
 "61": "Charm boosting leadership — finances grow with your presence",
 "18": "Power with Rahu — strong influence, quick rise, many rivals; wield power with care",
 "81": "Rahu behind power — dares all the way to the top, but rises and falls hard",
 "19": "Leader with charisma — steady advancement; deeply respected; management and government shine",
 "91": "Charisma lifting a leader — high success; elders open doors the whole way",
 "23": "Softness meets fire — quick mood swings; a hot-tempered artist; beware clashes at home",
 "32": "Fire over a tender heart — brave outside, fragile inside; needs more support than shown",
 "25": "Moon–Jupiter, an enemy pair by lore — sensitivity clashes with principle; beware friction with elders",
 "52": "Principle pressing on sensitivity — overthinking breeds stress; find inner balance",
 "26": "Gentleness with charm — graceful and approachable; service, art and beauty flourish",
 "62": "Charm with softness — people fall for you; ideal for all people-facing work",
 "29": "Moon with Ketu — sharp intuition, prophetic dreams, a calm mind, old merit behind you",
 "92": "Ketu lifting the Moon — charisma with grace; kind helpers appear",
 "35": "Bold action on principle — a fighter with wisdom; elders spot and promote you",
 "53": "Wisdom leading courage — razor-sharp yet reasoned decisions; suited to law and order",
 "36": "Mars–Venus, friendly stars — brave and charming; charge ahead and be loved; aggressive sales thrive",
 "63": "Charm backing courage — sells with confidence; closes deals without hesitation",
 "37": "Mars–Saturn, an enemy pair — impatience breeds obstacles; heavy repeated work; beware injuries",
 "73": "Saturn over fire — tired yet still fighting; endurance tested to the limit",
 "38": "Fire with Rahu — force on force; extreme risk; fast gains, fast losses; only mindfulness saves",
 "83": "Rahu igniting fire — dependable daring in a crisis, but haste can ruin great things",
 "39": "Fire with Ketu — courage under merit's wing; break through obstacles to success",
 "93": "Ketu steering fire — power aimed true; brave yet mindful; succeeds faster than most",
 "47": "Speech meets Saturn — negotiations drag and tire; put every agreement on paper",
 "74": "Saturn pressing speech — words strained under stress; beware miscommunication",
 "48": "Speech with Rahu — persuasive about risk; a bold closer; beware talk that overreaches",
 "84": "Rahu boosting speech — sways crowds; mind the thin line into deception",
 "49": "Speech with Ketu — enchanted words; sacred speech; a born teacher and orator",
 "94": "Ketu behind speech — teaches brilliantly; merit flows through your words",
 "57": "Wisdom meets Saturn — deep and careful but slow; success arrives steadily",
 "75": "Saturn seasoning wisdom — learns from hardship; a veteran's seasoned wit",
 "58": "Wisdom with Rahu — clever about risk; suited to finance, insurance, business law",
 "85": "Rahu under wisdom — calculated risk-taking; a true investor",
 "67": "Venus–Saturn, an enemy pair — love faces obstacles; beautiful money earned with fatigue",
 "76": "Saturn over charm — beauty upon weariness; love must prove itself",
 "68": "Charm with Rahu — big money through boldness; nightlife circles; beware fleeting love",
 "86": "Rahu amplifying charm — magnetizes wealth and people; beware greed taking over",
 "79": "Saturn with Ketu — endure and merit delivers; hardship ends in light; late life shines",
 "97": "Ketu above Saturn — merit lightens the load; your perseverance gets recognized",
},
"mm": {
 "15": "ပညာရှိသောခေါင်းဆောင် လူကြီးမေတ္တာရ စီမံခန့်ခွဲမှုနှင့် အစိုးရလုပ်ငန်းတွင် လျင်မြန်စွာတက်",
 "51": "ပညာက အာဏာကိုထောက် ရာထူးကြီးအပ်နှင်းခံရ ထောက်ပံ့သူများ",
 "24": "ညှိနှိုင်းမှုတွင် ဆွဲဆောင်မှုရှိ ကုန်သွယ်မှုတော် ငွေဘက်စုံဝင်",
 "42": "စကားက ရွှေဖြစ် အရောင်းသမားထူးချွန် ဖောက်သည်ပြန်လာမြဲ",
 "45": "ဉာဏ်နှင့်ပညာပေါင်း ပညာရှင်နှင့် စီမံကိန်းသမား ကောင်း",
 "54": "လူကြီးထောက်ပံ့သော အသံ သင်ကြားပို့ချတော် ယုံကြည်ခံရ",
 "46": "အလှပစ္စည်းရောင်းဝယ် စီးပွားဖြစ် ချိုသာသောစကားဖြင့် ဥစ္စာစီးဝင်",
 "64": "ဆွဲဆောင်မှုနှင့် နှုတ်သတ္တိ — ဘာရောင်းရောင်း ဝယ်သူရှိ ငွေမပြတ်",
 "56": "ပညာနှင့်ဆွဲဆောင်မှုတွဲ လူကြီးချစ် ငွေကြေးတည်ငြိမ် ဘဝချောမွေ့",
 "65": "ကိုယ်ကျင့်တရားပါသော ဆွဲဆောင်မှု လူကြီးကံကောင်းပေး ယုံကြည်ရသောနေရာနှင့်သင့်",
 "59": "ပညာနှင့်ကုသိုလ်ပေါင်း နတ်ကောင်းစောင့် ကုသိုလ်အကျိုးမြန် ဘဝတောက်ပ",
 "95": "ကုသိုလ်ဟောင်းက ပညာကိုမွေး ဆရာကောင်းတွေ့ ပညာရေးနှင့် တရားလမ်းသင့်",
 "69": "ဆွဲဆောင်မှုနှင့်ဘုန်းကံ ချစ်ခင်ခံရ ကူညီသူမပြတ် ငွေစီးဝင်မြဲ",
 "96": "ဘုန်းကံက ဆွဲဆောင်မှုကိုမြှင့် ကျော်စောထင်ရှား ဖျော်ဖြေရေးနှင့် လူမှုရေးသင့်",
 "89": "လာဘ်ကြီးရ သြဇာနှင့်ဘုန်းကံတွဲ မမျှော်လင့်သောကံကောင်း",
 "98": "ဘုန်းကံက စွန့်စားမှုကိုအုပ်စိုး ကံစမ်းတော် ငွေကြီးကိုင်တွယ်နိုင် နိုင်ငံရပ်ခြားကောင်း",
 "78": "ခံနိုင်ရည်အဆုံး ဆုလာဘ်ကြီး ကြိုးစားမှုက ဥစ္စာဖြစ် အိမ်ခြံမြေနှင့် စက်မှုကောင်း",
 "87": "သံမဏိစိတ်ဖြင့် ကြိုးစား ဇွဲဖြင့်ရသော ဥစ္စာ",
 "99": "ကုသိုလ်ပေါ်ကုသိုလ် အောင်မြင်မှုအမြင့်ဆုံး နတ်ကောင်းအထူးစောင့်",
 "66": "ဆွဲဆောင်မှုပေါ် ဥစ္စာ ကြွယ်ဝပြည့်စုံ အလှနှင့်သက်သောင့်သက်သာဘဝ",
 "55": "ပညာနှစ်ဆ လူကြီးမေတ္တာအထူးရ အောင်မြင်မှုဆက်တိုက် အယုံကြည်ခံရဆုံး",
 "44": "နှုတ်သတ္တိနှစ်ဆ စကားပြောကျွမ်း — စကားများလွန်း သတိ",
 "22": "နူးညံ့မှုနှစ်ဆ အိပ်မက်များသော အနုပညာစိတ် — တွေးလွန်း သတိ",
 "11": "ခေါင်းဆောင်ပေါ်ခေါင်းဆောင် ပြတ်သားလွန်း — ထိပ်တိုက်တွေ့တတ် သတိ",
 "88": "ရာဟုနှစ်ဆ စွန့်စားမှုအလွန်မြင့် ကြီးကြီးရ ကြီးကြီးရှုံး — သတိကြီးစွာထား",
 "77": "စနေနှစ်ဆ အခက်အခဲလေး ပင်ပန်းနှစ်ဆ တိုက်ပွဲဝင်ဘဝ",
 "33": "အင်္ဂါနှစ်ဆ စွမ်းအင်လျှံ စိတ်အလွန်မြန် — မတော်တဆမှုနှင့် ပဋိပက္ခ သတိ",
 "00": "သုညနှစ်ဆ အသက်စွမ်းအားနည်း အစီအစဉ်များ အကောင်အထည်မပေါ်တတ်",
 "13": "အာဏာနှင့်မီးတွေ့ တိုက်ပွဲတိုင်းဝံ့ — စိတ်ခံစားမှုက ဆင်ခြင်မှုကိုမနိုင်စေနှင့်",
 "31": "တက်ကြွသောခေါင်းဆောင် စိန်ခေါ်မှုသင့် — စစ်၊ ရဲ၊ အားကစား",
 "28": "နူးညံ့မှုနှင့် စွန့်စားမှုတွေ့ — ငွေနှင့်အချစ်တွင် လှည့်စားခံရမှု သတိ",
 "82": "နုနယ်သောနှလုံးသားပေါ် သြဇာ အပြင်ရက်ရော အတွင်းနူးညံ့ — အချစ်ရှုပ်ထွေး သတိ",
 "27": "လနှင့်စနေတွေ့ အချစ်ရေးအခက်အခဲ စောင့်ဆိုင်းရ နှလုံးပင်ပန်း",
 "72": "နူးညံ့မှုပေါ် ဝန်ထုပ်ဖိ စိတ်ဖိစီးမှုစုပုံ — သတိပြု",
 "34": "မီးနှင့်လျှာတွေ့ စကားမြန် စိတ်မြန် — စကားက ရန်သူဖြစ်စေတတ်",
 "43": "ထိမိအောင်ပွင့်လင်း ပြတ်သားသောစကား — နှုတ်က ကံဖျက်တတ် သတိ",
 "17": "ဝန်ထုပ်အောက်က အာဏာ ဝန်ကြီးထမ်း ခေါင်းဆောင်ပင်ပန်း",
 "71": "အာဏာမတိုင်မီ အခက်အခဲ ကိုယ့်ကိုပိုပြရ",
 "06": "ဥစ္စာယိုစိမ့် ငွေဝင်သော်လည်း မတည် — ဖြုန်းတီးမှု သတိ",
 "60": "မရေရာသော ဆွဲဆောင်မှု အချစ်မတည်ငြိမ် ငွေကြေး အဆင့်လိုက်တုံ့",
 "02": "ကျောက်ဆူးမဲ့ နူးညံ့သောနှလုံး စိတ်အတက်အကျ ဆုံးဖြတ်ရခက်",
 "20": "အိပ်မက်များ အနှစ်နည်း အပြီးသတ်ရန် တွန်းအားမလုံလောက်",
 "07": "သုညနှင့်ဝန်ထုပ်တွေ့ ကြန့်ကြာသောကာလ — သည်းခံမှုကြီးစွာလို",
 "70": "အချည်းနှီးပင်ပန်းတတ်သောအခါရှိ — အလကားလုပ်မိမည် သတိ",
 "01": "ဟင်းလင်းပေါ် အာဏာ — အစကောင်းသော်လည်း အဆက်မပြတ်ရန် အဖွဲ့လို",
 "10": "သုညနှင့်တွေ့သောခေါင်းဆောင် — ဘဝအဆင့်လိုက်တုံ့ အရန်အစီအစဉ်ထားပါ",
 "03": "သုညနှင့်မီးတွေ့ — ဦးတည်ချက်မဲ့ စိတ်မြန် — အလျင်စလိုဆုံးဖြတ်မှု သတိ",
 "30": "လမ်းခုလတ်မီးငြိမ်း — အစပြင်း အဆုံးအား နည်း — အရှိန်ထိန်းပါ",
 "04": "သုညနှင့်စကားတွေ့ — ပြောများ အနှစ်နည်း — မတည်နိုင်သောကတိ သတိ",
 "40": "အလေးချိန်မဲ့စကား — မေ့လွယ် — ရလဒ်ဖြင့် ယုံကြည်မှုတည်ဆောက်ပါ",
 "05": "သုညနှင့်ပညာတွေ့ — အကြံကောင်းသော်လည်း အကောင်အထည်နည်း — တွန်းအားပေးသူလို",
 "50": "ပညာနှင့်သုညတွေ့ — အသိပညာအဆင်သင့် အခွင့်အလမ်းနှောင်း — အချိန်စောင့်ပါ",
 "08": "သုညနှင့်ရာဟုတွေ့ — အခြေမဲ့စွန့်စား — လွယ်လွယ်ရ လွယ်လွယ်သွား",
 "80": "ရာဟုနှင့်သုည — မတည်မြဲသောလာဘ် — ဥစ္စာယိုစိမ့်မှု သတိ",
 "09": "သုညနှင့်ကိတ်တွေ့ — ကုသိုလ်ကာကွယ်သော်လည်း ကိုယ့်ဇွဲဖြင့် ဖြည့်ရမည်",
 "90": "သုညဖြင့်ဆုံးသောဘုန်းကံ — ကံကောင်းသော်လည်း မပေါ့ဆရ",
 "12": "နူးညံ့မှုပါသောခေါင်းဆောင် — အပြင်မာ အတွင်းနူး — နှလုံးသားဖြင့်အုပ်ချုပ် လူချစ်",
 "21": "နူးညံ့မှုက ခေါင်းဆောင်ကိုမြှင့် — ညှိနှိုင်းမှုက တံခါးဖွင့် လူကြီးချစ်",
 "14": "အာဏာနှင့်နှုတ်သတ္တိ — ရှင်းလင်းစွာအမိန့်ပေး ညှိနှိုင်းတော်သော အုပ်ချုပ်သူ",
 "41": "စကားက အာဏာကိုထောက် — ပြောလျှင်လိုက်နာ ယုံကြည်ခံရ",
 "16": "ဆွဲဆောင်မှုရှိသောခေါင်းဆောင် — ချစ်ခင်လိုက်နာခံရ ဦးဆောင်ရင်း ရောင်းရင်း ကောင်း",
 "61": "ဆွဲဆောင်မှုက ခေါင်းဆောင်မှုကိုမြှင့် — ဂုဏ်သတင်းနှင့်အတူ ငွေကြေးတိုး",
 "18": "အာဏာနှင့်ရာဟု — သြဇာပြင်း မြန်မြန်တက် ရန်သူများ — အာဏာကို သတိဖြင့်သုံးပါ",
 "81": "ရာဟုက အာဏာကိုထောက် — ထိပ်ဆုံးထိ ရဲရင့် — မြင့်မြင့်တက် ပြင်းပြင်းကျ",
 "19": "ဘုန်းကံပါသောခေါင်းဆောင် — တည်ငြိမ်စွာတိုးတက် လေးစားခံရ အုပ်ချုပ်ရေးကောင်း",
 "91": "ဘုန်းကံက ခေါင်းဆောင်ကိုမြှင့် — အောင်မြင်မှုမြင့် လူကြီးက လမ်းဖွင့်ပေးမြဲ",
 "23": "နူးညံ့မှုနှင့်မီးတွေ့ — စိတ်အတက်အကျမြန် — အနီးကပ်လူနှင့် ပဋိပက္ခ သတိ",
 "32": "နုနယ်သောနှလုံးပေါ်မီး — အပြင်ရဲ အတွင်းနု — အားပေးမှုပိုလို",
 "25": "လ–ကြာသပတေး ရန်တွဲ — နူးညံ့မှုနှင့် မူဝါဒ ထိပ်တိုက် — လူကြီးနှင့် သဘောကွဲ သတိ",
 "52": "မူက နူးညံ့မှုကိုဖိ — တွေးလွန်း စိတ်ဖိစီး — စိတ်ဟန်ချက်ရှာပါ",
 "26": "နူးညံ့မှုနှင့်ဆွဲဆောင်မှု — ယဉ်ကျေးချဉ်းကပ်လွယ် — ဝန်ဆောင်မှု အနုပညာ အလှ ကောင်း",
 "62": "ဆွဲဆောင်မှုနှင့်နူးညံ့မှု — လူချစ်ခံရ — လူတွေ့အလုပ်တိုင်း သင့်",
 "29": "လနှင့်ကိတ် — အာရုံထက် အိပ်မက်မှန် စိတ်ငြိမ် ကုသိုလ်ဟောင်းထောက်",
 "92": "ကိတ်က လကိုမြှင့် — ဘုန်းပါသောဆွဲဆောင်မှု — ကူညီသူပေါ်လာမြဲ",
 "35": "မူပေါ်ရဲရင့်လုပ် — ပညာပါသောတိုက်ခိုက်သူ — လူကြီးအမြင်ကျ တိုးမြှင့်ပေး",
 "53": "ပညာက သတ္တိကိုဦးဆောင် — ထက်မြက်ကျိုးကြောင်းညီသော ဆုံးဖြတ်ချက် — ဥပဒေလမ်းသင့်",
 "36": "အင်္ဂါ–သောကြာ မိတ်တွဲ — ရဲရင့်ပြီးဆွဲဆောင် — တက်ကြွသောအရောင်း ကောင်းစား",
 "63": "ဆွဲဆောင်မှုက သတ္တိကိုထောက် — ယုံကြည်စွာရောင်း — အရောင်းပိတ်မြန်",
 "37": "အင်္ဂါ–စနေ ရန်တွဲ — စိတ်မြန်မှုက အခက်ဖန် — အလုပ်ကြမ်းထပ် — ဒဏ်ရာ သတိ",
 "73": "စနေက မီးကိုဖိ — ပင်ပန်းလျက် ဆက်တိုက်ရ — ခံနိုင်ရည် အစွမ်းကုန်စမ်းခံရ",
 "38": "မီးနှင့်ရာဟု — အားနှင့်အားဆုံ — အစွန်းရောက်စွန့်စား — မြန်မြန်ရ မြန်မြန်ရှုံး — သတိသာလျှင်ကယ်",
 "83": "ရာဟုက မီးမွှေး — အရေးကြုံလျှင် အားကိုးရ — အလျင်စလိုက အကြီးဖျက်တတ်",
 "39": "မီးနှင့်ကိတ် — ကုသိုလ်အောက်က သတ္တိ — အခက်ကျော်ပြီး အောင်မြင်",
 "93": "ကိတ်က မီးကိုထိန်း — အားမှန်လမ်းမှန် — ရဲရင့်လျက်သတိရှိ — သူများထက်မြန်မြန်အောင်",
 "47": "စကားနှင့်စနေတွေ့ — ညှိနှိုင်းမှု ကြန့်ကြာပင်ပန်း — သဘောတူညီချက်တိုင်း စာချုပ်လုပ်ပါ",
 "74": "စနေက စကားကိုဖိ — ဖိစီးချိန် စကားမှား သတိ",
 "48": "စကားနှင့်ရာဟု — စွန့်စားမှုအကြောင်း ပြောတော် — ရဲရင့်သောအရောင်းသမား — လွန်ကဲသောစကား သတိ",
 "84": "ရာဟုက စကားကိုမြှင့် — လူအုပ်ကို ဆွဲဆောင်နိုင် — လှည့်စားခြင်းနှင့် နယ်နိမိတ် သတိ",
 "49": "စကားနှင့်ကိတ် — မန္တန်ပါသောစကား — မွေးရာပါဆရာ နှုတ်ရည်ရှင်",
 "94": "ကိတ်က စကားကိုထောက် — သင်ကြားပို့ချ ထူးချွန် — ကုသိုလ်က စကားမှတဆင့်စီး",
 "57": "ပညာနှင့်စနေတွေ့ — နက်နဲသေချာသော်လည်း နှေး — တည်ငြိမ်စွာ အောင်မြင်",
 "75": "စနေက ပညာကိုမှည့် — ဒုက္ခမှသင်ယူ — အတွေ့အကြုံရင့်ကျက်",
 "58": "ပညာနှင့်ရာဟု — စွန့်စားမှုကို နားလည် — ဘဏ္ဍာရေး အာမခံ စီးပွားဥပဒေ သင့်",
 "85": "ပညာအောက်ကရာဟု — တွက်ချက်ပြီးမှစွန့်စား — စစ်မှန်သော ရင်းနှီးမြှုပ်နှံသူ",
 "67": "သောကြာ–စနေ ရန်တွဲ — အချစ်ရေးအခက် — လှပသောငွေကို ပင်ပန်းမှုဖြင့်လဲ",
 "76": "စနေက ဆွဲဆောင်မှုကိုဖိ — ပင်ပန်းမှုပေါ်က အလှ — အချစ် သက်သေပြရ",
 "68": "ဆွဲဆောင်မှုနှင့်ရာဟု — ရဲရင့်မှုမှ ငွေကြီးရ — ညလူမှုရေး — ချစ်ရေးပေါ့ပျက် သတိ",
 "86": "ရာဟုက ဆွဲဆောင်မှုကိုချဲ့ — ဥစ္စာနှင့်လူကို ပြင်းစွာဆွဲ — လောဘကြီး သတိ",
 "79": "စနေနှင့်ကိတ် — သည်းခံလျှင် ကုသိုလ်ပို့ — ဒုက္ခကုန် အလင်းတွေ့ — ဘဝနှောင်းပိုင်းတောက်ပ",
 "97": "ကိတ်က စနေထက် — ကုသိုလ်က ဝန်ပေါ့စေ — ဇွဲကို လူမြင်တန်ဖိုးထား",
},
}

_CONNECT = {"en": ["moreover", "at the same time", "in addition", "and"],
            "mm": ["ထို့အပြင်", "တစ်ချိန်တည်းတွင်", "ထပ်မံ၍", "နှင့်"]}
ASPECT_HEAD = {
    "en": {"money": "Finances:", "work": "Career:", "love": "Love:", "char": "Character:", "health": "Health:"},
    "mm": {"money": "ငွေကြေး —", "work": "အလုပ် —", "love": "အချစ်ရေး —", "char": "စရိုက် —", "health": "ကျန်းမာရေး —"},
}
_NEG_TAIL = {
    "en": "This pair drags the number's energy down. If keeping this number, make merit regularly, stay mindful about money and relationships, or consider a number without this pair near the end.",
    "mm": "ဤဂဏန်းတွဲသည် နံပါတ်၏စွမ်းအားကို လျော့စေသည်။ ဆက်သုံးမည်ဆိုပါက ကုသိုလ်မှန်မှန်ပြု၍ ငွေနှင့်ဆက်ဆံရေးတွင် သတိထားပါ သို့မဟုတ် နောက်ဆုံးပိုင်းတွင် ဤတွဲမပါသော နံပါတ်ရွေးပါ။",
}
_MID_TAIL = {
    "en": "Overall a neutral pair — it neither drags nor lifts strongly; other pairs in the number carry the result.",
    "mm": "ခြုံငုံ၍ ကြားနေတွဲဖြစ်သည် — ကောင်းကျိုးဆိုးကျိုး မထင်ရှား၊ အခြားတွဲများက အဓိကဆုံးဖြတ်သည်။",
}


def star_name(digit: str, lang: str) -> str:
    return STAR[str(digit)][lang]


def pair_title_i18n(pair: str, lang: str) -> str:
    if lang == "th":
        return pair_meaning(pair)["title"]
    return f"{star_name(pair[0], lang)}–{star_name(pair[1], lang)}"


def pair_desc_i18n(pair: str, lang: str) -> str:
    if lang == "th":
        return pair_meaning(pair)["desc"]
    if pair in SPECIAL_TR[lang]:
        return SPECIAL_TR[lang][pair]
    a, b = pair[0], pair[1]
    da, db = DIGIT_TR[lang][a], DIGIT_TR[lang][b]
    if a == b:
        return {"en": f"Double {star_name(a,lang)} — {da['trait']} intensified",
                "mm": f"{star_name(a,lang)} နှစ်ဆ — {da['trait']} ပိုပြင်းထန်"}[lang]
    joiner = {"en": " combined with ", "mm": " နှင့် "}[lang]
    return da["trait"] + joiner + db["trait"]


def pair_paragraph_i18n(pair: str, power: int, lang: str) -> str:
    if lang == "th":
        return pair_paragraph(pair, power)
    a, b = pair[0], pair[1]
    da, db = DIGIT_TR[lang][a], DIGIT_TR[lang][b]
    H = ASPECT_HEAD[lang]
    same = (a == b)
    intro = {"en": f"Influence of pair {pair} ({pair_title_i18n(pair,lang)}) — {pair_desc_i18n(pair,lang)}.",
             "mm": f"ဂဏန်းတွဲ {pair} ({pair_title_i18n(pair,lang)}) ၏ သြဇာ — {pair_desc_i18n(pair,lang)}။"}[lang]

    def fuse(key):
        if same:
            return f"{H[key]} {da[key]}"
        c = _CONNECT[lang][hash(pair + key) % len(_CONNECT[lang])]
        return f"{H[key]} {da[key]}, {c} {db[key]}"

    parts = [intro]
    if power >= 2:
        parts += [fuse("money"), fuse("work"), fuse("love"), fuse("char"), fuse("health")]
    elif power >= 0:
        parts += [fuse("money"), fuse("work"), fuse("char"), _MID_TAIL[lang]]
    else:
        warn = {"en": "Special caution:", "mm": "အထူးသတိပြုရန် —"}[lang]
        parts += [f"{warn} {fuse('money')}", fuse("love"), fuse("health"), _NEG_TAIL[lang]]
    sep = {"en": " ", "mm": " "}[lang]
    return sep.join(parts)


# ---------------- วันเกิด 8 วัน ----------------
DAYS_TR = {
"en": {
 "sun":    {"name": "Sunday", "animal": "Garuda", "dir": "Northeast", "trait": "leader, ambitious, generous, proud"},
 "mon":    {"name": "Monday", "animal": "Tiger", "dir": "East", "trait": "gentle, calm, thoughtful, softly charming"},
 "tue":    {"name": "Tuesday", "animal": "Lion", "dir": "Southeast", "trait": "brave, honest, high energy, hot-tempered"},
 "wed_am": {"name": "Wednesday morning", "animal": "Tusked elephant", "dir": "South", "trait": "clever, articulate, cheerful, adaptable"},
 "wed_pm": {"name": "Wednesday afternoon (Yahu)", "animal": "Tuskless elephant", "dir": "Northwest", "trait": "daring, influential, strong destiny, bold"},
 "thu":    {"name": "Thursday", "animal": "Rat", "dir": "West", "trait": "wise, virtuous, favored by elders, trustworthy"},
 "fri":    {"name": "Friday", "animal": "Guinea pig", "dir": "North", "trait": "charming, artistic, good with money, loves beauty"},
 "sat":    {"name": "Saturday", "animal": "Naga", "dir": "Southwest", "trait": "patient, steadfast, serious, a fighter"},
},
"mm": {
 "sun":    {"name": "တနင်္ဂနွေနေ့", "animal": "ဂဠုန်", "dir": "အရှေ့မြောက်", "trait": "ခေါင်းဆောင်၊ ရည်မှန်းချက်ကြီး၊ ရက်ရော၊ ဂုဏ်မြတ်နိုး"},
 "mon":    {"name": "တနင်္လာနေ့", "animal": "ကျား", "dir": "အရှေ့", "trait": "နူးညံ့၊ စိတ်အေး၊ တွေးခေါ်တတ်၊ သိမ်မွေ့စွာဆွဲဆောင်"},
 "tue":    {"name": "အင်္ဂါနေ့", "animal": "ခြင်္သေ့", "dir": "အရှေ့တောင်", "trait": "ရဲရင့်၊ ရိုးသား၊ စွမ်းအင်မြင့်၊ စိတ်မြန်"},
 "wed_am": {"name": "ဗုဒ္ဓဟူးနေ့ (မနက်)", "animal": "အစွယ်ပါဆင်", "dir": "တောင်", "trait": "ဉာဏ်ကောင်း၊ စကားတော်၊ ပျော်ရွှင်၊ လိုက်လျောညီထွေ"},
 "wed_pm": {"name": "ရာဟုနေ့ (ဗုဒ္ဓဟူးမွန်းလွဲ)", "animal": "အစွယ်မဲ့ဆင်", "dir": "အနောက်မြောက်", "trait": "ရဲစွမ်း၊ သြဇာရှိ၊ ကံကြမ္မာပြင်း၊ ရဲရင့်"},
 "thu":    {"name": "ကြာသပတေးနေ့", "animal": "ကြွက်", "dir": "အနောက်", "trait": "ပညာရှိ၊ ကိုယ်ကျင့်ကောင်း၊ လူကြီးချစ်၊ ယုံကြည်ရ"},
 "fri":    {"name": "သောကြာနေ့", "animal": "ပူး", "dir": "မြောက်", "trait": "ဆွဲဆောင်မှုရှိ၊ အနုပညာဝါသနာပါ၊ ငွေကိုင်တော်၊ အလှချစ်"},
 "sat":    {"name": "စနေနေ့", "animal": "နဂါး", "dir": "အနောက်တောင်", "trait": "သည်းခံ၊ တည်ကြည်၊ လေးနက်၊ တိုက်ပွဲဝင်"},
},
}

# ---------------- เรือนมหาโพติ ----------------
HOUSES_TR = {
"en": [
 ("Impermanence", "burden", "early life shifts often; constant adaptation"),
 ("Extremity", "burden", "life swings high and low; balance must be kept"),
 ("Fame", "favorable", "renown and honor; widely recognized and respected"),
 ("Wealth", "favorable", "possesses riches; earns well; secure standing"),
 ("Kingly Position", "favorable", "power and prestige; high position; commands respect"),
 ("Sickly", "burden", "health needs special care; vitality gets drained"),
 ("Leader", "favorable", "born to lead; outstanding leadership"),
],
"mm": [
 ("အနိစ္စနေရာ", "ဝန်ထုပ်", "ဘဝအစောပိုင်း ပြောင်းလဲမှုများ လိုက်လျောညီထွေမှုလို"),
 ("အစွန်းရောက်နေရာ", "ဝန်ထုပ်", "ဘဝအတက်အကျ ပြင်းထန် ဟန်ချက်ထိန်းရမည်"),
 ("ကျော်စောခြင်းနေရာ", "ကောင်း", "ဂုဏ်သတင်းကျော်စော လူများလေးစား"),
 ("ဥစ္စာနေရာ", "ကောင်း", "ဥစ္စာဓနပြည့်စုံ ရှာဖွေတော် တည်ငြိမ်"),
 ("မင်းစည်းစိမ်နေရာ", "ကောင်း", "အာဏာနှင့်ဂုဏ် ရာထူးမြင့် လေးစားခံရ"),
 ("ရောဂါနေရာ", "ဝန်ထုပ်", "ကျန်းမာရေး အထူးဂရုစိုက်ရ ခွန်အားဆုတ်တတ်"),
 ("ခေါင်းဆောင်နေရာ", "ကောင်း", "မွေးရာပါခေါင်းဆောင် ထူးချွန်သောဦးဆောင်မှု"),
],
}

# ---------------- เกรด/คำตัดสิน ----------------
GRADE_TR = {
    "en": {"ดีมาก": "Excellent", "ดี": "Good", "ดีพอใช้": "Fair-Good", "พอใช้": "Fair", "ไม่ดี": "Poor", "เสีย": "Bad"},
    "mm": {"ดีมาก": "အလွန်ကောင်း", "ดี": "ကောင်း", "ดีพอใช้": "သင့်တင့်ကောင်း", "พอใช้": "အသင့်အတင့်", "ไม่ดี": "မကောင်း", "เสีย": "ဆိုး"},
}
COMPAT_VERDICT = {
    "th": [(75, "เข้ากันดีมาก — เบอร์นี้หนุนดวงวันเกิดของคุณ"), (55, "เข้ากันดี — ส่งเสริมกันเป็นส่วนใหญ่"),
           (40, "พอใช้ — ไม่หนุนไม่ฉุดชัดเจน"), (-1, "ควรระวัง — มีเลขที่เป็นศัตรูกับดาววันเกิดหลายตำแหน่ง")],
    "en": [(75, "Excellent match — this number strengthens your birth-day fortune"), (55, "Good match — mostly supportive"),
           (40, "Fair — neither boosts nor drags clearly"), (-1, "Caution — several digits are enemies of your birth star")],
    "mm": [(75, "အလွန်ကိုက်ညီ — ဤနံပါတ်သည် သင့်မွေးနေ့ကံကို အားဖြည့်သည်"), (55, "ကောင်းစွာကိုက်ညီ — အများအားဖြင့် ထောက်ပံ့သည်"),
           (40, "အသင့်အတင့် — ထူးထူးခြားခြား မကောင်းမဆိုး"), (-1, "သတိ — မွေးနေ့ဂြိုဟ်နှင့် ရန်ဖြစ်သောဂဏန်း များနေသည်")],
}
COUPLE_TONE = {
    "en": {"ดีมาก": "Excellent", "ดี": "Good", "กลาง": "Neutral", "ระวัง": "Caution"},
    "mm": {"ดีมาก": "အလွန်ကောင်း", "ดี": "ကောင်း", "กลาง": "ကြားနေ", "ระวัง": "သတိ"},
}
COUPLE_TEXT = {
    "en": {"มิตร": "{p1} and {p2} are friendly stars — they naturally strengthen each other",
           "เสริม": "Born on the same day ({d}) — easy mutual understanding, similar natures",
           "ศัตรู": "{p1} and {p2} are enemy stars in traditional lore — mutual understanding is needed",
           "กลาง": "{p1} and {p2} are neutral to each other — a smooth coexistence",
           "clash": "A clashing pair per Myanmar marriage tradition — extra patience and merit-making together are advised"},
    "mm": {"มิตร": "{p1} နှင့် {p2} သည် မိတ်ဂြိုဟ်ချင်း — သဘာဝအတိုင်း အားဖြည့်ပေးကြသည်",
           "เสริม": "နေ့တူမွေး ({d}) — အပြန်အလှန် နားလည်လွယ် စရိုက်တူ",
           "ศัตรู": "{p1} နှင့် {p2} သည် ရိုးရာကျမ်းအရ ရန်ဂြိုဟ်ချင်း — နားလည်မှု လိုအပ်သည်",
           "กลาง": "{p1} နှင့် {p2} ကြားနေ — အေးချမ်းစွာ အတူနေနိုင်",
           "clash": "မြန်မာ့ထုံးတမ်းအရ မတည့်သောစုံတွဲ — သည်းခံမှုနှင့် အတူကုသိုလ်ပြုမှု လိုအပ်သည်"},
}

# ---------------- ผลรวม/นวิน ----------------
SUM_TONE_TEXT = {
    "en": {"ดี": "A highly auspicious sum — promotes all-round success and prosperity",
           "ระวัง": "A cautionary sum — stay mindful; strengthen with merit and good digit pairs",
           "กลาง": "A neutral sum — neither lifts nor drags; its energy follows the ruling star"},
    "mm": {"ดี": "အလွန်မင်္ဂလာရှိသော ပေါင်းလဒ် — ဘက်စုံအောင်မြင်ကြီးပွားစေသည်",
           "ระวัง": "သတိပြုရမည့် ပေါင်းလဒ် — ကုသိုလ်နှင့် ဂဏန်းတွဲကောင်းဖြင့် အားဖြည့်ပါ",
           "กลาง": "ကြားနေပေါင်းလဒ် — အုပ်စိုးဂြိုဟ်၏ စွမ်းအားအတိုင်း သွားသည်"},
}
NAWIN_TEXT = {
    "en": {"n4": "Contains {n} nines — 'Konawin' at full strength: per Myanmar belief, 9 embodies the Nine Attributes of the Buddha; the more nines, the greater the success and protection",
           "n2": "Contains {n} nines — Nawin power (the Nine Attributes of the Buddha) supports prosperity per Myanmar belief",
           "999": "Contains the 999 sequence — Myanmar's most coveted lucky pattern, boosting both fortune and the number's value",
           "div9": "Digit sum {t} is divisible by 9 — 'complete Nawin power': the whole number is governed by 9",
           "37": "Contains 37 — matching the 37 Great Nats revered in Myanmar; believed to carry local guardian protection",
           "none": "No prominent Nawin marks — the number's power rests mainly on its digit-pair structure"},
    "mm": {"n4": "ဂဏန်း ၉ — {n} လုံးပါ — 'ကိုးနဝင်း' အပြည့်အဝ — ၉ သည် ဗုဒ္ဓဂုဏ်တော်ကိုးပါးကို ကိုယ်စားပြုပြီး များလေ အောင်မြင်ကာကွယ်မှု ကြီးလေ",
           "n2": "ဂဏန်း ၉ — {n} လုံးပါ — နဝင်းစွမ်းအား (ဗုဒ္ဓဂုဏ်တော်ကိုးပါး) က ကြီးပွားမှုကို ထောက်ပံ့သည်",
           "999": "၉၉၉ တွဲပါ — မြန်မာတွင် အလိုအရှိဆုံး မင်္ဂလာပုံစံ ကံနှင့်တန်ဖိုး နှစ်မျိုးလုံးမြှင့်",
           "div9": "ပေါင်းလဒ် {t} ကို ၉ ဖြင့် စားလို့ပြတ် — 'နဝင်းအပြည့်' နံပါတ်တစ်ခုလုံး ၉ အုပ်စိုးသည်",
           "37": "၃၇ ပါဝင် — မြန်မာတို့ကိုးကွယ်သော နတ်ကြီး ၃၇ ပါးနှင့် ကိုက်ညီ ဒေသစောင့်နတ် ကာကွယ်မှုရှိသည်ဟု ယုံကြည်",
           "none": "ထင်ရှားသော နဝင်းအမှတ်အသား မပါ — နံပါတ်၏စွမ်းအားသည် ဂဏန်းတွဲဖွဲ့စည်းပုံပေါ် အဓိကတည်သည်"},
}

# ---------------- อาชีพ ----------------
CAREER_TR = {
"en": {"1": "management, leadership, business ownership, government",
       "2": "coordination, service, interpreting, diplomacy, crafts",
       "3": "military, police, sports, engineering, trades, challenging work",
       "4": "trade, marketing, sales, media, online business",
       "5": "teaching, academia, law, consulting, medicine, roles of trust",
       "6": "finance & investment, art, entertainment, beauty, luxury goods, restaurants",
       "7": "real estate, land, factories, agriculture, endurance work",
       "8": "international business, high-risk investment, night business, logistics",
       "9": "merit-related work, teaching, international work, technology, roles of influence", "0": ""},
"mm": {"1": "စီမံခန့်ခွဲမှု၊ ခေါင်းဆောင်မှု၊ ကိုယ်ပိုင်စီးပွား၊ အစိုးရလုပ်ငန်း",
       "2": "ညှိနှိုင်းရေး၊ ဝန်ဆောင်မှု၊ စကားပြန်၊ သံတမန်၊ လက်မှုပညာ",
       "3": "စစ်၊ ရဲ၊ အားကစား၊ အင်ဂျင်နီယာ၊ လက်မှု၊ စိန်ခေါ်မှုရှိသောအလုပ်",
       "4": "ကုန်သွယ်ရေး၊ စျေးကွက်၊ အရောင်း၊ မီဒီယာ၊ အွန်လိုင်းလုပ်ငန်း",
       "5": "သင်ကြားရေး၊ ပညာရေး၊ ဥပဒေ၊ အတိုင်ပင်ခံ၊ ဆေးပညာ",
       "6": "ငွေကြေးရင်းနှီးမြှုပ်နှံမှု၊ အနုပညာ၊ ဖျော်ဖြေရေး၊ အလှပြင်၊ ဇိမ်ခံပစ္စည်း၊ စားသောက်ဆိုင်",
       "7": "အိမ်ခြံမြေ၊ စက်ရုံ၊ လယ်ယာ၊ ခံနိုင်ရည်လိုသောအလုပ်",
       "8": "နိုင်ငံရပ်ခြားစီးပွား၊ စွန့်စားရင်းနှီးမြှုပ်နှံမှု၊ ညလုပ်ငန်း၊ ထောက်ပံ့ပို့ဆောင်ရေး",
       "9": "ကုသိုလ်ရေးရာ၊ ဆရာ၊ နိုင်ငံရပ်ခြားလုပ်ငန်း၊ နည်းပညာ၊ သြဇာသုံးအလုပ်", "0": ""},
}

# ---------------- ยะดะยา ----------------
YADAYA_TR = {
"en": ["Make merit at the {dir} corner of the pagoda (the {day} planetary post); pour water over the day's Buddha image {k} times",
       "Release {k} fish or birds (per the {planet} star strength) or 9 per the Konawin custom",
       "Offer 9 candles and 9 flowers per Myanmar's Nine-Gods (Phaya Kozu) tradition",
       "Recite the Nine Attributes of the Buddha (Itipiso) 9 times before first using the number",
       "Start using the number on a Yatyaza (auspicious) day; avoid Pyathada days"],
"mm": ["ဘုရားရင်ပြင် {dir} ထောင့် ({day} ဂြိုဟ်တိုင်) တွင် ကုသိုလ်ပြု၍ နေ့နံဘုရားကို ရေ {k} ခွက် သွန်းလောင်းပါ",
       "ငါး သို့မဟုတ် ငှက် {k} ကောင် ({planet} ဂြိုဟ်သက်အလိုက်) သို့မဟုတ် ကိုးနဝင်းအလိုက် ၉ ကောင် လွှတ်ပါ",
       "ဖယောင်းတိုင် ၉ တိုင် ပန်း ၉ ပွင့် — ဘုရားကိုးဆူထုံးတမ်းအတိုင်း ပူဇော်ပါ",
       "နံပါတ်မစသုံးမီ ဣတိပိသော ဂုဏ်တော် ၉ ကြိမ် ရွတ်ဆိုပါ",
       "ရက်ရာဇာနေ့တွင် စတင်သုံးပါ — ပြဿဒါးနေ့ ရှောင်ပါ"],
}

# ---------------- ปฏิทิน/ฤกษ์ ----------------
WEEKDAY_TR = {
    "th": ["เสาร์", "อาทิตย์", "จันทร์", "อังคาร", "พุธ", "พฤหัสบดี", "ศุกร์"],
    "en": ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
    "mm": ["စနေ", "တနင်္ဂနွေ", "တနင်္လာ", "အင်္ဂါ", "ဗုဒ္ဓဟူး", "ကြာသပတေး", "သောကြာ"],
}
MONTH_TR = {
    "en": {0: "1st Waso", 1: "Tagu", 2: "Kason", 3: "Nayon", 4: "Waso", 5: "Wagaung", 6: "Tawthalin",
           7: "Thadingyut", 8: "Tazaungmon", 9: "Nadaw", 10: "Pyatho", 11: "Tabodwe", 12: "Tabaung",
           13: "Late Tagu", 14: "Late Kason"},
    "mm": {0: "ပဝါဆို", 1: "တန်ခူး", 2: "ကဆုန်", 3: "နယုန်", 4: "ဝါဆို", 5: "ဝါခေါင်", 6: "တော်သလင်း",
           7: "သီတင်းကျွတ်", 8: "တန်ဆောင်မုန်း", 9: "နတ်တော်", 10: "ပြာသို", 11: "တပို့တွဲ", 12: "တပေါင်း",
           13: "နှောင်းတန်ခူး", 14: "နှောင်းကဆုန်"},
}
ASTRO_VERDICT = {
    "th": {"yat": "ยัตยาซา — วันมงคล เหมาะเริ่มสิ่งใหม่/เปิดเบอร์", "pya": "เปียตะดา — วันอัปมงคล ควรเลี่ยงเริ่มการใหญ่",
           "pya2": "เปียตะดาช่วงบ่าย — เช้าใช้ได้ เลี่ยงช่วงบ่าย", "norm": "วันปกติ"},
    "en": {"yat": "Yatyaza — auspicious; ideal for new beginnings/activation", "pya": "Pyathada — inauspicious; avoid major starts",
           "pya2": "Afternoon Pyathada — morning is fine, avoid the afternoon", "norm": "Ordinary day"},
    "mm": {"yat": "ရက်ရာဇာ — မင်္ဂလာနေ့ အသစ်စတင်ရန်ကောင်း", "pya": "ပြဿဒါး — မကောင်းသောနေ့ အကြီးအကျယ်မစသင့်",
           "pya2": "မွန်းလွဲပြဿဒါး — မနက်ရ၏ မွန်းလွဲရှောင်ပါ", "norm": "သာမန်နေ့"},
}
RELATION_TR = {
    "en": {"มิตร": "friend", "เสริม": "self", "ศัตรู": "enemy", "กลาง": "neutral", "นวิน": "nawin", "สูญ": "void"},
    "mm": {"มิตร": "မိတ်", "เสริม": "ကိုယ်", "ศัตรู": "ရန်", "กลาง": "ကြားနေ", "นวิน": "နဝင်း", "สูญ": "သုည"},
}
MB_CROSS = {
    "en": {"pos": "Digit {d} ({planet}) prominent ×{n} — sits in your 'House {no} {house}', a favorable house in your chart → this number feeds that strength: {desc}",
           "neg": "Digit {d} ({planet}) prominent ×{n} — sits in your 'House {no} {house}', a burden house → the number stirs this area; stay mindful and support it with birth-day merit",
           "r8": "Digit 8 (Rahu) prominent ×{n} — Rahu stands above the 7 houses, granting influence, boldness and sudden windfalls; requires mindfulness",
           "r9": "Digit 9 (Ketu/Nawin) prominent ×{n} — merit-power above the chart, supporting every house per the Konawin belief"},
    "mm": {"pos": "ဂဏန်း {d} ({planet}) ထင်ရှား ×{n} — သင့် 'အိမ် {no} {house}' (ကောင်းသောအိမ်) တွင်တည် → ထိုအားကို ဖြည့်ပေးသည် — {desc}",
           "neg": "ဂဏန်း {d} ({planet}) ထင်ရှား ×{n} — သင့် 'အိမ် {no} {house}' (ဝန်ထုပ်အိမ်) တွင်တည် → ဤကဏ္ဍကို လှုံ့ဆော်သည် သတိထား၍ မွေးနေ့ကုသိုလ်ဖြင့် ထောက်ပံ့ပါ",
           "r8": "ဂဏန်း ၈ (ရာဟု) ထင်ရှား ×{n} — ရာဟုသည် အိမ် ၇ လုံးအထက်တည် သြဇာ ရဲစွမ်းနှင့် ရုတ်တရက်လာဘ် ပေး — သတိလို",
           "r9": "ဂဏန်း ၉ (ကိတ်/နဝင်း) ထင်ရှား ×{n} — ဇယားထက် ကုသိုလ်စွမ်းအား — ကိုးနဝင်းအယူအရ အိမ်အားလုံးကို ထောက်ပံ့သည်"},
}


# ---------------- บทสรุปความเข้ากันแบบละเอียด (5 ปัจจัย) ----------------
BREAKDOWN_UI = {
    "th": {"head": "📊 บทสรุปความเข้ากันแบบละเอียด", "factor": "ปัจจัย", "score": "คะแนน", "weight": "น้ำหนัก",
           "overall": "รวมทุกปัจจัย", "src_mm": "ศาสตร์พม่า", "src_in": "ศาสตร์อินเดีย",
           "verdict_top": "จุดที่หนุนแรงที่สุด", "verdict_low": "จุดที่ควรรู้"},
    "en": {"head": "📊 Detailed Compatibility Summary", "factor": "Factor", "score": "Score", "weight": "Weight",
           "overall": "Overall (all factors)", "src_mm": "Myanmar system", "src_in": "Indian system",
           "verdict_top": "Strongest support", "verdict_low": "Worth knowing"},
    "mm": {"head": "📊 ကိုက်ညီမှု အသေးစိတ်အနှစ်ချုပ်", "factor": "အချက်", "score": "ရမှတ်", "weight": "အလေးချိန်",
           "overall": "စုစုပေါင်း (အချက်အားလုံး)", "src_mm": "မြန်မာ့ပညာ", "src_in": "အိန္ဒိယပညာ",
           "verdict_top": "အားအကောင်းဆုံးအချက်", "verdict_low": "သိထားသင့်သည့်အချက်"},
}
FACTOR_NAME = {
    "th": {"digits": "ความสัมพันธ์รายหลัก (ดาววันเกิด × เลขทุกตัว ถ่วงตามตำแหน่ง)",
           "tail": "เลขท้ายเบอร์ (ชะตาหลัก) × ดาววันเกิด",
           "nawin": "พลังนวิน — จำนวนเลข 9 ในเบอร์",
           "sum": "ผลรวมเบอร์ × เลขวันเกิด (Mulank)",
           "mahabote": "ดาวเด่นของเบอร์ × ผังมหาโพติของคุณ"},
    "en": {"digits": "Digit-by-digit relation (birth star × every digit, position-weighted)",
           "tail": "Final digit (main destiny) × birth star",
           "nawin": "Nawin power — count of 9s in the number",
           "sum": "Number sum × birth-date number (Mulank)",
           "mahabote": "The number's dominant stars × your Mahabote chart"},
    "mm": {"digits": "ဂဏန်းတစ်လုံးချင်း ဆက်နွယ်မှု (မွေးနေ့ဂြိုဟ် × ဂဏန်းတိုင်း၊ နေရာအလိုက်)",
           "tail": "နောက်ဆုံးဂဏန်း (အဓိကကံ) × မွေးနေ့ဂြိုဟ်",
           "nawin": "နဝင်းစွမ်းအား — နံပါတ်ထဲက ၉ အရေအတွက်",
           "sum": "ဂဏန်းပေါင်းလဒ် × မွေးရက်ဂဏန်း (Mulank)",
           "mahabote": "နံပါတ်၏ထင်ရှားဂြိုဟ်များ × သင့်မဟာဘုတ်ဇယား"},
}
_REL_WORD = {
    "th": {"มิตร": "ดาวคู่มิตร", "เสริม": "ดาวเดียวกับวันเกิด", "นวิน": "เลข 9 (นวิน)",
           "กลาง": "เป็นกลาง", "สูญ": "เลข 0 (สูญ)", "ศัตรู": "ดาวคู่ศัตรู"},
    "en": {"มิตร": "a friendly star", "เสริม": "the same star as your birth day", "นวิน": "the 9 (Nawin)",
           "กลาง": "neutral", "สูญ": "a 0 (void)", "ศัตรู": "an enemy star"},
    "mm": {"มิตร": "မိတ်ဂြိုဟ်", "เสริม": "မွေးနေ့ဂြိုဟ်နှင့်တူ", "นวิน": "၉ (နဝင်း)",
           "กลาง": "ကြားနေ", "สูญ": "၀ (သုည)", "ศัตรู": "ရန်ဂြိုဟ်"},
}


def factor_comment(f: dict, lang: str, star_fn) -> str:
    """ประโยคอธิบายของแต่ละปัจจัย"""
    k, d = f["key"], f["data"]
    if k == "digits":
        good = sum(1 for x in d["detail"] if x["relation"] in ("มิตร", "เสริม", "นวิน"))
        bad = sum(1 for x in d["detail"] if x["relation"] == "ศัตรู")
        tot = len(d["detail"])
        return {"th": f"ใน {tot} หลัก มีเลขที่หนุนดวงวันเกิด {good} หลัก" + (f" และเลขศัตรู {bad} หลัก" if bad else " ไม่มีเลขศัตรูเลย"),
                "en": f"Of {tot} digits, {good} support your birth star" + (f" and {bad} are enemy digits" if bad else " with no enemy digits at all"),
                "mm": f"ဂဏန်း {tot} လုံးတွင် {good} လုံးက မွေးနေ့ကံကို ထောက်ပံ့ပြီး" + (f" ရန်ဂဏန်း {bad} လုံးရှိသည်" if bad else " ရန်ဂဏန်း မရှိပါ")}[lang]
    if k == "tail":
        rel = _REL_WORD[lang][d["rel"]]
        return {"th": f"เลขท้าย {d['tail']} เป็น{rel}ของดาววันเกิด — เลขท้ายคือชะตาหลักของเบอร์ จึงมีน้ำหนักมากเป็นพิเศษ",
                "en": f"The final digit {d['tail']} is {rel} of your birth star — the final digit is the number's main destiny, so it carries extra weight",
                "mm": f"နောက်ဆုံးဂဏန်း {d['tail']} သည် မွေးနေ့ဂြိုဟ်၏ {rel} ဖြစ်သည် — နောက်ဆုံးဂဏန်းသည် နံပါတ်၏အဓိကကံဖြစ်၍ အလေးချိန်ပိုများသည်"}[lang]
    if k == "nawin":
        n = d["nines"]
        if n == 0:
            return {"th": "เบอร์นี้ไม่มีเลข 9 — ไม่ได้พลังนวินเสริม (ไม่ใช่ข้อเสีย แต่ไม่มีโบนัส)",
                    "en": "No 9s in this number — no Nawin boost (not a flaw, just no bonus)",
                    "mm": "ဤနံပါတ်တွင် ၉ မပါ — နဝင်းအားဖြည့် မရ (အပြစ်မဟုတ် ဘောနပ်စ်မရသည်သာ)"}[lang]
        return {"th": f"มีเลข 9 จำนวน {n} ตัว — พลังพุทธคุณ 9 ประการหนุนทุกวันเกิดตามคติพม่า",
                "en": f"Contains {n} nine(s) — the Nine Attributes' power supports every birth day per Myanmar belief",
                "mm": f"၉ ဂဏန်း {n} လုံးပါ — ဗုဒ္ဓဂုဏ်တော်ကိုးပါး စွမ်းအားက မွေးနေ့တိုင်းကို ထောက်ပံ့သည်"}[lang]
    if k == "sum":
        rel = d["rel"]
        base = {"th": f"ผลรวมเบอร์ย่อได้เลข {d['root']} เทียบกับเลขวันเกิด (Mulank) {d['mulank']} ของคุณ",
                "en": f"The number's sum reduces to {d['root']}, checked against your birth-date number (Mulank) {d['mulank']}",
                "mm": f"နံပါတ်ပေါင်းလဒ် {d['root']} ကို သင့်မွေးရက်ဂဏန်း (Mulank) {d['mulank']} နှင့် တိုက်စစ်သည်"}[lang]
        tailtxt = {"ดี": {"th": " — อยู่ในกลุ่มเลขที่ตำราอินเดียถือว่า 'ส่งเสริมกัน'", "en": " — it falls in the 'compatible' set per the Indian school", "mm": " — အိန္ဒိယကျမ်းအရ 'ကိုက်ညီသော' အုပ်စုထဲ ဝင်သည်"},
                   "เลี่ยง": {"th": " — อยู่ในกลุ่มเลขที่ตำราอินเดียแนะนำให้เลี่ยง ควรเสริมด้วยปัจจัยอื่น", "en": " — it falls in the 'avoid' set per the Indian school; other factors should compensate", "mm": " — အိန္ဒိယကျမ်းအရ 'ရှောင်ရန်' အုပ်စုထဲ ဝင်သည် — အခြားအချက်များဖြင့် ဖြည့်သင့်သည်"},
                   "กลาง": {"th": " — เป็นกลาง ไม่หนุนไม่ฉุด", "en": " — neutral, neither boosts nor drags", "mm": " — ကြားနေ မကောင်းမဆိုး"}}[rel][lang]
        return base + tailtxt
    if k == "mahabote":
        p, n = d["pos"], d["neg"]
        return {"th": f"ดาวเด่นของเบอร์ตกเรือนมงคลของคุณ {p} ดวง" + (f" และเรือนภาระ {n} ดวง" if n else " ไม่แตะเรือนภาระเลย"),
                "en": f"The number's dominant stars land in {p} favorable house(s) of your chart" + (f" and {n} burden house(s)" if n else " and touch no burden house"),
                "mm": f"နံပါတ်၏ထင်ရှားဂြိုဟ်များသည် သင့်ဇယား၏ ကောင်းသောအိမ် {p} လုံးတွင် ကျရောက်ပြီး" + (f" ဝန်ထုပ်အိမ် {n} လုံး ထိသည်" if n else " ဝန်ထုပ်အိမ် မထိပါ")}[lang]
    return ""


# ---------------- เบอร์คู่ (number-pair) ----------------
NUMPAIR_UI = {
    "th": {"num2_label": "เบอร์ของคนที่ 2 (ใส่เพื่อเช็คเบอร์คู่กัน)", "head": "🔗 ความเข้ากันของเบอร์ทั้งสองเครื่อง",
           "score": "คะแนนเบอร์คู่", "tail_line": "เลขท้ายเบอร์ (ชะตาหลัก): {a} × {b}",
           "top_line": "ดาวเด่นของสองเบอร์: {a} ({sa}) × {b} ({sb})", "nawin_line": "ทั้งสองเบอร์มีเลข 9 — พลังนวินหนุนทั้งคู่ตามคติพม่า"},
    "en": {"num2_label": "Person 2's phone number (to check the pair of numbers)", "head": "🔗 Harmony Between the Two Numbers",
           "score": "Number-pair score", "tail_line": "Final digits (main destiny): {a} × {b}",
           "top_line": "Dominant stars of the two numbers: {a} ({sa}) × {b} ({sb})", "nawin_line": "Both numbers carry 9s — Nawin power supports the pair per Myanmar belief"},
    "mm": {"num2_label": "ဒုတိယလူ၏ ဖုန်းနံပါတ် (နံပါတ်စုံတွဲစစ်ရန်)", "head": "🔗 နံပါတ်နှစ်ခု ကိုက်ညီမှု",
           "score": "နံပါတ်စုံတွဲရမှတ်", "tail_line": "နောက်ဆုံးဂဏန်း (အဓိကကံ): {a} × {b}",
           "top_line": "နံပါတ်နှစ်ခု၏ ထင်ရှားဂြိုဟ်: {a} ({sa}) × {b} ({sb})", "nawin_line": "နံပါတ်နှစ်ခုစလုံး ၉ ပါ — နဝင်းစွမ်းအားက စုံတွဲကို ထောက်ပံ့သည်"},
}
NUMPAIR_REL = {
    "th": {"มิตร": "ดาวคู่มิตร — สองเบอร์หนุนพลังกัน ✚", "เสริม": "ดาวเดียวกัน — จังหวะชีวิตไปทางเดียวกัน ✚",
           "นวิน": "มีเลข 9 คุม — พลังบุญประสานทุกอย่างให้ราบรื่น ⭐", "กลาง": "เป็นกลางต่อกัน — อยู่ร่วมกันได้ปกติ",
           "สูญ": "มีเลข 0 — พลังเชื่อมโยงกันเบา", "ศัตรู": "ดาวคู่ศัตรู — ใช้คู่กันต้องอาศัยความเข้าใจ ⚠"},
    "en": {"มิตร": "friendly stars — the two numbers empower each other ✚", "เสริม": "same star — life rhythms move in step ✚",
           "นวิน": "governed by 9 — merit smooths everything ⭐", "กลาง": "neutral — coexist normally",
           "สูญ": "a 0 involved — the bond is light", "ศัตรู": "enemy stars — using them as a pair needs understanding ⚠"},
    "mm": {"มิตร": "မိတ်ဂြိုဟ်ချင်း — နံပါတ်နှစ်ခု အားဖြည့်ပေးကြသည် ✚", "เสริม": "ဂြိုဟ်တူ — ဘဝအရှိန်အတူသွား ✚",
           "นวิน": "၉ အုပ်စိုး — ကုသိုလ်စွမ်းအားက အားလုံးချောမွေ့စေ ⭐", "กลาง": "ကြားနေ — ပုံမှန်အတူသုံးနိုင်",
           "สูญ": "၀ ပါဝင် — ချိတ်ဆက်အား ပေါ့", "ศัตรู": "ရန်ဂြိုဟ်ချင်း — အတူသုံးလျှင် နားလည်မှုလို ⚠"},
}
NUMPAIR_VERDICT = {
    "th": [(75, "เบอร์คู่มงคล — สองเบอร์หนุนกันดีมาก เหมาะใช้เป็นคู่"), (55, "เข้ากันดี — ใช้คู่กันได้ราบรื่น"),
           (40, "กลางๆ — ไม่หนุนไม่ฉุด"), (-1, "ควรระวัง — พลังสองเบอร์ขัดกัน แนะนำปรับเบอร์ใดเบอร์หนึ่ง")],
    "en": [(75, "An auspicious pair — the numbers strongly support each other"), (55, "Good match — works smoothly as a pair"),
           (40, "Neutral — neither boosts nor drags"), (-1, "Caution — the numbers clash; consider adjusting one of them")],
    "mm": [(75, "မင်္ဂလာစုံတွဲနံပါတ် — အပြန်အလှန် ကောင်းစွာထောက်ပံ့"), (55, "ကောင်းစွာကိုက်ညီ — စုံတွဲအဖြစ် ချောမွေ့စွာသုံးနိုင်"),
           (40, "ကြားနေ — မကောင်းမဆိုး"), (-1, "သတိ — နံပါတ်နှစ်ခု ဆန့်ကျင်နေ — တစ်ခုကို ပြောင်းရန်စဉ်းစားပါ")],
}


def numpair_verdict(score: float, lang: str) -> str:
    for lo, txt in NUMPAIR_VERDICT[lang]:
        if score >= lo:
            return txt
    return NUMPAIR_VERDICT[lang][-1][1]


def compat_verdict(score: float, lang: str) -> str:
    for lo, txt in COMPAT_VERDICT[lang]:
        if score >= lo:
            return txt
    return COMPAT_VERDICT[lang][-1][1]


def grade_label(th_grade: str, lang: str) -> str:
    return th_grade if lang == "th" else GRADE_TR[lang].get(th_grade, th_grade)


def digit_trait(d: str, lang: str) -> str:
    if lang == "th":
        return DIGIT[d]["trait"]
    return DIGIT_TR[lang][d]["trait"]
