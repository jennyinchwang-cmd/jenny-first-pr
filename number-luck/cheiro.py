# -*- coding: utf-8 -*-
"""
ชั้น 4 (เสริม): เลขศาสตร์สากลสาย Cheiro/Chaldean + ความเข้ากันแบบอินเดีย (Mulank)
==============================================================================
1) Cheiro Compound Numbers (10-52) — ความหมาย "เลขผสม" ของผลรวมเบอร์
   อิงตำรา Cheiro's Book of Numbers (public domain, 1926) เรียบเรียงใหม่เอง 3 ภาษา
2) Mulank (เลขจิตอินเดีย = รากเลขของ "วันที่เกิด") × รากผลรวมเบอร์
   ตัดสินด้วยตารางมิตร-ศัตรูดาวสายพระเวท (Parashari) — mapping ดาวแบบอินเดีย
   (1=Sun 2=Moon 3=Jupiter 4=Rahu 5=Mercury 6=Venus 7=Ketu 8=Saturn 9=Mars)
   ⚠️ mapping นี้ต่างจากระบบไทย/พม่าที่ใช้ในชั้นอื่น — เป็น "มุมมองอินเดีย" เสริม

หมายเหตุ: ชั้นนี้เป็นข้อมูลเสริม (informational) ไม่ปรับเกรดหลักของเบอร์
สำนวนพม่า (mm) ควรให้เจ้าของภาษาตรวจก่อนใช้เชิงพาณิชย์เต็มตัว
"""

# ---------- ป้าย UI 3 ภาษา ----------
CHEIRO_UI = {
    "th": {"head": "🔢 เลขผสมสากล (Cheiro)", "compound": "เลขผสมของผลรวม",
           "single": "ผลรวมลดเหลือเลขโดด ไม่มีเลขผสมตามตำรานี้",
           "tone": {"ดี": "มงคล", "ระวัง": "พึงระวัง", "กลาง": "เป็นกลาง"},
           "mulank_head": "🕉️ ความเข้ากันแบบอินเดีย (Mulank)",
           "mulank_line": "เลขจิตของคุณ (จากวันที่เกิด {d}) = {m} ({pm}) × รากผลรวมเบอร์ = {r} ({pr})",
           "note": "มุมมองเลขศาสตร์สากล/อินเดีย — ตารางดาวต่างจากระบบพม่าด้านบน ใช้เป็นข้อมูลเสริม"},
    "en": {"head": "🔢 Universal Compound Number (Cheiro)", "compound": "Compound of the sum",
           "single": "The sum reduces to a single digit — no compound number in this system",
           "tone": {"ดี": "Fortunate", "ระวัง": "Caution", "กลาง": "Neutral"},
           "mulank_head": "🕉️ Indian Compatibility (Mulank)",
           "mulank_line": "Your psychic number (from day of birth {d}) = {m} ({pm}) × number's root = {r} ({pr})",
           "note": "Western/Indian numerology view — planet mapping differs from the Myanmar system above; supplementary only"},
    "mm": {"head": "🔢 နိုင်ငံတကာသုံး ပေါင်းစပ်ဂဏန်း (Cheiro)", "compound": "ပေါင်းလဒ်၏ ပေါင်းစပ်ဂဏန်း",
           "single": "ပေါင်းလဒ်ကို လျှော့တွက်ရာ ဂဏန်းတစ်လုံးတည်း ဖြစ်သွားသဖြင့် ဤကျမ်းအရ ပေါင်းစပ်ဂဏန်း မရှိပါ။",
           "tone": {"ดี": "မင်္ဂလာရှိ", "ระวัง": "သတိပြုရန်", "กลาง": "အလယ်အလတ်"},
           "mulank_head": "🕉️ အိန္ဒိယနည်း လိုက်ဖက်မှု (Mulank)",
           "mulank_line": "သင့်စိတ်ဂဏန်း (မွေးသည့်ရက် {d} မှ) = {m} ({pm}) × နံပါတ်ပေါင်းလဒ်၏ အမြစ်ဂဏန်း = {r} ({pr})",
           "note": "အနောက်တိုင်း/အိန္ဒိယ ဂဏန်းဗေဒင် ရှုထောင့် — ဂြိုဟ်သတ်မှတ်ပုံမှာ အထက်ပါ မြန်မာစနစ်နှင့် ကွာခြားသည်၊ ဖြည့်စွက်အချက်အလက်အဖြစ်သာ ရှုမြင်ပါ။"},
}

