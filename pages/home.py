import streamlit as st
from db import fetch  # 간단 통계용 – 실패해도 앱이 죽지 않게 try/except로 처리
import base64
from pathlib import Path


# =========================
# 🔹 로고 PNG를 base64로 불러오기
# =========================
def load_logo_base64() -> str:
    """
    메인 히어로 섹션에 넣을 chatcloud 로고를 base64로 변환합니다.
    기본 경로: assets/chat_cloud_final.png
    """
    candidate_paths = [
        Path("assets/chat_cloud_final.png"),
        Path("chat_cloud_final.png"),
        Path(__file__).parent / "assets" / "chat_cloud_final.png",
    ]
    for p in candidate_paths:
        if p.exists():
            return base64.b64encode(p.read_bytes()).decode("utf-8")
    return ""


LOGO_BASE64 = load_logo_base64()


def main_page():
    # =========================
    # 🔹 사이드바 내비게이션
    # =========================
    st.sidebar.title("📌 메뉴")

    menu = st.sidebar.radio(
        "메뉴",
        ["홈", "친구", "채팅방", "프로필", "채팅분석", "로그아웃"],
        index=0,
    )


    if menu == "친구":
        st.session_state.page = "friends"
        st.rerun()

    if menu == "홈":
        # 아래에서 메인 컨텐츠 렌더링
        pass

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

    # =========================
    # 🔹 공통 스타일 (Cloud + Glass)
    # =========================
    st.markdown(
        """
        <style>
        /* 전체 배경 */
        [data-testid="stAppViewContainer"] {
            background: radial-gradient(circle at 0% 0%, #1e293b 0, #020617 55%, #000 100%);
        }

        .block-container {
            max-width: 960px !important;
            padding-top: 3rem !important;
            padding-bottom: 3rem !important;
        }

        /* 히어로 섹션 */
      
        .hero {
            position: relative;
            padding: 26px 28px 24px 28px;
            border-radius: 26px;
            background: linear-gradient(135deg, rgba(14,116,144,0.8), rgba(76,29,149,0.9));
            box-shadow: 0 28px 60px rgba(15,23,42,0.9);
            overflow: hidden;
            margin-bottom: 26px;
            display: flex;
            align-items: center;
            gap: 40px;              /* 🔹 로고와 텍스트 사이 간격 ↑ */
        }
        .hero::before {
            content: "";
            position: absolute;
            width: 220px;
            height: 220px;
            border-radius: 999px;
            background: radial-gradient(circle, rgba(244,244,245,0.18), transparent 70%);
            top: -40px;
            right: -30px;
            filter: blur(2px);
        }

        /* 왼쪽 로고 영역 */
        .hero-left {
            position: relative;
            z-index: 2;
            flex: 0 0 300px;        /* 🔹 로고 영역 넓이 ↑ (기존 160px 근처였을 것) */
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .hero-logo-img {
            width: 230px;           /* 🔹 실제 PNG 크기 ↑ (기존 150px) */
            max-width: 100%;
            filter: drop-shadow(0 18px 35px rgba(15,23,42,0.8));
            border-radius: 22px;
            background: rgba(15,23,42,0.65);
            padding: 8px 10px;
        }
        .hero-logo-fallback {
            font-size: 42px;
        }

        /* 오른쪽 텍스트 영역 */
        .hero-right {
            position: relative;
            z-index: 2;
            flex: 1;
            min-width: 0;
            margin-left: 12px;       /* 🔹 글 전체를 아주 살짝 오른쪽으로 */
        }

        .hero-logo-pill {
            display: inline-flex;
            align-items: center;
            gap: 4px;
            padding: 4px 12px;
            border-radius: 999px;
            background: rgba(15,23,42,0.6);
            border: 1px solid rgba(148,163,184,0.6);
            font-size: 11px;
            color: #e5e7eb;
            margin-bottom: 10px;
        }
        .hero-logo-pill span {
            font-size: 13px;
        }

        .hero-title {
            font-size: 30px;
            font-weight: 800;
            color: #f9fafb;
            letter-spacing: -0.03em;
            margin-bottom: 6px;
        }
        .hero-subtitle {
            font-size: 13px;
            color: #e5e7eb;
            max-width: 520px;
            line-height: 1.5;
        }

        .hero-username {
            margin-top: 16px;
            font-size: 13px;
            color: #c7d2fe;
        }

        .hero-cloud-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 18px;
        }
        .hero-cloud-tag {
            padding: 6px 12px;
            border-radius: 999px;
            background: rgba(15,23,42,0.65);
            color: #e5e7eb;
            font-size: 11px;
            border: 1px solid rgba(148,163,184,0.4);
            backdrop-filter: blur(12px);
        }

        /* 섹션 타이틀 */
        .section-title {
            font-size: 16px;
            font-weight: 700;
            color: #e5e7eb;
            margin-bottom: 10px;
            margin-top: 10px;
        }
        .section-sub {
            font-size: 12px;
            color: #9ca3af;
            margin-bottom: 14px;
        }

        /* 퀵 액션 카드 */
        .qa-card {
            padding: 16px 16px 14px 16px;
            border-radius: 18px;
            background: rgba(15,23,42,0.88);
            border: 1px solid rgba(55,65,81,0.9);
            box-shadow: 0 18px 35px rgba(15,23,42,0.95);
            display: flex;
            flex-direction: column;
            gap: 6px;
            height: 100%;
            transition: all 0.18s ease-out;
        }
        .qa-card:hover {
            border-color: #6366f1;
            box-shadow: 0 26px 55px rgba(79,70,229,0.65);
            transform: translateY(-2px);
        }

        .qa-icon {
            font-size: 22px;
            margin-bottom: 4px;
        }
        .qa-title {
            font-size: 14px;
            font-weight: 600;
            color: #e5e7eb;
        }
        .qa-desc {
            font-size: 11px;
            color: #9ca3af;
        }

        .qa-card .stButton > button {
            margin-top: 8px;
            width: 100%;
            border-radius: 999px;
            padding: 7px 0;
            font-size: 12px;
            font-weight: 600;
            border: none;
            background: radial-gradient(circle at top left, #a855f7, #6366f1 45%, #0b1120 100%);
            color: #f9fafb;
            box-shadow: 0 15px 35px rgba(79,70,229,0.85);
            cursor: pointer;
        }
        .qa-card .stButton > button:hover {
            background: radial-gradient(circle at top left, #c4b5fd, #4f46e5 45%, #020617 100%);
        }

        /* 미니 통계 카드 */
        .stat-card {
            padding: 12px 14px;
            border-radius: 16px;
            background: rgba(15,23,42,0.9);
            border: 1px solid rgba(55,65,81,0.85);
            box-shadow: 0 14px 32px rgba(15,23,42,0.9);
        }
        .stat-label {
            font-size: 11px;
            color: #9ca3af;
            margin-bottom: 4px;
        }
        .stat-value {
            font-size: 18px;
            font-weight: 700;
            color: #e5e7eb;
        }
        .stat-footnote {
            font-size: 10px;
            color: #6b7280;
            margin-top: 2px;
        }

        .footer-caption {
            margin-top: 18px;
            font-size: 11px;
            color: #6b7280;
            text-align: right;
        }

        @media (max-width: 768px) {
            .hero {
                padding: 22px 18px 20px 18px;
                flex-direction: column;
                align-items: flex-start;
            }
            .hero-title {
                font-size: 24px;
            }
            .hero-left {
                flex: 0 0 auto;
                justify-content: flex-start;
                margin-bottom: 4px;
            }
            .hero-logo-img {
                width: 130px;
            }
            .block-container {
                padding-top: 2.2rem !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    username = st.session_state.user.get("username", "사용자")

    # =========================
    # 🔹 히어로 섹션 (로고 + 텍스트)
    # =========================
    if LOGO_BASE64:
        logo_img_html = f'<img src="data:image/png;base64,{LOGO_BASE64}" class="hero-logo-img"/>'
    else:
        # 이미지 못 찾으면 이모지로 대체
        logo_img_html = '<div class="hero-logo-fallback">☁️</div>'

    st.markdown(
        f"""
        <div class="hero">
            <div class="hero-left">
                {logo_img_html}
            </div>
            <div class="hero-right">
                <div class="hero-logo-pill">
                    <span>☁️</span>
                    <span>Chat_Cloud · Conversation Analytics</span>
                </div>
                <div class="hero-title">
                    오늘의 대화가<br/>구름처럼 퍼져 나가는 순간
                </div>
                <div class="hero-subtitle">
                    친구들과 나눈 대화가 감정, 키워드, 패턴으로 재구성되어
                    <b>클라우드 대시보드</b>에서 한눈에 보입니다.
                    오늘의 대화 구름을 확인해 보세요.
                </div>
                <div class="hero-username">
                    👋 {username}님, 오늘도 당신의 대화가 인사이트로 쌓이고 있어요.
                </div>
                <div class="hero-cloud-tags">
                    <div class="hero-cloud-tag">실시간 감정 구름</div>
                    <div class="hero-cloud-tag">키워드 네트워크</div>
                    <div class="hero-cloud-tag">행동 패턴 분석</div>
                    <div class="hero-cloud-tag">에피소드 타임라인</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # =========================
    # 🔹 퀵 액션 카드 영역
    # =========================
    st.markdown(
        """
        <div class="section-title">빠르게 시작해 볼까요?</div>
        <div class="section-sub">
            자주 사용하는 기능을 한 번에 모았습니다. 원하는 구름으로 바로 이동해 보세요.
        </div>
        """,
        unsafe_allow_html=True,
    )

    qa_col1, qa_col2, qa_col3, qa_col4 = st.columns(4)

    with qa_col1:
        st.markdown(
            """
            <div class="qa-card">
                <div class="qa-icon">🧑‍🤝‍🧑</div>
                <div class="qa-title">친구 목록</div>
                <div class="qa-desc">대화를 시작할 친구를 선택하고 1:1 채팅을 열어요.</div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("친구 보러가기", key="go_friends_from_main"):
            st.session_state.page = "friends"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with qa_col2:
        st.markdown(
            """
            <div class="qa-card">
                <div class="qa-icon">💬</div>
                <div class="qa-title">채팅방 목록</div>
                <div class="qa-desc">최근에 대화한 채팅방으로 바로 입장해 보세요.</div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("채팅방 입장", key="go_rooms_from_main"):
            st.session_state.page = "chat_rooms"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with qa_col3:
        st.markdown(
            """
            <div class="qa-card">
                <div class="qa-icon">📊</div>
                <div class="qa-title">채팅 분석</div>
                <div class="qa-desc">감정, 키워드, 행동 패턴이 구름처럼 시각화됩니다.</div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("대시보드 열기", key="go_dashboard_from_main"):
            st.session_state.page = "chat_dashboard"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with qa_col4:
        st.markdown(
            """
            <div class="qa-card">
                <div class="qa-icon">👤</div>
                <div class="qa-title">내 프로필</div>
                <div class="qa-desc">닉네임과 이미지로 나만의 클라우드를 꾸며보세요.</div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("프로필 설정", key="go_profile_from_main"):
            st.session_state.page = "profile"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # =========================
    # 🔹 간단 통계 카드 (옵션)
    # =========================
    total_messages = "-"
    total_rooms = "-"
    my_friends = "-"

    try:
        msg_res = fetch("SELECT COUNT(*) AS cnt FROM Messages")
        if msg_res:
            total_messages = f"{msg_res[0]['cnt']:,}"

        room_res = fetch("SELECT COUNT(*) AS cnt FROM ChatRooms")
        if room_res:
            total_rooms = f"{room_res[0]['cnt']:,}"

        user_id = st.session_state.user["user_id"]
        friend_res = fetch(
            "SELECT COUNT(*) AS cnt FROM Friends WHERE user_id = %s",
            (user_id,),
        )
        if friend_res:
            my_friends = f"{friend_res[0]['cnt']:,}"
    except Exception:
        # 통계 조회에 실패해도 조용히 넘어감
        pass

    st.markdown(
        """
        <div class="section-title">Chat_Cloud 한눈에 보기</div>
        <div class="section-sub">
            지금까지 쌓인 대화 구름의 규모를 간단하게 요약해 보여드립니다.
        </div>
        """,
        unsafe_allow_html=True,
    )

    stat_col1, stat_col2, stat_col3 = st.columns(3)

    with stat_col1:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-label">누적 메시지</div>
                <div class="stat-value">{total_messages}</div>
                <div class="stat-footnote">Messages</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with stat_col2:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-label">내 친구 수</div>
                <div class="stat-value">{my_friends}</div>
                <div class="stat-footnote">Friends</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with stat_col3:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-label">개설된 채팅방</div>
                <div class="stat-value">{total_rooms}</div>
                <div class="stat-footnote">Chat Rooms</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="footer-caption">
            오늘은 어떤 대화가 새로운 구름을 만들까요? ☁️
        </div>
        """,
        unsafe_allow_html=True,
    )
