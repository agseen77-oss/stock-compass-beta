STOCK_UNIVERSE = [
    {
        "name": "대한전선",
        "ticker": "001440.KS",
        "theme": "전력",
        "summary": "전력 인프라 투자 확대 수혜 후보",
        "base": 55,
        "reasons": ["전력 인프라 투자 확대", "AI 데이터센터 전력 수요", "전선 테마 관심"]
    },
    {
        "name": "LS ELECTRIC",
        "ticker": "010120.KS",
        "theme": "전력",
        "summary": "전력기기·스마트그리드 수혜 후보",
        "base": 55,
        "reasons": ["전력설비 투자 확대", "스마트그리드 관심", "전력 인프라 강세"]
    },
    {
        "name": "HD현대일렉트릭",
        "ticker": "267260.KS",
        "theme": "전력",
        "summary": "전력설비 수출 성장 후보",
        "base": 55,
        "reasons": ["변압기 수출 성장", "전력 인프라 투자 확대", "중장기 전력 수요"]
    },
    {
        "name": "제룡전기",
        "ticker": "033100.KQ",
        "theme": "전력",
        "summary": "변압기·전력설비 수혜 후보",
        "base": 53,
        "reasons": ["전력설비 투자 확대", "변압기 수요 기대", "전력 테마 연동"]
    },
    {
        "name": "두산에너빌리티",
        "ticker": "034020.KS",
        "theme": "원전",
        "summary": "원전·에너지 인프라 관심 후보",
        "base": 53,
        "reasons": ["원전 정책 기대", "에너지 인프라 투자", "대형주 수급 관심"]
    },
    {
        "name": "SK하이닉스",
        "ticker": "000660.KS",
        "theme": "AI 반도체",
        "summary": "HBM과 AI 반도체 수요 확대 후보",
        "base": 55,
        "reasons": ["HBM 수요 증가", "AI 서버 투자 확대", "반도체 뉴스 관심"]
    },
    {
        "name": "한미반도체",
        "ticker": "042700.KS",
        "theme": "AI 반도체",
        "summary": "AI 반도체 장비 수혜 후보",
        "base": 54,
        "reasons": ["HBM 장비 수요", "AI 반도체 투자 확대", "반도체 밸류체인 관심"]
    },
    {
        "name": "삼성전자",
        "ticker": "005930.KS",
        "theme": "AI 반도체",
        "summary": "메모리·AI 반도체 대표 후보",
        "base": 54,
        "reasons": ["메모리 업황 개선", "AI 반도체 기대", "대형주 수급 영향"]
    },
    {
        "name": "이수페타시스",
        "ticker": "007660.KS",
        "theme": "AI 반도체",
        "summary": "AI 서버 PCB 수혜 후보",
        "base": 52,
        "reasons": ["AI 서버 수요", "고다층 PCB 관심", "반도체 인프라 확대"]
    },
    {
        "name": "하나마이크론",
        "ticker": "067310.KQ",
        "theme": "AI 반도체",
        "summary": "반도체 후공정 관심 후보",
        "base": 51,
        "reasons": ["후공정 수요 기대", "AI 반도체 밸류체인", "반도체 업황 개선"]
    },
    {
        "name": "한화에어로스페이스",
        "ticker": "012450.KS",
        "theme": "방산",
        "summary": "방산 수출 확대 관심 후보",
        "base": 54,
        "reasons": ["방산 수출 기대", "국방예산 확대", "글로벌 안보 이슈"]
    },
    {
        "name": "LIG넥스원",
        "ticker": "079550.KS",
        "theme": "방산",
        "summary": "유도무기·방산 수출 후보",
        "base": 53,
        "reasons": ["방산 수출 기대", "유도무기 수요", "안보 이슈"]
    },
    {
        "name": "한국항공우주",
        "ticker": "047810.KS",
        "theme": "방산",
        "summary": "항공·방산 수출 관심 후보",
        "base": 52,
        "reasons": ["항공 방산 수요", "수출 기대", "국방 투자"]
    },
    {
        "name": "현대로템",
        "ticker": "064350.KS",
        "theme": "방산",
        "summary": "방산·철도 수주 관심 후보",
        "base": 52,
        "reasons": ["방산 수출 기대", "철도 수주 관심", "글로벌 수요"]
    },
    {
        "name": "한화시스템",
        "ticker": "272210.KS",
        "theme": "방산",
        "summary": "방산 전자·우주항공 관심 후보",
        "base": 51,
        "reasons": ["방산 전자 수요", "우주항공 관심", "국방예산 확대"]
    },
    {
        "name": "에스피시스템스",
        "ticker": "317830.KQ",
        "theme": "로봇",
        "summary": "스마트팩토리·로봇 자동화 관심 후보",
        "base": 50,
        "reasons": ["로봇 자동화 관심", "스마트팩토리 확대", "중소형 성장주"]
    },
    {
        "name": "현대차",
        "ticker": "005380.KS",
        "theme": "미래차",
        "summary": "전기차·자율주행 대표 후보",
        "base": 52,
        "reasons": ["전기차 전환", "자율주행 기대", "글로벌 판매 흐름"]
    },
    {
        "name": "LG디스플레이",
        "ticker": "034220.KS",
        "theme": "디스플레이",
        "summary": "OLED 업황 회복 관심 후보",
        "base": 49,
        "reasons": ["OLED 수요 회복 기대", "디스플레이 업황", "저평가 관심"]
    }
]


def get_stock_universe():
    return STOCK_UNIVERSE


def get_ticker(stock_name):
    for stock in STOCK_UNIVERSE:
        if stock["name"] == stock_name:
            return stock["ticker"]
    return ""


def get_theme(stock_name):
    for stock in STOCK_UNIVERSE:
        if stock["name"] == stock_name:
            return stock["theme"]
    return "시장"
