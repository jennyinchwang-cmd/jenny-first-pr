# -*- coding: utf-8 -*-
"""
คลังข้อความดวงคู่หลายศาสตร์ (พม่า/จีน/ไทย/ตะวันตก) — Number Luck
================================================================
3 ภาษา: th / en / mm  (⚠️ ภาษาพม่าผ่านการตรวจรอบแรกโดย Claude Code แล้ว — ควรมี native review อีกชั้นก่อน commercial use ขนาดใหญ่)
ใช้ร่วมกับ couple_rules / burmese_couple / chinese_couple / thai_couple / western_couple
"""

# ============ ชื่อการ์ด ============
CARDS = {
    "burmese": {
        "th": {"head": "🇲🇲 ศาสตร์พม่า", "sub": "โปรไฟล์วันเกิด 8 ภาค · มหาโบติ · นะขัต (ข้อมูลรายบุคคล)"},
        "en": {"head": "🇲🇲 Burmese", "sub": "8-sector birth profile · Mahabote · Nakhat (per-person)"},
        "mm": {"head": "🇲🇲 မြန်မာ့ဗေဒင်", "sub": "မွေးနေ့နံ ၈ ပါး · မဟာဘုတ် · နက္ခတ် (တစ်ဦးချင်းစီ)"},
    },
    "chinese": {
        "th": {"head": "🇨🇳 ศาสตร์จีน", "sub": "ความสัมพันธ์กิ่งดินปีเกิด (ชั้นเร็ว ไม่ใช่ปาจื่อเต็ม)"},
        "en": {"head": "🇨🇳 Chinese", "sub": "Earthly-branch relations (quick view, not full BaZi)"},
        "mm": {"head": "🇨🇳 တရုတ်ဗေဒင်", "sub": "မွေးနှစ် မြေခန်းဆက်စပ်မှု (အမြန်ကြည့်၊ ပါကျီ (八字) အပြည့် မဟုတ်)"},
    },
    "thai": {
        "th": {"head": "🇹🇭 ศาสตร์ไทย", "sub": "ทักษา + คู่มิตร/คู่ศัตรูดาวประจำวัน"},
        "en": {"head": "🇹🇭 Thai", "sub": "Thaksa + day-planet friend/enemy pairs"},
        "mm": {"head": "🇹🇭 ထိုင်းဗေဒင်", "sub": "ထက်ဆာ (ထိုင်း ဘုံ ၈ ခန်း) + မွေးနေ့ဂြိုဟ် မိတ်/ရန်တွဲ"},
    },
    "western": {
        "th": {"head": "🌍 ตะวันตก", "sub": "ราศีอาทิตย์ + ธาตุ + คุณภาพ (มุมมองเร็ว ไม่ใช่ synastry)"},
        "en": {"head": "🌍 Western", "sub": "Sun sign + element + modality (overview, not synastry)"},
        "mm": {"head": "🌍 အနောက်တိုင်း", "sub": "နေရာသီ + ဓာတ် + သဘာဝ (အကျဉ်း၊ synastry မဟုတ်)"},
    },
}

# ============ ป้ายระดับหลักฐาน / ที่มา ============
CONF = {
    "HIGH": {"th": "หลักฐานชัด", "en": "Well-evidenced", "mm": "အထောက်အထား ခိုင်မာ"},
    "MED": {"th": "หลักฐานปานกลาง", "en": "Moderately evidenced", "mm": "အထောက်အထား အလယ်အလတ်"},
    "LOW": {"th": "หลักฐานอ่อน", "en": "Weak evidence", "mm": "အထောက်အထား အားနည်း"},
}
SOURCE_HEAD = {"th": "📎 ที่มาและวิธีคำนวณ", "en": "📎 Source & method", "mm": "📎 ရင်းမြစ်နှင့် တွက်နည်း"}
LIMIT_HEAD = {"th": "⚠️ ข้อจำกัดของชั้นข้อมูลนี้", "en": "⚠️ Limits of this data level", "mm": "⚠️ ဤအဆင့်၏ ကန့်သတ်ချက်များ"}
QUICK_BADGE = {"th": "มุมมองเร็ว", "en": "Quick view", "mm": "အမြန်ကြည့်"}

