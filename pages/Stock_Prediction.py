import streamlit as st
from pages.utils.model import evaluate_model, get_forecast, get_data, get_differencing_order, get_rolling_mean, scaling, inverse_scaling
import pandas as pd
from pages.utils.capm_functions import plotly_table, Moving_average_forecast

st.set_page_config(
    page_title="Stock Prediction",
    page_icon="📈",
    layout="wide",
)

# Custom CSS for Stock Prediction page
st.markdown("""
<style>
    .prediction-header {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        color: #2d3748;
        margin-bottom: 2rem;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
    }
    
    .prediction-input {
        background: linear-gradient(145deg, #f7fafc, #edf2f7);
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    
    .model-metrics {
        background: linear-gradient(145deg, #e6fffa, #b2f5ea);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid #38b2ac;
    }
    
    .forecast-info {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-top: 4px solid #667eea;
        margin: 1rem 0;
    }
    
    .ai-badge {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        margin: 0.5rem 0;
    }
    
    .prediction-stats {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
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
    <div style="text-align: center;">
        <h3>🎯 RMSE Score</h3>
        <h2 style="color: #e53e3e;">{rmse}</h2>
        <p>Root Mean Square Error</p>
    </div>
    """, unsafe_allow_html=True)

with metric_col2:
    accuracy = max(0, min(100, (1 - rmse/100) * 100))
    st.markdown(f"""
    <div style="text-align: center;">
        <h3>✅ Model Accuracy</h3>
        <h2 style="color: #38a169;">{accuracy:.1f}%</h2>
        <p>Prediction Confidence</p>
    </div>
    """, unsafe_allow_html=True)

with metric_col3:
    st.markdown(f"""
    <div style="text-align: center;">
        <h3>🔢 Differencing Order</h3>
        <h2 style="color: #3182ce;">{differencing_order}</h2>
        <p>Stationarity Level</p>
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
<div style="background: #fff3cd; padding: 1rem; border-radius: 8px; border-left: 4px solid #ffc107;">
    <h4>⚠️ Investment Disclaimer</h4>
    <p>This prediction is for educational purposes only and should not be considered as financial advice. 
    Stock market predictions are inherently uncertain and actual results may vary significantly. 
    Always conduct your own research and consult with financial professionals before making investment decisions.</p>
</div>
""", unsafe_allow_html=True)