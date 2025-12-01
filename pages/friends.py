import streamlit as st
from db import fetch, execute

def friends_page():
    st.sidebar.title("📌 메뉴")
    menu = st.sidebar.radio("메뉴", ["홈", "친구", "채팅방", "프로필", "채팅분석", "로그아웃"],
                            index=1,)

    if menu == "친구":
       pass

    if menu == "홈":
        st.session_state.page = "main"
        st.rerun()


    elif menu == "채팅방":
        st.session_state.page = "chat_rooms"
        st.rerun()

    elif menu == "프로필":
        st.session_state.page = "profile"
        st.rerun()

    elif menu == "로그아웃":
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.page = "login"
        st.rerun()
        
    elif menu == "채팅분석":
        st.session_state.page = "chat_dashboard"
        st.rerun()

    # ---------- 공통 스타일 ----------
    st.markdown(
        """
        <style>
        /* 페이지 전체 폭 & 여백 (살짝 줄임) */
        .block-container {
            max-width: 780px !important;
            padding-top: 2.5rem !important;
            padding-bottom: 3rem !important;
        }

        /* 헤더 영역 */
        .friends-header {
            display: flex;
            align-items: center;
            gap: 14px;
            margin-bottom: 1.8rem;
        }
        .friends-header-icon {
            font-size: 32px;
            line-height: 1;
        }
        .friends-header-text-main {
            font-size: 30px;
            font-weight: 800;
        }
        .friends-header-text-sub {
            font-size: 13px;
            color: #9ca3af;
            margin-top: 2px;
        }

        /* 친구 카드 (다크톤) */
        .friend-card {
            padding: 14px 18px;
            border-radius: 18px;
            background: rgba(17,24,39,0.92);          /* 진한 네이비 */
            border: 1px solid rgba(55,65,81,0.9);      /* 회색 보더 */
            display: flex;
            align-items: center;
            margin: 4px 0 10px 0;
            transition: all 0.15s ease-out;
        }
        .friend-card:hover {
            border-color: #6366f1;
            box-shadow: 0 14px 30px rgba(79,70,229,0.45);
            transform: translateY(-1px);
        }

        .friend-info {
            display: flex;
            align-items: center;
        }

        .profile-img {
            width: 46px;
            height: 46px;
            border-radius: 999px;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 24px;
            margin-right: 14px;
            background: linear-gradient(135deg, #fef3c7, #facc15); /* 노랑 그라데이션 */
            box-shadow: 0 8px 18px rgba(250, 204, 21, 0.45);
        }

        .friend-name {
            font-size: 17px;
            font-weight: 600;
        }
        .friend-desc {
            font-size: 13px;
            color: #9ca3af;
            margin-top: 2px;
        }

        /* 기본 버튼 스타일 */
        .stButton > button {
            width: 100%;
            padding: 10px 18px;
            border-radius: 999px;
            border: none;
            font-size: 13px;
            font-weight: 600;
            background: #6366f1;
            color: #f9fafb;
            box-shadow: 0 10px 25px rgba(79,70,229,0.5);
            cursor: pointer;
            white-space: nowrap;
        }
        .stButton > button:hover {
            background: #4f46e5;
        }

        /* 채팅 시작 버튼(보라 네온 느낌) */
        .chat-start-btn .stButton > button {
            background: radial-gradient(circle at top left,
                                        #a855f7,
                                        #6366f1 40%,
                                        #111827 100%);
            box-shadow: 0 20px 45px rgba(79,70,229,0.9);
        }
        .chat-start-btn .stButton > button:hover {
            background: radial-gradient(circle at top left,
                                        #c084fc,
                                        #4f46e5 40%,
                                        #020617 100%);
        }

        /* 메인으로 버튼도 살짝 강조 */
        .back-btn .stButton > button {
            width: auto;
            padding-inline: 22px;
            background: radial-gradient(circle at top left,
                                        #a855f7,
                                        #6366f1 40%,
                                        #111827 100%);
            box-shadow: 0 18px 40px rgba(79,70,229,0.9);
        }

        /* '채팅 시작' 버튼 있는 컬럼을 카드 높이에 수직 중앙 정렬 */
        div[data-testid="column"]:has(.chat-start-btn) {
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }

        /* 모바일에서 살짝 축소 */
        @media (max-width: 768px) {
            .friends-header-text-main {
                font-size: 24px;
            }
            .friend-card {
                padding: 12px 14px;
            }
            .friend-name {
                font-size: 15px;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ---------- 데이터 ----------
    my_id = st.session_state.user["user_id"]

    friends = fetch(
        """
        SELECT U.user_id, U.username, U.profile_img
        FROM Users U 
        JOIN Friends F ON U.user_id = F.friend_id
        WHERE F.user_id=%s
        """,
        (my_id,),
    )

    # ---------- 헤더 ----------
    st.markdown(
        """
        <div class="friends-header">
            <div class="friends-header-icon"></div>
            <div>
                <div class="friends-header-text-main">친구 목록</div>
                <div class="friends-header-text-sub">
                    대화를 시작할 친구를 선택해 주세요.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---------- 검색 바 ----------
    search = st.text_input(
        "친구 검색",
        "",
        placeholder="🔍 이름으로 친구 검색",
    )

    if search:
        search_lower = search.lower()
        friends = [f for f in friends if search_lower in f["username"].lower()]

    if not friends:
        st.info("아직 등록된 친구가 없습니다. 친구를 추가해 보세요.")
        st.markdown('<div class="back-btn">', unsafe_allow_html=True)
        if st.button("⬅ 메인으로", key="back_main_empty"):
            st.session_state.page = "main"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        return

    # ---------- 친구 리스트 (지금 구조 그대로) ----------
    for f in friends:
        # 한 줄 = 카드(좌) + 버튼(우)
        col_card, col_btn = st.columns([8, 2])

        with col_card:
            st.markdown(
                f"""
                <div class="friend-card">
                    <div class="friend-info">
                        <div class="profile-img">💛</div>
                        <div>
                            <div class="friend-name">{f['username']}</div>
                            <div class="friend-desc">친구와 1:1 채팅을 시작합니다</div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col_btn:
            st.markdown('<div class="chat-start-btn">', unsafe_allow_html=True)
            if st.button("채팅 시작", key=f"btn_{f['user_id']}"):
                st.session_state.page = "start_chat"
                st.session_state.friend_id = f["user_id"]
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # ---------- 메인으로 ----------
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("⬅ 메인으로", key="back_main"):
        st.session_state.page = "main"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
