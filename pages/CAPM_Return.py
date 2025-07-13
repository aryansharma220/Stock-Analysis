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

# Custom CSS for CAPM page
st.markdown("""
<style>
    .capm-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
    }
    
    .input-section {
        background: linear-gradient(145deg, #f8f9fa, #e9ecef);
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        border: 1px solid #dee2e6;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
    }
    
    .capm-formula {
        background: linear-gradient(135deg, #e8f5e8, #d4edda);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #28a745;
        margin: 1rem 0;
        text-align: center;
    }
    
    .beta-explanation {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #17a2b8;
        margin: 1rem 0;
    }
    
    .data-container {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
    
    .results-section {
        background: linear-gradient(145deg, #fff8e1, #ffecb3);
        padding: 1.5rem;
        border-radius: 10px;
        border-top: 4px solid #ffc107;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="capm-header">
    <h1>💰 Capital Asset Pricing Model (CAPM)</h1>
    <p>Advanced portfolio analysis and risk-return optimization</p>
    <p><em>Analyze systematic risk and expected returns using modern portfolio theory</em></p>
</div>
""", unsafe_allow_html=True)

# CAPM Formula explanation
st.markdown("""
<div class="capm-formula">
    <h3>📈 CAPM Formula</h3>
    <h2 style="color: #28a745;">E(R) = Rf + β(E(Rm) - Rf)</h2>
    <p><strong>E(R)</strong> = Expected Return | <strong>Rf</strong> = Risk-free Rate | <strong>β</strong> = Beta | <strong>E(Rm)</strong> = Expected Market Return</p>
</div>
""", unsafe_allow_html=True)

# Input section
st.markdown('<div class="input-section">', unsafe_allow_html=True)
st.markdown("### 🎯 **Portfolio Configuration**")

col1,col2=st.columns(2)

with col1:
    st.markdown("#### 📊 **Select Stocks for Analysis**")
    stocks_list =st.multiselect(
        "Choose up to 4 stocks",
        ('TSLA','AAPL','NFLX','MSFT','MGM','AMZN','NVDA','GOOGL'),
        default=['TSLA','AAPL','NFLX','MSFT'],
        help="Select 2-4 stocks for comprehensive CAPM analysis"
    )
