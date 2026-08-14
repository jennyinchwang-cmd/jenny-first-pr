# -*- coding: utf-8 -*-
"""ประกอบวงแหวนราศีพม่า 8 วัน (ฉบับหรูหรา) จาก assets/day_*.png
ขอบทองเมทัลลิกไล่เฉด + ลายฉลุ + ดาวระยิบ — ตำแหน่งตามแท่น 8 ทิศชเวดากอง
รัน: python compose_wheel.py → assets/loading_wheel.webp"""
import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

ASSETS = Path(__file__).parent / "assets"
S = 4                 # supersample กันขอบหยัก
SIZE = 1120 * S
CX = CY = SIZE // 2
R_ANIMAL = 400 * S
MEDAL = 224 * S

NAVY_IN = (16, 28, 50)
NAVY_OUT = (7, 12, 24)
GOLD_HI = (255, 214, 130)   # ทองสว่าง
GOLD = (236, 172, 80)
GOLD_MID = (205, 138, 58)
GOLD_DK = (140, 88, 34)     # ทองเงา
EMBER = (255, 190, 110)

PLACEMENT = [
    ("day_sun_garuda.png",    45),   # อาทิตย์ — NE
    ("day_mon_tiger.png",     90),   # จันทร์ — E
    ("day_tue_lion.png",     135),   # อังคาร — SE
    ("day_wed_elephant.png", 180),   # พุธเช้า — S
    ("day_sat_naga.png",     225),   # เสาร์ — SW
    ("day_thu_rat.png",      270),   # พฤหัส — W
    ("day_rahu_elephant.png", 315),  # ราหู — NW
    ("day_fri_guineapig.png",  0),   # ศุกร์ — N
]


def lerp(c1, c2, t):
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))


def metallic_ring(draw, r_out, r_in, steps=48):
    """วงแหวนทองเมทัลลิก: ไล่เฉดสว่าง-เข้มรอบวงเหมือนสะท้อนแสง"""
    for i in range(steps):
        a1 = 360 / steps * i
        a2 = a1 + 360 / steps + 0.6
        # เฉดสะท้อน: สว่างที่มุม 315 (บนซ้าย) เข้มที่ 135
        t = (math.cos(math.radians(a1 - 315)) + 1) / 2
        col = lerp(GOLD_DK, GOLD_HI, t)
        draw.arc((CX - r_out, CY - r_out, CX + r_out, CY + r_out),
                 a1, a2, fill=col, width=r_out - r_in)


def diamond(draw, x, y, s, fill):
    draw.polygon([(x, y - s), (x + s, y), (x, y + s), (x - s, y)], fill=fill)


