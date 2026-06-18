import streamlit as st
from recommendation_engine import get_today_recommendations
from theme_engine import get_today_themes
from market_engine import get_market_signal
from news_engine import get_today_news
from summary_engine import get_today_summary
from score_engine import get_score_breakdown

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
score = get_score_breakdown(top["name"])

price = top.get("price", {})
current_price = price.get("current_price", 0)
change_rate = price.get("change_rate", 0)
volume_ratio = price.get("volume_ratio", 1)
data_ok = price.get("data_ok", False)

st.markdown("""
<style>
.block-container {
    padding-top: 2.4rem;
    padding-left: 1rem;
    padding-right: 1rem;
    max-width: 430px;
}
.title {font-size: 23px; font-weight: 900; color:#111827 !important;}
.sub {color:#4b5563 !important; font-size:13px; margin-bottom:24px;}
.main-card {
    border-radius: 22px;
    padding: 20px;
    background: linear-gradient(135deg, #eef9f1, #ffffff) !important;
    border: 1px solid #dcefe2;
    margin-bottom: 18px;
    color:#111827 !important;
}
.main-card * {color:#111827 !important;}
.action-card {
    border-radius: 22px;
    padding: 20px;
    background: #111827 !important;
    color: white !important;
    margin-bottom: 20px;
}
.action-card * {color:white !important;}
.action-label {font-size: 14px; color: #cbd5e1 !important;}
.action-main {font-size: 34px; font-weight: 900; margin: 6px 0;}
.stock {font-size: 31px; font-weight: 900;}
.badge {
    display:inline-block;
    padding:6px 10px;
    border-radius:999px;
    background:#eef4ff !important;
    color:#111827 !important;
    font-size:13px;
    margin:3px 3px 8px 0;
}
.rank-card {
    border:1px solid #e5e7eb;
    border-radius:16px;
    padding:14px;
    margin-bottom:10px;
    background:#ffffff !important;
    color:#111827 !important;
}
.rank-card * {color:#111827 !important;}
.rank-title {font-size:17px; font-weight:800; color:#111827 !important;}
.small {color:#4b5563 !important; font-size:13px;}
.reason {font-size:14px; line-height:1.8; color:#111827 !important;}
.notice {
    background:#fff8df !important;
    padding:12px;
    border-radius:14px;
    color:#665200 !important;
    font-size:12px;
    margin-top: 18px;
}
.notice * {color:#665200 !important;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🧭 Stock Compass Beta</div>', unsafe_allow_html=True)
st.markdown('<div class="sub">오늘 시장에서 가장 먼저 볼 종목</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="action-card">
    <div class="action-label">📌 오늘 행동</div>
    <div class="action-main">🟡 {top['judgement']}</div>
    <div>대표종목 : {top['name']}</div>
    <div>신뢰도 : {top['confidence']}%</div>
    <div>추천비중 : 20% 이내</div>
    <div>전략 : {summary['strategy']}</div>
</div>
""", unsafe_allow_html=True)

st.markdown("## 오늘의 컴파스 추천")

price_badge = ""
if data_ok:
    price_badge = f"""
    <span class="badge">현재가 {current_price:,}원</span>
    <span class="badge">등락률 {change_rate}%</span>
    """

st.markdown(f"""
<div class="main-card">
    <div class="stock">{top['name']}</div>
    <span class="badge">종합점수 {top['score']}점</span>
    <span class="badge">상승확률 {top['probability']}%</span>
    <span class="badge">{top['judgement']}</span>
    <span class="badge">타이밍 {top['timing']}</span>
    {price_badge}
</div>
""", unsafe_allow_html=True)

st.markdown("### 🧭 컴파스 판단")
st.info(f"{top['summary']}\n\n중기 상승 가능성이 높은 후보로 판단됩니다.")

st.markdown("## 🧾 왜 1등인가?")

with st.container(border=True):
    st.markdown(f"### {top['name']} 선정 근거")
    st.write(f"최종점수 **{score['final']}점**은 아래 항목을 종합해 계산했습니다.")

    reason_rows = [
        ("테마", score["theme"], "오늘 뉴스에서 관련 테마가 얼마나 강하게 부각되는지"),
        ("차트", score["chart"], "현재가가 주요 이동평균선 위에 있는지"),
        ("뉴스", score["news"], "긍정/부정 뉴스와 종목·테마 연관성"),
        ("수급", score["supply"], "거래량이 평소보다 강한지"),
        ("변동성", score["volatility"], "최근 변동성이 과도하지 않은지"),
    ]

    for label, value, desc in reason_rows:
        st.write(f"**{label} {value}점**")
        st.caption(desc)
        st.progress(value / 100)

    if data_ok:
        st.success(
            f"실제 가격 데이터 반영: 현재가 {current_price:,}원, "
            f"등락률 {change_rate}%, 거래량 강도 {volume_ratio}배"
        )
    else:
        st.warning("가격 데이터를 불러오지 못해 일부 기본 점수가 적용됐습니다.")

st.markdown("## 📊 점수 분석")

with st.container(border=True):
    col1, col2 = st.columns(2)
    col1.metric("최종점수", f"{score['final']}점")
    col2.metric("신뢰도", f"{top['confidence']}%")

    score_items = [
        ("테마", score["theme"]),
        ("차트", score["chart"]),
        ("뉴스", score["news"]),
        ("수급", score["supply"]),
        ("변동성", score["volatility"]),
    ]

    for label, value in score_items:
        st.write(f"{label} : {value}점")
        st.progress(value / 100)

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

for idx, news in enumerate(news_list, start=1):
    with st.expander(f"{idx}. {news['title']}", expanded=False):
        st.caption(f"테마 : {news['theme']} · 판단 : {news['sentiment']}")
        st.write(news["summary"])
        if news.get("link"):
            st.link_button("뉴스 보기", news["link"])

st.markdown("## 🧭 오늘의 결론")

st.markdown(f"""
<div class="main-card">
    <div class="rank-title">시장상태 : {summary['market_status']}</div>
    <div class="small">주도테마 : {summary['main_theme']}</div>
    <div class="small">대표종목 : {summary['main_stock']}</div>
</div>
""", unsafe_allow_html=True)

st.info(f"전략 : {summary['strategy']}\n\n{summary['comment']}")

st.markdown("## 오늘의 TOP3")

medals = ["🥇", "🥈", "🥉"]

for idx, item in enumerate(recs):
    item_price = item.get("price", {})
    price_text = ""
    if item_price.get("data_ok"):
        price_text = f"<div class='small'>현재가 {item_price.get('current_price', 0):,}원 · 등락률 {item_price.get('change_rate', 0)}%</div>"

    st.markdown(f"""
<div class="rank-card">
    <div class="rank-title">{medals[idx]} {item['name']}</div>
    <div>{item['score']}점 · 상승확률 {item['probability']}% · {item['judgement']}</div>
    {price_text}
    <div class="small">{item['summary']}</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="notice">
※ 이 서비스는 투자 판단 보조용이며, 실제 투자 결정은 본인 책임입니다.
</div>
""", unsafe_allow_html=True)
