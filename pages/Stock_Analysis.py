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

st.title("Stock Analysis")

col1, col2, col3 = st.columns(3)

today = dt.date.today()

with col1:
    ticker = st.text_input("Stock Ticker", "AAPL")
with col2:
    start_date = st.date_input("Choose Start Date", dt.date(today.year-1, today.month, today.day))
with col3:
    end_date = st.date_input("Choose End Date", dt.date(today.year, today.month, today.day))

st.subheader(ticker)

stock = yf.Ticker(ticker)

st.write(stock.info['longBusinessSummary'])
st.write("**Sector:**", stock.info['sector'])
st.write("**Industry:**", stock.info['industry'])
st.write("**Website:**", stock.info['website'])

    
col1, col2 = st.columns(2)

with col1:
  df = pd.DataFrame(index=['Market Cap','Previous Close','Open','Day Range','52 Week Range','Volume','Beta','Dividend Yield'])
  
  df[''] = [stock.info['marketCap'], stock.info['previousClose'], stock.info['open'], stock.info['dayHigh'], stock.info['fiftyTwoWeekHigh'], stock.info['volume'], stock.info['beta'], stock.info['dividendYield']]
  fig_df = plotly_table(df)
  
  st.plotly_chart(fig_df, use_container_width=True)
  
with col2:
  df = pd.DataFrame(index=['P/E Ratio','Forward P/E','Trailing EPS','Forward EPS','Price/Sales','Price/Book','Current Ratio','Debt/Equity'])
  
  df[''] = [stock.info['trailingPE'],stock.info['forwardPE'],stock.info['trailingEps'],stock.info['forwardEps'],stock.info['priceToSalesTrailing12Months'],stock.info['priceToBook'],stock.info['currentRatio'],stock.info['debtToEquity']]
  fig_df = plotly_table(df)
  
  st.plotly_chart(fig_df, use_container_width=True)
  
data = yf.download(ticker, start=start_date, end=end_date)

latest_close = float(data['Close'].iloc[-1])
prev_close = float(data['Close'].iloc[-2])
change = latest_close - prev_close
  
col1,col2,col3 = st.columns(3)

col1.metric(label=f"{ticker} Closing Price", value=round(latest_close, 2), delta=round(change, 2))

last_10_df=data.tail(10).sort_index(ascending=False).round(3)
fig_df = plotly_table(last_10_df)

st.write("##### Historical Data (Last 10 days)")

st.plotly_chart(fig_df, use_container_width=True)

col1,col2,col3,col4,col5,col6,col7,col8,col9,col10,col11,col12 = st.columns(12)

num_period=''
with col1:
  if st.button('5D'):
    num_period='5d'
with col2:
  if st.button('1M'):
    num_period='1mo'

with col3:
  if st.button('6M'):
    num_period='6mo'
    
with col4:
  if st.button('YTD'):
    num_period='ytd'

with col5:
  if st.button('1Y'):
    num_period='1y'

with col6:
  if st.button('5Y'):
    num_period='5y'

with col7:
  if st.button('MAX'):
    num_period='max'

col1, col2, col3 = st.columns([1,1,4])

with col1:
  chart_type = st.selectbox('Select Chart Type', ('Candlestick', 'Line'))
with col2:
  if chart_type == 'Candlestick':
    indicators = st.selectbox('',('RSI', 'MACD'))
  else:
    indicators = st.selectbox('',('RSI', 'MACD', 'Moving Average'))
    
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
  
