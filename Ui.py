import streamlit as st

def show_metrics(m):
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Current Price", f"${m['price']:.2f}")
    col2.metric("Daily Change", f"${m['change']:.2f}", f"{m['change_pct']:.2f}%")
    col3.metric("52-Week High", f"${m['high']:.2f}")
    col4.metric("52-Week Low", f"${m['low']:.2f}")

def show_info(m):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 📊 Trading Info")
        st.write(f"**Volume:** {m['volume']:,}" if m['volume'] else "N/A")
        st.write(f"**Sector:** {m['sector']}")
    with col2:
        st.markdown("### 🏢 Company")
        summary = m['summary'][:200] + "..." if len(m['summary']) > 200 else m['summary']
        st.write(summary if summary else "No information available")
    with col3:
        st.markdown("### 💡 Key Stats")
        st.write(f"**High:** ${m['high']:.2f}")
        st.write(f"**Low:** ${m['low']:.2f}")

def show_data(history, symbol):
    st.subheader("📊 Historical Data")
    st.dataframe(history[['Open', 'High', 'Low', 'Close', 'Volume']].tail(20),
                 use_container_width=True)
    st.download_button("📥 Download as CSV", history.to_csv(), 
                       f"{symbol}_data.csv", "text/csv")

def sidebar():
    with st.sidebar:
        st.header("🔍 Search")
        symbol = st.text_input("Enter Stock Symbol", "TSLA", max_chars=5).upper().strip()
        period = st.selectbox("Select Time Period", 
                              ["1 Month", "3 Months", "6 Months", "1 Year", "2 Years", "5 Years"],
                              index=3)
        if st.button("🔎 Search", use_container_width=True, type="primary"):
            st.rerun()
        st.divider()
        st.markdown("### 💡 Quick Examples")
        for example in ["AAPL = Apple", "MSFT = Microsoft", "GOOGL = Google", "TSLA = Tesla", "AMZN = Amazon"]:
            st.write(f"• {example}")
        return symbol, period