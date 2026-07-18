# Number Luck — Design System "ราตรีส้มทอง" (Night Ember)

แกะโทนจากภาพอ้างอิงสไตล์ horastro: ท้องฟ้ายามค่ำคืนสีกรมท่า + ลายเส้นโหราศาสตร์สีส้มทอง + ฟอนต์ serif หรูๆ

ไฟล์ในโฟลเดอร์นี้:
- `template.html` — หน้าเว็บตัวอย่างเต็มๆ (เปิดในเบราว์เซอร์ได้เลย) มี token + component ครบ
- `streamlit_theme.css` — CSS ก้อนพร้อมใช้ สำหรับฉีดเข้า `app.py` แทนธีมม่วงเดิม
- `DESIGN.md` — ไฟล์นี้

---

## 1. สี (Color Tokens)

| Token | ค่า | ใช้กับ |
|---|---|---|
| `--sky-0` | `#0d1329` | พื้นหลังลึกสุด / navbar |
| `--sky-1` | `#111832` | พื้นหลังหลักของหน้า |
| `--sky-2` | `#1a2244` | การ์ด / แผง |
| `--sky-3` | `#232c52` | การ์ดตอน hover |
| `--line` | `#2c3660` | เส้นขอบการ์ด (บาง 1px) |
| `--ember` | `#e8792e` | **ส้มหลัก** — ปุ่ม, ไฮไลต์, ลายเส้นประดับ |
| `--ember-hi` | `#f2a05c` | ส้มอ่อน — hover, ไอคอน, เรืองแสง |
| `--ember-deep` | `#c2601f` | ส้มเข้ม — ขอบปุ่ม, active |
| `--ivory` | `#f3ead9` | หัวข้อ (ครีมงาช้าง ห้ามใช้ขาวจัด) |
| `--text` | `#c9cfe4` | เนื้อความ |
| `--text-dim` | `#8d95b5` | คำอธิบายรอง |

**กติกา:** ธีมมืดอย่างเดียว (โลกกลางคืนของหมอดู — ตั้งใจเลือก ไม่ทำ light mode) · ส้มคือพระเอกใช้เท่าที่จำเป็น พื้นที่ส่วนใหญ่ให้กรมท่า+ครีมทำงาน · ไล่เฉดปุ่มหลักจาก `--ember-hi` → `--ember` → `--ember-deep` (บน→ล่าง)

## 2. ฟอนต์ (Typography)

| บทบาท | ฟอนต์ | หมายเหตุ |
|---|---|---|
| หัวข้อ (display) | **Playfair Display** (ละติน) + **Trirong** (ไทย) | serif หรู น้ำหนัก 500–700, `line-height:1.18` |
| เนื้อความ | **Sarabun** | น้ำหนัก 300–600, `line-height:1.75` |
| พม่า | **Padauk** | ใส่ต่อท้าย font stack ทั้งสองชุด |

- eyebrow/label: ตัวพิมพ์ใหญ่ + `letter-spacing:.18–.22em` + สีส้มอ่อน
- ตัวเลขเบอร์โทร: ฟอนต์ display + `letter-spacing:.14em` + `font-variant-numeric:tabular-nums`
- Google Fonts link อยู่หัวไฟล์ `template.html`

## 3. ลายเซ็นของธีม (Signature elements)

1. **วงล้อจักรราศีเส้นบางสีส้ม** — วาดด้วย canvas (โค้ดใน template.html) หมุนช้าๆ ใช้เป็น hero art
2. **ดาวระยิบพื้นหลัง** — canvas เต็มจอ จุดเล็กครีม/ส้ม กะพริบเบาๆ (ปิดเมื่อ `prefers-reduced-motion`)
3. **ตัวคั่น section `✦`** — ดาวส้มกลาง + เส้นจางสองข้าง
4. **ไอคอนในวงแหวนเส้นบาง** — วงกลม `border:1.5px solid var(--ember)` ครอบไอคอน
5. **แคปซูลขอบส้ม** (footer) — ใส่โดเมน `ft.jbacworkhub.com`
6. มุมโค้ง `14px` (การ์ด) / `999px` (ชิป, แคปซูล) / `8px` (ปุ่ม)

## 4. วิธีใช้กับแอป Streamlit จริง

1. เปิด `app.py` แทนที่บล็อก `st.markdown("""<style>...""")` เดิม (บรรทัด ~33–53) ด้วย:
   ```python
   from pathlib import Path
   css = Path(__file__).parent / "design" / "streamlit_theme.css"
   st.markdown(f"<style>{css.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)
   ```
2. สร้าง/แก้ `.streamlit/config.toml` ให้พื้นหลังเป็นกรมท่า:
   ```toml
   [theme]
   base = "dark"
   primaryColor = "#e8792e"
   backgroundColor = "#111832"
   secondaryBackgroundColor = "#1a2244"
   textColor = "#c9cfe4"
   font = "sans serif"
   ```
3. component ใหม่ๆ (การ์ดผลลัพธ์, ชิปคู่เลข) ก็อป pattern จาก `template.html` section "ตัวอย่างผลคำพยากรณ์" ได้เลย