# ดาวแบบอินเดีย (สำหรับชั้นนี้เท่านั้น)
INDIAN_PLANET = {
    1: {"th": "อาทิตย์ (Surya)", "en": "Sun (Surya)", "mm": "တနင်္ဂနွေ (Surya)"},
    2: {"th": "จันทร์ (Chandra)", "en": "Moon (Chandra)", "mm": "တနင်္လာ (Chandra)"},
    3: {"th": "พฤหัส (Guru)", "en": "Jupiter (Guru)", "mm": "ကြာသပတေး (Guru)"},
    4: {"th": "ราหู (Rahu)", "en": "Rahu", "mm": "ရာဟု"},
    5: {"th": "พุธ (Budha)", "en": "Mercury (Budha)", "mm": "ဗုဒ္ဓဟူး (Budha)"},
    6: {"th": "ศุกร์ (Shukra)", "en": "Venus (Shukra)", "mm": "သောကြာ (Shukra)"},
    7: {"th": "เกตุ (Ketu)", "en": "Ketu", "mm": "ကိတ်"},
    8: {"th": "เสาร์ (Shani)", "en": "Saturn (Shani)", "mm": "စနေ (Shani)"},
    9: {"th": "อังคาร (Mangal)", "en": "Mars (Mangal)", "mm": "အင်္ဂါ (Mangal)"},
}

