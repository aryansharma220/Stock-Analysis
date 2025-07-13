import dateutil.relativedelta
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
import dateutil
import datetime
import pandas_ta as pta

# function to plot interactive plotly chart
def interactive_plot(df):
  fig = px.line()
  for i in df.columns[1:]:
    fig.add_scatter(x = df['Date'], y = df[i], name =i)
  fig.update_layout(width=450, margin = dict(l=20,r=20,b=20,t=50), legend= dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
  return fig


# Function to normalize the prices based on the initial price

def normalize(df_2):
  df = df_2.copy()
  for i in df.columns[1:]:
    df[i] = df[i]/df[i][0]
  return df


# Function to calculate daily returns

def daily_returns(df_2):
  df_daily_return = df_2.copy()
  for i in df_2.columns[1:]:
    for j in range(1,len(df_2)):
      df_daily_return.loc[j,i] = ((df_2.loc[j,i]-df_2.loc[j-1,i])/df_2.loc[j-1,i])*100
    df_daily_return.loc[0,i] = 0
  return df_daily_return

# Function to calculate beta

def calculate_beta(stocks_daily_return, stock):
  rm  = stocks_daily_return['sp500'].mean()*252
  
  b,a = np.polyfit(stocks_daily_return['sp500'],stocks_daily_return[stock],1)
  return b,a


def plotly_table(df):
    headerColor = '#1e293b'
    rowOddColor = '#f8fafc'
    rowEvenColor = '#e2e8f0'
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=["<b></b>"]+["<b>"+str(i)+"</b>" for i in df.columns],
            line_color='#475569',
            fill_color=headerColor,
            align='center', 
            font=dict(color='white', size=15, family="Arial"), 
            height=40
        ),
        cells=dict(
            values=[["<b>"+str(i)+"</b>" for i in df.index]]+[df[i] for i in df.columns],
            fill_color = [rowOddColor, rowEvenColor],
            align = ['left'] + ['center'] * len(df.columns), 
            line_color=['#cbd5e1'], 
            font=dict(color='#1e293b', size=14, family="Arial"),
            height=35
        ))
    ])
    fig.update_layout(
        height=400, 
        margin=dict(l=5, r=5, t=5, b=5),
        paper_bgcolor='white',
        font=dict(family="Arial")
    )
    return fig



def filter_data(df, num_period):
  if num_period == '1mo':
    date = df.index[-1] + dateutil.relativedelta.relativedelta(months=-1)
  elif num_period == '5d':
    date = df.index[-1] + dateutil.relativedelta.relativedelta(days=-5)
  elif num_period == '6mo':
    date = df.index[-1] + dateutil.relativedelta.relativedelta(months=-6)
  elif num_period == '1y':
    date = df.index[-1] + dateutil.relativedelta.relativedelta(years=-1)
  elif num_period == '5y':
    date = df.index[-1] + dateutil.relativedelta.relativedelta(years=-5)
  elif num_period == 'ytd':
    date = datetime.datetime(df.index[-1].year, 1, 1).strftime('%Y-%m-%d')
  else:
    date = df.index[0]
    
  return df.reset_index()[df.reset_index()['Date'] > date]

