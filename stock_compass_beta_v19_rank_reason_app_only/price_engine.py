from functools import lru_cache
import yfinance as yf
from stock_universe import get_ticker


def get_price_data(stock_name):
    ticker = get_ticker(stock_name)

    if not ticker:
        return _empty_price()

    return _download_price(ticker)


@lru_cache(maxsize=128)
def _download_price(ticker):
    try:
        data = yf.download(
            ticker,
            period="6mo",
            interval="1d",
            progress=False,
            auto_adjust=True,
            threads=False
        )

        if data is None or data.empty:
            return _empty_price()

        close = _to_series(data["Close"])
        volume = _to_series(data["Volume"])

        if len(close) < 2:
            return _empty_price()

        current_price = float(close.iloc[-1])
        prev_price = float(close.iloc[-2])
        change_rate = ((current_price - prev_price) / prev_price) * 100 if prev_price else 0

        ma5 = float(close.rolling(5).mean().iloc[-1]) if len(close) >= 5 else current_price
        ma20 = float(close.rolling(20).mean().iloc[-1]) if len(close) >= 20 else ma5
        ma60 = float(close.rolling(60).mean().iloc[-1]) if len(close) >= 60 else ma20

        avg_volume20 = float(volume.rolling(20).mean().iloc[-1]) if len(volume) >= 20 else float(volume.mean())
        last_volume = float(volume.iloc[-1])
        volume_ratio = last_volume / avg_volume20 if avg_volume20 else 1

        high_52w = float(close.max())
        distance_from_high = ((current_price - high_52w) / high_52w) * 100 if high_52w else 0

        chart_score = _score_chart(current_price, ma5, ma20, ma60)
        volume_score = _score_volume(volume_ratio)
        momentum_score = _score_momentum(change_rate)
        volatility_score = _score_volatility(close)

        return {
            "ticker": ticker,
            "current_price": round(current_price),
            "change_rate": round(change_rate, 2),
            "ma5": round(ma5),
            "ma20": round(ma20),
            "ma60": round(ma60),
            "volume_ratio": round(volume_ratio, 2),
            "distance_from_high": round(distance_from_high, 2),
            "chart_score": chart_score,
            "volume_score": volume_score,
            "momentum_score": momentum_score,
            "volatility_score": volatility_score,
            "data_ok": True
        }

    except Exception:
        return _empty_price()


def _to_series(value):
    if hasattr(value, "iloc") and len(getattr(value, "shape", [])) == 2:
        return value.iloc[:, 0]
    return value


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
    returns = close.pct_change().dropna()

    if len(returns) < 20:
        return 60

    vol = float(returns.tail(20).std() * 100)

    if vol <= 1.5:
        return 85
    if vol <= 2.5:
        return 75
    if vol <= 4.0:
        return 60
    return 45


def _empty_price():
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
        "data_ok": False
    }
