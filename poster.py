import datetime
import random
import requests
from PIL import Image, ImageDraw, ImageFont
from zoneinfo import ZoneInfo

SITE = "www.pavitragranth.com"
TOPICS = {
    0: ("भगवान शिव", "Lord Shiva"),
    1: ("हनुमान जी", "Lord Hanuman"),
    2: ("भगवान गणेश", "Lord Ganesha"),
    3: ("भगवान विष्णु", "Lord Vishnu"),
    4: ("माँ लक्ष्मी", "Goddess Lakshmi"),
    5: ("शनिदेव", "Lord Shani"),
    6: ("सूर्य देव", "Lord Surya"),
}

CAPTIONS = [
    "🙏 प्रभु की कृपा से आपके जीवन में सुख, शांति और सकारात्मकता बनी रहे।\n\nआज का दिन श्रद्धा, विश्वास और अच्छे कर्मों से भरपूर हो। ईश्वर आपके हर कदम पर मार्गदर्शन करें। 🌸",
    "🌺 आज प्रभु का स्मरण करें और अपने दिन की शुरुआत कृतज्ञता से करें।\n\nप्रार्थना है कि आपके परिवार में सुख, स्वास्थ्य और शांति बनी रहे। 🙏",
    "🙏 विश्वास बनाए रखें और अच्छे कर्म करते रहें। प्रभु सही समय पर सही मार्ग दिखाते हैं।\n\nआपका आज का दिन मंगलमय हो। 🌼",
]


def main():
    date = datetime.datetime.now(ZoneInfo("Asia/Kolkata")).date()
    hindi_name, english_name = TOPICS[date.weekday()]
    caption = random.choice(CAPTIONS) + f"\n\n🙏 {hindi_name} का आशीर्वाद सभी पर बना रहे।\n\n🌐 https://pavitragranth.com\n\n#भक्ति #सनातनधर्म #PavitraGranth"
    prompt = (f"Photorealistic devotional image of {english_name}, respectful traditional Hindu iconography, "
              "beautiful Indian temple setting, natural warm light, peaceful sacred mood, marigold flowers, "
              "high quality photography, portrait 4:5 composition, no text, no lettering, no watermark. "
              "Keep the lower edge visually simple for a small website brand label.")
    image_url = "https://image.pollinations.ai/prompt/" + requests.utils.quote(prompt, safe="")
    response = requests.get(image_url, params={"width":1024,"height":1280,"nologo":"true"}, timeout=180)
    response.raise_for_status()
    if not response.headers.get("content-type", "").startswith("image/"):
        raise RuntimeError("Image service did not return an image")
    with open("post-image.jpg", "wb") as f:
        f.write(response.content)
    img = Image.open("post-image.jpg").convert("RGB")
    # Crop to 4:5 and resize for a consistent poster.
    w, h = img.size
    if w / h > 0.8:
        new_w = int(h * 0.8); x = (w - new_w) // 2
        img = img.crop((x, 0, x + new_w, h))
    else:
        new_h = int(w / 0.8); y = (h - new_h) // 2
        img = img.crop((0, y, w, y + new_h))
    img = img.resize((1024,1280), Image.Resampling.LANCZOS)
    overlay = Image.new("RGBA", img.size, (0,0,0,0))
    d = ImageDraw.Draw(overlay)
    d.rectangle((0,1210,1024,1280), fill=(0,0,0,110))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
        bbox = draw.textbbox((0,0), SITE, font=font)
        draw.text(((1024-(bbox[2]-bbox[0]))//2, 1228), SITE, font=font, fill="white")
    except OSError:
        draw.text((430,1235), SITE, fill="white")
    img.save("post-image.jpg", quality=92)
    with open("caption.txt", "w", encoding="utf-8") as f:
        f.write(caption)
    print(f"Preview created for {date} — topic: {hindi_name}")
    print(caption)

if __name__ == "__main__":
    main()
