import streamlit as st
import google.generativeai as genai
from PIL import Image
from gtts import gTTS
import os

# 1. إعداد مفتاح الـ API بشكل آمن
# ملاحظة: عند رفع التطبيق، ضع المفتاح في Settings > Secrets في Streamlit
# باسم: GEMINI_API_KEY
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = "تە_API_KEY_خۆ_ل_ڤێرە_دابنە" # للمعاينة المحلية فقط

genai.configure(api_key=api_key)

# 2. إعدادات الصفحة
st.set_page_config(page_title="Zakho AI Guide", page_icon="🏰", layout="centered")

# تنسيق CSS بسيط لتحسين الخطوط والعرض
st.markdown("""
    <style>
    .main { text-align: right; dir: rtl; }
    .stButton>button { width: 100%; border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏰 ڕێبەرێ زیرەکێ زاخۆ (AI Guide)")
st.subheader("گەشتەکا مێژوویی دگەل زیرەکیا دەستکرد")
st.write("وێنەیەکێ جهەکێ زاخۆ یان دەوربەرێن وێ باربکە دا مێژوویا وێ بزانی.")

# 3. رفع الصور
uploaded_file = st.file_uploader("وێنەیەکێ هەلبژێرە (JPG, PNG)...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # عرض الصورة المرفوعة بشكل أنيق
    image = Image.open(uploaded_file)
    st.image(image, caption='وێنەیێ هاتە بارکرن', use_container_width=True)
    
    submit = st.button("شلوڤەکرنا وێنەی 🔍")

    if submit:
        with st.spinner('AI یێ ل سەر دکۆلیت و زانیاریان کۆم دکەت...'):
            try:
                # 4. موديل Gemini 1.5 Flash
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # برومبت (Prompt) محسن للحصول على أفضل نتيجة
                prompt = """
                تۆ ڕێبەرەکێ گەشتیاری یێ شارەزایی ل باژێرێ زاخۆ. 
                ئەڤ وێنەیە ناس بکە و ئەڤان زانیاریان ب زمانێ کوردی (بەهدینی) بنڤێسە:
                1. ناڤێ جهی.
                2. کورتەیەکا مێژوویی (کەنگی هاتیە ئاڤاکرن).
                3. گرنگیا وی یا گەشتیاری و کولتوری.
                ب شێوەیەکێ جوان و ب خال بنڤێسە.
                """
                
                response = model.generate_content([prompt, image])
                result_text = response.text

                # 5. عرض النتائج بتنسيق جميل
                st.success("✅ زانیاری هاتنە دیتن:")
                st.markdown(f"### ℹ️ پێزانینێن ل دۆر ڤی جهی:")
                st.write(result_text)

                # 6. الجزء الصوتي (Audio)
                # ملاحظة: تم إبقاء التركية كحل مؤقت للنطق، لكن يفضل القراءة حالياً
                tts = gTTS(text=result_text, lang='tr')
                tts.save("zakho_info.mp3")
                
                with open("zakho_info.mp3", "rb") as f:
                    audio_bytes = f.read()
                    st.audio(audio_bytes, format='audio/mp3')
                
                # تنظيف الملف الصوتي المؤقت
                os.remove("zakho_info.mp3")

            except Exception as e:
                st.error(f"بوو مە ئاریشەیەک چێبوو: {e}")

st.divider()
st.info("ئەڤ پڕۆژە وەک دیاریەک پێشکێشە بۆ ئیدارا سەربەخۆیا زاخۆ و گەشتیارێن وێ.")
