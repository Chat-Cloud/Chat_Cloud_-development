import streamlit as st
import bcrypt
from db import fetch, execute

def register_page():
    st.subheader("회원가입")

    nickname = st.text_input("닉네임")
    login_id = st.text_input("아이디")
    password = st.text_input("비밀번호", type="password")
    profile_img = st.text_input("프로필 이미지 URL (선택)")

    if st.button("회원가입 완료"):
        exists = fetch("SELECT * FROM Users WHERE login_id=%s", (login_id,))
        if len(exists) > 0:
            st.error("이미 사용 중인 아이디입니다.")
            return

        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        execute("""
            INSERT INTO Users(username, login_id, password_hash, profile_img) 
            VALUES (%s, %s, %s, %s)
        """, (nickname, login_id, hashed_pw, profile_img))

        st.success("회원가입 완료!")
        st.session_state.page = "login"
        st.rerun()

def register_test():
    print("This is a test function in register.py")