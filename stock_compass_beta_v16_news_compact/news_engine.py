import re
import feedparser


def get_today_news():
    rss_urls = [
        "https://news.google.com/rss/search?q=전력%20AI%20데이터센터%20주식&hl=ko&gl=KR&ceid=KR:ko",
        "https://news.google.com/rss/search?q=반도체%20HBM%20AI%20주식&hl=ko&gl=KR&ceid=KR:ko",
        "https://news.google.com/rss/search?q=방산%20주식%20수출&hl=ko&gl=KR&ceid=KR:ko",
    ]

    news_list = []
    seen = set()

    for url in rss_urls:
        feed = feedparser.parse(url)

        for entry in feed.entries[:4]:
            raw_title = entry.get("title", "")
            title = clean_title(raw_title)
            link = entry.get("link", "")

            if not title or title in seen:
                continue

            seen.add(title)

            theme = detect_theme(title)
            sentiment = detect_sentiment(title)

            news_list.append({
                "title": title,
                "theme": theme,
                "sentiment": sentiment,
                "summary": make_summary(title, theme, sentiment),
                "link": link
            })

    if not news_list:
        return [
            {
                "title": "뉴스를 불러오지 못했습니다",
                "theme": "시장",
                "sentiment": "중립",
                "summary": "인터넷 연결 또는 RSS 응답 상태를 확인해 주세요.",
                "link": ""
            }
        ]

    return news_list[:5]


def clean_title(title):
    title = re.sub(r"\s+-\s+[^-]+$", "", title)
    title = title.replace("&quot;", "\"").replace("&amp;", "&")
    return title.strip()


def make_summary(title, theme, sentiment):
    return f"{theme} 관련 뉴스입니다. 현재 컴파스 판단은 {sentiment}으로 분류됩니다."


def detect_theme(title):
    if any(word in title for word in ["전력", "전선", "전기", "데이터센터", "전력망", "변압기"]):
        return "전력"
    if any(word in title for word in ["반도체", "HBM", "AI", "엔비디아", "하이닉스"]):
        return "AI 반도체"
    if any(word in title for word in ["방산", "국방", "무기", "수출"]):
        return "방산"
    return "시장"


def detect_sentiment(title):
    positive_words = ["상승", "강세", "확대", "수혜", "기대", "수주", "성장", "호조", "급증"]
    negative_words = ["하락", "약세", "부진", "우려", "급락", "감소"]

    if any(word in title for word in positive_words):
        return "긍정"
    if any(word in title for word in negative_words):
        return "부정"
    return "중립"