# ============ ชื่อแหล่งอ้างอิง (แสดงสั้น ๆ) ============
SOURCE_LABEL = {
    "maung_htin_aung_1959": {"th": "Maung Htin Aung (1959)", "en": "Maung Htin Aung (1959)", "mm": "မောင်ထင်အောင် (၁၉၅၉)"},
    "mmcal_mit": {"th": "mmcal — Dr. Yan Naing Aye (MIT)", "en": "mmcal — Dr. Yan Naing Aye (MIT)", "mm": "mmcal — ဒေါက်တာ ရန်နိုင်အေး (MIT)"},
    "sanmingtonghui_juan2": {"th": "《三命通會》卷二", "en": "Sān Mìng Tōng Huì, juàn 2", "mm": "《三命通會》 အတွဲ ၂"},
    "hko_ganzhi": {"th": "หอดูดาวฮ่องกง", "en": "Hong Kong Observatory", "mm": "ဟောင်ကောင် မိုးလေဝသဌာန"},
    "nlt_154": {"th": "หอสมุดแห่งชาติ (ทะเบียน 154)", "en": "National Library of Thailand (no. 154)", "mm": "ထိုင်းအမျိုးသားစာကြည့်တိုက် (နံပါတ် ၁၅၄)"},
    "thaksa_vannavidas": {"th": "ตำราทักษา (วรรณวิทัศน์)", "en": "Thaksa study (Vannavidas)", "mm": "ထက်ဆာ လေ့လာချက် (Vannavidas)"},
    "tropical_zodiac": {"th": "ระบบราศี tropical", "en": "Tropical zodiac", "mm": "Tropical ရာသီခွင်စနစ်"},
}

# ============ ตัวบุคคล ============
PERSON = {"th": {"a": "ฝ่ายแรก", "b": "ฝ่ายที่สอง"}, "en": {"a": "Partner A", "b": "Partner B"},
          "mm": {"a": "ပထမဦး", "b": "ဒုတိယဦး"}}

# ตัวเลือกช่วงเกิดวันพุธ (เลือกสำนัก/ช่วงที่ทราบ)
WED_SECTOR = {
    "th": {"am": "พุธ (ช้างมีงา)", "pm": "ราหู / พุธกลางคืน (ช้างไม่มีงา)", "unknown": "ไม่ทราบช่วงเช้า/บ่าย"},
    "en": {"am": "Wednesday (tusked elephant)", "pm": "Rahu / Wednesday night (tuskless elephant)", "unknown": "Not sure (morning/afternoon)"},
    "mm": {"am": "ဗုဒ္ဓဟူး (ဆင် — အစွယ်ရှိ)", "pm": "ရာဟု / ဗုဒ္ဓဟူးမွန်းလွဲ (ဟိုင်း — အစွယ်မဲ့ဆင်)", "unknown": "နံနက်/မွန်းလွဲ မသိ"},
}
WED_SECTOR_LABEL = {"th": "ช่วงเกิดวันพุธ", "en": "Wednesday birth period", "mm": "ဗုဒ္ဓဟူးနေ့ မွေးချိန်"}

# ============ พม่า: โปรไฟล์ ============
MM_FIELDS = {
    "th": {"planet": "ดาว", "animal": "สัตว์", "dir": "ทิศ", "trait": "นิสัยพื้นฐาน",
           "mahabote": "มหาโบติ", "nakhat": "นะขัต",
           "wed_unknown": "เกิดวันพุธแต่ไม่ระบุช่วงเช้า/บ่าย — ระบบยังไม่ระบุดาว/สัตว์/ทิศให้ (บางสำนักแยกพุธกับราหูต่างกัน)"},
    "en": {"planet": "Planet", "animal": "Animal", "dir": "Direction", "trait": "Basic nature",
           "mahabote": "Mahabote", "nakhat": "Nakhat",
           "wed_unknown": "Born Wednesday with unknown AM/PM — planet/animal/direction withheld (schools split Wednesday/Rahu differently)"},
    "mm": {"planet": "ဂြိုဟ်", "animal": "တိရစ္ဆာန်", "dir": "အရပ်", "trait": "အခြေခံ စိတ်နေသဘာထား",
           "mahabote": "မဟာဘုတ်", "nakhat": "နက္ခတ်",
           "wed_unknown": "ဗုဒ္ဓဟူးနေ့မွေးပြီး နံနက်/မွန်းလွဲ မသိပါ — ဂြိုဟ်/တိရစ္ဆာန်/အရပ်ကို မဖော်ပြပါ (ဗုဒ္ဓဟူးနှင့် ရာဟုကို အယူအဆအလိုက် ခွဲပုံမတူပါ)"},
}
MAHABOTE_LABELS = {"th": ["บิงคะ", "อะตุน", "ยะซา", "อะดิปติ", "มะระนะ", "เทเกะ", "ปุติ"],
                   "en": ["Binga", "Atun", "Yaza", "Adipati", "Marana", "Thike", "Puti"],
                   "mm": ["ဘင်္ဂ", "အထွန်း", "ရာဇ", "အဓိပတိ", "မရဏ", "သိုက်", "ပုတိ"]}