def main():
    random.seed(9)
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # ---- จานพื้น: ไล่เฉดรัศมี น้ำเงินกลางสว่างขอบเข้ม ----
    Rmax = SIZE // 2 - 6 * S
    for rr in range(Rmax, 0, -2 * S):
        t = rr / Rmax
        col = lerp(NAVY_IN, NAVY_OUT, t)
        d.ellipse((CX - rr, CY - rr, CX + rr, CY + rr), fill=col + (255,))

    # ---- ดาวระยิบพื้นหลัง ----
    for _ in range(260):
        a = random.uniform(0, 2 * math.pi)
        rr = random.uniform(120 * S, Rmax - 20 * S)
        x, y = CX + rr * math.cos(a), CY + rr * math.sin(a)
        s = random.choice([1, 1, 1, 2, 2, 3]) * S // 2 + 1
        alpha = random.randint(70, 220)
        d.ellipse((x - s, y - s, x + s, y + s), fill=EMBER + (alpha,))

    # ---- ขอบนอกเมทัลลิกหนา + เส้นคู่ ----
    metallic_ring(d, Rmax, Rmax - 16 * S)
    d.ellipse((CX - Rmax, CY - Rmax, CX + Rmax, CY + Rmax), outline=GOLD_HI + (200,), width=2 * S)
    r2 = Rmax - 22 * S
    d.ellipse((CX - r2, CY - r2, CX + r2, CY + r2), outline=GOLD_MID + (255,), width=2 * S)

    # ---- แถบลายฉลุรอบวงนอก: เพชร-จุด สลับ ----
    r_dec = Rmax - 40 * S
    for i in range(48):
        a = math.radians(360 / 48 * i)
        x, y = CX + r_dec * math.cos(a), CY + r_dec * math.sin(a)
        if i % 2 == 0:
            diamond(d, x, y, 7 * S, GOLD + (255,))
            diamond(d, x, y, 3 * S, GOLD_HI + (255,))
        else:
            d.ellipse((x - 3 * S, y - 3 * S, x + 3 * S, y + 3 * S), fill=GOLD_MID + (220,))
    r3 = Rmax - 58 * S
    d.ellipse((CX - r3, CY - r3, CX + r3, CY + r3), outline=GOLD_DK + (255,), width=1 * S)

    # ---- วงแหวนในรอบแกน ----
    inner = R_ANIMAL - MEDAL // 2 - 30 * S
    metallic_ring(d, inner + 5 * S, inner - 2 * S)
    core = 140 * S
    metallic_ring(d, core + 7 * S, core - 2 * S)
    core2 = core - 16 * S
    d.ellipse((CX - core2, CY - core2, CX + core2, CY + core2),
              outline=GOLD_MID + (255,), width=1 * S)

    # ---- ซี่ล้อ 8 ซี่ + หัวเพชร ----
    for ang in range(0, 360, 45):
        a = math.radians(ang + 22.5 - 90)
        x1, y1 = CX + (core + 8 * S) * math.cos(a), CY + (core + 8 * S) * math.sin(a)
        x2, y2 = CX + (inner - 6 * S) * math.cos(a), CY + (inner - 6 * S) * math.sin(a)
        d.line((x1, y1, x2, y2), fill=GOLD_DK + (255,), width=7 * S)
        d.line((x1, y1, x2, y2), fill=GOLD + (255,), width=3 * S)
        for rr in (core + 20 * S, inner - 20 * S):
            xx, yy = CX + rr * math.cos(a), CY + rr * math.sin(a)
            diamond(d, xx, yy, 8 * S, GOLD + (255,))
            diamond(d, xx, yy, 4 * S, GOLD_HI + (255,))
        # เม็ดไข่มุกกลางซี่
        xm, ym = CX + ((core + inner) / 2) * math.cos(a), CY + ((core + inner) / 2) * math.sin(a)
        d.ellipse((xm - 5 * S, ym - 5 * S, xm + 5 * S, ym + 5 * S), fill=GOLD_HI + (255,))

    # ---- แกนกลาง: ดอกบัวแฉก 16 กลีบ ----
    for i in range(16):
        a = math.radians(360 / 16 * i)
        x1, y1 = CX + (core2 - 8 * S) * math.cos(a), CY + (core2 - 8 * S) * math.sin(a)
        d.line((CX + 40 * S * math.cos(a), CY + 40 * S * math.sin(a), x1, y1),
               fill=GOLD_DK + (140,), width=2 * S)
    d.ellipse((CX - 34 * S, CY - 34 * S, CX + 34 * S, CY + 34 * S), outline=GOLD + (255,), width=3 * S)
    diamond(d, CX, CY, 18 * S, GOLD + (255,))
    diamond(d, CX, CY, 9 * S, GOLD_HI + (255,))

    # ---- เหรียญสัตว์ 8 ทิศ: กรอบทองเมทัลลิกสองชั้น + แสงหลังเหรียญ ----
    for fname, ang in PLACEMENT:
        im = Image.open(ASSETS / fname).convert("RGBA")
        w, h = im.size
        c = min(w, h)
        im = im.crop(((w - c) // 2, (h - c) // 2, (w + c) // 2, (h + c) // 2))
        im = im.resize((MEDAL, MEDAL), Image.LANCZOS)
        mask = Image.new("L", (MEDAL, MEDAL), 0)
        ImageDraw.Draw(mask).ellipse((0, 0, MEDAL - 1, MEDAL - 1), fill=255)
        im.putalpha(mask)

        a = math.radians(ang - 90)
        x = int(CX + R_ANIMAL * math.cos(a) - MEDAL // 2)
        y = int(CY + R_ANIMAL * math.sin(a) - MEDAL // 2)

        # แสงเรืองหลังเหรียญ
        halo = Image.new("RGBA", (MEDAL + 60 * S,) * 2, (0, 0, 0, 0))
        hd = ImageDraw.Draw(halo)
        hd.ellipse((0, 0, halo.width - 1, halo.height - 1), fill=EMBER + (70,))
        halo = halo.filter(ImageFilter.GaussianBlur(18 * S))
        img.alpha_composite(halo, (x - 30 * S, y - 30 * S))

        img.alpha_composite(im, (x, y))

        # กรอบเมทัลลิกสองชั้น
        fr = Image.new("RGBA", (MEDAL,) * 2, (0, 0, 0, 0))
        fd = ImageDraw.Draw(fr)
        steps = 40
        for i in range(steps):
            a1 = 360 / steps * i
            a2 = a1 + 360 / steps + 0.8
            t = (math.cos(math.radians(a1 - 315)) + 1) / 2
            fd.arc((0, 0, MEDAL - 1, MEDAL - 1), a1, a2, fill=lerp(GOLD_DK, GOLD_HI, t), width=8 * S)
        fd.ellipse((10 * S, 10 * S, MEDAL - 10 * S - 1, MEDAL - 10 * S - 1),
                   outline=GOLD_MID + (255,), width=2 * S)
        img.alpha_composite(fr, (x, y))
        # หมุดเพชรบน-ล่างเหรียญ
        for off in (-1, 1):
            px = x + MEDAL // 2 + int((MEDAL // 2) * math.cos(a)) * 0
            py = y + MEDAL // 2 + off * (MEDAL // 2)
            diamond(d, x + MEDAL // 2, py, 7 * S, GOLD_HI + (255,))

    # ---- ลดขนาด (anti-alias) + เซฟ ----
    out = img.resize((560, 560), Image.LANCZOS)
    out.save(ASSETS / "loading_wheel.webp", "WEBP", quality=90)
    out.save(ASSETS / "loading_wheel_preview.png")
    print("saved:", (ASSETS / 'loading_wheel.webp').stat().st_size // 1024, "KB")


if __name__ == "__main__":
    main()
