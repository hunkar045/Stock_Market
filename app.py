import streamlit as st
from data import fetch_stock, get_metrics
from Chart import make_chart
from Ui import show_metrics, show_info, show_data, sidebar

st.set_page_config(page_title="Stock Dashboard", page_icon="📈", layout="wide")

def main():
    st.title("📈 Stock Market Dashboard")
    
    symbol, period = sidebar()
    
    with st.spinner("📊 Loading stock data..."):
        info, history = fetch_stock(symbol, period)
    
    if not info:
        st.error(f"❌ Stock not found: {symbol}")
        st.info("Use ticker symbol (e.g., AAPL, MSFT, GOOGL)")
        return
    
    metrics = get_metrics(info)
    
    tab1, tab2, tab3 = st.tabs(["📊 Overview", "📈 Charts", "📋 Data"])
    
    with tab1:
        st.subheader(metrics['name'])
        show_metrics(metrics)
        st.divider()
        show_info(metrics)
    
    with tab2:
        if history is not None:
            st.plotly_chart(make_chart(history, symbol, period), use_container_width=True)
        else:
            st.warning("No chart data available")
    
    with tab3:
        if history is not None:
            show_data(history, symbol)
        else:
            st.warning("No data available")

if __name__ == "__main__":
    main()