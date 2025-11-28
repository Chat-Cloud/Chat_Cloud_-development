import streamlit as st

def main_page():
    st.sidebar.title("📌 메뉴")
    menu = st.sidebar.radio("이동", ["홈", "채팅방", "프로필", "로그아웃"])

    if menu == "홈":
        st.title(f"환영합니다, {st.session_state.user['username']}님!")

    elif menu == "채팅방":
        st.session_state.page = "chat_rooms"
        st.rerun()

    elif menu == "프로필":
        st.session_state.page = "profile"
        st.rerun()

    elif menu == "로그아웃":
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.page = "login"
        st.rerun()
