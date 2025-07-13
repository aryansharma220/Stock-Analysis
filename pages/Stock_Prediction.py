import streamlit as st
from pages.utils.model import evaluate_model, get_forecast, get_data, get_differencing_order, get_rolling_mean, scaling, inverse_scaling
import pandas as pd
from pages.utils.capm_functions import plotly_table, Moving_average_forecast

st.set_page_config(
    page_title="Stock Prediction",
    page_icon="📈",
    layout="wide",
)

st.title("Stock Prediction")

col1, col2, col3 = st.columns(3)

with col1:
    ticker = st.text_input("Stock Ticker", "AAPL")

rsme = 0

st.subheader(f"Predicting Next 30 days Close Price for: {ticker}")

close_price = get_data(ticker)
rolling_price = get_rolling_mean(close_price)

differencing_order = get_differencing_order(rolling_price)
scaled_data, scaler = scaling(rolling_price)
rmse = evaluate_model(scaled_data, differencing_order)

st.write(f"**Model RMSE Score:** {rmse}")

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

st.write("**Forecast Data (Next 30 days):**")
fig_tail = plotly_table(forecast.sort_index(ascending=False).round(3))
fig_tail.update_layout(height=220)
st.plotly_chart(fig_tail, use_container_width=True)

# Plot historical and forecasted prices together
import plotly.graph_objects as go
fig = go.Figure()
fig.add_trace(go.Scatter(x=historical.index, y=historical['Close'], mode='lines', name='Historical', line=dict(color='blue')))
fig.add_trace(go.Scatter(x=forecast.index, y=forecast['Close'], mode='lines', name='Forecast', line=dict(color='red', dash='dash')))
fig.update_layout(title=f"{ticker} Close Price: Historical & Next 30 Days Forecast", xaxis_title="Date", yaxis_title="Close Price", legend=dict(yanchor="top", xanchor="right"), height=500)
st.plotly_chart(fig, use_container_width=True)