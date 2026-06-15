import requests
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta

PERIOD_DAYS = {
    "1 Month": 30, "3 Months": 90, "6 Months": 180,
    "1 Year": 365, "2 Years": 730, "5 Years": 1825
}

HEADERS = {"User-Agent": "Mozilla/5.0"}


@st.cache_data(ttl=600)
def fetch_stock(symbol, period="1 Year"):
    """Fetch stock price history + company info from Yahoo Finance."""
    try:
        symbol = symbol.upper().strip()
        days = PERIOD_DAYS.get(period, 365)

        # --- Step 1: Get price history ---
        now = int(datetime.now().timestamp())
        ago = int((datetime.now() - timedelta(days=days)).timestamp())

        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
        r = requests.get(url, headers=HEADERS, timeout=15,
                         params={"period1": ago, "period2": now, "interval": "1d"})
        r.raise_for_status()

        result = r.json()["chart"]["result"]
        if not result:
            return None, None

        meta = result[0]["meta"]
        quotes = result[0]["indicators"]["quote"][0]
        dates = pd.to_datetime(result[0]["timestamp"], unit="s")

        history = pd.DataFrame({
            "Open": quotes["open"], "High": quotes["high"],
            "Low": quotes["low"], "Close": quotes["close"],
            "Volume": quotes["volume"]
        }, index=dates)
        history.index.name = "Date"
        history.dropna(subset=["Close"], inplace=True)

        if history.empty:
            return None, None

        info = {
            "longName": meta.get("shortName", symbol),
            "currentPrice": meta.get("regularMarketPrice", 0),
            "previousClose": meta.get("chartPreviousClose", 0),
            "fiftyTwoWeekHigh": meta.get("fiftyTwoWeekHigh", 0),
            "fiftyTwoWeekLow": meta.get("fiftyTwoWeekLow", 0),
            "volume": meta.get("regularMarketVolume", 0),
            "sector": "N/A",
            "longBusinessSummary": ""
        }

        return info, history

    except Exception:
        return None, None


def get_metrics(info):
    """Turn raw info dict into display-ready metrics."""
    price = info.get("currentPrice", 0) or 0
    prev = info.get("previousClose", 0) or 1
    change = price - prev

    return {
        "name": info.get("longName", "Unknown"),
        "price": price,
        "change": change,
        "change_pct": (change / prev * 100) if prev else 0,
        "high": info.get("fiftyTwoWeekHigh", 0) or 0,
        "low": info.get("fiftyTwoWeekLow", 0) or 0,
        "volume": info.get("volume", 0) or 0,
        "sector": info.get("sector", "N/A"),
        "summary": info.get("longBusinessSummary", "")
    }