# ---------- Cheiro Compound Numbers ----------
# tone: ดี / ระวัง / กลาง — name+text 3 ภาษา (เรียบเรียงเองจากแก่นตำรา)
_BASE = {
    10: {"tone": "ดี", "name": {"th": "กงล้อโชคชะตา", "en": "Wheel of Fortune", "mm": "ကံကြမ္မာစက်ဝန်း"},
         "text": {"th": "เลขแห่งการขึ้น-ลงตามการกระทำ ชื่อเสียงเด่นดัง แผนการมักสำเร็จตามที่ตั้งใจ",
                  "en": "Rise and fall follow one's own actions; the name becomes known and plans tend to be realized.",
                  "mm": "မိမိ၏လုပ်ရပ်အတိုင်း အတက်အကျရှိသော ဂဏန်း၊ နာမည်ကျော်ကြားပြီး ရည်ရွယ်ထားသည့် အစီအစဉ်များ အောင်မြင်တတ်သည်။"}},
    11: {"tone": "ระวัง", "name": {"th": "สิงห์ถูกล่าม", "en": "Hidden Trials", "mm": "လျှို့ဝှက် အခက်အခဲများ"},
         "text": {"th": "เตือนเรื่องอุปสรรคซ่อนเร้นและการถูกหักหลังจากคนใกล้ตัว ควรเลือกคบคนรอบข้างอย่างระวัง",
                  "en": "Warns of hidden obstacles and treachery from those around you; choose your circle carefully.",
                  "mm": "မမြင်ရသော အခက်အခဲနှင့် အနီးကပ်ရှိသူများ၏ သစ္စာဖောက်မှုကို သတိပေးသည်၊ မိတ်ဆွေရွေးချယ်ရာတွင် သတိထားပါ။"}},
    12: {"tone": "ระวัง", "name": {"th": "ผู้ถูกพลี", "en": "The Sacrifice", "mm": "စတေးခံရသူ"},
         "text": {"th": "เสี่ยงตกเป็นเหยื่อแผนของผู้อื่น หรือต้องเสียสละเพื่อคนอื่นบ่อยครั้ง ควรรักษาสิทธิ์ของตนเอง",
                  "en": "Risk of becoming a victim of others' schemes or sacrificing too much; guard your own interests.",
                  "mm": "သူတစ်ပါး၏ အကြံအစည်တွင် သားကောင်ဖြစ်တတ်ပြီး သူများအတွက် စွန့်လွှတ်ရမှု များတတ်သည်၊ မိမိအခွင့်အရေးကို ထိန်းသိမ်းပါ။"}},
    13: {"tone": "ระวัง", "name": {"th": "พลังแห่งการเปลี่ยนแปลง", "en": "Change & Upheaval", "mm": "ပြောင်းလဲမှုစွမ်းအား"},
         "text": {"th": "พลังสูงแต่ผันผวน มีการเปลี่ยนแผนกะทันหัน ใช้พลังถูกทางจะยิ่งใหญ่ ใช้ผิดทางจะพังเอง",
                  "en": "Great power with upheaval; sudden change of plans. Used rightly it builds, used wrongly it destroys.",
                  "mm": "စွမ်းအားကြီးသော်လည်း မတည်မငြိမ်ဖြစ်ပြီး အစီအစဉ်များ ရုတ်တရက် ပြောင်းလဲတတ်သည်။ မှန်ကန်စွာသုံးလျှင် ကြီးပွားပြီး လွဲမှားစွာသုံးလျှင် မိမိဘာသာ ပျက်စီးတတ်သည်။"}},
    14: {"tone": "ระวัง", "name": {"th": "การเคลื่อนไหวเสี่ยงภัย", "en": "Movement & Risk", "mm": "လှုပ်ရှားမှုနှင့် စွန့်စားမှု"},
         "text": {"th": "ดีเรื่องเงินและการค้าแต่มากับความเสี่ยง ระวังความเสียหายจากธรรมชาติและการตัดสินใจหุนหัน",
                  "en": "Fortunate for money and trade but carries risk; beware losses from natural forces and rash moves.",
                  "mm": "ငွေကြေးနှင့် ကုန်သွယ်မှုအတွက် ကောင်းသော်လည်း စွန့်စားရမှု ပါဝင်သည်၊ သဘာဝဘေးအန္တရာယ်နှင့် အလျင်စလို ဆုံးဖြတ်မှုကြောင့် ဆုံးရှုံးတတ်သဖြင့် သတိထားပါ။"}},
    15: {"tone": "ดี", "name": {"th": "วาทะและเสน่ห์", "en": "Eloquence & Charm", "mm": "နှုတ်ပါရမီနှင့် ဆွဲဆောင်မှု"},
         "text": {"th": "เสน่ห์แรง พูดจาโน้มน้าวเก่ง ได้ลาภได้ของขวัญจากผู้อื่น เหมาะงานที่ใช้วาจาและศิลปะ",
                  "en": "Strong charm and persuasive speech; gifts and favours come easily. Suits work of voice and art.",
                  "mm": "ဆွဲဆောင်မှုပြင်းပြီး စည်းရုံးပြောဆိုတတ်သည်၊ လက်ဆောင်နှင့် ကျေးဇူးများ လွယ်ကူစွာရရှိမည်။ စကားပြောနှင့် အနုပညာဆိုင်ရာ အလုပ်များနှင့် သင့်တော်သည်။"}},
    16: {"tone": "ระวัง", "name": {"th": "หอคอยฟ้าผ่า", "en": "The Shattered Tower", "mm": "မိုးကြိုးပစ်ခံရသော ရဲတိုက်"},
         "text": {"th": "เตือนแรงเรื่องแผนพังกะทันหันและอุบัติเหตุ ควรวางแผนสำรองและไม่ประมาทเสมอ",
                  "en": "Strong warning of sudden collapse of plans and accidents; always keep a fallback and stay alert.",
                  "mm": "အစီအစဉ်များ ရုတ်တရက် ပျက်စီးခြင်းနှင့် မတော်တဆမှုကို ပြင်းထန်စွာ သတိပေးသည်၊ အရန်အစီအစဉ် အမြဲထားပြီး မပေါ့ဆပါနှင့်။"}},
    17: {"tone": "ดี", "name": {"th": "ดาราแห่งเมไจ", "en": "Star of the Magi", "mm": "မာဂိပညာရှိတို့၏ ကြယ်"},
         "text": {"th": "เลขจิตวิญญาณสูง ผ่านอุปสรรคได้อย่างสง่างาม ชื่อเสียงยั่งยืนเหนือกาลเวลา",
                  "en": "A highly spiritual number; rises above trials with grace and leaves a lasting name.",
                  "mm": "ဝိညာဉ်ရေး မြင့်မားသော ဂဏန်း၊ အခက်အခဲများကို ဂုဏ်သိက္ခာရှိစွာ ကျော်လွှားနိုင်ပြီး နာမည်ကောင်း ရေရှည်တည်တံ့မည်။"}},
    18: {"tone": "ระวัง", "name": {"th": "ศึกภายใน", "en": "Conflict & Materialism", "mm": "ပဋိပက္ခနှင့် ရုပ်ဝါဒ"},
         "text": {"th": "ระวังความขัดแย้ง การหลอกลวง และวัตถุบังตา ควรทำสิ่งต่างๆ อย่างตรงไปตรงมา",
                  "en": "Beware quarrels, deception and material greed clouding judgment; act with honesty.",
                  "mm": "ရန်ဖြစ်ခြင်း၊ လှည့်ဖြားခြင်းနှင့် ရုပ်ဝတ္ထုလောဘကြောင့် အဆုံးအဖြတ်မှားတတ်သည်၊ ရိုးသားဖြောင့်မတ်စွာ ဆောင်ရွက်ပါ။"}},
    19: {"tone": "ดี", "name": {"th": "เจ้าชายแห่งสวรรค์", "en": "Prince of Heaven", "mm": "ကောင်းကင်မင်းသား"},
         "text": {"th": "หนึ่งในเลขดีที่สุดของตำรา ความสุข ความสำเร็จ เกียรติยศ สมหวังรอบด้าน",
                  "en": "One of the most fortunate numbers: happiness, success and honour in all undertakings.",
                  "mm": "ကံအကောင်းဆုံး ဂဏန်းများထဲမှ တစ်ခု — ဆောင်ရွက်သမျှတွင် ပျော်ရွှင်မှု၊ အောင်မြင်မှုနှင့် ဂုဏ်သိက္ခာ ရရှိမည်။"}},
    20: {"tone": "กลาง", "name": {"th": "การตื่นรู้", "en": "The Awakening", "mm": "နိုးထခြင်း"},
         "text": {"th": "เลขแห่งการเริ่มแผนใหม่และการเรียกร้องให้ลงมือ อาจมีความล่าช้าแต่ได้ผลด้านจิตใจมากกว่าวัตถุ",
                  "en": "New plans and a call to action; delays possible — rewards are more spiritual than material.",
                  "mm": "အစီအစဉ်သစ် စတင်ရန်နှင့် လက်တွေ့လှုပ်ရှားရန် နှိုးဆော်သည်၊ နှောင့်နှေးနိုင်သော်လည်း ရုပ်ဝတ္ထုထက် စိတ်ဓာတ်ရေးရာ အကျိုးက ပိုများမည်။"}},
    21: {"tone": "ดี", "name": {"th": "มงกุฎแห่งเมไจ", "en": "Crown of the Magi", "mm": "မာဂိပညာရှိတို့၏ သရဖူ"},
         "text": {"th": "ความก้าวหน้า เกียรติยศ และชัยชนะขั้นสุดท้ายหลังฝ่าฟัน เลขแห่งความสำเร็จที่มั่นคง",
                  "en": "Advancement, honours and final victory after effort; a number of assured success.",
                  "mm": "ကြိုးစားပြီးနောက် တိုးတက်မှု၊ ဂုဏ်ပြုခံရမှုနှင့် နောက်ဆုံးအောင်ပွဲ ရမည် — ခိုင်မာသော အောင်မြင်မှုဂဏန်း။"}},
    22: {"tone": "ระวัง", "name": {"th": "คนดีถูกบังตา", "en": "Blinded by Illusion", "mm": "အထင်အမြင် လွဲမှားခြင်း"},
         "text": {"th": "เตือนเรื่องหลงภาพลวงและไว้ใจคนผิด ตัดสินใจด้วยข้อมูลจริงไม่ใช่ความรู้สึก",
                  "en": "Warns of illusion and misplaced trust; judge by facts, not feelings.",
                  "mm": "ထင်ယောင်ထင်မှားမှုနှင့် လူမှားယုံကြည်မှုကို သတိပေးသည်၊ ခံစားချက်မဟုတ်ဘဲ အချက်အလက်အမှန်ဖြင့် ဆုံးဖြတ်ပါ။"}},
    23: {"tone": "ดี", "name": {"th": "ดาราราชสีห์", "en": "Royal Star of the Lion", "mm": "ခြင်္သေ့၏ တော်ဝင်ကြယ်"},
         "text": {"th": "เลขมงคลยิ่ง ได้รับการอุปถัมภ์จากผู้ใหญ่และผู้มีอำนาจ ทำการใดมักสำเร็จ",
                  "en": "Highly auspicious; help and protection from superiors — success in undertakings.",
                  "mm": "အလွန်မင်္ဂလာရှိသည်၊ လူကြီးသူမများ၏ ထောက်ပံ့ကူညီမှုရပြီး လုပ်သမျှ အောင်မြင်တတ်သည်။"}},
    24: {"tone": "ดี", "name": {"th": "ลาภจากผู้อุปถัมภ์", "en": "Gain through Favour", "mm": "ကျေးဇူးရှင်များထံမှ အကျိုးအမြတ်"},
         "text": {"th": "โชคดีด้านความรักและได้ประโยชน์จากผู้มีตำแหน่งสูง ความสัมพันธ์นำพาความสำเร็จ",
                  "en": "Fortune through love and through those in high position; relationships bring success.",
                  "mm": "အချစ်ရေးကောင်းပြီး ရာထူးကြီးသူများထံမှ အကျိုးကျေးဇူး ရရှိမည်၊ ဆက်ဆံရေးကောင်းက အောင်မြင်မှုကို ဆောင်ကြဉ်းပေးမည်။"}},
    25: {"tone": "ดี", "name": {"th": "แกร่งจากประสบการณ์", "en": "Strength from Experience", "mm": "အတွေ့အကြုံမှ ခွန်အား"},
         "text": {"th": "สำเร็จจากการเรียนรู้ผ่านอุปสรรค ช่วงแรกเหนื่อยแต่บั้นปลายมั่นคง",
                  "en": "Success earned through lessons and strife; hard early, secure later.",
                  "mm": "အခက်အခဲများမှ သင်ခန်းစာယူပြီး အောင်မြင်မည်၊ အစပိုင်းတွင် ပင်ပန်းသော်လည်း နောက်ပိုင်းတွင် တည်ငြိမ်ခိုင်မာမည်။"}},
    26: {"tone": "ระวัง", "name": {"th": "ภัยจากหุ้นส่วน", "en": "Grave Warnings", "mm": "ပြင်းထန်သော သတိပေးချက်"},
         "text": {"th": "เตือนแรงเรื่องเสียหายจากการเก็งกำไร หุ้นส่วน และคำแนะนำผิดๆ อย่าลงทุนตามคนอื่นโดยไม่ตรวจสอบ",
                  "en": "Strong warning of loss through speculation, partnerships and bad advice; verify before investing.",
                  "mm": "လောင်းကြေးဆန်သော ရင်းနှီးမြှုပ်နှံမှု၊ လုပ်ဖော်ကိုင်ဖက်နှင့် အကြံဉာဏ်မှားများကြောင့် ဆုံးရှုံးနိုင်သည်၊ မရင်းနှီးမီ သေချာစုံစမ်းပါ။"}},
    27: {"tone": "ดี", "name": {"th": "คทาแห่งอำนาจ", "en": "The Sceptre", "mm": "ရာဇလှံတံ"},
         "text": {"th": "อำนาจจากสติปัญญา ความคิดสร้างสรรค์ออกดอกออกผล เหมาะผู้นำและผู้สร้างงาน",
                  "en": "Authority through intellect; creative work bears fruit. A number for leaders and builders.",
                  "mm": "ဉာဏ်ပညာဖြင့် သြဇာအာဏာ ရရှိမည်၊ ဖန်တီးမှုလုပ်ငန်းများ အသီးအပွင့်ထွက်မည် — ခေါင်းဆောင်နှင့် တည်ဆောက်သူတို့၏ ဂဏန်း။"}},
    28: {"tone": "ระวัง", "name": {"th": "เริ่มใหม่ซ้ำซาก", "en": "Contradictions", "mm": "ဆန့်ကျင်ကွဲလွဲမှုများ"},
         "text": {"th": "อนาคตดูสดใสแต่เสี่ยงเสียสิ่งที่สร้างมาเพราะไว้ใจคนผิด ต้องมีสัญญา/หลักฐานเสมอ",
                  "en": "Promising outlook but risk of losing what was built through misplaced trust; always keep things in writing.",
                  "mm": "အလားအလာကောင်းသော်လည်း လူမှားယုံ၍ တည်ဆောက်ထားသမျှ ဆုံးရှုံးနိုင်သည်၊ စာချုပ်စာတမ်း အမြဲ ချုပ်ဆိုထားပါ။"}},
    29: {"tone": "ระวัง", "name": {"th": "เมฆหมอกแห่งใจ", "en": "Uncertainties", "mm": "မရေရာမှုများ"},
         "text": {"th": "ระวังความไม่แน่นอน การหลอกลวง และความเศร้าจากคนใกล้ตัว ควรมีหลักยึดทางใจที่มั่นคง",
                  "en": "Beware uncertainty, deception and grief through others; anchor yourself firmly.",
                  "mm": "မရေရာမှု၊ လှည့်ဖြားမှုနှင့် အနီးကပ်ရှိသူများကြောင့် စိတ်ဆင်းရဲမှုကို သတိထားပါ၊ စိတ်ဓာတ်ခိုင်မာအောင် ထိန်းထားပါ။"}},
    30: {"tone": "กลาง", "name": {"th": "นักคิดผู้สันโดษ", "en": "Thoughtful Deduction", "mm": "တွေးခေါ်ဆင်ခြင်သူ"},
         "text": {"th": "ปัญญาเหนือคนทั่วไปแต่ไม่เน้นวัตถุ ผลลัพธ์ขึ้นกับว่าเลือกใช้ความคิดไปทางไหน",
                  "en": "Mental superiority without material drive; outcome depends on how the mind is applied.",
                  "mm": "ထူးချွန်သော ဉာဏ်ရှိသော်လည်း ရုပ်ဝတ္ထုကို အလေးမထားပါ၊ ရလဒ်မှာ ထိုဉာဏ်ကို မည်သို့အသုံးချသည်အပေါ် မူတည်သည်။"}},
    31: {"tone": "กลาง", "name": {"th": "ผู้ยืนลำพัง", "en": "The Recluse", "mm": "အထီးကျန် ပညာရှိ"},
         "text": {"th": "คล้ายเลข 30 แต่โดดเดี่ยวกว่า พึ่งพาตนเองสูง เหมาะสายวิชาการและงานอิสระ",
                  "en": "Like 30 but more self-contained and isolated; suits scholarly and independent work.",
                  "mm": "၃၀ နှင့် ဆင်တူသော်လည်း ပို၍ အထီးကျန်ပြီး ကိုယ့်အားကိုယ်ကိုးတတ်သည် — ပညာရပ်ဆိုင်ရာနှင့် လွတ်လပ်သောလုပ်ငန်းများနှင့် သင့်တော်သည်။"}},
    32: {"tone": "ดี", "name": {"th": "มนตร์สื่อสาร", "en": "Magical Communication", "mm": "ဆက်သွယ်ပြောဆိုမှု အစွမ်း"},
         "text": {"th": "เสน่ห์ดึงดูดมวลชน สื่อสารเก่ง โชคดีเมื่อยึดมั่นความคิดตัวเอง อย่าให้คนอื่นชักจูงง่าย",
                  "en": "Charms crowds and communicates well; fortunate when holding one's own judgment firmly.",
                  "mm": "လူအများကို ဆွဲဆောင်နိုင်ပြီး ဆက်သွယ်ပြောဆိုမှု ကျွမ်းကျင်သည်၊ ကိုယ့်ဆုံးဖြတ်ချက်ကို ခိုင်မာစွာ ဆုပ်ကိုင်ထားလျှင် ကံကောင်းမည်။"}},
    37: {"tone": "ดี", "name": {"th": "มิตรภาพนำโชค", "en": "Fortunate Friendship", "mm": "ကံကောင်းစေသော မိတ်ဆွေ"},
         "text": {"th": "โชคดีด้านความรัก มิตรภาพ และหุ้นส่วน คนรอบตัวคือทรัพย์ที่แท้จริงของเลขนี้",
                  "en": "Good fortune in love, friendship and partnership; people around you are your true wealth.",
                  "mm": "အချစ်ရေး၊ မိတ်ဆွေရေးနှင့် လုပ်ဖော်ကိုင်ဖက်ရေးတွင် ကံကောင်းသည် — ပတ်ဝန်းကျင်ရှိသူများသည်ပင် သင်၏ စစ်မှန်သောဥစ္စာ ဖြစ်သည်။"}},
    43: {"tone": "ระวัง", "name": {"th": "คลื่นปฏิวัติ", "en": "Revolution & Upheaval", "mm": "တော်လှန်ပြောင်းလဲမှု"},
         "text": {"th": "ระวังความล้มเหลวจากการเปลี่ยนแปลงถอนรากและการต่อต้าน ควรค่อยเป็นค่อยไปไม่หักโหม",
                  "en": "Beware failure through radical upheaval and opposition; move gradually, not by force.",
                  "mm": "အမြစ်ပြတ် ပြောင်းလဲမှုနှင့် ဆန့်ကျင်မှုကြောင့် ကျရှုံးနိုင်သည်၊ အတင်းအဓမ္မမဟုတ်ဘဲ တဖြည်းဖြည်း လုပ်ဆောင်ပါ။"}},
    51: {"tone": "ดี", "name": {"th": "นักรบผงาด", "en": "The Warrior", "mm": "စစ်သည်တော်"},
         "text": {"th": "ก้าวหน้าฉับพลันในหน้าที่การงาน เหมาะสายทหาร/ผู้บริหาร แต่ความสำเร็จเร็วย่อมมีคู่แข่ง-ศัตรู ระวังตัวด้วย",
                  "en": "Sudden advancement and power — suits soldiers and leaders; swift success breeds rivals, stay guarded.",
                  "mm": "ရုတ်တရက် ရာထူးတိုးတက်မည် — စစ်ဘက်ဆိုင်ရာနှင့် ခေါင်းဆောင်ပိုင်းအလုပ်များနှင့် သင့်တော်သည်၊ အောင်မြင်မှုမြန်လျှင် ပြိုင်ဘက်နှင့် ရန်သူပေါ်တတ်သဖြင့် သတိထားပါ။"}},
}
_ALIAS = {33: 24, 34: 25, 35: 26, 36: 27, 38: 29, 39: 30, 40: 31, 41: 32,
          42: 24, 44: 26, 45: 27, 46: 37, 47: 29, 48: 30, 49: 31, 50: 32, 52: 43}

