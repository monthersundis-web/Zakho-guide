import streamlit as st

import google.generativeai as genai

from PIL import Image



# --- ڕێکخستنا زیرەکیا دەستکرد ---

if "GEMINI_API_KEY" in st.secrets:

    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

else:

    st.error("کلیلێ API نەهاتیە دیتن د Secrets دا!")

    st.stop()



# --- ستایل و دیزاین ---

st.set_page_config(page_title="ڕێبەرێ زاخۆ", page_icon="🏰")

st.markdown("""

    <style>

    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Arabic&display=swap');

    html, body, [class*="css"] { font-family: 'Noto Sans Arabic', sans-serif; direction: rtl; text-align: right; }

    .stButton>button { width: 100%; border-radius: 10px; background-color: #1e3a8a; color: white; height: 3em; font-weight: bold; }

    .footer { text-align: center; margin-top: 50px; padding: 20px; border-top: 1px solid #ddd; font-size: 14px; }

    </style>

    """, unsafe_allow_html=True)



st.write('<h1 style="text-align: center; color: #1e3a8a;">🏰 ڕێبەرێ زاخۆ یێ زیرەک</h1>', unsafe_allow_html=True)



uploaded_file = st.file_uploader("📸 وێنەیەکێ باربکە", type=["jpg", "jpeg", "png"])



if uploaded_file:

    image = Image.open(uploaded_file)

    st.image(image, use_container_width=True)

    

    if st.button("شلوڤەکرنا وێنەی 🔍"):

        with st.spinner('AI یێ کار دکەت...'):

            # ئەڤە لیستا هەمی مۆدێلێن کو دبیت کار بکەن

            # ئەم دێ ناڤێ مۆدێلی ب تەمامی نڤێسین (models/...) دا 404 نەت

            test_models = [

                'models/gemini-1.5-flash', 

                'models/gemini-1.5-flash-latest', 

                'gemini-1.5-flash',

                'models/gemini-pro-vision'

            ]

            

            success = False

            for m_name in test_models:

                try:

                    model = genai.GenerativeModel(m_name)

                    response = model.generate_content([

                        "تۆ ڕێبەرەکێ گەشتیاری یێ زاخۆیی، ب زمانێ کوردی بەهدینی ڤی وێنەی ناس بکە و مێژوویا وی ب کورتى بێژە.", 

                        image

                    ])

                    if response.text:

                        st.success(f"✅ ئەنجام هاتە دیتن:")

                        st.write(response.text)

                        success = True

                        break

                except Exception:

                    continue

            

            if not success:

                st.error("ببوورە، کێشەیەک د پەیوەندیێ دا هەیا. پشکنینا کلیلێ API بکە.")



# --- فۆتەر (دیزاین ب ناڤێ تە) ---

st.markdown(f"""

    <div class="footer">

        <b>دیزاین و گەشەپێدان: ئەندازیار سندس صبري</b><br>

        پڕۆژەیەک بۆ خزمەتا ئیدارا سەربەخۆیا زاخۆ

    </div>

    """, unsafe_allow_html=True)