NAKHAT_LABELS = {"th": ["ยักษ์", "เทวดา", "มนุษย์"], "en": ["Ogre", "Deva", "Human"],
                 "mm": ["ဘီလူး", "နတ်", "လူ"]}
MM_PROFILE_ONLY = {
    "th": "ศาสตร์พม่าในชั้นนี้ให้เฉพาะโปรไฟล์รายบุคคล (ยังไม่มีสูตรจับคู่ที่มีหลักฐานเพียงพอ) จึงไม่ตัดสินความเข้ากันของคู่",
    "en": "At this level the Burmese tradition provides per-person profiles only (no well-evidenced couple formula), so it does not rate compatibility.",
    "mm": "ဤအဆင့်တွင် မြန်မာ့ဗေဒင်သည် တစ်ဦးချင်းစီ၏ အချက်အလက်ကိုသာ ဖော်ပြသည် (အထောက်အထား ခိုင်မာသော စုံတွဲ ပုံသေနည်း မရှိသေး) ဖြစ်၍ လိုက်ဖက်မှုကို အဆင့်မသတ်မှတ်ပါ။",
}

# ============ จีน: กิ่งดิน ============
CN_ELEMENT = {"wood": {"th": "ไม้", "en": "Wood", "mm": "သစ်သား"}, "fire": {"th": "ไฟ", "en": "Fire", "mm": "မီး"},
              "earth": {"th": "ดิน", "en": "Earth", "mm": "မြေ"}, "metal": {"th": "ทอง", "en": "Metal", "mm": "သတ္တု"},
              "water": {"th": "น้ำ", "en": "Water", "mm": "ရေ"}}
CN_POLARITY = {"หยาง": {"th": "หยาง", "en": "Yang", "mm": "ယန်"}, "หยิน": {"th": "หยิน", "en": "Yin", "mm": "ယင်"}}
CN_ANIMAL = {"鼠": {"th": "หนู", "en": "Rat", "mm": "ကြွက်"}, "牛": {"th": "วัว", "en": "Ox", "mm": "နွား"},
             "虎": {"th": "เสือ", "en": "Tiger", "mm": "ကျား"}, "兔": {"th": "กระต่าย", "en": "Rabbit", "mm": "ယုန်"},
             "龙": {"th": "มังกร", "en": "Dragon", "mm": "နဂါး"}, "蛇": {"th": "งู", "en": "Snake", "mm": "မြွေ"},
             "马": {"th": "ม้า", "en": "Horse", "mm": "မြင်း"}, "羊": {"th": "แพะ", "en": "Goat", "mm": "ဆိတ်"},
             "猴": {"th": "ลิง", "en": "Monkey", "mm": "မျောက်"}, "鸡": {"th": "ไก่", "en": "Rooster", "mm": "ကြက်"},
             "狗": {"th": "สุนัข", "en": "Dog", "mm": "ခွေး"}, "猪": {"th": "หมู", "en": "Pig", "mm": "ဝက်"}}

