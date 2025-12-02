# pages/chat_dashboard.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import ast
import plotly.express as px
from collections import Counter
from itertools import combinations
import networkx as nx
from matplotlib import cm
from matplotlib import colors as mcolors
import plotly.graph_objects as go
import numpy as np

@st.cache_data
def load_data():
    print("Loading data...")
    df = pd.read_csv("output/analyzed_chat.csv")
    keywords = pd.read_csv("output/top_keywords.csv")

    # nouns 컬럼: 문자열 → 리스트 변환
    df["nouns"] = df["nouns"].apply(
        lambda x: ast.literal_eval(x) if isinstance(x, str) else []
    )

    return df, keywords
# 🔹 0. 페이지 맨 위쪽 어딘가에 CSS 한 번만 선언
st.markdown(
    """
    <style>
    /* border 있는 container에만 살짝 배경 주기 */
    [data-testid="stContainer"] > div:has(> .stHeading) {
        border-radius: 18px;
        background: radial-gradient(circle at top left, rgba(56, 189, 248, 0.12), rgba(15, 23, 42, 1));
        box-shadow: 0 18px 40px rgba(0, 0, 0, 0.55);
        padding: 1.0rem 1.2rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)



def chat_dashboard_page():
        # 대시보드에서만 컨테이너 폭 넓히기
    st.markdown(
        """
        <style>
        .block-container {
            max-width: 1200px !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.sidebar.title("📌 메뉴")
    menu = st.sidebar.radio(
        "메뉴",
        ["홈", "친구", "채팅방", "프로필", "채팅분석", "로그아웃"],
        index=4,  # ✅ 0: 홈, 1: 친구, 2: 채팅방
    )

    if menu == "친구":
        st.session_state.page = "friends"
        st.rerun()

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
        pass

    elif menu == "로그아웃":
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.page = "login"
        st.rerun()
    my_id = st.session_state.user["user_id"]


    plt.rcParams['font.family'] = 'Malgun Gothic'


    # ⚠️ 여기서는 set_page_config 호출하지 않음 (app.py에서 한 번만!)
    st.title("건희님과의 대화는 어땠을까요? ")

    df, keywords = load_data()

    # # =========================================
    # # 📊 1. 전체 요약
    # # =========================================
    # st.header("전체 요약 통계")
    # st.markdown('<div class="summary-section">', unsafe_allow_html=True)
    # col1, col2, col3, col4 = st.columns(4)
    # col1.metric("총 메시지 수", len(df))
    # col2.metric("참여자 수", df["sender"].nunique())
    # col3.metric("평균 메시지 길이", round(df["msg_len"].mean(), 1))
    # col4.metric("평균 단어 수", round(df["word_count"].mean(), 1))
    # st.markdown('</div>', unsafe_allow_html=True)  # 👉 카드 끝
        # 😊 2. 감정 분석 — neutral 포함 & 제외
    # =========================================
    with st.container(border=True):
        st.header("대화의 감정 상태는 어땠을까요?")
        st.markdown(
            "<span style='font-size:0.9rem; opacity:0.8;'>발신자별 감정 비율을 neutral 포함/제외로 비교해봤어요.</span>",
            unsafe_allow_html=True,
        )


    emotion_order = ["very_negative", "negative", "neutral", "positive", "very_positive"]
    colors = {
        "very_negative": "#B7415E",  # 딥 로즈 / 묵직한 와인
        "negative":      "#E69F86",  # 테라코타 / 소프트 브라운
        "neutral":       "#A3B9A9",  # 그레이시 민트
        "positive":      "#69A0C3",  # 소프트 블루
        "very_positive": "#2E4A7D"   # 딥 네이비
    }

    emotion_ratio = (
        df.groupby("sender")["emotion"]
          .value_counts(normalize=True)
          .rename("ratio")
          .reset_index()
    )

    emotion_pivot = emotion_ratio.pivot(
        index="sender",
        columns="emotion",
        values="ratio"
    ).fillna(0)

    emotion_pivot = emotion_pivot.reindex(columns=emotion_order, fill_value=0)

    colA, colB = st.columns(2)

    # ------------------------
    #  왼쪽: neutral 포함 (Plotly)
    # ------------------------
    with colA:
        st.subheader("neutral 포함")

        fig = px.bar(
            emotion_pivot.reset_index(),
            x="sender",
            y=emotion_order,
            title="감정 비율 (전체)",
            labels={"value": "비율", "sender": "발신자", "variable": "emotion"},
            color_discrete_map=colors
        )
        fig.update_layout(
            barmode="stack",
            legend_title_text="emotion",
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis_title=None,
        )
        st.plotly_chart(fig, use_container_width=True)

    # ------------------------
    #  오른쪽: neutral 제외 (Plotly)
    # ------------------------
    with colB:
        st.subheader("neutral 제외")

        emo_no_neutral = emotion_pivot.drop(columns=["neutral"])

        fig = px.bar(
            emo_no_neutral.reset_index(),
            x="sender",
            y=list(emo_no_neutral.columns),
            title="감정 비율 (neutral 제거)",
            labels={"value": "비율", "sender": "발신자", "variable": "emotion"},
            color_discrete_map=colors
        )
        fig.update_layout(
            barmode="stack",
            legend_title_text="emotion",
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis_title=None,
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    
    
        # 3. 시간대별 감정 변화 — neutral 포함 & 제외
    # =========================================
    with st.container(border=True):
        st.header("시간대별로 감정의 변화를 분석해봤어요")
        st.markdown(
            "<span style='font-size:0.9rem; opacity:0.8;'>하루 중 언제 감정이 더 올라가고 내려갔는지 살펴봤어요.</span>",
            unsafe_allow_html=True,
        )


    emotion_by_hour = df.groupby(["hour", "emotion"]).size().reset_index(name="count")

    colC, colD = st.columns(2)

    # ------------------------
    #  neutral 포함 (Plotly)
    # ------------------------
    with colC:
        st.subheader("neutral 포함")

        fig = px.line(
            emotion_by_hour,
            x="hour",
            y="count",
            color="emotion",
            markers=True,
            title="시간대별 감정 변화 (전체)",
            labels={"hour": "시간", "count": "메시지 수", "emotion": "emotion"},
            color_discrete_map=colors   # ← 여기만 추가
        )
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig, use_container_width=True)

    # ------------------------
    #  neutral 제외 (Plotly)
    # ------------------------
    with colD:
        st.subheader("neutral 제외")

        emo_by_hour_no_neutral = emotion_by_hour[emotion_by_hour["emotion"] != "neutral"]

        fig = px.line(
            emo_by_hour_no_neutral,
            x="hour",
            y="count",
            color="emotion",
            markers=True,
            title="시간대별 감정 변화 (neutral 제거)",
            labels={"hour": "시간", "count": "메시지 수", "emotion": "emotion"},
            color_discrete_map=colors   # ← 여기만 추가
        )
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")

    # ========================================= 
    # ⏰ 4. 시간대별 전체 메시지 빈도
    # =========================================
    with st.container(border=True):
        st.header("메시지가 활발했던 시간대는 언제일까요?")
        st.markdown(
            "<span style='font-size:0.9rem; opacity:0.8;'>하루 중 어떤 시간대에 대화가 가장 많았는지 보여줍니다.</span>",
            unsafe_allow_html=True,
        )


    hour_count = df.groupby("hour").size().reset_index(name="count")

    fig = px.bar(
        hour_count,
        x="hour",
        y="count",
        title="시간대별 메시지 빈도",
        labels={"hour": "시간(0~23)", "count": "메시지 수"},
        color="count",  # ← 빈도에 따라 색상 변화
        color_continuous_scale="Blues",  # ← 색이 점점 진해지는 팔레트
    )
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig, use_container_width=True)



    # =========================================
    # 📌 5. 행동 패턴 (질문 / 이모티콘 / 사진 / 동영상)
    # =========================================
    


    action_colors = {
        "질문": "#B7415E",  # 딥 로즈 / 묵직한 와인
        "이모티콘":      "#E69F86",  # 테라코타 / 소프트 브라운
        "사진":       "#A3B9A9",  # 그레이시 민트
        "동영상":      "#69A0C3",  # 소프트 블루
        "very_positive": "#2E4A7D"   # 딥 네이비
    }
    action_colors = {
        "질문": "#69A0C3",  # 딥 로즈 / 묵직한 와인
        "이모티콘":      "#A3B9A9",  # 테라코타 / 소프트 브라운
        "사진":       "#E69F86",  # 그레이시 민트
        "동영상":      "#B7415E",  # 소프트 블루
        "very_positive": "#2E4A7D"   # 딥 네이비
    }

    action_colors = {
        "질문": "#69A0C3",
        "이모티콘": "#A3B9A9",
        "사진": "#E69F86",
        "동영상": "#B7415E",
        "very_positive": "#2E4A7D"
    }

    with st.container(border=True):
        st.header("대화 패턴은 어땠을까요?")
        st.markdown(
            "<span style='font-size:0.9rem; opacity:0.8;'>질문, 이모티콘, 사진, 동영상이 얼마나 자주 쓰였는지 시각화했어요.</span>",
            unsafe_allow_html=True,
        )

    action_df = (
        df.groupby("sender")[["is_question", "is_emoji", "is_photo", "is_video"]]
        .sum()
        .rename(columns={
            "is_question": "질문",
            "is_emoji": "이모티콘",
            "is_photo": "사진",
            "is_video": "동영상"
        })
    )

    def plot_user_patterns(sender, row):
        labels = ["질문", "이모티콘", "사진", "동영상"]
        values = [row[l] for l in labels]
        # 색상 매핑
        palette = [action_colors[label] for label in labels]

        # 도넛
        donut = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.5,
            textinfo='percent+label',
            marker=dict(colors=palette)   # ← 도넛 색 적용
        )])
        donut.update_layout(title=f"{sender} 행동 패턴 비율", height=350)

        # 절대 개수 막대(수평)
        bar = go.Figure(data=[go.Bar(
            x=values,
            y=labels,
            orientation='h',
            text=values,
            textposition='auto',
            marker=dict(color=palette)   # ← 도넛 색 적용
        )])
        bar.update_layout(title=f"{sender} 개수", height=350)

        return donut, bar

    # 사용자별 2개 그래프 배치
    for sender, row in action_df.iterrows():
        donut, bar = plot_user_patterns(sender, row)
        col1, col2 = st.columns(2)
        col1.plotly_chart(donut, use_container_width=True)
        col2.plotly_chart(bar, use_container_width=True)



    # =========================================
    # 💞 6. 애정 표현 분석
    # =========================================
    with st.expander("📌 애정 표현 점수(Affection Score) 기준 설명"):
        st.markdown("""
    ### 애정 표현 점수란?
    대화 메시지 안에 포함된 **애정·호감 표현을 감지하여 점수화한 값**입니다.

    ### 포함되는 표현 예시
    - **사랑 계열:** 사랑해, 사랑해요, 사랑합니다 등  
    - **호감/칭찬:** 좋아해, 보고싶어, 그리워, 귀여워, 예뻐, 고마워 등  
    - **하트/애정 이모티콘:** ❤️ 💕 💖 💘 ❣️ 😘 🥰 😍 등  

    ### 계산 방식  
    한 메시지에서 감지된 모든 패턴의 **총 개수**를 점수로 사용합니다.  
    예: `사랑해❤️❤️ 귀여워` → 점수 4
    """)
    with st.container(border=True):
        st.header("상대방과의 애정도를 확인해봐요")
        st.markdown(
            "<span style='font-size:0.9rem; opacity:0.8;'>누가 더 자주 애정 표현을 했는지 하트 그래프로 표현했어요.</span>",
            unsafe_allow_html=True,
        )

    

    # 1. 데이터 & 비율 계산
    aff_df = df.groupby("sender")["affection_score"].sum().reset_index()
    total_score = aff_df["affection_score"].sum()
    aff_df["affection_pct"] = aff_df["affection_score"] / total_score * 100  # %

    min_s = aff_df["affection_score"].min()
    max_s = aff_df["affection_score"].max()
    max_pct = aff_df["affection_pct"].max()

    def score_to_color(score):
        # 점수에 따라 핑크 -> 진한 와인톤으로
        norm = (score - min_s) / (max_s - min_s + 1e-9)
        r = 255
        g = int(80 + norm * 80)
        b = int(100 + norm * 70)
        return f"rgb({r},{g},{b})"

    fig = go.Figure()

    # 2. x좌표: 0.2 ~ 0.8 구간에 균등 배치 (가운데 모이게)
    x_positions = np.linspace(0.2, 0.8, len(aff_df))

    for i, row in aff_df.iterrows():
        sender = row["sender"]
        score = row["affection_score"]
        pct = row["affection_pct"]

        x = x_positions[i]
        y = pct  # y축을 비율로 사용

        # 비율에 따라 하트 크기 (확연히 차이나게)
        size = 40 + (pct / max_pct) * 80   # 최소 40 ~ 최대 120 정도

        heart_color = score_to_color(score)

        # 🔆 발광 레이어 (투명 큰 하트 2겹)
        for glow_size in [size + 10, size + 18]:
            fig.add_trace(go.Scatter(
                x=[x], y=[y],
                mode="text",
                text="❤️",
                textfont=dict(size=glow_size, color="rgba(255, 80, 80, 0.16)"),
                hoverinfo="skip",
                showlegend=False
            ))

        # 🎯 메인 하트
        fig.add_trace(go.Scatter(
            x=[x],
            y=[y],
            mode="text",
            text="❤️",
            textfont=dict(size=size, color=heart_color),
            hovertext=f"{sender}<br>애정 점수: {score}<br>비율: {pct:.1f}%",
            hoverinfo="text",
            showlegend=False
        ))

        # 📊 하트 아래에 % 숫자 표시
        fig.add_annotation(
            x=x,
            y=y - max_pct * 0.07,  # 하트 바로 아래로 약간 내리기
            text=f"{pct:.1f}%",
            showarrow=False,
            font=dict(size=14, color="white")
        )

    # 3. 레이아웃: x축·y축 보이게 설정
    fig.update_layout(
        height=500,
        margin=dict(l=40, r=40, t=60, b=60),
        xaxis=dict(
            range=[0, 1],
            tickmode="array",
            tickvals=x_positions,
            ticktext=aff_df["sender"],
            title="발신자",
            showgrid=False,
            zeroline=False
        ),
        yaxis=dict(
            range=[0, max_pct * 1.25],
            title="애정 표현 비율 (%)",
            showgrid=True,
            zeroline=True
        ),
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        title="발신자별 애정 표현 비율 (하트 플롯)"
    )

    st.plotly_chart(fig, use_container_width=True)




    # =========================================
    # 🔍 7 & 🌏 8. 키워드 네트워크 (2열 레이아웃)
    # =========================================

    with st.container(border=True):
        st.header("💬 주요 관심사는 이렇게 나타났어요")
        st.markdown(
            "<span style='font-size:0.9rem; opacity:0.8;'>대화에서 자주 등장한 키워드들을 네트워크로 시각화했어요.</span>",
            unsafe_allow_html=True,
        )


    col_left, col_right = st.columns(2)  # 2열 레이아웃

    # ------------------------------------------------
    # 🎯 왼쪽: 발신자별 키워드 네트워크
    # ------------------------------------------------
    with col_left:
        st.subheader("🔍 발신자별 키워드 네트워크")

        sender_selected = st.selectbox(
            "대화자 선택",
            keywords["sender"].unique(),
            key="sender_network"
        )

        # [1] 선택한 발신자의 상위 키워드
        top_kw_raw = keywords[keywords["sender"] == sender_selected]["top_keywords"].values[0]
        top_words = dict(ast.literal_eval(top_kw_raw))   # {"단어": 빈도}
        top_word_set = set(top_words.keys())

        # [2] 선택한 발신자의 대화만 필터링
        sender_df = df[df["sender"] == sender_selected]

        # [3] 동시출현 계산
        cooccur_counter = Counter()
        for nouns in sender_df["nouns"]:
            filtered = [n for n in nouns if n in top_word_set]
            unique = set(filtered)
            for a, b in combinations(sorted(unique), 2):
                cooccur_counter[(a, b)] += 1

        min_cooccur = st.slider(
            "최소 동시 출현 횟수",
            1, 5, 1,
            key="sender_min_cooccur",
            help="값을 높이면 강하게 연결된 키워드만 보여줍니다."
        )

        edges = [(a, b, w) for (a, b), w in cooccur_counter.items() if w >= min_cooccur]

        if not edges:
            st.info("선택한 조건에서 연결된 키워드가 없습니다. 슬라이더를 조정해보세요.")
        else:
            G = nx.Graph()

            # 노드 추가 (size = 빈도)
            for word, freq in top_words.items():
                G.add_node(word, size=freq)

            for a, b, w in edges:
                G.add_edge(a, b, weight=w)

            sizes = [G.nodes[n]["size"] for n in G.nodes()]
            vmin, vmax = min(sizes), max(sizes)
            norm = mcolors.Normalize(vmin=vmin, vmax=vmax)
            cmap = cm.Reds  # 빨간 계열 그라디언트
            node_colors = [cmap(norm(G.nodes[n]["size"])) for n in G.nodes()]

            node_sizes = [s * 80 for s in sizes]
            edge_widths = [G[u][v]["weight"] * 0.5 for u, v in G.edges()]

            fig, ax = plt.subplots(figsize=(6, 5))
            fig.patch.set_alpha(0)
            ax.set_facecolor("none")


            # 🔹 발신자 네트워크용 Shell Layout (2단)
            top_list_sender = list(top_words.keys())  # 발신자 키워드 사용

            layer1_sender = top_list_sender[:5]      # 중심층
            layer2_sender = top_list_sender[5:]      # 둘째층

            layers_sender = []
            if layer1_sender:
                layers_sender.append(layer1_sender)
            if layer2_sender:
                layers_sender.append(layer2_sender)

            pos = nx.shell_layout(G, nlist=layers_sender)


            nx.draw_networkx_nodes(
                G, pos,
                node_size=node_sizes,
                node_color=node_colors,
                alpha=0.7,
                ax=ax,
            )
            nx.draw_networkx_edges(
                G, pos,
                width=edge_widths,
                alpha=0.5,
                edge_color="#999999",
                ax=ax,
            )
            # 노드별 개별 라벨 사이즈 계산
            for node in G.nodes():
                node_pos = pos[node]
                size = G.nodes[node]["size"]
                font_size = 8 + (size / max(sizes)) * 10   # 최소 8 ~ 최대 18
                nx.draw_networkx_labels(
                    G, {node: node_pos},
                    labels={node: node},
                    font_size=int(font_size),
                    font_color="white",
                    font_family="Malgun Gothic",
                    ax=ax,
                )


            ax.set_title(f"{sender_selected}님의 키워드 네트워크", fontsize=12)
            ax.axis("off")
            st.pyplot(fig)
            


    # ------------------------------------------------
    # 🌏 오른쪽: 전체 대화 키워드 네트워크 (Shell Layout)
    # ------------------------------------------------
    with col_right:
        st.subheader("🌏 전체 대화 키워드 네트워크")

        # [1] 전체 명사 빈도
        all_nouns = []
        for nlist in df["nouns"]:
            all_nouns.extend(nlist)

        word_freq_series = pd.Series(all_nouns).value_counts()

        top_n = st.slider(
            "상위 키워드 개수",
            20, 100, 26,
            key="global_top_n",
            help="상위 빈도 키워드만 네트워크에 사용합니다."
        )
        top_global_words = word_freq_series.head(top_n)
        target_words = set(top_global_words.index)

        # [2] 전체 동시출현
        global_cooccur = Counter()
        for nouns in df["nouns"]:
            filtered = [n for n in nouns if n in target_words]
            unique = set(filtered)
            for a, b in combinations(sorted(unique), 2):
                global_cooccur[(a, b)] += 1

        min_cooccur_global = st.slider(
            "최소 동시 출현 횟수(전체)",
            1, 10, 3,
            key="global_min_cooccur",
            help="값을 높이면 강하게 연결된 키워드만 보여줍니다."
        )

        edges_global = [
            (a, b, w)
            for (a, b), w in global_cooccur.items()
            if w >= min_cooccur_global
        ]

        if not edges_global:
            st.info("선택한 조건에서 연결된 키워드가 없습니다. 슬라이더 값을 조정해보세요.")
        else:
            G2 = nx.Graph()

            for word, freq in top_global_words.items():
                G2.add_node(word, size=freq)

            for a, b, w in edges_global:
                if a in target_words and b in target_words:
                    G2.add_edge(a, b, weight=w)

            sizes2 = [G2.nodes[n]["size"] for n in G2.nodes()]
            vmin2, vmax2 = min(sizes2), max(sizes2)
            norm2 = mcolors.Normalize(vmin=vmin2, vmax=vmax2)
            cmap2 = cm.Blues  # 파란 계열 그라디언트
            node_colors2 = [cmap2(norm2(G2.nodes[n]["size"])) for n in G2.nodes()]

            node_sizes2 = [s * 40 for s in sizes2]
            edge_widths2 = [G2[u][v]["weight"] * 0.4 for u, v in G2.edges()]

            fig2, ax2 = plt.subplots(figsize=(6, 5))
            fig2.patch.set_alpha(0)
            ax2.set_facecolor("none")

            # 🔹 Shell Layout용 계층 나누기 (2~3단 동심원)
            top_list = list(top_global_words.index)

            layer1 = top_list[:5]       # 가장 중요한 키워드
            layer2 = top_list[5:30]     # 중간 중요도
            layer3 = top_list[30:]      # 나머지

            layers = []
            if layer1:
                layers.append(layer1)
            if layer2:
                layers.append(layer2)
            if layer3:
                layers.append(layer3)

            pos2 = nx.shell_layout(G2, nlist=layers)

            nx.draw_networkx_nodes(
                G2, pos2,
                node_size=node_sizes2,
                node_color=node_colors2,
                alpha=0.7,
                ax=ax2,
            )
            nx.draw_networkx_edges( 
                G2, pos2,
                width=edge_widths2,
                alpha=0.5,
                edge_color="#888888",
                ax=ax2,
            )
            # --------------------------
            # 라벨 개별 출력 + 자동 폰트 크기 조절
            # --------------------------
            max_size = max(sizes2)

            for node in G2.nodes():
                node_pos = pos2[node]
                node_size = G2.nodes[node]["size"]

                # 최소 8 ~ 최대 18 크기 (원하는 대로 바꿔도 됨)
                font_size = 8 + (node_size / max_size) * 10

                nx.draw_networkx_labels(
                    G2,
                    {node: node_pos},     # 해당 노드만 출력
                    labels={node: node},
                    font_size=int(font_size),
                    font_color="white",
                    font_family="Malgun Gothic",
                    ax=ax2,
                )


            ax2.set_title("전체 대화 키워드 네트워크", fontsize=12)
            ax2.axis("off")
            st.pyplot(fig2)
            
    # =========================================
    # 🔍 7 & 🌏 8. 워드클라우드 (2열 레이아웃 적용)
    # =========================================

    
        # 🔍 7 & 🌏 8. 워드클라우드 (2열 레이아웃 적용)
    # =========================================

    with st.container(border=True):
        st.header("💬 워드클라우드 시각화")
        st.markdown(
            "<span style='font-size:0.9rem; opacity:0.8;'>단어의 크기로 자주 등장한 표현을 한눈에 확인할 수 있어요.</span>",
            unsafe_allow_html=True,
        )

    col_left, col_right = st.columns(2)

    # ------------------------------------------------
    # 🎯 좌측: 발신자별 워드클라우드
    # ------------------------------------------------
    with col_left:
        st.subheader("🔍 발신자별 주요 키워드")

        sender_selected = st.selectbox("대화자 선택", keywords["sender"].unique(), key="wc_sender")

        top_kw_raw = keywords[keywords["sender"] == sender_selected]["top_keywords"].values[0]
        top_words = ast.literal_eval(top_kw_raw)

        wc = WordCloud(
            font_path="C:/Windows/Fonts/malgun.ttf",
            background_color="white",
            width=600,
            height=400
        )

        wc.generate_from_frequencies(dict(top_words))
        st.image(wc.to_array(), caption=f"{sender_selected}님의 주요 키워드")


    # ------------------------------------------------
    # 🌏 우측: 전체 대화 워드클라우드
    # ------------------------------------------------
    with col_right:
        st.subheader("🌏 전체 대화 워드클라우드")    
        st.markdown("<div style='height: 86px'></div>", unsafe_allow_html=True)


        all_nouns = []
        for nlist in df["nouns"]:
            all_nouns.extend(nlist)

        word_freq = pd.Series(all_nouns).value_counts().to_dict()

        wc2 = WordCloud(
            font_path="C:/Windows/Fonts/malgun.ttf",
            background_color="white",
            width=600,
            height=400
        )

        wc2.generate_from_frequencies(word_freq)
        st.image(wc2.to_array(), caption="전체 대화 워드클라우드")

    # =============== 🔹 메인으로 버튼 ===============
        st.markdown('<div class="back-btn">', unsafe_allow_html=True)
        if st.button("⬅ 메인으로", key="back_main_from_rooms"):
            st.session_state.page = "main"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
