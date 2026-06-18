from news_engine import get_today_news


def get_today_recommendations():
    news_list = get_today_news()

    candidates = [
        {
            "name": "대한전선",
            "theme": "전력",
            "base": 76,
            "summary": "전력 인프라 투자 확대 수혜 예상",
            "reasons": [
                "전력 인프라 투자 확대 수혜",
                "AI 데이터센터 전력망 수요 증가",
                "전력 테마 뉴스 관심 증가"
            ]
        },
        {
            "name": "LS ELECTRIC",
            "theme": "전력",
            "base": 74,
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
            "base": 73,
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
            "base": 75,
            "summary": "HBM과 AI 반도체 수요 확대 후보",
            "reasons": [
                "HBM 수요 증가",
                "AI 서버 투자 확대",
                "반도체 뉴스 관심 증가"
            ]
        },
        {
            "name": "한미반도체",
            "theme": "AI 반도체",
            "base": 73,
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
            "base": 72,
            "summary": "방산 수출 확대 관심 후보",
            "reasons": [
                "방산 수출 기대",
                "국방예산 확대",
                "글로벌 안보 이슈"
            ]
        }
    ]

    for stock in candidates:
        news_score = 0

        for news in news_list:
            if news["theme"] == stock["theme"]:
                news_score += 5

            if stock["name"] in news["title"]:
                news_score += 10

            if news["sentiment"] == "긍정":
                news_score += 3
            elif news["sentiment"] == "부정":
                news_score -= 5

        final_score = min(95, stock["base"] + news_score)
        probability = max(55, min(90, final_score - 6))
        confidence = max(60, min(88, final_score - 8))

        stock["score"] = final_score
        stock["probability"] = probability
        stock["confidence"] = confidence

        if final_score >= 82:
            stock["judgement"] = "관심"
            stock["timing"] = "양호"
        elif final_score >= 75:
            stock["judgement"] = "관망"
            stock["timing"] = "보통"
        else:
            stock["judgement"] = "주의"
            stock["timing"] = "대기"

    sorted_stocks = sorted(
        candidates,
        key=lambda x: x["score"],
        reverse=True
    )

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
            "reasons": stock["reasons"]
        })

    return result
