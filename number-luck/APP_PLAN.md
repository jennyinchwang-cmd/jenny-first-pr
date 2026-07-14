# พิมพ์เขียวแอปมือถือ Number Luck (Flutter)

> เป้าหมาย: แอป Android (ก่อน) + iOS + เว็บ จากโค้ด Flutter ชุดเดียว
> หลังบ้าน: `api.py` (FastAPI — เสร็จแล้ว ทดสอบครบทุก endpoint)

## สถาปัตยกรรม
```
[Flutter App] ──HTTP──> [FastAPI api.py] ──> โมดูลเดิมทั้งหมด
 Android/iOS             (deploy เป็น            scorer / meanings / extra /
                          component ที่ 2         burmese / mmcal / horoscope /
                          บน DO app เดิม)         i18n (3 ภาษา)
```
- API ตอบ JSON พร้อมข้อความ 3 ภาษาแล้ว → แอปแค่แสดงผล ไม่ต้อง反คำนวณเอง
- เว็บ Streamlit ยังอยู่คู่กัน (ลูกค้าเว็บ) — สองหน้าบ้านใช้สมองเดียวกัน

## หน้าจอ (v1 — 6 หน้า)
1. **Home** — hero_banner + ช่องใส่เบอร์ + ปุ่มวิเคราะห์ + สลับภาษา (th/en/mm)
2. **ผลวิเคราะห์เบอร์** — เกรดวงกลมใหญ่ + การ์ดคู่เลข + คำทำนาย % (จาก /analyze)
3. **ดวงของฉัน** — ใส่วันเกิดครั้งเดียว (เก็บในเครื่อง) → รูปสัตว์ประจำวัน + บทสรุป 5 ปัจจัย + มหาโพติ
4. **ดวงรายสัปดาห์/เดือน** — จาก /horoscope/* + ปฏิทินจุดสีวันดี/ระวัง
5. **ฤกษ์** — /auspicious-days + (อนาคต) ฤกษ์กิจการจีน-พม่า
6. **ดวงคู่/เบอร์คู่** — /couple

## ฟีเจอร์แอปที่เว็บทำไม่ได้ (จุดขาย)
- 🔔 **แจ้งเตือนเช้าวันยัตยาซา/วันดีประจำสัปดาห์** (ดึงผู้ใช้กลับเข้าแอป)
- 💾 เก็บโปรไฟล์วันเกิด + ประวัติเบอร์ที่เคยดู (ในเครื่อง, ไม่ต้องมีบัญชี)
- 📤 แชร์การ์ดผลดวงเป็นรูป (ไปตลาด Facebook/Viber ของพม่า)

## Assets ที่มีแล้ว (assets/ — สร้างด้วย FAL.AI flux-dev, สไตล์ทอง-ม่วง)
- hero_banner.png + สัตว์ประจำวัน 8 รูป (garuda/tiger/lion/elephant×2/rat/guineapig/naga)
- คิวถัดไป: ไอคอนแอป, การ์ดแชร์, ภาพประกอบดาว 0-9

## ขั้นตอนที่เหลือ (ตามลำดับ)
1. Deploy `api.py` เป็น component ที่ 2 บน DO (run: `uvicorn api:app --host 0.0.0.0 --port 8080`)
2. ติดตั้ง Flutter SDK บนเครื่อง → `flutter create number_luck_app`
3. ทำหน้า Home + ผลวิเคราะห์ก่อน (MVP) → ทดสอบบนมือถือจริงผ่าน APK
4. สมัคร Google Play Console ($25) → internal testing → เปิดจริง
5. เฟส iOS: Apple Developer ($99/ปี) + cloud build (Codemagic)

## หมายเหตุเทคนิค
- fastapi + uvicorn ยังไม่ได้เพิ่มใน requirements.txt ของ DO (เพิ่มตอน deploy API จริง
  หรือแยก requirements-api.txt เพื่อไม่ให้ Streamlit component หนักขึ้น)
- แอปควร cache ผล /auspicious-days รายวัน ลด load เซิร์ฟเวอร์
