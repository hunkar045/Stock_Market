import plotly.graph_objects as go

def make_chart(history, symbol, period="1 Year"):
    """Create interactive stock price chart"""
    if history.empty:
        return None
    
    ma20 = history['Close'].rolling(20).mean()
    ma50 = history['Close'].rolling(50).mean()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=history.index, y=history['Close'], name="Price", 
                             line=dict(color='#1f77b4', width=2)))
    fig.add_trace(go.Scatter(x=history.index, y=ma20, name="20-day MA", 
                             line=dict(color='#ff7f0e', width=1, dash='dash')))
    fig.add_trace(go.Scatter(x=history.index, y=ma50, name="50-day MA", 
                             line=dict(color='#2ca02c', width=1, dash='dot')))
    
    fig.update_layout(
        title=f"{symbol} Stock Price ({period})",
        template='plotly_dark',
        height=500,
        hovermode='x unified',
        margin=dict(l=10, r=10, t=40, b=10),
        xaxis_title="Date",
        yaxis_title="Price ($)",
        font=dict(size=11)
    )
    return fig