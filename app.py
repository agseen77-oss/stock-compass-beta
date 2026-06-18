import streamlit as st
from recommendation_engine import get_today_recommendations
from theme_engine import get_today_themes
from market_engine import get_market_signal
from news_engine import get_today_news
from summary_engine import get_today_summary

st.set_page_config(
    page_title="Stock Compass Beta",
    page_icon="🧭",
    layout="centered"
)

recs = get_today_recommendations()
top = recs[0]
themes = get_today_themes()
market = get_market_signal()
news_list = get_today_news()
summary = get_today_summary()

st.markdown("""
<style>
.block-container {
    padding-top: 2.4rem;
    padding-left: 1rem;
    padding-right: 1rem;
    max-width: 430px;
}
.title {font-size: 23px; font-weight: 900;}
.sub {color:#777; font-size:13px; margin-bottom:24px;}
.main-card {
    border-radius: 22px;
    padding: 20px;
    background: linear-gradient(135deg, #eef9f1, #ffffff);
    border: 1px solid #dcefe2;
    margin-bottom: 18px;
}
.action-card {
    border-radius: 22px;
    padding: 20px;
    background: #111827;
    color: white;
    margin-bottom: 20px;
}
.action-label {
    font-size: 14px;
    color: #cbd5e1;
}
.action-main {
    font-size: 34px;
    font-weight: 900;
    margin: 6px 0;
}
.stock {font-size: 31px; font-weight: 900;}
.badge {
    display:inline-block;
    padding:6px 10px;
    border-radius:999px;
    background:#eef4ff;
    font-size:13px;
    margin:3px 3px 8px 0;
}
.judgement {
    background:#f1f8ff;
    padding:13px;
    border-radius:14px;
    font-size:14px;
    line-height:1.6;
    margin-top:12px;
}
.rank-card {
    border:1px solid #eee;
    border-radius:16px;
    padding:14px;
    margin-bottom:10px;
    background:#fff;
}
.rank-title {font-size:17px; font-weight:800;}
.small {color:#777; font-size:13px;}
.reason {font-size:14px; line-height:1.8;}
.notice {
    background:#fff8df;
    padding:12px;
    border-radius:14px;
    color:#665200;
    font-size:12px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🧭 Stock Compass Beta</div>', unsafe_allow_html=True)
st.markdown('<div class="sub">오늘 시장에서 가장 먼저 볼 종목</div>', unsafe_allow_html=True)

st.markdown("""
<div class="action-card">
    <div class="action-label">📌 오늘 행동</div>
    <div class="action-main">관심</div>
    <div>대표종목 : 대한전선</div>
    <div>전략 : 관심 유지, 무리한 추격매수는 주의</div>
</div>
""", unsafe_allow_html=True)

st.markdown("## 오늘의 컴파스 추천")

st.markdown(f"""
<div class="main-card">
    <div class="stock">{top['name']}</div>
    <span class="badge">종합점수 {top['score']}점</span>
    <span class="badge">상승확률 {top['probability']}%</span>
    <span class="badge">{top['judgement']}</span>
    <span class="badge">타이밍 {top['timing']}</span>

    <div class="judgement">
        <b>🧭 컴파스 판단</b><br>
        {top['summary']}<br>
        중기 상승 가능성이 높은 후보로 판단됩니다.
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("## 🟢 시장 신호등")

st.markdown(f"""
<div class="rank-card">
    <div class="rank-title">{market['signal']} 현재 시장 : {market['status']}</div>
    <div class="small">시장점수 {market['score']}점</div>
    <div class="small">{market['summary']}</div>
</div>
""", unsafe_allow_html=True)

for sector in market["sectors"]:
    st.markdown(f"""
<div class="rank-card">
    <div class="rank-title">{sector['name']}</div>
    <div class="small">{sector['status']}</div>
</div>
""", unsafe_allow_html=True)

st.markdown("## 🔥 오늘의 유망 테마")

selected_theme_name = st.selectbox(
    "테마 상세보기",
    [theme["theme"] for theme in themes]
)

selected_theme = next(theme for theme in themes if theme["theme"] == selected_theme_name)

for theme in themes:
    st.markdown(f"""
<div class="rank-card">
    <div class="rank-title">{theme['rank']}위 {theme['theme']}</div>
    <div>{theme['grade']} · {theme['status']}</div>
    <div class="small">관심도 {theme['score']}점</div>
</div>
""", unsafe_allow_html=True)

st.markdown("## 테마 상세 분석")

with st.container(border=True):
    st.markdown(f"### 🔥 {selected_theme['theme']}")
    st.metric("관심도", f"{selected_theme['score']}점")
    st.write(f"**등급:** {selected_theme['grade']}")
    st.write(f"**상태:** {selected_theme['status']}")
    st.info(selected_theme["reason"])

    st.markdown("#### 관련 종목")
    for stock in selected_theme["stocks"]:
        st.write(f"✅ {stock}")

st.markdown("## 추천 이유")

for reason in top["reasons"]:
    st.markdown(f'<div class="reason">✅ {reason}</div>', unsafe_allow_html=True)

st.markdown("## 📰 오늘 핵심 뉴스")

for news in news_list:
    st.markdown(f"""
<div class="rank-card">
    <div class="rank-title">{news['title']}</div>
    <div class="small">테마 : {news['theme']} · 판단 : {news['sentiment']}</div>
    <div class="small">{news['summary']}</div>
</div>
""", unsafe_allow_html=True)

st.markdown("## 🧭 오늘의 결론")

st.markdown(f"""
<div class="main-card">
    <div class="rank-title">시장상태 : {summary['market_status']}</div>
    <div class="small">주도테마 : {summary['main_theme']}</div>
    <div class="small">대표종목 : {summary['main_stock']}</div>
    <div class="judgement">
        <b>전략</b><br>
        {summary['strategy']}<br><br>
        {summary['comment']}
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("## 오늘의 TOP3")

medals = ["🥇", "🥈", "🥉"]

for idx, item in enumerate(recs):
    st.markdown(f"""
<div class="rank-card">
    <div class="rank-title">{medals[idx]} {item['name']}</div>
    <div>{item['score']}점 · 상승확률 {item['probability']}% · {item['judgement']}</div>
    <div class="small">{item['summary']}</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="notice">
※ 이 서비스는 투자 판단 보조용이며, 실제 투자 결정은 본인 책임입니다.
</div>
""", unsafe_allow_html=True)