RULE_LABEL = {
    "liuhe": {"th": "六合 · คู่ประสาน", "en": "六合 · harmonious pair", "mm": "六合 · သဟဇာတတွဲ"},
    "sanhe_2of3": {"th": "三合 · กลุ่มธาตุเดียวกัน (2/3)", "en": "三合 · same element group (2/3)", "mm": "三合 · ဓာတ်တူအုပ်စု (၂/၃)"},
    "liuchong": {"th": "六冲 · คู่ปะทะ", "en": "六冲 · clashing pair", "mm": "六冲 · ထိပ်တိုက်တွဲ"},
    "liuhai": {"th": "六害 · คู่บั่นทอน", "en": "六害 · draining pair", "mm": "六害 · အားနည်းစေသောတွဲ"},
    "sanxing_zimao": {"th": "三刑 · 子卯 (ขัดแย้ง)", "en": "三刑 · Zǐ–Mǎo (conflict)", "mm": "三刑 · ကြွက်–ယုန် (子卯) (ပဋိပက္ခ)"},
    "sanxing_2of3": {"th": "三刑 · ขัดแย้งซ้ำ (2/3)", "en": "三刑 · repeated conflict (2/3)", "mm": "三刑 · ထပ်တလဲလဲ ပဋိပက္ခ (၂/၃)"},
    "zixing": {"th": "自刑 · ลงโทษตัวเอง", "en": "自刑 · self-punishment", "mm": "自刑 · မိမိကိုယ်ကို ဒဏ်ခတ်ခြင်း"},
    "po": {"th": "破 · คู่รบกวน (ทดลอง)", "en": "破 · disrupting pair (experimental)", "mm": "破 · အနှောင့်အယှက်တွဲ (စမ်းသပ်ဆဲ)"},
    "same_branch": {"th": "กิ่งปีเดียวกัน", "en": "Same year branch", "mm": "မွေးနှစ်ခန်း တူညီ"},
}

CN_ONLY_WARN = {
    "th": "ชั้นนี้ใช้แค่ “กิ่งปี” = 1 ใน 8 อักษร (八字) เท่านั้น — ไม่ใช่คำตัดสินดวงคู่แบบปาจื่อเต็ม",
    "en": "This layer uses only the year branch = 1 of the 8 characters (八字) — not a full BaZi verdict.",
    "mm": "ဤအဆင့်သည် “မွေးနှစ်ခန်း” တစ်ခုတည်းကိုသာ သုံးသည် = စာလုံး ၈ လုံးအနက် ၁ လုံး (八字) — ပါကျီ (八字) အပြည့် ဆုံးဖြတ်ချက် မဟုတ်ပါ။",
}
CN_BOUNDARY_WARN = {
    "th": "มีฝ่ายเกิดใกล้รอยต่อปีจีน (ระหว่างตรุษจีนกับ立春) — กิ่งปีอาจต่างกันตามสำนัก ควรยืนยันปีนักษัตรที่ครอบครัวใช้",
    "en": "Someone was born near the Chinese year boundary (between Lunar New Year and Lìchūn) — the year branch may differ by school; confirm the family's zodiac year.",
    "mm": "တစ်ဦးဦးသည် တရုတ်နှစ်ကူး အပိုင်းအခြားအနီး (နှစ်ကူးနှင့် လိချွန်းကြား) တွင် မွေးသည် — မွေးနှစ်ခန်း အယူအဆအလိုက် ကွဲနိုင်သဖြင့် မိသားစုသုံးသော နှစ်ရာသီကို အတည်ပြုပါ။",
}

# ============ ไทย: ทักษา ============
THAKSA_REGION = {
    "th": ["บริวาร", "อายุ", "เดช", "ศรี", "มูละ", "อุตสาหะ", "มนตรี", "กาลกิณี"],
    "en": ["Attendants", "Age", "Power", "Glory", "Root", "Effort", "Advisor", "Inauspicious"],
    "mm": ["ပရိဝါရ", "အာယု", "တေဇ", "သီရိ", "မူလ", "ဥဿာဟ", "မန္တြီ", "ကာလကဏ္ဏီ"],
}
TH_REL = {
    "friend": {"th": "คู่มิตร (ตามคติดาวประจำวัน)", "en": "Friend pair (day-planet lore)", "mm": "မိတ်တွဲ (မွေးနေ့ဂြိုဟ် ထုံးတမ်း)"},
    "enemy": {"th": "คู่ศัตรู (ตามคติดาวประจำวัน)", "en": "Enemy pair (day-planet lore)", "mm": "ရန်တွဲ (မွေးနေ့ဂြိုဟ် ထုံးတမ်း)"},
    "same": {"th": "ดาวประจำวันเดียวกัน", "en": "Same day-planet", "mm": "မွေးနေ့ဂြိုဟ် တူညီ"},
    "not_listed": {"th": "ไม่อยู่ในคู่ที่ตำราระบุ", "en": "Not in a listed pair", "mm": "ကျမ်းတွင် ဖော်ပြထားသည့် အတွဲ မဟုတ်ပါ"},
}
TH_CATEGORY_NOTE = {
    "th": "ผลเป็น “หมวด” ตามคติดาวประจำวัน ไม่ใช่คะแนนความรัก — และไม่ควรใช้ตัดสินความสัมพันธ์ทั้งหมด",
    "en": "The result is a category from day-planet lore, not a love score — and not a judgment of the whole relationship.",
    "mm": "ရလဒ်သည် မွေးနေ့ဂြိုဟ် ထုံးတမ်းအရ “အမျိုးအစား” ဖြစ်ပြီး အချစ်ရမှတ် မဟုတ် — ဆက်ဆံရေးတစ်ခုလုံးကို ဆုံးဖြတ်ရန် မသုံးသင့်ပါ။",
}

