from news_engine import get_today_news
from price_engine import get_price_data
from stock_universe import get_stock_universe


def get_today_recommendations(limit=3):
    news_list = get_today_news()
    candidates = get_stock_universe()

    scored_stocks = []

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
            volume_score * 0.18 +
            momentum_score * 0.12 +
            news_score * 0.18 +
            theme_score * 0.14 +
            volatility_score * 0.08
        )

        probability = max(55, min(90, final_score - 5))
        confidence = max(60, min(88, final_score - 7))

        item = dict(stock)
        item["score"] = final_score
        item["probability"] = probability
        item["confidence"] = confidence
        item["price"] = price
        item["news_score"] = news_score
        item["theme_score"] = theme_score

        if final_score >= 82:
            item["judgement"] = "관심"
            item["timing"] = "양호"
        elif final_score >= 75:
            item["judgement"] = "관망"
            item["timing"] = "보통"
        else:
            item["judgement"] = "주의"
            item["timing"] = "대기"

        item["reasons"] = _make_reasons(item, price, news_score, theme_score)

        scored_stocks.append(item)

    sorted_stocks = sorted(scored_stocks, key=lambda x: x["score"], reverse=True)

    result = []

    for idx, stock in enumerate(sorted_stocks[:limit], start=1):
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
            "price": stock["price"],
            "theme": stock["theme"],
            "news_score": stock["news_score"],
            "theme_score": stock["theme_score"]
        })

    return result


def _calculate_news_score(stock, news_list):
    score = 50

    for news in news_list:
        if news["theme"] == stock["theme"]:
            score += 5

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
