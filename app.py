import streamlit as st
import google.generativeai as genai

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

st.title("اختبار Gemini")

model = genai.GenerativeModel("gemini-pro")
response = model.generate_content("اكتب ترحيب بزاخو بالكردي")
st.write(response.text)