# ============ ตะวันตก: ราศี/ธาตุ/คุณภาพ ============
W_SIGN = {
    "th": ["ราศีเมษ", "ราศีพฤษภ", "ราศีเมถุน", "ราศีกรกฎ", "ราศีสิงห์", "ราศีกันย์",
           "ราศีตุลย์", "ราศีพิจิก", "ราศีธนู", "ราศีมังกร", "ราศีกุมภ์", "ราศีมีน"],
    "en": ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
           "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"],
    "mm": ["မိဿ", "ပြိဿ", "မေထုန်", "ကရကဋ်", "သိဟ်", "ကန်",
           "တူ", "ဗြိစ္ဆာ", "ဓနု", "မကာရ", "ကုံ", "မိန်"],
}
W_ELEMENT = {"fire": {"th": "ไฟ", "en": "Fire", "mm": "မီး"}, "earth": {"th": "ดิน", "en": "Earth", "mm": "မြေ"},
             "air": {"th": "ลม", "en": "Air", "mm": "လေ"}, "water": {"th": "น้ำ", "en": "Water", "mm": "ရေ"}}
W_MODALITY = {"cardinal": {"th": "ผู้ริเริ่ม", "en": "Cardinal", "mm": "ဦးဆောင်တက်ကြွ"},
              "fixed": {"th": "มั่นคง", "en": "Fixed", "mm": "တည်ငြိမ်ခိုင်မာ"},
              "mutable": {"th": "ยืดหยุ่น", "en": "Mutable", "mm": "ပြောင်းလွယ်ပျော့ပြောင်း"}}
W_ELEM_REL = {
    "same_element": {"th": "ธาตุเดียวกัน — จังหวะพื้นฐานคล้ายกัน (ไม่แปลว่า “ดีที่สุด”)", "en": "Same element — similar basic rhythm (not “best”)", "mm": "ဓာတ်တူ — အခြေခံစည်းချက် ဆင်တူ (အကောင်းဆုံးဟု မဆိုလိုပါ)"},
    "supportive": {"th": "ธาตุเกื้อหนุนกัน (ไฟ–ลม / ดิน–น้ำ)", "en": "Supportive elements (Fire–Air / Earth–Water)", "mm": "အားဖြည့်သော ဓာတ်များ (မီး–လေ / မြေ–ရေ)"},
    "adjust": {"th": "ธาตุที่ต้องปรับจังหวะเข้าหากัน", "en": "Elements that need rhythm adjustment", "mm": "စည်းချက် ညှိယူရမည့် ဓာတ်များ"},
}
W_MOD_REL = {
    "same_modality": {"th": "คุณภาพเดียวกัน — เข้าใจวิธีลงมือของกันและกัน (แต่อาจยึดทางของตน)", "en": "Same modality — you grasp each other's approach (but may each hold your own line)", "mm": "သဘာဝတူ — အချင်းချင်း နည်းလမ်းကို နားလည်သည် (သို့သော် ကိုယ့်လမ်းကိုယ် ကိုင်နိုင်သည်)"},
    "different_modality": {"th": "คุณภาพต่างกัน — เติมเต็มจังหวะซึ่งกันและกัน", "en": "Different modalities — complementary rhythms", "mm": "သဘာဝကွဲ — တစ်ဦးနှင့်တစ်ဦး စည်းချက်ဖြည့်ပေးသည်"},
}
W_ONLY_WARN = {
    "th": "นี่คือภาพรวมจากราศีอาทิตย์เท่านั้น — โหราศาสตร์ตะวันตกจริงไม่ตัดสินจากราศีอาทิตย์เพียงอย่างเดียว",
    "en": "Sun-sign overview only — real Western astrology never judges by the Sun sign alone.",
    "mm": "နေရာသီအကျဉ်းသာဖြစ်သည် — တကယ့် အနောက်တိုင်းဗေဒင်သည် နေရာသီတစ်ခုတည်းဖြင့် မဆုံးဖြတ်ပါ။",
}
W_INGRESS_WARN = {
    "th": "มีฝ่ายเกิดวันคาบเกี่ยวที่ดวงอาทิตย์เปลี่ยนราศี — หากทราบเวลาเกิด ราศีอาทิตย์อาจเป็นอีกตัวหนึ่ง",
    "en": "Someone was born on a day the Sun changed sign — with a birth time, the Sun sign could differ.",
    "mm": "တစ်ဦးဦးသည် နေက ရာသီပြောင်းသည့်နေ့တွင် မွေးသည် — မွေးချိန်သိပါက နေရာသီ ကွဲနိုင်သည်။",
}

