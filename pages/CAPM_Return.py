import streamlit as st
import pandas as pd
import yfinance as yf
import datetime
import pandas_datareader as web
import pages.utils.capm_functions as capm_functions

st.set_page_config(
  page_title="CAPM",
  page_icon=":chart_with_upwards_trend:",
  layout="wide",
  initial_sidebar_state="auto",
)

st.title("Capital Asset Pricing Model (CAPM)")

# getting user input

col1,col2=st.columns(2)

with col1:
    stocks_list =st.multiselect("Choose 4 stocks",('TSLA','AAPL','NFLX','MSFT','MGM','AMZN','NVDA','GOOGL'),default=['TSLA','AAPL','NFLX','MSFT'])
with col2:
    years=st.number_input("Number of years",min_value=1,max_value=10,value=5)

# downloading data 

today = datetime.date.today()
start = datetime.date(today.year - years, today.month, today.day)
end = today
stocks_df = pd.DataFrame()
sp500 = pd.DataFrame()


try:
  sp500 = web.DataReader(['sp500'],'fred', start, end)

  
  # print(sp500.head())
except Exception as e:
  st.error(f"Error fetching S&P 500 data: {e}")

for stock in stocks_list:
  data = yf.download(stock, period=f"{years}y")
  # print(data.head())
  stocks_df[f'{stock}']=data['Close']
  
  # print(stocks_df.head())

stocks_df.reset_index(inplace=True)
sp500.reset_index(inplace=True)
sp500.rename(columns={'DATE':'Date'},inplace=True)

# print(stocks_df.dtypes)
# print(sp500.dtypes)

stocks_df = pd.merge(stocks_df, sp500, how='inner', on='Date')

# print(stock_df.head())

col1, col2 = st.columns(2)

with col1:
  st.markdown("### Dataframe head")
  st.dataframe(stocks_df.head(), use_container_width=True)
with col2:
  st.markdown("### Dataframe tail")
  st.dataframe(stocks_df.tail(), use_container_width=True)
  
  
col1, col2 = st.columns(2)

with col1:
  st.markdown("### Price of all the stocks")
  st.plotly_chart(capm_functions.interactive_plot(stocks_df))
with col2:
  # print(capm_functions.normalize(stock_df))
  st.markdown("### Price of all the stocks (After Normalization)")
  st.plotly_chart(capm_functions.interactive_plot(capm_functions.normalize(stocks_df)))
  
  
stocks_daily_return = capm_functions.daily_returns(stocks_df)

# print(stocks_daily_return.head())


beta={}
alpha={}

for i in stocks_daily_return.columns:
  if i!='Date' and i!='sp500':
    b,a = capm_functions.calculate_beta(stocks_daily_return,i)
    beta[i]=b
    alpha[i]=a
    
# print(beta)
# print(alpha)

beta_df = pd.DataFrame(columns=['Stock', 'Beta Value'])
beta_df['Stock'] = beta.keys()
beta_df['Beta Value'] = [str(round(i,2)) for i in beta.values()]

col1, col2 = st.columns(2)

with col1:
  st.markdown('### Calculated Beta Value')
  st.dataframe(beta_df, use_container_width=True)

rf=0
rm = stocks_daily_return['sp500'].mean()*252

return_df = pd.DataFrame()
return_value =[]

for stock, value in beta.items():
  return_value.append(str(round(rf+(value*(rm-rf)),2)))
return_df['Stock'] = stocks_list

return_df['Return Value'] = return_value

with col2:
  st.markdown('### Calculated Return using CAPM')
  st.dataframe(return_df, use_container_width=True)
  