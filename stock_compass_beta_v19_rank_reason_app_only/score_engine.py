from price_engine import get_price_data
from news_engine import get_today_news
from stock_universe import get_theme


def get_score_breakdown(stock_name):
    price = get_price_data(stock_name)
    news_list = get_today_news()
    theme = get_theme(stock_name)

    news_score = 50

    for news in news_list:
        if news["theme"] == theme:
            news_score += 5
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
    momentum = price["momentum_score"]
    volatility = price["volatility_score"]

    final = round(
        chart * 0.30 +
        supply * 0.18 +
        momentum * 0.12 +
        news_score * 0.18 +
        theme_score * 0.14 +
        volatility * 0.08
    )

    return {
        "chart": chart,
        "news": news_score,
        "supply": supply,
        "theme": theme_score,
        "volatility": volatility,
        "momentum": momentum,
        "final": final
    }
