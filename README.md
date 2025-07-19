# 📈 Time Series CAPM Analysis & Stock Trading Platform

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.46.1-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Stars](https://img.shields.io/github/stars/aryansharma220/Time_Series_Stocks?style=social)](https://github.com/aryansharma220/Time_Series_Stocks)

> **A comprehensive financial analysis platform combining Capital Asset Pricing Model (CAPM) calculations with advanced time series forecasting and interactive stock analysis tools.**

## 🚀 Features

### 📊 **Stock Analysis Dashboard**

- **Real-time Stock Information**: Get comprehensive stock data including market cap, previous close, open price, and trading volumes
- **Interactive Charts**: Candlestick charts, moving averages, and volume analysis
- **Technical Indicators**: RSI, MACD, Bollinger Bands, and other key technical analysis tools
- **Company Fundamentals**: Sector analysis, industry information, and business summaries

### 🔮 **Advanced Stock Prediction**

- **Time Series Forecasting**: 30-day price predictions using ARIMA models
- **Rolling Mean Analysis**: Smoothed price trends for better forecasting accuracy
- **Model Validation**: RMSE scoring for prediction reliability
- **Stationarity Testing**: Automatic differencing to ensure model accuracy

### 💰 **CAPM Analysis Suite**

- **Beta Calculation**: Measure stock volatility relative to market
- **Expected Return**: Calculate theoretical returns based on risk-free rate and market premium
- **Portfolio Analysis**: Multi-stock CAPM analysis with S&P 500 benchmarking
- **Risk Assessment**: Comprehensive risk-return profiling

### 📈 **Interactive Visualizations**

- **Plotly Integration**: Dynamic, interactive charts and graphs
- **Comparative Analysis**: Side-by-side stock comparisons
- **Historical Trends**: Multi-year data visualization
- **Normalized Price Charts**: Compare stocks on equal footing

## 🛠️ Technology Stack

| Category | Technologies |
|----------|-------------|
| **Frontend** | Streamlit, Plotly, HTML/CSS |
| **Data Analysis** | Pandas, NumPy, SciPy |
| **Machine Learning** | Scikit-learn, Statsmodels |
| **Financial Data** | yFinance, pandas-datareader |
| **Technical Analysis** | pandas_ta |
| **Time Series** | ARIMA, Statistical Models |

## 📋 Prerequisites

- Python 3.8 or higher
- pip package manager
- Internet connection for real-time data fetching

## ⚡ Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/aryansharma220/Time_Series_Stocks.git
cd Time_Series_CAPM_Analysis
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv capm-env
capm-env\Scripts\activate

# macOS/Linux
python3 -m venv capm-env
source capm-env/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Launch the Application

```bash
streamlit run Trading_App.py
```

### 5. Access the Platform

Open your browser and navigate to `http://localhost:8501`

## 📁 Project Structure

```text
Time_Series_CAPM_Analysis/
├── 📄 Trading_App.py              # Main Streamlit application
├── 📁 pages/                      # Multi-page application structure
│   ├── 📈 Stock_Analysis.py       # Stock analysis dashboard
│   ├── 🔮 Stock_Prediction.py     # Time series forecasting
│   ├── 💰 CAPM_Return.py          # CAPM calculations
│   └── 📁 utils/                  # Utility functions
│       ├── 🔧 capm_functions.py   # CAPM and plotting utilities
│       ├── 🤖 model.py            # Time series models
│       └── 📦 __init__.py         # Package initialization
├── 📋 requirements.txt            # Python dependencies
├── 📖 Documentation.docx          # Project documentation
├── 📝 SOURCES.txt                 # Data sources reference
└── 🚫 .gitignore                  # Git ignore rules
```

## 🎯 Usage Guide

### Stock Analysis

1. **Enter Stock Ticker**: Input any valid stock symbol (e.g., AAPL, TSLA, GOOGL)
2. **Select Date Range**: Choose your analysis timeframe
3. **View Metrics**: Analyze key financial indicators and company information
4. **Technical Analysis**: Examine RSI, MACD, and moving averages

### Stock Prediction

1. **Input Ticker Symbol**: Enter the stock you want to predict
2. **Model Training**: The system automatically trains an ARIMA model
3. **View Predictions**: Get 30-day price forecasts with confidence intervals
4. **Model Performance**: Check RMSE scores for prediction accuracy

### CAPM Analysis

1. **Select Stocks**: Choose up to 4 stocks for analysis
2. **Set Time Period**: Define the analysis timeframe (1-10 years)
3. **Calculate Beta**: View each stock's beta coefficient
4. **Expected Returns**: See CAPM-calculated expected returns
5. **Risk Comparison**: Compare risk-return profiles across stocks

## 📊 Key Metrics Explained

### Beta (β)

- **β > 1**: Stock is more volatile than the market
- **β = 1**: Stock moves with the market
- **β < 1**: Stock is less volatile than the market

### Expected Return (CAPM)

```text
E(R) = Rf + β(E(Rm) - Rf)
```

Where:

- `E(R)` = Expected return
- `Rf` = Risk-free rate
- `β` = Beta coefficient
- `E(Rm)` = Expected market return

### Technical Indicators

- **RSI**: Momentum oscillator (14-day period)
- **MACD**: Moving Average Convergence Divergence
- **Moving Averages**: 20, 50, and 200-day trends

## 🔧 Configuration

### Custom Stock Lists

Modify the stock selection in `CAPM_Return.py`:

```python
stocks_list = st.multiselect(
    "Choose 4 stocks",
    ('TSLA','AAPL','NFLX','MSFT','MGM','AMZN','NVDA','GOOGL'),
    default=['TSLA','AAPL','NFLX','MSFT']
)
```

### Prediction Parameters

Adjust forecasting parameters in `model.py`:

```python
# Modify forecast horizon
forecast_days = 30  # Change to desired number of days

# Adjust rolling window
rolling_window = 7  # Change window size for smoothing
```

## 🚨 Troubleshooting

### Common Issues

#### 1. Data Fetching Errors

```bash
# Check internet connection
# Verify stock ticker symbols
# Ensure yfinance is properly installed
pip install --upgrade yfinance
```

#### 2. Module Import Errors

```bash
# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

#### 3. Streamlit Port Conflicts

```bash
# Use different port
streamlit run Trading_App.py --server.port 8502
```

### Performance Optimization

- **Large Datasets**: Consider reducing date ranges for faster loading
- **Multiple Stocks**: CAPM analysis works best with 2-4 stocks
- **Real-time Data**: API calls may have rate limits

## 📈 Sample Analysis Results

### AAPL Stock Analysis (Example)

- **Current Price**: $185.64
- **Beta**: 1.24 (24% more volatile than market)
- **Expected Return (CAPM)**: 12.3%
- **30-day Prediction**: Upward trend with 15% confidence interval

### Portfolio CAPM Analysis

| Stock | Beta | Expected Return | Risk Level |
|-------|------|----------------|------------|
| AAPL  | 1.24 | 12.3%          | Moderate   |
| TSLA  | 2.15 | 18.7%          | High       |
| MSFT  | 0.89 | 10.1%          | Low        |
| GOOGL | 1.07 | 11.4%          | Moderate   |

---

## 🙏 Acknowledgments

- **yFinance**: Real-time financial data
- **Streamlit**: Web application framework
- **Plotly**: Interactive visualizations
- **Statsmodels**: Statistical analysis tools
- **Federal Reserve Economic Data (FRED)**: S&P 500 benchmark data

---

<div align="center">

**⭐ Star this repository if you find it helpful!**

[![GitHub followers](https://img.shields.io/github/followers/aryansharma220?style=social)](https://github.com/aryansharma220)

*Built with ❤️ for the financial analysis community*

</div>
