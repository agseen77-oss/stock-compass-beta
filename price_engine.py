from functools import lru_cache
from datetime import datetime, timedelta
import ast
import requests
import yfinance as yf
from stock_universe import get_ticker


def get_price_data(stock_name):
    ticker = get_ticker(stock_name)
    if not ticker:
        return _empty_price("NO_TICKER")
    return _download_price(ticker)


@lru_cache(maxsize=128)
def _download_price(ticker):
    symbol = _to_krx_code(ticker)

    for source_name, data in [
        ("yahoo_direct", _safe_yahoo_chart(ticker)),
        ("yfinance", _safe_yfinance(ticker)),
        ("naver", _safe_naver(symbol)),
    ]:
        result = _make_price_result(data, source=source_name, ticker=ticker)
        if result["data_ok"]:
            return result

    return _empty_price("ALL_PRICE_SOURCES_FAILED")


def _safe_yahoo_chart(ticker):
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
        params = {"range": "6mo", "interval": "1d", "includePrePost": "false", "events": "history"}
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, params=params, headers=headers, timeout=12)
        response.raise_for_status()
        payload = response.json()

        result = payload.get("chart", {}).get("result", [])
        if not result:
            return None

        quote = result[0].get("indicators", {}).get("quote", [])
        if not quote:
            return None

        close = [x for x in quote[0].get("close", []) if x is not None]
        volume = [x for x in quote[0].get("volume", []) if x is not None]

        if len(close) < 2:
            return None

        return {"Close": close, "Volume": volume}
    except Exception:
        return None


def _safe_yfinance(ticker):
    try:
        data = yf.Ticker(ticker).history(period="6mo", interval="1d", auto_adjust=True)
        if data is not None and not data.empty:
            return data
    except Exception:
        pass

    try:
        data = yf.download(ticker, period="6mo", interval="1d", progress=False, auto_adjust=True, threads=False)
        if data is not None and not data.empty:
            return data
    except Exception:
        pass

    return None


def _safe_naver(symbol):
    try:
        end = datetime.now()
        start = end - timedelta(days=240)
        url = (
            "https://api.finance.naver.com/siseJson.naver"
            f"?symbol={symbol}&requestType=1"
            f"&startTime={start.strftime('%Y%m%d')}"
            f"&endTime={end.strftime('%Y%m%d')}"
            "&timeframe=day"
        )
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": f"https://finance.naver.com/item/sise_day.naver?code={symbol}",
        }
        response = requests.get(url, headers=headers, timeout=12)
        response.raise_for_status()
        response.encoding = "euc-kr"
        rows = ast.literal_eval(response.text.strip())

        closes, volumes = [], []
        for row in rows[1:]:
            if len(row) >= 6 and row[4] is not None and row[5] is not None:
                closes.append(float(row[4]))
                volumes.append(float(row[5]))

        if len(closes) < 2:
            return None

        return {"Close": closes, "Volume": volumes}
    except Exception:
        return None


def _make_price_result(data, source, ticker=""):
    if data is None:
        return _empty_price(f"{source}_NO_DATA")

    try:
        close = _get_close(data)
        volume = _get_volume(data)

        close = [float(x) for x in close if x is not None]
        volume = [float(x) for x in volume if x is not None]

        if len(close) < 2 or len(volume) < 2:
            return _empty_price(f"{source}_SHORT_DATA")

        current_price = close[-1]
        prev_price = close[-2]
        change_rate = ((current_price - prev_price) / prev_price) * 100 if prev_price else 0

        ma5 = _moving_average(close, 5)
        ma20 = _moving_average(close, 20)
        ma60 = _moving_average(close, 60)

        avg_volume20 = _moving_average(volume, 20)
        last_volume = volume[-1]
        volume_ratio = last_volume / avg_volume20 if avg_volume20 else 1

        high_6m = max(close)
        distance_from_high = ((current_price - high_6m) / high_6m) * 100 if high_6m else 0

        return {
            "ticker": ticker,
            "current_price": round(current_price),
            "change_rate": round(change_rate, 2),
            "ma5": round(ma5),
            "ma20": round(ma20),
            "ma60": round(ma60),
            "volume_ratio": round(volume_ratio, 2),
            "distance_from_high": round(distance_from_high, 2),
            "chart_score": _score_chart(current_price, ma5, ma20, ma60),
            "volume_score": _score_volume(volume_ratio),
            "momentum_score": _score_momentum(change_rate),
            "volatility_score": _score_volatility(close),
            "source": source,
            "error_reason": "",
            "data_ok": True,
        }
    except Exception:
        return _empty_price(f"{source}_PARSE_FAILED")


def _get_close(data):
    if isinstance(data, dict):
        return data["Close"]
    value = data["Close"]
    if hasattr(value, "columns"):
        return value.iloc[:, 0].dropna().tolist()
    return value.dropna().tolist()


def _get_volume(data):
    if isinstance(data, dict):
        return data["Volume"]
    value = data["Volume"]
    if hasattr(value, "columns"):
        return value.iloc[:, 0].dropna().tolist()
    return value.dropna().tolist()


def _moving_average(values, n):
    if not values:
        return 0
    if len(values) < n:
        return sum(values) / len(values)
    return sum(values[-n:]) / n


def _score_chart(price, ma5, ma20, ma60):
    score = 45
    if price > ma5:
        score += 10
    if price > ma20:
        score += 15
    if price > ma60:
        score += 15
    if ma5 > ma20:
        score += 8
    if ma20 > ma60:
        score += 7
    return max(0, min(100, score))


def _score_volume(volume_ratio):
    if volume_ratio >= 2.0:
        return 90
    if volume_ratio >= 1.5:
        return 80
    if volume_ratio >= 1.1:
        return 70
    if volume_ratio >= 0.8:
        return 60
    return 50


def _score_momentum(change_rate):
    if change_rate >= 5:
        return 85
    if change_rate >= 2:
        return 75
    if change_rate >= 0:
        return 65
    if change_rate >= -2:
        return 55
    return 45


def _score_volatility(close):
    if len(close) < 21:
        return 60

    returns = []
    for i in range(1, len(close)):
        prev, curr = close[i - 1], close[i]
        if prev:
            returns.append((curr - prev) / prev)

    recent = returns[-20:]
    if len(recent) < 5:
        return 60

    avg = sum(recent) / len(recent)
    variance = sum((x - avg) ** 2 for x in recent) / len(recent)
    vol = (variance ** 0.5) * 100

    if vol <= 1.5:
        return 85
    if vol <= 2.5:
        return 75
    if vol <= 4.0:
        return 60
    return 45


def _to_krx_code(ticker):
    return ticker.replace(".KS", "").replace(".KQ", "").strip()


def _empty_price(reason=""):
    return {
        "ticker": "",
        "current_price": 0,
        "change_rate": 0,
        "ma5": 0,
        "ma20": 0,
        "ma60": 0,
        "volume_ratio": 1,
        "distance_from_high": 0,
        "chart_score": 50,
        "volume_score": 50,
        "momentum_score": 50,
        "volatility_score": 50,
        "source": "",
        "error_reason": reason,
        "data_ok": False,
    }
