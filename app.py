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

    html, body, [class*="css"] { font-family: 'Noto Sans Arabic', sans-serif; direction: rtl; text-align: right; }

    .stButton>button { width: 100%; border-radius: 12px; height: 3em; background-image: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); color: white; font-weight: bold; border: none; }

    .result-box { background-color: white; padding: 20px; border-radius: 15px; border-right: 5px solid #1e3a8a; box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin-top: 20px; text-align: right; }

    .footer { text-align: center; padding: 20px; color: #666; font-size: 14px; border-top: 1px solid #ddd; margin-top: 50px; }

    </style>

    """, unsafe_allow_html=True)



st.write(f'<h1 style="text-align: center; color: #1e3a8a;">🏰 ڕێبەرێ زاخۆ یێ زیرەک (AI)</h1>', unsafe_allow_html=True)



uploaded_file = st.file_uploader("📸 وێنەیەکێ جهەکێ زاخۆ باربکە", type=["jpg", "jpeg", "png"])



if uploaded_file:

    image = Image.open(uploaded_file)

    st.image(image, use_container_width=True)

    

    if st.button("شلوڤەکرنا وێنەی ب ژیریا دەستکرد 🔍"):

        with st.spinner('⏳ ئەندازیار سندس: AI یێ وێنەی شلوڤە دکەت...'):

            try:

                # مۆدێلێ ٢.٠ بەکار دئینین چونکی د لیستا تە دا یا دیار بوو کو ئەڤە کار دکەت

                # ئەم دێ ناڤێ مۆدێلی ب تەمامی وەک "models/gemini-2.0-flash-exp" نڤێسین

                model = genai.GenerativeModel(model_name='gemini-2.0-flash-exp')

                

                prompt = "تۆ ڕێبەرەکێ گەشتیاری یێ زاخۆیی، ڤی وێنەی ناس بکە و ب زمانێ کوردی بەهدینی مێژوویا وی ب کورتى بێژە."

                

                response = model.generate_content([prompt, image])

                

                st.markdown(f"""

                <div class="result-box">

                    <h3 style="color: #1e3a8a;">📝 ئەنجامێ شلوڤەکرنێ:</h3>

                    <p style="line-height: 1.6; font-size: 18px;">{response.text}</p>

                </div>

                """, unsafe_allow_html=True)

                st.balloons()

                

            except Exception as e:

                # ئەگەر دووبارە 404 دا، دێ ڤێ جارێ وەشانا سادە تاقی کەین

                try:

                    model = genai.GenerativeModel('gemini-1.5-flash')

                    response = model.generate_content([prompt, image])

                    st.write(response.text)

                except Exception as e2:

                    st.error(f"ئاریشەیا تەکنیکی: {e2}")



st.markdown(f"""

    <div class="footer">

        <b>دیزاین و گەشەپێدان ژ لایێ: ئەندازیار سندس صبري</b><br>

        پڕۆژەکێ داهێنەرانە بۆ ئیدارا سەربەخۆیا زاخۆ

    </div>

    """, unsafe_allow_html=True)