COMPOUND = dict(_BASE)
for k, v in _ALIAS.items():
    COMPOUND[k] = _BASE[v]


def _digit_sum(n: int) -> int:
    return sum(int(c) for c in str(n))


def digital_root(n: int) -> int:
    while n > 9:
        n = _digit_sum(n)
    return n if n > 0 else 9


def cheiro_compound(total: int) -> dict:
    """หาเลขผสม Cheiro จากผลรวมเบอร์ (ลดทอนจนอยู่ในช่วง 10-52; ถ้าเหลือเลขโดด = ไม่มีเลขผสม)"""
    t = total
    while t > 52:
        t = _digit_sum(t)
    if t < 10:
        return {"compound": None, "root": digital_root(total)}
    c = COMPOUND[t]
    return {"compound": t, "root": digital_root(total),
            "tone": c["tone"], "name": c["name"], "text": c["text"]}


# ---------- Mulank × รากผลรวมเบอร์ (ตารางมิตร-ศัตรูสายพระเวท/Parashari) ----------
# rel[a] = (friends, enemies) ที่ดาว a "มอง" ดาวอื่น — mapping เลขแบบอินเดีย
_REL = {
    1: ({2, 3, 9}, {4, 6, 8}),   # Sun: มิตร จันทร์/พฤหัส/อังคาร · ศัตรู ราหู/ศุกร์/เสาร์
    2: ({1, 5}, set()),          # Moon: ไม่มีศัตรูธรรมชาติ
    3: ({1, 2, 9}, {5, 6}),      # Jupiter
    4: ({5, 6, 8}, {1, 2, 9}),   # Rahu
    5: ({1, 6}, {2}),            # Mercury
    6: ({5, 8}, {1, 2}),         # Venus
    7: ({6, 9}, {1, 2}),         # Ketu
    8: ({5, 6}, {1, 2, 9}),      # Saturn
    9: ({1, 2, 3}, {5}),         # Mars
}


