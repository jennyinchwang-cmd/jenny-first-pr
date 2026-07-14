# Deploy Number Luck ขึ้น ft.jbacworkhub.com (DigitalOcean App Platform)

แนวเดียวกับ sales-dashboard ที่ deploy ไว้แล้ว

## 1) Push โค้ดขึ้น GitHub
โฟลเดอร์ `number-luck/` ในรีโป `jennyinchwang-cmd/jenny-first-pr` (branch master)

## 2) สร้าง App ใหม่บน DO App Platform
- Source: GitHub repo `jennyinchwang-cmd/jenny-first-pr`, branch `master`
- **Source Directory:** `number-luck`
- **Run Command:**
  ```
  streamlit run app.py --server.port 8080 --server.address 0.0.0.0 --server.headless true
  ```
- **HTTP Port:** `8080`
- Instance: Basic (512MB) พอ — แอปไม่มี database ไม่มี external API
- ไม่ต้องตั้ง Environment Variables (ยังไม่มี secret; ถ้าจะใส่รหัสผ่านกั้นค่อยเพิ่ม `APP_PASSWORD` ทีหลัง)

## 3) ผูกโดเมน ft.jbacworkhub.com
- ใน App → Settings → Domains → Add Domain: `ft.jbacworkhub.com`
- ไปที่ DNS ของ jbacworkhub.com เพิ่ม **CNAME**: `ft` → ค่า target ที่ DO แสดง (เช่น `xxxx.ondigitalocean.app`)
- รอ SSL ออกอัตโนมัติ (~ไม่กี่นาที)

## หมายเหตุ
- ไฟล์ที่ต้องอยู่ใน number-luck/: app.py, scorer.py, our_model.json, meanings.py,
  extra.py, burmese.py, mmcal.py, i18n.py, report.py, requirements.txt
- โฟลเดอร์ data/ กับ research/ ไม่จำเป็นบนเซิร์ฟเวอร์ (แต่ push ไปด้วยได้ ไม่หนัก)
- อัปเดตเว็บครั้งถัดไป: push ขึ้น master → DO auto-deploy