# ============ บทสรุปข้ามศาสตร์ (convergence) ============
CONV = {
    "th": {"head": "🧭 ภาพรวมข้ามศาสตร์", "supportive": "สัญญาณเกื้อหนุน (รายศาสตร์)",
           "challenging": "จุดที่ต้องดูแล (รายศาสตร์)", "mixed": "สัญญาณผสม",
           "profile_only": "ให้ข้อมูลรายบุคคลเท่านั้น (ยังไม่มีกฎความสัมพันธ์)",
           "missing": "ข้อมูลที่ขาดซึ่งอาจเปลี่ยนผล",
           "prompts_head": "💬 คำถามชวนคุย (ใช้ได้กับทุกคู่)"},
    "en": {"head": "🧭 Cross-tradition overview", "supportive": "Supportive signals (by tradition)",
           "challenging": "Areas to tend (by tradition)", "mixed": "Mixed signals",
           "profile_only": "Per-person profile only (no relationship rule yet)",
           "missing": "Missing data that could change the reading",
           "prompts_head": "💬 Conversation prompts (for any couple)"},
    "mm": {"head": "🧭 ပညာရပ်ပေါင်းစုံ ခြုံငုံသုံးသပ်ချက်", "supportive": "အားဖြည့်သည့် အချက်များ (ပညာရပ်အလိုက်)",
           "challenging": "ဂရုစိုက်ရမည့် အချက်များ (ပညာရပ်အလိုက်)", "mixed": "ရောနှောသော အချက်များ",
           "profile_only": "တစ်ဦးချင်း အချက်အလက်သာ (ဆက်ဆံရေးစည်းမျဉ်း မရှိသေး)",
           "missing": "ရလဒ်ကို ပြောင်းလဲစေနိုင်သော လိုအပ်နေသည့် အချက်အလက်များ",
           "prompts_head": "💬 စကားဝိုင်းမေးခွန်းများ (မည်သည့်စုံတွဲမဆို)"},
}

CONV_PROMPTS = {
    "th": ["เวลาที่รู้สึกว่า “คุยกันไม่รู้เรื่อง” พวกคุณมักปล่อยผ่าน หรือตกลงกันตรงนั้นก่อน?",
           "เรื่องเงิน ใครถนัดวางแผน ใครถนัดใช้ — แล้วสองอย่างนี้สมดุลกันไหม?",
           "เวลาคนหนึ่งอยากเร่ง อีกคนอยากช้า ปกติหาจุดตรงกลางกันยังไง?"],
    "en": ["When you feel unheard, do you usually let it pass, or settle it on the spot?",
           "With money, who plans and who spends — and is that balance working?",
           "When one wants speed and the other wants caution, how do you meet in the middle?"],
    "mm": ["“စကားမတည့်” ဟု ခံစားရသည့်အခါ များသောအားဖြင့် ကျော်လိုက်သလား၊ ထိုနေရာတွင် ပြေလည်အောင် လုပ်သလား?",
           "ငွေကြေးကိစ္စတွင် မည်သူက စီစဉ်၊ မည်သူက သုံးသလဲ — ထိုဟန်ချက် အဆင်ပြေပါသလား?",
           "တစ်ဦးက အလျင်လို၊ တစ်ဦးက သတိကြီးလိုသည့်အခါ အလယ်အလတ်ကို မည်သို့ ရှာကြသလဲ?"],
}

