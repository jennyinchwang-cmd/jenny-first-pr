# Number Luck — แอปมือถือ (Flutter)

แอปทำนายเบอร์พม่า (พม่า+จีน+อินเดีย · ไทย/EN/မြန်) — เรียกข้อมูลจาก Number Luck API

## โครงสร้าง
```
lib/
  main.dart              ธีมม่วง-ทอง + เก็บภาษาในเครื่อง
  api.dart               ไคลเอนต์เรียก API (แก้ baseUrl ตรงนี้หลัง deploy)
  strings.dart           ป้าย UI 3 ภาษา
  screens/
    home_screen.dart     ใส่เบอร์ + วันเกิด + สลับภาษา
    result_screen.dart   เกรดวงกลม + คู่เลข + คำทำนาย % + ความเข้ากันวันเกิด
assets/                  รูป hero + สัตว์ประจำวัน 8 (จาก FAL.AI)
```

## ⚙️ ก่อน build: ตั้ง URL ของ API
แก้ `lib/api.dart` บรรทัด `baseUrl` เป็น URL จริงหลัง deploy API
(ตอนนี้เป็น placeholder `https://number-luck-api.ondigitalocean.app`)

## 🔨 วิธี build (ต้องมี Flutter SDK)
```bash
# 1) ติดตั้ง Flutter SDK: https://docs.flutter.dev/get-started/install/windows
# 2) ในโฟลเดอร์นี้:
flutter pub get
flutter run                 # ทดสอบบนมือถือ/emulator ที่ต่ออยู่
flutter build apk --release # ได้ไฟล์ build/app/outputs/flutter-apk/app-release.apk
```
เอา APK ไปลงมือถือ Android ได้เลย (แชร์ไฟล์ให้ลูกค้าได้ด้วย) หรือขึ้น Google Play

## หน้าจอที่มีใน MVP นี้ (v1)
- ✅ Home (เบอร์ + วันเกิด + ภาษา)
- ✅ ผลวิเคราะห์ (เกรด + คู่เลข + คำทำนาย + ความเข้ากันวันเกิด 5 ปัจจัย)

## คิวถัดไป (v2)
- หน้าดวงรายสัปดาห์/เดือน (API พร้อมแล้ว: /horoscope/weekly, /monthly)
- หน้าฤกษ์ (/auspicious-days)
- แจ้งเตือนวันมงคล · เก็บโปรไฟล์/ประวัติ · แชร์การ์ดผลเป็นรูป
