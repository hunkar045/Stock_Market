# 📈 Stock Market Dashboard

A real-time stock market dashboard built with **Streamlit** and **Yahoo Finance API**.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.40-red?logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green)

## ✨ Features

- 🔍 Search any stock by ticker symbol (AAPL, TSLA, MSFT, etc.)
- 📊 Interactive price charts with 20-day & 50-day moving averages
- 💰 Live metrics — price, daily change, 52-week high/low, volume
- 🏢 Company info and sector details
- 📥 Download historical data as CSV
- ⏱️ Configurable time periods (1 month to 5 years)
- ⚡ Cached API calls for fast performance

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Streamlit | Web UI framework |
| Plotly | Interactive charts |
| Pandas | Data processing |
| Requests | Yahoo Finance API calls |

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

Opens at `http://localhost:8501`

## 📁 Project Structure

```
Stock_Market/
├── app.py              # Main entry point
├── data.py             # Fetches stock data from Yahoo Finance API
├── Chart.py            # Plotly chart generation
├── Ui.py               # Streamlit UI components
├── requirements.txt    # Python dependencies
└── .streamlit/
    └── config.toml     # Streamlit theme & server config
```

## 🌐 Deploy on Replit

1. Import this repo on [replit.com](https://replit.com)
2. Set the **Run** command to: `streamlit run app.py`
3. Click **▶ Run** — Replit installs packages automatically

## 📸 Usage

1. Enter a stock symbol in the sidebar (e.g. `AAPL`)
2. Pick a time period
3. View **Overview** → **Charts** → **Data** tabs
4. Download CSV from the Data tab