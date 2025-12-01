import streamlit as st
import bcrypt
from db import fetch

def login_page():
    st.header("🔐 로그인")

    # ✅ form으로 묶으면, 마지막 입력창에서 Enter 치면 기본 submit 버튼이 눌린다
    with st.form("login_form", clear_on_submit=False):
        login_id = st.text_input("아이디")
        password = st.text_input("비밀번호", type="password")

        spacer_left, col_login, col_register, spacer_right = st.columns([0.1, 2, 3, 10])
        with col_login:
            login_submitted = st.form_submit_button("로그인")
        with col_register:
            register_submitted = st.form_submit_button("회원가입")

    # ✅ 로그인 버튼(또는 Enter) 눌렀을 때 처리
    if login_submitted:
        user = fetch("SELECT * FROM Users WHERE login_id=%s", (login_id,))

        if len(user) == 0:
            st.error("존재하지 않는 아이디입니다.")
            return

        user = user[0]

        if bcrypt.checkpw(password.encode(), user["password_hash"].encode()):
            st.session_state.logged_in = True
            st.session_state.user = user
            st.success("로그인 성공!")
            st.rerun()
        else:
            st.error("비밀번호가 일치하지 않습니다.")

    # ✅ 회원가입 버튼 눌렀을 때 처리
    if register_submitted:
        st.session_state.page = "register"
        st.rerun()
