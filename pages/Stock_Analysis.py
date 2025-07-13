import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
import datetime as dt
import pandas_ta as pta
from pages.utils.capm_functions import plotly_table, candlestick, close_chart, RSI, MACD, Moving_average

st.set_page_config(
  page_title="Stock Analysis",
  page_icon=":chart_with_upwards_trend:",
  layout="wide",
  initial_sidebar_state="auto",
)

# Custom CSS for Stock Analysis page with dark mode support
st.markdown("""
<style>
    /* CSS Variables for theme adaptation */
    :root {
        --primary-purple: #667eea;
        --secondary-purple: #764ba2;
        --card-bg-light: rgba(255, 255, 255, 0.95);
        --card-bg-dark: rgba(40, 44, 52, 0.95);
        --text-primary-light: #2d3748;
        --text-primary-dark: #e2e8f0;
        --text-secondary-light: #666;
        --text-secondary-dark: #a0aec0;
        --border-light: rgba(0, 0, 0, 0.1);
        --border-dark: rgba(255, 255, 255, 0.1);
        --shadow-light: 0 2px 4px rgba(0, 0, 0, 0.1);
        --shadow-dark: 0 2px 4px rgba(0, 0, 0, 0.3);
        --input-bg-light: #f8f9fa;
        --input-bg-dark: rgba(45, 55, 72, 0.8);
    }
    
    /* Theme detection and variable assignment */
    @media (prefers-color-scheme: dark) {
        :root {
            --card-bg: var(--card-bg-dark);
            --text-primary: var(--text-primary-dark);
            --text-secondary: var(--text-secondary-dark);
            --border: var(--border-dark);
            --shadow: var(--shadow-dark);
            --input-bg: var(--input-bg-dark);
        }
    }
    
    @media (prefers-color-scheme: light) {
        :root {
            --card-bg: var(--card-bg-light);
            --text-primary: var(--text-primary-light);
            --text-secondary: var(--text-secondary-light);
            --border: var(--border-light);
            --shadow: var(--shadow-light);
            --input-bg: var(--input-bg-light);
        }
    }
    
    .stApp[data-theme="dark"] {
        --card-bg: var(--card-bg-dark);
        --text-primary: var(--text-primary-dark);
        --text-secondary: var(--text-secondary-dark);
        --border: var(--border-dark);
        --shadow: var(--shadow-dark);
        --input-bg: var(--input-bg-dark);
    }
    
    .stApp[data-theme="light"] {
        --card-bg: var(--card-bg-light);
        --text-primary: var(--text-primary-light);
        --text-secondary: var(--text-secondary-light);
        --border: var(--border-light);
        --shadow: var(--shadow-light);
        --input-bg: var(--input-bg-light);
    }
    
    .analysis-header {
        background: linear-gradient(135deg, var(--primary-purple) 0%, var(--secondary-purple) 100%);
        padding: 2.5rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .input-container {
        background: var(--input-bg);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        border: 1px solid var(--border);
        box-shadow: var(--shadow);
    }
    
    .metric-card {
        background: var(--card-bg);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: var(--shadow);
        border-left: 4px solid var(--primary-purple);
        margin: 0.5rem 0;
        border: 1px solid var(--border);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.2);
    }
    
    .company-info {
        background: var(--card-bg);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border: 1px solid var(--border);
        box-shadow: var(--shadow);
    }
    
    .chart-controls {
        background: var(--card-bg);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: var(--shadow);
        margin: 1rem 0;
        border: 1px solid var(--border);
    }
    
    .stock-ticker-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 6px 12px rgba(30, 60, 114, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .section-header {
        color: var(--primary-purple);
        border-bottom: 2px solid var(--primary-purple);
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }
    
    .price-change-positive {
        color: #38a169;
        font-weight: bold;
    }
    
    .price-change-negative {
        color: #e53e3e;
        font-weight: bold;
    }
    
    .control-button {
        background: var(--primary-purple);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        margin: 0.25rem;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 500;
    }
    
    .control-button:hover {
        background: var(--secondary-purple);
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(102, 126, 234, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="analysis-header">
    <h1>📊 Stock Analysis Dashboard</h1>
    <p>Comprehensive real-time stock analysis with technical indicators and fundamental metrics</p>
</div>
""", unsafe_allow_html=True)

