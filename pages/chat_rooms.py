import streamlit as st

def chat_rooms_page():
    st.header("💬 채팅방 목록")
    st.write("아직 구현 중!")

    if st.button("메인으로"):
        st.session_state.page = "main"
        st.rerun()
