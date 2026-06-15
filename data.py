import requests
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta

PERIOD_MAP = {"1 Month": 30, "3 Months": 90, "6 Months": 180, 
              "1 Year": 365, "2 Years": 730, "5 Years": 1825}

# Free Alpha Vantage API Key
API_KEY = "demo"  # Replace with your own key from alphavantage.co

@st.cache_data(ttl=600)
def fetch_stock(symbol, period="1 Year"):
    """Fetch stock data from Alpha Vantage API"""
    try:
        symbol = symbol.upper()
        
        # Fetch intraday data
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}&outputsize=full"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        if "Error Message" in data or "Time Series (Daily)" not in data:
            return None, None
        
        # Parse time series data
        time_series = data["Time Series (Daily)"]
        dates = sorted(time_series.keys())
        
        # Filter by period
        period_days = PERIOD_MAP.get(period, 365)
        cutoff_date = datetime.now() - timedelta(days=period_days)
        
        filtered_data = {
            date: values for date, values in time_series.items()
            if datetime.strptime(date, "%Y-%m-%d") >= cutoff_date
        }
        
        if not filtered_data:
            return None, None
        
        # Create DataFrame
        df = pd.DataFrame.from_dict(
            filtered_data, orient="index",
            columns=["Open", "High", "Low", "Close", "Volume"]
        ).astype(float)
        df.index = pd.to_datetime(df.index)
        df = df.sort_index()
        
        # Get current price info
        latest_date = sorted(time_series.keys())[0]
        latest = time_series[latest_date]
        
        info = {
            'longName': f"{symbol} Stock",
            'currentPrice': float(latest['Close']),
            'previousClose': float(latest['Close']),
            'fiftyTwoWeekHigh': float(max([v['High'] for v in time_series.values()])),
            'fiftyTwoWeekLow': float(min([v['Low'] for v in time_series.values()])),
            'volume': int(latest['Volume']),
            'sector': 'N/A'
        }
        
        return info, df
        
    except Exception as e:
        st.warning(f"Error: {str(e)}")
        return None, None

def get_metrics(info):
    """Calculate stock metrics"""
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