with col2:
    st.markdown("#### ⏱️ **Analysis Time Period**")
    years=st.number_input(
        "Number of years", 
        min_value=1, 
        max_value=10, 
        value=5,
        help="Historical data period for beta calculation"
    )
    
    # Display selected period info
    st.markdown(f"""
    <div style="text-align: center; padding: 1rem; background: #e3f2fd; border-radius: 8px; margin-top: 1rem;">
        <h4 style="color: #1976d2;">📅 Analysis Period</h4>
        <h3 style="color: #1976d2;">{years} Year{'s' if years > 1 else ''}</h3>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Beta explanation
st.markdown("""
<div class="beta-explanation">
    <h4>📚 Understanding Beta (β)</h4>
    <div style="display: flex; justify-content: space-around; text-align: center;">
        <div>
            <h3 style="color: #dc3545;">β > 1</h3>
            <p>More volatile than market</p>
        </div>
        <div>
            <h3 style="color: #ffc107;">β = 1</h3>
            <p>Moves with market</p>
        </div>
        <div>
            <h3 style="color: #28a745;">β < 1</h3>
            <p>Less volatile than market</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Data processing section
st.markdown("### 📊 **Data Processing & Analysis**")

with st.spinner('🔄 Fetching market data and calculating metrics...'):
    # downloading data 
    today = datetime.date.today()
    start = datetime.date(today.year - years, today.month, today.day)
    end = today
    stocks_df = pd.DataFrame()
    sp500 = pd.DataFrame()

    try:
      sp500 = web.DataReader(['sp500'],'fred', start, end)
    except Exception as e:
      st.error(f"❌ Error fetching S&P 500 data: {e}")

    for stock in stocks_list:
      data = yf.download(stock, period=f"{years}y")
      stocks_df[f'{stock}']=data['Close']

    stocks_df.reset_index(inplace=True)
    sp500.reset_index(inplace=True)
    sp500.rename(columns={'DATE':'Date'},inplace=True)

    stocks_df = pd.merge(stocks_df, sp500, how='inner', on='Date')

# Data display section
st.markdown('<div class="data-container">', unsafe_allow_html=True)
st.markdown("### 📋 **Historical Price Data**")

col1, col2 = st.columns(2)

with col1:
  st.markdown("#### 🔝 **Latest Data (Head)**")
  st.dataframe(stocks_df.head(), use_container_width=True)
with col2:
  st.markdown("#### 🔚 **Recent Data (Tail)**")
  st.dataframe(stocks_df.tail(), use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Visualization section
st.markdown("### 📈 **Price Trend Analysis**")

col1, col2 = st.columns(2)

with col1:
  st.markdown("#### 💹 **Absolute Price Movements**")
  st.plotly_chart(capm_functions.interactive_plot(stocks_df), use_container_width=True)
with col2:
  st.markdown("#### 📊 **Normalized Price Comparison**")
  st.plotly_chart(capm_functions.interactive_plot(capm_functions.normalize(stocks_df)), use_container_width=True)

# Calculate metrics
stocks_daily_return = capm_functions.daily_returns(stocks_df)

beta={}
alpha={}

for i in stocks_daily_return.columns:
  if i!='Date' and i!='sp500':
    b,a = capm_functions.calculate_beta(stocks_daily_return,i)
    beta[i]=b
    alpha[i]=a

beta_df = pd.DataFrame(columns=['Stock', 'Beta Value'])
beta_df['Stock'] = beta.keys()
beta_df['Beta Value'] = [str(round(i,2)) for i in beta.values()]

# Results section
st.markdown('<div class="results-section">', unsafe_allow_html=True)
st.markdown("### 🎯 **CAPM Analysis Results**")

col1, col2 = st.columns(2)

with col1:
  st.markdown('#### 📊 **Beta Coefficients**')
  st.markdown("*Systematic risk relative to market*")
  
  # Enhanced beta display
  for stock, beta_val in zip(beta_df['Stock'], beta_df['Beta Value']):
    beta_float = float(beta_val)
    if beta_float > 1:
        risk_level = "🔴 High Risk"
        color = "#dc3545"
    elif beta_float < 1:
        risk_level = "🟢 Low Risk"
        color = "#28a745"
    else:
        risk_level = "🟡 Market Risk"
        color = "#ffc107"
    
    st.markdown(f"""
    <div style="background: white; padding: 1rem; margin: 0.5rem 0; border-radius: 8px; border-left: 4px solid {color};">
        <strong>{stock}</strong>: β = {beta_val} | {risk_level}
    </div>
    """, unsafe_allow_html=True)

rf=0
rm = stocks_daily_return['sp500'].mean()*252

return_df = pd.DataFrame()
return_value =[]

for stock, value in beta.items():
  return_value.append(str(round(rf+(value*(rm-rf)),2)))
return_df['Stock'] = stocks_list
return_df['Return Value'] = return_value

with col2:
  st.markdown('#### 💰 **Expected Returns (CAPM)**')
  st.markdown("*Theoretical returns based on risk*")
  
  # Enhanced return display
  for stock, return_val in zip(return_df['Stock'], return_df['Return Value']):
    return_float = float(return_val)
    if return_float > 15:
        perf_level = "🚀 High Return"
        color = "#28a745"
    elif return_float > 10:
        perf_level = "📈 Good Return"
        color = "#17a2b8"
    else:
        perf_level = "📊 Moderate Return"
        color = "#ffc107"
    
    st.markdown(f"""
    <div style="background: white; padding: 1rem; margin: 0.5rem 0; border-radius: 8px; border-left: 4px solid {color};">
        <strong>{stock}</strong>: {return_val}% | {perf_level}
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Summary insights
st.markdown("### 💡 **Investment Insights**")

insights_col1, insights_col2, insights_col3 = st.columns(3)

with insights_col1:
    highest_beta_stock = max(beta, key=beta.get)
    highest_beta_value = beta[highest_beta_stock]
    st.markdown(f"""
    <div style="background: #fff3cd; padding: 1rem; border-radius: 8px; text-align: center;">
        <h4>⚡ Highest Beta</h4>
        <h3>{highest_beta_stock}</h3>
        <p>β = {highest_beta_value:.2f}</p>
        <small>Most volatile stock</small>
    </div>
    """, unsafe_allow_html=True)

with insights_col2:
    highest_return_idx = return_df['Return Value'].astype(float).idxmax()
    highest_return_stock = return_df.iloc[highest_return_idx]['Stock']
    highest_return_value = return_df.iloc[highest_return_idx]['Return Value']
    st.markdown(f"""
    <div style="background: #d4edda; padding: 1rem; border-radius: 8px; text-align: center;">
        <h4>💰 Highest Expected Return</h4>
        <h3>{highest_return_stock}</h3>
        <p>{highest_return_value}%</p>
        <small>Best risk-adjusted return</small>
    </div>
    """, unsafe_allow_html=True)

with insights_col3:
    lowest_beta_stock = min(beta, key=beta.get)
    lowest_beta_value = beta[lowest_beta_stock]
    st.markdown(f"""
    <div style="background: #d1ecf1; padding: 1rem; border-radius: 8px; text-align: center;">
        <h4>🛡️ Most Stable</h4>
        <h3>{lowest_beta_stock}</h3>
        <p>β = {lowest_beta_value:.2f}</p>
        <small>Lowest volatility</small>
    </div>
    """, unsafe_allow_html=True)

# Risk warning
st.markdown("---")
st.markdown("""
<div style="background: #f8d7da; padding: 1rem; border-radius: 8px; border-left: 4px solid #dc3545;">
    <h4>⚠️ Risk Disclaimer</h4>
    <p>CAPM is a theoretical model and actual returns may vary significantly from predictions. 
    Beta calculations are based on historical data and may not reflect future volatility. 
    Always diversify your portfolio and consult with financial advisors.</p>
</div>
""", unsafe_allow_html=True)
  