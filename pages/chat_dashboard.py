# pages/chat_dashboard.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import ast
import plotly.express as px

plt.rcParams['font.family'] = 'Malgun Gothic'


@st.cache_data
def load_data():
    df = pd.read_csv("output/analyzed_chat.csv")
    keywords = pd.read_csv("output/top_keywords.csv")

    # nouns 컬럼: 문자열 → 리스트 변환
    df["nouns"] = df["nouns"].apply(
        lambda x: ast.literal_eval(x) if isinstance(x, str) else []
    )

    return df, keywords


def chat_dashboard_page():
    # ⚠️ 여기서는 set_page_config 호출하지 않음 (app.py에서 한 번만!)
    st.title("카카오톡 대화 분석 대시보드")

    df, keywords = load_data()

    # =========================================
    # 📊 1. 전체 요약
    # =========================================
    st.header("전체 요약 통계")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("총 메시지 수", len(df))
    col2.metric("참여자 수", df["sender"].nunique())
    col3.metric("평균 메시지 길이", round(df["msg_len"].mean(), 1))
    col4.metric("평균 단어 수", round(df["word_count"].mean(), 1))

    # =========================================
    # 😊 2. 감정 분석 — neutral 포함 & 제외
    # =========================================
    st.header("감정 분석")

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
