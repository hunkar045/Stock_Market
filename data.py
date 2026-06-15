import requests
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta

PERIOD_MAP = {"1 Month": 30, "3 Months": 90, "6 Months": 180, 
              "1 Year": 365, "2 Years": 730, "5 Years": 1825}

@st.cache_data(ttl=600)
def fetch_stock(symbol, period="1 Year"):
    """Fetch stock data using yfinance with fallback"""
    try:
        import yfinance as yf
        symbol = symbol.upper()
        stock = yf.Ticker(symbol)
        info = stock.info
        
        if not info.get('longName'):
            return None, None
        
        period_days = PERIOD_MAP.get(period, 365)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=period_days)
        
        history = stock.history(start=start_date, end=end_date)
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