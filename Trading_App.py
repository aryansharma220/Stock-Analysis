import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime as dt

st.set_page_config(
    page_title="Trading Guide App",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="auto",
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .service-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
        transition: transform 0.3s ease;
    }
    
    .service-card:hover {
        transform: translateY(-5px);
    }
    
    .feature-highlight {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 1px solid #e1e8ed;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .footer-info {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        margin-top: 2rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Main Header
st.markdown("""
<div class="main-header">
    <h1>🚀 Advanced Trading Guide Platform</h1>
    <h3>Your Complete Financial Analysis & Investment Decision Hub</h3>
    <p>Empowering traders with professional-grade tools and insights</p>
</div>
""", unsafe_allow_html=True)

# Welcome section with metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
        <h2>📊</h2>
        <h4>Real-time Analysis</h4>
        <p>Live market data</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <h2>🤖</h2>
        <h4>AI Predictions</h4>
        <p>15-day forecasts</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <h2>📈</h2>
        <h4>CAPM Models</h4>
        <p>Risk assessment</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <h2>⚡</h2>
        <h4>Fast Execution</h4>
        <p>Instant results</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Services Section
st.markdown("## 🎯 Our Professional Services")

# Service 1: Stock Analysis
st.markdown("""
<div class="service-card">
    <h3>📊 Comprehensive Stock Analysis</h3>
    <p><strong>What you get:</strong></p>
    <ul>
        <li>📈 Interactive candlestick and line charts</li>
        <li>📉 Technical indicators (RSI, MACD, Moving Averages)</li>
        <li>💰 Real-time stock information and key metrics</li>
        <li>📋 Financial ratios and company fundamentals</li>
        <li>🎨 Professional-grade visualizations</li>
    </ul>
    <p><em>Perfect for technical analysis and fundamental research</em></p>
</div>
""", unsafe_allow_html=True)

# Service 2: Predictions
st.markdown("""
<div class="service-card">
    <h3>🔮 Advanced Stock Prediction</h3>
    <p><strong>AI-Powered Forecasting:</strong></p>
    <ul>
        <li>🤖 Machine learning-based price predictions</li>
        <li>📅 15-day forward-looking forecasts</li>
        <li>📊 Historical pattern analysis</li>
        <li>⚠️ Risk assessment and confidence intervals</li>
        <li>📈 Trend identification and momentum analysis</li>
    </ul>
    <p><em>Make informed decisions with data-driven insights</em></p>
</div>
""", unsafe_allow_html=True)

# Service 3: CAPM Return
st.markdown("""
<div class="service-card">
    <h3>💼 CAPM Return Analysis</h3>
    <p><strong>Portfolio Risk Management:</strong></p>
    <ul>
        <li>📊 Capital Asset Pricing Model calculations</li>
        <li>⚖️ Risk vs. return optimization</li>
        <li>📈 Expected return computations</li>
        <li>🎯 Market performance benchmarking</li>
        <li>📋 Portfolio diversification insights</li>
    </ul>
    <p><em>Understand your investments' risk-adjusted returns</em></p>
</div>
""", unsafe_allow_html=True)

# Service 4: Beta Analysis
st.markdown("""
<div class="service-card">
    <h3>🎯 Beta & Risk Analytics</h3>
    <p><strong>Individual Stock Risk Assessment:</strong></p>
    <ul>
        <li>📊 Beta coefficient calculations</li>
        <li>📈 Market correlation analysis</li>
        <li>⚡ Volatility measurements</li>
        <li>🎯 Expected return estimations</li>
        <li>📋 Risk categorization and scoring</li>
    </ul>
    <p><em>Quantify market risk for better portfolio management</em></p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Feature Highlights
st.markdown("## ✨ Key Features & Benefits")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="feature-highlight">
        <h4>🎨 Professional Visualizations</h4>
        <ul>
            <li>Interactive charts with zoom and pan</li>
            <li>Multiple timeframe analysis</li>
            <li>Customizable technical indicators</li>
            <li>Export-ready professional charts</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-highlight">
        <h4>⚡ Real-time Data</h4>
        <ul>
            <li>Live market data integration</li>
            <li>Instant calculations and updates</li>
            <li>Historical data spanning years</li>
            <li>Multiple stock exchanges support</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-highlight">
        <h4>🔬 Advanced Analytics</h4>
        <ul>
            <li>Machine learning predictions</li>
            <li>Statistical risk models</li>
            <li>Portfolio optimization tools</li>
            <li>Correlation analysis</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-highlight">
        <h4>👤 User-Friendly Interface</h4>
        <ul>
            <li>Intuitive navigation and controls</li>
            <li>Responsive design for all devices</li>
            <li>Educational tooltips and guides</li>
            <li>Beginner to professional modes</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Sample chart to showcase capabilities
st.markdown("## 📊 Sample Analysis Preview")

# Create a sample chart to demonstrate capabilities
fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=('Stock Price Movement', 'Volume Analysis', 'RSI Indicator', 'Portfolio Performance'),
    specs=[[{"secondary_y": False}, {"secondary_y": False}],
           [{"secondary_y": False}, {"secondary_y": False}]]
)

# Sample data
import numpy as np
dates = [dt.date.today() - dt.timedelta(days=x) for x in range(30, 0, -1)]
prices = 100 + np.cumsum(np.random.randn(30) * 2)
volume = np.random.randint(1000000, 5000000, 30)
rsi = 30 + np.random.randn(30) * 20

# Add sample traces
fig.add_trace(go.Scatter(x=dates, y=prices, name='Stock Price', line=dict(color='#667eea', width=3)), row=1, col=1)
fig.add_trace(go.Bar(x=dates, y=volume, name='Volume', marker_color='rgba(102, 126, 234, 0.6)'), row=1, col=2)
fig.add_trace(go.Scatter(x=dates, y=rsi, name='RSI', line=dict(color='#f093fb', width=2)), row=2, col=1)
fig.add_trace(go.Scatter(x=dates, y=np.cumsum(np.random.randn(30)), name='Portfolio Returns', 
                        line=dict(color='#4ecdc4', width=3)), row=2, col=2)

fig.update_layout(
    height=500,
    showlegend=False,
    title_text="Interactive Financial Analysis Dashboard Preview",
    title_x=0.5,
    plot_bgcolor='white',
    paper_bgcolor='white'
)

st.plotly_chart(fig, use_container_width=True)

# Getting Started Section
st.markdown("---")
st.markdown("## 🚀 Get Started")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### Step 1: Choose Analysis Type
    - Select from Stock Analysis, Predictions, or CAPM
    - Each tool is designed for specific insights
    """)

with col2:
    st.markdown("""
    ### Step 2: Input Your Data
    - Enter stock ticker symbols
    - Select date ranges and parameters
    - Customize your analysis settings
    """)

with col3:
    st.markdown("""
    ### Step 3: Analyze & Decide
    - Review generated charts and metrics
    - Export results for further analysis
    - Make informed investment decisions
    """)

# Footer
st.markdown("""
<div class="footer-info">
    <h4>💡 Ready to Start Your Financial Analysis Journey?</h4>
    <p>Navigate to any of our specialized tools using the sidebar menu</p>
    <p><em>Professional trading tools made accessible for everyone</em></p>
    <br>
    <p style="font-size: 0.9em; color: #666;">
        📧 Built with Streamlit & Python | 🔄 Real-time Data | 📊 Professional Analytics
    </p>
</div>
""", unsafe_allow_html=True)