def close_chart(dataframe, num_period=False):
    if num_period:
        dataframe = filter_data(dataframe, num_period)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Open'],
                            mode='lines', name='Open', line=dict(width=2.5, color='#3b82f6'),
                            hovertemplate='<b>Open</b><br>Date: %{x}<br>Price: $%{y:.2f}<extra></extra>'))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Close'],
                            mode='lines', name='Close', line=dict(width=3, color='#1e293b'),
                            hovertemplate='<b>Close</b><br>Date: %{x}<br>Price: $%{y:.2f}<extra></extra>'))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['High'],
                            mode='lines', name='High', line=dict(width=2, color='#10b981'),
                            hovertemplate='<b>High</b><br>Date: %{x}<br>Price: $%{y:.2f}<extra></extra>'))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Low'],
                            mode='lines', name='Low', line=dict(width=2, color='#ef4444'),
                            hovertemplate='<b>Low</b><br>Date: %{x}<br>Price: $%{y:.2f}<extra></extra>'))
    
    fig.update_xaxes(
        rangeslider_visible=True,
        gridcolor='rgba(128,128,128,0.2)',
        title_text="Date",
        title_font_size=14
    )
    fig.update_yaxes(
        gridcolor='rgba(128,128,128,0.2)',
        title_text="Price ($)",
        title_font_size=14
    )
    fig.update_layout(
        height=550, 
        margin=dict(l=10, r=20, t=40, b=10), 
        plot_bgcolor='white', 
        paper_bgcolor='#f8fafc',
        title_text="Stock Price Analysis",
        title_font_size=18,
        title_x=0.5,
        legend=dict(
            yanchor="top",
            xanchor="right",
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="rgba(0,0,0,0.2)",
            borderwidth=1
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Arial"
        )
    )
    
    return fig
  
  
def candlestick(dataframe, num_period):
    dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=dataframe['Date'],
        open=dataframe['Open'], 
        high=dataframe['High'],
        low=dataframe['Low'], 
        close=dataframe['Close'],
        increasing_line_color='#10b981',
        decreasing_line_color='#ef4444',
        increasing_fillcolor='rgba(16, 185, 129, 0.3)',
        decreasing_fillcolor='rgba(239, 68, 68, 0.3)',
        name='OHLC'
    ))
    
    fig.update_xaxes(
        gridcolor='rgba(128,128,128,0.2)',
        title_text="Date",
        title_font_size=14
    )
    fig.update_yaxes(
        gridcolor='rgba(128,128,128,0.2)',
        title_text="Price ($)",
        title_font_size=14
    )
    fig.update_layout(
        showlegend=False, 
        height=550, 
        margin=dict(l=10, r=20, t=40, b=10), 
        plot_bgcolor='white', 
        paper_bgcolor='#f8fafc',
        title_text="Candlestick Chart",
        title_font_size=18,
        title_x=0.5,
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Arial"
        )
    )
    return fig
  

def RSI(dataframe, num_period):
    dataframe['RSI'] = pta.rsi(dataframe['Close'])
    dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    
    # Add RSI line with gradient effect
    fig.add_trace(go.Scatter(
        x=dataframe['Date'],
        y=dataframe.RSI, 
        name='RSI', 
        line=dict(width=3, color='#f59e0b'),
        hovertemplate='<b>RSI</b><br>Date: %{x}<br>Value: %{y:.2f}<extra></extra>'
    ))
    
    # Add overbought line (70)
    fig.add_trace(go.Scatter(
        x=dataframe['Date'],
        y=[70]*len(dataframe), 
        name='Overbought (70)', 
        line=dict(width=2, color='#dc2626', dash='dash'),
        hovertemplate='<b>Overbought Level</b><br>Value: 70<extra></extra>'
    ))
    
    # Add oversold line (30) with fill
    fig.add_trace(go.Scatter(
        x=dataframe['Date'],
        y=[30]*len(dataframe), 
        fill='tonexty', 
        name='Oversold (30)', 
        line=dict(width=2, color='#16a34a', dash='dash'),
        fillcolor='rgba(220, 38, 38, 0.1)',
        hovertemplate='<b>Oversold Level</b><br>Value: 30<extra></extra>'
    ))
    
    # Add neutral zone
    fig.add_shape(
        type="rect",
        x0=dataframe['Date'].iloc[0], x1=dataframe['Date'].iloc[-1],
        y0=30, y1=70,
        fillcolor="rgba(156, 163, 175, 0.1)",
        line=dict(width=0),
        layer="below"
    )
    
    fig.update_xaxes(
        gridcolor='rgba(128,128,128,0.2)',
        title_text="Date",
        title_font_size=12
    )
    fig.update_yaxes(
        gridcolor='rgba(128,128,128,0.2)',
        title_text="RSI Value",
        title_font_size=12
    )
    fig.update_layout(
        yaxis_range=[0, 100],
        height=250, 
        plot_bgcolor='white', 
        paper_bgcolor='#f8fafc', 
        margin=dict(l=10, r=20, t=30, b=10),
        title_text="Relative Strength Index (RSI)",
        title_font_size=16,
        title_x=0.5,
        legend=dict(
            orientation='h',
            yanchor='top',
            y=1.02,
            xanchor='right',
            x=1,
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="rgba(0,0,0,0.2)",
            borderwidth=1
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=11,
            font_family="Arial"
        )
    )
    
    return fig

