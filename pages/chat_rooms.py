import streamlit as st
from db import fetch


def chat_rooms_page():
    # =============== 🔹 사이드바 메뉴 ===============
    st.sidebar.title("📌 메뉴")
    menu = st.sidebar.radio(
        "메뉴",
        ["홈", "친구", "채팅방", "프로필", "채팅분석", "로그아웃"],
        index=2,  # 0: 홈, 1: 친구, 2: 채팅방
    )

    if menu == "친구":
        st.session_state.page = "friends"
        st.rerun()

    if menu == "홈":
        st.session_state.page = "main"
        st.rerun()

    elif menu == "채팅방":
        # 현재 페이지
        pass

    elif menu == "프로필":
        st.session_state.page = "profile"
        st.rerun()

    elif menu == "채팅분석":
        st.session_state.page = "chat_dashboard"
        st.rerun()

    elif menu == "로그아웃":
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.page = "login"
        st.rerun()

    my_id = st.session_state.user["user_id"]

    # =============== 🔹 공통 스타일 (home / friends 톤 맞추기) ===============
    st.markdown(
        """
        <style>
        /* 전체 배경 – home / friends / chat_messages와 동일 톤 */
        [data-testid="stAppViewContainer"] {
            background: radial-gradient(circle at 0% 0%, #1e293b 0, #020617 55%, #000 100%);
        }

        /* 페이지 폭 */
        .block-container {
            max-width: 960px !important;
            padding-top: 3rem !important;
            padding-bottom: 3rem !important;
        }

        /* 상단 히어로 카드 */
        .rooms-hero {
            padding: 18px 18px 16px 18px;
            border-radius: 22px;
            background: rgba(15,23,42,0.9);
            border: 1px solid rgba(55,65,81,0.9);
            box-shadow: 0 22px 40px rgba(15,23,42,0.95);
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 18px;
        }
        .rooms-hero-icon {
            font-size: 26px;
        }
        .rooms-hero-main {
            font-size: 18px;
            font-weight: 700;
            color: #e5e7eb;
            margin-bottom: 2px;
        }
        .rooms-hero-sub {
            font-size: 12px;
            color: #9ca3af;
        }

        /* 섹션 타이틀 (필요 시 사용) */
        .section-title {
            font-size: 16px;
            font-weight: 700;
            color: #e5e7eb;
            margin-bottom: 6px;
            margin-top: 4px;
        }
        .section-sub {
            font-size: 12px;
            color: #9ca3af;
            margin-bottom: 14px;
        }

        /* 한 줄(카드 + 버튼)을 감싸는 래퍼 */
        .room-row {
            max-width: 820px;
            margin: 0 auto 6px auto;
        }

        /* 채팅방 카드 – friends의 friend-card와 톤 통일 */
        .chat-room-card {
            padding: 12px 16px;
            border-radius: 18px;
            background: rgba(15,23,42,0.9);
            border: 1px solid rgba(55,65,81,0.9);
            box-shadow: 0 18px 35px rgba(15,23,42,0.95);
            display: flex;
            align-items: center;
            margin: 0;
            transition: all 0.18s ease-out;
        }

        .room-row:hover .chat-room-card {
            border-color: #6366f1;
            box-shadow: 0 26px 55px rgba(79,70,229,0.65);
            transform: translateY(-2px);
        }

        /* 아바타 – friends와 동일한 노란 버블 */
        .chat-room-avatar {
            width: 46px;
            height: 46px;
            border-radius: 999px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            margin-right: 14px;
            background: linear-gradient(135deg, #fef3c7, #facc15);
            box-shadow: 0 8px 18px rgba(250, 204, 21, 0.45);
            flex-shrink: 0;
        }

        .chat-room-main {
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 4px;
            min-width: 0;
        }
        .chat-room-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 8px;
        }
        .chat-room-name {
            font-size: 15px;
            font-weight: 600;
            color: #e5e7eb;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .chat-room-time {
            font-size: 11px;
            color: #9ca3af;
            flex-shrink: 0;
        }
        .chat-room-preview {
            font-size: 13px;
            color: #d1d5db;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        /* 입장 버튼 – friends.py 버튼 스타일과 동일 느낌 */
        .enter-btn .stButton > button {
            width: 100%;
            border-radius: 999px;
            padding: 8px 0;
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
        .enter-btn .stButton > button:hover {
            background: radial-gradient(
                circle at top left,
                #c4b5fd,
                #4f46e5 45%,
                #020617 100%
            );
        }

        /* 버튼 컬럼 수직 정렬(카드 중앙) */
        div[data-testid="column"]:has(.enter-btn) {
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }

        /* 채팅방 없을 때 */
        .rooms-empty {
            margin-top: 40px;
            padding: 24px 20px;
            border-radius: 18px;
            border: 1px dashed rgba(75,85,99,0.9);
            background: rgba(15,23,42,0.9);
            text-align: center;
        }
        .rooms-empty-title {
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 4px;
            color: #e5e7eb;
        }
        .rooms-empty-text {
            font-size: 13px;
            color: #9ca3af;
        }

        /* 메인으로 버튼 */
        .back-btn {
            margin-top: 20px;
        }
        .back-btn .stButton > button {
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
        }

        /* 여백 약간 촘촘하게 */
        div[data-testid="stVerticalBlock"] {
            margin-bottom: 0.6rem !important;
            row-gap: 0.6rem !important;
        }

        @media (max-width: 768px) {
            .room-row { max-width: 100%; }
            .chat-room-card {
                padding: 10px 14px;
                border-radius: 18px;
            }
            .rooms-hero-main {
                font-size: 17px;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # =============== 🔹 상단 히어로 ===============
    st.markdown(
        """
        <div class="rooms-hero">
          <div class="rooms-hero-icon">💬</div>
          <div>
            <div class="rooms-hero-main">채팅방 목록</div>
            <div class="rooms-hero-sub">최근 대화를 나눈 친구들과의 채팅방입니다.</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # =============== 🔹 채팅방 목록 데이터 ===============
    rooms = fetch("SELECT room_id, room_name FROM ChatRooms ORDER BY room_id DESC")

    if not rooms:
        st.markdown(
            """
            <div class="rooms-empty">
              <div class="rooms-empty-title">아직 열린 채팅방이 없어요</div>
              <div class="rooms-empty-text">친구 목록에서 먼저 채팅을 시작해 보세요.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        for r in rooms:
            # 1) 상대 이름 조회
            friend = fetch(
                """
                SELECT U.username
                FROM RoomMembers R
                JOIN Users U ON R.user_id = U.user_id
                WHERE R.room_id = %s
                  AND R.user_id <> %s
                LIMIT 1
                """,
                (r["room_id"], my_id),
            )
            room_name = friend[0]["username"] if friend else "이름 없는 채팅방"

            # 2) 마지막 메시지
            last_msg = fetch(
                """
                SELECT content, created_at 
                FROM Messages 
                WHERE room_id = %s 
                ORDER BY created_at DESC 
                LIMIT 1
                """,
                (r["room_id"],),
            )
            if last_msg:
                preview = last_msg[0]["content"]
                t = last_msg[0]["created_at"]
                time_str = t.strftime("%m/%d %H:%M")
            else:
                preview = "메시지가 없습니다."
                time_str = ""

            # 프리뷰 길이 제한
            max_len = 40
            if len(preview) > max_len:
                preview_short = preview[:max_len].rstrip() + "…"
            else:
                preview_short = preview

            # ---- 한 줄: 카드(col_card) + 입장(col_btn) ----
            st.markdown('<div class="room-row">', unsafe_allow_html=True)
            col_card, col_btn = st.columns([5, 2])

            with col_card:
                card_html = f"""
                <div class="chat-room-card">
                  <div class="chat-room-avatar">💬</div>
                  <div class="chat-room-main">
                    <div class="chat-room-top">
                      <div class="chat-room-name">{room_name}</div>
                      <div class="chat-room-time">{time_str}</div>
                    </div>
                    <div class="chat-room-preview">{preview_short}</div>
                  </div>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)

            with col_btn:
                st.markdown('<div class="enter-btn">', unsafe_allow_html=True)
                if st.button("입장", key=f"room_{r['room_id']}"):
                    st.session_state.room_id = r["room_id"]
                    st.session_state.page = "chat_messages"
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

    # =============== 🔹 메인으로 버튼 ===============
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("⬅ 메인으로", key="back_main_from_rooms"):
        st.session_state.page = "main"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
