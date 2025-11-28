import streamlit as st
from db import fetch, execute
from datetime import datetime
import html

def chat_messages_page():
    st.set_page_config(layout="wide")

    # 1) room_id 가져오기
    room_id = st.session_state.get("room_id", None)
    if room_id is None:
        st.error("채팅방 정보를 찾을 수 없습니다.")
        return

    my_id = st.session_state.user["user_id"]

    st.markdown("<h2>💬 채팅</h2>", unsafe_allow_html=True)

    # 2) 메시지 불러오기
    messages = fetch("""
        SELECT M.message_id, M.user_id, M.content, M.created_at, U.username
        FROM Messages M
        JOIN Users U ON M.user_id = U.user_id
        WHERE M.room_id=%s
        ORDER BY M.created_at ASC
    """, (room_id,))

    # 3) CSS 버블 스타일
    st.markdown("""
        <style>
        .msg-left {
            background: #ffffff;
            padding: 10px 14px;
            border-radius: 12px;
            margin-bottom: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            max-width: 65%;
        }
        .msg-right {
            background: #DCF8C6; /* 카카오톡 녹색 버블 */
            padding: 10px 14px;
            border-radius: 12px;
            margin-bottom: 10px;
            margin-left: auto;
            max-width: 65%;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .username {
            font-size: 12px;
            color: #555;
        }
        .time {
            font-size: 10px;
            color: #999;
            text-align: right;
        }
        </style>
    """, unsafe_allow_html=True)

    # 4) 메시지 표시
    for msg in messages:

        bubble = "msg-right" if msg["user_id"] == my_id else "msg-left"


        # 메시지 내용 Escape (핵심)
        content = html.escape(msg["content"])

        time_str = msg["created_at"].strftime("%H:%M")

        st.markdown(f"""
            <div class='{bubble}'>
                <span>{content}</span>
                <div class='time'>{time_str}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # 5) 메시지 입력 UI
    new_message = st.text_input("메시지 입력", key="chat_input")

    if st.button("전송"):
        if new_message.strip() != "":
            # DB 저장
            execute("""
                INSERT INTO Messages(room_id, user_id, content, message_type)
                VALUES (%s, %s, %s, 'text')
            """, (room_id, my_id, new_message))
            st.rerun()

    if st.button("⬅ 채팅방 목록으로"):
        st.session_state.page = "chat_rooms"
        st.rerun()
