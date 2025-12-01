import streamlit as st

def main_page():
    st.sidebar.title("📌 메뉴")
    menu = st.sidebar.radio("메뉴", ["홈", "친구", "채팅방", "프로필", "채팅분석", "로그아웃"])

    if menu == "친구":
        st.session_state.page = "friends"
        st.rerun()
        
    if menu == "홈":
        st.title(f"환영합니다, {st.session_state.user['username']}님!")

    elif menu == "채팅방":
        st.session_state.page = "chat_rooms"
        st.rerun()

    elif menu == "프로필":
        st.session_state.page = "profile"
        st.rerun()
        
    elif menu == "채팅분석":
        st.session_state.page = "chat_dashboard"
        st.rerun()
        
    elif menu == "로그아웃":
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.page = "login"
        st.rerun()
