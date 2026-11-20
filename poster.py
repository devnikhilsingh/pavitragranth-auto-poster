import datetime
import random
import time
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

def get_font(size, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for path in paths:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            pass
    return ImageFont.load_default()

def make_fallback(english_name):
    """Create a simple branded devotional-style graphic if the image API is down."""
    width, height = 1024, 1280
    img = Image.new("RGB", (width, height))
    pixels = img.load()
    top = (38, 20, 67)
    bottom = (153, 74, 34)
    for y in range(height):
        t = y / (height - 1)
        color = tuple(int(top[i] * (1-t) + bottom[i] * t) for i in range(3))
        for x in range(width):
            pixels[x, y] = color
    d = ImageDraw.Draw(img, "RGBA")
    # Soft decorative glow and temple-inspired arches.
    d.ellipse((160, 150, 864, 854), fill=(255, 202, 102, 28), outline=(255, 220, 160, 120), width=5)
    d.ellipse((230, 220, 794, 784), outline=(255, 232, 190, 100), width=3)
    d.arc((180, 110, 844, 910), 190, 350, fill=(255, 220, 150, 150), width=8)
    d.polygon([(0,950),(180,820),(340,950),(512,770),(690,950),(850,820),(1024,950),(1024,1280),(0,1280)], fill=(20,12,35,100))
    # Decorative diya-like glow at center.
    d.ellipse((460, 600, 564, 704), fill=(255, 196, 84, 65))
    d.ellipse((480, 620, 544, 684), fill=(255, 218, 145, 120))
    d.polygon([(512,580),(492,640),(512,672),(532,640)], fill=(255,240,185,190))
    # Text
    title_font = get_font(54, True)
    subtitle_font = get_font(30)
    brand_font = get_font(28, True)
    title = english_name
    box = d.textbbox((0,0), title, font=title_font)
    d.text(((width-(box[2]-box[0]))//2, 390), title, font=title_font, fill=(255,245,220,255), stroke_width=1, stroke_fill=(90,40,20,150))
    line = "A moment of devotion"
    box = d.textbbox((0,0), line, font=subtitle_font)
    d.text(((width-(box[2]-box[0]))//2, 475), line, font=subtitle_font, fill=(255,226,175,240))
    d.rectangle((0,1198,width,height), fill=(0,0,0,115))
    box = d.textbbox((0,0), SITE, font=brand_font)
    d.text(((width-(box[2]-box[0]))//2, 1220), SITE, font=brand_font, fill="white")
    return img

def main():
    date = datetime.datetime.now(ZoneInfo("Asia/Kolkata")).date()
    hindi_name, english_name = TOPICS[date.weekday()]
    caption = random.choice(CAPTIONS) + f"\n\n🙏 {hindi_name} का आशीर्वाद सभी पर बना रहे।\n\n🌐 https://pavitragranth.com\n\n#भक्ति #सनातनधर्म #PavitraGranth"
    prompt = (f"Photorealistic devotional image of {english_name}, respectful traditional Hindu iconography, "
              "beautiful Indian temple setting, natural warm light, peaceful sacred mood, marigold flowers, "
              "high quality photography, portrait 4:5 composition, no text, no lettering, no watermark. "
              "Keep the lower edge visually simple for a small website brand label.")
    image_url = "https://image.pollinations.ai/prompt/" + requests.utils.quote(prompt, safe="")
    img = None
    for attempt in range(3):
        try:
            print(f"Trying image service (attempt {attempt + 1}/3)...")
            response = requests.get(image_url, params={"width":1024,"height":1280,"nologo":"true"}, timeout=90)
            response.raise_for_status()
            if not response.headers.get("content-type", "").startswith("image/"):
                raise RuntimeError("Image service returned a non-image response")
            from io import BytesIO
            img = Image.open(BytesIO(response.content)).convert("RGB")
            break
        except Exception as exc:
            print(f"Image service attempt failed: {exc}")
            if attempt < 2:
                time.sleep(8 * (attempt + 1))
    if img is None:
        print("Image provider unavailable. Creating a built-in branded fallback graphic instead.")
        img = make_fallback(english_name)
    # Crop to 4:5 and resize to a consistent post size.
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
    d.rectangle((0,1198,1024,1280), fill=(0,0,0,110))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)
    font = get_font(30)
    bbox = draw.textbbox((0,0), SITE, font=font)
    draw.text(((1024-(bbox[2]-bbox[0]))//2, 1228), SITE, font=font, fill="white")
    img.save("post-image.jpg", quality=92)
    with open("caption.txt", "w", encoding="utf-8") as f:
        f.write(caption)
    print(f"Preview created for {date} — topic: {hindi_name}")
    print(caption)

if __name__ == "__main__":
    main()
