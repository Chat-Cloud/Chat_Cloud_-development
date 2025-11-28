import streamlit as st
from db import fetch, execute

def start_chat_page():
    params = st.experimental_get_query_params()
    friend_id = int(params.get("friend_id",[0])[0])
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
        # 이미 존재하는 방
        room_id = room[0]["room_id"]
    else:
        # 2) 새로운 1:1 채팅방 만들기
        execute("INSERT INTO ChatRooms(room_name) VALUES (NULL)")
        new_room = fetch("SELECT LAST_INSERT_ID() AS id")[0]["id"]

        execute("INSERT INTO RoomMembers(room_id, user_id) VALUES (%s, %s)", (new_room, my_id))
        execute("INSERT INTO RoomMembers(room_id, user_id) VALUES (%s, %s)", (new_room, friend_id))

        room_id = new_room

    # 3) 메시지 페이지로 이동
    st.session_state.page = "chat_messages"
    st.session_state.room_id = room_id
    st.rerun()
