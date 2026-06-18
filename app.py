import streamlit as st
from recommendation_engine import get_today_recommendations

st.set_page_config(
    page_title="Stock Compass Beta",
    page_icon="🧭",
    layout="centered"
)

recs = get_today_recommendations()
top = recs[0]

st.markdown("""
<style>
.block-container {
    padding-top: 1.1rem;
    padding-left: 1rem;
    padding-right: 1rem;
    max-width: 430px;
}
.title {
    font-size: 25px;
    font-weight: 900;
}
.sub {
    color: #777;
    font-size: 13px;
    margin-bottom: 18px;
}
.main-card {
    border-radius: 20px;
    padding: 20px;
    background: linear-gradient(135deg, #eef9f1, #ffffff);
    border: 1px solid #dcefe2;
    margin-bottom: 20px;
}
.stock {
    font-size: 32px;
    font-weight: 900;
    margin-bottom: 4px;
}
.stars {
    font-size: 22px;
    margin-bottom: 12px;
}
.badge {
    display: inline-block;
    padding: 6px 10px;
    border-radius: 999px;
    background: #eef4ff;
    font-size: 13px;
    margin: 3px 3px 8px 0;
}
.judgement {
    background: #f1f8ff;
    padding: 13px;
    border-radius: 14px;
    font-size: 14px;
    line-height: 1.6;
    margin-top: 12px;
}
.reason {
    font-size: 14px;
    line-height: 1.8;
}
.rank-card {
    border: 1px solid #eeeeee;
    border-radius: 16px;
    padding: 14px;
    margin-bottom: 10px;
    background: #ffffff;
}
.rank-title {
    font-size: 17px;
    font-weight: 800;
}
.small {
    color: #777;
    font-size: 13px;
}
.notice {
    background: #fff8df;
    padding: 12px;
    border-radius: 14px;
    color: #665200;
    font-size: 12px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🧭 Stock Compass Beta</div>', unsafe_allow_html=True)
st.markdown('<div class="sub">오늘 시장에서 가장 먼저 볼 종목</div>', unsafe_allow_html=True)

st.markdown("## 오늘의 컴파스 추천")

st.markdown(f"""
<div class="main-card">
    <div class="stock">{top['name']}</div>
    <div class="stars">★★★★★</div>
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

st.markdown("## 추천 이유")

for reason in top["reasons"]:
    st.markdown(f'<div class="reason">✅ {reason}</div>', unsafe_allow_html=True)

st.markdown("## 오늘 시장 온도")

col1, col2 = st.columns(2)
col1.metric("시장점수", "72점")
col2.metric("시장상태", "긍정")

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