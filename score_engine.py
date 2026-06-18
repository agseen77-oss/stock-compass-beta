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
        },
        "SK하이닉스": {
            "chart": 86,
            "news": 84,
            "supply": 80,
            "theme": 90,
            "volatility": 70,
            "final": 83
        },
        "한미반도체": {
            "chart": 82,
            "news": 81,
            "supply": 77,
            "theme": 88,
            "volatility": 68,
            "final": 80
        },
        "한화에어로스페이스": {
            "chart": 80,
            "news": 79,
            "supply": 76,
            "theme": 84,
            "volatility": 71,
            "final": 78
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