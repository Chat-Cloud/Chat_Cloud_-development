import streamlit as st
import streamlit.components.v1 as components
from db import fetch, execute
import html
from streamlit_javascript import st_javascript
# 한 번만 wide 설정
st.set_page_config(layout="wide")
    
def chat_messages_page():
    

    # ===== 기본 세션 체크 =====
    room_id = st.session_state.get("room_id")
    if room_id is None:
        st.error("채팅방 정보를 찾을 수 없습니다.")
        return

    my_id = st.session_state.user["user_id"]

    # ===== 상대 이름 =====
    friend = fetch("""
        SELECT U.username
        FROM RoomMembers R
        JOIN Users U ON R.user_id = U.user_id
        WHERE R.room_id=%s AND R.user_id != %s
    """, (room_id, my_id))
    friend_name = friend[0]["username"] if friend else "상대방"

    # ===== 메시지 불러오기 =====
    messages = fetch("""
        SELECT M.message_id, M.user_id, M.content, M.created_at, U.username
        FROM Messages M
        JOIN Users U ON M.user_id = U.user_id
        WHERE M.room_id=%s
        ORDER BY M.created_at ASC
    """, (room_id,))

    # ===== 메시지를 HTML로 누적 =====
    html_messages = ""
    for msg in messages:
        me = (msg["user_id"] == my_id)
        content = html.escape(msg["content"])
        time_str = msg["created_at"].strftime("%H:%M")

        wrapper = "msg-right" if me else "msg-left"
        color = "#DCF8C6" if me else "#FFFFFF"

        html_messages += f"""
        <div class="{wrapper}">
            <div class="bubble" style="background:{color};">
                <div>{content}</div>
                <div class="time">{time_str}</div>
            </div>
        </div>
        """

    # ===== 스크롤박스 HTML =====
    chat_html = f"""
    <html>
    <head>
    <style>
        body {{
            margin: 0;
            font-family: Arial, sans-serif;
        }}

        .messages-box {{
            height: 60vh;
            overflow-y: auto;
            padding: 10px 8px;
            background: rgba(255,255,255,0.04);
            border-radius: 12px;
        }}

        .msg-left {{
            display: flex;
            justify-content: flex-start;
            margin: 6px 0;
            padding-left: 4px;
        }}
        .msg-right {{
            display: flex;
            justify-content: flex-end;
            margin: 6px 0;
            padding-right: 4px;
        }}

        .bubble {{
            max-width: 65%;
            padding: 10px 14px;
            border-radius: 14px;
            word-break: break-word;
            font-size: 15px;
            color: #000;
        }}

        .time {{
            font-size: 10px;
            color: #555;
            margin-top: 4px;
            text-align: right;
        }}
    </style>
    </head>
    <body>
        <div class="messages-box" id="box">
            {html_messages}
        </div>
        <script>
            var box = document.getElementById("box");
            if (box) {{
                box.scrollTop = box.scrollHeight;
            }}
        </script>
    </body>
    </html>
    """

    # ===== 입력값 세션 초기화 =====
    if "chat_input" not in st.session_state:
        st.session_state.chat_input = ""

    # ===== 전송 콜백 함수 (rerun은 Streamlit이 자동) =====
    def send_message():
        text = st.session_state.chat_input.strip()
        if text:
            execute("""
                INSERT INTO Messages(room_id, user_id, content, message_type)
                VALUES (%s, %s, %s, 'text')
            """, (room_id, my_id, text))
        # 전송 후 입력창 비우기
        st.session_state.chat_input = ""

    # ===== 중앙 고정 컨테이너 (레이아웃 변동 최소화) =====
    st.markdown(
        """
        <style>
        .chat-wrapper {
            max-width: 900px;
            margin: 0 auto;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    with st.container():
        st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)

        # 제목
        st.markdown(f"<h2>💬 {friend_name}님과 채팅</h2>", unsafe_allow_html=True)

        # 스크롤 박스 (고정 height)
        components.html(chat_html, height=400, scrolling=False)

        st.markdown("---")

        # 입력창
        new_message = st.text_area(
            "메시지 입력",
            key="chat_input",
            height=120,
            placeholder="메시지를 입력하세요...",
        )
        # 엔터키 감지: JS → Python 이벤트
        enter_pressed = st_javascript("""
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                // shift+enter는 줄바꿈
                e.preventDefault();
                return true;  // Streamlit에 신호 보내기
            }
        });
        """)

        # 엔터 누르면 send_message 실행
        if enter_pressed:
            send_message()

        # 버튼 줄 (폭 고정용)
        b1, b2 = st.columns([3, 1])
        with b1:
            st.button("전송", on_click=send_message)
        with b2:
            if st.button("⬅ 채팅방 목록으로"):
                st.session_state.page = "chat_rooms"

        st.markdown("</div>", unsafe_allow_html=True)
