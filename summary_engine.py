from recommendation_engine import get_today_recommendations


def get_today_summary():
    top = get_today_recommendations()[0]

    return {
        "market_status": "강세",
        "main_theme": "뉴스 기반 주도 테마",
        "main_stock": top["name"],
        "strategy": f"{top['judgement']} 유지, 무리한 추격매수는 주의",
        "comment": f"오늘 컴파스 기준 대표 후보는 {top['name']}입니다. 뉴스, 테마, 점수를 종합해 가장 높은 기대값을 보인 종목입니다."
    }