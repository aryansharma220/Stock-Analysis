import streamlit as st
from pages.utils.model import evaluate_model, get_forecast, get_data, get_differencing_order, get_rolling_mean, scaling, inverse_scaling
import pandas as pd
from pages.utils.capm_functions import plotly_table, Moving_average_forecast

st.set_page_config(
    page_title="Stock Prediction",
    page_icon="📈",
    layout="wide",
)

# Custom CSS for Stock Prediction page with dark mode support
st.markdown("""
<style>
    /* CSS Variables for theme adaptation */
    :root {
        --prediction-gradient-1: #ff9a9e;
        --prediction-gradient-2: #fecfef;
        --ai-blue: #667eea;
        --ai-purple: #764ba2;
        --success-green: #38a169;
        --warning-orange: #ed8936;
        --error-red: #e53e3e;
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
        --input-bg-light: rgba(247, 250, 252, 0.8);
        --input-bg-dark: rgba(45, 55, 72, 0.8);
        --metrics-bg-light: rgba(230, 255, 250, 0.8);
        --metrics-bg-dark: rgba(56, 178, 172, 0.1);
    }
    
    @media (prefers-color-scheme: dark) {
        :root {
            --card-bg: var(--card-bg-dark);
            --text-primary: var(--text-primary-dark);
            --text-secondary: var(--text-secondary-dark);
            --border: var(--border-dark);
            --shadow: var(--shadow-dark);
            --input-bg: var(--input-bg-dark);
            --metrics-bg: var(--metrics-bg-dark);
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
            --metrics-bg: var(--metrics-bg-light);
        }
    }
    
    .stApp[data-theme="dark"] {
        --card-bg: var(--card-bg-dark);
        --text-primary: var(--text-primary-dark);
        --text-secondary: var(--text-secondary-dark);
        --border: var(--border-dark);
        --shadow: var(--shadow-dark);
        --input-bg: var(--input-bg-dark);
        --metrics-bg: var(--metrics-bg-dark);
    }
    
    .stApp[data-theme="light"] {
        --card-bg: var(--card-bg-light);
        --text-primary: var(--text-primary-light);
        --text-secondary: var(--text-secondary-light);
        --border: var(--border-light);
        --shadow: var(--shadow-light);
        --input-bg: var(--input-bg-light);
        --metrics-bg: var(--metrics-bg-light);
    }
    
    .prediction-header {
        background: linear-gradient(135deg, var(--prediction-gradient-1) 0%, var(--prediction-gradient-2) 50%, var(--prediction-gradient-2) 100%);
        padding: 2.5rem;
        border-radius: 20px;
        text-align: center;
        color: var(--text-primary-light);
        margin-bottom: 2rem;
        box-shadow: 0 12px 24px rgba(255, 154, 158, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .prediction-input {
        background: var(--input-bg);
        backdrop-filter: blur(15px);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        border: 1px solid var(--border);
        box-shadow: var(--shadow);
    }
    
    .model-metrics {
        background: var(--metrics-bg);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 5px solid var(--success-green);
        border: 1px solid var(--border);
        box-shadow: var(--shadow);
    }
    
    .forecast-info {
        background: var(--card-bg);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: var(--shadow);
        border-top: 4px solid var(--ai-blue);
        margin: 1rem 0;
        border: 1px solid var(--border);
    }
    
    .ai-badge {
        background: linear-gradient(90deg, var(--ai-blue) 0%, var(--ai-purple) 100%);
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 25px;
        font-weight: bold;
        display: inline-block;
        margin: 0.5rem 0;
        box-shadow: 0 4px 8px rgba(102, 126, 234, 0.3);
    }
    
    .prediction-stats {
        background: var(--card-bg);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid var(--success-green);
        margin: 1rem 0;
        border: 1px solid var(--border);
        box-shadow: var(--shadow);
    }
    
    .metric-container {
        text-align: center;
        padding: 1rem;
        background: var(--card-bg);
        border-radius: 12px;
        margin: 0.5rem;
        border: 1px solid var(--border);
        box-shadow: var(--shadow);
        transition: all 0.3s ease;
    }
    
    .metric-container:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.15);
    }
    
    .metric-title {
        color: var(--text-primary);
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-size: 1.8em;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    
    .metric-description {
        color: var(--text-secondary);
        font-size: 0.9em;
    }
    
    .rmse-value {
        color: var(--error-red);
    }
    
    .accuracy-value {
        color: var(--success-green);
    }
    
    .order-value {
        color: var(--ai-blue);
    }
    
    .disclaimer-box {
        background: rgba(255, 243, 205, 0.9);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid var(--warning-orange);
        margin-top: 2rem;
        border: 1px solid var(--border);
    }
    
    .disclaimer-title {
        color: var(--warning-orange);
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .disclaimer-text {
        color: var(--text-primary);
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="prediction-header">
    <h1>🔮 AI-Powered Stock Prediction</h1>
    <p>Advanced time series forecasting using ARIMA models and machine learning algorithms</p>
    <div class="ai-badge">🤖 Powered by Advanced Analytics</div>
</div>
""", unsafe_allow_html=True)

