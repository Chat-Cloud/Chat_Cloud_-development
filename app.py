import streamlit as st
import bcrypt
from db import fetch, execute
from pages.login import login_page
from pages.register import register_page
from pages.home import main_page
from pages.chat_rooms import chat_rooms_page
from pages.chat_messages import chat_messages_page
from pages.profile import profile_page
from pages.friends import friends_page
from pages.start_chat import start_chat_page
from pages.chat_dashboard import chat_dashboard_page

st.set_page_config(page_title="Messenger", layout="centered")


# 1️⃣ 세션 초기화
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "login"


# 2️⃣ 라우팅 (오직 한 곳에서만 처리)
if not st.session_state.logged_in:

    # 로그인 전
    if st.session_state.page == "login":
        login_page()

    elif st.session_state.page == "register":
        register_page()

else:

    # 로그인 후
    if st.session_state.page == "main":
        main_page()

    elif st.session_state.page == "friends":
        friends_page()

    elif st.session_state.page == "start_chat":
        start_chat_page()

    elif st.session_state.page == "chat_rooms":
        chat_rooms_page()

    elif st.session_state.page == "chat_messages":
        chat_messages_page()

    elif st.session_state.page == "profile":
        profile_page()
    
    # ✅ 새로 추가한 분석 대시보드 메뉴
    elif st.session_state.page == "chat_dashboard":
        chat_dashboard_page()

    else:
        # 기본 페이지
        main_page()