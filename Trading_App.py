import streamlit as st

st.set_page_config(
  page_title="Trading App",
  page_icon=":chart_with_upwards_trend:",
  layout="wide",
  initial_sidebar_state="auto",
)

# Custom CSS for adaptive dark/light mode styling
st.markdown("""
<style>
    /* CSS Variables for theme adaptation */
    :root {
        --primary-blue: #1e3c72;
        --secondary-blue: #2a5298;
        --accent-purple: #667eea;
        --accent-purple-light: #764ba2;
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
    }
    
    /* Detect dark mode */
    @media (prefers-color-scheme: dark) {
        :root {
            --card-bg: var(--card-bg-dark);
            --text-primary: var(--text-primary-dark);
            --text-secondary: var(--text-secondary-dark);
            --border: var(--border-dark);
            --shadow: var(--shadow-dark);
            --stats-bg: rgba(40, 44, 52, 0.8);
        }
    }
    
    @media (prefers-color-scheme: light) {
        :root {
            --card-bg: var(--card-bg-light);
            --text-primary: var(--text-primary-light);
            --text-secondary: var(--text-secondary-light);
            --border: var(--border-light);
            --shadow: var(--shadow-light);
            --stats-bg: rgba(248, 249, 250, 0.9);
        }
    }
    
    /* Streamlit dark theme override */
    .stApp[data-theme="dark"] {
        --card-bg: var(--card-bg-dark);
        --text-primary: var(--text-primary-dark);
        --text-secondary: var(--text-secondary-dark);
        --border: var(--border-dark);
        --shadow: var(--shadow-dark);
        --stats-bg: rgba(40, 44, 52, 0.8);
    }
    
    .stApp[data-theme="light"] {
        --card-bg: var(--card-bg-light);
        --text-primary: var(--text-primary-light);
        --text-secondary: var(--text-secondary-light);
        --border: var(--border-light);
        --shadow: var(--shadow-light);
        --stats-bg: rgba(248, 249, 250, 0.9);
    }
    
    .main-header {
        background: linear-gradient(90deg, var(--primary-blue) 0%, var(--secondary-blue) 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .service-card {
        background: var(--card-bg);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid var(--accent-purple);
        margin: 1rem 0;
        box-shadow: var(--shadow);
        transition: all 0.3s ease;
        border: 1px solid var(--border);
    }
    
    .service-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.15);
        border-left-color: var(--accent-purple-light);
    }
    
    .service-title {
        color: var(--accent-purple);
        font-size: 1.3em;
        font-weight: bold;
        margin-bottom: 0.5rem;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    }
    
    .service-description {
        color: var(--text-secondary);
        line-height: 1.6;
        font-size: 0.95em;
    }
    
    .feature-highlight {
        background: linear-gradient(135deg, var(--accent-purple) 0%, var(--accent-purple-light) 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin: 1.5rem 0;
        box-shadow: 0 6px 12px rgba(102, 126, 234, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .stats-container {
        background: var(--stats-bg);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border: 1px solid var(--border);
        box-shadow: var(--shadow);
    }
    
    .feature-icon-container {
        background: var(--card-bg);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
        border: 1px solid var(--border);
        box-shadow: var(--shadow);
    }
    
    .feature-icon-container:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(102, 126, 234, 0.15);
    }
    
    .feature-icon {
        font-size: 2.5em;
        margin-bottom: 0.5rem;
        filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
    }
    
    .feature-title {
        color: var(--text-primary);
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .feature-desc {
        color: var(--text-secondary);
        font-size: 0.9em;
    }
    
    .stats-title {
        color: var(--accent-purple);
        text-align: center;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .stats-item {
        text-align: center;
        padding: 0.5rem;
    }
    
    .stats-number {
        color: var(--accent-purple);
        font-weight: bold;
        font-size: 1.5em;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    }
    
    .stats-label {
        color: var(--text-secondary);
        font-size: 0.9em;
    }
    
    .footer-content {
        text-align: center;
        color: var(--text-secondary);
        padding: 1.5rem;
        background: var(--card-bg);
        border-radius: 8px;
        margin-top: 2rem;
        border: 1px solid var(--border);
    }
    
    .divider {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--border), transparent);
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Main header with gradient background
st.markdown("""
<div class="main-header">
    <h1>📈 Trading Guide App</h1>
    <h3>Your Complete Financial Analysis Platform</h3>
    <p>Empowering investors with advanced analytics, real-time data, and predictive insights</p>
</div>
""", unsafe_allow_html=True)

# Feature highlight
st.markdown("""
<div class="feature-highlight">
    <h4>🚀 Advanced Stock Analysis & Portfolio Management</h4>
    <p>Combine technical analysis, fundamental metrics, and quantitative models for smarter investment decisions</p>
</div>
""", unsafe_allow_html=True)

st.markdown("## 🛠️ Our Comprehensive Services")

# Create columns for better layout
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="service-card">
        <div class="service-title">📊 Stock Information & Analysis</div>
        <div class="service-description">
            Access comprehensive stock data including real-time prices, company fundamentals, technical indicators, and detailed financial metrics. Get insights into market cap, P/E ratios, trading volumes, and more.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="service-card">
        <div class="service-title">🔮 Advanced Stock Prediction</div>
        <div class="service-description">
            Leverage cutting-edge ARIMA time series models to forecast stock prices for the next 30 days. Our models use historical data, rolling averages, and statistical analysis to provide reliable predictions with accuracy metrics.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="service-card">
        <div class="service-title">💰 CAPM Return Analysis</div>
        <div class="service-description">
            Discover how the Capital Asset Pricing Model (CAPM) calculates expected returns based on systematic risk. Compare multiple stocks against market benchmarks and understand risk-return relationships.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="service-card">
        <div class="service-title">📈 Beta Coefficient Calculator</div>
        <div class="service-description">
            Calculate Beta coefficients and expected returns for individual stocks. Understand volatility relative to market movements and make informed decisions about portfolio risk management.
        </div>
    </div>
    """, unsafe_allow_html=True)

