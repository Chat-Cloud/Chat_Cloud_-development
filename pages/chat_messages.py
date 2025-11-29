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
            height: 70vh;
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

        # ===== 전송 함수 (문자열을 인자로 받도록 변경) =====
    def send_message(text: str):
        text = text.strip()
        if text:
            execute("""
                INSERT INTO Messages(room_id, user_id, content, message_type)
                VALUES (%s, %s, %s, 'text')
            """, (room_id, my_id, text))

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

        # 🔹 상단: 제목 + 채팅방 목록 버튼
        title_col, btn_col = st.columns([4, 1])
        with title_col:
            st.markdown(f"<h2>💬 {friend_name}님과 채팅</h2>", unsafe_allow_html=True)
        with btn_col:
            # 오른쪽 정렬
            st.markdown("<div style='text-align:right;'>", unsafe_allow_html=True)
            if st.button("⬅ 채팅방으로", key="back_to_rooms"):
                st.session_state.page = "chat_rooms"
            st.markdown("</div>", unsafe_allow_html=True)

        # 🔹 스크롤 박스 (height는 네가 이미 700으로 늘린 상태 반영)
        components.html(chat_html, height=700, scrolling=False)

        # 아래 구분선 (원하면 없애도 됨)
        st.markdown(
            "<hr style='margin:6px 0 2px 0; border:0; border-top:1px solid rgba(255,255,255,0.08);'>",
            unsafe_allow_html=True,
        )

        # 🔹 chat_input 위 여백 최소화 + 위치 살짝 위로
        st.markdown("""
        <style>
        div[data-testid="stChatInput"] {
            margin-top: 0px !important;
        }
        div[data-testid="stChatInput"] > div:first-child {
            bottom: 120px !important;  /* 필요하면 20~60 사이에서 조절 */
        }
        </style>
        """, unsafe_allow_html=True)

        # 🔹 입력창
        user_input = st.chat_input("메시지를 입력하세요...")

        if user_input:
            send_message(user_input)
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

        