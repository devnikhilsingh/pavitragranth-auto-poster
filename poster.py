import datetime
import time
import requests
from PIL import Image, ImageDraw, ImageFont
from zoneinfo import ZoneInfo
from io import BytesIO

SITE = "www.pavitragranth.com"
DAILY_POSTS = {
  0: {"hindi":"भगवान शिव","english":"Lord Shiva","caption":"🙏 सोमवार की सुबह भोलेनाथ के स्मरण से शुरू करें।\n\nशिव जी हमें सिखाते हैं कि कठिन समय में भी धैर्य रखें, मन शांत रखें और सत्य के मार्ग पर चलते रहें।\n\nमहादेव से प्रार्थना है कि आपके घर में शांति और आपके मन में विश्वास बना रहे। 🕉️\n\nहर हर महादेव! 🙏","hashtags":"#महादेव #हरहरमहादेव #शिवभक्ति #सोमवार #PavitraGranth","prompt":"Premium realistic devotional artwork of Lord Shiva seated peacefully in meditation in the Himalayas, subtle crescent moon, Ganga flowing from his hair, trident nearby, soft dawn light, calm sacred atmosphere, finely detailed traditional iconography, natural colors, portrait 4:5. No text, no watermark, no distorted face or extra limbs."},
  1: {"hindi":"हनुमान जी","english":"Lord Hanuman","caption":"🙏 मंगलवार को बजरंगबली का स्मरण हमें साहस और सेवा का भाव याद दिलाता है।\n\nजब मन कमजोर पड़ने लगे, तो हनुमान जी की भक्ति से शक्ति और हिम्मत पाने की प्रार्थना करें। अपने कर्म सच्चे रखें और विश्वास बनाए रखें।\n\nजय श्री राम। जय हनुमान! 🚩","hashtags":"#जयहनुमान #बजरंगबली #हनुमानभक्ति #मंगलवार #जयश्रीराम #PavitraGranth","prompt":"Premium realistic devotional image of Lord Hanuman in dignified traditional form, standing in a serene temple courtyard holding gada, saffron dhoti, subtle vermilion tilak, warm sunrise rays, detailed stone temple and flowers, respectful iconography, portrait 4:5. No text or watermark, anatomically correct."},
  2: {"hindi":"भगवान गणेश","english":"Lord Ganesha","caption":"🌺 बुधवार को गणपति बप्पा का स्मरण करें।\n\nविघ्नहर्ता से प्रार्थना करें कि हमें विवेक, धैर्य और सही निर्णय लेने की शक्ति दें। हर नई शुरुआत अच्छे विचार और नेक कर्मों के साथ करें।\n\nगणपति बप्पा मोरया! 🙏","hashtags":"#गणपतिबप्पा #गणेशभक्ति #विघ्नहर्ता #बुधवार #PavitraGranth","prompt":"Premium realistic devotional artwork of Lord Ganesha seated gracefully on a lotus pedestal inside a traditional Indian temple, finely detailed sacred form, gentle expression, soft golden morning light, flowers and tasteful offerings, natural rich colors, portrait 4:5. No text, watermark, or distorted features."},
  3: {"hindi":"भगवान विष्णु","english":"Lord Vishnu","caption":"🙏 गुरुवार को श्रीहरि विष्णु का ध्यान करें।\n\nभगवान विष्णु से प्रार्थना करें कि जीवन में संतुलन, सद्बुद्धि और धर्म के मार्ग पर चलने की प्रेरणा मिले। मन में श्रद्धा रखें और दूसरों के प्रति दया का भाव बनाए रखें।\n\nॐ नमो भगवते वासुदेवाय। 🌼","hashtags":"#श्रीहरि #विष्णुभक्ति #ॐनमोभगवतेवासुदेवाय #गुरुवार #PavitraGranth","prompt":"Premium devotional artwork of Lord Vishnu in traditional four-armed form reclining serenely on Sheshnag over cosmic ocean, lotus and conch details, gentle golden and blue light, finely detailed traditional Indian sacred art, calm mood, portrait 4:5. Respectful accurate iconography, no text, watermark, or malformed hands."},
  4: {"hindi":"माँ लक्ष्मी","english":"Goddess Lakshmi","caption":"🌸 शुक्रवार माँ लक्ष्मी के स्मरण और कृतज्ञता का सुंदर अवसर है।\n\nमाँ लक्ष्मी से प्रार्थना करें कि हमारे घरों में सुख-शांति बनी रहे और हमें धन के साथ विनम्रता, उदारता और संतोष भी मिले। जो कुछ मिला है, उसके लिए आज मन से धन्यवाद करें।\n\nजय माँ लक्ष्मी! 🙏","hashtags":"#जयमहालक्ष्मी #माँलक्ष्मी #लक्ष्मीपूजन #शुक्रवार #भक्ति #PavitraGranth","prompt":"Elegant premium devotional image of Goddess Lakshmi seated on a pink lotus, traditional red and gold sari, graceful four arms with lotus flowers and blessing gesture, temple lamps, subtle golden glow, finely detailed sacred artwork, natural lighting, peaceful expression, portrait 4:5. Accurate traditional iconography, no text, watermark, extra fingers or limbs."},
  5: {"hindi":"शनिदेव","english":"Lord Shani","caption":"🙏 शनिवार शनिदेव के स्मरण के साथ अच्छे कर्मों और अनुशासन का संकल्प लेने का दिन है।\n\nशनि देव हमें कर्म, न्याय, धैर्य और विनम्रता का महत्व याद दिलाते हैं। किसी जरूरतमंद की मदद करें और अपने कर्म ईमानदारी से करते रहें।\n\nॐ शं शनैश्चराय नमः। 🪔","hashtags":"#शनिदेव #शनिवार #शनिभक्ति #कर्म #भक्ति #PavitraGranth","prompt":"Respectful traditional devotional artwork of Lord Shani Dev, dignified dark blue complexion, traditional sacred attire and attributes, crow nearby, oil lamps and subtle deep blue-gold lighting, refined realistic sacred painting, peaceful balanced composition, portrait 4:5. No text, watermark, or distorted anatomy."},
  6: {"hindi":"सूर्य देव","english":"Surya Dev","caption":"☀️ रविवार की शुरुआत सूर्य देव को नमन करके करें।\n\nउगते सूर्य की रोशनी हमें हर दिन नई शुरुआत और ऊर्जा का संदेश देती है। आज अपने मन में अच्छे विचार रखें, कृतज्ञ रहें और पूरे उत्साह से अपने काम करें।\n\nॐ सूर्याय नमः। 🙏","hashtags":"#सूर्यदेव #रविवार #सूर्यनमस्कार #ॐसूर्यायनमः #PavitraGranth","prompt":"Beautiful premium traditional devotional artwork of Surya Dev standing in a radiant golden chariot drawn by seven horses at sunrise, dignified traditional Indian iconography, warm dawn sky, temple silhouettes, realistic fine details and natural light, spiritual mood, portrait 4:5. No text, watermark, malformed horses or limbs."}
}
def font():
    for path in ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf","/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"]:
        try: return ImageFont.truetype(path,28)
        except OSError: pass
    return ImageFont.load_default()