def _rel_score(a: int, b: int) -> int:
    if a == b:
        return 1  # ดาวเดียวกัน เสริมกันเอง
    f, e = _REL[a]
    return 1 if b in f else (-1 if b in e else 0)


MULANK_VERDICT = {
    2: {"th": "มหามิตร — ผลรวมเบอร์หนุนเลขจิตของคุณเต็มกำลัง ตามคติอินเดียถือว่าส่งเสริมกันดีมาก",
        "en": "Great friends — the number's vibration fully supports your psychic number.",
        "mm": "မဟာမိတ် — ဖုန်းနံပါတ်၏ စွမ်းအင်က သင့်စိတ်ဂဏန်းကို အပြည့်အဝ ထောက်ပံ့သည်။"},
    1: {"th": "มิตร — พลังสองฝั่งไปทางเดียวกัน ใช้เบอร์นี้ได้อย่างราบรื่น",
        "en": "Friendly — both energies flow the same way; a smooth match.",
        "mm": "မိတ်ဆွေ — စွမ်းအင်နှစ်ခု တစ်လမ်းတည်း စီးဆင်းနေသဖြင့် အဆင်ပြေချောမွေ့စွာ သုံးနိုင်သည်။"},
    0: {"th": "เป็นกลาง — ไม่หนุนไม่ขัด ผลของเบอร์ขึ้นกับโครงสร้างคู่เลขเป็นหลัก",
        "en": "Neutral — neither helps nor hinders; the pair structure decides.",
        "mm": "အလယ်အလတ် — မထောက်ပံ့သလို မဆန့်ကျင်ပါ၊ ဂဏန်းအတွဲ ဖွဲ့စည်းပုံက အဓိက ဆုံးဖြတ်မည်။"},
    -1: {"th": "ต้องปรับตัว — พลังคนละสาย ตามคติอินเดียแนะให้เสริมด้วยเลขกลาง (เช่นรากผลรวม 5) ในเบอร์ถัดไป",
         "en": "Needs adjustment — differing currents; Indian custom suggests a neutral root (e.g. 5) next time.",
         "mm": "ညှိနှိုင်းရန် လိုသည် — စွမ်းအင်လမ်းကြောင်း ကွဲပြားနေသဖြင့် နောက်နံပါတ်တွင် အလယ်အလတ် အမြစ်ဂဏန်း (၅) ရှိသည့် နံပါတ်ကို ရွေးရန် အိန္ဒိယဓလေ့က အကြံပြုသည်။"},
    -2: {"th": "คู่ขัด — ตามตำราอินเดียถือว่าดาวเป็นศัตรูกัน หากใช้แล้วรู้สึกติดขัด อาจพิจารณาเบอร์ที่รากผลรวมเป็นมิตรกับเลขจิต",
         "en": "Clashing — the planets are enemies in the Indian system; consider a number whose root befriends your psychic number.",
         "mm": "ဆန့်ကျင်ဘက် — အိန္ဒိယကျမ်းအရ ဂြိုဟ်ချင်း ရန်ဖက်ဖြစ်သည်၊ သင့်စိတ်ဂဏန်းနှင့် မိတ်ဖြစ်သည့် အမြစ်ဂဏန်းရှိသော နံပါတ်ကို ပြောင်းသုံးရန် စဉ်းစားနိုင်သည်။"},
}


def mulank_compat(birth_day_of_month: int, number_total: int) -> dict:
    """ความเข้ากันแบบอินเดีย: เลขจิต (รากของวันที่เกิด 1-31) × รากผลรวมเบอร์"""
    m = digital_root(birth_day_of_month)
    r = digital_root(number_total)
    s = _rel_score(m, r) + _rel_score(r, m)
    s = max(-2, min(2, s))
    # เลข 5 (พุธอินเดีย) เข้าได้กับทุกคน — ยกพื้นไม่ให้ติดลบ
    if 5 in (m, r) and s < 0:
        s = 0
    return {"mulank": m, "root": r, "score": s,
            "verdict": {lg: MULANK_VERDICT[s][lg] for lg in ("th", "en", "mm")},
            "mulank_planet": INDIAN_PLANET[m], "root_planet": INDIAN_PLANET[r]}