# ============ เบอร์คู่ (ข้อมูลเสริม) ============
NUM_SUPP = {
    "th": {"head": "📱 เบอร์โทรของทั้งคู่ (ข้อมูลเสริม แยกจากศาสตร์วันเกิด)", "note": "เป็นเลขศาสตร์ของ Number Luck — ไม่ผสมเป็นคะแนนเดียวกับดวงคู่ตามศาสตร์วันเกิด"},
    "en": {"head": "📱 Both phone numbers (supplementary, separate from birth traditions)", "note": "Number Luck numerology — never blended into one score with the birth-date traditions."},
    "mm": {"head": "📱 နှစ်ဦးစလုံး၏ ဖုန်းနံပါတ် (ဖြည့်စွက်၊ မွေးနေ့ဗေဒင်နှင့် သီးခြား)", "note": "Number Luck ဂဏန်းဗေဒင် — မွေးနေ့ဗေဒင်နှင့် ရမှတ်တစ်ခုတည်း ရောစပ်၍ မပြပါ။"},
}

# ============ Disclaimer ============
DISCLAIMER = {
    "th": "ผลทั้งหมดเป็นความเชื่อและมรดกทางวัฒนธรรม ไม่ใช่ข้อเท็จจริงทางวิทยาศาสตร์ ใช้เพื่อสะท้อนความสัมพันธ์และชวนพูดคุย ไม่ใช่คำทำนายชี้ขาดว่า “คู่แท้” หรือ “ต้องเลิก” — โปรดใช้วิจารณญาณ",
    "en": "All results reflect cultural belief and heritage, not scientific fact. Use them to reflect on your relationship and open conversations — never as a verdict of “soulmate” or “must break up.”",
    "mm": "ရလဒ်အားလုံးသည် ရိုးရာယုံကြည်မှုနှင့် ယဉ်ကျေးမှုအမွေအနှစ်သာဖြစ်ပြီး သိပ္ပံနည်းကျ အချက်အလက် မဟုတ်ပါ — ဆက်ဆံရေးကို ဆင်ခြင်သုံးသပ်ရန်နှင့် စကားဝိုင်းဖွင့်ရန် သုံးပါ၊ “ဘဝဖော်အစစ်” သို့မဟုတ် “ခွဲရမည်” ဟု ဆုံးဖြတ်ရန် မဟုတ်ပါ။",
}