# Input section
st.markdown('<div class="prediction-input">', unsafe_allow_html=True)
st.markdown("### 🎯 **Stock Selection for Prediction**")

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    ticker = st.text_input("📈 Enter Stock Ticker", "AAPL", help="Enter the stock symbol you want to predict (e.g., AAPL, TSLA, MSFT)")

with col2:
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <h4>📅 Forecast Period</h4>
        <h2 style="color: #667eea;">30 Days</h2>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <h4>🔄 Model Type</h4>
        <h3 style="color: #667eea;">ARIMA</h3>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

rsme = 0

# Prediction header
st.markdown(f"""
<div class="forecast-info">
    <h2>🚀 Generating Predictions for: <span style="color: #667eea;">{ticker.upper()}</span></h2>
    <p>📊 Analyzing historical data and applying time series modeling for accurate forecasting</p>
</div>
""", unsafe_allow_html=True)

# Show processing steps
with st.spinner('🔄 Processing data and training model...'):
    close_price = get_data(ticker)
    rolling_price = get_rolling_mean(close_price)

    differencing_order = get_differencing_order(rolling_price)
    scaled_data, scaler = scaling(rolling_price)
    rmse = evaluate_model(scaled_data, differencing_order)

# Model performance metrics
st.markdown('<div class="model-metrics">', unsafe_allow_html=True)
st.markdown("### 📈 **Model Performance Metrics**")

metric_col1, metric_col2, metric_col3 = st.columns(3)

with metric_col1:
    st.markdown(f"""
    <div class="metric-container">
        <h3 class="metric-title">🎯 RMSE Score</h3>
        <h2 class="metric-value rmse-value">{rmse}</h2>
        <p class="metric-description">Root Mean Square Error</p>
    </div>
    """, unsafe_allow_html=True)

with metric_col2:
    accuracy = max(0, min(100, (1 - rmse/100) * 100))
    st.markdown(f"""
    <div class="metric-container">
        <h3 class="metric-title">✅ Model Accuracy</h3>
        <h2 class="metric-value accuracy-value">{accuracy:.1f}%</h2>
        <p class="metric-description">Prediction Confidence</p>
    </div>
    """, unsafe_allow_html=True)

