import streamlit as st
import bcrypt
from db import fetch, execute
import os
def register_page():
    st.subheader("회원가입")

    nickname = st.text_input("닉네임")
    login_id = st.text_input("아이디")
    password = st.text_input("비밀번호", type="password")
    profile_file = st.file_uploader("프로필 이미지 업로드", type=["jpg", "jpeg", "png"])

    if st.button("회원가입 완료"):
        exists = fetch("SELECT * FROM Users WHERE login_id=%s", (login_id,))
        if len(exists) > 0:
            st.error("이미 사용 중인 아이디입니다.")
            return
         # 폴더 생성
        SAVE_DIR = "profile_images"
        os.makedirs(SAVE_DIR, exist_ok=True)
        
        # 프로필 파일 저장
        file_path = None
        if profile_file:
            file_path = os.path.join(SAVE_DIR, profile_file.name)
            with open(file_path, "wb") as f:
                f.write(profile_file.getbuffer())
        
        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        execute("""
            INSERT INTO Users(username, login_id, password_hash, profile_img) 
            VALUES (%s, %s, %s, %s)
        """, (nickname, login_id, hashed_pw, file_path))

        st.success("회원가입 완료!")
        st.session_state.page = "login"
        st.rerun()

def register_test():
    print("This is a test function in register.py")
    
    