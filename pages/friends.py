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
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 1px 4px rgba(0,0,0,0.1);
        }
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
        .friend-info {
            display: flex;
            align-items: center;
        }
        </style>
    """, unsafe_allow_html=True)

    for f in friends:

        col1, col2 = st.columns([7, 2])

        with col1:
            st.markdown(f"""
            <div class="friend-card">
                <div class="friend-info">
                    <div class="profile-img">💛</div>
                    <div>
                        <div style="font-size:18px;font-weight:bold;">{f['username']}</div>
                        <div style="font-size:13px;color:#777;">친구와 1:1 채팅하기</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            # 🔥 진짜 Streamlit 버튼 (이 버튼이 핵심)
            if st.button("채팅 시작", key=f"btn_{f['user_id']}"):
                st.session_state.page = "start_chat"
                st.session_state.friend_id = f["user_id"]
                st.rerun()

    if st.button("⬅ 메인으로"):
        st.session_state.page = "main"
        st.rerun()
