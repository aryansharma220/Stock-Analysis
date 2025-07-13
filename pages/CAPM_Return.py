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

# Custom CSS for CAPM page with dark mode support
st.markdown("""
<style>
    /* CSS Variables for theme adaptation */
    :root {
        --capm-blue: #667eea;
        --capm-purple: #764ba2;
        --success-green: #28a745;
        --warning-yellow: #ffc107;
        --danger-red: #dc3545;
        --info-blue: #17a2b8;
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
        --input-bg-light: rgba(248, 249, 250, 0.8);
        --input-bg-dark: rgba(45, 55, 72, 0.8);
        --formula-bg-light: rgba(232, 245, 232, 0.8);
        --formula-bg-dark: rgba(40, 167, 69, 0.1);
        --results-bg-light: rgba(255, 248, 225, 0.8);
        --results-bg-dark: rgba(255, 193, 7, 0.1);
    }
    
    @media (prefers-color-scheme: dark) {
        :root {
            --card-bg: var(--card-bg-dark);
            --text-primary: var(--text-primary-dark);
            --text-secondary: var(--text-secondary-dark);
            --border: var(--border-dark);
            --shadow: var(--shadow-dark);
            --input-bg: var(--input-bg-dark);
            --formula-bg: var(--formula-bg-dark);
            --results-bg: var(--results-bg-dark);
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
            --formula-bg: var(--formula-bg-light);
            --results-bg: var(--results-bg-light);
        }
    }
    
    .stApp[data-theme="dark"] {
        --card-bg: var(--card-bg-dark);
        --text-primary: var(--text-primary-dark);
        --text-secondary: var(--text-secondary-dark);
        --border: var(--border-dark);
        --shadow: var(--shadow-dark);
        --input-bg: var(--input-bg-dark);
        --formula-bg: var(--formula-bg-dark);
        --results-bg: var(--results-bg-dark);
    }
    
    .stApp[data-theme="light"] {
        --card-bg: var(--card-bg-light);
        --text-primary: var(--text-primary-light);
        --text-secondary: var(--text-secondary-light);
        --border: var(--border-light);
        --shadow: var(--shadow-light);
        --input-bg: var(--input-bg-light);
        --formula-bg: var(--formula-bg-light);
        --results-bg: var(--results-bg-light);
    }
    
    .capm-header {
        background: linear-gradient(135deg, var(--capm-blue) 0%, var(--camp-purple) 100%);
        padding: 2.5rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 12px 24px rgba(102, 126, 234, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .input-section {
        background: var(--input-bg);
        backdrop-filter: blur(15px);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        border: 1px solid var(--border);
        box-shadow: var(--shadow);
    }
    
    .camp-formula {
        background: var(--formula-bg);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid var(--success-green);
        margin: 1rem 0;
        text-align: center;
        border: 1px solid var(--border);
        box-shadow: var(--shadow);
    }
    
    .beta-explanation {
        background: var(--card-bg);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid var(--info-blue);
        margin: 1rem 0;
        border: 1px solid var(--border);
        box-shadow: var(--shadow);
    }
    
    .data-container {
        background: var(--card-bg);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: var(--shadow);
        margin: 1rem 0;
        border: 1px solid var(--border);
    }
    
    .results-section {
        background: var(--results-bg);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 15px;
        border-top: 4px solid var(--warning-yellow);
        margin: 1rem 0;
        border: 1px solid var(--border);
        box-shadow: var(--shadow);
    }
    
    .beta-card {
        background: var(--card-bg);
        backdrop-filter: blur(10px);
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 10px;
        border: 1px solid var(--border);
        box-shadow: var(--shadow);
        transition: all 0.3s ease;
    }
    
    .beta-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(102, 126, 234, 0.15);
    }
    
    .insight-card {
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        transition: all 0.3s ease;
        border: 1px solid var(--border);
        box-shadow: var(--shadow);
        backdrop-filter: blur(10px);
    }
    
    .insight-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
    }
    
    .insight-volatility {
        background: rgba(255, 243, 205, 0.9);
        border-left: 4px solid var(--warning-yellow);
    }
    
    .insight-return {
        background: rgba(212, 237, 218, 0.9);
        border-left: 4px solid var(--success-green);
    }
    
    .insight-stability {
        background: rgba(209, 236, 241, 0.9);
        border-left: 4px solid var(--info-blue);
    }
    
    .risk-disclaimer {
        background: rgba(248, 215, 218, 0.9);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid var(--danger-red);
        margin-top: 2rem;
        border: 1px solid var(--border);
    }
    
    .formula-title {
        color: var(--success-green);
        font-weight: bold;
        margin-bottom: 1rem;
    }
    
    .formula-equation {
        color: var(--success-green);
        font-size: 1.5em;
        font-weight: bold;
        margin: 1rem 0;
    }
    
    .formula-description {
        color: var(--text-primary);
        font-size: 0.9em;
    }
    
    .period-info {
        background: rgba(227, 242, 253, 0.9);
        border-radius: 12px;
        padding: 1rem;
        margin-top: 1rem;
        text-align: center;
        border: 1px solid var(--border);
    }
    
    .period-title {
        color: var(--info-blue);
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .period-value {
        color: var(--info-blue);
        font-size: 1.2em;
        font-weight: bold;
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
    <h3 class="formula-title">📈 CAPM Formula</h3>
    <h2 class="formula-equation">E(R) = Rf + β(E(Rm) - Rf)</h2>
    <p class="formula-description"><strong>E(R)</strong> = Expected Return | <strong>Rf</strong> = Risk-free Rate | <strong>β</strong> = Beta | <strong>E(Rm)</strong> = Expected Market Return</p>
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
    <div class="period-info">
        <h4 class="period-title">📅 Analysis Period</h4>
        <h3 class="period-value">{years} Year{'s' if years > 1 else ''}</h3>
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
    <div class="insight-card insight-volatility">
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
    <div class="insight-card insight-return">
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
    <div class="insight-card insight-stability">
        <h4>🛡️ Most Stable</h4>
        <h3>{lowest_beta_stock}</h3>
        <p>β = {lowest_beta_value:.2f}</p>
        <small>Lowest volatility</small>
    </div>
    """, unsafe_allow_html=True)

# Risk warning
st.markdown("---")
st.markdown("""
<div class="risk-disclaimer">
    <h4>⚠️ Risk Disclaimer</h4>
    <p>CAPM is a theoretical model and actual returns may vary significantly from predictions. 
    Beta calculations are based on historical data and may not reflect future volatility. 
    Always diversify your portfolio and consult with financial advisors.</p>
</div>
""", unsafe_allow_html=True)
  