# Key features section
st.markdown('<hr class="divider">', unsafe_allow_html=True)

st.markdown("## ✨ Key Features")

feat_col1, feat_col2, feat_col3, feat_col4 = st.columns(4)

with feat_col1:
    st.markdown("""
    <div class="feature-icon-container">
        <div class="feature-icon">🔄</div>
        <h4 class="feature-title">Real-time Data</h4>
        <p class="feature-desc">Live market data and instant updates</p>
    </div>
    """, unsafe_allow_html=True)

with feat_col2:
    st.markdown("""
    <div class="feature-icon-container">
        <div class="feature-icon">📊</div>
        <h4 class="feature-title">Interactive Charts</h4>
        <p class="feature-desc">Dynamic visualizations with Plotly</p>
    </div>
    """, unsafe_allow_html=True)

with feat_col3:
    st.markdown("""
    <div class="feature-icon-container">
        <div class="feature-icon">🤖</div>
        <h4 class="feature-title">AI Predictions</h4>
        <p class="feature-desc">Machine learning forecasting models</p>
    </div>
    """, unsafe_allow_html=True)

with feat_col4:
    st.markdown("""
    <div class="feature-icon-container">
        <div class="feature-icon">📈</div>
        <h4 class="feature-title">Risk Analysis</h4>
        <p class="feature-desc">CAPM and beta calculations</p>
    </div>
    """, unsafe_allow_html=True)

# Quick stats
st.markdown("""
<div class="stats-container">
    <h4 class="stats-title">Platform Statistics</h4>
    <div style="display: flex; justify-content: space-around; flex-wrap: wrap;">
        <div class="stats-item">
            <h3 class="stats-number">500+</h3>
            <p class="stats-label">Supported Stocks</p>
        </div>
        <div class="stats-item">
            <h3 class="stats-number">4</h3>
            <p class="stats-label">Analysis Tools</p>
        </div>
        <div class="stats-item">
            <h3 class="stats-number">30 Days</h3>
            <p class="stats-label">Prediction Range</p>
        </div>
        <div class="stats-item">
            <h3 class="stats-number">Real-time</h3>
            <p class="stats-label">Data Updates</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown("""
<div class="footer-content">
    <p>🔒 Secure • 📱 Responsive • 🚀 Fast • 📊 Accurate</p>
    <p style="font-size: 0.9em; margin-top: 0.5rem;">Built with Streamlit • Powered by yFinance & Advanced Analytics</p>
</div>
""", unsafe_allow_html=True)