def Moving_average(dataframe, num_period):
    dataframe['SMA_50'] = pta.sma(dataframe['Close'], 50)
    dataframe['SMA_20'] = pta.sma(dataframe['Close'], 20)
    dataframe = filter_data(dataframe, num_period)
    fig = go.Figure()
    
    # Add price lines with improved styling
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Open'],
                            mode='lines',
                            name='Open', line=dict(width=2, color='#3b82f6'),
                            hovertemplate='<b>Open</b><br>Date: %{x}<br>Price: $%{y:.2f}<extra></extra>'))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Close'],
                            mode='lines',
                            name='Close', line=dict(width=3, color='#1e293b'),
                            hovertemplate='<b>Close</b><br>Date: %{x}<br>Price: $%{y:.2f}<extra></extra>'))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['High'],
                            mode='lines', name='High', line=dict(width=1.5, color='#10b981'),
                            hovertemplate='<b>High</b><br>Date: %{x}<br>Price: $%{y:.2f}<extra></extra>'))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Low'],
                            mode='lines', name='Low', line=dict(width=1.5, color='#ef4444'),
                            hovertemplate='<b>Low</b><br>Date: %{x}<br>Price: $%{y:.2f}<extra></extra>'))
    
    # Add moving averages with enhanced styling
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['SMA_50'],
                            mode='lines', name='SMA 50', line=dict(width=2.5, color='#8b5cf6', dash='dot'),
                            hovertemplate='<b>SMA 50</b><br>Date: %{x}<br>Price: $%{y:.2f}<extra></extra>'))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['SMA_20'],
                            mode='lines', name='SMA 20', line=dict(width=2.5, color='#f59e0b', dash='dashdot'),
                            hovertemplate='<b>SMA 20</b><br>Date: %{x}<br>Price: $%{y:.2f}<extra></extra>'))
    
    fig.update_xaxes(
        rangeslider_visible=True,
        gridcolor='rgba(128,128,128,0.2)',
        title_text="Date",
        title_font_size=14
    )
    fig.update_yaxes(
        gridcolor='rgba(128,128,128,0.2)',
        title_text="Price ($)",
        title_font_size=14
    )
    fig.update_layout(
        height=550, 
        margin=dict(l=10, r=20, t=40, b=10), 
        plot_bgcolor='white', 
        paper_bgcolor='#f8fafc',
        title_text="Stock Price with Moving Averages",
        title_font_size=18,
        title_x=0.5,
        legend=dict(
            yanchor="top",
            xanchor="right",
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="rgba(0,0,0,0.2)",
            borderwidth=1
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Arial"
        )
    )
    
    return fig
  

