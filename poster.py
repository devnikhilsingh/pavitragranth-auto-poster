import datetime
import time
import requests
from PIL import Image, ImageDraw, ImageFont
from zoneinfo import ZoneInfo
from io import BytesIO

SITE = "www.pavitragranth.com"
DAILY_POSTS = {
  0: {"hindi":"भगवान शिव","english":"Lord Shiva","caption":"🙏 सोमवार का दिन भोलेनाथ के स्मरण और मन को शांत रखने का संदेश देता है।\n\nमहादेव हमें सिखाते हैं कि जीवन में कितनी भी कठिनाइयाँ आएँ, धैर्य, विश्वास और सच्चाई का साथ नहीं छोड़ना चाहिए। शिव जी से प्रार्थना करें कि हमारे मन से चिंता दूर हो, हमें सही निर्णय लेने की बुद्धि मिले और हम हर परिस्थिति में विनम्र बने रहें।\n\nआपके और आपके परिवार के जीवन में सुख, शांति और शिव कृपा बनी रहे।\n\nहर हर महादेव! 🕉️🙏","hashtags":"#Mahadev #HarHarMahadev #ShivBhakti #LordShiva #MondayBlessings #Bhakti #SanatanDharma"},
  1: {"hindi":"हनुमान जी","english":"Lord Hanuman","caption":"🚩 मंगलवार को बजरंगबली का स्मरण साहस, सेवा और अटूट विश्वास की प्रेरणा देता है।\n\nजब जीवन में मुश्किलें आएँ या मन घबराने लगे, तब हनुमान जी से शक्ति और धैर्य की प्रार्थना करें। उनकी भक्ति हमें याद दिलाती है कि सच्चे मन से प्रयास करते रहें, अपने कर्तव्य निभाएँ और प्रभु श्रीराम पर विश्वास बनाए रखें।\n\nबजरंगबली आप सभी को हिम्मत, सद्बुद्धि और अपने परिवार की रक्षा का आशीर्वाद दें।\n\nजय श्री राम! जय हनुमान! 🙏","hashtags":"#JaiHanuman #Bajrangbali #HanumanBhakti #JaiShriRam #TuesdayBlessings #Bhakti #SanatanDharma"},
  2: {"hindi":"भगवान गणेश","english":"Lord Ganesha","caption":"🌺 बुधवार गणपति बप्पा के स्मरण और नई शुरुआत के लिए शुभ भावना रखने का दिन है।\n\nविघ्नहर्ता भगवान गणेश से प्रार्थना करें कि हमारे जीवन की बाधाओं को दूर करने की शक्ति दें, हमें विवेक और धैर्य प्रदान करें और हर काम सोच-समझकर करने की बुद्धि दें।\n\nआज किसी भी नए काम की शुरुआत अच्छे विचार, मेहनत और विश्वास के साथ करें। बप्पा की कृपा आप सभी पर बनी रहे।\n\nगणपति बप्पा मोरया! 🙏","hashtags":"#GanpatiBappa #GaneshBhakti #GaneshJi #Vighnaharta #WednesdayBlessings #Bhakti #SanatanDharma"},
  3: {"hindi":"भगवान विष्णु","english":"Lord Vishnu","caption":"🙏 गुरुवार को श्रीहरि विष्णु का स्मरण हमें धर्म, धैर्य और करुणा के मार्ग पर चलने की प्रेरणा देता है।\n\nभगवान से प्रार्थना करें कि हमारे मन में सद्बुद्धि बनी रहे, हम कठिन परिस्थितियों में भी सही मार्ग चुन सकें और दूसरों के प्रति दया व सम्मान का भाव रखें। जीवन में जो भी जिम्मेदारियाँ मिली हैं, उन्हें ईमानदारी से निभाना भी भक्ति का एक सुंदर रूप है।\n\nश्रीहरि की कृपा से आपके घर में सुख, शांति और मंगल बना रहे।\n\nॐ नमो भगवते वासुदेवाय। 🌼","hashtags":"#JaiShriHari #VishnuBhakti #LordVishnu #OmNamoBhagavateVasudevaya #ThursdayBlessings #Bhakti #SanatanDharma"},
  4: {"hindi":"माँ लक्ष्मी","english":"Goddess Lakshmi","caption":"🌸 शुक्रवार का पावन दिन माँ लक्ष्मी के स्मरण, पूजा और कृतज्ञता व्यक्त करने का सुंदर अवसर है।\n\nमाँ लक्ष्मी केवल धन-समृद्धि ही नहीं, बल्कि सुख, सौभाग्य, शांति और सद्बुद्धि की भी प्रतीक हैं। आइए आज उनसे प्रार्थना करें कि हमारे घरों में प्रेम और शांति बनी रहे, मेहनत का फल मिले और हम जो कुछ प्राप्त करें उसे विनम्रता व उदारता के साथ बाँटना भी सीखें।\n\nअपने जीवन में मिली छोटी-बड़ी खुशियों के लिए आज मन से धन्यवाद करें। माँ लक्ष्मी की कृपा आप सभी और आपके परिवार पर बनी रहे।\n\nजय माँ लक्ष्मी! 🙏🪷","hashtags":"#MaaLakshmi #LakshmiMata #JaiMaaLakshmi #Mahalakshmi #FridayBlessings #LakshmiPuja #Bhakti #SanatanDharma"},
  5: {"hindi":"शनिदेव","english":"Lord Shani","caption":"🙏 शनिवार शनिदेव के स्मरण के साथ ईमानदारी, अनुशासन और अच्छे कर्मों का संकल्प लेने का दिन है।\n\nशनिदेव हमें कर्मों का महत्व, धैर्य और न्याय का संदेश देते हैं। आइए आज अपने व्यवहार पर ध्यान दें, किसी जरूरतमंद की मदद करें और बिना किसी दिखावे के अपने कर्तव्यों को सच्चाई से निभाएँ।\n\nप्रार्थना है कि शनिदेव हमें कठिन समय का सामना करने की शक्ति, सही कर्म करने की बुद्धि और विनम्रता प्रदान करें।\n\nॐ शं शनैश्चराय नमः। 🪔","hashtags":"#ShaniDev #Shanidev #ShaniBhakti #SaturdayBlessings #Karma #Bhakti #SanatanDharma"},
  6: {"hindi":"सूर्य देव","english":"Surya Dev","caption":"☀️ रविवार की सुबह सूर्य देव को नमन करके नई ऊर्जा और सकारात्मक सोच के साथ दिन शुरू करें।\n\nउगते सूर्य की किरणें हमें याद दिलाती हैं कि हर सुबह एक नई शुरुआत लेकर आती है। सूर्य देव से प्रार्थना करें कि हमें स्वास्थ्य, उत्साह, स्पष्ट सोच और अपने लक्ष्य की ओर निरंतर आगे बढ़ने की शक्ति मिले।\n\nआज अपने परिवार और जीवन की अच्छी बातों के लिए कृतज्ञ रहें, और दिन को अच्छे कर्मों से सुंदर बनाएँ।\n\nॐ सूर्याय नमः। 🙏","hashtags":"#SuryaDev #SuryaBhagwan #SundayBlessings #SuryaNamaskar #Bhakti #SanatanDharma"}
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
