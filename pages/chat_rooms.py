import streamlit as st

import streamlit as st
from db import fetch
import datetime

def chat_rooms_page():

    st.title("💬 채팅방 목록")

    # 채팅방 리스트 가져오기
    rooms = fetch("SELECT room_id, room_name FROM ChatRooms ORDER BY room_id DESC")

    # CSS 스타일 추가
    st.markdown("""
        <style>
        .chat-card {
            padding: 15px;
            border-radius: 12px;
            background-color: #ffffff;
            box-shadow: 0 2px 6px rgba(0,0,0,0.08);
            margin-bottom: 12px;
            display: flex;
            cursor: pointer;
            transition: 0.2s;
        }
        .chat-card:hover {
            background-color: #f8f8f8;
        }
        .chat-profile {
            width: 55px;
            height: 55px;
            border-radius: 20%;
            background-color: #ddd;
            margin-right: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 26px;
            color: #666;
        }
        .chat-info {
            flex-grow: 1;
        }
        .chat-title {
            font-size: 18px;
            font-weight: bold;
        }
        .chat-preview {
            font-size: 14px;
            color: #666;
            margin-top: 3px;
        }
        .chat-time {
            font-size: 12px;
            color: #999;
            text-align: right;
        }
        </style>
    """, unsafe_allow_html=True)


    for r in rooms:

        # 마지막 메시지 가져오기
        last_msg = fetch("""
            SELECT content, created_at FROM Messages 
            WHERE room_id=%s 
            ORDER BY created_at DESC LIMIT 1
        """, (r["room_id"],))

        preview = last_msg[0]["content"] if last_msg else "메시지가 없습니다."
        time = last_msg[0]["created_at"] if last_msg else ""

        # 시간 포맷
        if time:
            time = time.strftime("%m/%d %H:%M")

        # ChatRoom 카드 HTML
        card_html = f"""
        <div class="chat-card" onclick="window.location.href='?page=chat_messages&room_id={r['room_id']}'">
            <div class="chat-profile">💬</div>
            <div class="chat-info">
                <div class="chat-title">{r['room_name']}</div>
                <div class="chat-preview">{preview}</div>
            </div>
            <div class="chat-time">{time}</div>
        </div>
        """

        st.markdown(card_html, unsafe_allow_html=True)

    # 뒤로가기 버튼
    if st.button("⬅ 메인으로"):
        st.session_state.page = "main"
        st.rerun()
