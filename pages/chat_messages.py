import streamlit as st
import streamlit.components.v1 as components
from db import fetch, execute
import html
from streamlit_javascript import st_javascript


st.set_page_config(layout="wide")


def chat_messages_page():
    # ===== 기본 세션 체크 =====
    room_id = st.session_state.get("room_id")
    if room_id is None:
        st.error("채팅방 정보를 찾을 수 없습니다.")
        return

    my_id = st.session_state.user["user_id"]

    # ===== 상대 이름 =====
    friend = fetch(
        """
        SELECT U.username
        FROM RoomMembers R
        JOIN Users U ON R.user_id = U.user_id
        WHERE R.room_id=%s AND R.user_id != %s
        """,
        (room_id, my_id),
    )
    friend_name = friend[0]["username"] if friend else "상대방"

    # ===== 메시지 불러오기 =====
    messages = fetch(
        """
        SELECT M.message_id, M.user_id, M.content, M.created_at, U.username
        FROM Messages M
        JOIN Users U ON M.user_id = U.user_id
        WHERE M.room_id=%s
        ORDER BY M.created_at ASC
        """,
        (room_id,),
    )

    # ===== 메시지를 HTML로 누적 (버블 스타일 변경) =====
    html_messages = ""
    for msg in messages:
        me = (msg["user_id"] == my_id)
        content = html.escape(msg["content"])
        time_str = msg["created_at"].strftime("%H:%M")

        wrapper = "msg-right" if me else "msg-left"

        # ✅ home/friends 스타일에 맞춘 버블 색
        if me:
            # 내 메시지: 보라→인디고 그라데이션
            color = "linear-gradient(135deg, #a855f7, #6366f1)"
        else:
            # 상대 메시지: 짙은 네이비 톤
            color = "rgba(50, 80, 150, 0.86)"

        html_messages += f"""
        <div class="{wrapper}">
            <div class="bubble" style="background:{color};">
                <div class="content">{content}</div>
                <div class="time">{time_str}</div>
            </div>
        </div>
        """

    # ===== 스크롤박스 HTML (다크 글래스 스타일) =====
    chat_html = f"""
    <html>
    <head>
    <style>
        html, body {{
            margin: 0;
            padding: 0;
            height: 100%;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            background: transparent;
        }}

        .messages-box {{
            height: 80%;
            max-height: 80%;
            overflow-y: auto;
            padding: 12px 10px 16px 10px;
            background: radial-gradient(circle at top left,
                        rgba(15,23,42,0.96),
                        rgba(15,23,42,0.94));
            border-radius: 20px;
            border: 1px solid rgba(55,65,81,0.9);
            box-shadow: 0 22px 40px rgba(15,23,42,0.98);
        }}

        .msg-left {{
            display: flex;
            justify-content: flex-start;
            margin: 6px 0;
            padding-left: 2px;
        }}
        .msg-right {{
            display: flex;
            justify-content: flex-end;
            margin: 6px 0;
            padding-right: 2px;
        }}

        .bubble {{
            max-width: 60%;
            padding: 9px 13px 7px 13px;
            border-radius: 16px;
            word-break: break-word;
            font-size: 14px;
            line-height: 1.45;
            color: #e5e7eb;
            box-shadow: 0 18px 35px rgba(15,23,42,0.95);
            position: relative;
        }}

        .msg-right .bubble {{
            border-bottom-right-radius: 6px;
        }}
        .msg-left .bubble {{
            border-bottom-left-radius: 6px;
        }}

        .content {{
            white-space: pre-wrap;
        }}

        .time {{
            font-size: 10px;
            color: #9ca3af;
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

    # ===== 전송 함수 =====
    def send_message(text: str):
        text = text.strip()
        if text:
            execute(
                """
                INSERT INTO Messages(room_id, user_id, content, message_type)
                VALUES (%s, %s, %s, 'text')
                """,
                (room_id, my_id, text),
            )

    # ===== 공통 스타일: 배경 / 컨테이너 / 타이틀 / 버튼 =====
    st.markdown(
        """
        <style>
        /* 전체 배경 – home/friends와 동일 톤 */
        [data-testid="stAppViewContainer"] {
            background: radial-gradient(circle at 0% 0%, #1e293b 0, #020617 55%, #000 100%);
        }

        /* 페이지 폭 */
        .block-container {
            max-width: 960px !important;
            padding-top: 3rem !important;
            padding-bottom: 2.5rem !important;
        }

        /* 중앙 래퍼 */
        .chat-wrapper {
            max-width: 900px;
            margin: 0 auto 1.5rem auto;
        }

        .chat-header {
            margin-bottom: 6px;
        }

        .chat-title {
            font-size: 19px;
            font-weight: 700;
            color: #e5e7eb;
            margin-bottom: 2px;
        }

        .chat-sub {
            font-size: 12px;
            color: #9ca3af;
            margin-bottom: 0;
        }

        /* 채팅방 목록 버튼 */
        .chat-back-btn .stButton > button {
            width: auto;
            border-radius: 999px;
            padding: 7px 18px;
            font-size: 12px;
            font-weight: 600;
            border: none;
            background: radial-gradient(
                circle at top left,
                #a855f7,
                #6366f1 45%,
                #0b1120 100%
            );
            color: #f9fafb;
            box-shadow: 0 15px 35px rgba(79,70,229,0.85);
            cursor: pointer;
            white-space: nowrap;
        }

        /* chat_input 위 여백 줄이기 + 고정 느낌 */
        div[data-testid="stChatInput"] {
            margin-top: 2px !important;
        }

        /* 모바일 대응 */
        @media (max-width: 768px) {
            .chat-title {
                font-size: 17px;
            }
            .block-container {
                padding-top: 2.2rem !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ===== 레이아웃 =====
    with st.container():
        st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)

        # 🔹 상단: 제목 + 채팅방 목록 버튼
        title_col, btn_col = st.columns([4, 1])
        with title_col:
            st.markdown(
                f"""
                <div class="chat-header">
                    <div class="chat-title">💬 {friend_name}님과 채팅</div>
                    <div class="chat-sub">메시지를 입력해 대화를 이어가 보세요.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with btn_col:
            st.markdown('<div class="chat-back-btn" style="text-align:right;">', unsafe_allow_html=True)
            if st.button("채팅방 목록", key="back_to_rooms"):
                st.session_state.page = "chat_rooms"
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        # 🔹 스크롤 박스 (고정 높이 + 내부 스크롤)
        components.html(chat_html, height=700, scrolling=False)

        # 🔹 구분선 (얇게)
        st.markdown(
            "<hr style='margin:6px 0 2px 0; border:0; border-top:1px solid rgba(148,163,184,0.25);'>",
            unsafe_allow_html=True,
        )

        # 🔹 입력창 (st.chat_input 그대로 사용)
        user_input = st.chat_input("메시지를 입력하세요...")

        if user_input:
            send_message(user_input)
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