def main():
    date=datetime.datetime.now(ZoneInfo("Asia/Kolkata")).date()
    post=DAILY_POSTS[date.weekday()]
    caption=post["caption"]+"\n\n🌐 https://pavitragranth.com\n\n"+post["hashtags"]
    prompt=post["prompt"]+" Leave only subtle clean space at the bottom for a small website signature."
    url="https://image.pollinations.ai/prompt/"+requests.utils.quote(prompt,safe="")
    img=None
    for attempt in range(3):
        try:
            print(f"Requesting image (attempt {attempt+1}/3)...")
            r=requests.get(url,params={"width":1024,"height":1280,"nologo":"true"},timeout=90,headers={"User-Agent":"PavitraGranthDailyPoster/1.0"})
            r.raise_for_status()
            if not r.headers.get("content-type","").startswith("image/"): raise RuntimeError("Image service returned non-image content.")
            img=Image.open(BytesIO(r.content)).convert("RGB"); break
        except Exception as e:
            print(f"Attempt failed: {e}")
            if attempt<2: time.sleep(10*(attempt+1))
    if img is None: raise RuntimeError("Image generation unavailable after 3 attempts. No placeholder will be posted.")
    w,h=img.size
    if w/h>0.8:
        nw=int(h*0.8); x=(w-nw)//2; img=img.crop((x,0,x+nw,h))
    else:
        nh=int(w/0.8); y=(h-nh)//2; img=img.crop((0,y,w,y+nh))
    img=img.resize((1024,1280),Image.Resampling.LANCZOS)
    overlay=Image.new("RGBA",img.size,(0,0,0,0)); d=ImageDraw.Draw(overlay)
    d.rectangle((0,1200,1024,1280),fill=(0,0,0,85))
    img=Image.alpha_composite(img.convert("RGBA"),overlay).convert("RGB")
    draw=ImageDraw.Draw(img); f=font(); b=draw.textbbox((0,0),SITE,font=f)
    draw.text(((1024-(b[2]-b[0]))//2,1224),SITE,font=f,fill="white")
    img.save("post-image.jpg",quality=94)
    with open("caption.txt","w",encoding="utf-8") as f: f.write(caption)
    print(f"Preview created for {date} — {post['hindi']}")
    print("\nCaption preview:\n"+caption)
if __name__=="__main__": main()
