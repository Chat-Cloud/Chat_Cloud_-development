import streamlit as st
from  db import fetch, execute

st.title("📱 Messenger Project - Users CRUD")

menu = ["Read (전체 조회)", "Create (추가)", "Update (수정)", "Delete (삭제)"]
choice = st.sidebar.selectbox("메뉴 선택", menu)

# ------------------------------------------
# READ
# ------------------------------------------
if choice == "Read (전체 조회)":
    st.header("👤 사용자 목록 조회")
    df = fetch("SELECT * FROM Users")
    st.dataframe(df)

# ------------------------------------------
# CREATE
# ------------------------------------------
elif choice == "Create (추가)":
    st.header("➕ 새로운 사용자 추가")

    username = st.text_input("Username")
    profile_img = st.text_input("프로필 이미지 URL (선택)")

    if st.button("추가"):
        execute(
            "INSERT INTO Users(username, profile_img) VALUES (%s, %s)",
            (username, profile_img)
        )
        st.success(f"{username} 추가 완료!")

# ------------------------------------------
# UPDATE
# ------------------------------------------
elif choice == "Update (수정)":
    st.header("✏ 사용자 정보 수정")

    df = fetch("SELECT * FROM Users")
    user_list = df["user_id"].tolist()

    user_id = st.selectbox("수정할 사용자 ID", user_list)

    new_username = st.text_input("새 username")
    new_profile_img = st.text_input("새 프로필 이미지 URL")

    if st.button("수정"):
        execute(
            "UPDATE Users SET username=%s, profile_img=%s WHERE user_id=%s",
            (new_username, new_profile_img, user_id)
        )
        st.success("수정 완료!")

# ------------------------------------------
# DELETE
# ------------------------------------------
elif choice == "Delete (삭제)":
    st.header("🗑 사용자 삭제")

    df = fetch("SELECT * FROM Users")
    user_list = df["user_id"].tolist()
    
    user_id = st.selectbox("삭제할 사용자 ID", user_list)

    if st.button("삭제"):
        execute(
            "DELETE FROM Users WHERE user_id=%s",
            (user_id,)
        )
        st.error(f"{user_id}번 사용자 삭제 완료!")