# Input section with improved styling
st.markdown('<div class="input-container">', unsafe_allow_html=True)
st.markdown("### 🔍 **Stock Selection & Time Range**")

col1, col2, col3 = st.columns(3)

today = dt.date.today()

with col1:
    ticker = st.text_input("📈 Stock Ticker", "AAPL", help="Enter stock symbol (e.g., AAPL, TSLA, GOOGL)")
with col2:
    start_date = st.date_input("📅 Start Date", dt.date(today.year-1, today.month, today.day))
with col3:
    end_date = st.date_input("📅 End Date", dt.date(today.year, today.month, today.day))

st.markdown('</div>', unsafe_allow_html=True)

# Stock header with ticker
st.markdown(f"""
<div style="background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%); 
           padding: 1rem; border-radius: 8px; color: white; text-align: center; margin: 1rem 0;">
    <h2>📈 {ticker.upper()} - Stock Analysis</h2>
</div>
""", unsafe_allow_html=True)

stock = yf.Ticker(ticker)

# Company information with better styling
st.markdown('<div class="company-info">', unsafe_allow_html=True)
st.markdown("### 🏢 **Company Overview**")
st.write(stock.info['longBusinessSummary'])

info_col1, info_col2, info_col3 = st.columns(3)
with info_col1:
    st.markdown(f"**🏭 Sector:** {stock.info['sector']}")
with info_col2:
    st.markdown(f"**🔧 Industry:** {stock.info['industry']}")
with info_col3:
    st.markdown(f"**🌐 Website:** [{stock.info['website']}]({stock.info['website']})")

st.markdown('</div>', unsafe_allow_html=True)

# Financial metrics section
st.markdown("### 📊 **Financial Metrics**")
    
col1, col2 = st.columns(2)

with col1:
  st.markdown("#### 💰 Market Fundamentals")
  df = pd.DataFrame(index=['Market Cap','Previous Close','Open','Day Range','52 Week Range','Volume','Beta','Dividend Yield'])
  
  df[''] = [stock.info['marketCap'], stock.info['previousClose'], stock.info['open'], stock.info['dayHigh'], stock.info['fiftyTwoWeekHigh'], stock.info['volume'], stock.info['beta'], stock.info['dividendYield']]
  fig_df = plotly_table(df)
  
  st.plotly_chart(fig_df, use_container_width=True)
  
with col2:
  st.markdown("#### 📈 Valuation Ratios")
  df = pd.DataFrame(index=['P/E Ratio','Forward P/E','Trailing EPS','Forward EPS','Price/Sales','Price/Book','Current Ratio','Debt/Equity'])
  
  df[''] = [stock.info['trailingPE'],stock.info['forwardPE'],stock.info['trailingEps'],stock.info['forwardEps'],stock.info['priceToSalesTrailing12Months'],stock.info['priceToBook'],stock.info['currentRatio'],stock.info['debtToEquity']]
  fig_df = plotly_table(df)
  
  st.plotly_chart(fig_df, use_container_width=True)

# Price data and metrics
data = yf.download(ticker, start=start_date, end=end_date)

latest_close = float(data['Close'].iloc[-1])
prev_close = float(data['Close'].iloc[-2])
change = latest_close - prev_close

# Current price display with enhanced styling
st.markdown("### 💹 **Current Price Information**")
price_col1, price_col2, price_col3 = st.columns([2, 1, 1])

with price_col1:
    change_color = "🟢" if change >= 0 else "🔴"
    change_text = "+" if change >= 0 else ""
    st.markdown(f"""
    <div class="metric-card">
        <h3>{change_color} {ticker.upper()} Current Price</h3>
        <h2>${round(latest_close, 2)}</h2>
        <p style="color: {'green' if change >= 0 else 'red'};">
            {change_text}{round(change, 2)} ({change_text}{round((change/prev_close)*100, 2)}%)
        </p>
    </div>
    """, unsafe_allow_html=True)

