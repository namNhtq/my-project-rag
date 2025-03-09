import streamlit as st
import requests
import os
from config import API_URL  

st.title("Ứng dụng RAG với FastAPI & Streamlit")

query = st.text_input("Nhập câu hỏi của bạn:")

if st.button("Gửi"):
    try:
        response = requests.post(API_URL, json={"query": query})
        if response.status_code == 200:
            st.write("Trả lời:", response.json()["answer"])
        else:
            st.error(f"Lỗi khi gọi API: {response.status_code}")
    except requests.exceptions.RequestException as e:
        st.error(f"Lỗi kết nối API: {e}")