with metric_col3:
    st.markdown(f"""
    <div class="metric-container">
        <h3 class="metric-title">🔢 Differencing Order</h3>
        <h2 class="metric-value order-value">{differencing_order}</h2>
        <p class="metric-description">Stationarity Level</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Generate forecast
forecast = get_forecast(scaled_data, differencing_order)
# Inverse scale forecasted values
forecast['Close'] = inverse_scaling(scaler, forecast['Close'])
# Prepare a DataFrame for plotting: combine historical and forecast
historical = rolling_price.copy()
if isinstance(historical, pd.Series):
    historical = historical.to_frame(name='Close')
else:
    historical.columns = ['Close']
historical['Type'] = 'Historical'
forecast_plot = forecast.copy()
forecast_plot['Type'] = 'Forecast'
full_plot = pd.concat([historical, forecast_plot])

# Forecast data table
st.markdown("### 📋 **30-Day Price Forecast**")
st.markdown("*Predicted closing prices for the next 30 trading days*")
fig_tail = plotly_table(forecast.sort_index(ascending=False).round(3))
fig_tail.update_layout(height=220)
st.plotly_chart(fig_tail, use_container_width=True)

# Plot historical and forecasted prices together
st.markdown("### 📊 **Interactive Forecast Visualization**")
st.markdown("*Historical price data combined with 30-day AI predictions*")

import plotly.graph_objects as go
fig = go.Figure()

# Enhanced chart styling
fig.add_trace(go.Scatter(
    x=historical.index, 
    y=historical['Close'], 
    mode='lines', 
    name='📈 Historical Prices', 
    line=dict(color='#1f77b4', width=2),
    hovertemplate='<b>Historical</b><br>Date: %{x}<br>Price: $%{y:.2f}<extra></extra>'
))

fig.add_trace(go.Scatter(
    x=forecast.index, 
    y=forecast['Close'], 
    mode='lines', 
    name='🔮 AI Forecast', 
    line=dict(color='#ff7f0e', width=3, dash='dash'),
    hovertemplate='<b>Prediction</b><br>Date: %{x}<br>Price: $%{y:.2f}<extra></extra>'
))

fig.update_layout(
    title=f"📊 {ticker.upper()} Stock Price Analysis & 30-Day Forecast",
    xaxis_title="📅 Date",
    yaxis_title="💰 Close Price ($)",
    legend=dict(yanchor="top", xanchor="right", x=0.99, y=0.99),
    height=600,
    hovermode='x unified',
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(128,128,128,0.2)'
    ),
    yaxis=dict(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(128,128,128,0.2)'
    )
)

st.plotly_chart(fig, use_container_width=True)

# Key insights section
st.markdown("### 💡 **Key Insights & Recommendations**")

insights_col1, insights_col2 = st.columns(2)

with insights_col1:
    # Calculate trend direction
    trend_direction = "📈 Upward" if forecast['Close'].iloc[-1] > forecast['Close'].iloc[0] else "📉 Downward"
    price_change = forecast['Close'].iloc[-1] - forecast['Close'].iloc[0]
    price_change_pct = (price_change / forecast['Close'].iloc[0]) * 100
    
    st.markdown(f"""
    <div class="prediction-stats">
        <h4>📊 Forecast Summary</h4>
        <p><strong>Trend Direction:</strong> {trend_direction}</p>
        <p><strong>30-Day Price Change:</strong> ${price_change:.2f} ({price_change_pct:+.2f}%)</p>
        <p><strong>Current Price:</strong> ${historical['Close'].iloc[-1]:.2f}</p>
        <p><strong>Predicted Price (30 days):</strong> ${forecast['Close'].iloc[-1]:.2f}</p>
    </div>
    """, unsafe_allow_html=True)

with insights_col2:
    volatility = forecast['Close'].std()
    risk_level = "🟢 Low" if volatility < 5 else "🟡 Medium" if volatility < 15 else "🔴 High"
    
    st.markdown(f"""
    <div class="prediction-stats">
        <h4>⚠️ Risk Assessment</h4>
        <p><strong>Volatility:</strong> ${volatility:.2f}</p>
        <p><strong>Risk Level:</strong> {risk_level}</p>
        <p><strong>Model Confidence:</strong> {accuracy:.1f}%</p>
        <p><strong>Recommendation:</strong> {'✅ Consider' if accuracy > 70 else '⚠️ Caution advised'}</p>
    </div>
    """, unsafe_allow_html=True)

# Disclaimer
st.markdown("---")
st.markdown("""
<div class="disclaimer-box">
    <h4 class="disclaimer-title">⚠️ Investment Disclaimer</h4>
    <p class="disclaimer-text">This prediction is for educational purposes only and should not be considered as financial advice. 
    Stock market predictions are inherently uncertain and actual results may vary significantly. 
    Always conduct your own research and consult with financial professionals before making investment decisions.</p>
</div>
""", unsafe_allow_html=True)