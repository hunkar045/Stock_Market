import yfinance as yf
import streamlit as st

PERIOD_MAP = {"1 Month": "1mo", "3 Months": "3mo", "6 Months": "6mo", 
              "1 Year": "1y", "2 Years": "2y", "5 Years": "5y"}

@st.cache_data(ttl=600)
def fetch_stock(symbol, period="1 Year"):
    """Fetch stock data with caching"""
    try:
        symbol = symbol.upper()
        stock = yf.Ticker(symbol)
        info = stock.info
        if not info.get('longName'):
            return None, None
        yf_period = PERIOD_MAP.get(period, "1y")
        history = stock.history(period=yf_period)
        return (info, history) if not history.empty else (info, None)
    except Exception:
        return None, None

def get_metrics(info):
    """Calculate and return stock metrics"""
    price = info.get('currentPrice', 0) or 0
    prev_close = info.get('previousClose', 0) or 1
    change = price - prev_close
    change_pct = (change / prev_close * 100) if prev_close else 0
    
    return {
        'name': info.get('longName', 'Unknown Stock'),
        'price': price,
        'change': change,
        'change_pct': change_pct,
        'high': info.get('fiftyTwoWeekHigh', 0) or 0,
        'low': info.get('fiftyTwoWeekLow', 0) or 0,
        'volume': info.get('volume', 0) or 0,
        'sector': info.get('sector', 'N/A'),
        'summary': info.get('longBusinessSummary', '')
    }