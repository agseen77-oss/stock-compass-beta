from price_engine import get_price_data
from news_engine import get_today_news


def get_score_breakdown(stock_name):
    price = get_price_data(stock_name)
    news_list = get_today_news()

    theme = _detect_stock_theme(stock_name)

    news_score = 50
    for news in news_list:
        if news["theme"] == theme:
            news_score += 6
        if stock_name in news["title"]:
            news_score += 12
        if news["sentiment"] == "긍정":
            news_score += 4
        elif news["sentiment"] == "부정":
            news_score -= 6

    news_score = max(30, min(100, news_score))

    theme_count = sum(1 for news in news_list if news["theme"] == theme)
    if theme_count >= 4:
        theme_score = 90
    elif theme_count >= 3:
        theme_score = 82
    elif theme_count >= 2:
        theme_score = 74
    elif theme_count >= 1:
        theme_score = 65
    else:
        theme_score = 55

    chart = price["chart_score"]
    supply = price["volume_score"]
    volatility = price["volatility_score"]

    final = round(
        chart * 0.30 +
        supply * 0.20 +
        news_score * 0.20 +
        theme_score * 0.20 +
        volatility * 0.10
    )

    return {
        "chart": chart,
        "news": news_score,
        "supply": supply,
        "theme": theme_score,
        "volatility": volatility,
        "final": final
    }


def _detect_stock_theme(stock_name):
    if stock_name in ["대한전선", "LS ELECTRIC", "HD현대일렉트릭"]:
        return "전력"
    if stock_name in ["SK하이닉스", "한미반도체"]:
        return "AI 반도체"
    if stock_name in ["한화에어로스페이스"]:
        return "방산"
    return "시장"
