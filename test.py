from dotenv import load_dotenv
import streamlit as st
import os
# .env 파일 불러오기
# 현재 파일(db.py)이 있는 위치에서 .env 절대경로 지정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, ".env")

# print("ENV_PATH:", ENV_PATH)
# print("File exists:", os.path.exists(ENV_PATH))

# with open(ENV_PATH, "rb") as f:
#     print("Raw bytes:", f.read())

# with open(ENV_PATH, "r", encoding="utf-8") as f:
#     print("Text:", f.read())

# load_dotenv(ENV_PATH)

# print("DB_HOST =", os.getenv("DB_HOST"))
# print("DB_USER =", os.getenv("DB_USER"))
# print("DB_PASSWORD =", os.getenv("DB_PASSWORD"))
# print("DB_DATABASE =", os.getenv("DB_DATABASE"))

# from pages.login import login_page
# from pages.login import login_test

# # import sys
# # print(sys.path)  # 현재 파이썬 경로 출력
# from pages.register import register_page


# from pages.register import register_test

# from pages.home import main_page

# from pages.chat_messages import chat_messages_page
# from pages.chat_rooms import chat_rooms_page
# from pages.profile import profile_page
# from db import fetch, execute

import requests
from PIL import Image
from io import BytesIO

url = "https://raw.githubusercontent.com/Chat-Cloud/Chat_Cloud_-development/main/profile_images/Gemini_Generated_Image_hvto3ghvto3ghvto.png"

st.image(url, width=200)