def MACD(dataframe, num_period):
    macd = pta.macd(dataframe['Close']).iloc[:,0]
    macd_signal = pta.macd(dataframe['Close']).iloc[:,1]
    macd_hist = pta.macd(dataframe['Close']).iloc[:,2]
    dataframe['MACD'] = macd
    dataframe['MACD_Signal'] = macd_signal
    dataframe['MACD_Hist'] = macd_hist
    dataframe = filter_data(dataframe, num_period)
    
    fig = go.Figure()
    
    # Add MACD line
    fig.add_trace(go.Scatter(
        x=dataframe['Date'],
        y=dataframe['MACD'], 
        name='MACD', 
        line=dict(width=2.5, color='#2563eb'),
        hovertemplate='<b>MACD</b><br>Date: %{x}<br>Value: %{y:.4f}<extra></extra>'
    ))
    
    # Add Signal line
    fig.add_trace(go.Scatter(
        x=dataframe['Date'],
        y=dataframe['MACD_Signal'], 
        name='Signal', 
        line=dict(width=2.5, color='#dc2626', dash='dash'),
        hovertemplate='<b>Signal</b><br>Date: %{x}<br>Value: %{y:.4f}<extra></extra>'
    ))
    
    # Add histogram bars with improved colors
    colors = ['#ef4444' if val < 0 else '#10b981' for val in dataframe['MACD_Hist']]
    fig.add_trace(go.Bar(
        x=dataframe['Date'],
        y=dataframe['MACD_Hist'],
        name='Histogram',
        marker_color=colors,
        opacity=0.6,
        hovertemplate='<b>Histogram</b><br>Date: %{x}<br>Value: %{y:.4f}<extra></extra>'
    ))
    
    # Add zero line
    fig.add_hline(y=0, line_dash="dot", line_color="rgba(128,128,128,0.5)", line_width=1)
    
    fig.update_xaxes(
        gridcolor='rgba(128,128,128,0.2)',
        title_text="Date",
        title_font_size=12
    )
    fig.update_yaxes(
        gridcolor='rgba(128,128,128,0.2)',
        title_text="MACD Value",
        title_font_size=12
    )
    fig.update_layout(
        height=250, 
        plot_bgcolor='white', 
        paper_bgcolor='#f8fafc', 
        margin=dict(l=10, r=20, t=30, b=10),
        title_text="MACD (Moving Average Convergence Divergence)",
        title_font_size=16,
        title_x=0.5,
        legend=dict(
            orientation='h',
            yanchor='top',
            y=1.02,
            xanchor='right',
            x=1,
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="rgba(0,0,0,0.2)",
            borderwidth=1
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=11,
            font_family="Arial"
        )
    )
    
    return fig
  
def Moving_average_forecast(forecast):
    fig = go.Figure()
    
    # Historical data
    fig.add_trace(go.Scatter(
        x=forecast.index[-30:], 
        y=forecast['Close'].iloc[-30:],
        mode='lines',
        name='Historical Close Price', 
        line=dict(width=3, color='#1e293b'),
        hovertemplate='<b>Historical</b><br>Date: %{x}<br>Price: $%{y:.2f}<extra></extra>'
    ))
    
    # Future prediction
    fig.add_trace(go.Scatter(
        x=forecast.index[:-31], 
        y=forecast['Close'].iloc[:-31],
        mode='lines', 
        name='Predicted Close Price', 
        line=dict(width=3, color='#dc2626', dash='dot'),
        hovertemplate='<b>Prediction</b><br>Date: %{x}<br>Price: $%{y:.2f}<extra></extra>'
    ))
    
    # Add confidence interval area
    fig.add_shape(
        type="rect",
        x0=forecast.index[:-31][0], x1=forecast.index[:-31][-1],
        y0=forecast['Close'].iloc[:-31].min() * 0.95, 
        y1=forecast['Close'].iloc[:-31].max() * 1.05,
        fillcolor="rgba(220, 38, 38, 0.1)",
        line=dict(width=0),
        layer="below"
    )
    
    fig.update_xaxes(
        rangeslider_visible=False,
        gridcolor='rgba(128,128,128,0.2)',
        title_text="Date",
        title_font_size=14
    )
    fig.update_yaxes(
        gridcolor='rgba(128,128,128,0.2)',
        title_text="Price ($)",
        title_font_size=14
    )
    fig.update_layout(
        height=550, 
        margin=dict(l=10, r=20, t=40, b=10), 
        plot_bgcolor='white', 
        paper_bgcolor='#f8fafc',
        title_text="Stock Price Forecast",
        title_font_size=18,
        title_x=0.5,
        legend=dict(
            yanchor="top",
            xanchor="right",
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="rgba(0,0,0,0.2)",
            borderwidth=1
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Arial"
        )
    )
    
    return fig