# Historical data table
st.markdown("### 📋 **Recent Trading History**")
last_10_df=data.tail(10).sort_index(ascending=False).round(3)
fig_df = plotly_table(last_10_df)

st.plotly_chart(fig_df, use_container_width=True)

# Time period buttons with better styling
st.markdown("### ⏱️ **Chart Time Periods**")
st.markdown('<div class="chart-controls">', unsafe_allow_html=True)

col1,col2,col3,col4,col5,col6,col7,col8,col9,col10,col11,col12 = st.columns(12)

num_period=''
with col1:
  if st.button('5D', help="5 Days"):
    num_period='5d'
with col2:
  if st.button('1M', help="1 Month"):
    num_period='1mo'

with col3:
  if st.button('6M', help="6 Months"):
    num_period='6mo'
    
with col4:
  if st.button('YTD', help="Year to Date"):
    num_period='ytd'

with col5:
  if st.button('1Y', help="1 Year"):
    num_period='1y'

with col6:
  if st.button('5Y', help="5 Years"):
    num_period='5y'

with col7:
  if st.button('MAX', help="Maximum Range"):
    num_period='max'

st.markdown('</div>', unsafe_allow_html=True)

# Chart controls
st.markdown("### 📊 **Technical Analysis Charts**")
chart_col1, chart_col2, chart_col3 = st.columns([1, 1, 4])

with chart_col1:
  chart_type = st.selectbox('📈 Chart Type', ('Candlestick', 'Line'), help="Choose your preferred chart style")
with chart_col2:
  if chart_type == 'Candlestick':
    indicators = st.selectbox('🔧 Technical Indicators',('RSI', 'MACD'), help="Select technical analysis indicator")
  else:
    indicators = st.selectbox('🔧 Technical Indicators',('RSI', 'MACD', 'Moving Average'), help="Select technical analysis indicator")
    
ticker_ = yf.Ticker(ticker)
new_df1 = ticker_.history(period = 'max')
data1 = ticker_.history(period = 'max')
if num_period =='':
  if chart_type =='Candlestick' and indicators =='RSI':
    st.plotly_chart(candlestick(data1,'1y'), use_container_width=True)
    st.plotly_chart(RSI(data1,'1y'), use_container_width=True)

  if chart_type =='Candlestick' and indicators =='MACD':
    st.plotly_chart(candlestick(data1,'1y'), use_container_width=True)
    st.plotly_chart(MACD(data1,'1y'), use_container_width=True)  
    
  if chart_type =='Line' and indicators =='RSI':
    st.plotly_chart(close_chart(data1,'1y'), use_container_width=True)
    st.plotly_chart(RSI(data1,'1y'), use_container_width=True)
    
  if chart_type =='Line' and indicators =='Moving Average':
    st.plotly_chart(Moving_average(data1,'1y'), use_container_width=True)
    
  if chart_type =='Line' and indicators =='MACD':
    st.plotly_chart(close_chart(data1,'1y'), use_container_width=True)
    st.plotly_chart(MACD(data1,'1y'), use_container_width=True)
    
else:
  
  if chart_type =='Candlestick' and indicators =='RSI':
    st.plotly_chart(candlestick(new_df1,num_period), use_container_width=True)
    st.plotly_chart(RSI(new_df1, num_period), use_container_width=True)
    
  if chart_type =='Candlestick' and indicators =='MACD':
    st.plotly_chart(candlestick(new_df1,num_period), use_container_width=True)
    st.plotly_chart(MACD(new_df1,num_period), use_container_width=True)
    
  if chart_type =='Line' and indicators =='RSI':
    st.plotly_chart(close_chart(new_df1,num_period), use_container_width=True)
    st.plotly_chart(RSI(new_df1,num_period), use_container_width=True)  
    
  if chart_type =='Line' and indicators =='Moving Average':
    st.plotly_chart(Moving_average(new_df1,num_period), use_container_width=True)
    
  if chart_type =='Line' and indicators =='MACD':
    st.plotly_chart(close_chart(new_df1,num_period), use_container_width=True)
    st.plotly_chart(MACD(new_df1,num_period), use_container_width=True)
  
