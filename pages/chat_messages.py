import streamlit as st
import bcrypt
from db import fetch

def chat_messages_page():
    import streamlit as st

    st.header("💬 채팅 메시지")
    st.write("아직 구현 중!")

    if st.button("메인으로"):
        st.session_state.page = "main"
        st.rerun()