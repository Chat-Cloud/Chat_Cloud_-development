import streamlit as st
from db import fetch, execute


def friends_page():
    # =============== 🔹 사이드바 내비게이션 ===============
    st.sidebar.title("📌 메뉴")
    menu = st.sidebar.radio(
        "메뉴",
        ["홈", "친구", "채팅방", "프로필", "채팅분석", "로그아웃"],
        index=1,
    )

    if menu == "친구":
        # 현재 페이지
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

    elif menu == "채팅분석":
        st.session_state.page = "chat_dashboard"
        st.rerun()

    elif menu == "로그아웃":
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.page = "login"
        st.rerun()

    # =============== 🔹 공통 스타일 (home.py와 톤 맞추기) ===============
    st.markdown(
        """
        <style>
        /* 전체 배경 – home.py와 동일 톤 */
        [data-testid="stAppViewContainer"] {
            background: radial-gradient(circle at 0% 0%, #1e293b 0, #020617 55%, #000 100%);
        }

        /* 페이지 폭 – home.py(960px)와 맞춤 */
        .block-container {
            max-width: 960px !important;
            padding-top: 3rem !important;
            padding-bottom: 3rem !important;
        }

        /* 섹션 타이틀 – home.py 공통 스타일 */
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

        /* 상단 Friends 히어로 카드 (작은 글래스 카드 느낌) */
        .friends-hero {
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
        .friends-hero-icon {
            font-size: 26px;
        }
        .friends-hero-main {
            font-size: 18px;
            font-weight: 700;
            color: #e5e7eb;
            margin-bottom: 2px;
        }
        .friends-hero-sub {
            font-size: 12px;
            color: #9ca3af;
        }

        /* 친구 리스트 카드 영역 – home.py의 qa-card 톤과 맞춤 */
        .friend-card-outer {
            margin-bottom: 10px;
        }

        .friend-card {
            padding: 14px 16px;
            border-radius: 18px;
            background: rgba(15,23,42,0.9);
            border: 1px solid rgba(55,65,81,0.9);
            box-shadow: 0 18px 35px rgba(15,23,42,0.95);
            display: flex;
            align-items: center;
            gap: 14px;
            transition: all 0.18s ease-out;
        }
        .friend-card:hover {
            border-color: #6366f1;
            box-shadow: 0 26px 55px rgba(79,70,229,0.65);
            transform: translateY(-2px);
        }

        .friend-avatar {
            width: 46px;
            height: 46px;
            border-radius: 999px;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 24px;
            background: linear-gradient(135deg, #fef3c7, #facc15);
            box-shadow: 0 10px 20px rgba(250,204,21,0.5);
            flex-shrink: 0;
        }

        .friend-meta {
            display: flex;
            flex-direction: column;
            justify-content: center;
            min-width: 0;
        }
        .friend-name {
            font-size: 15px;
            font-weight: 600;
            color: #e5e7eb;
            margin-bottom: 2px;
        }
        .friend-desc {
            font-size: 12px;
            color: #9ca3af;
        }

        /* 버튼 – home.py의 qa-card 버튼과 동일 느낌 */
        .friend-action .stButton > button {
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
        .friend-action .stButton > button:hover {
            background: radial-gradient(
                circle at top left,
                #c4b5fd,
                #4f46e5 45%,
                #020617 100%
            );
        }

        /* "메인으로" 버튼 – 약간 강조 */
        .back-btn .stButton > button {
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
        }

        /* 버튼 컬럼 수직정렬 (카드 가운데에 오게) */
        div[data-testid="column"]:has(.friend-action) {
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }

        /* 모바일 대응 */
        @media (max-width: 768px) {
            .friends-hero {
                flex-direction: row;
                align-items: flex-start;
            }
            .friend-card {
                padding: 12px 12px;
            }
            .friend-name {
                font-size: 14px;
            }
            .section-title {
                font-size: 15px;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # =============== 🔹 데이터 조회 ===============
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

    # =============== 🔹 상단 Friends 히어로 ===============
    st.markdown(
        """
        <div class="friends-hero">
            <div class="friends-hero-icon">🧑‍🤝‍🧑</div>
            <div>
                <div class="friends-hero-main">친구 목록</div>
                <div class="friends-hero-sub">
                    대화를 시작할 친구를 선택하면 1:1 채팅방이 열립니다.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # =============== 🔹 검색 바 ===============
    st.markdown(
        """
        <div class="section-title">친구 검색</div>
        <div class="section-sub">이름으로 빠르게 친구를 찾아보세요.</div>
        """,
        unsafe_allow_html=True,
    )

    search = st.text_input(
        "친구 검색",
        "",
        placeholder="🔍 이름으로 친구 검색",
    )

    if search:
        search_lower = search.lower()
        friends = [f for f in friends if search_lower in f["username"].lower()]

    # =============== 🔹 친구가 없을 때 ===============
    if not friends:
        st.info("아직 등록된 친구가 없습니다. 친구를 추가해 보세요.")
        st.markdown('<div class="back-btn">', unsafe_allow_html=True)
        if st.button("⬅ 메인으로", key="back_main_empty"):
            st.session_state.page = "main"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        return

    # =============== 🔹 친구 리스트 (카드 + 버튼) ===============
    st.markdown(
        """
        <div class="section-title">내 친구들</div>
        <div class="section-sub">대화를 시작할 친구의 채팅방으로 바로 들어가 보세요.</div>
        """,
        unsafe_allow_html=True,
    )

    for f in friends:
        col_card, col_btn = st.columns([8, 2])

        with col_card:
            st.markdown(
                f"""
                <div class="friend-card-outer">
                    <div class="friend-card">
                        <div class="friend-avatar">💛</div>
                        <div class="friend-meta">
                            <div class="friend-name">{f['username']}</div>
                            <div class="friend-desc">친구와 1:1 채팅을 시작합니다.</div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col_btn:
            st.markdown('<div class="friend-action">', unsafe_allow_html=True)
            if st.button("채팅 시작", key=f"btn_{f['user_id']}"):
                st.session_state.page = "start_chat"
                st.session_state.friend_id = f["user_id"]
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    # =============== 🔹 메인으로 버튼 ===============
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("⬅ 메인으로", key="back_main"):
        st.session_state.page = "main"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
