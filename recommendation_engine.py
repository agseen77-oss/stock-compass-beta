from news_engine import get_today_news
from price_engine import get_price_data


def get_today_recommendations():
    news_list = get_today_news()

    candidates = [
        {
            "name": "대한전선",
            "theme": "전력",
            "base": 55,
            "summary": "전력 인프라 투자 확대 수혜 후보",
            "reasons": [
                "전력 인프라 투자 확대 수혜",
                "AI 데이터센터 전력망 수요 증가",
                "전력 테마 뉴스 관심"
            ]
        },
        {
            "name": "LS ELECTRIC",
            "theme": "전력",
            "base": 55,
            "summary": "전력기기·스마트그리드 수혜 후보",
            "reasons": [
                "전력설비 투자 확대",
                "스마트그리드 관심 증가",
                "전력 인프라 테마 강세"
            ]
        },
        {
            "name": "HD현대일렉트릭",
            "theme": "전력",
            "base": 55,
            "summary": "전력설비 수출 성장 후보",
            "reasons": [
                "변압기 수출 성장",
                "전력 인프라 투자 확대",
                "중장기 전력 수요 기대"
            ]
        },
        {
            "name": "SK하이닉스",
            "theme": "AI 반도체",
            "base": 55,
            "summary": "HBM과 AI 반도체 수요 확대 후보",
            "reasons": [
                "HBM 수요 증가",
                "AI 서버 투자 확대",
                "반도체 뉴스 관심"
            ]
        },
        {
            "name": "한미반도체",
            "theme": "AI 반도체",
            "base": 55,
            "summary": "AI 반도체 장비 수혜 후보",
            "reasons": [
                "HBM 장비 수요 기대",
                "AI 반도체 투자 확대",
                "반도체 밸류체인 관심"
            ]
        },
        {
            "name": "한화에어로스페이스",
            "theme": "방산",
            "base": 55,
            "summary": "방산 수출 확대 관심 후보",
            "reasons": [
                "방산 수출 기대",
                "국방예산 확대",
                "글로벌 안보 이슈"
            ]
        }
    ]

    for stock in candidates:
        price = get_price_data(stock["name"])
        news_score = _calculate_news_score(stock, news_list)
        theme_score = _calculate_theme_score(stock, news_list)

        chart_score = price["chart_score"]
        volume_score = price["volume_score"]
        momentum_score = price["momentum_score"]
        volatility_score = price["volatility_score"]

        final_score = round(
            chart_score * 0.30 +
            volume_score * 0.20 +
            news_score * 0.20 +
            theme_score * 0.20 +
            volatility_score * 0.10
        )

        probability = max(55, min(90, final_score - 5))
        confidence = max(60, min(88, final_score - 7))

        stock["score"] = final_score
        stock["probability"] = probability
        stock["confidence"] = confidence
        stock["price"] = price

        if final_score >= 82:
            stock["judgement"] = "관심"
            stock["timing"] = "양호"
        elif final_score >= 75:
            stock["judgement"] = "관망"
            stock["timing"] = "보통"
        else:
            stock["judgement"] = "주의"
            stock["timing"] = "대기"

        stock["reasons"] = _make_reasons(stock, price, news_score, theme_score)

    sorted_stocks = sorted(candidates, key=lambda x: x["score"], reverse=True)

    result = []

    for idx, stock in enumerate(sorted_stocks[:3], start=1):
        result.append({
            "rank": idx,
            "name": stock["name"],
            "score": stock["score"],
            "confidence": stock["confidence"],
            "probability": stock["probability"],
            "timing": stock["timing"],
            "judgement": stock["judgement"],
            "risk": "보통",
            "summary": stock["summary"],
            "reasons": stock["reasons"],
            "price": stock["price"]
        })

    return result


def _calculate_news_score(stock, news_list):
    score = 50

    for news in news_list:
        if news["theme"] == stock["theme"]:
            score += 6

        if stock["name"] in news["title"]:
            score += 12

        if news["sentiment"] == "긍정":
            score += 4
        elif news["sentiment"] == "부정":
            score -= 6

    return max(30, min(100, score))


def _calculate_theme_score(stock, news_list):
    theme_count = sum(1 for news in news_list if news["theme"] == stock["theme"])

    if theme_count >= 4:
        return 90
    if theme_count >= 3:
        return 82
    if theme_count >= 2:
        return 74
    if theme_count >= 1:
        return 65
    return 55


def _make_reasons(stock, price, news_score, theme_score):
    reasons = []

    if price["data_ok"]:
        reasons.append(f"실제 차트 점수 {price['chart_score']}점")
        reasons.append(f"거래량 강도 {price['volume_ratio']}배")
        reasons.append(f"당일 등락률 {price['change_rate']}%")
    else:
        reasons.append("가격 데이터를 불러오지 못해 기본 점수 적용")

    reasons.append(f"뉴스 점수 {news_score}점")
    reasons.append(f"{stock['theme']} 테마 점수 {theme_score}점")

    return reasons
