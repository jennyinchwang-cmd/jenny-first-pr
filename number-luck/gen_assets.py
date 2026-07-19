# -*- coding: utf-8 -*-
"""สร้างรูปประกอบแอป Number Luck ด้วย FAL.AI — สัตว์ประจำวันเกิด 8 ทิศ + ภาพหลัก
รัน: python gen_assets.py   (ผลลัพธ์ลง number-luck/assets/)"""
import os
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dotenv import load_dotenv

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

load_dotenv(Path(__file__).parent.parent / ".env")
import fal_client

ASSETS = Path(__file__).parent / "assets"
ASSETS.mkdir(exist_ok=True)

# ธีม "ราตรีส้มทอง" — เส้นสายส้มทองเผาบนกรมท่ากลางคืน (ดู design/DESIGN.md)
STYLE = ("ornate emblem in traditional Burmese temple art style, thin elegant burnt-orange "
         "and amber filigree line art with subtle ember glow, on deep midnight navy blue "
         "night sky background, a few tiny stars, mystical and sacred, perfectly centered, "
         "symmetrical composition, app icon style, no text, no letters")

IMAGES = {
    "day_sun_garuda":      f"majestic Garuda mythical bird with spread wings, {STYLE}",
    "day_mon_tiger":       f"noble tiger standing proudly in profile, {STYLE}",
    "day_tue_lion":        f"regal Burmese lion (chinthe) sitting upright, {STYLE}",
    "day_wed_elephant":    f"elephant with large tusks walking gracefully, {STYLE}",
    "day_rahu_elephant":   f"tuskless elephant with raised trunk, {STYLE}",
    "day_thu_rat":         f"small elegant rat sitting alertly, {STYLE}",
    "day_fri_guineapig":   f"cute round guinea pig, {STYLE}",
    "day_sat_naga":        f"coiled naga serpent dragon with crown, {STYLE}",
    "hero_banner":         ("mystical astrology zodiac wheel drawn in thin burnt-orange filigree "
                            "line art, crescent moon phases and small stars, golden pagoda "
                            "silhouette, soft glowing ember clouds on deep midnight navy night "
                            "sky, elegant fortune telling atmosphere, wide banner composition, "
                            "no text, no letters"),
}


def main():
    if not os.getenv("FAL_KEY", "").strip():
        sys.exit("no FAL_KEY in .env")
    for name, prompt in IMAGES.items():
        dest = ASSETS / f"{name}.png"
        if dest.exists():
            print(f"skip (มีแล้ว): {name}")
            continue
        size = "landscape_16_9" if name == "hero_banner" else "square_hd"
        print(f"🎨 {name} …")
        result = fal_client.subscribe(
            "fal-ai/flux/dev",
            arguments={"prompt": prompt, "image_size": size, "num_images": 1},
            with_logs=False,
        )
        urllib.request.urlretrieve(result["images"][0]["url"], dest)
        print(f"   ✅ {dest.name}")
    print("เสร็จทั้งหมด → number-luck/assets/")


if __name__ == "__main__":
    main()
