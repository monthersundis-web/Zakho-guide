import streamlit as st
import google.generativeai as genai
from PIL import Image
from gtts import gTTS
import io
import os

# ======================
# API KEY
# ======================
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    st.error("⚠️ GEMINI_API_KEY غير موجود في Streamlit Secrets")
    st.stop()

genai.configure(api_key=api_key)

# ======================
# Page settings
# ======================
st.set_page_config(
    page_title="Zakho AI Guide",
    page_icon="🏰",
    layout="centered"
)

st.markdown("""
<style>
.main { text-align: right; direction: rtl; }
.stButton>button { width: 100%; border-radius: 20px; }
</style>
""", unsafe_allow_html=True)

st.title("🏰 ڕێبەرێ زیرەکێ زاخۆ")
st.subheader("گەشتەکا مێژوویی دگەل زیرەکیا دەستکرد")
st.write("وێنەیەکێ جهەکێ مێژوویی ل زاخۆ باربکە دا بۆ زانیاریێن تەواو.")

# ======================
# Upload image
# ======================
uploaded_file = st.file_uploader(
    "وێنەیەکێ هەلبژێرە (JPG, PNG)",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="وێنەیێ هاتە بارکرن", use_container_width=True)

    if st.button("🔍 شلوڤەکرنا وێنەی"):
        with st.spinner("AI ل سەر وێنەی دکۆلیت و زانیاریان کۆم دکەت..."):
            try:
                # ======================
                # Convert image to bytes
                # ======================
                img_bytes_io = io.BytesIO()
                image.save(img_bytes_io, format="JPEG")
                img_bytes = img_bytes_io.getvalue()

                # ======================
                # Gemini Vision model (STABLE)
                # ======================
                model = genai.GenerativeModel("gemini-pro-vision")

                prompt = """
                تۆ ڕێبەرەکێ گەشتیاری یێ شارەزایی ل باژێرێ زاخۆ.
                ئەڤ وێنەیە ناس بکە و ب زمانێ کوردی (بەهدینی) ئەڤان خاڵان ڕوون بکە:
                - ناڤێ جهی
                - کورتەیەکا مێژوویی (کەنگی هاتیە ئاڤاکرن)
                - گرنگیا وی یا گەشتیاری و کولتوری
                بنڤێسە ب شێوەیەکێ سادە و جوان.
                """

                response = model.generate_content([
                    prompt,
                    {
                        "mime_type": "image/jpeg",
                        "data": img_bytes
                    }
                ])

                result = response.text

                st.success("✅ زانیاری هاتنە دیتن")
                st.markdown(result)

                # ======================
                # Optional Audio
                # ======================
                if st.checkbox("🔊 گوهدارن (تجريبي)"):
                    tts = gTTS(result, lang="en")
                    tts.save("temp.mp3")
                    st.audio("temp.mp3")
                    os.remove("temp.mp3")

            except Exception as e:
                st.error(f"❌ هەڵە چێبوو: {e}")

st.divider()
st.info("ئەم پڕۆژە بۆ گەشتیارێن زاخۆ و پێشخستنا شارێ زاخۆیە 🌿")
