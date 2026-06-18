def get_score_breakdown(stock_name):
    score_map = {
        "대한전선": {
            "chart": 88,
            "news": 82,
            "supply": 79,
            "theme": 91,
            "volatility": 76,
            "final": 84
        },
        "LS ELECTRIC": {
            "chart": 84,
            "news": 80,
            "supply": 76,
            "theme": 89,
            "volatility": 74,
            "final": 81
        },
        "HD현대일렉트릭": {
            "chart": 81,
            "news": 78,
            "supply": 73,
            "theme": 87,
            "volatility": 72,
            "final": 79
        }
    }

    return score_map.get(stock_name, {
        "chart": 70,
        "news": 70,
        "supply": 70,
        "theme": 70,
        "volatility": 70,
        "final": 70
    })
