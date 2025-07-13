import streamlit as st

st.set_page_config(
  page_title="Trading App",
  page_icon=":chart_with_upwards_trend:",
  layout="wide",
  initial_sidebar_state="auto",
)

st.title("Trading Guide App :bar_chart:")

st.header("We provide the best platform for you to collect all information prior to investing in stocks.")

st.markdown("## We provide the following services")

st.markdown("#### :one: Stock Information")
st.write("Through this page, you can see all the information about stocks that you are interested in.")

st.markdown("#### :two: Stock Prediction")
st.write("You can explore predicted closing prices for the next 15 days based on the historical stock data and advanced forecasting models. Use this tool to gain valuable insights into market trends and make informed investment decisions.")

st.markdown("#### :three: CAPM Return")
st.write("Discover how the Capital Asset Pricing Model (CAPM) calculates the expected return of different stocks asset based on its risk and market performance.")

st.markdown("#### :four: CAPM Beta")
st.write("Calculates Beta and Expected return for individual stocks.")