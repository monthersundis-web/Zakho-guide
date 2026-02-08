import streamlit as st

import google.generativeai as genai

from PIL import Image

import time



# --- ١. ڕێکخستنا زیرەکیا دەستکرد ---

if "GEMINI_API_KEY" in st.secrets:

    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

else:

    st.error("کلیلێ API نەهاتیە دیتن!")

    st.stop()



# --- ٢. دیزاین و ستایل (CSS) ---

st.set_page_config(page_title="ڕێبەرێ زاخۆ یێ زیرەک", page_icon="🏰", layout="centered")



st.markdown("""

    <style>

    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Arabic:wght@400;700&display=swap');

    

    html, body, [class*="css"] {

        font-family: 'Noto Sans Arabic', sans-serif;

        direction: rtl;

        text-align: right;

    }

    .main {

        background-color: #f8f9fa;

    }

    .stButton>button {

        width: 100%;

        border-radius: 12px;

        height: 3em;

        background-image: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);

        color: white;

        font-weight: bold;

        border: none;

        transition: 0.3s;

    }

    .stButton>button:hover {

        transform: scale(1.02);

        box-shadow: 0 4px 15px rgba(0,0,0,0.1);

    }

    .result-box {

        background-color: white;

        padding: 20px;

        border-radius: 15px;

        border-right: 5px solid #1e3a8a;

        box-shadow: 0 2px 10px rgba(0,0,0,0.05);

        margin-top: 20px;

    }

    .footer {

        text-align: center;

        padding: 20px;

        color: #666;

        font-size: 14px;

        border-top: 1px solid #ddd;

        margin-top: 50px;

    }

    </style>

    """, unsafe_allow_html=True)



# --- ٣. ناڤەرۆکا لاپەرەی ---

st.write(f'<h1 style="text-align: center; color: #1e3a8a;">🏰 ڕێبەرێ زاخۆ یێ زیرەک (AI)</h1>', unsafe_allow_html=True)

st.write(f'<p style="text-align: center; color: #555;">پێشکەفتیترین تەکنۆلۆژیا بۆ ناسینەوا شوینوارێن زاخۆ</p>', unsafe_allow_html=True)



uploaded_file = st.file_uploader("📸 وێنەیەکێ جهەکێ زاخۆ باربکە یان بگرە", type=["jpg", "jpeg", "png"])



if uploaded_file:

    image = Image.open(uploaded_file)

    st.image(image, caption='وێنەیێ بارکری', use_container_width=True)

    

    if st.button("شلوڤەکرنا وێنەی ب ژیریا دەستکرد 🔍"):

        with st.spinner('⏳ ئەندازیار سندس: AI یێ ل سەر وێنەی دکۆلیت...'):

            try:

                # تاقیکرنا مۆدێلێ Gemini 2.0 چونکی د لیستا تە دا یا دیار بوو

                model = genai.GenerativeModel('gemini-1.5-flash') # یان gemini-2.0-flash-exp

                

                prompt = """

                تۆ پسپۆرەکێ مێژوویی و ڕێبەرەکێ گەشتیاری یێ زیرەکی ل زاخۆ.

                ڤی وێنەی ناس بکە و ئەڤان زانیاریان ب زمانێ کوردی (بەهدینی) بنڤێسە:

                1. ناڤێ جهی ب شێوەیەکێ دیار.

                2. مێژوویا وی ب کورتی.

                3. گرنگیا وی بۆ زاخۆ.

                ب شێوەیەکێ ئەدەبی و جوان بنڤێسە.

                """

                

                response = model.generate_content([prompt, image])

                

                # نیشاندانا ئەنجامی د ناڤ سندوقەکا جوان دا

                st.markdown(f"""

                <div class="result-box">

                    <h3 style="color: #1e3a8a;">📝 ئەنجامێ شلوڤەکرنێ:</h3>

                    <p style="line-height: 1.6;">{response.text}</p>

                </div>

                """, unsafe_allow_html=True)

                

                st.balloons() # ئاهەنگگێڕان بۆ سەرکەفتنێ

                

            except Exception as e:

                # ئەگەر دووبارە 404 دا، مۆدێلێ دی تاقی دکەت ب شێوەیەکێ ئۆتۆماتیکی

                st.info("🔄 بزاڤەکا دی دکەین...")

                try:

                    model = genai.GenerativeModel('gemini-pro-vision')

                    response = model.generate_content([prompt, image])

                    st.write(response.text)

                except:

                    st.error(f"ببوورە، ئاریشەیەکا تەکنیکی هەیە: {e}")



# --- ٤. فۆتەر (دیزاین ب ناڤێ تە) ---

st.markdown(f"""

    <div class="footer">

        پڕۆژەکێ تەکنۆلۆژی یێ پێشکەفتییە بۆ ئیدارا سەربەخۆیا زاخۆ<br>

        <b>دیزاین و گەشەپێدان ژ لایێ: ئەندازیار سندس صبري</b><br>

        © {time.strftime("%Y")} هەمی ماف دپاراستینە

    </div>

    """, unsafe_allow_html=True)
