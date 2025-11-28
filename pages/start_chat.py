import streamlit as st
from db import fetch, execute

def start_chat_page():
    friend_id = st.session_state.get("friend_id", None)
    if friend_id is None:
        st.error("친구 ID를 찾을 수 없습니다.")
        return

    my_id = st.session_state.user["user_id"]

    # 1) 기존 채팅방 있는지 확인
    room = fetch("""
        SELECT room_id
        FROM ChatRooms
        WHERE room_id IN (SELECT room_id FROM RoomMembers WHERE user_id=%s)
        AND   room_id IN (SELECT room_id FROM RoomMembers WHERE user_id=%s)
        AND room_name IS NULL
        LIMIT 1
    """, (my_id, friend_id))

    if len(room) > 0:
        room_id = room[0]["room_id"]
        
    else:
        # 새로운 1:1 채팅방 생성
        new_room = execute(
            "INSERT INTO ChatRooms(room_name) VALUES (NULL)",
            return_id=True
        )

        execute(
            "INSERT INTO RoomMembers(room_id, user_id) VALUES (%s, %s)",
            (new_room, my_id)
        )

        execute(
            "INSERT INTO RoomMembers(room_id, user_id) VALUES (%s, %s)",
            (new_room, friend_id)
        )

        room_id = new_room

    # 채팅방 이동
    st.session_state.page = "chat_messages"
    st.session_state.room_id = room_id
    st.rerun()
