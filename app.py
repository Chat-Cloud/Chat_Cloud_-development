import streamlit as st
import bcrypt
from db import fetch, execute
from pages.login import login_page
from pages.register import register_page
from pages.home import main_page
from pages.chat_rooms import chat_rooms_page
from pages.chat_messages import chat_messages_page
from pages.profile import profile_page
st.set_page_config(page_title="Messenger Login", layout="centered")

# -----------------------------------------------------
# 세션 상태 초기화 설정
# -----------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "login"
    
    
# -----------------------------------------------------
# 페이지 라우팅
# -----------------------------------------------------
if not st.session_state.logged_in:
    if st.session_state.page == "login":
        login_page()
    elif st.session_state.page == "register":
        register_page()
else:
    # 로그인 상태
    if st.session_state.page == "main":
        main_page()
    elif st.session_state.page == "chat_rooms":
        chat_rooms_page()
    elif st.session_state.page == "chat_messages":
        chat_messages_page()
    elif st.session_state.page == "profile":
        profile_page()
    else:
        main_page()