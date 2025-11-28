import streamlit as st
from db import fetch, execute

def friends_page():
    st.title("👥 친구 목록")

    my_id = st.session_state.user["user_id"]

    friends = fetch("""
        SELECT U.user_id, U.username, U.profile_img
        FROM Users U 
        JOIN Friends F ON U.user_id = F.friend_id
        WHERE F.user_id=%s
    """, (my_id,))

    st.markdown("""
        <style>
        .friend-card {
            padding: 12px;
            border-radius: 10px;
            background: white;
            margin-bottom: 10px;
            display: flex;
            cursor: pointer;
            box-shadow: 0 1px 4px rgba(0,0,0,0.1);
        }
        .friend-card:hover { background: #f5f5f5; }
        .profile-img {
            width: 50px; height: 50px;
            border-radius: 18%;
            margin-right: 12px;
            background: #ddd;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 26px;
        }
        </style>
    """, unsafe_allow_html=True)

    for f in friends:
        profile = f["profile_img"] or "😎"

        card = f"""
        <div class="friend-card" onclick="window.location.href='?page=start_chat&friend_id={f['user_id']}'">
            <div class="profile-img">💛</div>
            <div>
                <div style="font-size:18px;font-weight:bold;">{f['username']}</div>
                <div style="font-size:13px;color:#777;">1:1 대화 시작하기</div>
            </div>
        </div>
        """
        st.markdown(card, unsafe_allow_html=True)

    if st.button("뒤로가기"):
        st.session_state.page = "main"
        st.rerun()
