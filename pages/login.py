import streamlit as st
import bcrypt
from db import fetch

def login_page():
    st.header("🔐 로그인")

    login_id = st.text_input("아이디")
    password = st.text_input("비밀번호", type="password")

    if st.button("로그인"):
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

    if st.button("회원가입"):
        st.session_state.page = "register"
        st.rerun()

def login_test():
    print("This is a test function in login.py")