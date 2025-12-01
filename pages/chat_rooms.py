import streamlit as st
from db import fetch

def chat_rooms_page():
    st.sidebar.title("📌 메뉴")
    menu = st.sidebar.radio(
        "메뉴",
        ["홈", "친구", "채팅방", "프로필", "채팅분석", "로그아웃"],
        index=2,  # ✅ 0: 홈, 1: 친구, 2: 채팅방
    )

    if menu == "친구":
        st.session_state.page = "friends"
        st.rerun()

    if menu == "홈":
        st.session_state.page = "main"
        st.rerun()

    elif menu == "채팅방":
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

    # ---------- 스타일 ----------
    st.markdown(
        """
        <style>
        .block-container {
            max-width: 900px !important;
            padding-top: 2.5rem !important;
            padding-bottom: 3rem !important;
        }

        .rooms-header {
            display: flex;
            align-items: center;
            gap: 14px;
            margin-bottom: 12px;
            margin-top: 0.5rem;
        }
        # .rooms-icon {
        #     width: 42px;
        #     height: 42px;
        #     border-radius: 999px;
        #     display: flex;
        #     align-items: center;
        #     justify-content: center;
        #     font-size: 22px;
        #     background: radial-gradient(circle at 30% 0,
        #                                 rgba(244,114,182, 0.95),
        #                                 rgba(129,140,248, 0.95));
        #     box-shadow: 0 10px 26px rgba(79,70,229, 0.8);
        # }
        .rooms-icon {
            width: 42px;
            height: 42px;
            border-radius: 999px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 22px;
            background: linear-gradient(135deg, #fef3c7, #facc15); /* 노란 그라데이션 */
            box-shadow: 0 8px 18px rgba(250, 204, 21, 0.45);
        }

        .rooms-title-main {
            font-size: 28px;
            font-weight: 800;
        }
        .rooms-title-sub {
            font-size: 13px;
            color: #9ca3af;
            margin-top: 2px;
        }

        /* 한 줄(카드 + 버튼)을 감싸는 래퍼 */
        .room-row {
            max-width: 780px;          /* ✅ 카드+버튼 전체 가로 길이 */
            margin: 0 auto 4px auto;  /* 가운데 정렬 + 아래 여백 */
        }

        
        /* 카드 자체 – friends.py 스타일로 변경 */
        .chat-room-card {
            padding: 12px 18px;
            border-radius: 18px;
            background: rgba(17,24,39,0.92);          /* 진한 네이비 */
            border: 1px solid rgba(55,65,81,0.9);      /* 회색 보더 */
            display: flex;
            align-items: center;
            margin: 0;
            transition: all 0.15s ease-out;
        }


        .room-row:hover .chat-room-card {
            border-color: #6366f1;
            box-shadow: 0 22px 55px rgba(79,70,229,0.45);
            transform: translateY(-1px);
        }

        # /* 아바타 */
        # .chat-room-avatar {
        #     width: 40px;
        #     height: 40px;
        #     border-radius: 999px;
        #     background: radial-gradient(circle at 30% 0,
        #                                 rgba(244,114,182,1),
        #                                 rgba(129,140,248,1));
        #     display: flex;
        #     align-items: center;
        #     justify-content: center;
        #     font-size: 20px;
        #     box-shadow: 0 12px 26px rgba(79,70,229,0.9);
        #     flex-shrink: 0;
        # }
        .chat-room-avatar {
            width: 46px;
            height: 46px;
            border-radius: 999px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            margin-right: 14px;
            background: linear-gradient(135deg, #fef3c7, #facc15); /* friends와 동일 */
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

        /* 오른쪽 '입장' 버튼 스타일 */
        

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
        }
        .rooms-empty-text {
            font-size: 13px;
            color: #9ca3af;
        }

        .back-btn {
            margin-top: 26px;
        }
        .back-btn .stButton > button {
            border-radius: 999px;
            padding: 8px 16px;
            font-size: 13px;
        }

        @media (max-width: 768px) {
            .room-row { max-width: 100%; }
            .chat-room-card {
                padding: 10px 14px;
                border-radius: 18px;
            }
        }
        
        /* 🔥 Streamlit이 기본으로 넣는 세로 간격 줄이기 */
        div[data-testid="stVerticalBlock"] {
            margin-bottom: 0.6rem !important;   /* 기본 1rem 정도 → 0.2rem */
            row-gap: 0.6rem !important;         /* 내부 요소 간격도 촘촘하게 */
        }

        </style>
        """,
        unsafe_allow_html=True,
    )

    # 헤더
    st.markdown(
        """
        <div class="rooms-header">
          <div class="rooms-icon">💬</div>
          <div>
            <div class="rooms-title-main">채팅방 목록</div>
            <div class="rooms-title-sub">최근 대화를 한 친구들과의 채팅방이에요</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 데이터
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
            # 1) 상대 이름
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

            max_len = 40
            if len(preview) > max_len:
                preview_short = preview[:max_len].rstrip() + "…"
            else:
                preview_short = preview

            # ---- 한 줄: 카드(col1) + 입장 버튼(col2) ----
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

    # 메인으로
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("⬅ 메인으로", key="back_main_from_rooms"):
        st.session_state.page = "main"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
