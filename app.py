import streamlit as st

import google.generativeai as genai

from PIL import Image



# 1. پشکنینا کلیلێ د Secrets دا

if "GEMINI_API_KEY" in st.secrets:

    api_key = st.secrets["GEMINI_API_KEY"]

    genai.configure(api_key=api_key)

else:

    st.error("❌ کلیلێ API د پشکێ Secrets دا نەهاتیە دیتن! کلیلێ دابنە.")

    st.stop()



st.title("🏰 پشکنەرا ئاریشەیا ڕێبەرێ زاخۆ")



uploaded_file = st.file_uploader("وێنەیەک باربکە بۆ پشکنینێ...", type=["jpg", "png", "jpeg"])



if uploaded_file is not None:

    image = Image.open(uploaded_file)

    st.image(image, use_container_width=True)

    

    if st.button("دەستپێکرنا پشکنینا تەکنیکی 🔍"):

        # پێنگاڤا ١: پشکنینا لیستا مۆدێلان

        try:

            st.write("🔄 پێنگاڤا ١: پشکنینا مۆدێلان...")

            models = [m.name for m in genai.list_models()]

            st.write("✅ مۆدێلێن بەردەست بۆ تە:", models)

        except Exception as e:

            st.error(f"❌ ئاریشە د کلیلێ API دا هەیا: {e}")

            st.stop()



        # پێنگاڤا ٢: تاقیکرنا مۆدێلێ Flash ب وێنەیی

        try:

            st.write("🔄 پێنگاڤا ٢: تاقیکرنا ناردنا وێنەی...")

            model = genai.GenerativeModel('gemini-1.5-flash')

            response = model.generate_content(["ئەڤە چیە؟ ب کوردی بێژە", image])

            st.success("🎉 پیرۆزە! کار کر:")

            st.write(response.text)

        except Exception as e:

            st.error(f"❌ ئاریشەیا سەرەکی ئەڤەیە: {e}")

            st.info("ئەگەر ل سەر نڤێسابوو (API key not valid)، واتە کلیلێ تە یێ خەلەتە.")

            st.info("ئەگەر ل سەر نڤێسابوو (User location not supported)، واتە کێشەیا جوگرافی هەیا.")


st.info("ئەڤ پرەژە هاتیە دروستكرن ژ لایێ ئەندازیار سندس صبري ")
