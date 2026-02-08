import streamlit as st

import google.generativeai as genai

from PIL import Image



# وەرگرتنا کلیلێ API ژ Secrets

if "GEMINI_API_KEY" in st.secrets:

    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

else:

    st.error("کلیلێ API نەهاتیە دیتن د Secrets دا!")



st.set_page_config(page_title="Zakho AI Guide", page_icon="🏰")

st.title("🏰 ڕێبەرێ زیرەکێ زاخۆ")



uploaded_file = st.file_uploader("وێنەیەک باربکە...", type=["jpg", "png", "jpeg"])



if uploaded_file is not None:

    image = Image.open(uploaded_file)

    st.image(image, use_container_width=True)

    

    if st.button("شلوڤەکرنا وێنەی 🔍"):

        with st.spinner('AI یێ بزاڤێ دکەت زانیاریان بدۆزیتەوە...'):

            # ئەڤە لیستەکا ناڤێن مۆدێلانە، سیستەم دێ ئێک ب ئێک تاقی کەت هەتا ئێک کار دکەت

            model_names = ['gemini-1.5-flash', 'gemini-1.5-flash-latest', 'gemini-pro-vision']

            success = False

            

            for m_name in model_names:

                try:

                    model = genai.GenerativeModel(m_name)

                    response = model.generate_content(["تۆ ڕێبەرەکێ گەشتیاری یێ زاخۆیی، ب کوردی بەهدینی مێژوویا ڤی وێنەی ب کورتى بێژە", image])

                    st.success(f"✅ ئەنجام ب مۆدێلێ ({m_name}):")

                    st.write(response.text)

                    success = True

                    break # ئەگەر کار کر، ئێدی ناچیتە سەر یێ دی

                except Exception as e:

                    continue # ئەگەر 404 دا، دێ مۆدێلێ دی تاقی کەت

            

            if not success:

                st.error("ببوورە، چ مۆدێلان کار نەکر. کلیلێ API یان وەشانا لایبرەریێ پشکنی بکە.")



st.info("ئەڤ پڕۆژە هاتییە دروستكرن ژ لایێ ئەندازیار سندس صبري.")