# ============ หมายเหตุต่อกฎ (note_key → 3 ภาษา) ============
NOTES = {
    "same_branch": {
        "th": "เกิดปีนักษัตรเดียวกัน — มีพื้นนิสัยเชิงสัญลักษณ์คล้ายกัน แต่เป็นเพียง 1 ใน 8 อักษร",
        "en": "Same zodiac year — symbolically similar temperament, but only 1 of 8 characters.",
        "mm": "မွေးနှစ်ရာသီ တူညီ — သဘာဝချင်း ဆင်တူသော်လည်း စာလုံး ၈ လုံးအနက် ၁ လုံးသာ ဖြစ်သည်။",
    },
    "sanhe_2of3": {
        "th": "อยู่ในกลุ่ม三合เดียวกันเพียง 2 ใน 3 กิ่ง — ยังไม่นับเป็น三合局สมบูรณ์",
        "en": "Two of three branches of the same 三合 group — not a complete 三合 formation.",
        "mm": "三合 အုပ်စုတစ်ခုတည်းတွင် ၃ ခန်းအနက် ၂ ခန်းသာ — 三合 ပြည့်စုံမှု မဟုတ်သေးပါ။",
    },
    "chong_not_fatal": {
        "th": "六冲 ไม่ได้แปลว่าต้องเลิก — เป็นแรงปะทะที่กระตุ้นให้ปรับตัว (ตำราให้ดูทั้งดวง)",
        "en": "六冲 does not mean separation — it's a friction that prompts adjustment (texts read the whole chart).",
        "mm": "六冲 သည် ခွဲရမည်ဟု မဆိုလို — ညှိယူရန် လှုံ့ဆော်သော ပွတ်တိုက်မှုဖြစ်သည် (ကျမ်းက ဇာတာတစ်ခုလုံးကို ကြည့်သည်)။",
    },
    "xing_context": {
        "th": "刑 เป็นสัญญาณขัดแย้งที่ต้องดูบริบททั้งดวง ไม่ควรฟันธงว่าร้ายทันที (มีหลายสำนัก)",
        "en": "刑 is a conflict signal to read in full context, not an immediate verdict (multiple schools).",
        "mm": "刑 သည် ဇာတာတစ်ခုလုံး၏ အခြေအနေဖြင့် ကြည့်ရသည့် ပဋိပက္ခလက္ခဏာဖြစ်ပြီး ချက်ချင်း ဆုံးဖြတ်ရန် မဟုတ် (အယူအဆများစွာ ရှိသည်)။",
    },
    "xing_2of3": {
        "th": "อยู่ในกลุ่ม三刑เพียง 2 ใน 3 กิ่ง — ชุดยังไม่ครบ จึงเป็นแค่สัญญาณที่ต้องสังเกต",
        "en": "Two of three branches of a 三刑 set — the set is incomplete, so treat it as a signal to watch.",
        "mm": "三刑 အုပ်စုတွင် ၃ ခန်းအနက် ၂ ခန်းသာ — အုပ်စုမပြည့်စုံသဖြင့် စောင့်ကြည့်ရမည့် လက္ခဏာသာဖြစ်သည်။",
    },
    "po_experimental": {
        "th": "破 มีหลักฐานเก่าอ่อนกว่ากฎอื่น — แสดงเป็นข้อมูลทดลองเท่านั้น ไม่ใช้หักผลหลัก",
        "en": "破 has weaker classical evidence than the other rules — shown as experimental only.",
        "mm": "破 သည် အခြားစည်းမျဉ်းများထက် ရှေးကျမ်းအထောက်အထား အားနည်းသည် — စမ်းသပ်ဆဲအဖြစ်သာ ပြသည်။",
    },
    "mahabote_individual": {
        "th": "มหาโบติเป็นพื้นดวงรายบุคคล ไม่ใช่สูตรจับคู่ — ไม่นำมาคิดคะแนนความเข้ากัน",
        "en": "Mahabote is a per-person chart type, not a couple formula — not used for compatibility.",
        "mm": "မဟာဘုတ်သည် တစ်ဦးချင်း ဇာတာအမျိုးအစားဖြစ်ပြီး စုံတွဲ ပုံသေနည်း မဟုတ် — လိုက်ဖက်မှုအတွက် မသုံးပါ။",
    },
    "nakhat_individual": {
        "th": "นะขัตเป็นประเภทพื้นดวงรายบุคคล — ยังไม่มีตารางจับคู่ที่ยืนยัน จึงไม่ให้คะแนนคู่",
        "en": "Nakhat is a per-person type — no verified pairing table, so no couple score.",
        "mm": "နက္ခတ်သည် တစ်ဦးချင်း အမျိုးအစားဖြစ်သည် — အတည်ပြုထားသော တွဲဖက်ဇယား မရှိသဖြင့် စုံတွဲအမှတ် မပေးပါ။",
    },
    "thai_planet_category": {
        "th": "เป็น “หมวด” ตามคติดาวประจำวัน ไม่ใช่คะแนนความรัก",
        "en": "A category from day-planet lore, not a love score.",
        "mm": "မွေးနေ့ဂြိုဟ် ထုံးတမ်းအရ “အမျိုးအစား” ဖြစ်ပြီး အချစ်ရမှတ် မဟုတ်ပါ။",
    },
    "thaksa_derived": {
        "th": "การเทียบดาวของอีกฝ่ายลงในทักษาเป็นการประยุกต์ของ Number Luck ไม่ใช่สูตรสมพงศ์มาตรฐาน",
        "en": "Placing the partner's star in one's Thaksa is a Number Luck application, not a standard Somphong formula.",
        "mm": "အဖော်၏ဂြိုဟ်ကို ထက်ဆာတွင် ထည့်ကြည့်ခြင်းသည် Number Luck ၏ အသုံးချနည်းဖြစ်ပြီး ထိုင်းရိုးရာ စုံတွဲတွက်နည်း (สมพงศ์) မဟုတ်ပါ။",
    },
    "element_narrative": {
        "th": "การจัดธาตุเป็นภาษาเชิงสัญลักษณ์ ไม่ใช่ผลทดลองทางวิทยาศาสตร์",
        "en": "Element typing is symbolic language, not an experimental result.",
        "mm": "ဓာတ်အမျိုးအစားခွဲခြင်းသည် သင်္ကေတဘာသာစကားဖြစ်ပြီး စမ်းသပ်ရလဒ် မဟုတ်ပါ။",
    },
}
