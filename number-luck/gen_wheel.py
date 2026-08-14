# -*- coding: utf-8 -*-
"""เจนรูปวงแหวนราศีพม่า 8 วัน สำหรับหน้ารอผลวิเคราะห์ (loading page)
รัน: python gen_wheel.py   → ได้ assets/zodiac_wheel.png (จัตุรัส 1:1)"""
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

PROMPT = (
    "circular Burmese zodiac wheel mandala, top-down view, 8 sections arranged around "
    "a ring like the eight planetary posts of Shwedagon pagoda, each section contains "
    "a small traditional Burmese temple-art animal: garuda bird, tiger, lion, tusked "
    "elephant, tuskless elephant, rat, guinea pig, naga serpent — drawn as thin elegant "
    "burnt-orange and amber filigree line art with subtle ember glow, ornate Burmese "
    "temple ornament borders between sections, concentric decorative rings with tiny "
    "star dots, empty dark center circle, on deep midnight navy blue background, "
    "mystical sacred astrology instrument, perfectly centered, radially symmetrical, "
    "crisp line art, no text, no letters, no watermark"
)

print("กำลังเจนรูปวงแหวนราศีพม่า (flux-dev, 1:1)...")
res = fal_client.subscribe(
    "fal-ai/flux/dev",
    arguments={"prompt": PROMPT, "image_size": "square_hd", "num_images": 1,
               "num_inference_steps": 40, "guidance_scale": 4.0},
)
url = res["images"][0]["url"]
out = ASSETS / "zodiac_wheel.png"
urllib.request.urlretrieve(url, out)
print(f"บันทึกแล้ว: {out}")
